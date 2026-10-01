"""Глави книг про GRASP і SOLID у корпус примірника patterns — разове видобування.

Не частина рушія і не джерело `sources.json`: книги — локальні копії користувача, а
оновлювач тягне лише https-адреси з білого списку. Скрипт прив'язаний до цього
примірника й цих видань — назви файлів, межі глав і ознаки заголовків нижче вибрано
під них. Перелік книг і глав — у README примірника, розділ «Книги».

Запуск із кореня docfactory/ інтерпретатором venv примірника (потрібен pypdf):

    instances/patterns/.venv/bin/python instances/patterns/books.py [--books ТЕКА]
        [--7z ШЛЯХ] [--dry] [--overwrite] [larman] [csharp] [clean]

`--books` — тека з файлами книг (змовчання — C:\\Books\\docfactory\\patterns у WSL).
`--7z` — 7z.exe, яким розпаковується CHM Ларманa (змовчання — 7-Zip у Program Files).
`--dry` — лише показати, що вийде. Наявна глава в корпусі не перезаписується, поки
не сказано `--overwrite`. Розпакований CHM лягає в `out/books/larman/` примірника і
там лишається: скрипт нічого не видаляє.

Після запуску — `./df patterns manifest` і `./df patterns vectors`, як після refresh.
"""

import argparse
import datetime
import pathlib
import re
import subprocess
import sys

import pypdf

INSTANCE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(INSTANCE.parents[1]))
from engine.readers import _markup  # noqa: E402

CORPUS = INSTANCE / "corpus"
WORK = INSTANCE / "out" / "books"
BOOKS_DIR = "/mnt/c/Books/docfactory/patterns"
SEVEN_ZIP = "/mnt/c/Program Files/7-Zip/7z.exe"

LARMAN_FILE = "Craig Larman - Applying UML and PatiB .chm"
CSHARP_FILE = "Agile-Principles-Patterns-and-Practices-in-C.pdf"
CLEAN_FILE = "Book - Clean Architecture - Robert Cecil Martin.pdf"

BOOKS = {
    "larman": dict(prefix="book-larman-2004",
                   short="Applying UML and Patterns, 3rd ed. (Craig Larman, 2004)",
                   cite="книга — Craig Larman, «Applying UML and Patterns: An Introduction to "
                        "Object-Oriented Analysis and Design and Iterative Development», 3rd ed., "
                        "Prentice Hall, 2004"),
    "csharp": dict(prefix="book-martin-csharp-2006",
                   short="Agile Principles, Patterns, and Practices in C# "
                         "(Robert C. Martin, Micah Martin, 2006)",
                   cite="книга — Robert C. Martin, Micah Martin, «Agile Principles, Patterns, "
                        "and Practices in C#», Prentice Hall, 2006"),
    "clean": dict(prefix="book-clean-architecture-2017",
                  short="Clean Architecture (Robert C. Martin, 2017)",
                  cite="книга — Robert C. Martin, «Clean Architecture: A Craftsman's Guide to "
                       "Software Structure and Design», Prentice Hall, 2017"),
}

LARMAN_CHAPTERS = [
    ("ch17", "Chapter 17. GRASP: Designing Objects with Responsibilities"),
    ("ch18", "Chapter 18. Object Design Examples with GRASP"),
    ("ch25", "Chapter 25. GRASP: More Objects with Responsibilities"),
]
LARMAN_SECTIONS = [
    ("ch26lev1sec3",
     "Section 26.2. Some GRASP Principles as a Generalization of Other Patterns"),
]
# Назви глав рівно так, як вони стоять у змісті PDF (з подвійним пробілом у C#).
CSHARP_CHAPTERS = [
    "Chapter 7.  What Is Agile Design?",
    "Chapter 8.  The Single-Responsibility Principle (SRP)",
    "Chapter 9.  The Open/Closed Principle (OCP)",
    "Chapter 10.  The Liskov Substitution Principle (LSP)",
    "Chapter 11.  The Dependency-Inversion Principle (DIP)",
    "Chapter 12.  The Interface Segregation Principle (ISP)",
    "Chapter 28.  Principles of Package and Component Design",
]
CLEAN_CHAPTERS = [
    "Chapter 7 SRP: The Single Responsibility Principle",
    "Chapter 8 OCP: The Open-Closed Principle",
    "Chapter 9 LSP: The Liskov Substitution Principle",
    "Chapter 10 ISP: The Interface Segregation Principle",
    "Chapter 11 DIP: The Dependency Inversion Principle",
    "Chapter 12 Components",
    "Chapter 13 Component Cohesion",
    "Chapter 14 Component Coupling",
]


