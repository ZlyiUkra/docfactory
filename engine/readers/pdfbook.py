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
  «Exercise N», щоб вправу знаходило питання «вправа 2 глави 5»;
- `name_prefix` — початок імені кожного документа книжки (друга книжка в тому самому примірнику);
- для набору іншого видавця: `headings` і `labels` з виразом шрифту після кегля («10.5/DemiIt» —
  лише шрифт, чия назва містить DemiIt: у Manning назва врізки й підрозділ мають один кегль),
  `code_char_width` — ширина знака моноширинного шрифту в кеглях (Courier — 0.6), `furniture_above` —
  висота, вище якої рядок — колонтитул, `drop_fonts` — шрифти, текст яких випадає (написи на малюнках),
  `bullet_fonts` — шрифт маркерів списку (Wingdings), `aside_fonts` — шрифт приміток на полях лістингу:
  вони стають рядком «Annotations:» під кодом, поруч з яким стоять.

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
_CAPTION = re.compile(r"^(Listing|Figure|Table) (\d+\.\d+)(?=[A-Z])")


def _segments(page) -> list[tuple]:
    """(y, x, текст, моноширинний?, кегль, шрифт) кожного шматка тексту сторінки."""
    out = []

    def visit(text, cm, tm, font, size):
        text = text.replace("\n", "")
        if not text.strip() or not tm:
            return
        name = str(font.get("/BaseFont", "")) if font else ""
        x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
        y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
        out.append((y, x, text, bool(_MONO.search(name)), round(size * abs(tm[0] or 1), 1),
                    name.split("+")[-1]))

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


def _spec(key) -> tuple:
    """«10.5» чи «10.5/DemiIt» → (кегль, вираз шрифту або None)."""
    size, _, rx = str(key).partition("/")
    return round(float(size), 1), (re.compile(rx) if rx else None)


def _hyphen_end(text: str):
    """Збіг переносу в кінці рядка: «dupli-», а в Manning дефіс окремим шматком — «suc -»."""
    return re.search(rf"([A-Za-z])\s?[{_HYPHEN}]$", text)


