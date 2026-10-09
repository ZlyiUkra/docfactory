"""Читач посібників Texinfo з репозиторію GitHub на тегах випусків.

`gh-texinfo` — `url`      — дерево теки документації через API
                            (…/repos/ВЛАСНИК/РЕПО/git/trees/), тег і теку дописує сам
                            читач: …/git/trees/n7.1.5:doc;
               `raw`      — корінь сирих файлів (https://raw.githubusercontent.com/ВЛАСНИК/РЕПО/);
               `blob`     — корінь людських адрес (https://github.com/ВЛАСНИК/РЕПО/blob/);
               `folder`   — тека посібників у репозиторії («doc»);
               `versions` — теги випусків, від найновішого;
               `tag_prefix` — що зрізати з тегу, щоб лишилась версія («n»: n7.1.5 → 7.1.5);
               `flags`    — прапорці @set, з якими збирає документацію сам проєкт
                            (FFmpeg: config-not-all і config-<бібліотека>);
               `manuals`  — імена посібників (файлів без «.texi», «-doc» зрізано), що беруться;
                            решта файлів теки — частини, які посібники підтягують через
                            `@include`, або зведені «-all», що повторюють решту;
               `schemas`  — файли XML Schema тієї самої теки, що стають окремими документами
                            (ffprobe.xsd — схема виводу ffprobe);
               `label`    — підпис продукту в назві документа («FFmpeg»).

Навіщо. FFmpeg пише документацію у Texinfo (doc/*.texi), а сайт ffmpeg.org показує лише
редакцію з гілки розробки, перебудовану щоночі, — без вибору версії. Посібник кожного
випуску є тільки в його тезі, і лише у вигляді вихідного Texinfo: готових info чи HTML у
репозиторії немає, тож `gnu-info` тут не годиться.

Одиниця — посібник у випуску. Посібник — файл теки з `@settitle` (ffmpeg.texi,
ffmpeg-filters.texi, faq.texi…); решта файлів (filters.texi, muxers.texi,
fftools-common-opts.texi) — частини, які посібники підтягують через `@include`. Чи файл
посібник, видно лише з його тексту, тож перелік посібників задає `manuals`: інакше `list`
мусив би тягнути кожен файл кожного тегу. Посібник, у тексті якого немає `@settitle`,
не записується — значить, `manuals` розійшовся з репозиторієм. У FFmpeg 0.6–0.7
посібники звалися «ffmpeg-doc.texi» — суфікс «-doc» зрізається, щоб посібник мав те саме
ім'я в усіх версіях. Ім'я документа — посібник і хеш тегу: `revision_suffix` зрізає хеш, і
однакові розділи сусідніх випусків зливаються в один фрагмент з усіма версіями.

Перелік — одне звернення до API на тег (вміст теки); тексти тягнуться лише під час
запису, і файли тегу кешуються, поки читач не перейде до наступного тегу: спільні частини
(fftools-common-opts.texi, authors.texi) не качаються для кожного посібника знову.

Розбір. Розділи Texinfo стають заголовками markdown (`@chapter` — «##», `@section` —
«###», `@subsection` — «####», `@subsubsection` — «#####»), таблиці опцій — пунктами
«- `-show_format`» з описом одразу під ними, приклади — огорожами коду, @multitable —
таблицею. Умовні блоки розкриваються так, як їх розкриває HTML-збірка проєкту:
@ifhtml береться, @iftex/@ifnothtml/@ignore — ні, @ifset — за `flags`. Макроси
(@macro … @end macro) підставляються. Однаковий шлях заголовків усередині посібника
отримує номер («Examples 2»), бо ключ фрагмента — цей шлях.
"""

import hashlib
import json
import re

from engine.readers import Item, _markup, register

_HEADINGS = {
    2: ("chapter", "unnumbered", "appendix", "majorheading", "chapheading", "heading",
        "centerchap"),
    3: ("section", "unnumberedsec", "appendixsec", "appendixsection", "subheading"),
    4: ("subsection", "unnumberedsubsec", "appendixsubsec", "subsubheading"),
    5: ("subsubsection", "unnumberedsubsubsec", "appendixsubsubsec"),
}
_LEVEL = {name: level for level, names in _HEADINGS.items() for name in names}

