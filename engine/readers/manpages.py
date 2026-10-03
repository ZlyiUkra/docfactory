"""Читач проєкту Linux man-pages: архів кожного випуску з kernel.org, розмітка groff (man(7)).

`man-pages` — `url`      — тека випусків (…/pub/linux/docs/man-pages/); старіші випуски
                           читач шукає ще й у її підтеці `Archive/`;
              `versions` — перелік випусків, від найновішого («6.19», «6.9.1», «2.00»);
              `sections` — розділи man, які брати («2», «4», «5», «7»);
              `label`    — префікс назви документа.

Навіщо. Теорію ядра, на якій стоять контейнери, — namespaces(7), cgroups(7),
capabilities(7), clone(2), proc(5) — пише сам проєкт man-pages, і лише в розмітці groff:
готового HTML усіх випусків ніде немає. Без розбору в корпус лягли б макроси (`.BR
clone (2)`, `.TP`, `\\fB…\\fR`), а таблиці tbl (`.TS` … `.TE`) — рядками форматів.

Одиниця — неповторний текст сторінки: та сама сторінка в кількох випусках дає один
документ з усіма цими версіями в рядку «версія» (як програми іспитів CNCF). Рядок `.TH`
несе дату правки й назву випуску — його відмінність текстом не вважається. Сторінки-
посилання (`.so man2/x.2`) — не текст, вони пропускаються. Архів кожного випуску
тягнеться один раз за прогін, у пам'яті лишаються тільки неповторні тексти.
"""

import hashlib
import io
import lzma
import re
import tarfile

from engine.readers import Item, _markup, register

_HREF = re.compile(r'href="man-pages-([0-9.]+)\.tar\.xz"')

# Іменовані символи groff, що трапляються в man-pages.
_CHARS = {
    "em": "—", "en": "–", "hy": "-", "aq": "'", "dq": '"', "lq": "“", "rq": "”",
    "oq": "‘", "cq": "’", "bu": "•", "co": "©", "rg": "®", "tm": "™", "de": "°",
    "mu": "×", "di": "÷", "+-": "±", "<=": "≤", ">=": "≥", "!=": "≠", "->": "→",
    "<-": "←", "ua": "↑", "da": "↓", "rs": "\\", "ti": "~", "ha": "^", "ga": "`",
    "lB": "[", "rB": "]", "lC": "{", "rC": "}", "la": "⟨", "ra": "⟩", "sq": "□",
    "Fo": "«", "Fc": "»", "ss": "ß", "pc": "·", "ci": "○", "sc": "§", "ps": "¶",
    "mc": "µ", "*m": "µ", "*p": "π", "if": "∞", "fo": "‹", "fc": "›", "es": "∅",
    "Do": "$", "at": "@", "sh": "#", "eu": "€", "Eu": "€", "or": "|", "ba": "|",
    "br": "│", "ul": "_", "rn": "‾", "tno": "¬", "no": "¬",
}
_STRINGS = {"lq": "“", "rq": "”", "R": "®", "Tm": "™", "S": "", "dq": '"'}

_ESC = re.compile(
    r"\\(?:"
    r"f(?:\[[^\]]*\]|\(..|.)"          # шрифт: \fB, \f[B], \f(CW
    r"|s[-+]?\d+"                       # кегль: \s-1
    r"|\((..)"                          # символ: \(em
    r"|\[([^\]]*)\]"                    # символ: \[em], \[u2014]
    r"|\*(?:\((..)|\[([^\]]*)\]|(.))"   # рядок: \*(lq, \*[lq], \*R
    r"|(.))")                           # одна літера після \


