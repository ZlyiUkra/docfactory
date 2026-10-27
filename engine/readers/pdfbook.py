"""Читач `pdf-book` — книжка, що лежить у користувача PDF-файлом (видання O'Reilly): глава — документ.

Поля джерела:
- `url` — сторінка книжки у видавця (https); стоїть у шапці кожного документа, сама не читається;
- `file` — абсолютний шлях PDF на цій машині. Читач відкриває лише його й до мережі не звертається:
  білий список тут — сам шлях, оголошений у `sources.json`;
- `chapters` — вираз назв пунктів верхнього рівня закладок PDF, що стають документами (типово
  `^(Preface|Chapter \\d+\\.)`): зміст, предметний покажчик і колофон — не текст книжки;
- `headings` — об'єкт «кегль шрифту заголовка → рівень» (`{"18.9": 2, "15.8": 3}`); рядок, усі шматки
  якого набрано не моноширинним шрифтом цього кегля, стає заголовком;
- `labels` — кеглі заголовків врізок (`[15.0]`): такий рядок стає підписом жирним, а не розділом;
- `code_max` — найбільший кегль моноширинного шрифту блоку коду (типово 9.2): рядок, цілком набраний
  моноширинним шрифтом не більшого кегля, — рядок коду; моноширинний шматок серед тексту — `код`;
- `furniture` — вираз рядків колонтитулів (типово номер сторінки з назвою глави чи розділу через «|»);
- `drop` — вираз рядків, що випадають (мітка «CHAPTER 5» над назвою глави на її першій сторінці);
- `exercises` — назва розділу вправ (`Exercises`): кожен пункт «N.» у ньому стає підрозділом
  «Exercise N», щоб вправу знаходило питання «вправа 2 глави 5».

Навіщо. Простий витяг тексту з PDF (читач `pdf`) губить межі коду: рядок `func divAndRemainder(…)`
стоїть упритул до абзацу, а відступи коду видно лише з координат. Тут кожен шматок тексту береться з
його шрифтом, кеглем і місцем на сторінці (`visitor_text` pypdf), рядки складаються за висотою, і
шрифт вирішує, що це: абзац, заголовок, код чи колонтитул. Відступ рядка коду — відстань від лівого
краю коду сторінки в ширинах знака моноширинного шрифту (половина кегля).

Два вади набору лагодяться за словником самої книжки. Перенос слова в кінці рядка («dupli-» +
«cate») знімається, лише якщо злите слово в книжці трапляється цілим, — інакше дефіс справжній
(«compile-time»). Розрив кернінгу після великої літери Y, T, V, W, F чи P («Y ou’re», «T o») зливається,
лише якщо злите слово є в словнику («T any» лишається); після «A» й «I» не зливається нічого («A new»).
Праву частину розриву словником не перевірити: «ou» трапляється в книжці саме через ці розриви.
"""

import re
import textwrap
from collections import Counter

from engine.readers import Item, _markup, register

_MONO = re.compile(r"Mono|Courier|Code", re.I)
# Номер сторінки — арабський або римський (передмова: «xvii | Preface»).
_FURNITURE = r"^(\d+|[ivxlc]+)\s*\|\s*\S.*$|^\S.*\|\s*(\d+|[ivxlc]+)$|^(\d+|[ivxlc]+)$"
_WORD = re.compile(r"[A-Za-z][A-Za-z’']*")
_SOFT = "­"
_BULLET = re.compile(r"^[•●▪◦–]\s*")
# Перенос: звичайний дефіс і дефіс Юнікоду (U+2010, U+2011), яким набирає Antenna House.
_HYPHEN = "-\u2010\u2011"
# Літери, після яких кернінг набору розриває слово («Y ou», «T o», «W e»): права частина розриву —
# не слово, і злите слово перевіряється лише словником. «A» й «I» тут немає: «A new» — два слова.
_KERN = "YTVWFP"


def _segments(page) -> list[tuple]:
    """(y, x, текст, моноширинний?, кегль) кожного шматка тексту сторінки."""
    out = []

    def visit(text, cm, tm, font, size):
        text = text.replace("\n", "")
        if not text.strip() or not tm:
            return
        name = str(font.get("/BaseFont", "")) if font else ""
        x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
        y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
        out.append((y, x, text, bool(_MONO.search(name)), round(size * abs(tm[0] or 1), 1)))

    page.extract_text(visitor_text=visit)
    return out