# Блоки, вміст яких HTML-збірка показує, і ті, яких не показує.
_KEEP = {"ifhtml", "ifnottex", "ifnotinfo", "ifnotplaintext", "ifnotdocbook", "ifnotxml",
         "ifnotlatex"}
_DROP = {"iftex", "ifinfo", "ifnothtml", "ifplaintext", "ifdocbook", "ifxml", "iflatex",
         "ignore", "tex", "html", "titlepage", "menu", "direntry", "detailmenu", "copying",
         "documentdescription", "latex", "docbook", "xml"}
_CONDITIONAL = _KEEP | _DROP | {"ifset", "ifclear"}

# Рядкові команди без тексту для читача.
_SKIP_LINE = {
    "setfilename", "documentencoding", "documentlanguage", "top", "contents", "shortcontents",
    "summarycontents", "page", "sp", "node", "cindex", "findex", "kindex", "pindex",
    "tindex", "vindex", "printindex", "need", "vskip", "noindent", "indent",
    "setchapternewpage", "paragraphindent", "firstparagraphindent", "syncodeindex",
    "synindex", "defindex", "defcodeindex", "headings", "finalout", "smallbook",
    "dircategory", "insertcopying", "frenchspacing", "allowcodebreaks", "kbdinputstyle",
    "exampleindent", "footnotestyle", "setcontentsaftertitlepage", "clickstyle",
    "codequoteundirected", "codequotebacktick", "deftypefnnewline", "xrefautomaticsectiontitle",
    "everyheading", "everyfooting", "evenheading", "oddheading", "evenfooting", "oddfooting",
    "author", "subtitle", "title", "vskip", "raisesections", "lowersections", "anchor",
    "documentdescription",
}
_CODE = {"code", "samp", "option", "command", "env", "file", "kbd", "key", "verb",
         "indicateurl"}
_PLAIN = {"var", "emph", "strong", "b", "i", "t", "r", "sc", "dfn", "cite", "asis",
          "slanted", "sansserif", "titlefont", "w", "math", "center", "headitemfont",
          "clicksequence", "sub", "sup", "U"}
_SYMBOL = {
    "dots": "...", "enddots": "...", "tie": " ", "minus": "-", "copyright": "©",
    "registeredsymbol": "®", "bullet": "•", "result": "=>", "expansion": "==>",
    "equiv": "==", "error": "error-->", "print": "-|", "point": "-!-", "TeX": "TeX",
    "LaTeX": "LaTeX", "today": "", "comma": ",", "atchar": "@", "lbracechar": "{",
    "rbracechar": "}", "backslashchar": "\\", "hashchar": "#", "geq": ">=", "leq": "<=",
    "arrow": "->", "click": "->", "euro": "€", "pounds": "£", "textdegree": "°",
    "exclamdown": "¡", "questiondown": "¿", "ss": "ß", "l": "ł", "L": "Ł", "o": "ø",
    "O": "Ø", "ae": "æ", "AE": "Æ", "oe": "œ", "OE": "Œ", "aa": "å", "AA": "Å",
    "dotless": "", "quotedblleft": '"', "quotedblright": '"', "quoteleft": "'",
    "quoteright": "'", "guillemetleft": "«", "guillemetright": "»", "ordf": "ª",
    "ordm": "º", "image": "", "footnote": "",
}
_ESCAPE = {"@": "@", "{": "{", "}": "}", "*": " ", ".": ".", ":": "", "!": "!", "?": "?",
           " ": " ", "\t": " ", "\n": " ", "-": "", "/": "", "&": "&", ",": ",", "=": "",
           "'": "", '"': "", "^": "", "`": "", "~": "", "\\": "\\", "|": "|"}
_ACCENT = set("'\"^`~=,") | {"H", "dotaccent", "ringaccent", "tieaccent", "u", "ubaraccent",
                             "udotaccent", "v", "ogonek"}


