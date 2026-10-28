"""Читачі ecmarkup — розмітки, якою tc39 видає ECMA-262 і ECMA-402.

`toc`  — багатосторінкове видання (ECMA-262): зі змісту беруться адреси глав,
         кожна глава тягнеться окремою сторінкою і стає окремим документом.
`page` — одна сторінка з розділами (ECMA-402): сторінка ділиться на верхні
         розділи й додатки, кожен стає документом.

Розмітка зчищається так, щоб вийшов той самий вигляд, що в решті корпусу:
заголовок підрозділу окремим рядком, абзаци через порожній рядок, кроки
алгоритмів рядками з дефісом — саме по цих заголовках `common/corpus.py` ділить
документ на фрагменти. Код перенесено з колишніх завантажувачів практики без змін
по суті; змінилося тільки те, що адреса й дозвіл беруться з оголошення джерел.
"""

import html as html_lib
import re

from engine.readers import Item, register

# Розмітка видання мініфікована: значення атрибутів без лапок, а одразу за
# іменем файлу може стояти якір (href=indexed-collections.html#sec-...).
_HREF = re.compile(r"href=[\"']?([a-z0-9-]+\.html)[\"']?")
_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
_FIRST_CLAUSE_ID = re.compile(r"<emu-clause[^>]*\bid=[\"']?([\w.-]+)[\"']?[\s>]")
# Верхній розділ або додаток однієї сторінки ecmarkup: атрибути там без лапок.
_TOP = re.compile(r"<(emu-clause|emu-annex) id=([^\s>]+)[^>]*>\s*<h1><span class=secnum>"
                  r"([0-9]+|Annex [A-Z])(?=</span>|\s*<span)")


def _body(page: str) -> str:
    """Вміст сторінки без бічного меню: від spec-container до кінця."""
    start = page.find("<div id=spec-container")
    return page[start:] if start != -1 else page


def _strip(chunk: str) -> str:
    """Зчищає розмітку, лишаючи заголовки і абзаци окремими рядками."""
    chunk = re.sub(r"<(script|style)\b.*?</\1>", " ", chunk, flags=re.S)
    chunk = re.sub(r"<h1[^>]*>", "\n\n", chunk)
    chunk = re.sub(r"</h1>", "\n\n", chunk)
    chunk = re.sub(r"<li\b[^>]*>", "\n- ", chunk)
    chunk = re.sub(r"</(p|li|tr|dd|dt|emu-alg|emu-note|emu-table|div)>", "\n", chunk)
    chunk = re.sub(r"<br\s*/?>", "\n", chunk)
    chunk = re.sub(r"<[^>]+>", " ", chunk)
    chunk = html_lib.unescape(chunk)

    lines = [re.sub(r"[ \t ]+", " ", ln).strip() for ln in chunk.splitlines()]
    text = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", text).strip("\n")


def _title(page: str) -> str:
    """Заголовок розділу: «20 Fundamental Objects»."""
    m = _H1.search(_body(page))
    if not m:
        return ""
    return _strip(m.group(1)).replace("\n", " ").strip()


# Рядок-заголовок розділу в уже зчищеному тілі: «20.1.3 …», «B.1.1 …»,
# «Annex B …». Ним або довжиною тіла глава доводить, що вона — глава.
_SECTION_LINE = re.compile(r"^(?:Annex [A-Z]|[A-Z]|\d+)(?:\.\d+)*\s+\S", re.M)

# Найкоротше тіло справжньої глави без нумерованих підзаголовків — службові
# сторінки видання: колофон 920 символів, бібліографія 2049. Сторінка-заглушка
# («This page has moved.», тіло помилки) до цієї межі не дотягує.
_MIN_BODY = 400


def _looks_like_chapter(title: str, body: str) -> bool:
    return bool(title) and (bool(_SECTION_LINE.search(body))
                            or len(body) >= _MIN_BODY)


