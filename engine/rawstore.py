"""Сховище сирих відповідей примірника: `instances/<домен>/raw/`.

Навіщо. Без сховища `refresh` завантажує сторінку, одразу пропускає її крізь читач і
зберігає лише готовий текст: сирого HTML не лишається ніде, і будь-яка правка читача
означає повторне завантаження всього джерела — в Oracle Cloud це дві години пауз між
зверненнями. Зі сховищем кожна відповідь лягає на диск такою, як прийшла, а крок
`build` збирає тексти з неї наново, без мережі, за хвилини.

Увімкнене за замовчуванням у кожного примірника з config.json; `"raw_store": false` вимикає,
і тоді кроки поводяться до байта так само, як до появи сховища. Зібрані раніше примірники
заводять сховище з першим же оновленням. Між оновленнями сховище, як і тексти корпусу, лежить
в архіві примірника: серверу воно не потрібне.

Як лежить. Один файл на адресу: `raw/<хост>/<ключ>.gz`. Ключ — сума адреси й заголовка
Accept: та сама адреса з «Accept: text/markdown» — інша відповідь. Усередині стиснутого
файла перший рядок — JSON з адресою, днем і часом отримання та валідаторами сервера
(ETag, Last-Modified), далі — тіло байт у байт. Запис — через тимчасовий файл із
перейменуванням, тож обірваний прогін не лишає півфайла.

Стара версія не видаляється. Коли сервер віддав інше тіло, ніж лежить у сховищі, або
сторінки більше немає (404, 410), попередній файл переїжджає в
`raw/_old/<день прогону>/<хост>/` і разом зі сховищем іде в архів примірника.

Відповідь 404 чи 410 теж записується — позначкою без тіла: частина читачів пробує кілька
адрес і на 404 бере наступну (README пакета, якого в найперших збірках не було). Без
позначки крок build не відрізнив би «сторінки немає» від «не завантажували» і впав би там,
де мережевий прогін ішов далі.

У git сховище не йде (`instances/*/raw/` у .gitignore): це чужі сторінки, як і корпус.
"""

import gzip
import hashlib
import json
import os
import pathlib
import re
import time
import urllib.parse

DIR = "raw"
OLD = "_old"
# Сторінки більше немає нагорі — це не збій зв'язку, а відповідь.
GONE = ("збій: HTTP 404", "збій: HTTP 410")


def of(instance_dir: pathlib.Path, stamp: str) -> "Store | None":
    """Сховище примірника; None — коли його вимкнено (`"raw_store": false`) або теки
    без config.json, яка примірником не є (так виглядають тимчасові примірники smoke)."""
    path = instance_dir / "config.json"
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8")).get("raw_store", True)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"{path}: не читається ({exc})")
    if not isinstance(value, bool):
        raise SystemExit(f"{path}: поле raw_store мусить бути true або false, а не {value!r}")
    return Store(instance_dir / DIR, stamp) if value else None


def _host(url: str) -> str:
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return re.sub(r"[^a-z0-9.-]", "_", host) or "_"


def _key(url: str, accept: str) -> str:
    return hashlib.sha256(f"{url}\n{accept}".encode("utf-8")).hexdigest()[:32]


class Store:
    def __init__(self, root: pathlib.Path, stamp: str):
        self.root = root
        self.stamp = stamp

    def path(self, url: str, accept: str = "") -> pathlib.Path:
        return self.root / _host(url) / f"{_key(url, accept)}.gz"

    def _read(self, url: str, accept: str, whole: bool) -> tuple[dict, bytes] | None:
        try:
            with gzip.open(self.path(url, accept), "rb") as f:
                meta = json.loads(f.readline())
                data = f.read() if whole else b""
        except (OSError, EOFError, ValueError):
            return None
        if not isinstance(meta, dict) or meta.get("url") != url \
                or meta.get("accept", "") != accept:
            return None
        if whole and hashlib.sha256(data).hexdigest() != meta.get("sha256"):
            return None
        return meta, data

    def meta(self, url: str, accept: str = "") -> dict | None:
        """Шапка запису без тіла: для умовного запиту вистачає валідаторів."""
        got = self._read(url, accept, whole=False)
        return got[0] if got else None

    def get(self, url: str, accept: str = "") -> tuple[dict, bytes] | None:
        """(шапка, тіло) або None. Тіло, що не сходиться з сумою в шапці, — теж None:
        пошкоджений запис не має права стати текстом корпусу. Код відповіді — поле
        `code` шапки: «200» або позначка зникнення з GONE."""
        return self._read(url, accept, whole=True)

    def gone(self, url: str, accept: str, code: str) -> None:
        """Позначка «сторінки немає»; попереднє тіло, якщо було, — в _old."""
        self.put(url, accept, b"", {}, code)

    def put(self, url: str, accept: str, data: bytes, validators: dict,
            code: str = "200") -> None:
        digest = hashlib.sha256(data).hexdigest()
        old = self.meta(url, accept)
        if old and old.get("code", "200") == "200" and old.get("sha256") != digest:
            self.retire(url, accept)
        meta = {"url": url, "accept": accept, "code": code, "day": self.stamp,
                "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "etag": validators.get("etag", ""),
                "modified": validators.get("modified", ""),
                "sha256": digest, "bytes": len(data)}
        path = self.path(url, accept)
        path.parent.mkdir(parents=True, exist_ok=True)
        # PID у тимчасовому імені: паралельні `refresh` джерел одного репозиторію тягнуть ті
        # самі дерева в ту саму мить, і зі спільним «.tmp» один процес перейменовував файл
        # другого — той падав на `replace` з «No such file». Тепер кожен пише свій, а
        # `replace` атомарний, тож лишається цілий запис того, хто перейменував останнім.
        tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
        try:
            with gzip.open(tmp, "wb", compresslevel=6) as f:
                f.write(json.dumps(meta, ensure_ascii=False).encode("utf-8") + b"\n")
                f.write(data)
            tmp.replace(path)
        except OSError:
            tmp.unlink(missing_ok=True)
            raise

    def retire(self, url: str, accept: str = "") -> None:
        """Переносить наявний запис у `_old/<день>/<хост>/` — не видаляє."""
        path = self.path(url, accept)
        if not path.exists():
            return
        dest = self.root / OLD / self.stamp / path.parent.name / path.name
        n = 1
        while dest.exists():
            n += 1
            dest = dest.with_name(f"{path.stem}-{n}.gz")
        dest.parent.mkdir(parents=True, exist_ok=True)
        path.replace(dest)