def _braced(text: str, start: int) -> tuple[str, int]:
    """(вміст фігурних дужок, позиція після закривної) від відкривної на `start`."""
    depth, i = 0, start
    while i < len(text):
        c = text[i]
        if c == "@" and i + 1 < len(text):
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    return text[start + 1:], len(text)


def _args(text: str) -> list[str]:
    """Аргументи команди через кому — лише коми верхнього рівня, не в дужках."""
    out, depth, cur, i = [], 0, [], 0
    while i < len(text):
        c = text[i]
        if c == "@" and i + 1 < len(text):
            cur.append(text[i:i + 2])
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        if c == "," and depth == 0:
            out.append("".join(cur).strip())
            cur = []
        else:
            cur.append(c)
        i += 1
    out.append("".join(cur).strip())
    return out


def inline(text: str, code: bool = False) -> str:
    """Рядок Texinfo → текст: @code{x} → `x` (у прикладі коду — просто x), посилання —
    назвою, символи — собою. Невідома команда з дужками лишає свій вміст."""
    out, i = [], 0
    while i < len(text):
        c = text[i]
        if c != "@":
            out.append(c)
            i += 1
            continue
        if i + 1 >= len(text):
            i += 1
            continue
        nxt = text[i + 1]
        m = re.match(r"[A-Za-z]+", text[i + 1:])
        if not m:
            if nxt in "'\"^`~=," and i + 2 < len(text):
                # Наголос: @'{e} чи @'e — лишається сама буква.
                if text[i + 2] == "{":
                    inner, i = _braced(text, i + 2)
                    out.append(inline(inner, code))
                else:
                    out.append(text[i + 2])
                    i += 3
                continue
            out.append(_ESCAPE.get(nxt, nxt))
            i += 2
            continue
        name = m.group(0)
        j = i + 1 + len(name)
        if j < len(text) and text[j] == "{":
            inner, i = _braced(text, j)
        else:
            # Команда без дужок посеред тексту (@tab у таблиці обробляється раніше).
            i = j
            if name in _SYMBOL:
                out.append(_SYMBOL[name])
            elif name in _ACCENT and i < len(text) and text[i] == " ":
                i += 1
            continue
        if name in _CODE:
            body = inline(inner, True)
            out.append(body if code else f"`{body}`")
        elif name in ("url", "uref"):
            a = _args(inner) + ["", ""]
            href, label, alt = inline(a[0], True), inline(a[1], code), inline(a[2], code)
            out.append(alt or (f"{label} ({href})" if label else href))
        elif name == "email":
            a = _args(inner) + [""]
            out.append(inline(a[1], code) or inline(a[0], True))
        elif name in ("ref", "xref", "pxref", "inforef"):
            a = _args(inner) + ["", "", "", ""]
            target = inline(a[2] or a[1] or a[0], code)
            if a[3]:
                target += f" ({inline(a[3], True)})"
            out.append({"xref": "See ", "pxref": "see "}.get(name, "") + target)
        elif name in ("acronym", "abbr"):
            a = _args(inner) + [""]
            out.append(inline(a[0], code) + (f" ({inline(a[1], code)})" if a[1] else ""))
        elif name in ("anchor", "image", "footnote", "caption", "shortcaption", "errormsg"):
            if name == "footnote":
                out.append(f" (footnote: {inline(inner, code)})")
        elif name in _SYMBOL and not inner.strip():
            out.append(_SYMBOL[name])
        else:
            out.append(inline(inner, code))
    return "".join(out)