def _document_262(page: str, url: str, stamp: str) -> str:
    """Готовий текст документа глави 262: трирядкова шапка, порожній рядок, тіло.

    Сторінку, якої не впізнає, відкидає винятком — тим самим, яким відмовляють
    решта читачів. Раніше перевірки не було, і заглушка «This page has moved.»
    ставала документом на двадцять один символ: refresh писав його поверх
    доброї глави, manifest фіксував суму пошкодження, а check далі казав
    «без змін»."""
    title = _title(page)
    body = _strip(_body(page))
    if not _looks_like_chapter(title, body):
        raise SystemExit(
            f"Сторінка не схожа на главу видання ({url}): "
            f"{'немає заголовка h1' if not title else 'тіло куце і без жодного підзаголовка'}"
            f" — документ не записую, наявний лишається як був.")
    anchor = _FIRST_CLAUSE_ID.search(_body(page))
    source = f"{url}#{anchor.group(1)}" if anchor else url
    return f"# {title}\n# джерело: {source}\n# отримано: {stamp}\n\n{body}\n"


def _page_id(name: str) -> str:
    """Ідентифікатор глави — слаг сторінки видання, без позиції і без .html."""
    return name[:-5] if name.endswith(".html") else name


def _file_name(position: int, name: str) -> str:
    """Ім'я файла глави: позиція у змісті плюс слаг сторінки. Позиція тут
    і є тим, що зсувається, коли у зміст вклинюють нову главу."""
    return f"{position:02d}-{_page_id(name)}.txt"


def _chapters(toc_html: str) -> list[str]:
    """Імена сторінок глав у порядку змісту багатосторінкового видання."""
    seen, out = set(), []
    for name in _HREF.findall(toc_html):
        if name not in seen:
            seen.add(name)
            out.append(name)
    if not out:
        raise SystemExit("У змісті не знайдено жодного посилання на главу — "
                         "розмітка сторінки змінилася, читача треба поправити.")
    return out


@register("toc")
def toc(source: dict, ctx) -> list[Item]:
    base = source["url"]
    names = _chapters(ctx.text(base))
    items = []
    for pos, name in enumerate(names, 1):
        url = base + name

        def make(url=url):
            return _document_262(ctx.text(url), url, ctx.stamp)

        # Ідентифікатор — з префіксом джерела: обидва видання починаються
        # главами Scope і Conformance, і голий слаг «scope» означав би два
        # документи одразу — refresh за таким id перезаписував би обидва.
        items.append(Item(id=f"{source['id']}/{_page_id(name)}",
                          file=_file_name(pos, name), make=make))
    return items


# ── ECMA-402: одна сторінка → документ на верхній розділ ──────────────────

def _slug(cid: str) -> str:
    return re.sub(r"^(sec-|annex-)", "", cid)


def _name_402(num: str, cid: str) -> str:
    tag = f"{int(num):02d}" if num.isdigit() else num.replace("Annex ", "")
    return f"402-{tag}-{_slug(cid)}.txt"


def _chapters_402(page: str) -> list[tuple[str, str, str]]:
    """(id, номер, html розділу) для кожного верхнього розділу і додатків A/B."""
    hits = list(_TOP.finditer(page))
    out = []
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(page)
        cid, num = m.group(2), m.group(3)
        if cid in ("sec-colophon", "sec-copyright-and-software-license"):
            continue
        out.append((cid, num, page[m.start():end]))
    if not out:
        raise SystemExit("На сторінці ECMA-402 не знайдено жодного розділу — "
                         "розмітка змінилася, читача треба поправити.")
    return out


