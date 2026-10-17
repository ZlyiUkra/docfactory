"""Читач історії сайту Sphinx, сторінки якого написано в MyST Markdown (OCRmyPDF).

`ghdocs-history-myst` — те саме, що `ghdocs-history` (усі поля, зокрема `sphinx: true` для `.rst` старих
                        тегів), але текст кожного файла `.md` перед звичайним розбором проходить
                        `myst_to_markdown`.

Навіщо. OCRmyPDF до 16-ї версії писав документацію в reStructuredText, потім переписав її в MyST: директиви
в огорожах (`:::{note}` … `:::`, ```` ```{eval-rst} ````, `:::{list-table}`, `:::{versionadded} 16.0`), ролі
(`` {issue}`1234` ``, `` {ref}`назва <мітка>` ``, `` {func}`ocrmypdf.ocr` ``) і мітки розділів `(label)=`. Для
читача markdown це сирі рядки з двокрапками: виноска лягала б «:::{note}», таблиця змінних середовища —
переліком «* -», а опис змінних у вставці rST — блоком коду.

Що виходить. Виноски — підписом «Note:» і текстом; позначки версії — рядком «Added in version 16.0: …»;
`code` — блоком коду з підписом; `list-table` — таблицею markdown; вставка `eval-rst` — тим самим розбором
Sphinx, що й сторінки `.rst`; `toctree`, `image`, `literalinclude` зникають; ролі — словами чи кодом.

Чому окремий модуль, а не поле в `ghdocs-history`: спільний читач звірено в багатьох готових примірниках, а тут
досить підмінити текст файла, перш ніж читач його розбере (як `ghdocs-history-pod`).
"""

import re

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_FENCE = re.compile(r"^(?P<ind>[ \t]*)(?P<mark>`{3,}|:{3,})\{(?P<name>[\w:-]+)\}[ \t]*(?P<arg>.*)$")
_ADMON = {"note": "Note", "warning": "Warning", "tip": "Tip", "important": "Important", "caution": "Caution",
          "seealso": "See also", "attention": "Attention", "danger": "Danger", "hint": "Hint",
          "error": "Error", "todo": "To do"}
_VERSIONED = {"versionadded": "Added in version", "versionchanged": "Changed in version",
              "deprecated": "Deprecated since version", "versionremoved": "Removed in version"}
_DROP = {"toctree", "image", "literalinclude", "include", "contents", "autofunction", "autoclass", "automodule",
         "autodata", "automethod", "autoexception", "autosummary", "currentmodule", "module", "index"}
_CODE = {"code", "code-block", "sourcecode", "code-cell", "prompt"}
_ROLE = re.compile(r"\{([\w:-]+)\}`([^`]*)`")
_LABEL = re.compile(r"^\([\w.:-]+\)=[ \t]*$", re.M)


def _role(m) -> str:
    kind, body = m.group(1), m.group(2)
    titled = re.match(r"^(.*?)\s*<([^<>]+)>$", body, re.S)
    if kind == "issue":
        return f"issue #{body.strip()}"
    if kind in ("ref", "doc", "term", "numref", "any"):
        if titled and titled.group(1):
            return titled.group(1)
        return re.sub(r"[-_]+", " ", body.strip().lstrip("~").rsplit("/", 1)[-1])
    if titled and titled.group(1):
        return f"`{titled.group(1)}`"
    return f"`{body.strip().lstrip('~!')}`"


def _options(body: list[str]) -> tuple[dict, list[str]]:
    """Параметри директиви: блок YAML між `---` чи рядки `:ключ: значення` на початку тіла."""
    opts: dict = {}
    i = 0
    if body and body[0].strip() == "---":
        j = 1
        while j < len(body) and body[j].strip() != "---":
            k, _, v = body[j].partition(":")
            opts[k.strip()] = v.strip()
            j += 1
        i = j + 1
    while i < len(body):
        m = re.match(r"^\s*:([\w-]+):\s*(.*)$", body[i])
        if not m:
            break
        opts[m.group(1)] = m.group(2).strip()
        i += 1
    return opts, body[i:]


