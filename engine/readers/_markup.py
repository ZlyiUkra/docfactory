"""Спільне для читачів документації сайтів: шапка документа і зведення розмітки до тексту.

Сайти віддають сторінку в трьох формах — markdown (зокрема MDX з компонентами й
старий Jekyll з тегами Liquid), HTML і серіалізоване дерево елементів Next.js. Тут
усі три зводяться до одного вигляду: заголовок окремим рядком «## Назва» з
порожніми рядками навколо, код між огорожами «```», пункт списку з «- », решта —
звичайні абзаци. Саме по таких заголовках `common/corpus.py` у режимі `markdown`
ділить документ на фрагменти, і саме тому огорожі коду тут бережуться: рядок
«# коментар» усередині коду заголовком не стає.

Посилання зводяться до свого тексту: адреса в тілі абзацу — шум для пошуку по
словах, а джерело документа й так лежить у шапці.
"""

import html as html_lib
import re
from html.parser import HTMLParser
from urllib.parse import urljoin

# Найкоротше тіло, яке ще може бути документом без жодного заголовка. Сторінка-
# заглушка («This page has moved.», тіло помилки) до цієї межі не дотягує.
MIN_BODY = 120

# Компоненти MDX, чия роль — підпис до вмісту. Сам вміст лишається, а підпис
# стає рядком перед ним: «Pitfall:» у тексті — це те, що людина бачить рамкою.
LABELS = {
    "Pitfall": "Pitfall:", "Note": "Note:", "DeepDive": "Deep Dive:",
    "Solution": "Solution:", "Hint": "Hint:", "YouWillLearn": "You will learn:",
    "LearnMore": "Learn more:", "Recap": "Recap:", "Challenges": "Challenges:",
    "Canary": "Canary only:", "Wip": "Under construction:",
    "Deprecated": "Deprecated:", "Experimental": "Experimental:",
    "RSC": "React Server Components:", "ServerComponents": "Server Components:",
    "Gotcha": "Gotcha:", "Intro": "", "Recipes": "Examples:",
}

_HEADINGS = ("h1", "h2", "h3", "h4", "h5", "h6")


def document(title: str, url: str, stamp: str, body: str, version: str = "") -> str:
    """Готовий документ корпусу: шапка з трьох рядків (плюс версія, коли вона є),
    порожній рядок, тіло."""
    head = f"# {' '.join(title.split())}\n# джерело: {url}\n# отримано: {stamp}\n"
    if version:
        head += f"# версія: {version}\n"
    return f"{head}\n{body}\n"


def require(title: str, body: str, where: str, min_chars: int = MIN_BODY) -> None:
    """Відмова винятком для сторінки, якої читач не впізнав. Та сама відмова, що
    в читачах ecmarkup: куций документ не має права лягти поверх доброго."""
    if not title.strip():
        raise SystemExit(f"Сторінка не схожа на документ ({where}): немає назви — "
                         f"документ не записую, наявний лишається як був.")
    if len(body) < min_chars and not re.search(r"^#{2,6} \S", body, re.M):
        raise SystemExit(f"Сторінка не схожа на документ ({where}): тіло куце "
                         f"({len(body)} символів) і без жодного заголовка — "
                         f"документ не записую.")


def refuse_html(text: str, where: str) -> None:
    """Markdown-адреса, що відповіла HTML, — це сторінка помилки чи редирект на
    оболонку сайту, а не документ."""
    if text.lstrip()[:15].lower().startswith(("<!doctype", "<html")):
        raise SystemExit(f"Замість markdown прийшов HTML ({where}) — документ не записую.")


def slug(text: str) -> str:
    """Ім'я документа для файла й ідентифікатора: латиниця, цифри й дефіси."""
    return "-".join(re.findall(r"[a-z0-9]+", text.lower())) or "index"


