"""Розмітка документації CPython і PEP: те, чого не знає шар Sphinx (`_sphinx`).

Навіщо. У документації Python кожна функція, клас, метод і атрибут описані директивою домену
Python (`.. function:: dumps(obj, …)`, `.. method:: default(o)`), а модуль названо один раз на
початку сторінки (`.. module:: json`). Шар `_sphinx` робить із такої директиви рядок «Function:
`dumps(…)`» посеред тексту, і без цього шару сталося б таке:

- сторінка `json` лишалася б кількома розділами на 24 КБ, і запит про `json.dumps` повертав би
  шматок сторінки, де цієї назви може й не бути: її там написано лише як `dumps`;
- вкладені методи класу губили б ім'я класу, а в сигнатурі на кілька рядків (`\\` у кінці рядка)
  перший рядок ставав би кодом, а решта — окремим абзацом із відступом;
- ролі `:pep:` і `:rfc:` лишали б голе число, `:mod:`!json`` — знак оклику, а поля `:param:` —
  двокрапки навколо назви параметра.

Тут кожен запис API стає заголовком із повним іменем (`json.dumps`, `json.JSONEncoder.default`), а
сигнатура — блоком коду під ним. Рівень заголовка рахується від останнього звичайного заголовка
сторінки, тож метод стоїть під своїм класом, а той — під своїм розділом.

Журнал `Misc/NEWS.d/*.rst` має назву випуску лише в імені файла, а тему — у рядках над кожним
записом: тут із нього виходить документ із розділом на кожну тему.

Шапка PEP (`PEP: 8`, `Title: …`, `Status: …`) стає назвою документа і рядком стану: заголовка в
самому файлі PEP немає, а зі стану видно, чи пропозицію прийнято.
"""

import re

from engine.readers import _sphinx
from engine.readers.sitedocs import _rst_block, _rst_dedent

_DIRECTIVE = _sphinx._DIRECTIVE
# Записи мови й бібліотеки: ім'я йде першим у сигнатурі.
_PY = ("function", "class", "method", "classmethod", "staticmethod", "attribute", "data",
       "exception", "decorator", "decoratormethod", "coroutinefunction", "coroutinemethod",
       "abstractmethod", "property", "type", "py:function", "py:class", "py:method",
       "py:classmethod", "py:staticmethod", "py:attribute", "py:data", "py:exception",
       "py:decorator", "py:property")
# Записи C API: ім'я стоїть після типу результату. `cfunction` і подібні — запис Python 2.6–3.1.
_C = ("c:function", "c:type", "c:macro", "c:member", "c:var", "c:data", "c:struct", "c:union",
      "c:enum", "c:enumerator", "c:alias", "cfunction", "ctype", "cmacro", "cmember", "cvar")
# Записи, чиє ім'я — перше слово аргументу, без модуля.
_WORD = ("opcode", "envvar", "monitoring-event", "2to3fixer")
_OPTION = ("option", "cmdoption")
_WHOLE = ("describe", "object", "pdbcommand")
_DROP = ("moduleauthor", "sectionauthor", "testsetup", "testcleanup", "tabularcolumns",
         "codeauthor", "limited-api-list", "miscnews", "c:namespace")
_CODE = ("productionlist", "grammar-snippet", "doctest", "testcode", "testoutput")
_UNWRAP = ("container", "cssclass", "ifconfig", "tab-set", "versionhint")
_MODULE = ("module", "py:module", "currentmodule", "py:currentmodule")
_NO_MODULE = ("", "None", "builtins", "__builtin__")
_OPTION_LINE = re.compile(r"^\s*:[\w-]+:(\s|$)")
_FIELD = re.compile(r"^(\s*):(param|parameter|arg|argument|type|raises|raise|except|exception|"
                    r"returns|return|rtype|keyword|key|kwarg)(?:\s+([^:]+))?:\s*(.*)$")
_HEADER = re.compile(r"^([A-Z][\w-]*):\s*(.*)$")
_MARK = re.compile(r"PYAPIH(\d)X([0-9a-f]+)X")
_HEADING = re.compile(r"^(#{1,6}) (\S.*)$")
_NEWS_META = re.compile(r"^\.\.\s+([\w -]+):\s*(.*)$")


