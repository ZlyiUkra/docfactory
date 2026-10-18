"""Читач DocFX: документація learn.microsoft.com з її репозиторію GitHub.

`docfx` — набір сторінок learn.microsoft.com, зібраний з markdown репозиторію
(dotnet/AspNetCore.Docs, dotnet/AspNetDocs). `url` — дерево гілки через API
(…/repos/ВЛАСНИК/РЕПО/git/trees/ГІЛКА?recursive=1), поле `docset` — тека набору в
репозиторії («aspnetcore»), `site` — адреса набору на сайті
(«https://learn.microsoft.com/en-us/aspnet/core/»). Документом стає кожен .md набору,
крім вставок (`includes/`) і прикладів (`samples/`, `snippets/`). Поле `name_prefix`
стає перед іменем документа — щоб сторінки двох наборів одного примірника не ділили ключ.

Версії. DocFX тримає всі версії продукту в одному файлі: блок
«:::moniker range=">= aspnetcore-8.0"» … «:::moniker-end» сайт показує лише у версіях,
що підпадають під вираз, а поле шапки `monikerRange` каже, в яких версіях сторінка є
взагалі. Поле джерела `moniker` («aspnetcore-8.0») розгортає кожну сторінку так, як сайт
показує її з `?view=aspnetcore-8.0`: чужі блоки випадають, сторінки поза `monikerRange` у
перелік не потрапляють. Кожна версія — окреме джерело однієї родини (families у
config.json): незмінний розділ сусідніх версій зливається в один фрагмент з версіями
обох, і вектор для нього рахується раз. Без поля `moniker` лишається текст усіх блоків.
Поле `link: "github"` — для версій, яких сайт уже не показує: посилання документа веде
на файл у репозиторії на тому коміті, з якого він узятий.

Монікери без номера (`monikers`). У SQL Server версії звуться «sql-server-2017»,
«sql-server-ver15» (2019), «sql-server-ver16» (2022), «sql-server-linux-ver15», а поряд
стоять продукти взагалі без номера — «azuresqldb-current», «fabric». Порядок версій
продукту тут з назви не виводиться, тож поле джерела `monikers` дає його явно: перелік
переліків, кожен — монікери одного продукту від найстарішого до найновішого (як їх
показує learn.microsoft.com/api/familyTrees). З полем «>= sql-server-ver15» — це ver15 і
все новіше в переліку того самого продукту; монікер, якого в полі немає, не справджує
нічого. `moniker` тоді може бути й переліком: редакція «SQL Server 2022» — це те, що сайт
показує і для «sql-server-ver16», і для «sql-server-linux-ver16»; сторінка входить у
редакцію, якщо її монікери перетинаються з переліком, а блок лишається, якщо його вираз
справджує хоч один монікер, з якими сторінка є в редакції. Монікери сторінки — з поля шапки
`monikerRange`; без нього — з `build.fileMetadata.monikerRange` у docfx.json набору (шаблон
шляху → вираз; з кількох шаблонів діє останній, як у DocFX), а без нього — з
`moniker_range` групи вмісту; `exclude_monikers` з того ж docfx.json віднімаються. Саме так
сторінку бачить сайт: шапка сторінки T-SQL з «=fabric» робить її сторінкою Fabric, хоч
шаблон теки t-sql/** Fabric не називає. Позначки блоків пишуть по-різному
(«::: moniker range="…"», «:::moniker range=…», зрідка «::: monikerRange="…"»), і з полем
`monikers` читач приймає всі. Без поля — усе, як було.

Сторінки YAML. Поле `yaml_pages: true` бере ще й .yml набору, але лише ті, де є текст:
«YamlMime:FAQ» (питання й відповіді стають розділами). Сторінки-вітрини (Landing, Hub),
змісти й перелік варіантів — самі посилання, вони не беруться.

Ще кілька полів, без яких усе лишається, як було: `exclude` — вирази шляхів у репозиторії,
що не беруться; `rows: true` — сітка «:::row:::»/«:::column:::» стає рядками (перемикач
продуктів над синтаксисом T-SQL — одним рядком через « | »), а не блоком із відступом;
`icons` — об'єкт «частина імені файла значка → текст»: значок посеред рядка
(«**Applies to:** :::image type="icon" source="…/yes-icon.svg"::: SQL Server») стає текстом
(«✓»), решта таких значків випадає. Адреса дерева «…/git/trees/КОМІТ:ТЕКА?recursive=1» — дерево
лише однієї теки, коли повне GitHub обрізає (SupportArticles-docs): шляхи доповнюються текою.

Розмітка DocFX, яку читач розгортає до тексту:
- «[!INCLUDE[…](шлях)]» — вставка, теж зі своїми блоками версій і вставками;
- «[!code-csharp[](шлях?name=snippet_1)]» і «:::code … source="шлях" id="snippet_1":::» —
  приклад коду з файла репозиторію: фрагмент між позначками «<snippet_1>» … «</snippet_1>»
  чи «#region snippet_1» … «#endregion», рядки `range`, або файл цілком. Шлях
  «~/../ТЕКА/…» веде в залежний репозиторій (поле `repos`: тека → «власник/репо/гілка»):
  так DocFX кладе їх поруч із головним під час збирання сайту;
- «<xref:uid>» і «[текст](xref:uid)» — назва статті з тим самим `uid` у шапці або ім'я
  типу чи члена API, як його показує сайт (`displayProperty=nameWithType` — «Тип.Член»,
  `fullName` — повне ім'я);
- вкладки «# [Visual Studio](#tab/visual-studio)» … «---» — підписи, а не заголовки: як
  заголовки вони різали б статтю на розділи «Visual Studio» і «.NET CLI»;
- «:::zone pivot="…"» — кожен варіант з підписом; «:::image …:::», «[!div …]», «[!VIDEO …]»
  випадають; «> [!NOTE]» стає «> Note:».
"""

