"""Читач історії сторінок man у форматі AsciiDoc з багатьох тегів одного репозиторію (Tesseract).

`ghdocs-history-asciidoc` — файли `.asc` (`doc/tesseract.1.asc`, `doc/unicharset.5.asc` …) з багатьох тегів
                            разом. Поля ті самі, що в `ghdocs-history` (`url`, `tags`, `folders`,
                            `extensions`, `exclude`, `name_prefix` …). Текст кожного файла `.asc` перед
                            звичайним розбором стає markdown.

Навіщо. Сторінки man Tesseract написано в AsciiDoc, з якого a2x робить man і HTML: заголовки підкресленням
(`----`, `~~~~`), списки означень `'FILE'::`, буквальні блоки між рядками `....`, стилі `[verse]`, якорі
`[[LANGUAGES]]`, перехресні посилання `<<LANGUAGES,*LANGUAGES AND SCRIPTS*>>`, `'курсив'`, `*жирний*` і ` +` у
кінці рядка. Читач markdown узяв би відкреслення `....` за текст, а опис опції `--psm` — за продовження абзацу
попередньої.

Що виходить. Заголовок документа — ім'я й короткий опис із розділу NAME; розділи стають «##», підрозділи —
«###»; терміни списків означень (опції й параметри) — заголовками на рівень нижче розділу, без розмітки
AsciiDoc усередині, опис — текстом під ним: так `--oem`, `--psm` чи `tessedit_create_tsv` знаходяться окремим
розділом, а не шматком довгого «OPTIONS», поділеного за довжиною; кілька термінів поспіль («-l LANG», «-l
SCRIPT») — одним заголовком через кому; буквальні блоки, `[verse]` і абзаци з відступом поза списками — блоками коду.

Чому окремий модуль, а не поле в `ghdocs-history`: спільний читач звірено в багатьох готових примірниках, а тут
досить підмінити текст файла, перш ніж читач його розбере (як `ghdocs-history-pod`).
"""

import re

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_UNDER = {"=": 1, "-": 2, "~": 3, "^": 4, "+": 5}
_DELIM = re.compile(r"^(\.{4,}|-{4,}|\*{4,}|_{4,}|\+{4,}|/{4,}|={4,})[ \t]*$")
_TERM = re.compile(r"^(\S.*?)(?::{2,4}|;;)(?:[ \t]+(.*))?$")
_BULLET = re.compile(r"^[ \t]*(\*{1,5}|-|\.{1,5}|\d+\.)[ \t]+(.*)$")
_ONELINE = re.compile(r"^(={1,5})[ \t]+(.+?)(?:[ \t]+=+)?[ \t]*$")
_ATTR_ENTRY = re.compile(r"^:!?[\w-]+!?:.*$")
_ANCHOR = re.compile(r"^\[\[[^\]]+\]\]$")
_BLOCK_ATTR = re.compile(r"^\[[\w ,.=\"'#%-]*\]$")
_ATTR_REF = {"blank": "", "nbsp": " ", "plus": "+", "amp": "&", "lt": "<", "gt": ">", "startsb": "[",
             "endsb": "]", "vbar": "|", "caret": "^", "asterisk": "*", "tilde": "~", "apostrophe": "'",
             "backslash": "\\", "backtick": "`", "two-colons": "::", "two-semicolons": ";;",
             "empty": "", "sp": " ", "zwsp": ""}