def _mark(depth: int, title: str) -> str:
    """Заголовок API, який переживе розбір rst: у ньому не лишається ні `*`, ні `_`."""
    return f"PYAPIH{min(depth, 5)}X{title.encode().hex()}X"


def _signatures(arg: str, block: list[str]) -> tuple[list[str], list[str]]:
    """Сигнатури директиви й тіло: аргумент триває до першого порожнього рядка.

    `\\` у кінці рядка — перенос однієї сигнатури, новий рядок без нього — ще одна сигнатура
    тієї ж функції (`min(iterable, …)` і `min(arg1, arg2, …)`)."""
    head = [arg]
    n = 0
    while n < len(block) and block[n].strip():
        if not _OPTION_LINE.match(block[n]):
            head.append(block[n].strip())
        n += 1
    joined: list[str] = []
    for part in head:
        if joined and joined[-1].endswith("\\"):
            joined[-1] = joined[-1][:-1].rstrip() + " " + part
        elif part:
            joined.append(part)
    return [re.sub(r"\\(.)", r"\1", s) for s in joined], block[n:]


def _py_name(sig: str, module: str, cls: str) -> str:
    m = re.match(r"(?:(?:async|await|abstract|class|static|final)\s+)*(@?[\w.]+)", sig)
    name = m.group(1) if m else sig.split("(")[0].strip()
    if cls and "." not in name:
        return f"{cls}.{name}"
    if module and not name.startswith(module + "."):
        return f"{module}.{name}"
    return name


def _c_name(sig: str) -> str:
    m = re.search(r"([A-Za-z_][\w.]*)\s*\(", sig)
    if m:
        return m.group(1)
    words = re.findall(r"[A-Za-z_][\w.]*", sig)
    return words[-1] if words else sig


class _Page:
    """Що сторінка оголосила вище за текстом: модуль і програма командного рядка."""

    def __init__(self) -> None:
        self.module = ""
        self.program = ""