import json
import posixpath
import re
import textwrap
from urllib.parse import unquote, urlsplit

from engine.readers import Item, _markup, register

# Дерево гілки чи коміту; «КОМІТ:ТЕКА» — дерево лише однієї теки (у SupportArticles-docs
# повне дерево GitHub обрізає), шляхи якого читач доповнює назад до кореня репозиторію.
_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/([^/:%]+)(?:(?::|%3A)(.+))?$")
_MONIKER = re.compile(r'^[ \t]*:::[ \t]*moniker[ \t]+range="([^"]*)"[ \t]*$'
                      r"|^[ \t]*:::[ \t]*moniker-end[ \t]*$", re.M)
_TERM = re.compile(r"(>=|<=|>|<|=)?\s*([a-z][a-z-]*?)-(\d+(?:\.\d+)*)")
# Для поля `monikers`: позначки в усіх написаннях, які трапляються в sql-docs, і умова —
# знак та ціле ім'я монікера, з цифрами чи без.
_MONIKER_ANY = re.compile(r'^[ \t]*:::[ \t]*moniker(?:[ \t]+range|range)[ \t]*=[ \t]*"([^"]*)"[ \t:]*$'
                          r"|^[ \t]*:::[ \t]*moniker-end[ \t:]*$", re.M | re.I)
_NAMED_TERM = re.compile(r"(>=|<=|>|<|=)?\s*([a-z][a-z0-9.-]*[a-z0-9])")
_YAML_MIME = re.compile(r"\A﻿?#+\s*YamlMime:(\w+)")
_YAML_KEY = re.compile(r"""^("[^"]*"|'[^']*'|[^\s:#"'-][^:#]*?|-[^\s:#][^:#]*?)\s*:(?:\s+(.*))?$""")
_INCLUDE = re.compile(r"\[!INCLUDE\s*\[[^\]]*\]\(\s*<?([^)\s>]+)>?[^)]*\)\]", re.I)
_CODE_REF = re.compile(r"\[!code-([\w+#.-]+)\s*\[[^\]]*\]\(\s*<?([^)\s>]+)>?[^)]*\)\]")
_CODE_TRIPLE = re.compile(r":::code\s+(.*?):::", re.S)
_ATTR = re.compile(r'([\w-]+)="([^"]*)"')
_XREF_TAG = re.compile(r"<xref:([^>\s]+)>")
# Текст посилання сам буває з дужками в коді: «[`[JSImport]` attribute](xref:…)».
_XREF_LINK = re.compile(r"\[((?:`[^`\n]*`|\[[^\]\n]*\]|[^\]`\n])*)\]\(<?xref:([^)\s>]+)>?\)")
_TAB = re.compile(r"^#{1,6}\s*\[([^\]]+)\]\(#tab/[^)]*\)\s*$")
_ZONE = re.compile(r'^\s*:::\s*zone\s+(pivot|target)="([^"]*)"\s*:?:?:?\s*$')
_ZONE_END = re.compile(r"^\s*:::\s*zone-end\s*:?:?:?\s*$")
_IMAGE_COMPLEX = re.compile(r'^\s*:::image\s+type="complex".*?:::image-end:::\s*$', re.S | re.M)
_TRIPLE_LINE = re.compile(r"^\s*:::[\w-]+(?:\s.*)?:::\s*$|^\s*:::[\w-]+:::\s*$")
_NO_LOC = re.compile(r':::no-loc\s+text="((?:\\.|[^"\\])*)":::')
_ICON = re.compile(r':::image\s+type="[a-z]+"\s[^\n]*?:::')
_ALERT = re.compile(r"\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", re.I)
_DIV = re.compile(r"^\s*>?\s*\[!(?:div|VIDEO)\b[^\]]*\]\s*$", re.I)
_FENCE = re.compile(r"^\s*(```+|~~~+)")
_HR = re.compile(r"^\s*-{3,}\s*$")
_PIVOT = re.compile(r"^\s*-\s+id:\s*(\S+)\s*\n\s+title:\s*(.+?)\s*$", re.M)
# Позначка фрагмента в коментарі будь-якої мови прикладу: «// <snippet_1>»,
# «<!-- </snippet_1> -->», «@* <snippet_1> *@», «# <snippet_1>». Без коментаря рядок
# «<div>» — це розмітка самого прикладу, і він лишається.
_SNIPPET_MARK = re.compile(r"^\s*(?://|#|<!--|@\*|/\*|'|--|;|\{/\*)\s*</?[\w.-]+>\s*"
                           r"(?:-->|\*@|\*/|\*/\})?\s*$")
