"""Читач документації Sphinx, де довідник API записано директивами домену Python, вкладеними в клас (PyMuPDF).

`ghdocs-history-pydomain` — те саме, що `ghdocs-history` (поля `url`, `tags`, `folders`, `files`, `recursive`,
                            `extensions`, `exclude`, `name_prefix`, `site` …), і одна різниця: файл `.rst` (чи
                            `.txt`, яким PyMuPDF 1.19 називав ті самі сторінки) з raw.githubusercontent.com перед
                            розбором стає markdown, а кожна директива `.. method::`, `.. attribute::`,
                            `.. function::`, `.. property::` чи `.. data::` — заголовком другого рівня з іменем
                            класу попереду: «## Page.get_text()», а повний підпис стоїть першим рядком розділу.
                            Поле `sphinx` джерелу не потрібне.

Навіщо. Довідник PyMuPDF — сторінка на клас (`page.rst` — 85 методів і 31 властивість на 143 тисячі символів),
і кожен метод там не розділ, а директива на відступі всередині `.. class:: Page`. Спільний розбір Sphinx
(`sphinx: true`) директиви `method` не знає: підпис лишався б звичайним рядком, сторінка ділилася б на кілька
розділів за нечисленними заголовками, а фрагменти різалися б за довжиною посеред методів і не називали б ні
методу, ні класу. Читач `ghdocs-history-jsdomain` розбирає такі директиви лише на верхньому рівні сторінки й
тіла класу не розгортає: у довіднику MuPDF.js, для якого його написано, методи в клас не вкладено.

Що робить читач:

- тіло директиви `.. class:: Page` знімається з відступу й розбирається далі; сам підпис класу стає рядком
  «Class: ``Page``», а ім'я класу лягає перед іменем кожного його методу й властивості;
- ім'я методу стає заголовком, а підпис із параметрами — рядком коду під ним: підпис між версіями міняється,
  і в заголовку він дав би тому самому методові різних версій різні ключі розділу; другий і дальші підписи
  тієї самої директиви (перевантаження, записані рядками під першим) — рядками «Also: ``…``»;
- поля `:arg rect-like rect: …`, `:param …`, `:returns: …`, `:rtype: …`, `:raises …:` стають рядками
  «- `rect` (rect-like): …», «Returns: …», «Return type: …», «Raises: …»;
- підстановки зі спільного файла `header.rst`, якого сторінка сама не містить, заміняються текстом, що його
  бачить читач сайту: `|PDF|` → «PDF», `|PyMuPDF|` → «PyMuPDF»; `|history_begin|` і `|history_end|` — обгортка
  згорнутого блоку історії — знімаються, а сама історія («New in v1.17.7») лишається;
- підстановка, означена на самій сторінці сирим HTML (`.. |PyMuPDFLayoutMode_Valid| raw:: html`), заміняється
  текстом цього HTML без тегів;
- рядки `.. include:: header.rst`, `.. include:: footer.rst` і блоки `.. meta::`, `.. raw:: html` знімаються:
  це шапка, підвал і службовий HTML сайту.

Решту розмітки (заголовки, блоки коду, таблиці, примітки, позначки версій) перетворює `_sphinx.to_markdown`.

Чому обгортка, а не поле в `ghdocs-history`: перелік тегів, імена документів і версії той читач складає сам і
звірений у десятках примірників. Тут лише текст файла міняється дорогою.
"""

import html
import re
from urllib.parse import urlsplit

from engine.readers import _sphinx, register
from engine.readers.ghhistory import ghdocs_history

_API = re.compile(r"^( *)\.\.\s+(?:py:)?(class|exception|method|classmethod|staticmethod|function|attribute|"
                  r"property|data)::\s*(.*)$")
_DROP_LINE = re.compile(r"^\s*\.\.\s+include::\s*\S*(?:header|footer)\S*\s*$")
_DROP_BLOCK = re.compile(r"^( *)\.\.\s+(?:meta|raw)::.*$")
_SUBST_RAW = re.compile(r"^( *)\.\.\s+\|([^|]+)\|\s+raw::\s*html\s*$")
_SUBST_USE = re.compile(r"\|([A-Za-z][\w ]*\w)\|")
_OPTION = re.compile(r"^:(?:no-?index|no-index-entry|no-contents-entry|no-typesetting|module|canonical|async|"
                     r"abstractmethod|classmethod|staticmethod|final|type|value)(?:\s*:|:)")
_PARAM = re.compile(r"^:(?:arg|param|parameter|argument|keyword|kwarg)\s+(?:([^:`]+?)\s+)?([\w.*]+):\s*(.*)$")
_FIELD = re.compile(r"^:(returns?|rtype|raises?|type|var|ivar)(?:\s+([^:]*))?:\s*(.*)$")
_LABELS = {"return": "Returns", "returns": "Returns", "rtype": "Return type", "raise": "Raises",
           "raises": "Raises", "type": "Type", "var": "Variable", "ivar": "Variable"}
# Обгортки згорнутого блоку історії й напис праворуч угорі сторінки класу — зі спільного `header.rst`.
_KNOWN = {"history_begin": "", "history_end": "", "pdf_only_class": "This class is for PDF only."}
_CONTAINERS = ("class", "exception")


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _block(lines: list[str], i: int, indent: int) -> int:
    """Індекс рядка, на якому закінчується тіло директиви з відступом `indent`, що почалося з рядка `i`."""
    j = i
    while j < len(lines) and (not lines[j].strip() or _indent(lines[j]) > indent):
        j += 1
    while j > i and not lines[j - 1].strip():
        j -= 1
    return j