def _expand_macros(text: str) -> str:
    """Означення @macro … @end macro — геть із тексту, виклики — підставлені."""
    macros: dict[str, tuple[list[str], str]] = {}

    def define(m):
        params = [p.strip() for p in (m.group(2) or "").split(",") if p.strip()]
        macros[m.group(1)] = (params, m.group(3))
        return ""

    text = re.sub(r"^@r?macro\s+(\w+)\s*(?:\{([^}]*)\})?[ \t]*\n(.*?)^@end r?macro[ \t]*$\n?",
                  define, text, flags=re.M | re.S)
    if not macros:
        return text
    pattern = re.compile(r"@(" + "|".join(map(re.escape, sorted(macros, key=len,
                                                                reverse=True))) + r")\b")
    for _ in range(4):                              # макрос у макросі — кілька проходів
        out, i, changed = [], 0, False
        for m in pattern.finditer(text):
            if m.start() < i:
                continue
            params, body = macros[m.group(1)]
            end = m.end()
            values: list[str] = []
            if end < len(text) and text[end] == "{":
                inner, end = _braced(text, end)
                values = _args(inner) if len(params) > 1 else [inner]
            for k, p in enumerate(params):
                body = body.replace(f"\\{p}\\", values[k] if k < len(values) else "")
            out.append(text[i:m.start()])
            out.append(body.rstrip("\n"))
            i, changed = end, True
        out.append(text[i:])
        text = "".join(out)
        if not changed:
            break
    return text


def _conditionals(lines: list[str], flags: set[str]) -> list[str]:
    """Розкриває умовні блоки так, як HTML-збірка: лишає рядки показаних гілок."""
    flags = set(flags)
    out, stack = [], []                         # stack: (ім'я блоку, чи показується)
    for line in lines:
        m = re.match(r"^@(\w+)(?:\s+(.*?))?\s*$", line)
        name = m.group(1) if m else ""
        shown = all(keep for _, keep in stack)
        inside_ignore = any(n in ("ignore", "tex", "html", "latex") for n, _ in stack)
        if name == "end" and m.group(2):
            block = m.group(2).split()[0]
            if block in _CONDITIONAL and stack and stack[-1][0] == block:
                stack.pop()
                continue
            if inside_ignore:
                continue
        elif name in _CONDITIONAL and not inside_ignore:
            if name in ("ifset", "ifclear"):
                flag = (m.group(2) or "").split()[0] if m.group(2) else ""
                keep = (flag in flags) == (name == "ifset")
            else:
                keep = name in _KEEP
            stack.append((name, keep))
            continue
        elif name in ("ignore", "tex", "html", "latex") and inside_ignore:
            stack.append((name, False))
            continue
        if not shown:
            continue
        if name == "set" and m.group(2):
            flags.add(m.group(2).split()[0])
            continue
        if name == "clear" and m.group(2):
            flags.discard(m.group(2).split()[0])
            continue
        out.append(line)
    return out