_REGION_MARK = re.compile(r"^\s*#\s*(?:end)?region\b.*$", re.I)
# Приклад, узятий файлом цілком, може бути завдовжки в сотні рядків; хвіст за межею
# лишається у файлі, а документ каже, де його шукати.
MAX_CODE_LINES = 400
MAX_DEPTH = 6
_LANG = {"cshtml": "cshtml", "razor": "razor", "csharp": "csharp", "javascript": "javascript",
         "typescript": "typescript", "json": "json", "xml": "xml", "html": "html"}


def _version_key(text: str) -> tuple:
    return tuple(int(x) for x in text.split("."))


def in_range(expr: str, moniker: str) -> bool:
    """Чи показує сайт у версії `moniker` блок з виразом `expr`. Вираз — альтернативи
    через «||», кожна з умов через пробіл («>= aspnetcore-6.0 < aspnetcore-8.0»); умова
    без знака — рівність. Номер без мінорної частини («aspnetcore-9») — те саме, що
    «.0»: так автори іноді пишуть. Умова про інший продукт альтернативу не справджує."""
    product, _, number = moniker.rpartition("-")
    have = _version_key(number)
    have += (0,) * (3 - len(have))
    for alt in expr.split("||"):
        terms = _TERM.findall(alt)
        if not terms:
            continue
        ok = True
        for op, name, num in terms:
            want = _version_key(num)
            want += (0,) * (3 - len(want))
            if name != product:
                ok = False
            elif not {">=": have >= want, "<=": have <= want, ">": have > want,
                      "<": have < want}.get(op, have == want):
                ok = False
        if ok:
            return True
    return False


def _monikers(text: str, moniker: str) -> str:
    """Текст без блоків, яких сайт у цій версії не показує. Блоки DocFX не вкладаються,
    тож досить пройти позначки по черзі."""
    if not moniker:
        return _MONIKER.sub("", text)
    out, pos, keep = [], 0, True
    for m in _MONIKER.finditer(text):
        if keep:
            out.append(text[pos:m.start()])
        keep = in_range(m.group(1), moniker) if m.group(1) is not None else True
        pos = m.end()
    if keep:
        out.append(text[pos:])
    return "".join(out)


class MonikerOrder:
    """Монікери продуктів у порядку версій — поле джерела `monikers`. Вираз DocFX — це
    альтернативи через «||», кожна з умов через пробіл; умова без знака — рівність,
    «>=»/«>»/«<=»/«<» рахуються в переліку того самого продукту. Результат — множина
    монікерів, яку вираз описує; ім'я, якого в переліках немає, дає порожню множину."""

    def __init__(self, lists: list):
        self._lists = [[str(m).lower() for m in lst] for lst in lists]
        self._pos = {m: (i, j) for i, lst in enumerate(self._lists) for j, m in enumerate(lst)}
        self._memo: dict = {}

    def expand(self, expr: str) -> frozenset:
        expr = (expr or "").strip().lower()
        if expr not in self._memo:
            out: set = set()
            for alt in expr.split("||"):
                cur = None
                for op, name in _NAMED_TERM.findall(alt):
                    got = self._term(op, name)
                    cur = got if cur is None else cur & got
                out |= cur or set()
            self._memo[expr] = frozenset(out)
        return self._memo[expr]

    def _term(self, op: str, name: str) -> set:
        if name not in self._pos:
            return set()
        i, j = self._pos[name]
        lst = self._lists[i]
        return set({">=": lst[j:], ">": lst[j + 1:], "<=": lst[:j + 1], "<": lst[:j]}.get(op, [name]))


def _glob(pattern: str):
    """Шаблон шляху DocFX («ado/**/*.md», «./*.yml») як вираз: «**/» — будь-скільки тек,
    зокрема жодної, «*» — будь-що в межах однієї теки."""
    p = pattern.strip()
    if p.startswith("./"):
        p = p[2:]
    out, i = [], 0
    while i < len(p):
        if p.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif p.startswith("**", i):
            out.append(".*")
            i += 2
        elif p[i] == "*":
            out.append("[^/]*")
            i += 1
        elif p[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(p[i]))
            i += 1
    return re.compile("".join(out) + r"\Z")


def _monikers_where(text: str, keep) -> str:
    """Текст без блоків, чий вираз `keep` відкидає; `keep` None — лишаються всі блоки,
    випадають лише позначки. Позначки — в усіх написаннях (`_MONIKER_ANY`)."""
    if keep is None:
        return _MONIKER_ANY.sub("", text)
    out, pos, on = [], 0, True
    for m in _MONIKER_ANY.finditer(text):
        if on:
            out.append(text[pos:m.start()])
        on = keep(m.group(1)) if m.group(1) is not None else True
        pos = m.end()
    if on:
        out.append(text[pos:])
    return "".join(out)