def _esc(m) -> str:
    two, bracket, s2, sb, s1, one = m.groups()
    full = m.group(0)
    if full[1] == "f" or full[1] == "s":
        return ""
    if two is not None:
        return _CHARS.get(two, "")
    if bracket is not None:
        if bracket.startswith("u") and re.fullmatch(r"u[0-9A-Fa-f]{4,6}", bracket):
            return chr(int(bracket[1:], 16))
        return _CHARS.get(bracket, "")
    if full[1] == "*":
        return _STRINGS.get(s2 or sb or s1 or "", "")
    return {"-": "-", "e": "\\", "\\": "\\", "~": " ", " ": " ", "0": " ", "&": "",
            "%": "", ":": "", "|": "", "^": "", "c": "", "/": "", ",": "", "'": "'",
            "`": "`", ".": ".", "t": "\t", "!": "", "z": "", "a": ""}.get(one, "")


def inline(text: str) -> str:
    """Рядок groff без керівних послідовностей."""
    return _ESC.sub(_esc, text)


def _args(line: str) -> list[str]:
    """Аргументи макроса: слова, а в лапках — разом із пробілами."""
    out, cur, quoted, i = [], "", False, 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            if quoted and i + 1 < len(line) and line[i + 1] == '"':
                cur += '"'
                i += 2
                continue
            quoted = not quoted
        elif ch in " \t" and not quoted:
            if cur:
                out.append(cur)
                cur = ""
        else:
            cur += ch
        i += 1
    if cur:
        out.append(cur)
    return out


def _table(lines: list[str]) -> list[str]:
    """Таблиця tbl — рядки з комірками через « | ». Блоки T{ … T} складаються в одну
    комірку, рядки-лінії («_», «=») пропускаються."""
    i = 0
    # Перший рядок може бути опціями («tab(:);»), далі формати до рядка з крапкою.
    tab = "\t"
    if i < len(lines) and lines[i].rstrip().endswith(";"):
        m = re.search(r"tab\s*\((.)\)", lines[i])
        if m:
            tab = m.group(1)
        i += 1
    while i < len(lines) and not lines[i].rstrip().endswith("."):
        i += 1
    i += 1
    rows, row, block = [], [], None
    for raw in lines[i:]:
        if block is not None:
            if raw.startswith("T}"):
                row.append(" ".join(block).strip())
                block = None
                rest = raw[2:]
                if rest.startswith(tab):
                    cells = rest[1:].split(tab)
                    row.extend(inline(c).strip() for c in cells[:-1])
                    last = cells[-1]
                    if last.strip() == "T{":
                        block = []
                    else:
                        row.append(inline(last).strip())
                        rows.append(row)
                        row = []
                else:
                    rows.append(row)
                    row = []
            elif not raw.startswith("."):
                block.append(inline(raw))
            continue
        if raw.startswith(".") or raw.strip() in ("_", "=", ""):
            continue
        if raw.startswith(".T&"):
            continue
        cells = raw.split(tab)
        for c in cells[:-1]:
            row.append(inline(c).strip())
        if cells[-1].strip() == "T{":
            block = []
        else:
            row.append(inline(cells[-1]).strip())
            rows.append(row)
            row = []
    return [" | ".join(c for c in r) for r in rows if any(c for c in r)]


_FONT_MACROS = {"B", "I", "SM", "SB"}
_ALT_MACROS = {"BR", "BI", "IB", "IR", "RB", "RI"}