class _Writer:
    """Збирає markdown: абзаци, пункти списків, огорожі коду, таблиці."""

    def __init__(self):
        self.lines: list[str] = []
        self.para: list[str] = []
        self.lists: list[dict] = []             # таблиці опцій, переліки, нумеровані
        self.glue = False                       # опис пункту — одразу під ним, без порожнього рядка
        self.paths: dict[str, int] = {}
        self.stack: list[tuple[int, str]] = []

    def _emit(self, text: str, glue: bool = False):
        if not glue and self.lines and self.lines[-1] != "":
            self.lines.append("")
        self.lines.append(text)

    def flush(self):
        if self.para:
            text = " ".join(" ".join(self.para).split())
            # Лапки й тире Texinfo — ``так'' і --- — у тексті, не в коді.
            text = re.sub(r"(?<!@)``|''", '"', text).replace("---", "—")
            text = inline(text)
            text = " ".join(text.split())
            if text:
                self._emit(text, self.glue)
            self.glue = False
        self.para = []

    def heading(self, level: int, title: str):
        self.flush()
        self.lists.clear()
        title = " ".join(inline(title).split()) or "Untitled"
        self.stack = [(lv, t) for lv, t in self.stack if lv < level]
        path = "/".join(t.lower() for _, t in self.stack + [(level, title)])
        seen = self.paths.get(path, 0) + 1
        self.paths[path] = seen
        if seen > 1:
            title = f"{title} {seen}"
        self.stack.append((level, title))
        self._emit("#" * level + " " + title)
        self.lines.append("")
        self.glue = False

    def item(self, term: str):
        self.flush()
        depth = max(len(self.lists) - 1, 0)
        top = self.lists[-1] if self.lists else {"kind": "itemize"}
        lead = "  " * depth
        if top["kind"] == "table":
            fmt = top.get("fmt") or "asis"
            shown = inline(f"@{fmt}{{{term}}}" if term.strip() else "")
            self._emit(f"{lead}- {' '.join(shown.split())}", top.get("open", False))
            top["open"] = True                  # @itemx — під попереднім пунктом
            self.glue = True
            return
        top["n"] = top.get("n", 0) + 1
        mark = f"{top['n']}." if top["kind"] == "enumerate" else "-"
        self.para = [f"{lead}{mark}"] + ([term] if term.strip() else [])
        self.glue = False

    def code(self, lines: list[str], raw: bool):
        self.flush()
        body = [ln if raw else inline(ln, True) for ln in lines]
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()
        if body:
            self._emit("```", self.glue)
            self.lines.extend(body)
            self.lines.append("```")
        self.glue = False

    def table(self, rows: list[tuple[bool, list[str]]]):
        self.flush()
        if not rows:
            return
        width = max(len(cells) for _, cells in rows)
        out = []
        for k, (head, cells) in enumerate(rows):
            cells = [" ".join(inline(" ".join(c.split())).split()) for c in cells]
            cells += [""] * (width - len(cells))
            out.append("| " + " | ".join(cells) + " |")
            if head and (k + 1 == len(rows) or not rows[k + 1][0]):
                out.append("|" + "---|" * width)
        self._emit(out[0], self.glue)
        self.lines.extend(out[1:])
        self.glue = False

    def text(self) -> str:
        self.flush()
        return re.sub(r"\n{3,}", "\n\n", "\n".join(self.lines)).strip()


def texinfo_to_markdown(source: str, flags=()) -> tuple[str, str]:
    """(назва з @settitle, тіло markdown) посібника, чиї @include уже розкрито."""
    source = _expand_macros(source.replace("\r\n", "\n"))
    lines = _conditionals(source.split("\n"), set(flags))
    title, w = "", _Writer()
    block: list[str] | None = None             # рядки поточного прикладу
    block_end, raw = "", False
    rows: list[tuple[bool, list[str]]] | None = None
    for line in lines:
        if block is not None:
            if re.match(rf"^@end\s+{block_end}\b", line):
                w.code(block, raw)
                block = None
            else:
                block.append(line)
            continue
        m = re.match(r"^@(\w+)(?:[ \t]+(.*?))?[ \t]*$", line)
        name, arg = (m.group(1), m.group(2) or "") if m else ("", "")
        if line.startswith("\\input") or name in ("c", "comment"):
            continue
        if name == "bye":
            break
        if rows is not None:
            if name == "end" and arg.startswith("multitable"):
                w.table(rows)
                rows = None
                continue
            if line.startswith(("@item", "@headitem")):
                head = line.startswith("@headitem")
                rest = re.sub(r"^@(head)?item\b\s*", "", line)
                rows.append((head, [c.strip() for c in re.split(r"@tab\b", rest)]))
            elif rows and line.strip():
                parts = re.split(r"@tab\b", line)
                rows[-1][1][-1] += " " + parts[0].strip()
                rows[-1][1].extend(p.strip() for p in parts[1:])
            continue
        if name == "settitle":
            title = " ".join(inline(arg).split())
            continue
        if name in _LEVEL:
            w.heading(_LEVEL[name], arg)
            continue
        if name in _SKIP_LINE:
            continue
        if name in ("example", "smallexample", "lisp", "smalllisp", "verbatim"):
            w.flush()
            block, block_end, raw = [], name, name == "verbatim"
            continue
        if name in ("display", "smalldisplay", "format", "smallformat", "flushleft",
                    "flushright", "raggedright"):
            w.flush()
            block, block_end, raw = [], name, False
            continue
        if name in ("table", "ftable", "vtable"):
            w.flush()
            fmt = arg.lstrip("@").split()[0] if arg.strip() else "asis"
            w.lists.append({"kind": "table", "fmt": fmt})
            continue
        if name in ("itemize", "enumerate"):
            w.flush()
            w.lists.append({"kind": name})
            continue
        if name == "multitable":
            w.flush()
            rows = []
            continue
        if name in ("item", "itemx"):
            if name == "item" and w.lists:
                w.lists[-1]["open"] = False
            w.item(arg)
            continue
        if name == "end":
            block_name = arg.split()[0] if arg else ""
            if block_name in ("table", "ftable", "vtable", "itemize", "enumerate"):
                w.flush()
                if w.lists:
                    w.lists.pop()
            elif block_name in ("quotation", "smallquotation", "cartouche", "float", "group"):
                w.flush()
            continue
        if name in ("quotation", "smallquotation"):
            w.flush()
            if arg.strip():
                w.para = [f"{arg.strip()}:"]
            continue
        if name in ("cartouche", "float", "group", "center"):
            w.flush()
            if name == "center" and arg.strip():
                w.para = [arg]
                w.flush()
            continue
        if not line.strip():
            w.flush()
            continue
        if re.match(r"^@anchor\{[^}]*\}\s*$", line):
            continue
        w.para.append(line)
    return title, chunk_tables(w.text())


