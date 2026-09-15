"""Оновлювач корпусу: за оголошенням джерел завантажує документи в `corpus/`.

Тягне лише те, що дозволяє білий список примірника (`sources.allowed`). Наявні
файли не перезаписує без `--refresh`; `--refresh [id…]` перезаписує все або
назване. `--missing` лише докачує відсутні файли, наявних не чіпає ніколи. `--list`
показує, що завантажилося б, нічого не пишучи. Один документ на файл, окрім джерел,
що розгортаються (`toc`, `page`): ті дають файл на главу.

Заморожене джерело (`frozen: true` — знімок на закріпленому тезі чи коміті) не
питається зовсім, доки його не назвуть: вміст такого знімка змінитися не може, а
кожен його перелік — звернення до чужого API з лімітом на годину.
"""

import json
import time
import urllib.error

from engine import net
from engine import readers
from engine import sources as S

# Скільки чекати перед повтором, коли сервер каже «забагато» (429) чи «тимчасово
# недоступний» (503). Такий збій — прохання пригальмувати, а не відмова: після
# третього очікування звернення все ж рахується збоєм, і прогін іде далі.
RETRY_WAITS = (60, 300, 900)
_RETRY_CODES = {"збій: HTTP 429", "збій: HTTP 503"}


def pause_of(instance_dir) -> float:
    """Пауза між зверненнями: поле `pause_sec` у config.json примірника, інакше
    типова net.PAUSE_SEC. Чужий сайт, що банить за частоту, задає свою паузу
    даними примірника, а не правкою ядра."""
    path = instance_dir / "config.json"
    if not path.exists():
        return net.PAUSE_SEC
    try:
        value = json.loads(path.read_text(encoding="utf-8")).get("pause_sec")
    except (OSError, ValueError) as exc:
        raise SystemExit(f"{path}: не читається ({exc})")
    if value is None:
        return net.PAUSE_SEC
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 600:
        raise SystemExit(f"{path}: поле pause_sec мусить бути числом 0–600, а не {value!r}")
    return float(value)


class Ctx:
    """Контекст читача: звернення крізь білий список примірника і дата прогону.

    Між будь-якими двома зверненнями — не менше `pause` секунд, хоч би хто їх
    робив: перелік джерела, тіло документа чи звірка. Раніше пауза стояла лише
    після записаного документа, і читач, що складає перелік з кількох сторінок,
    бив по сайту без неї."""

    def __init__(self, sources, stamp: str, pause: float | None = None):
        self._sources = sources
        self.stamp = stamp
        self.pause = net.PAUSE_SEC if pause is None else pause
        self._last = 0.0

    def allowed(self, url: str) -> bool:
        return S.allowed(url, self._sources)

    _allow = allowed

    def fetch(self, url: str, since: str = "") -> tuple[str, bytes]:
        """net.fetch з паузою між зверненнями і повторами на 429/503."""
        for wait in RETRY_WAITS + (None,):
            gap = self._last + self.pause - time.monotonic()
            if gap > 0:
                time.sleep(gap)
            code, data = net.fetch(url, self.allowed, since=since)
            self._last = time.monotonic()
            if wait is None or code not in _RETRY_CODES:
                return code, data
            print(f"  {url}: {code}, чекаю {wait} с і пробую знову", flush=True)
            time.sleep(wait)
        return code, data

    def bytes(self, url: str) -> bytes:
        code, data = self.fetch(url)
        if code != "200":
            raise SystemExit(f"{url}: {code}")
        return data

    def text(self, url: str) -> str:
        return self.bytes(url).decode("utf-8", errors="replace")


def named(source, targets) -> bool:
    """Чи назване джерело: його id або документ із нього («react-15.3/docs-refs»,
    «react-15.3--docs-refs.txt»)."""
    sid = source["id"]
    return any(t == sid or t.startswith((sid + "/", sid + "--")) for t in targets)


def _wanted(item, source, targets, do_refresh, missing) -> bool:
    if not do_refresh or missing:
        return False
    if not targets:
        return True
    return item.id in targets or item.file in targets or source["id"] in targets


def refresh(instance_dir, targets: set, do_refresh: bool, listing: bool,
            missing: bool = False) -> int:
    data = S.load(instance_dir)
    src = data["sources"]
    corpus = instance_dir / "corpus"
    if not listing:
        corpus.mkdir(exist_ok=True)
    ctx = Ctx(src, time.strftime("%Y-%m-%d"), pause_of(instance_dir))
    written = skipped = failed = 0

    asleep = {s["id"] for s in src if s.get("frozen") and not named(s, targets)}
    if asleep:
        print(f"── Заморожених джерел не питаю: {len(asleep)} (знімки на закріпленому тезі "
              f"чи коміті; назвіть id, щоб звернутися) ──")
    for source in src:
        # З --missing імена обмежують, які джерела питати: «докачай відсутнє в
        # react-15.3» не мусить гортати ще сорок джерел.
        if source["id"] in asleep or (missing and targets and not named(source, targets)):
            continue
        reader = readers.get(source["reader"])
        try:
            items = reader(source, ctx)
        except (net.Refused, SystemExit, urllib.error.URLError) as e:
            print(f"── {source['id']}: не вдалось скласти перелік: {e}")
            failed += 1
            continue
        print(f"── {source['id']} ({source['reader']}): {len(items)} документів ──")
        for it in items:
            path = corpus / it.file
            if listing:
                print(f"  {it.file}")
                continue
            if path.exists() and not _wanted(it, source, targets, do_refresh, missing):
                size = len(path.read_text(encoding="utf-8"))
                print(f"  {it.file}  уже є, {size} символів")
                skipped += 1
                continue
            try:
                text = it.make()
            except (net.Refused, SystemExit, urllib.error.URLError) as e:
                print(f"  {it.file}  збій: {e}")
                failed += 1
                continue
            # Запис через тимчасовий файл із перейменуванням: невдалий запис
            # (повний диск, права, обрив) лишає попередній документ цілим —
            # корпус тут єдина копія, попередньої версії ніде немає. А OSError
            # валить один документ і рахується збоєм, не обриває весь прогін.
            tmp = path.with_name(path.name + ".tmp")
            try:
                tmp.write_text(text, encoding="utf-8")
                tmp.replace(path)
            except OSError as e:
                print(f"  {it.file}  запис не вдався: {e}")
                failed += 1
                tmp.unlink(missing_ok=True)
                continue
            print(f"  {it.file}  {len(text)} символів", flush=True)
            written += 1

    if listing:
        print("── Лише перелік; нічого не записано ──")
    else:
        print(f"── Готово: записано {written}, лишено як є {skipped}, збоїв {failed} ──")
    return 1 if failed else 0