def _lines(segs: list[tuple]) -> list[list[tuple]]:
    """Шматки → рядки зверху вниз; рядок — шматки зліва направо."""
    rows: list[list[tuple]] = []
    for seg in sorted(segs, key=lambda s: (-s[0], s[1])):
        if rows and abs(rows[-1][0][0] - seg[0]) <= 1.5:
            rows[-1].append(seg)
        else:
            rows.append([seg])
    return [sorted(r, key=lambda s: s[1]) for r in rows]


class _Book:
    def __init__(self, source: dict):
        self.headings = {round(float(k), 1): int(v) for k, v in (source.get("headings") or {}).items()}
        self.labels = {round(float(v), 1) for v in source.get("labels") or ()}
        self.code_max = float(source.get("code_max", 9.2))
        self.furniture = re.compile(source.get("furniture") or _FURNITURE)
        self.exercises = str(source.get("exercises") or "")
        self.drop = re.compile(source["drop"]) if source.get("drop") else None
        self.top = max(self.headings, default=99.0)

    def _code_text(self, row: list[tuple], left: float) -> str:
        size = row[0][4]
        cw = size * 0.5
        text = " " * max(0, round((row[0][1] - left) / cw))
        end = row[0][1]
        for y, x, t, mono, sz in row:
            gap = round((x - end) / cw)
            if text.strip() and gap > 0 and not text.endswith(" ") and not t.startswith(" "):
                text += " " * gap
            text += t
            end = x + len(t) * cw
        return text.rstrip()

    def _prose_text(self, row: list[tuple]) -> str:
        parts: list[str] = []
        code = False
        for y, x, t, mono, sz in row:
            if mono and not code:
                lead = " " if t.startswith(" ") else ""
                parts.append(lead + "`" + t.strip())
                code = True
            elif mono:
                parts.append(t)
            else:
                if code:
                    parts[-1] = parts[-1].rstrip() + "`" + (" " if parts[-1].endswith(" ") else "")
                    code = False
                parts.append(t)
        if code:
            parts[-1] = parts[-1].rstrip() + "`"
        return re.sub(r"[ \t]+", " ", "".join(parts)).strip()

    def page_blocks(self, page) -> list[tuple]:
        """Блоки сторінки: ("h", рівень, текст), ("label", текст), ("p", текст, кегль, y_верх, y_низ),
        ("code", [рядки], y_верх, y_низ)."""
        rows = _lines(_segments(page))
        prose_x = Counter(round(r[0][1]) for r in rows if not all(s[3] for s in r))
        code_x = [r[0][1] for r in rows if all(s[3] for s in r)]
        left = min(code_x) if code_x else (prose_x.most_common(1)[0][0] if prose_x else 72.0)
        blocks: list[tuple] = []
        for row in rows:
            raw = "".join(s[2] for s in row).strip()
            sizes = {s[4] for s in row}
            size = max(sizes)
            y = row[0][0]
            mono = all(s[3] for s in row)
            if not mono and self.furniture.match(raw) and size < 10:
                continue
            if not mono and self.drop and self.drop.match(raw):
                continue
            if not mono and size > self.top:
                continue  # назва глави на її першій сторінці: назву документа дають закладки
            if not mono and sizes <= set(self.headings):
                blocks.append(("h", self.headings[size], " ".join(raw.split())))
                continue
            if not mono and sizes <= self.labels:
                blocks.append(("label", " ".join(raw.split())))
                continue
            if mono and size <= self.code_max:
                text = self._code_text(row, left)
                last = blocks[-1] if blocks else None
                if last and last[0] == "code":
                    # Порожній рядок коду PDF не малює: його видно з подвійного проміжку.
                    gap = last[3] - y
                    lines = last[1] + ([""] if gap > size * 1.9 else []) + [text]
                    blocks[-1] = ("code", lines, last[2], y)
                else:
                    blocks.append(("code", [text], y, y))
                continue
            text = self._prose_text(row)
            last = blocks[-1] if blocks else None
            starts_item = bool(_BULLET.match(text) or re.match(r"^\d+\.\s", text))
            if (last and last[0] == "p" and not starts_item
                    and last[4] - y <= last[2] * 1.45 and abs(last[2] - size) < 0.6):
                prev = last[1]
                if re.search(rf"[A-Za-z][{_HYPHEN}]$", prev):
                    joined = prev[:-1] + _SOFT + text
                else:
                    joined = prev + " " + text
                blocks[-1] = ("p", joined, last[2], last[3], y)
            else:
                blocks.append(("p", text, size, y, y))
        return blocks

    def markdown(self, pages) -> str:
        blocks: list[tuple] = []
        for page in pages:
            here = self.page_blocks(page)
            # Абзац чи код, розірвані сторінкою, — одне ціле: наступна сторінка починається з
            # малої літери чи з продовження коду.
            if blocks and here:
                a, b = blocks[-1], here[0]
                if a[0] == "p" and b[0] == "p" and re.match(r"^[a-z(“\"`]", b[1]):
                    sep = _SOFT if re.search(rf"[A-Za-z][{_HYPHEN}]$", a[1]) else " "
                    body = a[1][:-1] if sep == _SOFT else a[1]
                    blocks[-1] = ("p", body + sep + b[1], b[2], a[3], b[4])
                    here = here[1:]
                elif a[0] == "code" and b[0] == "code":
                    blocks[-1] = ("code", a[1] + b[1], a[2], b[3])
                    here = here[1:]
            blocks.extend(here)
        out: list[str] = []
        in_ex, ex_level = False, 3
        for b in blocks:
            if b[0] == "h":
                in_ex = bool(self.exercises) and b[2].strip() == self.exercises
                ex_level = b[1] + 1
                out.append("#" * b[1] + " " + b[2])
            elif b[0] == "label":
                out.append(f"**{b[1]}**")
            elif b[0] == "code":
                # Відступ від лівого краю коду сторінки: окремий рядок, набраний посередині,
                # без dedent стояв би за пів рядка від краю.
                out.append("```\n" + textwrap.dedent("\n".join(b[1])).strip("\n") + "\n```")
            else:
                # Номер пункту списку PDF віддає двічі («1.1. The simple calculator…»).
                text = re.sub(r"^(\d+)\.\1\.\s*", r"\1. ", _BULLET.sub("- ", b[1]))
                m = re.match(r"^(\d+)\.\s+(.*)$", text, re.S) if in_ex else None
                if m:
                    out.append("#" * min(ex_level, 6) + f" Exercise {m.group(1)}")
                    text = m.group(2)
                out.append(text)
        return "\n\n".join(out)