TABLE_ROWS = 20


def chunk_tables(body: str) -> str:
    """Довга таблиця (перелік форматів і кодеків у general — сотні рядків) — шматками по
    TABLE_ROWS рядків, кожен зі своєю шапкою, через порожній рядок. Фрагмент ріже текст
    лише по порожніх рядках, і цільна таблиця ставала одним фрагментом на 12 тисяч знаків,
    хвіст якого модель векторів не бачить."""
    out, table, fence = [], [], False

    def flush():
        if not table:
            return
        head = []
        if len(table) > 1 and set(table[1].replace("|", "")) <= {"-"}:
            head, rows = table[:2], table[2:]
        else:
            rows = table
        if len(rows) <= TABLE_ROWS:
            out.extend(table)
        else:
            for k in range(0, len(rows), TABLE_ROWS):
                if k:
                    out.append("")
                out.extend(head + rows[k:k + TABLE_ROWS])
        table.clear()

    for line in body.split("\n"):
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("| "):
            table.append(line)
            continue
        flush()
        out.append(line)
    flush()
    return "\n".join(out)


def schema_to_markdown(xsd: str) -> str:
    """XML Schema → розділ на кожен тип: «### streamType» і його означення в огорожі.
    Схема цілком — одна огорожа на десятки кілобайт, яку фрагмент не поділить."""
    body = xsd.replace("\r\n", "\n").strip()
    parts = re.split(r"(?m)^(?=\s*<xsd:(?:complexType|simpleType|element)\s+name=\")", body)
    out = []
    for k, part in enumerate(parts):
        part = part.strip("\n")
        if not part.strip():
            continue
        name = re.match(r'\s*<xsd:(\w+)\s+name="([^"]+)"', part)
        head = f"## {name.group(2)} ({name.group(1)})" if name and k else "## Schema header"
        lines = part.split("\n")
        pad = min((len(ln) - len(ln.lstrip()) for ln in lines if ln.strip()), default=0)
        out.append(f"{head}\n\n```xml\n" + "\n".join(ln[pad:] for ln in lines) + "\n```")
    return "\n\n".join(out)


def _version(tag: str, prefix: str) -> str:
    return tag[len(prefix):] if prefix and tag.startswith(prefix) else tag