def _document_402(chunk: str, cid: str, url: str, stamp: str) -> str:
    """Та сама відмова, що в _document_262: розділ без заголовка h1 чи з куцим
    тілом без підзаголовків — виняток, а не куций документ поверх доброго.
    Колишній тихий fallback «немає h1 — хай назвою буде cid» саме й ховав
    такий випадок."""
    m = _H1.search(chunk)
    title = _strip(m.group(1)).replace("\n", " ").strip() if m else ""
    body = _strip(chunk)
    if not _looks_like_chapter(title, body):
        raise SystemExit(
            f"Розділ {cid} не схожий на розділ ECMA-402: немає заголовка або "
            f"тіло куце і без підзаголовків — документ не записую.")
    return f"# {title}\n# джерело: {url}#{cid}\n# отримано: {stamp}\n\n{body}\n"


@register("page")
def page(source: dict, ctx) -> list[Item]:
    url = source["url"]
    html = ctx.text(url)
    items = []
    for cid, num, chunk in _chapters_402(html):
        def make(chunk=chunk, cid=cid):
            return _document_402(chunk, cid, url, ctx.stamp)

        # Той самий префікс джерела, що в toc: слаги розділів двох видань
        # збігаються, ключем їх робить лише ім'я джерела попереду.
        items.append(Item(id=f"{source['id']}/{_slug(cid)}",
                          file=_name_402(num, cid), make=make))
    return items


# ── Редакції: одна сторінка видання → документ на кожен розділ ────────────
#
# Редакції ECMA-262 і ECMA-402 лежать кожна однією сторінкою: ecmarkup з 2016 року
# (emu-clause, emu-annex, emu-intro) і старша верстка ES5.1, ES2015 і 402 1.0
# (section). Обидві дають розділу id і заголовок h1 з номером у span.secnum.
#
# Документом стає кожен розділ окремо — лише власний текст, без підрозділів, — а
# ключем документа id розділу. Номер у ключ не потрапляє навмисно: між редакціями
# номери зсуваються (Array.prototype.includes — 22.1.3.11 у 2016, 23.1.3.16 у 2026),
# а id лишається, і однаковий текст різних редакцій зливається в один фрагмент з
# переліком редакцій. Номер стоїть у кінці назви документа.
#
# З тієї ж причини посилання на розділ, яке видання пише номером («see 7.1.4»),
# стає назвою розділу: інакше перенумерація міняла б текст і тоді, коли сам розділ
# не змінився ні словом.

_CLAUSE_TAG = re.compile(r"<(/?)(emu-clause|emu-annex|emu-intro|section)\b([^>]*)>")
_ID_ATTR = re.compile(r"\bid=[\"']?([^\"'\s>]+)")
_SECNUM = re.compile(r"<span class=[\"']?secnum[\"']?[^>]*>(.*?)</span>", re.S)
# Посилання всередині тексту: href на розділ і текст, що є номером («7.1.4», «B.3.2»,
# «Annex B», «15.4.4.14»).
_XREF = re.compile(r"<a\s+href=[\"']?#([^\"'\s>]+)[\"']?[^>]*>([^<]*)</a>")
# Номер кроку, який архівні видання 2021–2026 вписують у сам пункт прихованим span («1. »,
# «a. », «iv. »): у чернетці й старших виданнях його немає, і з ним однакові кроки двох
# редакцій не зливалися б.
_LIST_MARKER = re.compile(r"<span[^>]*\baria-hidden=[\"']?true[\"']?[^>]*>\s*[0-9a-zA-Z]+\.\s*</span>")
_NUMBER_TEXT = re.compile(r"^\s*(?:Annex [A-Z]|[A-Z](?:\.\d+)+|\d+(?:\.\d+)*)\s*$")
# Службові розділи видання: колофон і ліцензія.
_SKIP_IDS = ("sec-colophon", "sec-copyright-and-software-license")