def _dedent(block: list[str]) -> list[str]:
    cut = min((_indent(ln) for ln in block if ln.strip()), default=0)
    return [ln[cut:] if ln.strip() else "" for ln in block]


def _field(line: str) -> str | None:
    """Рядок поля Sphinx у тілі директиви → рядок тексту; `None`, коли рядок — не поле."""
    m = _PARAM.match(line)
    if m:
        kind = f" ({m.group(1).strip()})" if m.group(1) else ""
        return f"- `{m.group(2)}`{kind}: {m.group(3)}".rstrip(": ").rstrip()
    m = _FIELD.match(line)
    if m:
        name = f" `{m.group(2).strip()}`" if m.group(2) and m.group(1) not in ("returns", "return") else ""
        return f"{_LABELS[m.group(1)]}{name}: {m.group(3)}".rstrip(": ").rstrip()
    return None


def _fields(body: list[str]) -> list[str]:
    """Поля на нульовому відступі тіла — рядками тексту, кожне окремим абзацом чи пунктом списку."""
    out, was_field = [], False
    for ln in body:
        new = _field(ln) if ln[:1] == ":" else None
        if new is None:
            if ln.strip():
                # Продовження опису параметра стоїть на відступі під ним — лишається частиною пункту.
                was_field = was_field and ln[:1] == " "
            out.append(ln)
            continue
        if out and out[-1].strip() and not (was_field and new.startswith("- ") and out[-1].startswith(("- ", " "))):
            out.append("")
        out.append(new)
        was_field = True
    return out


def _convert(lines: list[str], owner: str) -> list[str]:
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        m = _API.match(line)
        if not m:
            out.append(line)
            i += 1
            continue
        indent, kind, sig = len(m.group(1)), m.group(2), " ".join(m.group(3).split())
        j = _block(lines, i + 1, indent)
        body = _dedent(lines[i + 1:j])
        # Рядки одразу під директивою, до першого порожнього: ще підписи (перевантаження) і параметри директиви.
        more, k = [], 0
        while k < len(body) and body[k].strip() and _signature_line(body[k]):
            if not _OPTION.match(body[k].strip()):
                more.append(" ".join(body[k].split()))
            k += 1
        body = body[k:]
        pad = " " * indent
        if kind in _CONTAINERS:
            name = re.match(r"[\w.]+", sig)
            out += ["", f"{pad}Class: ``{sig}``", ""]
            out += [pad + x if x else "" for x in _convert(body, name.group(0) if name else owner)] + [""]
        else:
            full = sig if not owner or sig.startswith(owner + ".") else f"{owner}.{sig}"
            # У заголовку — лише ім'я: підпис між версіями міняється (додали параметр), і з ним у заголовку
            # той самий метод різних версій мав би різні ключі розділу й займав би у видачі кілька місць.
            name = re.match(r"[\w.]+", full)
            short = (name.group(0) if name else full) + ("()" if "(" in full else "")
            out += ["", f"## {short}", ""]
            if short != full:
                out += [f"``{full}``", ""]
            out += [f"Also: ``{x}``" for x in more] + ([""] if more else [])
            out += _convert(_fields(body), owner) + [""]
        i = j
    return out


def _signature_line(line: str) -> bool:
    """Чи рядок одразу під директивою — ще один підпис (перевантаження) або параметр директиви, а не опис."""
    stripped = line.strip()
    return bool(_OPTION.match(stripped) or re.fullmatch(r"[\w.]+\(.*\)(?:\s*->.*)?", stripped))


def _substitutions(lines: list[str]) -> tuple[list[str], dict]:
    """Знімає з тексту службові блоки й означення підстановок; повертає решту й словник «ім'я → текст»."""
    substs, out, i = dict(_KNOWN), [], 0
    while i < len(lines):
        line = lines[i]
        if _DROP_LINE.match(line):
            i += 1
            continue
        m = _SUBST_RAW.match(line)
        if m:
            j = _block(lines, i + 1, len(m.group(1)))
            text = html.unescape(re.sub(r"<[^>]+>", "", " ".join(x.strip() for x in lines[i + 1:j])))
            substs.setdefault(m.group(2).strip(), " ".join(text.split()))
            i = j
            continue
        m = _DROP_BLOCK.match(line)
        if m:
            i = _block(lines, i + 1, len(m.group(1)))
            continue
        out.append(line)
        i += 1
    return out, substs


def pydomain_to_markdown(text: str) -> str:
    """Сторінка Sphinx з директивами домену Python → markdown."""
    lines, substs = _substitutions(text.replace("\r\n", "\n").expandtabs(4).split("\n"))
    body = "\n".join(_convert(lines, ""))
    # Невідома підстановка — назва з `header.rst` (`|PDF|`, `|PyMuPDF Office|`): на сайті видно саму назву.
    body = _SUBST_USE.sub(lambda m: substs.get(m.group(1), m.group(1)), body)
    return _sphinx.to_markdown(body).strip() + "\n"


class _PyDomainCtx:
    """`ctx`, що віддає сторінки Sphinx з GitHub уже як markdown; решта звернень — до справжнього."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        parts = urlsplit(url)
        if parts.netloc == "raw.githubusercontent.com" and parts.path.endswith((".rst", ".txt")):
            return pydomain_to_markdown(text)
        return text


@register("ghdocs-history-pydomain")
def ghdocs_history_pydomain(source: dict, ctx) -> list:
    return ghdocs_history(source, _PyDomainCtx(ctx))
