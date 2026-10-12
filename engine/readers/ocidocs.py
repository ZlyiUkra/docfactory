"""Читачі документації Oracle Cloud Infrastructure (docs.oracle.com/iaas).

`oci-toc`          — `url` — дерево документації `/iaas/toc.json`; поле `root` — адреса
                     кореневої сторінки розділу (`/iaas/Content/Compute/home.htm`).
                     Документом стає кожна сторінка піддерева, що лежить усередині
                     `within`; текст — основна частина HTML-сторінки. Поле `label` —
                     префікс назви («Compute: Creating an Instance»); `exclude` — префікси
                     адрес піддерева, що не беруться (у Developer Guide це 688 сторінок
                     згенерованого довідника PL/SQL SDK — 31 МБ типів і процедур для всіх
                     сервісів OCI, тобто довідник класів, а не посібник).
`oci-releasenotes` — `url` — тека журналів змін `/iaas/releasenotes/`; поле `services` —
                     імена сервісів, як їх пише `services.json` (`compute`, `network`…).
                     Документом стає кожна нотатка з переліків цих сервісів; до назви
                     дописується дата випуску.

Навіщо окремий модуль. Сайт згенеровано з DITA: markdown-двійників немає, sitemap.xml
немає, а повний перелік сторінок — 18 711 — лежить лише в дереві, з якого скрипт сайту
малює ліве меню. Вузол дерева — хеш, а адреса й назва — у словнику `pages`; шлях
сторінки там відносний, і його основа — окремий словник `sourceBasepaths`.

Зі сторінки береться текст від першого `<article>` (сама тема DITA) до плаваючого змісту
й підвалу: шапка, меню розділу, кнопки відгуку й посилання «на цій сторінці» в корпус
не йдуть. Мовну частину адреси читач ставить сам (`/en-us/iaas/…`): сайт віддає
`/iaas/…` лише перенаправленням.

`oci-faq`          — `url` — сторінка запитань і відповідей на www.oracle.com
                     (`/cloud/free/faq/`). Один документ; кожне запитання стає
                     підрозділом.

Журнали змін: перелік сервісу — сторінка-картки з коротким описом, обрізаним на «...».
Повний текст лежить у кожній нотатці окремо, тож беруться нотатки. Нотатка про кілька
сервісів одразу («New experience in Oracle Cloud Console») стоїть у кількох переліках —
вона береться раз.
"""

import html as html_lib
import json
import re
from urllib.parse import urljoin, urlsplit

from engine.readers import Item, _markup, register

_SITE = "https://docs.oracle.com"
_LANG = "/en-us"
_META_TITLE = re.compile(r'<meta content="([^"]*)" name="title"\s*/?>')
_H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S)
_TAG = re.compile(r"<[^>]+>")
# Кінець основного тексту: що трапиться першим.
_ENDS = ('id="vl-cfs-mount-footer"', "vl-floating-toc-container", 'data-trackas="dcoc-footer"')
# Вкладена тема DITA сайт малює гармошкою: її назва — посилання-перемикач, а не заголовок.
# Так на сторінці «Common Policies» стоять усі шістдесят політик, а на «Always Free
# Resources» — подробиці кожної форми; без заголовка вони злипалися б в один розділ.
_ACCORDION = re.compile(r'<a class="uk-accordion-title[^"]*"[^>]*>(.*?)</a>', re.S)
# Вкладки «Console / CLI / API» сторінок-завдань: підписи — окремим списком над панелями,
# тож у тексті панелі стояли б без назви, і кроки консолі не відрізнялися б від команд CLI.
# Панель — пункт списку-перемикача, що одразу відкриває блок з id; id бувають і «console»,
# і «create-cluster-console», і «managingvnics_tasks_detatch_console», тож назва панелі
# береться не з id, а з підпису на тому самому місці в списку над нею.
_TAB_GROUP = re.compile(r'<ul class="oci-tab-group[^"]*" uk-tab="">(.*?)</ul>', re.S)
_TAB_LABEL = re.compile(r"<a\b[^>]*>(.*?)</a>", re.S)
_TAB_PANEL = re.compile(r'<li\b[^>]*>\s*<div id="[^"]*">')
# Пункт списку, що починається абзацом (`<p>` чи `<div class="p">`): маркер «-» лишався б
# окремим рядком, а текст пункту — окремим абзацом під ним, уже поза списком.
_LI_P = re.compile(r'(<li\b[^>]*>)\s*<(?:p\b[^>]*|div|div class="[^"]*")>')
_NOTE_LINK = re.compile(r'<h2 id="[^"]*"><a href="(/iaas/releasenotes/[^"#]+\.htm)"')
_NOTE_DATE = re.compile(r'class="vl-relnotedate">([^<]+)<')
_MONTHS = {m: i for i, m in enumerate(
    ("January February March April May June July August September October November "
     "December").split(), 1)}