def _inline_plain(text: str) -> str:
    """Розмітка AsciiDoc поза кодом: посилання, жирний, курсив, атрибути, розриви рядків."""
    text = re.sub(r"<<([^,>]+),\s*([^>]+)>>", r"\2", text)
    text = re.sub(r"<<([^>]+)>>", r"\1", text)
    text = re.sub(r"link:(\S+?)\[([^\]]*)\]", lambda m: f"{m.group(2)} ({m.group(1)})" if m.group(2)
                  else m.group(1), text)
    text = re.sub(r"(https?://[^\s\[]+)\[([^\]]*)\]", lambda m: f"{m.group(2)} ({m.group(1)})"
                  if m.group(2) else m.group(1), text)
    text = re.sub(r"\{([\w-]+)\}", lambda m: _ATTR_REF.get(m.group(1), m.group(0)), text)
    text = re.sub(r"\+\+\+(.+?)\+\+\+|pass:\[(.*?)\]", lambda m: m.group(1) or m.group(2) or "", text)
    text = re.sub(r"(?<![\w*\\])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![\w*])", r"**\1**", text)
    text = re.sub(r"(?<![\w'\\])'(?!\s)([^'\n]+?)(?<!\s)'(?![\w'])", r"*\1*", text)
    text = re.sub(r"(?<![\w\\])_(?!\s)([^_\n]+?)(?<!\s)_(?!\w)", r"*\1*", text)
    text = re.sub(r"(?<![\w+\\])\+(?!\s)([^+\n]+?)(?<!\s)\+(?![\w+])", r"`\1`", text)
    text = re.sub(r"[ \t]+\+$", "", text, flags=re.M)
    text = text.replace(" -- ", " — ")
    return re.sub(r"\\([*'_+`{<])", r"\1", text)


def _inline(text: str) -> str:
    """Те саме, але текст у зворотних лапках лишається як є: там `*` і `'` — частина коду."""
    parts = re.split(r"(`[^`\n]+`)", text)
    return "".join(p if p.startswith("`") and p.endswith("`") and len(p) > 1 else _inline_plain(p)
                   for p in parts)


def _plain(text: str) -> str:
    """Термін списку означень без розмітки: він стає жирним рядком, і вкладений жирний його рвав би."""
    text = _inline(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)([^*\n]+?)\*(?![\w*])", r"\1", text)
    return " ".join(text.split())


def _underline(line: str, nxt: str) -> int:
    """Рівень заголовка, підкресленого рядком `nxt`, або 0. Довжини мусять майже збігатися — інакше це
    відкреслення блоку після абзацу."""
    if not line.strip() or line[:1] in (" ", "\t") or _DELIM.match(line) or _BLOCK_ATTR.match(line.strip()):
        return 0
    if not re.fullmatch(r"([=\-~^+])\1+", nxt.rstrip()):
        return 0
    if abs(len(nxt.rstrip()) - len(line.rstrip())) > 2:
        return 0
    return _UNDER[nxt[0]]


def _title(paragraph: str, fallback: str) -> str:
    text = " ".join(_plain(paragraph).split())
    names, sep, desc = text.partition(" - ")
    if not sep:
        return text or fallback
    return f"{names.strip()} — {desc.strip()}"


def asciidoc_to_markdown(src: str, stem: str = "") -> str:
    """AsciiDoc → markdown з одним заголовком першого рівня (назва сторінки) і розділами «##»."""
    lines = src.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    header = stem
    title = None
    in_name = False
    verse = False
    depth = 2
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()
        nxt = lines[i + 1] if i + 1 < n else ""
        level = _underline(line, nxt)
        one = _ONELINE.match(line) if not level and not _DELIM.match(line) else None
        if level or one:
            if one:
                level, head = len(one.group(1)), one.group(2)
            else:
                head = line
            head = _plain(head)
            i += 2 if not one else 1
            if level == 1:
                header = head
                continue
            in_name = level == 2 and head.upper() == "NAME"
            depth = min(level, 6)
            out.extend(["", "#" * min(level, 6) + " " + head, ""])
            continue
        if line.startswith("//") and not _DELIM.match(line):
            i += 1
            continue
        if _ATTR_ENTRY.match(line) or _ANCHOR.match(line.strip()):
            i += 1
            continue
        if _BLOCK_ATTR.match(line.strip()) and line.strip() != "[]":
            verse = line.strip().startswith("[verse") or line.strip().startswith("[literal") \
                or line.strip().startswith("[source") or line.strip().startswith("[listing")
            i += 1
            continue
        if _DELIM.match(line):
            close = line.strip()
            body = []
            i += 1
            while i < n and lines[i].rstrip() != close:
                body.append(lines[i].rstrip())
                i += 1
            i += 1
            literal, verse = verse, False
            if close[0] == "/":
                continue
            if close[0] in ".-+" or literal:
                out.extend(["", "```", *body, "```", ""])
            else:
                out.extend(["", *[_inline(b) for b in body], ""])
            continue
        if not line.strip():
            out.append("")
            i += 1
            continue
        # абзац: до порожнього рядка, відкреслення блоку чи заголовка
        para = []
        while i < n and lines[i].strip() and not _DELIM.match(lines[i].rstrip()) \
                and not _underline(lines[i].rstrip(), lines[i + 1] if i + 1 < n else ""):
            para.append(lines[i].rstrip())
            i += 1
        if verse:
            out.extend(["", "```", *para, "```", ""])
            verse = False
            continue
        if in_name and title is None:
            title = _title(" ".join(para), header)
            out.extend(["", " ".join(_inline(" ".join(para)).split()), ""])
            continue
        first = para[0]
        if first[:1] in (" ", "\t") and not _BULLET.match(first):
            out.extend(["", "```", *[p[_indent(para):] for p in para], "```", ""])
            continue
        _emit(para, out, min(depth + 1, 6))
    md = "\n".join(out)
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return f"# {title or header or 'manual page'}\n\n{md}\n"