class _Book:
    def __init__(self, source: dict):
        self.headings = [(*_spec(k), int(v)) for k, v in (source.get("headings") or {}).items()]
        self.labels = [_spec(v) for v in source.get("labels") or ()]
        self.code_max = float(source.get("code_max", 9.2))
        self.cw = float(source.get("code_char_width", 0.5))
        self.furniture = re.compile(source.get("furniture") or _FURNITURE)
        self.above = float(source["furniture_above"]) if source.get("furniture_above") else None
        self.drop_fonts = re.compile(source["drop_fonts"]) if source.get("drop_fonts") else None
        self.aside_fonts = re.compile(source["aside_fonts"]) if source.get("aside_fonts") else None
        self.bullet_fonts = re.compile(source["bullet_fonts"]) if source.get("bullet_fonts") else None
        self.exercises = str(source.get("exercises") or "")
        self.drop = re.compile(source["drop"]) if source.get("drop") else None
        self.top = max((h[0] for h in self.headings), default=99.0)

    @staticmethod
    def _match(row: list[tuple], specs: list[tuple]):
        for spec in specs:
            if all(s[4] == spec[0] and (spec[1] is None or spec[1].search(s[5])) for s in row):
                return spec
        return None

    def _code_text(self, row: list[tuple], left: float) -> str:
        size = row[0][4]
        cw = size * self.cw
        text = " " * max(0, round((row[0][1] - left) / cw))
        end = row[0][1]
        for y, x, t, mono, sz, *_ in row:
            gap = round((x - end) / cw)
            if text.strip() and gap > 0 and not text.endswith(" ") and not t.startswith(" "):
                text += " " * gap
            text += t
            end = x + len(t) * cw
        return text.rstrip()

    def _prose_text(self, row: list[tuple]) -> str:
        parts: list[str] = []
        code = False
        for y, x, t, mono, sz, *_ in row:
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
        text = re.sub(r"[ \t]+", " ", "".join(parts)).strip()
        # Підпис лістингу Manning — номер і назва окремими шматками без пробілу між ними.
        return _CAPTION.sub(r"\1 \2 ", text)

    @staticmethod
    def _notes(segs: list[tuple]) -> list[tuple]:
        """Примітки на полях лістингу (поле `aside_fonts`) → [(y верхнього рядка, текст)]. Рядки однієї
        примітки стоять з тим самим лівим краєм один під одним; продовження рядка — правіше на тій самій
        висоті."""
        notes: list[list] = []  # [x, y_top, y_last, [шматки]]
        for y, x, t, *_ in sorted(segs, key=lambda s: (-s[0], s[1])):
            for n in notes:
                if abs(y - n[2]) <= 1.5 and x > n[0] or abs(x - n[0]) <= 3 and 0 < n[2] - y <= 12:
                    n[3].append(t)
                    n[2] = min(n[2], y)
                    break
            else:
                notes.append([x, y, y, [t]])
        out = []
        for x, y_top, _, parts in notes:
            text = ""
            for t in parts:
                m = _hyphen_end(text)
                text = (text[:m.start(1) + 1] + _SOFT + t.strip()) if m else (text + " " + t.strip())
            out.append((y_top, " ".join(text.split())))
        return out

    def page_blocks(self, page) -> list[tuple]:
        """Блоки сторінки: ("h", рівень, текст), ("label", текст), ("p", текст, кегль, y_верх, y_низ),
        ("code", [рядки], y_верх, y_низ, [примітки])."""
        segs = _segments(page)
        if self.drop_fonts:
            segs = [s for s in segs if not self.drop_fonts.search(s[5])]
        if self.bullet_fonts:
            # Маркер списку набрано шрифтом знаків (Wingdings): сам знак нічого не каже, але з ним
            # рядок починає пункт списку, а не продовжує абзац.
            segs = [(y, x, "• ", False, sz, f) if self.bullet_fonts.search(f) else (y, x, t, m, sz, f)
                    for y, x, t, m, sz, f in segs]
        asides = [s for s in segs if self.aside_fonts and self.aside_fonts.search(s[5])]
        if asides:
            segs = [s for s in segs if not self.aside_fonts.search(s[5])]
        rows = _lines(segs)
        if self.above is not None:
            rows = [r for r in rows if r[0][0] <= self.above]
        prose_x = Counter(round(r[0][1]) for r in rows if not all(s[3] for s in r))
        code_x = [r[0][1] for r in rows if all(s[3] for s in r)]
        left = min(code_x) if code_x else (prose_x.most_common(1)[0][0] if prose_x else 72.0)
        blocks: list[tuple] = []
        for row in rows:
            raw = "".join(s[2] for s in row).strip()
            size = max(s[4] for s in row)
            y = row[0][0]
            mono = all(s[3] for s in row)
            if not mono and self.furniture.match(raw) and size < 10:
                continue
            if not mono and self.drop and self.drop.match(raw):
                continue
            if not mono and size > self.top:
                continue  # назва глави на її першій сторінці: назву документа дають закладки
            heading = None if mono else self._match(row, self.headings)
            if heading:
                blocks.append(("h", heading[2], " ".join(raw.split())))
                continue
            if not mono and self._match(row, self.labels):
                blocks.append(("label", " ".join(raw.split())))
                continue
            if mono and size <= self.code_max:
                text = self._code_text(row, left)
                last = blocks[-1] if blocks else None
                if last and last[0] == "code":
                    # Порожній рядок коду PDF не малює: його видно з подвійного проміжку.
                    gap = last[3] - y
                    lines = last[1] + ([""] if gap > size * 1.9 else []) + [text]
                    blocks[-1] = ("code", lines, last[2], y, last[4])
                else:
                    blocks.append(("code", [text], y, y, []))
                continue
            text = self._prose_text(row)
            last = blocks[-1] if blocks else None
            starts_item = bool(_BULLET.match(text) or re.match(r"^\d+\.\s", text))
            if (last and last[0] == "p" and not starts_item
                    and last[4] - y <= last[2] * 1.45 and abs(last[2] - size) < 0.6):
                prev = last[1]
                m = _hyphen_end(prev)
                joined = (prev[:m.start(1) + 1] + _SOFT + text) if m else (prev + " " + text)
                blocks[-1] = ("p", joined, last[2], last[3], y)
            else:
                blocks.append(("p", text, size, y, y))
        # Примітка на полях належить лістингу, поруч з яким стоїть; підписи до малюнків (тим самим
        # шрифтом, але без коду поруч) без самого малюнка нічого не кажуть і випадають.
        for y_top, note in self._notes(asides):
            for b in blocks:
                if b[0] == "code" and b[3] - 6 <= y_top <= b[2] + 6:
                    b[4].append(note)
                    break
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
                    m = _hyphen_end(a[1])
                    body = (a[1][:m.start(1) + 1] + _SOFT) if m else (a[1] + " ")
                    blocks[-1] = ("p", body + b[1], b[2], a[3], b[4])
                    here = here[1:]
                elif a[0] == "code" and b[0] == "code":
                    blocks[-1] = ("code", a[1] + b[1], a[2], b[3], a[4] + b[4])
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
                if b[4]:
                    out.append("Annotations: " + "; ".join(b[4]))
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
    # `name_prefix` — початок імені документа: дві книжки в одному примірнику мають і «Preface», і
    # «Chapter 1 …», а однакові імена злилися б у результатах в одне.
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    for title, text in texts:
        name = lead + _markup.slug(title)

        def make(title=title, text=text):
            body = _repair(text, vocab)
            _markup.require(title, body, source["url"])
            return _markup.document(title, source["url"], ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    return items