def _localized(path: str) -> str:
    """`/iaas/…` → повна адреса з мовою: саме її сайт віддає без перенаправлення."""
    return _SITE + (path if path.startswith(_LANG + "/") else _LANG + path)


def _inside(url: str, within: list) -> bool:
    return any(url.startswith(w) if w.endswith("/") else url == w for w in within)


def _tabs(part: str) -> str:
    """Список підписів вкладок знімається, а кожна панель під ним отримує заголовок
    «#### <підпис>»; без зрізаного <li> заголовок став би пунктом «- #### CLI»."""
    groups = list(_TAB_GROUP.finditer(part))
    out, pos = [], 0
    for n, group in enumerate(groups):
        out.append(part[pos:group.start()])
        pos = group.end()
        stop = groups[n + 1].start() if n + 1 < len(groups) else len(part)
        for label in _TAB_LABEL.findall(group.group(1)):
            panel = _TAB_PANEL.search(part, pos, stop)
            if not panel:
                break
            name = re.sub(r"\s+", " ", _TAG.sub("", label)).strip()
            out.append(part[pos:panel.start()] + f"<h4>{name}</h4><div>")
            pos = panel.end()
    out.append(part[pos:])
    return "".join(out)


def _page_text(html: str, where: str) -> tuple[str, str]:
    """(назва, тіло) сторінки DITA."""
    m = _META_TITLE.search(html)
    title = html_lib.unescape(m.group(1)).strip() if m else ""
    if not title:
        h1 = _H1.search(html)
        title = re.sub(r"\s+", " ", _TAG.sub("", h1.group(1))).strip() if h1 else ""
    start = html.find('id="dcoc-content-body"')
    start = html.find("<article", max(start, 0))
    if start < 0:
        raise SystemExit(f"{where}: немає <article> — розмітка сторінки змінилася.")
    end = min([i for i in (html.find(e, start) for e in _ENDS) if i > 0] or [len(html)])
    part = _ACCORDION.sub(r"<h3>\1</h3>", html[start:end])
    part = _tabs(part)
    part = _LI_P.sub(r"\1", part)
    body = _markup.html_body(part)
    # Перший заголовок тіла — та сама назва, що вже стоїть у шапці документа.
    first, _, rest = body.partition("\n")
    if first.lstrip("# ").strip() == title:
        body = rest.lstrip("\n")
    return title, body


def _document(ctx, source: dict, url: str, html: str, day: str = "") -> str:
    title, body = _page_text(html, url)
    _markup.require(title, body, url, min_chars=1)
    if source.get("label"):
        title = f"{source['label']}: {title}"
    if day:
        title += f" ({day})"
    return _markup.document(title, url, ctx.stamp, body, source.get("version", ""))


def _name(url: str) -> str:
    path = urlsplit(url).path
    for head in (_LANG + "/iaas/Content/", _LANG + "/iaas/"):
        if path.startswith(head):
            path = path[len(head):]
            break
    return _markup.slug(re.sub(r"\.html?$", "", path))