def _walk(lines: list[str], page: _Page, depth: int = 1, cls: str = "") -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        d = _DIRECTIVE.match(ln)
        if not d:
            f = _FIELD.match(ln)
            if f:
                pad, kind, what, rest = f.groups()
                block, j = _rst_block(lines, i + 1, len(pad))
                words = (what or "").split()
                if kind in ("returns", "return"):
                    label = "Returns"
                elif kind == "rtype":
                    label = "Return type"
                elif kind in ("raises", "raise", "except", "exception"):
                    label = "Raises " + " ".join(words)
                elif kind == "type":
                    label = f"Type of {' '.join(words)}"
                else:
                    label = words[-1] if words else kind
                    if len(words) > 1:
                        label += f" ({' '.join(words[:-1])})"
                lines[i:j] = ["", f"{pad}**{label.strip()}:** {rest}".rstrip()] + \
                    [pad + x for x in _rst_dedent(block)] + [""]
                out.extend(lines[i:i + 2])
                i += 2
                continue
            out.append(ln)
            i += 1
            continue
        pad, name, arg = d.group(1), d.group(2).lower(), (d.group(3) or "").strip()
        block, j = _rst_block(lines, i + 1, len(pad))
        if name in _MODULE:
            page.module = "" if arg in _NO_MODULE else arg
            if name in _MODULE[:2] or depth == 1:
                cls = ""
            i = j
        elif name == "program":
            page.program = arg
            i = j
        elif name in _DROP:
            i = j
        elif name in _PY or name in _C or name in _WORD or name in _OPTION or name in _WHOLE:
            sigs, body = _signatures(arg, block)
            first = sigs[0] if sigs else ""
            kid_cls = cls
            if name in _PY:
                title = _py_name(first, page.module, cls)
                if name.split(":")[-1] in ("class", "exception", "type"):
                    kid_cls = title
            elif name in _C:
                title = _c_name(first)
            elif name in _WORD:
                title = first.split()[0] if first else name
            elif name in _OPTION:
                title = re.split(r",\s*", first)[0]
                title = f"{page.program} {title}" if page.program else title
            else:
                title = first[:80]
            out.extend(["", f"{pad}{_mark(depth, title)}", ""])
            if name not in _WORD or " " in first:
                out.extend([f"{pad}::", ""] + [f"{pad}   {s}" for s in sigs] + [""])
            inner = _walk(_rst_dedent(body), page, depth + 1, kid_cls)
            out.extend(pad + x if x.strip() else x for x in inner)
            out.append("")
            i = j
        elif name == "glossary":
            terms = _rst_dedent(block)
            k = 0
            while k < len(terms):
                t = terms[k]
                if t.strip() and t[0] != " " and not t.startswith(".."):
                    terms[k] = "\n" + _mark(depth, t.strip()) + "\n"
                k += 1
            out.extend(_walk("\n".join(terms).split("\n"), page, depth + 1, cls))
            i = j
        elif name == "deprecated-removed":
            parts = arg.split()
            note = " ".join(" ".join(x.split()) for x in block if x.strip())
            head = f"Deprecated since version {parts[0] if parts else '?'}"
            if len(parts) > 1:
                head += f", removed in version {parts[1]}"
            out.extend(["", f"{pad}{head}" + (f": {note}" if note else "."), ""])
            i = j
        elif name == "audit-event":
            parts = arg.split(None, 1)
            event = parts[0] if parts else ""
            what = parts[1].split()[0] if len(parts) > 1 else ""
            tail = f" with arguments `{what}`" if what and what != "." else ""
            out.extend(["", f"{pad}Raises an auditing event `{event}`{tail}.", ""])
            i = j
        elif name == "impl-detail":
            out.extend(["", f"{pad}**CPython implementation detail:** {arg}".rstrip(), ""])
            out.extend(_walk([pad + x for x in _rst_dedent(block)], page, depth, cls))
            i = j
        elif name == "availability":
            out.extend(["", f"{pad}Availability: {arg}", ""])
            i = j
        elif name == "rubric":
            out.extend(["", f"{pad}**{arg}**", ""])
            i = j
        elif name in _CODE:
            _, body = _signatures(arg, block)
            kept = _rst_dedent(body)
            if kept:
                out.extend(["", f"{pad}::", ""] + [f"{pad}   {x}" for x in kept] + [""])
            i = j
        elif name == "only":
            if "latex" not in arg and "man" not in arg.split():
                out.extend(_walk([pad + x for x in _rst_dedent(block)], page, depth, cls))
            i = j
        elif name in _UNWRAP:
            _, body = _signatures("", block)
            out.extend(_walk([pad + x for x in _rst_dedent(body)], page, depth, cls))
            i = j
        else:
            out.append(ln)
            i += 1
    return out


def _roles(text: str) -> str:
    """Ролі, для яких шар Sphinx не знає, що показати: без цього лишається голе число."""
    # Роль, перенесена на другий рядок: спільний розбір rst працює порядково й лишив би її як є.
    text = re.sub(r"(:[\w:-]+:`[^`\n]*)\n[ \t]*([^`\n]*`)", r"\1 \2", text)
    text = re.sub(r"(:[\w:-]+:`)!", r"\1", text)
    text = re.sub(r":pep:`([^`<]+?)\s*<(\d+)[^`>]*>`", r"\1 (PEP \2)", text, flags=re.I)
    text = re.sub(r":pep:`(\d+)[^`]*`", r"PEP \1", text, flags=re.I)
    text = re.sub(r":rfc:`([^`<]+?)\s*<(\d+)[^`>]*>`", r"\1 (RFC \2)", text, flags=re.I)
    text = re.sub(r":rfc:`(\d+)[^`]*`", r"RFC \1", text, flags=re.I)
    text = re.sub(r":(?:issue|bpo):`(\d+)`", r"bpo-\1", text)
    text = re.sub(r":gh:`(\d+)`", r"gh-\1", text)
    text = re.sub(r":cve:`([\d-]+)`", r"CVE-\1", text)
    text = re.sub(r":cwe:`(\d+)`", r"CWE-\1", text)
    # Посилання на виноску: сама виноска лишається в кінці сторінки.
    return re.sub(r"\s*\[(?:#[\w-]*|\d+)\]_", "", text)