class Writer:
    """Пише главу документом корпусу: назва й рядок «джерело» кажуть главу, книгу,
    автора й рік — відповідь посилається на них замість адреси."""

    def __init__(self, dry: bool, overwrite: bool):
        self.dry, self.overwrite = dry, overwrite
        self.stamp = datetime.date.today().isoformat()

    def __call__(self, book: str, chapter: str, body: str) -> None:
        b = BOOKS[book]
        title = f"{chapter} — {b['short']}"
        num = re.match(r"(Chapter|Section) (\d+)(?:\.(\d+))?", chapter)
        tag = f"ch{int(num.group(2)):02d}" + (f"-{num.group(3)}" if num.group(3) else "")
        name = re.sub(r"^(Chapter|Section) [\d.]+\s*", "", chapter)
        fname = f"{b['prefix']}--{tag}-{_markup.slug(name)}.txt"
        head = f"# {title}\n# джерело: {b['cite']}; {chapter}\n# отримано: {self.stamp}\n"
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        _markup.require(title, body, fname)
        path = CORPUS / fname
        if path.exists() and not self.overwrite:
            print(f"  {fname}  уже є — лишаю як є (--overwrite, щоб переписати)")
            return
        print(f"  {fname}  {len(body)} символів, заголовків {len(re.findall(r'^#', body, re.M))}")
        if not self.dry:
            path.write_text(f"{head}\n{body}\n", encoding="utf-8")


# ── Larman: CHM, розпакований 7-Zip ────────────────────────────────────────

# Навігація сторінки (Previous/Next Section) — таблиця над текстом і під ним.
_NAV = re.compile(r'<table width="100%" border="0" cellspacing="0" cellpadding="0">\s*<tr><td>'
                  r'<div STYLE="MARGIN-LEFT: 0.15in;">.*?</table>', re.S | re.I)


def unpack_chm(books: pathlib.Path, seven_zip: str) -> pathlib.Path:
    """Розпаковує CHM у out/books/larman/ один раз; наявне не чіпає. 7z.exe — віндова
    програма, тож шляхи йому даються відносно робочої теки, а не лінуксові."""
    dest = WORK / "larman"
    if not (dest / "0131489062.hhc").exists():
        WORK.mkdir(parents=True, exist_ok=True)
        chm = WORK / "larman.chm"
        if not chm.exists():
            chm.write_bytes((books / LARMAN_FILE).read_bytes())
        subprocess.run([seven_zip, "x", "-y", "-olarman", "larman.chm"], cwd=WORK,
                       check=True, stdout=subprocess.DEVNULL)
    return dest


def larman_page(path: pathlib.Path) -> str:
    t = path.read_text(encoding="latin-1")
    t = t[t.lower().index("<body"):]
    t = _NAV.sub("", t)
    # Підпис рисунка чи таблиці і назва врізки — не розділи: заголовком вони різали б
    # текст, а врізка («Key Point») ставала б «батьком» наступного розділу.
    t = re.sub(r'<h(\d) class="doc(?:Figure|Table|Sidebar)Title"[^>]*>(.*?)</h\1>',
               r"<p>\2</p>", t, flags=re.S | re.I)
    t = re.sub(r"<li>\s*<p[^>]*>(.*?)</p>\s*</li>", r"<li>\1</li>", t, flags=re.S | re.I)
    body = _markup.html_body(t)
    body = re.sub(r"^#+\s*$", "", body, flags=re.M)
    return re.sub(r"^\[View full size image\]\s*$", "", body, flags=re.M)


def larman_files(root: pathlib.Path, stem: str) -> list[str]:
    """Сторінки глави в порядку змісту CHM: сама глава і її розділи."""
    hhc = (root / "0131489062.hhc").read_text(encoding="latin-1")
    seen, out = set(), []
    for f in re.findall(r'<param name="Local" value="0131489062/([^"]+)">', hhc):
        f = f.split("#")[0]
        if (f == f"{stem}.html" or f.startswith(f"{stem}lev")) and f not in seen:
            seen.add(f)
            out.append(f)
    return out


def larman(write, books: pathlib.Path, seven_zip: str) -> None:
    root = unpack_chm(books, seven_zip)
    pages = root / "0131489062"
    for stem, chapter in LARMAN_CHAPTERS:
        write("larman", chapter,
              "\n\n".join(larman_page(pages / f) for f in larman_files(root, stem)))
    for stem, section in LARMAN_SECTIONS:
        write("larman", section, larman_page(pages / f"{stem}.html"))


# ── Книги Мартіна: PDF, заголовки за шрифтом ───────────────────────────────

_CODE = re.compile(r"[{};]\s*$|^\s*[{}]|=>")
_CAPTION = re.compile(r"^(Figure|Listing|Table) \d")


def heading_pieces(page, is_heading) -> set[str]:
    """Шматки тексту, набрані шрифтом заголовка, — так їх видно надійніше, ніж за
    формою рядка: короткий рядок без крапки буває і кодом, і підписом."""
    out = set()

    def visit(text, cm, tm, fd, fs):
        font = fd.get("/BaseFont", "") if isinstance(fd, dict) else ""
        if text.strip() and is_heading(font, fs * (tm[0] or 1)):
            out.add(text.strip())
    page.extract_text(visitor_text=visit)
    return out


