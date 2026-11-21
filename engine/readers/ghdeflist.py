"""Читач посібника, де параметри описано списком означень, а не заголовками: кожен термін стає розділом.

`ghdocs-history-deflist` — те саме, що `ghdocs-history` (усі його поля), і дві заміни в кожному файлі з
                           raw.githubusercontent.com перед розбором:
                           - термін списку означень pandoc — рядок, що починається кодом у зворотних лапках, а під
                             ним стоїть означення «:   текст», — стає заголовком на рівень глибшим за розділ, у
                             якому він стоїть. Назва — самі імена з терміна без значень («--toc-depth», «-f, -r,
                             --from, --read», «title, author, date»), повний термін лишається першим рядком розділу,
                             а текст означення — звичайними абзацами без відступу;
                           - блок назви pandoc на початку файла («% Pandoc User's Guide», «% John MacFarlane»,
                             «% January 19, 2013») стає заголовком «# Pandoc User's Guide»;
                           - атрибути pandoc у фігурних дужках знімаються із заголовків («## General options
                             {.options}» → «## General options») і з термінів («[`--reference-doc=`*FILE*]
                             {#option--reference-doc}»), а рядки меж блоку «::: {#input-formats}» зникають. Коли
                             ідентифікатор заголовка — повне ім'я з крапками, що закінчується текстом заголовка
                             («### stringify {#pandoc.utils.stringify}»), заголовком стає це повне ім'я:
                             «### pandoc.utils.stringify».
                           Поле `terms: false` вимикає першу заміну: у довіднику фільтрів Lua термінами записано
                           параметри функцій, і кожен параметр розділом бути не має.

Навіщо. Посібник pandoc (`MANUAL.txt`, до лінії 1.17 — `README`) описує кожен параметр командного рядка і кожну
змінну шаблону терміном списку означень: «`--toc-depth=`*NUMBER*», порожній рядок, «:   Specify the number of
section levels…». Заголовки мають лише групи: «General writer options» — це сто параметрів під одним заголовком на
двадцять тисяч символів. Фрагменти такого розділу ріжуться за довжиною, жоден не названий параметром, який описує,
і питання «pandoc --toc-depth» знаходить їх лише за збігом слів у тексті.

Чому імена без значень. Термін між версіями міняється («`--lof`» у 3.5, «`--lof[=true|false]`» далі), і в назві
розділу він дав би тому самому параметрові різних версій різні ключі: у видачі параметр займав би кілька місць.

Чому обгортка, а не поле в `ghdocs-history`: перелік тегів, імена документів, версії й адреси сайту той читач
складає сам і звірений у десятках примірників. Тут лише текст файла міняється дорогою.
"""

import re
from urllib.parse import urlsplit

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_ATX = re.compile(r"^(#{1,6})\s+\S")
_SETEXT = re.compile(r"^(=+|-+)\s*$")
_FENCE = re.compile(r"^(```|~~~)")
_CODE = re.compile(r"`([^`]+)`")
_DEF = re.compile(r"^:\s{1,4}")
_TITLE = re.compile(r"\A%[ \t]*(.+)\n(?:%.*\n)*")
_ATTR = re.compile(r"^(#{1,6})\s+(.*?)\s*\{([^}]*)\}\s*#*\s*$")
_SPAN = re.compile(r"^\[(`.*)\]\{[^}]*\}\s*$")
_DIV = re.compile(r"^:{3,}(?:\s*\{[^}]*\}|\s*[\w-]*)?\s*$")


def _names(term: str) -> str:
    """«`-f` *FORMAT*, `--from=`*FORMAT*» → «-f, --from»."""
    names = []
    for chunk in _CODE.findall(term):
        name = re.split(r"[=\[\s<(|]", chunk.strip(), maxsplit=1)[0].rstrip(",;:")
        if name and name not in names:
            names.append(name)
    # У терміні параметра після імені йдуть його значення («`--wrap=auto`|`none`|`preserve`») — вони не імена.
    if names and names[0].startswith("-"):
        names = [n for n in names if n.startswith("-")]
    return ", ".join(names)


def _heading(m: re.Match) -> str:
    """Заголовок без атрибутів pandoc; повне ім'я з ідентифікатора, коли воно закінчується текстом заголовка."""
    text = m.group(2).strip()
    ident = next((a[1:] for a in m.group(3).split() if a.startswith("#")), "")
    bare = text.strip("` ")
    if "." in ident and ident.rsplit(".", 1)[-1] == bare:
        text = ident
    return f"{m.group(1)} {text}"


def deflist_to_headings(text: str, terms: bool = True) -> str:
    """Терміни списків означень → заголовки; решта тексту лишається як була."""
    text = text.replace("\r\n", "\n")
    if m := _TITLE.match(text):
        text = f"# {m.group(1).strip()}\n\n" + text[m.end():]
    lines = text.split("\n")
    out, level, fence, i = [], 1, "", 0
    while i < len(lines):
        line = lines[i]
        if fence:
            out.append(line)
            if line.startswith(fence):
                fence = ""
            i += 1
            continue
        if m := _FENCE.match(line):
            fence = m.group(1)
            out.append(line)
            i += 1
            continue
        if _DIV.match(line):
            i += 1
            continue
        if m := _ATTR.match(line):
            line = _heading(m)
        elif m := _SPAN.match(line):
            line = m.group(1)
        elif (line.rstrip().endswith("}") and i + 1 < len(lines) and _SETEXT.match(lines[i + 1])
              and not line.startswith((" ", "\t"))):
            # заголовок з підкресленням («Reader options {.options}» над «-------») теж несе атрибути
            line = re.sub(r"\s*\{[^{}]*\}\s*$", "", line)
        if m := _ATX.match(line):
            level = len(m.group(1))
        elif _SETEXT.match(line) and i and lines[i - 1].strip() and not lines[i - 1].startswith((" ", "\t")):
            level = 1 if line.startswith("=") else 2
        if terms and line.startswith("`"):
            j = i + 1 if i + 1 < len(lines) and lines[i + 1].strip() else i + 2
            if j < len(lines) and _DEF.match(lines[j]) and (name := _names(line)):
                out += ["", "#" * min(level + 1, 6) + " " + name, "", line.rstrip(), ""]
                out.append(_DEF.sub("", lines[j]))
                i = j + 1
                # тіло означення: рядки з відступом і порожні, до першого рядка з першої колонки
                while i < len(lines) and (not lines[i].strip() or lines[i].startswith(("    ", "\t"))):
                    body = lines[i]
                    out.append(body[4:] if body.startswith("    ") else body.lstrip("\t"))
                    i += 1
                continue
        out.append(line)
        i += 1
    return "\n".join(out)


class _DefListCtx:
    """`ctx`, що віддає файли з GitHub із термінами-заголовками; решта звернень — до справжнього."""

    def __init__(self, ctx, terms: bool = True):
        self._ctx = ctx
        self._terms = terms

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        if urlsplit(url).netloc == "raw.githubusercontent.com":
            return deflist_to_headings(text, self._terms)
        return text


@register("ghdocs-history-deflist")
def ghdocs_history_deflist(source: dict, ctx) -> list:
    return ghdocs_history(source, _DefListCtx(ctx, source.get("terms") is not False))
