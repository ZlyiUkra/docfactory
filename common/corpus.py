"""
СПІЛЬНЕ · документи практики і поділ їх на фрагменти.

Документи — уся база специфікацій ECMAScript: повна ECMA-262 розділ за розділом
плюс ECMA-402, 404, 414 і вільні документи, на які спирається 402 (RFC 4647,
звіти Unicode). Вони лежать у corpus/ як звичайні .txt і завантажені з
https://tc39.es/ та суміжних джерел один раз, вручну. Код їх тільки читає:
нічого не завантажує з мережі, нічого не перезаписує.

Формат файлу: три рядки шапки, які починаються з «#» (заголовок розділу,
адреса джерела з якорем, дата вивантаження), порожній рядок, далі текст.
Шапка потрібна для посилання у відповіді агента, тому в тіло вона не потрапляє.

ЧОМУ ІНДЕКСУЄМО ФРАГМЕНТИ, А НЕ ЦІЛІ ДОКУМЕНТИ

Розділи специфікації дуже різні за розміром: найменший (10.4.7, незмінний
прототип) — 1570 символів, найбільший (22.1, String Objects) — 52257, тобто
в тридцять три рази більший. Якби одиницею пошуку був цілий документ, то на
запит про `String.prototype.replace` пошук повернув би весь розділ 22.1:
п'ятдесят кілобайт тексту, з яких потрібні дві сотні символів. У промпт таке
не влізе, а якби й влізло — модель шукала б відповідь у стосі стороннього
тексту, і саме там беруться вигадані відповіді.

Тому індекс будується по фрагментах, а у відповідь агентові йде фрагмент разом
із номером свого розділу. Документів при цьому лишається стільки ж —
ділиться не документ, а те, що ми з нього дістаємо.

ДЕ ПРОХОДИТЬ МЕЖА ФРАГМЕНТА

Специфікація сама пронумерована: «22.1.3.19 String.prototype.replace ( ... )»
стоїть окремим рядком перед своїм текстом. Ця нумерація і є межею — фрагмент
починається з такого заголовка і триває до наступного. Різати за кількістю
символів наосліп не треба: підзаголовок уже позначає, де закінчується одна тема
і починається інша.

Залишається один випадок, який нумерація не покриває: підрозділ, довший за
`MAX_CHARS`. Такий ділиться далі по порожніх рядках, шматки нумеруються
(«частина 2 з 3») і кожен зберігає заголовок свого підрозділу, щоб посилання
не загубилося.

ДОКУМЕНТАЦІЯ БЕЗ НУМЕРАЦІЇ

Документація сайтів (React та інші) номерів розділів не має: межею там є заголовок
markdown «## Назва», який читачі рушія ставлять окремим рядком. Цей режим обирає
поле `sections: "markdown"` у config.json примірника (див. profile.py). Розділом
тоді стає шлях заголовків — «reference/usestate-initialstate/parameters», — бо
голе «Parameters» в одному документі трапляється під кожним API. Код між огорожами
«```» заголовків не має: рядок «## …» усередині прикладу розділу не відкриває.

Такі документи ще й несуть версію (рядок шапки «# версія: 18.3.1»), і той самий
текст дослівно повторюється в документації сусідніх версій. Повтор тут не
викидається, а зливається: фрагмент лишається один, а в його `versions`
дописується кожна версія, де цей текст є, — так видно, від якої до якої версії
документація казала саме це.
"""

import hashlib
import json
import os
import pathlib
import re
import sys

from . import instance

# Один корпус — уся база документів примірника в теці corpus/. Вибору набору
# немає: код завжди читає весь корпус. Мітка набору для ecmascript лишається
# «suite» — на ній будується імʼя колекції Qdrant (spec-suite-bge-small), тож
# вектори, залиті модулями 5 і 6, лишаються придатними без перерахунку. Інший
# домен задає свою полем doc_set у config.json.
DOC_SET = instance.config().get("doc_set") or "suite"

# Як ділити документ на розділи: "numbered" — номери специфікації, "markdown" —
# заголовки «## …». Те саме поле читає profile.py; тут воно потрібне раніше за
# будь-який профіль, бо поділ — основа і пошуку, і векторів.
SECTIONS = instance.config().get("sections") or "numbered"

