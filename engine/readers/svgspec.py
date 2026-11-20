"""Читачі специфікацій SVG: багатосторінкове видання і специфікація однією сторінкою з міткою видання.

`svg-chapters`      — `url` — зміст багатосторінкового видання SVG (SVG 1.1, SVG 2 і чернетка редакторів
                      SVG 2): кожна сторінка видання — документ. `exclude` — вирази імен сторінок, що не
                      беруться; `version` — мітка видання в шапці документа; `label` — назва видання в назві
                      документа («SVG 2»).
`spec-html-edition` — `url` — специфікація однією сторінкою (Bikeshed, ReSpec чи інструмент робочої групи
                      SVG). Те саме, що `spec-html`, і три різниці: `version` — мітка видання в шапці
                      документа, `prefix` — початок імені документа, спільний для видань однієї
                      специфікації («filter-effects»), і номер розділу, записаний у самому заголовку
                      («1. Introduction»), а не в окремому `<span class="secno">`.

Навіщо окремий читач, коли є `whatwg-html` і `spec-html`.

1. Видань кілька. Той самий розділ «Paths» є в SVG 1.1, у знімку SVG 2 і в чернетці редакторів, і пошук
   мусить уміти сказати, з якого видання текст. Читачі `webspecs` версії в шапку не пишуть.
2. Назва сторінки видання SVG стоїть у `<h1>` («Chapter 9: Paths», у SVG 1.1 — «8 Paths»), а `whatwg-html`
   бере назвою перший `<h2>`: документ звався б «9.1. Introduction», а не «Paths».
3. Формули. Перетворення координат, дуга еліпса й матриці фільтрів записані MathML. Спільний розбір
   піддерево `<math>` відкидає, і від розділу «Conversion from endpoint to center parameterization»
   лишилися б слова без жодної формули. Тут формула стає рядком тексту: `x_1`, `r_x^2`, `(a) / (b)`,
   `sqrt(...)`, а таблиця (матриця чи вектор) — рядки через «; » у квадратних дужках.
4. Службові блоки видання: рядок навігації «Top ⋅ Contents ⋅ Previous», заголовок «Contents» і підпис
   «View this example as SVG» не є текстом специфікації і в документ не йдуть.

Номери розділів лишаються тільки в назві документа («SVG 2: 9 Paths»), а з заголовків підрозділів і з
імені документа знімаються: «## 9.3. Path data» стає «## Path data». Причина — видань кілька, і нумерація
в них різна: «Paths» — розділ 8 у SVG 1.1 і розділ 9 у SVG 2, а в CSS Transforms властивість `transform`
описує розділ 4 опублікованої версії і розділ 3 чернетки редакторів. Пошук згортає видання одного розділу
в одне місце видачі за ключем «ім'я документа і шлях заголовків»; з номером у ключі той самий розділ трьох
видань займав би три місця з трьох. Послатися на розділ можна назвою й адресою сторінки.

У багатосторінкових виданнях позначки коду в рядку знімаються. Знімок SVG 2 пише назву елемента як
‘path’, а чернетка редакторів, зібрана Bikeshed, бере її ще й у `<code>`. З позначками незмінений абзац
двох видань різнився б самими лапками і не зливався б в один фрагмент із переліком обох видань, за яким
видно, чи чернетка вже відійшла від знімка. З тієї ж причини друкарський апостроф Bikeshed усередині
слова («viewport’s») стає прямим, як у знімку.

Сам розбір HTML — клас `_Spec` з `webspecs`: кроки алгоритмів з номерами, код у огорожах, пропуск
змісту й спливних панелей. Тут лише те, чим видання SVG відрізняються.
"""

import re
from html.parser import HTMLParser
from urllib.parse import urljoin

from engine.readers import Item, _markup, register
from engine.readers.webspecs import _DROP_ALWAYS, _Spec, _norm

# Службові блоки сторінки видання SVG, яких немає в `webspecs._SKIP_CLASS`.
_SKIP_CLASS = {"header", "view-as-svg", "bs-old-id", "expanding-toggle"}
_NUMBER = re.compile(r"^((?:\d+|[A-Z])(?:\.\d+)*)\.?\s+(\S.*)$")
_CHAPTER = re.compile(r"^(?:Chapter|Appendix)\s+(\d+|[A-Z])\s*:\s*(\S.*)$")
_SUB = re.compile(r"^(#{2,6}) (?:\d+|[A-Z])(?:\.\d+)+\.?\s+(?=\S)")
_APOSTROPHE = re.compile(r"(?<=\w)’(?=\w)")
_MATH = re.compile(r"<math\b.*?</math>", re.S | re.I)
_PAGE = re.compile(r"href=\"([A-Za-z0-9_-]+\.html)[\"#]")