def _repair(text: str, vocab: set) -> str:
    def soft(m):
        whole = m.group(1) + m.group(2)
        return whole if whole.lower() in vocab else m.group(1) + "-" + m.group(2)

    def kern(m):
        whole = m.group(1) + m.group(2)
        return whole if whole.lower() in vocab else m.group(0)

    text = re.sub(rf"([A-Za-z’']+){_SOFT}([A-Za-z’']+)", soft, text)
    text = text.replace(_SOFT, "-")
    return re.sub(rf"\b([{_KERN}]) ([a-z’']+)\b", kern, text)


@register("pdf-book")
def pdf_book(source: dict, ctx) -> list[Item]:
    import pypdf

    path = source.get("file")
    if not path:
        raise SystemExit(f"{source['id']}: читач pdf-book потребує поля file — шляху PDF.")
    chapters = re.compile(source.get("chapters") or r"^(Preface|Chapter \d+\.)")
    book = _Book(source)
    try:
        reader = pypdf.PdfReader(path)
    except OSError as exc:
        raise SystemExit(f"{source['id']}: не відкрив {path}: {exc}")
    top = []
    for entry in reader.outline:
        if not isinstance(entry, list):
            top.append((" ".join(str(entry.title).split()), reader.get_destination_page_number(entry)))
    spans = []
    for i, (title, start) in enumerate(top):
        end = top[i + 1][1] if i + 1 < len(top) else len(reader.pages)
        if chapters.search(title):
            spans.append((title, start, end))
    if not spans:
        raise SystemExit(f"{source['id']}: у закладках {path} немає жодної глави за виразом "
                         f"{chapters.pattern}.")
    # Перший прохід — словник книжки для переносів і розривів кернінгу: його не видно з однієї глави.
    texts = [(title, book.markdown(reader.pages[a:b])) for title, a, b in spans]
    vocab = {w.lower() for _, t in texts for w in _WORD.findall(t.replace(_SOFT, " "))}
    items = []
    for title, text in texts:
        name = _markup.slug(title)

        def make(title=title, text=text):
            body = _repair(text, vocab)
            _markup.require(title, body, source["url"])
            return _markup.document(title, source["url"], ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    return items
