"""Читачі сторінок, чий текст є лише в зібраному HTML: перелік із sitemap.xml або явний.

`sitemap-html` — `url` — sitemap.xml сайту; документом стає кожна адреса з нього, що
                 лежить усередині поля `within` цього ж джерела. `match` — вираз, який
                 адреса мусить містити; `exclude` — вирази адрес, що не беруться.
                 `end` — вирази, на яких текст сторінки закінчується (найближчий); типово —
                 `</article>`. `drop` — вирази фрагментів HTML, що вирізаються до
                 перетворення в текст (бічна навігація всередині статті).
                 `start` — вираз, після якого шукається `<h1>` статті (коли раніше
                 стоїть `<h1>` шапки сайту). `version` — версія всіх документів джерела.
`html-list`    — явний перелік: документом стає `url` і кожна адреса з `pages`; решта
                 полів ті самі. Для окремих статей на сайтах, де брати треба кілька
                 сторінок, а не розділ: Вікіпедія, блог.

Навіщо. refactoring.guru не має ні markdown-двійників, ні llms.txt, а меню сайту —
не повний перелік: техніки рефакторингу лежать у корені сайту поруч зі службовими
сторінками. Повний перелік є тільки в sitemap.xml, тож `html-pages` (перелік із
посилань сторінок-змістів) тут не підходить, а `sitemap-md` чекає markdown.

Текст — від `<h1>` до кінця статті. Мова блоку коду записана в атрибуті
`lang="typescript"`, а не в класі, тож тут вона переноситься в клас `language-…`:
інакше блоки «До» й «Після» п'ятьма мовами на сторінці техніки стали б п'ятьма
однаковими на вигляд безіменними блоками.

Чому окремий модуль, а не поля в `html-pages` чи `sitemap-md`: інші примірники зібрані
й звірені, а правка спільного читача — ризик зсуву в готовій роботі.
"""

import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.sitemap import _LOC, _inside

_H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S)
_PRE_LANG = re.compile(r'<pre\b[^>]*\blang="([\w+#-]+)"[^>]*>')
# Пункт списку, весь текст якого — абзац: перенос рядка між <li> і <p> стає пробілом
# після «- », і абзац відривав текст від маркера порожнім рядком.
_LI_P = re.compile(r"<li>\s*<p>(.*?)</p>\s*</li>", re.S)


def _text(html: str, url: str, stamp: str, version: str, ends: list, drops: list,
          start_at=None) -> str:
    at = start_at.search(html) if start_at else None
    m = _H1.search(html, at.end() if at else 0)
    if not m:
        raise SystemExit(f"На сторінці немає <h1> ({url}) — документ не записую.")
    title = _markup.html_body(m.group(1)).strip()
    start = m.end()
    stop = min((e.start() for e in (r.search(html, start) for r in ends) if e),
               default=len(html))
    part = html[start:stop]
    for r in drops:
        part = r.sub("", part)
    part = _LI_P.sub(r"<li>\1</li>", part)
    part = _PRE_LANG.sub(lambda p: f'<pre class="language-{p.group(1)}">', part)
    body = _markup.html_body(part)
    _markup.require(title, body, url)
    return _markup.document(title, url, stamp, body, version)


@register("sitemap-html")
def sitemap_html(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач sitemap-html вимагає поле `within` — "
                         f"інакше сайтмап потягнув би весь сайт.")
    match = re.compile(source["match"]) if source.get("match") else None
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    ends, drops, start_at = _fields(source)
    pages: list[str] = []
    for loc in _LOC.findall(ctx.text(source["url"])):
        page = loc.rstrip("/")
        if (page not in pages and _inside(page, within) and ctx.allowed(page)
                and (not match or match.search(page))
                and not any(r.search(page) for r in exclude)):
            pages.append(page)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")

    return _items(source, ctx, pages, ends, drops, start_at)


@register("html-list")
def html_list(source: dict, ctx) -> list[Item]:
    pages = [source["url"]] + list(source.get("pages") or ())
    for page in pages:
        if not ctx.allowed(page):
            raise SystemExit(f"{source['id']}: адреса {page} поза білим списком — "
                             f"допишіть її в `within`.")
    return _items(source, ctx, pages, *_fields(source))


def _fields(source: dict) -> tuple:
    ends = [re.compile(r) for r in source.get("end") or [r"</article>"]]
    drops = [re.compile(r, re.S) for r in source.get("drop") or ()]
    start_at = re.compile(source["start"]) if source.get("start") else None
    return ends, drops, start_at


def _items(source: dict, ctx, pages: list, ends: list, drops: list, start_at) -> list[Item]:
    items = []
    for page in pages:
        name = _markup.slug(urlsplit(page).path)

        def make(page=page):
            return _text(ctx.text(page), page, ctx.stamp, source.get("version", ""),
                         ends, drops, start_at)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