# Тека документів — у примірнику, з яким працює цей запуск (див. instance.py):
# код тепер спільний на всі домени, а corpus/ у кожного домену свій.
DOCS_DIRS = [instance.root() / "corpus"]
DOCS_DIR = DOCS_DIRS[0]

# Межа розміру фрагмента. Її задає не смак, а вікно моделі ембедингів:
# e5-small читає 512 токенів і мовчки відрізає все, що далі. Текст специфікації
# щільний на розділові знаки й ідентифікатори, тому дає приблизно один токен на
# три символи — при межі 1800 п'ятнадцять фрагментів із 284 вилазили за вікно
# (найдовший — 616 токенів), і їхні хвости в індекс не потрапляли зовсім.
MAX_CHARS = 1400
# Межа склеювання хвостів при різанні задовгого підрозділу: куций останній
# шматок приклеюється до попереднього, щоб «частина 3 з 3» не була трьома
# рядками. На відбір цілих розділів ця межа не впливає: короткий розділ — теж
# повноцінна одиниця специфікації і лишається в індексі (див. split_document).
MIN_CHARS = 200

# Рядок-заголовок специфікації: номер розділу, пробіл, назва.
# Обмеження довжини відсікає звичайні речення, що починаються з числа.
_HEADING = re.compile(r"^(\d+(?:\.\d+)*)\s+(\S.{0,110})$")

# Заголовок markdown, як його ставлять читачі рушія: два-шість «#», пробіл, назва.
_MD_HEADING = re.compile(r"^(#{2,6}) (\S.*)$")


def version_key(version: str) -> tuple:
    """Ключ порівняння версій: «0.14.8» < «15.6.2» < «18.3.1» < «19.3»."""
    return tuple(int(n) for n in re.findall(r"\d+", version))


def version_within(version: str, want: str) -> bool:
    """Чи належить версія лінії `want`: «18» бере «18.3.1», «16.8» — «16.8.6»,
    але «1» не бере «18» — порівняння по межі сегмента, як у quality.within."""
    return version == want or version.startswith(want + ".")


def version_line(version: str) -> str:
    """Лінія версії для переліку в описі: «18.3.1» → «18», «0.14.8» → «0.14»."""
    parts = version.split(".")
    return ".".join(parts[:2]) if parts[0] == "0" and len(parts) > 1 else parts[0]


def _slug(title: str) -> str:
    return "-".join(re.findall(r"[a-z0-9]+", title.lower())) or "x"


class _NumberedHeadings:
    """Заголовки специфікації: рядок без відступу «20.1.3 Назва»."""

    def feed(self, line: str) -> tuple[str, str] | None:
        m = _HEADING.match(line.strip())
        if m and line.strip() == line:
            return m.group(1), line.strip()
        return None


class _MarkdownHeadings:
    """Заголовки markdown поза огорожами коду. Розділ — шлях слагів від
    найвищого заголовка до цього, назва — той самий шлях словами."""

    def __init__(self):
        self.fence = False
        self.stack: list[tuple[int, str]] = []

    def feed(self, line: str) -> tuple[str, str] | None:
        if line.startswith("```"):
            self.fence = not self.fence
            return None
        if self.fence:
            return None
        m = _MD_HEADING.match(line)
        if not m:
            return None
        level, title = len(m.group(1)), m.group(2).strip()
        self.stack = [(lv, t) for lv, t in self.stack if lv < level] + [(level, title)]
        return ("/".join(_slug(t) for _, t in self.stack),
                " › ".join(t for _, t in self.stack))


def _headings():
    return _MarkdownHeadings() if SECTIONS == "markdown" else _NumberedHeadings()


