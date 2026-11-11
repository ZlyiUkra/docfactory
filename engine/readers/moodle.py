"""Читач `moodle-course` — курс на Moodle, відкритий для гостя: опис курсу і його PDF-матеріали.

`moodle-course` — `url` — сторінка курсу (`…/course/view.php?id=N`); `version` — рік курсу
                  («2026-27»), він же версія кожного документа. `skip` — вираз назв посилань і
                  імен файлів, які не беруться (змовчання — розв'язки, файли стилю, форуми);
                  `headings` — вирази рядка-заголовка розділу для PDF, що не є слайдами
                  (аркуші завдань, приклади звітів); змовчання — «Question 1», «1 Introduction».
                  `assign: false` — не брати вкладень завдань: курс поточного року віддає їх
                  лише після входу, і кожен прогін бився б об сторінку входу.
                  `within` мусить пускати сторінку курсу, `mod/resource/view.php`,
                  `mod/assign/view.php` і `pluginfile.php/`: ресурс віддає PDF редиректом.

Документи. `info` — опис курсу: поля картки курсу («General prerequisites», «Course
synopsis» тощо), кожне — розділ. Кожне посилання-ресурс (`mod/resource`) — документ з PDF.
Кожне завдання (`mod/assign`) — сторінка, де PDF лежать вкладеннями; кожне вкладення —
документ. Ім'я документа — назва посилання без дужок («Lecture 9 slides (updated Nov. 9th)»
→ `lecture-9-slides`), тож та сама лекція різних років має те саме ім'я, і родина джерел
зливає її в одне місце видачі.

Слайди. PDF, зібраний LaTeX-класом Beamer (поле `Creator` у метаданих), ріжеться по
сторінках: сторінка — розділ, назва розділу — перший рядок слайда, а якщо він кінчається
двокрапкою, то разом із другим (Beamer ставить підзаголовок кадру окремим рядком). Останній
рядок слайда, коли він закінчується номером сторінки, — колонтитул і випадає. Покроковий показ
Beamer дає кілька сторінок одного кадру, де кожна доповнює попередню; така сторінка заміняє
попередню, а не дописується до неї. Інший PDF стає абзацами з заголовками за `headings`.

Навіщо окремий читач. Курс Moodle — це не сайт документації: перелік матеріалів є лише на
сторінці курсу, PDF лежать за адресою з номером ревізії, яка змінюється з кожним оновленням
файла, а розв'язки висять поруч із завданнями, хоч студентам їх не видають. Тому читач іде
від сторінки курсу, бере ресурс за постійною адресою `view.php?id=` і відкидає розв'язки.
"""

import html
import io
import re
from urllib.parse import urljoin

from engine.readers import Item, _markup, register
from engine.readers.cncfcurriculum import OCR_NOTE
from engine.readers.legalpt import _SCAN_CHARS, _ocr_cached, _paragraphs

_SKIP = (r"(?i)solution|style ?file|example file|latex|\.sty$|\.tex$|\.zip$|forum|signup|"
         r"reading list|class tutor")
_HEADINGS = (r"^(Question|Problem|Exercise)\s+\d+\b",
             r"^\d{1,2}(\.\d{1,2})*\.?\s+[A-Z][A-Za-z][A-Za-z ,:'’()-]{1,70}$")
_LINK = re.compile(r'<a href="(https://[^"]+/mod/(resource|assign)/view\.php\?id=\d+)"[^>]*>'
                   r'(.*?)</a>', re.S)
_ATTACH = re.compile(r'href="(https://[^"]+/pluginfile\.php/[^"]+?\.pdf)(?:\?forcedownload=1)?"')
_FIELD = re.compile(r'<span class="customfieldname">(.*?)</span>.*?'
                    r'<div class="text_to_html">(.*?)</div>', re.S)
_TAG = re.compile(r"<[^>]+>")
_CTRL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
# Колонтитул Beamer: коротка назва лекції і номер слайда наприкінці рядка.
_FOOTER = re.compile(r"^.{0,120}\s\d{1,3}$")
_BULLET = re.compile(r"^[▶•◮►▸‣◦●]\s*")
# Зсув по висоті, менший за цей (у пунктах сторінки), — індекс формули, а не новий рядок.
_SAME_LINE = 6


def _plain(fragment: str) -> str:
    return " ".join(html.unescape(_TAG.sub(" ", fragment)).split())


def _name(label: str) -> str:
    return _markup.slug(re.sub(r"\([^)]*\)", " ", label))


def _info(source: dict, ctx) -> Item:
    def make():
        page = ctx.text(source["url"])
        title = _plain(re.search(r"<title>(.*?)</title>", page, re.S).group(1)).split("|")[0]
        title = re.sub(r"^Course:\s*", "", title).strip()
        parts = [f"## {_plain(name)}\n\n{_plain(text)}" for name, text in _FIELD.findall(page)
                 if _plain(text)]
        body = "\n\n".join(parts)
        _markup.require(title, body, source["url"])
        return _markup.document(title, source["url"], ctx.stamp, body, source.get("version", ""))

    return Item(id=f"{source['id']}/info", file=f"{source['id']}--info.txt", make=make)


