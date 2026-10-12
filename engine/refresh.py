"""Оновлювач корпусу: за оголошенням джерел завантажує документи в `corpus/`.

Тягне лише те, що дозволяє білий список примірника (`sources.allowed`). Наявні
файли не перезаписує без `--refresh`; `--refresh [id…]` перезаписує все або
назване. З іменами неназваних джерел не питає зовсім. `--missing` лише докачує
відсутні файли, наявних не чіпає ніколи. `--list`
показує, що завантажилося б, нічого не пишучи. Один документ на файл, окрім джерел,
що розгортаються (`toc`, `page`): ті дають файл на главу.

Заморожене джерело (`frozen: true` — знімок на закріпленому тезі чи коміті) не
питається зовсім, доки його не назвуть: вміст такого знімка змінитися не може, а
кожен його перелік — звернення до чужого API з лімітом на годину.

Зі сховищем сирого (`raw_store: true` у config.json, див. rawstore) кожна відповідь
лягає ще й туди, а крок `build` (`offline`) проходить той самий шлях без мережі: тексти
збираються зі сховища, і правка читача не вимагає нового завантаження.
"""

import json
import time
import urllib.error

from engine import net
from engine import rawstore
from engine import readers
from engine import redact as R
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
    бив по сайту без неї.

    Зі сховищем сирого (`store`) кожна відповідь 200 лягає туди, і та сама адреса в
    межах прогону вдруге не питається: дерево toc.json Oracle читають двадцять
    джерел, а сервер чує його раз. Між прогонами запит умовний — з валідаторами
    попередньої відповіді, і «304» означає «бери зі сховища». `offline` — крок build:
    мережі немає зовсім, лише сховище; адреси, якої там немає, — збій, як у мережі."""

    def __init__(self, sources, stamp: str, pause: float | None = None,
                 store: "rawstore.Store | None" = None, offline: bool = False):
        self._sources = sources
        self._stamp = stamp
        self.pause = net.PAUSE_SEC if pause is None else pause
        self._last = 0.0
        self.store = store
        self.offline = offline
        self._seen: set = set()
        self._day = ""

    @property
    def stamp(self) -> str:
        """День отримання для шапки документа. Без мережі це день, коли сторінку
        отримало сховище, а не сьогодні: інакше перезібраний документ казав би
        «отримано сьогодні», і умовний запит звірки за цією датою міг би
        пропустити зміну нагорі."""
        return self._day if self.offline and self._day else self._stamp

    def allowed(self, url: str) -> bool:
        return S.allowed(url, self._sources)

    _allow = allowed

    def _call(self, url: str, request):
        """Звернення `request()` з паузою між зверненнями і повторами на 429/503."""
        for wait in RETRY_WAITS + (None,):
            gap = self._last + self.pause - time.monotonic()
            if gap > 0:
                time.sleep(gap)
            result = request()
            self._last = time.monotonic()
            if wait is None or result[0] not in _RETRY_CODES:
                return result
            print(f"  {url}: {result[0]}, чекаю {wait} с і пробую знову", flush=True)
            time.sleep(wait)
        return result

    def fetch(self, url: str, since: str = "", gzip: bool = False,
              accept: str = "") -> tuple[str, bytes]:
        """net.fetch з паузою між зверненнями і повторами на 429/503; зі сховищем —
        крізь нього."""
        if self.store is not None and not since:
            return self._stored(url, gzip, accept)
        # `gzip` передається лише тоді, коли його попросили: без нього виклик той
        # самий, що й до появи поля, і заглушки net.fetch у smoke його не знають.
        extra = {"gzip": True} if gzip else {}
        if accept:
            extra["accept"] = accept
        return self._call(url, lambda: net.fetch(url, self.allowed, since=since, **extra))

    def _stored(self, url: str, gzip: bool, accept: str) -> tuple[str, bytes]:
        # Білий список питається й тоді, коли мережі не буде: запис, що лишився в
        # сховищі від ширшого оголошення, не має права стати текстом корпусу.
        if not self.allowed(url):
            raise net.Refused(f"адреса поза оголошенням примірника: {url}")
        if self.offline or (url, accept) in self._seen:
            got = self.store.get(url, accept)
            if got is None:
                return ("збій: немає в сховищі сирого (спершу refresh)", b"")
            self._day = got[0].get("day", "")
            return got[0].get("code", "200"), got[1]
        old = self.store.meta(url, accept) or {}
        code, data, valid = self._call(url, lambda: net.fetch_full(
            url, self.allowed, gzip=gzip, accept=accept,
            etag=old.get("etag", ""), modified=old.get("modified", "")))
        if code == "304":
            got = self.store.get(url, accept)
            if got is not None and got[0].get("code", "200") == "200":
                self._seen.add((url, accept))
                return "200", got[1]
            # Запис пошкоджений — сервер про це не знає; питаємо ще раз, без умов.
            code, data, valid = self._call(url, lambda: net.fetch_full(
                url, self.allowed, gzip=gzip, accept=accept))
        try:
            if code == "200":
                self.store.put(url, accept, data, valid)
                self._seen.add((url, accept))
            elif code in rawstore.GONE:
                self.store.gone(url, accept, code)
                self._seen.add((url, accept))
        except OSError as e:
            # Сховище — запас на майбутнє; через нього документ цього прогону не падає.
            print(f"  {url}: сховище сирого не записалося: {e}", flush=True)
        return code, data

    def bytes(self, url: str, gzip: bool = False, accept: str = "") -> bytes:
        code, data = self.fetch(url, gzip=gzip, accept=accept)
        if code != "200":
            raise SystemExit(f"{url}: {code}")
        return data

    def text(self, url: str, gzip: bool = False, accept: str = "") -> str:
        return self.bytes(url, gzip, accept).decode("utf-8", errors="replace")


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
            missing: bool = False, offline: bool = False) -> int:
    data = S.load(instance_dir)
    src = data["sources"]
    corpus = instance_dir / "corpus"
    stamp = time.strftime("%Y-%m-%d")
    store = rawstore.of(instance_dir, stamp)
    if offline:
        if store is None:
            raise SystemExit("Крок build збирає тексти зі сховища сирого, а в цьому примірнику "
                             "його не ввімкнено: поле raw_store у config.json.")
        if not store.root.is_dir():
            raise SystemExit(f"Сховище {store.root} порожнє: спершу refresh.")
        print("── Збираю тексти зі сховища сирого, без мережі ──")
    if not listing:
        corpus.mkdir(exist_ok=True)
    ctx = Ctx(src, stamp, pause_of(instance_dir), store, offline)
    rules = R.rules(instance_dir)
    written = skipped = failed = 0

    asleep = {s["id"] for s in src if s.get("frozen") and not named(s, targets)}
    if asleep:
        print(f"── Заморожених джерел не питаю: {len(asleep)} (знімки на закріпленому тезі "
              f"чи коміті; назвіть id, щоб звернутися) ──")
    for source in src:
        # Імена обмежують, які джерела питати: «перекачай ці сторінки» не мусить
        # гортати ще двадцять джерел. Перелік неназваного джерела — теж звернення, і
        # дороге: README пакета — по зверненню на кожну з сотень версій. Відсутні файли
        # неназваних джерел дописує `--missing` без імен.
        if source["id"] in asleep or (targets and not named(source, targets)):
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
                text = R.apply(it.make(), rules)
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