def to_markdown(src: str) -> tuple[str, str]:
    """Сторінка groff → (назва з розділу NAME, markdown). Таблиці й незаповнені блоки —
    огорожею коду, абзаци склеюються в рядки."""
    out: list[str] = []
    para: list[str] = []
    fill = True
    code: list[str] = []
    name_line = ""
    section = ""
    lines = src.split("\n")

    def flush() -> None:
        nonlocal para
        if para:
            out.append(" ".join(" ".join(para).split()))
            out.append("")
            para = []

    def flush_code() -> None:
        nonlocal code
        if code:
            while code and not code[-1].strip():
                code.pop()
            if code:
                out.extend(["```", *code, "```", ""])
            code = []

    def emit(text: str) -> None:
        if fill:
            if text.strip():
                para.append(text)
        else:
            code.append(text)

    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if line.startswith(("'\\\"", ".\\\"", "\\\"")) or line in (".", "'"):
            continue
        if not line.startswith((".", "'")):
            if not line.strip() and fill:
                flush()
                continue
            text = inline(line)
            if section == "NAME" and fill:
                name_line += " " + text
            emit(text)
            continue
        m = re.match(r"[.']\s*(\S+)\s?(.*)$", line)
        if not m:
            continue
        mac, rest = m.group(1), m.group(2)
        args = _args(rest)
        if mac == "TH":
            continue
        if mac in ("SH", "SS"):
            flush()
            flush_code()
            fill = True
            title = inline(" ".join(args)) if args else ""
            if not title and i < len(lines):
                title = inline(lines[i])
                i += 1
            section = title.strip().upper() if mac == "SH" else section
            out.extend([("## " if mac == "SH" else "### ") + title.strip(), ""])
            continue
        if mac in ("PP", "P", "LP", "sp", "HP"):
            if fill:
                flush()
            else:
                code.append("")
            continue
        if mac == "br":
            if fill:
                flush()
            continue
        if mac in ("TP", "TQ"):
            flush()
            # Наступний рядок — мітка пункту, далі — його тіло.
            while i < len(lines) and lines[i].startswith(".\\\""):
                i += 1
            if i < len(lines):
                tag_line = lines[i]
                i += 1
                tag = _render_line(tag_line)
                if tag.strip():
                    out.extend([tag.strip(), ""])
            continue
        if mac == "IP":
            flush()
            if args:
                tag = inline(args[0]).strip()
                if tag:
                    para.append(tag if tag in ("•", "*", "-") else tag)
            continue
        if mac in ("RS", "RE", "in", "ad", "na", "nh", "hy", "ne", "PD", "ft", "ps",
                   "ta", "UC", "ns", "rs", "fl", "ll", "ss", "cs", "bp", "ti", "ce",
                   "so", "mso", "ds", "nr", "de", "if", "ie", "el", "ig", "rr", "tr",
                   "ev", "hw", "lf", "pl", "po", "vs", "ls", "cu", "ul", "UE", "ME",
                   "YS", "\\}", "\\{"):
            if mac == "so":
                return "", ""
            if mac in ("de", "ig"):
                # Тіло визначення макроса чи коментар-блок — до «..».
                while i < len(lines) and lines[i].strip() != "..":
                    i += 1
                i += 1
            continue
        if mac in ("nf", "EX"):
            flush()
            fill = False
            continue
        if mac in ("fi", "EE"):
            flush_code()
            fill = True
            continue
        if mac == "TS":
            flush()
            block = []
            while i < len(lines) and not lines[i].startswith(".TE"):
                block.append(lines[i])
                i += 1
            i += 1
            rows = _table(block)
            if rows:
                out.extend(["```", *rows, "```", ""])
            continue
        if mac in _FONT_MACROS:
            text = inline(" ".join(args)) if args else ""
            if not text and i < len(lines):
                text = inline(lines[i])
                i += 1
            if section == "NAME" and fill:
                name_line += " " + text
            emit(text)
            continue
        if mac in _ALT_MACROS:
            text = "".join(inline(a) for a in args)
            if section == "NAME" and fill:
                name_line += " " + text
            emit(text)
            continue
        if mac == "MR":
            # .MR сторінка розділ [розділовий знак] — посилання на іншу сторінку (6.x).
            if args:
                text = f"{inline(args[0])}({inline(args[1]) if len(args) > 1 else ''})"
                text += inline(args[2]) if len(args) > 2 else ""
                emit(text)
            continue
        if mac in ("UR", "MT"):
            if args:
                emit(inline(args[0]))
            continue
        if mac in ("SY", "OP"):
            emit(" ".join(inline(a) for a in args))
            continue
        # Невідомий макрос: аргументи як текст — краще зайве слово, ніж загублене.
        if args:
            emit(" ".join(inline(a) for a in args))
    flush()
    flush_code()
    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return " ".join(name_line.split()), body