def yaml_load(text: str):
    """Підмножина YAML, якою DocFX пише сторінки FAQ: словники й списки за відступом,
    рядки в лапках і без (зокрема на кількох рядках), блоки «|» і «>». Блок зберігає
    відносні відступи — відповідь FAQ буває списком із вкладеними пунктами чи кодом.
    Бібліотеки YAML примірник не тягне: більше цим файлам не треба."""
    lines = text.replace("\r\n", "\n").replace("\t", "    ").split("\n")
    n = len(lines)

    def ind(s):
        return len(s) - len(s.lstrip(" "))

    def skip(i):
        while i < n and (not lines[i].strip() or lines[i].lstrip().startswith("#")):
            i += 1
        return i

    def dash(s):
        t = s.lstrip()
        return t == "-" or t.startswith("- ")

    def scalar(v):
        v = v.strip()
        if len(v) > 1 and v[0] in "\"'" and v[-1] == v[0]:
            inner = v[1:-1]
            return inner.replace("''", "'") if v[0] == "'" else inner.replace('\\"', '"')
        return re.sub(r"\s+#\s.*$", "", v)

    def block(i, parent, style):
        body = []
        while i < n and (not lines[i].strip() or ind(lines[i]) > parent):
            body.append(lines[i])
            i += 1
        body = textwrap.dedent("\n".join(body)).strip("\n").split("\n")
        if not style.startswith(">"):
            return "\n".join(body), i
        out, para = [], []
        for ln in body:
            if ln.strip() and not ln.startswith(" "):
                para.append(ln.strip())
                continue
            if para:
                out.append(" ".join(para))
                para = []
            out.append(ln)
        if para:
            out.append(" ".join(para))
        return "\n".join(out), i

    def value(v, i, indent):
        if v in ("|", "|-", "|+", ">", ">-", ">+"):
            return block(i + 1, indent, v)
        if not v:
            j = skip(i + 1)
            if j < n and (ind(lines[j]) > indent or (ind(lines[j]) == indent and dash(lines[j]))):
                return node(j)
            return "", i + 1
        i += 1
        if v[0] in "\"'":
            while not (len(v) > 1 and v.rstrip().endswith(v[0])) and i < n:
                v += " " + lines[i].strip()
                i += 1
        else:
            while (i < n and lines[i].strip() and ind(lines[i]) > indent
                   and not lines[i].lstrip().startswith("#")):
                v += " " + lines[i].strip()
                i += 1
        return scalar(v), i

    def node(i):
        return seq(i, ind(lines[i])) if dash(lines[i]) else mapping(i, ind(lines[i]))

    def seq(i, indent):
        out = []
        while True:
            i = skip(i)
            if i >= n or ind(lines[i]) != indent or not dash(lines[i]):
                return out, i
            rest = lines[i].lstrip()[1:]
            item = rest.lstrip()
            if not item:
                j = skip(i + 1)
                if j < n and ind(lines[j]) > indent:
                    val, i = node(j)
                else:
                    val, i = None, i + 1
            elif _YAML_KEY.match(item):
                lines[i] = " " * (indent + 1 + len(rest) - len(item)) + item
                val, i = mapping(i, ind(lines[i]))
            else:
                val, i = value(item, i, indent)
            out.append(val)

    def mapping(i, indent):
        out = {}
        while True:
            i = skip(i)
            if i >= n or ind(lines[i]) != indent or dash(lines[i]):
                return out, i
            m = _YAML_KEY.match(lines[i].strip())
            if not m:
                i += 1
                continue
            out[scalar(m.group(1))], i = value((m.group(2) or "").strip(), i, indent)

    try:
        start = skip(0)
        return node(start)[0] if start < n else {}
    except (IndexError, ValueError, RecursionError):
        return {}


def faq_page(text: str) -> tuple[dict, str]:
    """Сторінка «YamlMime:FAQ» як markdown: (поля metadata з назвою, тіло). Розділ FAQ —
    заголовок другого рівня, кожне питання — заголовок під ним (без назви розділу —
    другого рівня), відповідь — його текст."""
    data = yaml_load(text)
    if not isinstance(data, dict):
        return {}, ""
    meta = {k: v for k, v in (data.get("metadata") or {}).items() if isinstance(v, str)}
    if isinstance(data.get("title"), str) and data["title"].strip():
        meta["title"] = data["title"].strip()
    out = []
    for key in ("summary", "text"):
        if isinstance(data.get(key), str) and data[key].strip():
            out += [data[key].strip(), ""]
    for sec in data.get("sections") or []:
        if not isinstance(sec, dict):
            continue
        name = " ".join(str(sec.get("name") or "").split())
        # Розділ «Ignored» — домовленість DocFX: сайт його назви не показує.
        if name.lower() == "ignored":
            name = ""
        if name:
            out += [f"## {name}", ""]
        if isinstance(sec.get("text"), str) and sec["text"].strip():
            out += [sec["text"].strip(), ""]
        for q in sec.get("questions") or []:
            if not isinstance(q, dict):
                continue
            question = " ".join(str(q.get("question") or "").split())
            if question:
                out += [("### " if name else "## ") + question, ""]
            if isinstance(q.get("answer"), str) and q["answer"].strip():
                out += [q["answer"].strip(), ""]
    extra = data.get("additionalContent")
    if isinstance(extra, str) and extra.strip():
        out += [extra.strip(), ""]
    return meta, "\n".join(out)