def _clauses(page: str) -> list[dict]:
    """Розділи сторінки в порядку появи: id, номер, назва і власний html — тіло без
    вкладених розділів."""
    names = ("emu-clause", "emu-annex", "emu-intro") if "<emu-clause" in page else ("section",)
    stack: list[dict] = []
    out: list[dict] = []
    for m in _CLAUSE_TAG.finditer(page):
        closing, name, attrs = m.group(1), m.group(2), m.group(3)
        if name not in names:
            continue
        if not closing:
            cid = _ID_ATTR.search(attrs)
            node = {"id": cid.group(1) if cid else "", "start": m.end(), "outer": m.start(),
                    "holes": []}
            stack.append(node)
            out.append(node)
            continue
        if not stack:
            continue
        node = stack.pop()
        node["end"] = m.start()
        if stack:
            stack[-1]["holes"].append((node["outer"], m.end()))
    clauses = []
    for node in out:
        if "end" not in node or not node["id"].startswith("sec-") or node["id"] in _SKIP_IDS:
            continue
        pos, parts = node["start"], []
        for a, b in node["holes"]:
            parts.append(page[pos:a])
            pos = b
        parts.append(page[pos:node["end"]])
        own = "".join(parts)
        h1 = _H1.search(own)
        number, title = "", ""
        if h1 and not own[:h1.start()].strip():
            head = h1.group(1)
            num = _SECNUM.search(head)
            if num:
                number = _strip(num.group(1)).strip()
                head = head[:num.start()] + head[num.end():]
            title = " ".join(_strip(head).split())
            own = own[h1.end():]
        clauses.append({"id": node["id"], "number": number, "title": title, "html": own})
    if not clauses:
        raise SystemExit("На сторінці видання не знайдено жодного розділу — розмітка "
                         "змінилася, читача треба поправити.")
    return clauses


def _bare_title(title: str) -> str:
    """Назва без переліку параметрів: «ToNumber ( argument )» → «ToNumber»."""
    return re.sub(r"\s*\(.*\)\s*$", "", title).strip() or title


def _named_refs(html: str, titles: dict) -> str:
    """Посилання номером на розділ цієї ж сторінки → «§ Назва розділу»."""
    def swap(m):
        target, text = m.group(1), m.group(2)
        if target in titles and _NUMBER_TEXT.match(text):
            return f"§ {html_lib.escape(titles[target])}"
        return m.group(0)
    return _XREF.sub(swap, html)


def _clause_name(cid: str) -> str:
    """Ключ документа з id розділу: «sec-array.prototype.includes» →
    «array-prototype-includes»."""
    return "-".join(re.findall(r"[a-z0-9]+", _slug(cid).lower())) or "x"


@register("clauses")
def clauses(source: dict, ctx) -> list[Item]:
    """Поля: `url` — сторінка видання; `version` — мітка редакції; `label` — що
    стоїть перед номером у назві документа («ECMA-262»)."""
    url = source["url"]
    version = str(source.get("version") or "")
    label = source.get("label") or ""
    page = ctx.text(url)
    found = _clauses(page)
    titles = {c["id"]: _bare_title(c["title"]) for c in found if c["title"]}
    items, taken = [], set()
    for c in found:
        name = _clause_name(c["id"])
        if name in taken:
            continue
        taken.add(name)

        def make(c=c):
            body = _strip(_named_refs(_LIST_MARKER.sub("", c["html"]), titles))
            if not body.strip():
                raise SystemExit(f"Розділ {c['id']} без власного тексту — документ не записую.")
            where = " ".join(x for x in (label, f"§{c['number']}" if c["number"] else "") if x)
            title = f"{c['title'] or c['id']} — {where}" if where else (c["title"] or c["id"])
            head = f"# {title}\n# джерело: {url}#{c['id']}\n# отримано: {ctx.stamp}\n"
            if version:
                head += f"# версія: {version}\n"
            return f"{head}\n{body}\n"

        # Розділ без власного тексту (рубрика, увесь вміст якої — підрозділи) документом
        # не стає: фрагмента з нього однаково не вийшло б.
        if not _strip(_LIST_MARKER.sub("", c["html"])).strip():
            continue
        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items