def github_anchor(heading: str) -> str:
    """Якір, який GitHub ставить заголовку markdown: «19.3.0 (September 9, 2026)»
    → «1930-september-9-2026»."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


# ── markdown / MDX / Jekyll ───────────────────────────────────────────────

_FRONT = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)
_FENCE = re.compile(r"^\s*(```+|~~~+)\s*([\w+#.-]*)")
_HEADING_MD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_COMPONENT = re.compile(r"^\s*<(/?)([A-Z][A-Za-z0-9.]*)(\s[^<>]*)?/?>\s*$")
_COMPONENT_OPEN = re.compile(r"^\s*<[A-Z][A-Za-z0-9.]*(\s[^<>]*)?$")
_LIQUID_HL = re.compile(r"^\s*\{%\s*highlight\s+([\w+#-]+)[^%]*%\}\s*$")
_LIQUID_END = re.compile(r"^\s*\{%\s*endhighlight\s*%\}\s*$")
_LIQUID = re.compile(r"^\s*\{%.*%\}\s*$")
_CODE_SPAN = re.compile(r"(`+)(.+?)\1")
_IMG = re.compile(r"!\[([^\]]*)\]\((?:[^()]|\([^)]*\))*\)")
_LINK = re.compile(r"\[([^\]]+)\]\(((?:[^()]|\([^)]*\))*)\)")
_REFLINK = re.compile(r"\[([^\]]+)\]\[[^\]]*\]")
_TAG = re.compile(r"</?[A-Za-z][\w.-]*(?:\s[^<>]*)?/?>")
_ANCHOR = re.compile(r"\s*\{/\*.*?\*/\}")


def title_of(meta: dict, url: str) -> str:
    """Назва документа з шапки YAML. Шапку пишуть люди, і вона буває з друкарською
    помилкою: у react.dev сторінка `<script>` має `script: "<script>"` замість
    `title:`. Без запасного шляху така сторінка відмовлялася як «без назви», тож
    назвою стає єдине поле шапки, а без нього — останній сегмент адреси."""
    if meta.get("title"):
        return meta["title"]
    if len(meta) == 1:
        return next(iter(meta.values()))
    tail = url.rstrip("/").rsplit("/", 1)[-1]
    return re.sub(r"\.md$", "", tail)


def front_matter(text: str) -> tuple[dict, str]:
    """(поля шапки YAML, решта тексту). Розбирається лише простий «ключ: значення»
    — більше читачам не треба, а бібліотека YAML тягнула б залежність."""
    text = text.replace("\r\n", "\n").lstrip("﻿")
    m = _FRONT.match(text)
    if not m:
        return {}, text
    meta = {}
    for ln in m.group(1).splitlines():
        key, sep, value = ln.partition(":")
        if sep and key.strip() and not key[:1].isspace():
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, text[m.end():]


def _inline(line: str, links_base: str | None = None) -> str:
    """Рядок тексту без посилань, якорів і тегів — окрім того, що в `коді`. З
    `links_base` посилання не зводиться до тексту, а лишає поруч адресу в дужках:
    на сторінці-мапі (перелік версій з посиланнями на анонси й релізи) адреса і є
    змістом, а відносна стає повною від `links_base`."""
    line = _ANCHOR.sub("", line)
    line = _IMG.sub(r"\1", line)
    if links_base is None:
        line = _LINK.sub(r"\1", line)
    else:
        line = _LINK.sub(lambda m: (f"{m.group(1)} ({urljoin(links_base, m.group(2).split()[0])})"
                                    if m.group(2).strip() else m.group(1)), line)
    line = _REFLINK.sub(r"\1", line)
    parts, pos = [], 0
    for m in _CODE_SPAN.finditer(line):
        parts.append(html_lib.unescape(_TAG.sub("", line[pos:m.start()])))
        parts.append(m.group(0))
        pos = m.end()
    parts.append(html_lib.unescape(_TAG.sub("", line[pos:])))
    return "".join(parts)


def _component(tag: str) -> list[str]:
    """Рядки, якими стає рядок-компонент MDX: підпис і назва, якщо вони є."""
    out = [""]
    m = re.match(r"\s*<(/?)([A-Z][A-Za-z0-9.]*)", tag)
    if m and not m.group(1):
        label = LABELS.get(m.group(2))
        if label:
            out += [label, ""]
        t = re.search(r'\b(?:titleText|title|alt)="([^"]*)"', tag)
        if t:
            out += [t.group(1), ""]
    return out


def _closes(line: str, fence: str) -> bool:
    s = line.strip()
    return bool(s) and set(s) == {fence[0]} and len(s) >= len(fence)


# Власний якір заголовка Gatsby («## Basic Hooks {#basic-hooks}»). Лишений у тексті, він
# потрапляв у шлях розділу («basic-hooks-basic-hooks») і в підпис, і той самий розділ
# знімка репозиторію не збігався з розділом сайту, де якоря в заголовку не видно.
_HEADING_ID = re.compile(r"\s*\{#[\w-]+\}\s*$")


def markdown_body(text: str, links_base: str | None = None) -> str:
    """Тіло markdown у вигляді корпусу. Шапку YAML знімає front_matter, не ця
    функція. `links_base` — лишати адреси посилань (див. _inline)."""
    lines: list[str] = []
    fence, comment, pending = "", False, None
    for raw in text.replace("\r\n", "\n").split("\n"):
        ln = raw.rstrip()
        if fence:
            if (_LIQUID_END.match(ln) if fence == "{%" else _closes(ln, fence)):
                lines.append("```")
                fence = ""
            else:
                lines.append(ln)
            continue
        if pending is not None:
            pending += " " + ln.strip()
            if ">" in ln:
                lines.extend(_component(pending))
                pending = None
            continue
        if comment:
            if "-->" not in ln:
                continue
            ln, comment = ln.split("-->", 1)[1], False
        while "<!--" in ln:
            before, _, after = ln.partition("<!--")
            if "-->" in after:
                ln = before + after.split("-->", 1)[1]
            else:
                ln, comment = before, True
        m = _LIQUID_HL.match(ln)
        if m:
            lines.append("```" + m.group(1))
            fence = "{%"
            continue
        if _LIQUID.match(ln):
            continue
        m = _FENCE.match(ln)
        if m:
            lines.append("```" + m.group(2))
            fence = m.group(1)
            continue
        if _COMPONENT.match(ln):
            lines.extend(_component(ln))
            continue
        if _COMPONENT_OPEN.match(ln):
            pending = ln.strip()
            continue
        m = _HEADING_MD.match(ln)
        if m:
            title = _inline(_HEADING_ID.sub("", m.group(2)), links_base).strip()
            if title:
                lines.extend(["", "#" * max(2, len(m.group(1))) + " " + title, ""])
            continue
        lines.append(_inline(ln, links_base))
    if fence:
        lines.append("```")
    return tidy("\n".join(lines), strip=False)


def tidy(text: str, strip: bool) -> str:
    """Порожні рядки по одному, код між огорожами як є. `strip` вирівнює рядки
    тексту до лівого краю — для HTML і дерева, де відступ нічого не означає; у
    markdown відступ лишається, бо рядок «    ## …» — це код, а не заголовок."""
    out: list[str] = []
    fence = False
    for ln in text.split("\n"):
        if ln.startswith("```"):
            fence = not fence
            out.append(ln.rstrip())
            continue
        if fence:
            out.append(ln.rstrip())
            continue
        ln = ln.replace("\xa0", " ").rstrip()
        if strip:
            ln = re.sub(r"[ \t]+", " ", ln).strip()
        if not ln.strip():
            if out and out[-1] == "":
                continue
            out.append("")
            continue
        out.append(ln)
    if fence:
        out.append("```")
    return "\n".join(out).strip("\n")