class Document:
    """Один файл із corpus/ разом із шапкою."""

    def __init__(self, path: pathlib.Path):
        raw = path.read_text(encoding="utf-8").splitlines()
        # Шапка — рядки з «#» на самому початку файла, до першого іншого. Раніше
        # бралися перші три «#»-рядки будь-де у файлі: для специфікації це те
        # саме, а в тілі markdown «## …» — звичайний заголовок, не шапка.
        n = 0
        while n < len(raw) and raw[n].startswith("#"):
            n += 1
        head = [ln[1:].strip() for ln in raw[:n]]
        body = "\n".join(raw[n:]).strip("\n")

        self.doc_id = path.stem                      # напр. 18-string-objects
        # Ім'я документа без джерела: «react-17--docs-hooks-intro» → «docs-hooks-
        # intro». Однакове в тієї самої сторінки різних версій — за ним зливаються
        # повтори.
        self.slug = path.stem.partition("--")[2] or path.stem
        self.path = path
        self.title = head[0] if head else path.stem  # напр. 22.1 String Objects
        self.url = ""
        self.fetched = ""
        self.version = ""
        for line in head[1:]:
            if line.startswith("джерело:"):
                self.url = line.split(":", 1)[1].strip()
            elif line.startswith("отримано:"):
                self.fetched = line.split(":", 1)[1].strip()
            elif line.startswith("версія:"):
                self.version = line.split(":", 1)[1].strip()
        self.text = body

    @property
    def section(self) -> str:
        """Номер розділу з заголовка: «22.1» з «22.1 String Objects»."""
        m = _HEADING.match(self.title)
        return m.group(1) if m else ""

    def __repr__(self):
        return f"<Document {self.doc_id} {len(self.text)} симв.>"


class Passage:
    """Фрагмент документа — одиниця, яку індексує і повертає пошук."""

    def __init__(self, doc: Document, section: str, heading: str, text: str,
                 part: int = 1, parts: int = 1):
        self.doc_id = doc.doc_id
        self.doc_title = doc.title
        self.url = doc.url
        self.fetched = doc.fetched
        self.section = section
        self.heading = heading
        self.text = text
        self.part = part
        self.parts = parts
        self.slug = doc.slug
        # Рядок шапки може назвати кілька версій через кому: один запис CHANGELOG
        # буває спільним для двох ліній, випущених одним днем.
        self.versions = sorted((v.strip() for v in doc.version.split(",") if v.strip()),
                               key=version_key, reverse=True)

    @property
    def anchor(self) -> str:
        """Розділ, упізнаваний поза документом: у специфікації номер і так
        унікальний, а шлях заголовків markdown — лише разом з ім'ям документа."""
        return f"{self.slug}#{self.section}" if SECTIONS == "markdown" else self.section

    def absorb(self, other: "Passage") -> None:
        """Той самий текст у документі іншої версії. Версія дописується, а
        представником стає найновіша: її адресу й назву бачить той, хто звіряє
        цитату, — за старою адресою текст міг давно змінитися."""
        newest = self.versions[0] if self.versions else ""
        for v in other.versions:
            if v not in self.versions:
                self.versions.append(v)
        self.versions.sort(key=version_key, reverse=True)
        if other.versions and version_key(other.versions[0]) > version_key(newest):
            for field in ("doc_id", "doc_title", "url", "fetched", "part", "parts"):
                setattr(self, field, getattr(other, field))

    @property
    def pid(self) -> str:
        """Стійкий ідентифікатор фрагмента — він же посилання у відповіді агента."""
        base = f"{self.doc_id}#{self.section or 'head'}"
        return f"{base}/{self.part}" if self.parts > 1 else base

    @property
    def label(self) -> str:
        """Людський підпис: те, що агент цитує клієнтові як джерело."""
        tail = f" (частина {self.part} з {self.parts})" if self.parts > 1 else ""
        return f"{self.heading}{tail}"

    def as_prompt_block(self) -> str:
        """Готовий блок для tool_result: підпис, посилання, текст."""
        return f"[{self.pid}] {self.label}\nдокумент: {self.doc_title}\n\n{self.text}"

    def __repr__(self):
        return f"<Passage {self.pid} {len(self.text)} симв.>"


def load_documents() -> list[Document]:
    """Усі .txt корпусу в порядку імен файлів (він же порядок розділів)."""
    docs = []
    for folder in DOCS_DIRS:
        files = sorted(folder.glob("*.txt"))
        if not files:
            raise SystemExit(
                f"У {folder} немає жодного .txt, і кешу фрагментів "
                f"({cache_path().name}) теж немає — працювати нема з чим.\n"
                "  Корпус виносили в архів? Розпакуйте його назад у corpus/.\n"
                "  Примірник новий? Зберіть корпус: ./df <домен> refresh.")
        docs.extend(Document(p) for p in files)
    return docs