def _page_lines(page) -> list[str]:
    """Рядки сторінки зі шматків тексту, а не з готового `extract_text()`.

    LaTeX не ставить пробілу між словом і наступним словом іншого кольору чи шрифту: межа
    шрифту і є пробілом. Готове видобування склеює такі слова («beingfully connectedand»),
    і пошук по словах їх не бачить. Тут кожен шматок (одна команда показу тексту) стає
    окремим словом, якщо між ним і попереднім немає пробілу. Шматок, зсунутий по висоті
    менше ніж на `_SAME_LINE`, лишається в тому самому рядку: так верхній і нижній індекси
    формули не розсипаються на окремі рядки."""
    parts: list = []

    def visit(text, cm, tm, _font, _size):
        if text:
            parts.append((text, tm[5] * cm[3] + cm[5]))

    page.extract_text(visitor_text=visit)
    lines: list[str] = []
    y0 = None
    for text, y in parts:
        for k, piece in enumerate(text.split("\n")):
            if k or y0 is None or abs(y - y0) > _SAME_LINE or not lines:
                lines.append(piece)
            else:
                prev = lines[-1]
                glue = "" if not prev or prev[-1].isspace() or not piece or piece[0].isspace() else " "
                lines[-1] = prev + glue + piece
            y0 = y
    lines = [" ".join(_CTRL.sub(" ", line).split()) for line in lines]
    return [line for line in lines if line]


def _flow(lines: list[str]) -> list[str]:
    """Рядки слайда, зламані шириною кадру, — назад в абзаци; пункт `▶` починає новий абзац.
    Адреса, перенесена на наступний рядок, склеюється без пробілу."""
    out: list[str] = []
    for line in lines:
        line = "\\" + line if line.startswith("#") else line
        if _BULLET.match(line):
            out.append("- " + _BULLET.sub("", line))
        elif out and out[-1].startswith(("http://", "https://")) and " " not in out[-1] \
                and " " not in line:
            out[-1] += line
        elif out and (re.search(r"https?://\S+/$", out[-1]) and " " not in line):
            out[-1] += line
        elif out:
            out[-1] += " " + line
        else:
            out.append(line)
    return out


def _slides(reader, doc_title: str) -> str:
    """Слайди Beamer: сторінка — розділ `## назва кадру`."""
    frames: list[list] = []  # [назва, рядки тіла]
    for index, page in enumerate(reader.pages):
        lines = _page_lines(page)
        if lines and _FOOTER.match(lines[-1]) and len(lines) > 1:
            lines = lines[:-1]
        if not lines:
            continue
        if index == 0:
            frames.append([doc_title, lines])
            continue
        head, rest = lines[0], lines[1:]
        if head.endswith(":") and rest:
            head, rest = f"{head} {rest[0]}", rest[1:]
        body = _flow(rest)
        if frames and frames[-1][0] == head and " ".join(body).startswith(" ".join(frames[-1][1])):
            frames[-1][1] = body
        else:
            frames.append([head, body])
    out = []
    for number, (head, body) in enumerate(frames):
        text = "\n\n".join(body) if number else "\n".join(body)
        out.append(text if number == 0 else f"## {head}\n\n{text}")
    return "\n\n".join(out)


def _pdf_doc(source: dict, ctx, url: str, label: str, name: str) -> Item:
    def make():
        from pypdf import PdfReader
        data = ctx.bytes(url)
        if not data.startswith(b"%PDF"):
            raise SystemExit(f"{url}: не PDF — документ не записую.")
        reader = PdfReader(io.BytesIO(data))
        meta = reader.metadata or {}
        own = " ".join(str(meta.get("/Title") or "").split())
        title = f"{label}: {own}" if own and own.lower() not in label.lower() else label
        title = f"{title} ({source['version']})" if source.get("version") else title
        if "beamer" in str(meta.get("/Creator") or "").lower():
            body = _slides(reader, title)
        else:
            heads = [re.compile(r) for r in source.get("headings") or _HEADINGS]
            lines, scanned = [], False
            for index, page in enumerate(reader.pages):
                found = _page_lines(page)
                # Приклад міні-проєкту — скан без текстового шару: сторінку розпізнає OCR.
                if sum(len(line) for line in found) < _SCAN_CHARS:
                    scanned = True
                    found = [" ".join(line.split()) for line in _ocr_cached(data, index)]
                lines.extend(line for line in found if line)
            body = _paragraphs([("\\" + l if l.startswith("#") else l) for l in lines], heads)
            if scanned:
                body = f"{OCR_NOTE} Цитату звіряти з PDF за адресою джерела.\n\n{body}"
        _markup.require(title, body, url)
        return _markup.document(title, url, ctx.stamp, body, source.get("version", ""))

    return Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make)


@register("moodle-course")
def moodle_course(source: dict, ctx) -> list[Item]:
    skip = re.compile(source.get("skip", _SKIP))
    page = ctx.text(source["url"])
    # Картка курсу 2020-21 ще не мала полів опису: документа опису тоді немає.
    items = [_info(source, ctx)] if any(_plain(t) for _n, t in _FIELD.findall(page)) else []
    names = {"info"}

    def add(url: str, label: str, name: str) -> None:
        if name in names:
            name = f"{name}-{len(names)}"
        names.add(name)
        items.append(_pdf_doc(source, ctx, url, label, name))

    for url, kind, inner in _LINK.findall(page):
        label = _plain(re.sub(r'<span class="accesshide.*?</span>', "", inner, flags=re.S))
        url = html.unescape(url)
        if not label or skip.search(label) or not ctx.allowed(url):
            continue
        if kind == "resource":
            add(url, label, _name(label))
            continue
        if source.get("assign") is False:
            continue
        for attach in dict.fromkeys(_ATTACH.findall(ctx.text(url))):
            attach = urljoin(url, html.unescape(attach))
            file = attach.rsplit("/", 1)[-1]
            if not skip.search(file) and ctx.allowed(attach):
                add(attach, f"{label}: {file}", _name(f"{label} {file.rsplit('.', 1)[0]}"))
    if not any(item.id != f"{source['id']}/info" for item in items):
        raise SystemExit(f"{source['id']}: на сторінці курсу немає жодного матеріалу — розмітка змінилась "
                         f"або курс закрито для гостя.")
    return items