def _render_line(line: str) -> str:
    """Один рядок — текст: звичайний чи макрос шрифту (мітка пункту .TP)."""
    if not line.startswith((".", "'")):
        return inline(line)
    m = re.match(r"[.']\s*(\S+)\s?(.*)$", line)
    if not m:
        return ""
    mac, args = m.group(1), _args(m.group(2))
    if mac in _ALT_MACROS:
        return "".join(inline(a) for a in args)
    if mac == "MR" and args:
        return f"{inline(args[0])}({inline(args[1]) if len(args) > 1 else ''})"
    return " ".join(inline(a) for a in args)


def _vkey(v: str) -> tuple:
    return tuple(int(n) for n in re.findall(r"\d+", v))


@register("man-pages")
def man_pages(source: dict, ctx) -> list[Item]:
    versions = source.get("versions")
    sections = set(source.get("sections") or ())
    if not versions or not sections:
        raise SystemExit(f"{source['id']}: читач man-pages потребує полів versions і sections.")
    base = source["url"].rstrip("/") + "/"
    where = {v: base for v in _HREF.findall(ctx.text(base))}
    archive = base + "Archive/"
    if ctx.allowed(archive):
        for v in _HREF.findall(ctx.text(archive)):
            where.setdefault(v, archive)
    label = source.get("label", "")

    # Неповторні тексти: (сторінка, хеш тексту) → [версії], сам текст — окремо.
    texts: dict = {}
    seen: dict = {}
    for v in versions:
        if v not in where:
            raise SystemExit(f"{source['id']}: випуску {v} немає ні в {base}, ні в {archive}.")
        url = f"{where[v]}man-pages-{v}.tar.xz"
        if not ctx.allowed(url):
            continue
        data = ctx.bytes(url)
        with tarfile.open(fileobj=io.BytesIO(lzma.decompress(data))) as tar:
            for member in tar.getmembers():
                m = re.search(r"/man(\d)[a-z]*/([^/]+)\.(\d\w*)$", member.name)
                if not member.isfile() or not m or m.group(1) not in sections:
                    continue
                raw = tar.extractfile(member).read().decode("utf-8", errors="replace")
                body = re.sub(r"^\.TH .*$", "", raw, count=1, flags=re.M)
                if re.match(r"\s*\.so\s", re.sub(r"^\.\\\".*\n", "", body, flags=re.M)):
                    continue
                page = f"{m.group(2)}.{m.group(3)}"
                key = (page, hashlib.sha256(body.encode()).hexdigest())
                if key not in seen:
                    seen[key] = []
                    texts[key] = raw
                seen[key].append(v)
        del data

    items = []
    for (page, digest), found in sorted(seen.items()):
        found = sorted(found, key=_vkey, reverse=True)
        name, _, sec = page.rpartition(".")
        doc = f"{_markup.slug(f'{name}-{sec}')}-{digest[:8]}"
        newest = found[0]
        url = f"{where[newest]}man-pages-{newest}.tar.xz#man{sec[0]}/{page}"

        def make(page=page, raw=texts[(page, digest)], found=found, url=url,
                 name=name, sec=sec):
            lead, body = to_markdown(raw)
            what = lead.split(" - ", 1)[1].strip() if " - " in lead else ""
            title = f"{name}({sec})" + (f" — {what}" if what else "")
            if label:
                title = f"{label}: {title}"
            _markup.require(title, body, url)
            return _markup.document(title, url, ctx.stamp, body, ", ".join(found))

        items.append(Item(id=f"{source['id']}/{doc}", file=f"{source['id']}--{doc}.txt",
                          make=make))
    return items