def _paragraphs(text: str) -> list[str]:
    """Абзаци для різання задовгого розділу. У markdown порожній рядок усередині
    блоку коду абзацу не закінчує: розрізаний навпіл приклад — два шматки, жоден
    з яких не працює."""
    if SECTIONS != "markdown":
        return text.split("\n\n")
    blocks, current, fence = [], [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            fence = not fence
        if not line.strip() and not fence:
            if current:
                blocks.append("\n".join(current))
                current = []
            continue
        current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


def _split_long(doc: Document, section: str, heading: str, text: str,
                max_chars: int = None) -> list[Passage]:
    """Розрізає задовгий підрозділ по порожніх рядках, зберігаючи заголовок."""
    ceiling = max_chars or MAX_CHARS
    if len(text) <= ceiling:
        return [Passage(doc, section, heading, text)]

    chunks, current = [], []
    size = 0
    for para in _paragraphs(text):
        # Абзац, який сам довший за межу (довгий алгоритм списком), лишаємо цілим:
        # різати його посередині кроку гірше, ніж перевищити межу.
        if size and size + len(para) > ceiling:
            chunks.append("\n\n".join(current))
            current, size = [], 0
        current.append(para)
        size += len(para) + 2
    if current:
        chunks.append("\n\n".join(current))

    # Останній шматок може вийти зовсім куций — приклеюємо його до попереднього.
    if len(chunks) > 1 and len(chunks[-1]) < MIN_CHARS:
        tail = chunks.pop()
        chunks[-1] = chunks[-1] + "\n\n" + tail

    return [Passage(doc, section, heading, c, i + 1, len(chunks))
            for i, c in enumerate(chunks)]


def split_document(doc: Document, max_chars: int = None) -> list[Passage]:
    """Ділить один документ на фрагменти по заголовках специфікації.

    `max_chars` перекриває межу розміру. Потрібен лише дослідові з розміром
    шматка, який у практиці модуля 4 ще не написаний; звичайні виклики його
    не задають.
    """
    section, heading = doc.section, doc.title
    buffer: list[str] = []
    out: list[Passage] = []
    headings = _headings()

    def flush():
        text = "\n".join(buffer).strip()
        if text:
            out.extend(_split_long(doc, section, heading, text, max_chars))
        buffer.clear()

    for line in doc.text.split("\n"):
        hit = headings.feed(line)
        if hit:
            flush()
            section, heading = hit
            continue
        buffer.append(line)
    flush()

    # Жодного відбору за довжиною. Колишнє правило «len(p.text) >= MIN_CHARS»
    # мало прибирати рубрики без власного тексту, а насправді мовчки викидало
    # кожен короткий нумерований розділ — 368 справжніх розділів на кшталт
    # «20.5.3.3 Error.prototype.name», — і пошук відповідав за них сусідніми
    # номерами. Для інструмента цитування це найгірша з відмов. Рубрика ж без
    # тексту фрагмента й так не дає: flush() порожній буфер не записує.
    return out


def section_map() -> dict[str, bool]:
    """Номери всіх розділів, названих у документах заголовком, і чи має кожен
    власний текст (True) чи це рубрика, весь вміст якої лежить у підрозділах
    (False). Розбір рядків той самий, що в split_document, тож множина розділів
    «з текстом» — це рівно те, що мусить тримати індекс; старт сервера і smoke
    звіряють одне з одним, і втрата розділів стає видимою, а не тихою."""
    known: dict[str, bool] = {}
    for doc in load_documents():
        section, has_text = doc.section, False
        headings = _headings()

        def note():
            if section:
                key = f"{doc.slug}#{section}" if SECTIONS == "markdown" else section
                known[key] = known.get(key, False) or has_text

        for line in doc.text.split("\n"):
            hit = headings.feed(line)
            if hit:
                note()
                section, has_text = hit[0], False
                continue
            if line.strip():
                has_text = True
        note()
    return known


# Типографіка, якою та сама сторінка різних редакцій різниться, не різнячись
# змістом: криві лапки проти прямих, тире, нерозривний пробіл, багатокрапка. Сайти
# React перемальовували її при переїздах, і 604 дослівно однакові фрагменти через це
# не зливалися, а потім стояли у видачі поруч як різні відповіді.
_TYPOGRAPHY = str.maketrans({
    "\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
    "\u2013": "-", "\u2014": "-", "\u00a0": " ", "\u2026": "...",
})


def same_text(text: str) -> str:
    """Текст, зведений до вигляду, у якому фрагменти порівнюють на однаковість.

    Сам текст фрагмента це не міняє: у корпусі й у відповіді лишається те, що
    написано в документі. Зводиться лише ключ порівняння.
    """
    return re.sub(r"\s+", " ", text.translate(_TYPOGRAPHY)).strip()


# Кеш готових фрагментів. Версія формату піднімається, коли міняється склад
# полів Passage або правила поділу: старий файл тоді не збігається відбитком і
# перезбирається сам.
CACHE_VERSION = 1

# Поля, з яких фрагмент відновлюється, — рівно вони, не менше й не більше.
# Якщо у Passage з'явиться нове поле, а цей перелік про нього не знатиме, кеш
# не пишеться зовсім (див. _cache_write): повільний старт кращий за тихо
# загублене поле.
CACHE_FIELDS = ("doc_id", "doc_title", "url", "fetched", "section", "heading",
                "text", "part", "parts", "slug", "versions")

_from_cache = False


def used_cache() -> bool:
    """Чи взято фрагменти з кешу останнім load_passages(). Для діагностики."""
    return _from_cache


def cache_path() -> pathlib.Path:
    """Файл кешу — в out/ примірника: тека службова і в git не потрапляє."""
    return instance.root() / "out" / "passages.json"


def _corpus_stamp() -> str:
    """Відбиток корпусу: склад теки, дата теки й сума паспорта.

    Головна вимога до відбитка — дешевизна: він береться при кожному старті, і
    якщо коштуватиме як саме читання, кеш не матиме сенсу. Обійти теку з
    розміром і датою кожного файла — найнадійніше, але на 22 733 файлах через
    межу WSL це 19 секунд проти 0,1 на самі імена: `stat` там коштує майже як
    відкриття. Тому беруться три дешеві ознаки, і разом вони ловлять усе, що
    робить із корпусом сама фабрика:

    - перелік імен — доданий, прибраний чи перейменований документ;
    - дата теки corpus/ — оновлювач пише кожен документ через тимчасовий файл
      із перейменуванням (engine/refresh.py), а перейменування в теку міняє її
      дату завжди, навіть коли текст той самий;
    - сума index.json — паспорт корпусу, у якому лежить контрольна сума тексту
      кожного документа; `manifest` переписує його після кожного оновлення.

    Лишається один випадок, якого ці ознаки не бачать: хтось переписав документ
    поверх, не через перейменування, і не оновив паспорт. Тоді кеш лишиться
    старим — але таким самим лишиться й паспорт, тобто корпус уже розійдеться
    сам із собою, і `smoke` скаже про це раніше за пошук. Способу зловити це
    дешево немає: він і є той самий обхід із `stat`.

    Порожній рядок означає «відбитка немає»: кеш тоді не читається і не
    пишеться, а все працює як до його появи.
    """
    parts: list = [CACHE_VERSION, SECTIONS, MAX_CHARS, MIN_CHARS]
    for folder in DOCS_DIRS:
        try:
            with os.scandir(folder) as entries:
                names = sorted(e.name for e in entries if e.name.endswith(".txt"))
            parts.append([names, os.stat(folder).st_mtime_ns])
        except OSError:
            return ""
        try:
            passport = hashlib.sha256((folder / "index.json").read_bytes()).hexdigest()
        except OSError:
            passport = ""          # паспорта ще немає — свіжий примірник
        parts.append(passport)
    return hashlib.sha256(json.dumps(parts).encode("utf-8")).hexdigest()


class _Head:
    """Шапка документа, зведена до полів, які з неї бере Passage.

    Потрібна лише кешеві: відновити фрагмент — це покликати той самий
    конструктор Passage, а не розкладати його поля повз нього."""

    __slots__ = ("doc_id", "title", "url", "fetched", "slug", "version")

    def __init__(self, record: dict):
        self.doc_id = record["doc_id"]
        self.title = record["doc_title"]
        self.url = record["url"]
        self.fetched = record["fetched"]
        self.slug = record["slug"]
        # Версії зберігаються списком, а конструктор чекає рядок шапки — той
        # самий, що в документі: кілька версій через кому.
        self.version = ",".join(record["versions"])


def _cache_read(stamp: str | None) -> list[Passage] | None:
    """Фрагменти з кешу — або None, якщо його немає, він чужий чи не читається.

    `stamp` None означає «відбиток не звіряти»: так кеш читається в архівному
    режимі, де корпусу вже немає і звіряти його склад нема з чим.

    Жодна поломка кешу не має права стати поломкою пошуку, тому тут немає
    жодного підняття помилки: будь-яка несподіванка означає «кешу немає».
    """
    if stamp is not None and not stamp:
        return None
    try:
        data = json.loads(cache_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    if stamp is not None and data.get("stamp") != stamp:
        return None
    records = data.get("passages")
    if not isinstance(records, list):
        return None
    want = set(CACHE_FIELDS)
    out = []
    try:
        for record in records:
            if not isinstance(record, dict) or set(record) != want:
                return None
            out.append(Passage(_Head(record), record["section"], record["heading"],
                               record["text"], record["part"], record["parts"]))
    except (TypeError, KeyError, ValueError):
        return None
    return out


def _cache_write(stamp: str, passages: list[Passage]) -> None:
    """Записати кеш у out/ примірника. Невдача нічого не ламає: наступний
    запуск збере фрагменти з файлів, як робив до появи кешу.

    Запис через тимчасовий файл і os.replace: обірваний на середині запуск не
    лишає недописаного кешу, який довелося б відрізняти від цілого. Корпус ця
    функція не чіпає взагалі — вона пише один файл і більше нічого.
    """
    if not stamp:
        return
    want = set(CACHE_FIELDS)
    if any(set(vars(p)) != want for p in passages):
        return
    records = [{field: getattr(p, field) for field in CACHE_FIELDS} for p in passages]
    path = cache_path()
    tmp = path.with_name(path.name + ".tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps({"stamp": stamp, "passages": records},
                                  ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, path)
    except OSError:
        try:
            tmp.unlink()
        except OSError:
            pass


def _corpus_short() -> tuple[int, int] | None:
    """(скільки файлів, скільки має бути) — якщо корпус коротший за паспорт.

    Паспорт `corpus/index.json` пише крок `manifest`, і він перелічує кожен
    документ корпусу. Тобто в самій теці лежить незалежна відповідь на питання
    «скільки тут має бути файлів», і зайве читання одного файла коштує чверть
    секунди проти ста на саме збирання. Немає паспорта — немає й судження:
    повертається None, і все працює як раніше.
    """
    try:
        data = json.loads((DOCS_DIR / "index.json").read_text(encoding="utf-8"))
        want = len(data["documents"])
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if not want:
        return None
    have = 0
    for folder in DOCS_DIRS:
        try:
            with os.scandir(folder) as entries:
                have += sum(1 for e in entries if e.name.endswith(".txt"))
        except OSError:
            continue
    return (have, want) if have < want else None


def corpus_archived() -> bool:
    """Чи винесено корпус в архів: текстів немає, а кеш фрагментів є.

    Режим свідомий, не аварійний. Корпус astro — 22 733 файли, і поки вони
    лежать у теці, кожне звернення git до дерева обходить їх усі, а сам корпус
    важить 120 МБ проти 20 у кеші. Коли документацію не оновлюють, тексти в
    теці не потрібні нікому: пошук по словах бере їх із кешу, пошук за змістом —
    із Qdrant, а `read_section` віддає той самий текст, що й раніше.

    Відрізнити архів від свіжого примірника, де корпусу ще немає, просто: у
    свіжого немає й кешу, і там мовчки працювати ні з чим — помилка. Тому
    ознака саме подвійна.

    Чого в архівному режимі не буде: оновлення корпусу (`refresh`, `manifest`,
    `check` читають файли) і звірки індексу з документами — звіряти нема з чим.
    Щоб повернутися, досить розпакувати архів назад у corpus/.
    """
    if not cache_path().exists():
        return False
    for folder in DOCS_DIRS:
        try:
            with os.scandir(folder) as entries:
                if any(e.name.endswith(".txt") for e in entries):
                    return False
        except OSError:
            continue
    return True


def load_passages() -> list[Passage]:
    """Фрагменти корпусу — з кешу, якщо корпус не змінився, інакше з файлів.

    Саме збирання — нижче, у _split_all(); тут лише кеш. Він нічого не заміняє
    й нічого не видаляє: не збігся відбиток, не читається файл, не той склад
    полів — збираємо з корпусу, як і раніше.
    """
    global _from_cache
    if corpus_archived():
        kept = _cache_read(None)
        if kept is None:
            raise SystemExit(
                f"Корпус у {DOCS_DIR} порожній, а кеш фрагментів "
                f"({cache_path()}) не читається — працювати нема з чим.\n"
                "  Поверніть тексти в corpus/ (розпакуйте архів або візьміть з git) "
                "і підніміть крок знову.")
        _from_cache = True
        return kept
    stamp = _corpus_stamp()
    kept = _cache_read(stamp)
    _from_cache = kept is not None
    if kept is not None:
        return kept
    passages = _split_all()
    short = _corpus_short()
    if short:
        # Корпус коротший за власний паспорт — найімовірніше його саме
        # розпаковують із архіву, і розпакування ще не скінчилося. Індекс із
        # половини корпусу — не помилка коду, а неповна відповідь на кожне
        # питання, тому про це кажуть уголос. І кеш у цьому стані не пишеться:
        # інакше неповний зліпок затер би повний, і повертатися було б нікуди.
        print(f"common.corpus: УВАГА: у corpus/ {short[0]} документів, а паспорт "
              f"описує {short[1]} — індекс неповний, кеш не оновлюю",
              file=sys.stderr)
    else:
        _cache_write(stamp, passages)
    return passages


def _split_all() -> list[Passage]:
    """Зібрати фрагменти з файлів корпусу — вхід і лексичного, і векторного пошуку.

    Однакові тексти зливаються в один фрагмент. Потреба в цьому не теоретична:
    розділ 6.1.7 The Object Type містить підрозділи 6.1.7.1–6.1.7.4, а вони
    трапляються в корпусі ще й окремими документами. Тобто кілька файлів
    повторюють шматки першого слово в слово.

    Без злиття пошук повертає обидві копії, і агент отримує два однакові
    тексти замість двох різних — половина місця в промпті витрачена ні на що.
    Лишається та копія, що трапилась першою; порядок файлів сталий, тож і вибір
    сталий. Документів від цього не меншає — зникає тільки повтор усередині індексу.

    Ключ злиття — (номер розділу, текст), а не сам текст. Різні розділи з
    дослівно однаковим коротким тілом — сусідні «See 23.2» у переліку
    конструкторів глобального об'єкта — це різні одиниці специфікації, і за
    ключем-текстом дванадцять таких розділів зникали з індексу мовчки.

    У режимі markdown ключ — ще й ім'я документа без джерела, а повтор не
    викидається, а зливається (Passage.absorb): документація сусідніх версій
    повторює одна одну дослівно, і те, в яких версіях текст був саме таким, —
    відповідь на питання «з якої версії», а не шум.

    Порівнюється при цьому не сам текст, а зведений (same_text): переїзд сайту
    міняв лапки й тире, не міняючи жодного слова, і без зведення такі копії
    лишалися окремими фрагментами.
    """
    merge = SECTIONS == "markdown"
    seen: dict = {}
    out = []
    for doc in load_documents():
        for p in split_document(doc):
            same = same_text(p.text)
            key = (p.slug, p.section, same) if merge else (p.section, same)
            kept = seen.get(key)
            if kept is None:
                seen[key] = p
                out.append(p)
            elif merge:
                kept.absorb(p)
    return out


def fingerprint(passages: list[Passage]) -> str:
    """Відбиток набору документів — щоб кеш векторів не пережив їхню зміну.

    Береться ідентифікатор кожного фрагмента і довжина його тексту: перейменування
    файлу, доданий розділ чи інша межа різання дадуть інший відбиток, і індекс
    перебудується сам.
    """
    payload = [[p.pid, len(p.text)] for p in passages]
    import hashlib
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()[:16]
