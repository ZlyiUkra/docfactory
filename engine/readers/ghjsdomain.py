"""Читач документації Sphinx, де довідник API записано директивами домену JavaScript (MuPDF.js).

`ghdocs-history-jsdomain` — те саме, що `ghdocs-history` (поля `url`, `tags`, `folders`, `files`, `recursive`,
                            `extensions`, `exclude`, `name_prefix` …), і одна різниця: файл `.rst` з
                            raw.githubusercontent.com перед розбором стає markdown, а кожна директива
                            `.. method::`, `.. function::`, `.. attribute::` чи `.. data::` — заголовком
                            четвертого рівня зі своїм підписом. Поле `sphinx` джерелу не потрібне.

Навіщо. Довідник JavaScript API MuPDF — сторінка на тип (`PDFAnnotation.rst`, 134 методи), і кожен метод там
не розділ, а директива: `.. method:: PDFAnnotation.prototype.setRect(rect)` з описом на відступі. Спільний
розбір Sphinx (`sphinx: true`) такої директиви не знає і лишає підпис звичайним рядком тексту. Розділів на
сторінці виходило п'ять-шість, фрагменти різалися за довжиною посеред методів, і жоден не називав методу,
який описує; назвою документа ставало ім'я файла («PDFAnnotation.rst»).

Тут підпис стає заголовком («#### PDFAnnotation.prototype.setRect(rect)»), опис знімається з відступу, а поля
`:param Rect rect: …`, `:returns: …`, `:throws: …` — рядками «- `rect` (Rect): …», «Returns: …», «Throws: …».
Службові рядки `.. default-domain:: js` і `.. highlight:: javascript` знімаються. Решту розмітки (заголовки,
блоки коду, таблиці, примітки) перетворює `_sphinx.to_markdown`, як і для інших сайтів Sphinx.

Чому обгортка, а не поле в `ghdocs-history`: перелік тегів, імена документів і версії той читач складає сам і
звірений у десятках примірників. Тут лише текст файла міняється дорогою.
"""

import re
from urllib.parse import urlsplit

from engine.readers import _sphinx, register
from engine.readers.ghhistory import ghdocs_history

_API = re.compile(r"^\.\.\s+(?:js:)?(method|function|attribute|data|class)::\s*(.*)$")
_SERVICE = re.compile(r"^\.\.\s+(?:default-domain|highlight)::.*$")
_PARAM = re.compile(r"^:param\s+(?:(.+)\s+)?([\w.$\[\]]+):\s*(.*)$")
_FIELD = re.compile(r"^:(returns?|throws?|raises?|rtype|type)(?:\s+[^:]*)?:\s*(.*)$")
_LABELS = {"return": "Returns", "returns": "Returns", "throw": "Throws", "throws": "Throws",
           "raise": "Throws", "raises": "Throws", "rtype": "Return type", "type": "Type"}


def _field(line: str) -> str:
    """Рядок поля Sphinx у тілі директиви → рядок тексту; інший рядок повертається як був."""
    stripped = line.strip()
    m = _PARAM.match(stripped)
    if m:
        kind = f" ({m.group(1).strip()})" if m.group(1) else ""
        return f"- `{m.group(2)}`{kind}: {m.group(3)}".rstrip(": ").rstrip()
    m = _FIELD.match(stripped)
    if m:
        return f"{_LABELS[m.group(1)]}: {m.group(2)}".rstrip(": ").rstrip()
    return line


def _dedent(block: list[str]) -> list[str]:
    """Тіло директиви без свого відступу: один таб або стільки пробілів, скільки має перший рядок."""
    first = next((ln for ln in block if ln.strip()), "")
    indent = first[:len(first) - len(first.lstrip())]
    cut = 1 if indent.startswith("\t") else len(indent)
    out, fields = [], False
    for ln in block:
        ln = ln[cut:] if ln[:cut].strip() == "" else ln.lstrip()
        new = _field(ln) if not ln[:1].isspace() else ln
        # Поля йдуть підряд без порожніх рядків між ними — у markdown це був би один абзац.
        if new is not ln:
            if fields and out and out[-1].strip() and not new.startswith("- "):
                out.append("")
            fields = True
        elif ln.strip():
            fields = False
        out.append(new)
    return out


def jsdomain_to_markdown(text: str) -> str:
    """Сторінка Sphinx з директивами домену JavaScript → markdown."""
    lines = text.replace("\r\n", "\n").split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if _SERVICE.match(line):
            i += 1
            continue
        m = _API.match(line)
        if not m:
            out.append(line)
            i += 1
            continue
        j = i + 1
        while j < len(lines) and (not lines[j].strip() or lines[j][:1].isspace()):
            j += 1
        body = _dedent(lines[i + 1:j])
        if m.group(1) != "class" and m.group(2).strip():
            out += ["", f"#### {m.group(2).strip()}", ""]
        out += body + [""]
        i = j
    return _sphinx.to_markdown("\n".join(out)).strip() + "\n"


class _JsDomainCtx:
    """`ctx`, що віддає сторінки `.rst` з GitHub уже як markdown; решта звернень — до справжнього."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        parts = urlsplit(url)
        if parts.netloc == "raw.githubusercontent.com" and parts.path.endswith(".rst"):
            return jsdomain_to_markdown(text)
        return text


@register("ghdocs-history-jsdomain")
def ghdocs_history_jsdomain(source: dict, ctx) -> list:
    return ghdocs_history(source, _JsDomainCtx(ctx))
