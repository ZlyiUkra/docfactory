"""Розмітка Sphinx поверх reStructuredText: те, що спільний розбір rst (sitedocs.rst) не знає.

Навіщо. Сайт Certbot (eff-certbot.readthedocs.io) збирає Sphinx із файлів `.rst` репозиторію, а
документацію плагінів DNS — з опису модуля Python (`.. automodule::` у їхньому index.rst). Розбір
rst фабрики писався для README.rst і посібника SOPS, де Sphinx немає, і без цього шару в корпус
лягло б:

- `:ref:`DNS plugins <dns_plugins>`` — кодом із міткою в кутових дужках замість слів посилання;
- `.. toctree::` і `.. automodule::` — переліком імен сторінок і модулів посеред тексту;
- `:caption: To acquire a certificate for ``example.com``` у прикладі — випадав разом з іншими
  параметрами директиви, і приклад лишався без підпису, до чого він;
- проста таблиця (рядки `=====  =====`) — рисками знаків «=» і злиплими в абзац клітинками: так
  записано таблицю параметрів кожного плагіна DNS (`--dns-cloudflare-credentials` …);
- підстановка `|dns_plugs|` (`.. |dns_plugs| replace:: …`) — словом у вертикальних рисках;
- просте посилання `apache_`, `credentials_` (на ціль `.. _apache:` чи на назву розділу) — словом
  із підкресленням у кінці.

Довідка `certbot --help all` (`cli-help.txt`, яку сторінка man вставляє `literalinclude`) — не rst,
а вивід argparse: тут вона стає розділом на кожну групу параметрів, а текст групи — кодом, щоб
вирівнювання колонок не розсипалося в абзац.
"""

import ast
import re

from engine.readers.sitedocs import _indent, _rst_block, plain, rst

_DIRECTIVE = re.compile(r"^(\s*)\.\.\s+([\w:-]+)::(?:\s+(.*))?$")
_SUBST_DEF = re.compile(r"^\s*\.\.\s+\|([^|]+)\|\s+replace::\s*(.*)$")
# Підстановка-картинка (`.. |build-status| image:: …` — значок збірки в README): саму директиву
# розбір rst викидає, а `|build-status|` у тексті лишався б.
_SUBST_OTHER = re.compile(r"^\s*\.\.\s+\|([^|]+)\|\s+(?!replace::)[\w-]+::")
# Директиви, тексту яких читач не бачить: зміст сайту, вставки коду Python (autodoc),
# вставка файла (довідка CLI лежить окремим документом), позначки сторінки.
_DROP = ("toctree", "automodule", "autoclass", "autofunction", "automethod", "autodata",
         "autoattribute", "autoexception", "autosummary", "literalinclude", "program-output",
         "currentmodule", "module", "py:module", "py:currentmodule", "index", "highlight")
_FIELD_ORPHAN = re.compile(r"^:(orphan|nosearch|tocdepth):.*$", re.M)
# Роль із назвою й ціллю: на сайті видно лише назву.
_ROLE_TITLED = re.compile(r":(?:ref|doc|term|numref|any|py:\w+):`([^`<]*?)\s*<[^`>]+>`")
# Роль посилання без назви: на сайті — назва розділу, якої тут немає; мітка (`dns_plugins`)
# з підкресленнями заміняється пробілами, щоб читалася словами.
_ROLE_REF = re.compile(r":(?:ref|doc|numref|any):`([^`]+)`")
_SIMPLE_BORDER = re.compile(r"^(\s*)=+(?:[ \t]+=+)+[ \t]*$")
_TARGET_NAME = re.compile(r"^\s*\.\.\s+_([^:`]+):")
_HEADING_UNDER = re.compile(r"^([=\-~^\"'`#*+_.:<>])\1{2,}\s*$")
_LINE_BLOCK = re.compile(r"^\|(?:\s+|$)")
_HELP_GROUP = re.compile(r"^([A-Za-z][\w ,&/()'-]*):\s*$")


def _caption(lines: list[str], i: int, indent: int) -> tuple[str, list[str], int]:
    """Підпис `:caption:` директиви коду (з рядками-продовженнями) і решта блоку без нього."""
    block, j = _rst_block(lines, i + 1, indent)
    caption, rest, k = "", [], 0
    while k < len(block):
        ln = block[k]
        if ln.strip().startswith(":caption:"):
            parts = [ln.strip()[len(":caption:"):].strip()]
            base = _indent(ln)
            k += 1
            while k < len(block) and block[k].strip() and _indent(block[k]) > base \
                    and not block[k].strip().startswith(":"):
                parts.append(block[k].strip())
                k += 1
            caption = " ".join(p for p in parts if p)
            continue
        rest.append(ln)
        k += 1
    return caption, rest, j


def _simple_table(lines: list[str], i: int) -> tuple[list[str], int]:
    """Проста таблиця rst → пункти списку «клітинка — клітинка». Межі колонок — за першою
    рамкою; рядок, у якого перша клітинка порожня, — продовження попереднього."""
    border = lines[i]
    spans = [(m.start(), m.end()) for m in re.finditer(r"=+", border)]
    rows: list[list[str]] = []
    j = i + 1
    while j < len(lines):
        ln = lines[j]
        if _SIMPLE_BORDER.match(ln):
            nxt = lines[j + 1] if j + 1 < len(lines) else ""
            j += 1
            if not nxt.strip():
                break  # нижня рамка
            continue  # рамка під шапкою
        if not ln.strip():
            j += 1
            continue
        cells = []
        for n, (a, _) in enumerate(spans):
            b = spans[n + 1][0] if n + 1 < len(spans) else len(ln)
            cell = ln[a:b].strip() if n + 1 < len(spans) else ln[a:].strip()
            # Клітинка з рядками «| …» (line block) — один текст, риски лише ділили рядки.
            cells.append(_LINE_BLOCK.sub("", cell))
        if rows and not cells[0]:
            for n, c in enumerate(cells):
                if c:
                    rows[-1][n] = f"{rows[-1][n]} {c}".strip()
        else:
            rows.append(cells)
        j += 1
    pad = re.match(r"\s*", border).group(0)
    out = [""] + [f"{pad}- " + " — ".join(c for c in row if c) for row in rows if any(row)] + [""]
    return out, j