_ROW = re.compile(r"^\s*:::\s*row(?:\s[^:]*)?:::\s*$")
_ROW_END = re.compile(r"^\s*:::\s*row-end\s*:::\s*$")
_COLUMN = re.compile(r"^\s*:::\s*column(?:\s[^:]*)?:::\s*$")
_COLUMN_END = re.compile(r"^\s*:::\s*column-end\s*:::\s*$")


def _layout_rows(text: str) -> str:
    """Сітка «:::row:::» / «:::column:::» поза огорожами коду — звичайними рядками. Вміст
    колонок DocFX пише з відступом у вісім пробілів, і без сітки він ставав би блоком
    коду. Рядок, де кожна колонка — один короткий рядок (перемикач продуктів «SQL Server |
    SQL Database | …» над синтаксисом), стає одним рядком через « | »; інакше колонки
    йдуть абзацами одна за одною."""
    if ":::" not in text:
        return text
    out, fence, cols, cur = [], "", None, None
    for ln in text.split("\n"):
        fm = _FENCE.match(ln)
        if fence or (fm and cols is None):
            out.append(ln)
            if fence and fm and not ln.strip()[len(fence):].strip():
                fence = ""
            elif not fence and fm:
                fence = fm.group(1)
            continue
        if cols is None:
            if _ROW.match(ln):
                cols = []
            else:
                out.append(ln)
            continue
        if _COLUMN.match(ln):
            cur = []
        elif _COLUMN_END.match(ln):
            if cur is not None:
                cols.append([c for c in cur if c])
            cur = None
        elif _ROW_END.match(ln):
            if cols and all(len(c) <= 1 and len(c[0] if c else "") <= 200 for c in cols):
                out.extend(["", " | ".join(c[0] for c in cols if c), ""])
            else:
                for c in cols:
                    out.extend(["", *c, ""])
            cols = cur = None
        elif cur is not None:
            cur.append(ln.strip())
    if cols is not None:
        for c in cols + ([cur] if cur else []):
            out.extend(["", *[x for x in c if x], ""])
    return "\n".join(out)


def _dedent_block(lines: list[str]) -> list[str]:
    body = textwrap.dedent("\n".join(lines)).split("\n")
    while body and not body[-1].strip():
        body.pop()
    while body and not body[0].strip():
        body.pop(0)
    return body


def _lines_range(lines: list[str], spec: str) -> list[str]:
    """Рядки за переліком DocFX «5-10,12,20-»: з одиниці, кінці включно."""
    out = []
    for part in spec.split(","):
        a, dash, b = part.strip().partition("-")
        if not a.strip().isdigit():
            continue
        start = int(a)
        end = (int(b) if b.strip().isdigit() else len(lines)) if dash else start
        out.extend(lines[start - 1:end])
    return out


def snippet(text: str, name: str = "", rng: str = "", start: str = "", end: str = "") -> list | None:
    """Рядки прикладу коду, як їх вставляє DocFX. `name` — позначка фрагмента (теги в
    коментарі чи #region, без різниці в регістрі; кілька однойменних ділянок
    склеюються), `rng` — рядки, `start`/`end` — межі рядків. Нічого не знайдено — None:
    документ без прикладу кращий за чужий шматок файла."""
    lines = text.replace("\r\n", "\n").split("\n")
    if name:
        n = re.escape(name)
        open_tag = re.compile(r"<\s*" + n + r"\s*>", re.I)
        close_tag = re.compile(r"<\s*/\s*" + n + r"\s*>", re.I)
        region = re.compile(r"^\s*#\s*region\s+" + n + r"\s*$", re.I)
        picked, inside = [], False
        for ln in lines:
            if not inside and open_tag.search(ln) and _SNIPPET_MARK.match(ln):
                inside = True
                continue
            if inside and close_tag.search(ln) and _SNIPPET_MARK.match(ln):
                inside = False
                continue
            if inside:
                picked.append(ln)
        if not picked:
            depth, inside = 0, False
            for ln in lines:
                if not inside:
                    if region.match(ln):
                        inside, depth = True, 1
                    continue
                if re.match(r"^\s*#\s*region\b", ln, re.I):
                    depth += 1
                elif re.match(r"^\s*#\s*endregion\b", ln, re.I):
                    depth -= 1
                    if depth == 0:
                        inside = False
                        continue
                picked.append(ln)
        if not picked:
            return None
        lines = picked
    elif rng:
        lines = _lines_range(lines, rng)
    elif start.isdigit():
        lines = lines[int(start) - 1:int(end) if end.isdigit() else len(lines)]
    lines = [ln for ln in lines if not (_SNIPPET_MARK.match(ln) or _REGION_MARK.match(ln))]
    body = _dedent_block(lines)
    return body or None


def _strip_front(text: str) -> str:
    return _markup.front_matter(text)[1]


