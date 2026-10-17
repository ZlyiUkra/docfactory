"""Розмітка довідки LibreOffice (`.xhp`) → markdown корпусу. Помічник читача `ghdocs-history-xhp`.

Довідка help.libreoffice.org збирається з репозиторію `LibreOffice/help`: кожна сторінка — файл XML
`helpdocument` зі своїм словником. Що з ним робиться:
- заголовки: нові файли пишуть `<h1>`…`<h6>`, старі (3.x–5.x) — `<paragraph role="heading" level="N">`;
- абзаци `paragraph` за роллю: `code`/`bascode`/`pycode` — рядки коду (сусідні зливаються в один блок),
  `note`/`tip`/`warning` — з підписом, решта — звичайний текст; так само елементи `<note>`, `<tip>`,
  `<warning>`, `<bascode>`, `<pycode>` нових файлів;
- `<embed href="файл#id"/>` і `<embedvar>` вставляють розділ, абзац чи змінну іншої сторінки того самого
  знімка — без цього розділи «Syntax»/«Example» функцій Calc і рядки «To access this command» порожні;
- `<switch>`/`<switchinline>` (варіанти для Windows, macOS, Linux чи для програм Writer, Calc…) —
  усі варіанти з підписами, як їх показує онлайн-довідка перемикачем;
- `<bookmark_value>` — терміни покажчика довідки («parameters;command line») — рядком «Index:» під
  найближчим заголовком: це синоніми, якими люди шукають сторінку;
- `<ahelp visibility="hidden">`, коментарі, картинки й «Related Topics» (самі посилання) — геть;
- `$[officename]`, `%PRODUCTNAME` — «LibreOffice», `%PRODUCTVERSION` — лінія знімка.
"""

import hashlib
import re
import xml.etree.ElementTree as ET

PRODUCT = "LibreOffice"
_NAME = re.compile(r"\$\[officename\]|%PRODUCTNAME|\$\[officeproductname\]")
_VERSION = re.compile(r"%PRODUCTVERSION|\$\[officeversion\]")
_AMP = re.compile(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)")
EMBED = re.compile(r'<embed(?:var)?\s+href="/?([^"#]+)#([^"]+)"')
_CODE_ROLES = {"code": "", "bascode": "basic", "pycode": "python", "codeparagraph": ""}
_MARKS = {"note": "Note", "tip": "Tip", "warning": "Warning"}
_HEAD = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}
_SKIP = {"comment", "image", "object", "video", "alt", "meta", "bookmark", "embedvar_dummy"}
_LABELS = {"WIN": "Windows", "MAC": "macOS", "UNIX": "Linux", "UNX": "Linux", "LINUX": "Linux",
           "WRITER": "Writer", "CALC": "Calc", "IMPRESS": "Impress", "DRAW": "Draw", "MATH": "Math",
           "CHART": "Chart", "BASIC": "Basic", "DATABASE": "Base", "BASE": "Base"}
_BLOCKS = {"paragraph", "h1", "h2", "h3", "h4", "h5", "h6", "list", "table", "section", "switch", "embed",
           "note", "tip", "warning", "bascode", "pycode", "sort", "listitem", "tablerow"}


def parse(text: str):
    """Дерево сторінки; старі файли бувають з голим «&» — його екрануємо й пробуємо вдруге."""
    for attempt in (text, _AMP.sub("&amp;", text)):
        try:
            return ET.fromstring(attempt)
        except ET.ParseError:
            continue
    return None


def ids(root) -> dict:
    return {el.get("id"): el for el in root.iter() if el.get("id")}


def fingerprint(el) -> str:
    """Відбиток вставленого елемента: вставка змінюється — змінюється й сторінка, що її вставляє."""
    return hashlib.sha1(ET.tostring(el)).hexdigest()


def refs(el) -> list[tuple[str, str]]:
    """Вставки всередині елемента — пари «шлях від text/…, id»."""
    out = []
    for sub in el.iter():
        if sub.tag in ("embed", "embedvar") and sub.get("href"):
            href = sub.get("href").lstrip("/")
            if "#" in href:
                path, _, ident = href.partition("#")
                out.append((path, ident))
    return out