# ── HTML ──────────────────────────────────────────────────────────────────

class _HtmlText(HTMLParser):
    """HTML статті → текст корпусу. Підсвітка коду Gatsby кладе виділені рядки в
    <span class="gatsby-highlight-code-line"> без символу переносу — перенос тоді
    дописується на закритті такого span, інакше два рядки коду злиплися б."""

    _SKIP = {"script", "style", "svg", "noscript", "iframe", "template", "button"}
    _BLOCK = {"p", "div", "ul", "ol", "table", "blockquote", "section", "figure",
              "figcaption", "dl", "dt", "dd", "tr", "hr", "details", "summary",
              "article", "header", "footer", "aside", "main"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0
        self.pre = False
        self.spans: list[str] = []

    def _nl(self, n: int = 2) -> None:
        if "".join(self.out[-2:]).endswith("- "):
            return
        self.out.append("\n" * n)

    def _tail(self) -> str:
        return self.out[-1] if self.out else ""

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        a = dict(attrs)
        if self.pre:
            if tag == "span":
                self.spans.append(a.get("class") or "")
            elif tag == "br":
                self.out.append("\n")
            return
        if tag in _HEADINGS:
            self._nl()
            self.out.append("#" * max(2, int(tag[1])) + " ")
        elif tag == "pre":
            m = re.search(r"(?:gatsby-code-|language-)([\w+#-]+)", a.get("class") or "")
            self._nl()
            self.out.append("```" + (m.group(1) if m else "") + "\n")
            self.pre, self.spans = True, []
        elif tag == "code":
            self.out.append("`")
        elif tag == "li":
            self._nl(1)
            self.out.append("- ")
        elif tag == "br":
            self.out.append("\n")
        elif tag == "img":
            if a.get("alt"):
                self.out.append(a["alt"])
        elif tag in ("td", "th"):
            self.out.append(" | ")
        elif tag in self._BLOCK:
            self._nl()

    def handle_endtag(self, tag):
        if tag in self._SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if self.pre:
            if tag == "span" and self.spans:
                if ("gatsby-highlight-code-line" in self.spans.pop()
                        and not self._tail().endswith("\n")):
                    self.out.append("\n")
            elif tag == "pre":
                if not self._tail().endswith("\n"):
                    self.out.append("\n")
                self.out.append("```")
                self._nl()
                self.pre = False
            return
        if tag in _HEADINGS:
            self._nl()
        elif tag == "code":
            self.out.append("`")
        elif tag == "li":
            self._nl(1)
        elif tag in self._BLOCK:
            self._nl()

    def handle_data(self, data):
        if self.skip:
            return
        self.out.append(data if self.pre else re.sub(r"\s+", " ", data))


def html_body(html: str) -> str:
    parser = _HtmlText()
    parser.feed(html)
    parser.close()
    return tidy("".join(parser.out), strip=True)


# ── дерево елементів Next.js ──────────────────────────────────────────────

_INLINE = {"a", "strong", "em", "b", "i", "span", "kbd", "sup", "sub", "del", "s",
           "u", "abbr", "small", "mark", "CodeStep", "Math", "MathI"}


def _is_el(node) -> bool:
    return (isinstance(node, list) and len(node) == 4 and node[0] == "$r"
            and isinstance(node[1], str) and isinstance(node[3], dict))


def _raw(node) -> str:
    if isinstance(node, str):
        return node
    if isinstance(node, (int, float)) and not isinstance(node, bool):
        return str(node)
    if _is_el(node):
        return _raw(node[3].get("children"))
    if isinstance(node, list):
        return "".join(_raw(x) for x in node)
    return ""


def tree_body(tree) -> str:
    """Серіалізоване дерево сторінки Next.js (вузол — ["$r", тип, ключ, props])
    → текст корпусу. Правила ті самі, що для HTML і MDX."""
    out: list[str] = []

    def nl(n: int = 2) -> None:
        if "".join(out[-2:]).endswith("- "):
            return
        out.append("\n" * n)

    def walk(node) -> None:
        if isinstance(node, str):
            out.append(re.sub(r"\s+", " ", node))
            return
        if isinstance(node, bool) or node is None or isinstance(node, dict):
            return
        if isinstance(node, (int, float)):
            out.append(str(node))
            return
        if not isinstance(node, list):
            return
        if not _is_el(node):
            for x in node:
                walk(x)
            return
        kind, props = node[1], node[3]
        kids = props.get("children")
        if kind in _HEADINGS:
            nl()
            out.append("#" * max(2, int(kind[1])) + " ")
            walk(kids)
            nl()
        elif kind == "pre":
            cls = kids[3].get("className") if _is_el(kids) else ""
            m = re.search(r"language-([\w+#-]+)", cls if isinstance(cls, str) else "")
            nl()
            out.append("```" + (m.group(1) if m else "") + "\n"
                       + _raw(kids).rstrip("\n") + "\n```")
            nl()
        elif kind == "code":
            out.append("`" + _raw(kids) + "`")
        elif kind == "li":
            nl(1)
            out.append("- ")
            walk(kids)
            nl(1)
        elif kind == "br":
            out.append("\n")
        elif kind == "img":
            if isinstance(props.get("alt"), str):
                out.append(props["alt"])
        elif kind in ("td", "th"):
            out.append(" | ")
            walk(kids)
        elif kind == "InlineToc":
            return
        elif kind in _INLINE:
            walk(kids)
        elif kind[:1].isupper():
            nl()
            if LABELS.get(kind):
                out.append(LABELS[kind])
                nl()
            for key in ("titleText", "title", "alt"):
                if isinstance(props.get(key), str) and props[key].strip():
                    out.append(props[key])
                    nl()
                    break
            walk(kids)
            nl()
        else:
            nl()
            walk(kids)
            nl()

    walk(tree)
    return tidy("".join(out), strip=True)