# ── MathML → рядок ─────────────────────────────────────────────────────────

class _Tree(HTMLParser):
    """Формула MathML як дерево: вузол — [тег, атрибути, діти]; текст — рядок серед дітей."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = ["math", {}, []]
        self.path = [self.root]

    def handle_starttag(self, tag, attrs):
        node = [tag, {k: (v or "") for k, v in attrs}, []]
        self.path[-1][2].append(node)
        self.path.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.path) - 1, 0, -1):
            if self.path[i][0] == tag:
                del self.path[i:]
                return

    def handle_data(self, data):
        self.path[-1][2].append(data)


def _kids(node) -> list:
    return [c for c in node[2] if not isinstance(c, str)]


def _atom(text: str) -> str:
    """Операнд індексу, степеня чи дробу: складений вираз береться в дужки."""
    return text if re.fullmatch(r"[\w.′']+|\([^()]*\)", text) else f"({text})"


def _math(node) -> str:
    if isinstance(node, str):
        return node.strip()
    tag, attrs, kids = node[0], node[1], _kids(node)
    if tag in ("annotation", "annotation-xml"):
        return ""
    if tag in ("mi", "mn", "mo", "mtext", "ms"):
        text = _norm("".join(c for c in node[2] if isinstance(c, str)))
        return {"−": "-", "⁢": "", "⁡": "", "′": "'"}.get(text, text)
    parts = [_math(k) for k in kids]
    if tag == "msub" and len(parts) == 2:
        return f"{_atom(parts[0])}_{_atom(parts[1])}"
    if tag == "msup" and len(parts) == 2:
        return f"{_atom(parts[0])}{parts[1]}" if parts[1] == "'" else f"{_atom(parts[0])}^{_atom(parts[1])}"
    if tag == "msubsup" and len(parts) == 3:
        return f"{_atom(parts[0])}_{_atom(parts[1])}^{_atom(parts[2])}"
    if tag == "mfrac" and len(parts) == 2:
        return f"({parts[0]}) / ({parts[1]})"
    if tag == "msqrt":
        return f"sqrt({' '.join(p for p in parts if p)})"
    if tag == "mroot" and len(parts) == 2:
        return f"root({parts[0]}, {parts[1]})"
    if tag in ("mover", "munder", "munderover") and parts:
        # Надрядковий знак (стрілка вектора, риска) пишеться після основи, межі суми — в дужках.
        rest = [p for p in parts[1:] if p]
        if tag == "mover" and len(rest) == 1 and len(rest[0]) == 1:
            return f"{parts[0]}{rest[0]}" if rest[0] in "'′" else parts[0]
        return parts[0] + (f"[{', '.join(rest)}]" if rest else "")
    if tag == "mtable":
        return "[" + "; ".join(p for p in parts if p) + "]"
    if tag == "mtr":
        return ", ".join(p for p in parts if p and p != ",")
    if tag == "mfenced":
        inner = (attrs.get("separators", ",").strip()[:1] + " ").join(p for p in parts if p) \
            if len(kids) > 1 else "".join(parts)
        opened, closed = attrs.get("open", "("), attrs.get("close", ")")
        # Дужки навколо самої таблиці зайві: таблиця вже в квадратних.
        if len(kids) == 1 and kids[0][0] == "mtable":
            return inner
        if len(kids) == 1 and kids[0][0] == "mrow" and len(_kids(kids[0])) == 1 \
                and _kids(kids[0])[0][0] == "mtable":
            return inner
        return f"{opened}{inner}{closed}"
    return " ".join(p for p in parts if p)


def math_to_text(markup: str) -> str:
    """Формула `<math>…</math>` одним рядком; порожній рядок, коли в ній немає жодного знака."""
    tree = _Tree()
    tree.feed(markup)
    tree.close()
    text = " ".join(_math(tree.root).split())
    text = re.sub(r"\(\s+", "(", re.sub(r"\s+\)", ")", text))
    return re.sub(r"\b(cos|sin|tan|atan2?|arccos|arcsin|sqrt|mod|sign|abs)\s+\(", r"\1(", text)


def _with_formulas(html: str) -> str:
    """HTML, у якому кожна формула MathML замінена своїм текстом: виносна — окремим абзацом коду."""

    def repl(m):
        text = math_to_text(m.group(0))
        if not text:
            return " "
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        block = re.search(r"<math\b[^>]*\bdisplay\s*=\s*[\"']?block", m.group(0), re.I)
        return f"<p><code>{text}</code></p>" if block else f" <code>{text}</code> "

    return _MATH.sub(repl, html)


# ── сторінка видання SVG ───────────────────────────────────────────────────

class _Page(_Spec):
    """Сторінка видання SVG чи специфікації робочої групи: `_Spec` і службові блоки видання."""

    def __init__(self, split: bool, h1: bool):
        super().__init__(split)
        self.h1 = h1

    def handle_starttag(self, tag, attrs):
        if self.body and not self.skip_at and self.heading is None and self.pre is None \
                and tag not in ("br", "img", "hr", "wbr", "meta", "link", "input", "col"):
            a = {k: (v or "") for k, v in attrs}
            cls = set(a.get("class", "").split())
            contents = tag == "h2" and (a.get("id") in ("toc", "Contents") or "contents" in cls)
            if cls & _SKIP_CLASS or contents:
                self.stack.append(tag)
                self.skip_at = len(self.stack)
                return
            if tag == "h1" and self.h1 and not self.chapters:
                self.stack.append(tag)
                self._flush()
                self.heading = {"tag": tag, "id": a.get("id", ""), "num": [], "parts": [],
                                "in_num": 0}
                return
        super().handle_starttag(tag, attrs)


def _split_number(ch: dict) -> None:
    """Номер, записаний у самому заголовку («9. Paths», «Chapter 9: Paths»), — у поле `num`."""
    if ch["num"]:
        return
    m = _CHAPTER.match(ch["title"]) or _NUMBER.match(ch["title"])
    if m:
        ch["num"], ch["title"] = m.group(1), m.group(2).strip()


def _body(ch: dict, plain: bool = False) -> str:
    """Тіло документа; `plain` — без позначок коду в рядку (огорожі блоків коду лишаються)."""
    paras = [_SUB.sub(r"\1 ", p) for p in ch["paras"]]
    if plain:
        # Bikeshed ставить друкарський апостроф («viewport’s»), знімок пише прямий: зводиться до прямого.
        paras = [p if p.startswith("```") else _APOSTROPHE.sub("'", p.replace("`", "")) for p in paras]
    return "\n\n".join(paras).strip()


def _title(label: str, ch: dict) -> str:
    num = ch["num"]
    if num.isalpha():
        return f"{label}: Appendix {num}: {ch['title']}"
    return f"{label}: {num} {ch['title']}".replace("  ", " ").strip()


def _parse(html: str, split: bool, h1: bool) -> list[dict]:
    parser = _Page(split, h1)
    parser.feed(_with_formulas(html))
    parser.close()
    for ch in parser.chapters:
        _split_number(ch)
    return parser.chapters


@register("svg-chapters")
def svg_chapters(source: dict, ctx) -> list[Item]:
    index = source["url"]
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    pages = []
    for page in _PAGE.findall(ctx.text(index)):
        if page not in pages and not any(r.search(page) for r in exclude):
            pages.append(page)
    if not pages:
        raise SystemExit(f"{index}: у змісті немає посилань на сторінки видання — розмітка змінилася.")
    label = source.get("label") or source["title"]
    version = str(source.get("version") or "")
    items = []
    for page in pages:
        url = urljoin(index, page)
        if not ctx.allowed(url):
            raise SystemExit(f"{source['id']}: {url} поза білим списком.")
        name = _markup.slug(page[:-5])

        def make(url=url):
            chapters = _parse(ctx.text(url), split=False, h1=True)
            if not chapters:
                raise SystemExit(f"{url}: на сторінці немає заголовка — документ не записую.")
            ch = chapters[0]
            title, body = _title(label, ch), _body(ch, plain=True)
            _markup.require(title, body, url, min_chars=1)
            return _markup.document(title, url, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("spec-html-edition")
def spec_html_edition(source: dict, ctx) -> list[Item]:
    url = source["url"]
    chapters = [ch for ch in _parse(ctx.text(url), split=True, h1=False)
                if not _DROP_ALWAYS.match(ch["title"])]
    if not chapters:
        raise SystemExit(f"{url}: жодного розділу після змісту — розмітка змінилася.")
    label = source.get("label") or source["title"]
    version = str(source.get("version") or "")
    prefix = source.get("prefix") or source["id"]
    cite = source.get("cite") or url
    items, seen = [], set()
    for ch in chapters:
        name = _markup.slug(f"{prefix} {ch['title']}")
        if name in seen:
            raise SystemExit(f"{source['id']}: два розділи дають одне ім'я «{name}».")
        seen.add(name)

        def make(ch=ch):
            title, body = _title(label, ch), _body(ch)
            where = f"{cite}#{ch['id']}" if ch["id"] else cite
            _markup.require(title, body, where, min_chars=1)
            return _markup.document(title, where, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    return items