def _prepare(text: str) -> str:
    """Sphinx → rst, який розуміє спільний розбір."""
    text = text.replace("\r\n", "\n").expandtabs(8)
    lines = text.split("\n")
    substs = {}
    # Імена, на які можна послатися «назва_»: явні цілі й назви розділів (неявні цілі rst).
    names = set()
    for n, ln in enumerate(lines):
        m = _SUBST_DEF.match(ln)
        if m:
            substs[m.group(1)] = m.group(2).strip()
        o = _SUBST_OTHER.match(ln)
        if o:
            substs.setdefault(o.group(1), "")
        t = _TARGET_NAME.match(ln)
        if t:
            names.add(t.group(1).strip().lower())
        if n and _HEADING_UNDER.match(ln) and lines[n - 1].strip() \
                and not _HEADING_UNDER.match(lines[n - 1]):
            names.add(lines[n - 1].strip().lower())
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if _SUBST_DEF.match(ln):
            i += 1
            continue
        d = _DIRECTIVE.match(ln)
        if d:
            name = d.group(2).lower()
            if name in _DROP:
                _, i = _rst_block(lines, i + 1, len(d.group(1)))
                continue
            if name in ("code", "code-block", "sourcecode"):
                caption, body, j = _caption(lines, i, len(d.group(1)))
                if caption:
                    out.extend(["", f"{d.group(1)}{caption.rstrip(':')}:", ""])
                out.append(ln)
                out.extend(body)
                i = j
                continue
        if _SIMPLE_BORDER.match(ln) and (not out or not out[-1].strip()):
            rows, i = _simple_table(lines, i)
            out.extend(rows)
            continue
        out.append(ln)
        i += 1
    text = "\n".join(out)
    # Посилання на розділ `назва`_, перенесене на інший рядок: розбір іде рядками й інакше
    # лишив би `Getting help and та suggestions`_ із рисками.
    text = re.sub(r"(?<![`\\])`(?!`)([^`\n]+)\n[ \t]*([^`\n]*?)`(__?)(?![\w`])",
                  lambda m: f"`{m.group(1).strip()} {m.group(2).strip()}`{m.group(3)}", text)
    for name, value in substs.items():
        text = text.replace(f"|{name}|", value)
    if names:
        alt = "|".join(re.escape(x) for x in sorted(names, key=len, reverse=True))
        text = re.sub(rf"(?<![\w`|])({alt})_(?![\w])", r"\1", text, flags=re.I)
    text = _FIELD_ORPHAN.sub("", text)
    # `~модуль.ім'я` — Sphinx показує лише останню частину; тильда в тексті — лише шум.
    text = text.replace("`~", "`")
    text = _ROLE_TITLED.sub(r"\1", text)
    text = _ROLE_REF.sub(lambda m: m.group(1).lstrip("~").replace("_", " ")
                         if re.fullmatch(r"[\w.~/-]+", m.group(1)) else m.group(1), text)
    return text


def demote(text: str) -> str:
    """Заголовки markdown на рівень нижче; «#» у блоках коду (коментар у прикладі) — не заголовок."""
    out, fence = [], False
    for ln in text.split("\n"):
        if re.match(r"^\s*(```|~~~)", ln):
            fence = not fence
        out.append("#" + ln if not fence and re.match(r"^#{1,5} ", ln) else ln)
    return "\n".join(out)


def to_markdown(text: str) -> str:
    """Сторінка Sphinx (`.rst`) → markdown."""
    return plain(rst(_prepare(text)))


def docstring(text: str) -> str:
    """Опис модуля Python (перший рядок-літерал файла) — сторінка плагіна на Read the Docs
    (`.. automodule::`). Код старих версій буває під Python 2, і `ast` його не розбере, тож
    тоді опис береться виразом — він однаково стоїть першим у файлі."""
    try:
        doc = ast.get_docstring(ast.parse(text), clean=True)
    except (SyntaxError, ValueError):
        m = re.match(r'\s*(?:#.*\n\s*)*[rRuU]?("""|\'\'\')(.*?)\1', text, re.S)
        doc = m.group(2).replace("\\\\", "\\") if m else None
    return doc or ""


def help_text(text: str) -> str:
    """Вивід `certbot --help all` → markdown: група параметрів («automation:», «security:») —
    розділ, її рядки — код."""
    lines = text.replace("\r\n", "\n").expandtabs(8).split("\n")
    out: list[str] = []
    block: list[str] = []

    def flush():
        while block and not block[-1].strip():
            block.pop()
        while block and not block[0].strip():
            block.pop(0)
        if block:
            out.extend(["```", *block, "```", ""])
        block.clear()

    # Назва — з рядка використання («  certbot [SUBCOMMAND] …»): перша група («usage») назвою
    # сторінки бути не може, а саме її взяло б за назву.
    prog = next((ln.split()[0] for ln in lines[1:4] if ln.strip()), "")
    if prog:
        out.extend([f"# {prog} command-line options ({prog} --help all)", ""])
    for ln in lines:
        g = _HELP_GROUP.match(ln)
        if g and not ln.startswith(" "):
            flush()
            out.extend([f"## {g.group(1)}", ""])
            continue
        block.append(ln.rstrip())
    flush()
    return "\n".join(out)