def _drop_comments(text: str) -> str:
    """Текст без коментарів HTML поза огорожами коду. Прибрати їх треба до вставок:
    у коментарі вставки not-latest-version.md записано, як її вставляти, — разом із
    самою «[!INCLUDE]», і розгорнута вона вставляла себе в себе. Коментар усередині
    прикладу коду — частина прикладу і лишається."""
    out, fence, comment = [], "", False
    for ln in text.split("\n"):
        fm = _FENCE.match(ln)
        if fence and not comment:
            out.append(ln)
            if fm and not ln.strip()[len(fence):].strip():
                fence = ""
            continue
        if comment:
            if "-->" not in ln:
                continue
            ln, comment = ln.split("-->", 1)[1], False
        while "<!--" in ln:
            before, _, after = ln.partition("<!--")
            if "-->" in after:
                ln = before + after.split("-->", 1)[1]
            else:
                ln, comment = before, True
        if not fence and fm:
            fence = fm.group(1)
        out.append(ln)
    return "\n".join(out)


@register("docfx")
def docfx(source: dict, ctx) -> list[Item]:
    parts = urlsplit(source["url"])
    m = _TREE.match(parts.path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував адресу дерева гілки "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/ГІЛКА[:ТЕКА].")
    owner, repo, branch, folder = m.groups()
    folder = unquote(folder).strip("/") if folder else ""
    docset = source["docset"].strip("/")
    site = source["site"].rstrip("/") + "/"
    moniker = source.get("moniker", "")
    # Перелік монікерів редакції; рядок — редакція з одного, як і було.
    wanted = [m for m in ([moniker] if isinstance(moniker, str) else moniker) if m]
    order = MonikerOrder(source["monikers"]) if source.get("monikers") else None
    if order is not None:
        wanted = [m.lower() for m in wanted]
    view = f"?view={moniker}" if isinstance(moniker, str) and moniker else ""
    prefix = source.get("name_prefix", "")
    repos = source.get("repos") or {}
    yaml_pages = source.get("yaml_pages") is True
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    # Значки посеред рядка («**Applies to:** :::image type="icon" source="…/yes-icon.svg":::
    # SQL Server …»): з полем `icons` (частина імені файла → текст) названий значок стає
    # текстом, решта випадає. Без поля рядок той самий, що й був.
    icons = source.get("icons")
    # Сітка «:::row:::» — лише з полем `rows: true`: у примірниках, зібраних раніше, її
    # вміст лишається таким, як був.
    rows = source.get("rows") is True
    tree = _markup_json(ctx, source["url"])
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")

    def raw_of(path: str) -> str | None:
        """Адреса файла за шляхом від кореня головного репозиторію. Перша тека, названа в
        `repos`, — залежний репозиторій; шлях, що виходить за корінь, — ні до чого."""
        path = posixpath.normpath(path)
        if path.startswith("../") or path == "..":
            return None
        head, _, rest = path.partition("/")
        if head in repos:
            return f"https://raw.githubusercontent.com/{repos[head]}/{rest}"
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

    def resolve(ref: str, base_dir: str) -> str | None:
        ref = unquote(ref.split("?", 1)[0].split("#", 1)[0]).strip()
        if not ref or re.match(r"^[a-z]+://", ref):
            return None
        if ref.startswith("~/"):
            return posixpath.normpath(posixpath.join(docset, ref[2:]))
        if ref.startswith("/"):
            return posixpath.normpath(ref.lstrip("/"))
        return posixpath.normpath(posixpath.join(base_dir, ref))

    # Вставки однакові для всіх сторінок і розгортаються тисячі разів (у sql-docs —
    # «[!INCLUDE[ssnoversion-md]…]» майже в кожному абзаці); короткі тримаються в пам'яті
    # до кінця джерела, а не читаються щоразу зі сховища. Текст той самий.
    small: dict = {}

    def get(path: str) -> str | None:
        if path in small:
            return small[path]
        url = raw_of(path)
        if url is None or not ctx.allowed(url):
            return None
        code, data = ctx.fetch(url)
        if code != "200":
            return None
        text = data.decode("utf-8", errors="replace").replace("\r\n", "\n").lstrip("﻿")
        if "/includes/" in "/" + path and len(text) <= 16384:
            small[path] = text
        return text

    # docfx.json набору — монікери тек (fileMetadata) і групи; лише з полем `monikers`.
    rules: list = []
    drops: list = []
    group_range = ""
    pivot_files = [f"{docset}/zone-pivot-groups.yml"]
    if order is not None:
        try:
            conf = json.loads(get(f"{docset}/docfx.json") or "{}").get("build") or {}
        except ValueError as exc:
            raise SystemExit(f"{docset}/docfx.json: не JSON ({exc}) — монікерів тек не знаю.")
        meta_rules = conf.get("fileMetadata") or {}
        rules = [(_glob(g), r) for g, r in (meta_rules.get("monikerRange") or {}).items()
                 if isinstance(r, str)]
        drops = [(_glob(g), {str(m).lower() for m in v})
                 for g, v in (meta_rules.get("exclude_monikers") or {}).items() if isinstance(v, list)]
        groups = conf.get("groups") or {}
        for content in conf.get("content") or []:
            grp = groups.get(content.get("group") or "") if isinstance(content, dict) else None
            if isinstance(grp, dict) and grp.get("moniker_range"):
                group_range = grp["moniker_range"]
                break
        for f in (meta_rules.get("zone_pivot_group_filename") or {}).values():
            if isinstance(f, str):
                pivot_files.append(f"{docset}/{f.removesuffix('.json')}.yml")

    def page_monikers(rel: str, meta: dict):
        """Монікери, з якими сайт показує сторінку (шлях від теки набору); None — сторінка
        без версій, є в кожній."""
        own = meta.get("monikerRange", "")
        if not own:
            for rx, rng in rules:
                if rx.match(rel):
                    own = rng
            own = own or group_range
        if not own:
            return None
        got = order.expand(own)
        for rx, ms in drops:
            if rx.match(rel):
                got = got - ms
        return got

    # Підписи варіантів «:::zone pivot» — з переліку набору; без нього підписом стає id.
    pivots: dict = {}
    for pf in pivot_files if source.get("pivots", True) else ():
        found = {pm.group(1): pm.group(2).strip().strip('"') for pm in _PIVOT.finditer(get(pf) or "")}
        for key, label in found.items():
            pivots.setdefault(key, label)

    paths = []
    for entry in tree["tree"]:
        path = entry.get("path", "")
        if folder:
            path = f"{folder}/{path}"
        if (entry.get("type") != "blob" or not path.startswith(docset + "/")
                or not (path.endswith(".md") or (yaml_pages and path.endswith(".yml")))):
            continue
        segs = path.split("/")
        if any(s in ("includes", "samples", "snippets", "_includes") for s in segs[:-1]):
            continue
        if segs[-1].lower() in ("readme.md", "license.md", "toc.md", "toc.yml"):
            continue
        if any(r.search(path) for r in exclude):
            continue
        paths.append(path)

    # Шапки всіх сторінок читаються вже під час переліку: `monikerRange` вирішує, чи є
    # сторінка в цій версії, а `uid` → назва потрібні посиланням xref з інших сторінок.
    titles: dict = {}
    pages = []
    shown: dict = {}
    for path in paths:
        text = get(path)
        if text is None:
            continue
        if path.endswith(".yml"):
            mime = _YAML_MIME.match(text)
            if not mime or mime.group(1) != "FAQ":
                continue
            meta, _ = faq_page(text)
        else:
            meta, _ = _markup.front_matter(text)
        if meta.get("uid"):
            titles[meta["uid"]] = _markup.title_of(meta, path)
        if order is not None:
            got = page_monikers(path[len(docset) + 1:], meta)
            here = [m for m in wanted if got is None or m in got]
            if wanted and not here:
                continue
            shown[path] = frozenset(here) if wanted else None
            pages.append(path)
            continue
        rng = meta.get("monikerRange", "")
        if wanted and rng and not any(in_range(rng, m) for m in wanted):
            continue
        pages.append(path)

    def xref(uid: str, display: str = "") -> str:
        uid = unquote(uid)
        query = ""
        if "?" in uid:
            uid, _, query = uid.partition("?")
        uid = uid.split("#", 1)[0].strip('"')
        if uid in titles:
            return titles[uid]
        name = re.sub(r"\(.*\)$", "", uid).rstrip("*")
        name = re.sub(r"`+\d+", "", name)
        segs = name.split(".")
        if "displayProperty=fullName" in query:
            shown = name
        elif "displayProperty=nameWithType" in query:
            shown = ".".join(segs[-2:])
        else:
            shown = segs[-1]
        return f"`{shown}`" if shown else uid

    def code_block(lang: str, ref_path: str | None, attrs: dict) -> str:
        if ref_path is None:
            return ""
        text = get(ref_path)
        if text is None:
            return ""
        lines = snippet(text, attrs.get("name", ""), attrs.get("range", ""),
                        attrs.get("start", ""), attrs.get("end", ""))
        if lines is None:
            return ""
        tail = []
        if len(lines) > MAX_CODE_LINES:
            lines = lines[:MAX_CODE_LINES]
            tail = [f"// … (далі — у файлі {ref_path})"]
        lang = _LANG.get(lang, lang)
        return "\n".join(["", "```" + lang, *lines, *tail, "```", ""])

    def versions_of(text: str, here) -> str:
        """Текст без блоків, яких сайт у цій редакції не показує. `here` — монікери
        редакції, з якими є сторінка (лише з полем `monikers`)."""
        if order is not None:
            return _monikers_where(text, None if here is None else
                                   (lambda e: bool(order.expand(e) & here)))
        if isinstance(moniker, str):
            return _monikers(text, moniker)
        return _monikers_where(text, (lambda e: any(in_range(e, m) for m in wanted))
                               if wanted else None)

    def expand(text: str, path: str, depth: int, stack: tuple = (), here=None) -> str:
        """Текст файла `path` (сторінки чи вставки) з розгорнутими версіями, вставками й
        прикладами коду. Шляхи вставки — від її власної теки, як у DocFX."""
        base = posixpath.dirname(path)
        text = versions_of(_drop_comments(text), here)
        text = _IMAGE_COMPLEX.sub("", text)

        def include(im):
            target = resolve(im.group(1), base)
            if target is None or depth >= MAX_DEPTH or target in stack:
                return ""
            inner = get(target)
            if inner is None:
                return ""
            return expand(_strip_front(inner).strip("\n"), target, depth + 1, stack + (path,), here)

        text = _INCLUDE.sub(include, text)

        def code_ref(cm):
            ref = cm.group(2)
            attrs = {}
            if "?" in ref:
                for kv in ref.split("?", 1)[1].split("#", 1)[0].split("&"):
                    k, _, v = kv.partition("=")
                    attrs[k] = unquote(v)
            frag = ref.split("#", 1)[1] if "#" in ref else ""
            lm = re.fullmatch(r"L(\d+)(?:-L(\d+))?", frag)
            if lm:
                attrs["range"] = f"{lm.group(1)}-{lm.group(2) or lm.group(1)}"
            elif frag and not attrs.get("name"):
                attrs["name"] = frag
            return code_block(cm.group(1), resolve(ref, base), attrs)

        def code_triple(cm):
            attrs = dict(_ATTR.findall(cm.group(1)))
            if "source" not in attrs:
                return ""
            if attrs.get("id"):
                attrs["name"] = attrs["id"]
            return code_block(attrs.get("language", ""), resolve(attrs["source"], base), attrs)

        text = _CODE_REF.sub(code_ref, text)
        return _CODE_TRIPLE.sub(code_triple, text)

    def clean(text: str) -> str:
        """Решта розмітки DocFX поза огорожами коду: вкладки, варіанти, зображення,
        позначки на кшталт «[!div]»; посилання xref — назвами."""
        out, fence = [], ""
        for ln in (_layout_rows(text) if rows else text).split("\n"):
            fm = _FENCE.match(ln)
            if fence:
                out.append(ln)
                if fm and ln.strip().startswith(fence[0] * len(fence)) and not ln.strip()[len(fence):].strip():
                    fence = ""
                continue
            if fm:
                fence = fm.group(1)
                out.append(ln)
                continue
            tm = _TAB.match(ln)
            if tm:
                out.extend(["", f"**{tm.group(1).strip()}**", ""])
                continue
            zm = _ZONE.match(ln)
            if zm:
                if zm.group(1) == "pivot":
                    names = [pivots.get(p.strip(), p.strip()) for p in zm.group(2).split(",")]
                    out.extend(["", f"**{', '.join(names)}**", ""])
                continue
            if _ZONE_END.match(ln) or _HR.match(ln) or _DIV.match(ln):
                continue
            ln = _NO_LOC.sub(lambda nm: nm.group(1).replace('\\"', '"'), ln)
            if icons is not None:
                ln = _ICON.sub(lambda im: next((v for k, v in icons.items() if k in im.group(0)), ""), ln)
            if _TRIPLE_LINE.match(ln):
                continue
            ln = _XREF_LINK.sub(lambda xm: xm.group(1) or xref(xm.group(2)), ln)
            ln = _XREF_TAG.sub(lambda xm: xref(xm.group(1)), ln)
            ln = _ALERT.sub(lambda am: am.group(1).capitalize() + ":", ln)
            out.append(ln)
        return "\n".join(out)

    items, used = [], set()
    for path in pages:
        rel = path[len(docset) + 1:].removesuffix(".md")
        if yaml_pages:
            rel = rel.removesuffix(".yml")
        page = re.sub(r"(^|/)index$", r"\1", rel)
        here = shown.get(path)
        if order is not None and wanted:
            # Сторінку лише для Linux сайт відкриває з ?view= монікера Linux.
            view = f"?view={next(m for m in wanted if here is None or m in here)}"
        # Версій, яких сайт уже не показує, адреса з ?view= не відкриє — вона переводить
        # на найновішу; тоді посилання веде на сам файл того коміту.
        url = (f"https://github.com/{owner}/{repo}/blob/{branch}/{path}"
               if source.get("link") == "github" else site + page + view)
        name = _markup.slug(re.sub(r"(^|/)index$", "", rel) or "index")
        if name in used:
            name = _markup.slug(rel)
        if yaml_pages and name in used:
            name = _markup.slug(path[len(docset) + 1:])
        used.add(name)
        if prefix:
            name = f"{prefix}-{name}"

        def make(path=path, url=url, here=here):
            text = get(path)
            if text is None:
                raise SystemExit(f"{path}: файл не прочитався — документ не записую.")
            if path.endswith(".yml"):
                meta, rest = faq_page(text)
            else:
                meta, rest = _markup.front_matter(text)
            title = _markup.title_of(meta, url)
            body = _markup.markdown_body(clean(expand(rest, path, 0, (), here)))
            _markup.require(title, body, url, min_chars=1)
            return _markup.document(title, url, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    if not items:
        raise SystemExit(f"{source['url']}: у наборі {docset} немає жодної сторінки"
                         f"{' для ' + ', '.join(wanted) if wanted else ''}.")
    return items


def _markup_json(ctx, url: str) -> dict:
    import json
    try:
        data = json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(data, dict) or not isinstance(data.get("tree"), list):
        raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
    return data