def _list_table(caption: str, opts: dict, body: list[str]) -> list[str]:
    """`list-table` → таблиця markdown: рядок — пункт «* -», клітинка — вкладений «-»."""
    rows: list[list[str]] = []
    for line in body:
        m = re.match(r"^\s*\*\s+-\s+(.*)$", line)
        if m:
            rows.append([m.group(1).strip()])
            continue
        m = re.match(r"^\s*-\s+(.*)$", line)
        if m and rows:
            rows[-1].append(m.group(1).strip())
            continue
        if line.strip() and rows:
            rows[-1][-1] += " " + line.strip()
    if not rows:
        return body
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    head = int(opts.get("header-rows", "0") or 0)
    out = [caption, ""] if caption else []
    first = rows[0] if head else [""] * width
    out.append("| " + " | ".join(c.replace("|", "\\|") for c in first) + " |")
    out.append("|" + "---|" * width)
    for r in rows[1 if head else 0:]:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
    return out


def _directive(name: str, arg: str, body: list[str]) -> list[str]:
    if name == "eval-rst":
        from engine.readers import _sphinx  # тут, а не нагорі: _sphinx тягне sitedocs, а той — ghhistory
        return ["", _sphinx.to_markdown("\n".join(body)), ""]
    opts, body = _options(body)
    if name in _DROP:
        caption = opts.get("caption") or opts.get("alt")
        return [caption] if caption and name == "image" else []
    if name == "figure":
        return ["", *myst_lines(body), ""]
    if name in _CODE:
        lang = arg.strip() or opts.get("language", "")
        caption = opts.get("caption", "")
        return ["", *([caption, ""] if caption else []), f"```{lang}", *body, "```", ""]
    if name == "list-table":
        return ["", *_list_table(arg.strip(), opts, body), ""]
    if name in _VERSIONED:
        version, _, rest = arg.strip().partition(" ")
        text = " ".join([rest.strip(), *[b.strip() for b in myst_lines(body) if b.strip()]]).strip()
        return ["", f"{_VERSIONED[name]} {version}" + (f": {text}" if text else "."), ""]
    if name in _ADMON or name == "admonition":
        label = _ADMON.get(name) or arg.strip() or "Note"
        inner = myst_lines(body)
        return ["", f"**{label}:**", "", *inner, ""]
    if name in ("envvar", "option", "describe", "object", "py:function", "function", "data", "py:data"):
        return ["", f"**{arg.strip()}**", "", *myst_lines(body), ""]
    return ["", *myst_lines(body), ""]


def myst_lines(lines: list[str]) -> list[str]:
    """Директиви MyST у переліку рядків — розгорнуті; вкладені огорожі (`::::` навколо `:::`) теж."""
    out: list[str] = []
    i = 0
    plain_fence = None
    while i < len(lines):
        line = lines[i]
        if plain_fence:
            out.append(line)
            if line.strip().startswith(plain_fence) and line.strip().strip(plain_fence[0]) == "":
                plain_fence = None
            i += 1
            continue
        m = _FENCE.match(line)
        if not m:
            pf = re.match(r"^\s*(`{3,}|~{3,})", line)
            if pf:
                plain_fence = pf.group(1)
            out.append(line)
            i += 1
            continue
        mark, ind = m.group("mark"), len(m.group("ind"))
        body = []
        i += 1
        depth = 0
        while i < len(lines):
            s = lines[i].strip()
            if _FENCE.match(lines[i]) and _FENCE.match(lines[i]).group("mark") == mark:
                depth += 1
            elif s == mark or (s.startswith(mark[0]) and set(s) == {mark[0]} and len(s) == len(mark)):
                if depth == 0:
                    break
                depth -= 1
            body.append(lines[i][ind:] if lines[i][:ind].strip() == "" else lines[i])
            i += 1
        i += 1
        out.extend(_directive(m.group("name"), m.group("arg"), body))
    return out


def myst_to_markdown(text: str) -> str:
    text = _LABEL.sub("", text.replace("\r\n", "\n"))
    lines = myst_lines(text.split("\n"))
    out, fence = [], None
    for line in lines:
        f = re.match(r"^\s*(`{3,}|~{3,})", line)
        if f and (fence is None or line.strip().startswith(fence)):
            fence = None if fence else f.group(1)
            out.append(line)
            continue
        out.append(line if fence else _ROLE.sub(_role, line))
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out))


class _Ctx:
    """Той самий контекст завантаження, лише текст файлів `.md` проходить `myst_to_markdown`."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        if not url.split("?", 1)[0].endswith(".md"):
            return text
        return myst_to_markdown(text)


@register("ghdocs-history-myst")
def ghdocs_history_myst(source: dict, ctx):
    return ghdocs_history(source, _Ctx(ctx))