def pdf_chapter(reader, first: int, last: int, is_heading, skip) -> str:
    """Текст сторінок [first, last) абзацами. Рядки PDF — рядки верстки, тож абзацом
    вважається рядок, що закінчується крапкою й помітно коротший за повний; курсив і
    код посеред речення pypdf віддає окремими рядками — вони склеюються назад."""
    lines: list[tuple[str, bool]] = []
    for p in range(first, last):
        page = reader.pages[p]
        heads = heading_pieces(page, is_heading)
        for ln in (page.extract_text() or "").splitlines():
            if not ln.strip() or any(r.search(ln) for r in skip):
                continue
            lines.append((ln, ln.strip() in heads))
    widths = sorted(len(ln) for ln, h in lines if not h)
    full = widths[int(len(widths) * 0.9)] if widths else 80
    out: list[str] = []
    para = ""
    head = ""
    heads_out: list[str] = []

    def flush():
        nonlocal para
        if para.strip():
            out.append(para.strip())
        para = ""

    for ln, is_head in lines:
        if is_head:
            # Капітель: «S» + «YMPTOM», « 1: A» + «CCIDENTAL» — шматки одного слова;
            # пробіли між словами шматки несуть самі. Інакше рядок великого шрифту —
            # новий заголовок («Violations of LSP», далі «A Simple Example»).
            last = head.split(" ")[-1] if head else ""
            if head and (ln.startswith(" ") or head.endswith(" ")
                         or (len(last) == 1 and last.isupper() and ln.isupper())):
                head += ln
                continue
            if head:
                heads_out.append(head)
            head = ln
            continue
        if head:
            heads_out.append(head)
            head = ""
        if heads_out:
            flush()
            for h in heads_out:
                h = "## " + re.sub(r"\s+", " ", h).strip()
                # Заголовки до першого абзацу — назва самої глави (вона вже в назві
                # документа) і номер глави; той самий заголовок поспіль — колонтитул.
                if out and not re.fullmatch(r"## \d+", h) and h not in out[-2:]:
                    out.append(h)
            heads_out.clear()
        if _CAPTION.match(ln.strip()) or _CODE.search(ln):
            flush()
            out.append(ln.rstrip())
            continue
        if para and not para.endswith(" ") and not ln.startswith(" "):
            para += " "
        para += ln
        if re.search(r"[.?!:”\"]\s*$", ln) and len(ln) < full * 0.75:
            flush()
    flush()
    return "\n\n".join(out)


def outline_pages(reader) -> dict:
    res = {}

    def walk(items):
        for x in items:
            if isinstance(x, list):
                walk(x)
            else:
                res[x.title.strip()] = reader.get_destination_page_number(x)
    walk(reader.outline)
    return res


def outline_book(write, book: str, path: pathlib.Path, wanted: list, is_heading, skip) -> None:
    reader = pypdf.PdfReader(str(path))
    pages = outline_pages(reader)
    # Межа глави — наступний пункт змісту того самого рівня, а не підрозділ.
    order = sorted(v for k, v in pages.items()
                   if re.match(r"(Chapter|Section|PART|Appendix|Index)\b", k))
    for title in wanted:
        start = pages[title]
        end = min(v for v in order if v > start)
        write(book, re.sub(r"\s+", " ", title),
              pdf_chapter(reader, start, end, is_heading, skip))


def main() -> None:
    ap = argparse.ArgumentParser(description="Глави книг про GRASP і SOLID у корпус patterns.")
    ap.add_argument("which", nargs="*", choices=["larman", "csharp", "clean"],
                    help="які книги; змовчання — усі три")
    ap.add_argument("--books", default=BOOKS_DIR, help="тека з файлами книг")
    ap.add_argument("--7z", dest="seven_zip", default=SEVEN_ZIP, help="шлях до 7z.exe")
    ap.add_argument("--dry", action="store_true", help="лише показати, нічого не писати")
    ap.add_argument("--overwrite", action="store_true", help="переписати наявні глави")
    args = ap.parse_args()
    which = args.which or ["larman", "csharp", "clean"]
    books = pathlib.Path(args.books)
    write = Writer(args.dry, args.overwrite)
    if "larman" in which:
        larman(write, books, args.seven_zip)
    if "csharp" in which:
        outline_book(write, "csharp", books / CSHARP_FILE, CSHARP_CHAPTERS,
                     lambda font, size: "Arial,Bold" in font and size >= 14,
                     [re.compile(r"^\[View full size image\]$"),
                      re.compile(r"^© Jennifer M\. Kohnke$")])
    if "clean" in which:
        outline_book(write, "clean", books / CLEAN_FILE, CLEAN_CHAPTERS,
                     lambda font, size: "Bold" in font and size >= 30, [])


if __name__ == "__main__":
    main()