def _pep(text: str) -> str:
    """Шапка PEP → назва й рядок стану; решта файла — звичайний rst."""
    lines = text.split("\n")
    fields: dict[str, str] = {}
    n, last = 0, ""
    while n < len(lines) and lines[n].strip():
        m = _HEADER.match(lines[n])
        if m:
            last = m.group(1)
            fields[last] = m.group(2).strip()
        elif last:
            fields[last] += " " + lines[n].strip()
        n += 1
    title = f"PEP {fields.get('PEP', '').strip()} – {fields.get('Title', '').strip()}"
    state = [f"{k}: {fields[k]}" for k in ("Status", "Type", "Topic", "Created", "Python-Version",
                                           "Author", "Requires", "Replaces", "Superseded-By",
                                           "Resolution") if fields.get(k)]
    return "\n".join([title, "#" * max(len(title), 4), "", ". ".join(state) + ".", ""] + lines[n:])


def _news(text: str, path: str) -> str:
    """Файл `Misc/NEWS.d/3.14.0.rst` → розділ на кожну тему, запис журналу — пункт списку.

    Назви випуску у файлі немає: вона лише в імені файла. Записи розділяє рядок `..`, а тему й
    номер завдання кожен запис несе у своїх рядках `.. section:`, `.. gh-issue:`."""
    sections: dict[str, list[str]] = {}
    meta: dict[str, str] = {}
    body: list[str] = []
    released = ""

    def flush() -> None:
        nonlocal meta, body
        kept = _rst_dedent(body)
        while kept and not kept[-1].strip():
            kept.pop()
        if kept:
            ref = f"gh-{meta['gh-issue']}" if meta.get("gh-issue") else \
                f"bpo-{meta['bpo']}" if meta.get("bpo") else ""
            first = f"{ref}: {kept[0]}" if ref and ref != "gh-0" and ref != "bpo-0" else kept[0]
            sections.setdefault(meta.get("section") or "Other", []).extend(
                ["", f"- {first}"] + [f"  {x}" if x.strip() else x for x in kept[1:]])
        meta, body = {}, []

    for ln in text.split("\n"):
        m = _NEWS_META.match(ln)
        if m:
            meta[m.group(1)] = m.group(2).strip()
            if m.group(1) == "release date":
                released = m.group(2).strip()
        elif ln.strip() == "..":
            flush()
        else:
            body.append(ln)
    flush()
    title = "Python " + path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    out = [title, "#" * len(title), ""]
    if released:
        out += [f"Released {released}.", ""]
    for name, items in sections.items():
        out += [name, "=" * max(len(name), 4)] + items + [""]
    return "\n".join(out)


def to_markdown(text: str, path: str = "") -> str:
    """Сторінка документації CPython чи PEP (`.rst`) → markdown із заголовком на кожен запис API."""
    text = text.replace("\r\n", "\n").expandtabs(8)
    if "/NEWS.d/" in path:
        text = _news(text, path)
    elif text.startswith("PEP:"):
        text = _pep(text)
    text = "\n".join(_walk(_roles(text).split("\n"), _Page()))
    out: list[str] = []
    level = 1
    for ln in _sphinx.to_markdown(text).split("\n"):
        h = _HEADING.match(ln)
        if h:
            level = len(h.group(1))
            ln = ln.replace(" --- ", " — ")
        # Записи без порожнього рядка між ними розбір rst склеює в один абзац.
        for part in re.split(rf"\s*({_MARK.pattern})\s*", ln) if "PYAPIH" in ln else [ln]:
            m = _MARK.fullmatch(part)
            if m:
                depth = min(level + int(m.group(1)), 6)
                out.extend(["", "#" * depth + " " + bytes.fromhex(m.group(2)).decode(), ""])
            elif not re.fullmatch(r"\d|[0-9a-f]+", part) or "PYAPIH" not in ln:
                out.append(part)
    return "\n".join(out)