@register("gh-texinfo")
def gh_texinfo(source: dict, ctx) -> list[Item]:
    need = ("raw", "blob", "versions")
    if any(not source.get(k) for k in need):
        raise SystemExit(f"{source['id']}: читач gh-texinfo потребує полів {', '.join(need)}.")
    tree_base = source["url"].rstrip("/") + "/"
    raw_base, blob_base = source["raw"].rstrip("/") + "/", source["blob"].rstrip("/") + "/"
    folder = source.get("folder", "doc").strip("/")
    prefix = source.get("tag_prefix", "")
    flags = set(source.get("flags") or ())
    manuals = set(source.get("manuals") or ())
    if not manuals:
        raise SystemExit(f"{source['id']}: читач gh-texinfo потребує поля manuals.")
    schemas = set(source.get("schemas") or ())
    label = source.get("label", "")
    cache: dict = {"tag": None, "files": {}}

    def fetch(tag: str, path: str) -> str | None:
        """Файл теки на тезі; None — такого файла в тезі немає (config.texi генерує збірка)."""
        if cache["tag"] != tag:
            cache["tag"], cache["files"] = tag, {}
        if path not in cache["files"]:
            names = cache.get(("names", tag))
            if names is not None and path not in names:
                cache["files"][path] = None
            else:
                url = f"{raw_base}{tag}/{folder}/{path}"
                if not ctx.allowed(url):
                    raise SystemExit(f"{url}: поза білим списком.")
                cache["files"][path] = ctx.text(url)
        return cache["files"][path]

    def assemble(tag: str, path: str, depth: int = 0) -> str:
        text = fetch(tag, path)
        if text is None:
            return ""
        if depth > 8:
            raise SystemExit(f"{tag}/{path}: @include вкладено глибше восьми рівнів.")
        out = []
        for line in text.replace("\r\n", "\n").split("\n"):
            inc = re.match(r"^@(include|verbatiminclude)\s+(\S+)\s*$", line)
            if not inc:
                out.append(line)
                continue
            part = assemble(tag, inc.group(2), depth + 1) if inc.group(1) == "include" \
                else (fetch(tag, inc.group(2)) or "")
            if inc.group(1) == "verbatiminclude" and part:
                part = f"@verbatim\n{part.rstrip()}\n@end verbatim"
            out.append(part)
        return "\n".join(out)

    items = []
    for tag in source["versions"]:
        tree_url = f"{tree_base}{tag}:{folder}"
        if not ctx.allowed(tree_url):
            raise SystemExit(f"{tree_url}: поза білим списком.")
        try:
            tree = json.loads(ctx.text(tree_url))
        except ValueError as exc:
            raise SystemExit(f"{tree_url}: відповідь не JSON ({exc}) — перелік не складено.")
        names = {e["path"] for e in tree.get("tree") or () if e.get("type") == "blob"}
        if not names:
            raise SystemExit(f"{tree_url}: тека порожня або тегу немає.")
        cache[("names", tag)] = names
        version = _version(tag, prefix)
        digest = hashlib.sha1(tag.encode()).hexdigest()[:8]
        for path in sorted(names):
            stem = path.rsplit(".", 1)[0]
            if path in schemas:
                doc = f"{_markup.slug(path.replace('.', '-'))}-{digest}"

                def make(tag=tag, path=path, version=version):
                    text = fetch(tag, path) or ""
                    body = schema_to_markdown(text)
                    title = f"{path} — XML Schema of the output ({label} {version})"
                    _markup.require(title, body, f"{raw_base}{tag}/{folder}/{path}")
                    return _markup.document(title, f"{blob_base}{tag}/{folder}/{path}",
                                            ctx.stamp, body, version)
            elif path.endswith(".texi") and re.sub(r"-doc$", "", stem) in manuals:
                manual = re.sub(r"-doc$", "", stem)
                doc = f"{_markup.slug(manual)}-{digest}"

                def make(tag=tag, path=path, version=version, manual=manual):
                    text = assemble(tag, path)
                    if not re.search(r"^@settitle\b", text, re.M):
                        raise SystemExit(f"{tag}/{path}: не посібник (немає @settitle).")
                    title, body = texinfo_to_markdown(text, flags)
                    title = f"{title or manual} ({label} {version})"
                    _markup.require(title, body, f"{raw_base}{tag}/{folder}/{path}")
                    return _markup.document(title, f"{blob_base}{tag}/{folder}/{path}",
                                            ctx.stamp, body, version)
            else:
                continue
            items.append(Item(id=f"{source['id']}/{doc}", file=f"{source['id']}--{doc}.txt",
                              make=make))
    return items