def _indent(para: list[str]) -> int:
    return min(len(p) - len(p.lstrip()) for p in para if p.strip())


def _emit(para: list[str], out: list[str], level: int) -> None:
    """Абзац, що може складатися з термінів списку означень, пунктів переліку й звичайного тексту."""
    text: list[str] = []
    mark = "#" * level + " "

    def flush():
        if text:
            out.extend(["", _inline(" ".join(re.sub(r"[ \t]+\+$", "", t.strip()) for t in text)), ""])
            text.clear()

    for line in para:
        if line.strip() == "+":
            flush()
            continue
        term = _TERM.match(line) if not line[:1] in (" ", "\t") else None
        if term and not re.search(r"https?:$|\w::\w", line):
            flush()
            head = _plain(term.group(1))
            # «tessedit_create_tsv (bool, default: 0) [Both]»: заголовком — ім'я параметра, тип і змовчання —
            # першим рядком опису; інакше зміна змовчання між версіями давала б розділу новий ключ.
            spec = re.match(r"^(\S+)\s+(\(.*)$", head)
            if spec:
                head = spec.group(1)
            if len(out) > 1 and out[-1] == "" and out[-2].startswith(mark) and getattr(_emit, "_last", None) == \
                    (id(out), len(out)):
                out[-2] += ", " + head
            else:
                out.extend(["", mark + head, ""])
            _emit._last = (id(out), len(out))
            if spec:
                text.append(spec.group(2) + ".")
                flush()
            if term.group(2):
                text.append(term.group(2))
            continue
        bullet = _BULLET.match(line)
        if bullet and not re.match(r"^\*\S", line.strip()):
            flush()
            mark = bullet.group(1)
            depth = len(mark) - 1 if mark[0] in "*." else 0
            sign = "1." if mark[0] == "." or mark[0].isdigit() else "-"
            out.append("  " * depth + f"{sign} " + _inline(bullet.group(2).strip()))
            continue
        if out and re.match(r"^\s*(?:-|1\.) ", out[-1]) and not text and line[:1] in (" ", "\t"):
            out[-1] += " " + _inline(line.strip())
            continue
        text.append(line)
    flush()


class _Ctx:
    """Той самий контекст завантаження, лише текст файлів `.asc` проходить `asciidoc_to_markdown`."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        path = url.split("?", 1)[0]
        if not re.search(r"\.(asc|adoc|asciidoc)$", path):
            return text
        stem = re.sub(r"\.(asc|adoc|asciidoc)$", "", path.rsplit("/", 1)[-1])
        return asciidoc_to_markdown(text, stem)


@register("ghdocs-history-asciidoc")
def ghdocs_history_asciidoc(source: dict, ctx):
    return ghdocs_history(source, _Ctx(ctx))