class Render:
    """Перетворення одного документа. `resolve(path, id)` дає елемент вставки того самого знімка
    (або None), `version` — лінія для %PRODUCTVERSION."""

    def __init__(self, resolve, version: str):
        self.resolve = resolve
        self.version = version
        self.out: list[tuple[str, str]] = []
        self.index: list[str] = []
        self.title = ""

    # --- рядки ---
    def sub(self, s: str) -> str:
        return _VERSION.sub(self.version, _NAME.sub(PRODUCT, s))

    def inline(self, el, depth: int = 0) -> str:
        parts = [el.text or ""]
        for ch in el:
            parts.append(self._inline_child(ch, depth))
            parts.append(ch.tail or "")
        return "".join(parts)

    def _inline_child(self, ch, depth: int) -> str:
        tag = ch.tag
        if tag in _SKIP or (tag == "ahelp" and ch.get("visibility") == "hidden"):
            return ""
        if tag == "br":
            return "\n"
        if tag in ("literal", "input") or (tag == "item" and ch.get("type") in ("literal", "input")):
            txt = " ".join(self.inline(ch, depth).split())
            return f"`{txt}`" if txt else ""
        if tag == "embedvar":
            if depth > 4:
                return ""
            target = self._target(ch.get("href", ""))
            return self.inline(target, depth + 1) if target is not None else ""
        if tag == "switchinline":
            return self._switch_inline(ch, depth)
        return self.inline(ch, depth)

    def _switch_inline(self, el, depth: int) -> str:
        kind = el.get("select", "")
        default, cases = "", []
        for ch in el:
            text = " ".join(self.inline(ch, depth).split())
            if ch.tag == "defaultinline":
                default = text
            elif ch.tag == "caseinline" and text:
                cases.append(f"{_LABELS.get(ch.get('select', ''), ch.get('select', '').title())}: {text}")
        if kind == "sys" and default and cases:
            return f"{default} ({'; '.join(cases)})"
        if default and cases:
            return f"{default} ({'; '.join(cases)})"
        return default or "; ".join(cases)

    def _target(self, href: str):
        href = href.lstrip("/")
        if "#" not in href:
            return None
        path, _, ident = href.partition("#")
        return self.resolve(path, ident)

    # --- блоки ---
    def para(self, text: str, kind: str = "p") -> None:
        text = self.sub(text)
        if kind == "p":
            text = " ".join(text.split())
            if not text:
                return
            if self.index:
                self.out.append(("p", "Index: " + " · ".join(self.index)))
                self.index = []
        else:
            text = text.strip("\n")
            if not text.strip():
                return
        self.out.append((kind, text))

    def heading(self, level: int, text: str) -> None:
        text = " ".join(self.sub(text).split())
        if not text:
            return
        if level == 1 and (not self.title or text == self.title):
            self.title = self.title or text
            return
        self.out.append(("h", "#" * max(2, level) + " " + text))
        if self.index:
            self.out.append(("p", "Index: " + " · ".join(self.index)))
            self.index = []

    def blocks(self, el, depth: int = 0, top: bool = False) -> None:
        if el.text and el.text.strip() and el.tag not in ("body", "helpdocument"):
            self.para(el.text)
        for ch in el:
            self.block(ch, depth, top)
            if ch.tail and ch.tail.strip():
                self.para(ch.tail)

    def block(self, ch, depth: int, top: bool = False) -> None:
        tag = ch.tag
        if tag == "bookmark":
            if top:
                for v in ch.iter("bookmark_value"):
                    val = " ".join(self.sub("".join(v.itertext())).split())
                    if val and val not in self.index:
                        self.index.append(val)
            return
        if tag in _SKIP or (tag == "ahelp" and ch.get("visibility") == "hidden"):
            return
        if tag in _HEAD:
            self.heading(_HEAD[tag], self.inline(ch, depth))
        elif tag == "paragraph":
            self._paragraph(ch, depth)
        elif tag == "list":
            self._list(ch, depth)
        elif tag == "table":
            self._table(ch, depth)
        elif tag == "section":
            if ch.get("id") == "relatedtopics":
                return
            if ch.get("id") == "howtoget":
                self.para("To access this command:")
            self.blocks(ch, depth, top)
        elif tag == "switch":
            self._switch(ch, depth, top)
        elif tag == "embed":
            if depth > 4:
                return
            target = self._target(ch.get("href", ""))
            if target is None:
                return
            if target.tag in ("paragraph",) or target.tag in _HEAD:
                self.block(target, depth + 1)
            elif target.tag == "variable" and not any(c.tag in _BLOCKS for c in target):
                self.para(self.inline(target, depth + 1))
            else:
                self.blocks(target, depth + 1)
        elif tag in _MARKS:
            before = len(self.out)
            self.blocks(ch, depth, top)
            for i in range(before, len(self.out)):
                if self.out[i][0] == "p":
                    self.out[i] = ("p", f"{_MARKS[tag]}: {self.out[i][1]}")
                    break
        elif tag in ("bascode", "pycode"):
            lang = "basic" if tag == "bascode" else "python"
            for p in ch.iter("paragraph"):
                self.para(self.inline(p, depth), f"code:{lang}")
        elif tag == "embedvar":
            self.para(self._inline_child(ch, depth))
        elif tag == "variable" or tag == "sort" or any(c.tag in _BLOCKS for c in ch):
            if any(c.tag in _BLOCKS for c in ch):
                self.blocks(ch, depth, top)
            else:
                self.para(self.inline(ch, depth))
        else:
            self.para(self.inline(ch, depth))

    def _paragraph(self, p, depth: int) -> None:
        role = p.get("role", "paragraph")
        if p.get("visibility") == "hidden":
            return
        if role == "heading":
            self.heading(int(p.get("level") or 2), self.inline(p, depth))
        elif role in _CODE_ROLES:
            self.para(self.inline(p, depth), f"code:{_CODE_ROLES[role]}")
        elif role in _MARKS:
            self.para(f"{_MARKS[role]}: {self.inline(p, depth)}")
        else:
            self.para(self.inline(p, depth))

    def _sub_render(self, el, depth: int) -> list[tuple[str, str]]:
        """Вміст пункту списку чи клітинки — окремим проходом, щоб скласти його в один рядок."""
        saved, saved_index = self.out, self.index
        self.out, self.index = [], []
        self.blocks(el, depth)
        got, self.out, self.index = self.out, saved, saved_index
        return got

    def _list(self, el, depth: int) -> None:
        ordered = el.get("type") == "ordered"
        lines, n = [], 0
        for item in el:
            if item.tag != "listitem":
                continue
            n += 1
            mark = f"{n}. " if ordered else "- "
            pad = " " * len(mark)
            first = True
            for kind, text in self._sub_render(item, depth):
                if kind.startswith("code"):
                    body = "\n".join(pad + ln for ln in [f"```{kind[5:]}", *text.split("\n"), "```"])
                    lines.append(body if not first else mark + body.lstrip())
                else:
                    chunk = "\n".join((mark if first and i == 0 else pad) + ln
                                      for i, ln in enumerate(text.split("\n")))
                    lines.append(chunk)
                first = False
        if lines:
            self.out.append(("raw", "\n".join(lines)))

    def _table(self, el, depth: int) -> None:
        rows = []
        for row in el.iter("tablerow"):
            cells = []
            for cell in row:
                if cell.tag != "tablecell":
                    continue
                parts = []
                for kind, text in self._sub_render(cell, depth):
                    parts.append(" ".join(text.split()) if not kind.startswith("code")
                                 else "`" + " ".join(text.split()) + "`")
                cells.append(" ".join(parts).replace("|", "\\|"))
            if any(cells):
                rows.append(cells)
        if not rows:
            return
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        lines = ["| " + " | ".join(rows[0]) + " |", "|" + " --- |" * width]
        lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
        if self.index:
            self.out.append(("p", "Index: " + " · ".join(self.index)))
            self.index = []
        self.out.append(("raw", "\n".join(lines)))

    def _switch(self, el, depth: int, top: bool) -> None:
        kind = el.get("select", "")
        for ch in el:
            if ch.tag not in ("case", "default"):
                continue
            if ch.tag == "default":
                label = "Other systems" if kind == "sys" else "Otherwise"
            else:
                name = _LABELS.get(ch.get("select", ""), ch.get("select", "").title())
                label = f"On {name}" if kind == "sys" else f"In {name}"
            self.para(f"{label}:")
            self.blocks(ch, depth, top)

    # --- збирання ---
    def markdown(self) -> str:
        chunks, code, lang = [], [], None
        for kind, text in self.out + [("end", "")]:
            if kind.startswith("code:"):
                if code and kind[5:] != lang:
                    chunks.append(f"```{lang}\n" + "\n".join(code) + "\n```")
                    code = []
                lang = kind[5:]
                code.append(text.rstrip())
                continue
            if code:
                chunks.append(f"```{lang}\n" + "\n".join(code) + "\n```")
                code, lang = [], None
            if kind != "end":
                chunks.append(text)
        return "\n\n".join(chunks).strip() + "\n"


def to_markdown(root, resolve, version: str) -> tuple[str, str]:
    """(назва, тіло) сторінки довідки."""
    r = Render(resolve, version)
    title_el = root.find("./meta/topic/title")
    if title_el is not None:
        r.title = " ".join(r.sub("".join(title_el.itertext())).split())
    body = root.find("body")
    if body is not None:
        r.blocks(body, 0, top=True)
    return r.title, r.markdown()