@register("oci-toc")
def oci_toc(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    exclude = tuple(source.get("exclude") or [])
    root = source.get("root", "")
    if not within or not root:
        raise SystemExit(f"{source['id']}: читач oci-toc вимагає поля `root` і `within`.")
    try:
        toc = json.loads(ctx.text(source["url"]))
        pages, bases = toc["pages"], toc["sourceBasepaths"]
    except (ValueError, KeyError) as exc:
        raise SystemExit(f"{source['url']}: не схоже на дерево toc.json ({exc}).")

    def path_of(node_id: str) -> str:
        page = pages.get(node_id) or {}
        path = str(page.get("p") or "")
        if path.startswith("http"):
            return ""
        if not path.startswith("/"):
            path = str(bases.get(str(page.get("s")), "")) + "/" + path
        return path.split("#")[0]

    found = []

    def seek(nodes) -> None:
        for node in nodes:
            if path_of(node["i"]) == root:
                found.append(node)
            seek(node.get("c") or [])

    def size(node) -> int:
        return 1 + sum(size(c) for c in node.get("c") or [])

    # Та сама сторінка стоїть у дереві й посиланням з інших розділів («Getting Started»
    # посилається на Compute/home.htm без дітей); сам розділ — входження з найбільшим
    # піддеревом.
    seek(toc.get("tree") or [])
    found.sort(key=size, reverse=True)
    if not found:
        raise SystemExit(f"{source['id']}: у дереві немає сторінки {root} — "
                         f"розділ переїхав або поле `root` не те.")
    urls: list[str] = []

    def walk(node) -> None:
        path = path_of(node["i"])
        if path:
            url = _localized(path)
            if (url not in urls and _inside(url, within) and not url.startswith(exclude)
                    and ctx.allowed(url)):
                urls.append(url)
        for child in node.get("c") or []:
            walk(child)

    walk(found[0])
    items = []
    for url in urls:
        name = _name(url)

        def make(url=url):
            return _document(ctx, source, url, ctx.text(url))

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items


def _iso(day: str) -> str:
    """«May 27, 2025» → «2025-05-27»; незнайомий запис — як є."""
    m = re.match(r"([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})", day.strip())
    if not m or m.group(1) not in _MONTHS:
        return day.strip()
    return f"{m.group(3)}-{_MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}"


@register("oci-releasenotes")
def oci_releasenotes(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    services = source.get("services") or []
    if not within or not services:
        raise SystemExit(f"{source['id']}: читач oci-releasenotes вимагає поля "
                         f"`services` і `within`.")
    urls: list[str] = []
    for service in services:
        index = urljoin(source["url"], f"services/{service}/index.htm")
        links = _NOTE_LINK.findall(ctx.text(index))
        if not links:
            raise SystemExit(f"{index}: не знайдено жодної нотатки — розмітка змінилася.")
        for path in links:
            url = _localized(path)
            if url not in urls and _inside(url, within) and ctx.allowed(url):
                urls.append(url)
    items = []
    for url in urls:
        name = _name(url)

        def make(url=url):
            html = ctx.text(url)
            m = _NOTE_DATE.search(html)
            return _document(ctx, source, url, html, _iso(m.group(1)) if m else "")

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items


# Запитання на сторінках www.oracle.com — не заголовок, а div гармошки: без заміни
# на заголовок усі відповіді злипалися б в один розділ, і пошук не міг би віддати
# саме ту, про яку питають.
_FAQ_Q = re.compile(r'<div class="cb105w3">(.*?)</div>', re.S)
# Кнопки гармошки й рекламні заклики між блоками — не текст відповіді.
_FAQ_NOISE = re.compile(r"^(?:Open all Close all|Sign up today|-)$", re.M)
# Рекламний блок «Sign up for Oracle Cloud Free Tier» стоїть на початку й у кінці сторінки.
_FAQ_PROMO = re.compile(r"^## Sign up for Oracle Cloud Free Tier\n.*?(?=^## |\Z)", re.M | re.S)


@register("oci-faq")
def oci_faq(source: dict, ctx) -> list[Item]:
    url = source["url"]
    if not ctx.allowed(url):
        raise SystemExit(f"{source['id']}: {url} поза білим списком.")

    def make():
        html = ctx.text(url)
        start = html.find("<h1")
        if start < 0:
            raise SystemExit(f"{url}: немає <h1> — розмітка сторінки змінилася.")
        end = html.find("<footer", start)
        h1 = _H1.search(html, start)
        title = re.sub(r"\s+", " ", _TAG.sub("", h1.group(1))).strip() if h1 else ""
        part = _FAQ_Q.sub(r"<h3>\1</h3>", html[h1.end() if h1 else start:end if end > 0 else None])
        body = _FAQ_PROMO.sub("", _FAQ_NOISE.sub("", _markup.html_body(part)))
        body = _markup.tidy(body, strip=False)
        _markup.require(title, body, url, min_chars=1)
        if source.get("label"):
            title = f"{source['label']}: {title}"
        return _markup.document(title, url, ctx.stamp, body, source.get("version", ""))

    name = _markup.slug(urlsplit(url).path)
    return [Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make)]
