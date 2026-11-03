"""Читач сторінок, чия адреса відрізняється лише рядком запиту або чия назва не лежить у `<h1>`.

`html-query` — `url` — sitemap.xml (закінчується на `.xml`) або перша сторінка; `pages` —
               ще адреси. Адреси із сайтмапа беруться, якщо лежать у `within`, містять
               вираз `match` і не містять жодного з виразів `exclude`. `title_re` — вираз
               назви документа; береться перша непорожня група. Текст починається після
               назви або, якщо є поле `start`, після цього виразу. `end` — вирази, на яких
               текст закінчується (найближчий). `drop` — вирази фрагментів, що вирізаються
               до перетворення в текст. `min_chars` — найкоротше тіло без підзаголовка.
               `accept` — заголовок Accept запиту. `title_fallback` — вираз назви (перша
               група) для сторінки, де `title_re` нічого не дав; тоді текст починається після
               виразу `fallback_start`.

Навіщо. ifthenpay.com віддає кожну статтю за адресою `blog/post/?lang=en&p=14`: спільний читач
`sitemap-html` будує ім'я документа лише зі шляху, і всі статті стали б одним файлом. Назва
статті там лежить в абзаці `<p class="text-xl …">`, а не в `<h1>`. Сайт документації SIBS ставить
перед справжнім `<h1>` порожній і відповідає 403 на запит без заголовка Accept, а центр допомоги
ifthenpay тримає назву в `<h2>`.

Чому окремий модуль, а не поля в `sitemap-html`: інші примірники зібрані й звірені на спільному
читачі, і зміна в ньому ризикує зсувом у готовій роботі.
"""

import html
import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.sitemap import _LOC, _inside


def _name(page: str) -> str:
    """Ім'я документа зі шляху й запиту: без запиту статті блогу зливаються в одну."""
    parts = urlsplit(page)
    return _markup.slug(f"{parts.path} {re.sub(r'[=&]', ' ', parts.query)}")


def _body(page_html: str, url: str, stamp: str, source: dict) -> str:
    found = re.search(source["title_re"], page_html, re.S)
    title_raw = next((g for g in (found.groups() if found else ()) if g and g.strip()), "")
    start_field = "start"
    if not title_raw.strip() and source.get("title_fallback"):
        # Сторінки рішень Easypay не мають `<h1>`: назва лише в `<title>`, а він стоїть перед
        # меню сайту, тож текст починається не після назви, а після `fallback_start`.
        found = re.search(source["title_fallback"], page_html, re.S)
        title_raw = found.group(1) if found else ""
        start_field = "fallback_start"
    title = _markup.html_body(title_raw).strip()
    if not title:
        raise SystemExit(f"На сторінці немає назви за `title_re` ({url}).")
    start = found.end()
    if source.get(start_field):
        at = re.search(source[start_field], page_html)
        if at:
            start = at.end()
    ends = [re.compile(r) for r in source.get("end") or [r"<footer\b"]]
    stop = min((e.start() for e in (r.search(page_html, start) for r in ends) if e),
               default=len(page_html))
    part = page_html[start:stop]
    for pattern in source.get("drop") or ():
        part = re.sub(pattern, "", part, flags=re.S)
    body = _markup.html_body(part)
    _markup.require(title, body, url, int(source.get("min_chars", _markup.MIN_BODY)))
    return _markup.document(title, url, stamp, body, source.get("version", ""))


@register("html-query")
def html_query(source: dict, ctx) -> list[Item]:
    if not source.get("title_re"):
        raise SystemExit(f"{source['id']}: читач html-query вимагає поле `title_re`.")
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач html-query вимагає поле `within`.")
    match = re.compile(source["match"]) if source.get("match") else None
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    accept = source.get("accept", "")
    pages: list[str] = []
    if urlsplit(source["url"]).path.endswith(".xml"):
        for loc in _LOC.findall(ctx.text(source["url"], accept=accept)):
            page = html.unescape(loc)
            if (page not in pages and _inside(page, within) and ctx.allowed(page)
                    and (not match or match.search(page))
                    and not any(r.search(page) for r in exclude)):
                pages.append(page)
    else:
        pages.append(source["url"])
    for page in source.get("pages") or ():
        if not ctx.allowed(page):
            raise SystemExit(f"{source['id']}: адреса {page} поза білим списком — "
                             f"допишіть її в `within`.")
        if page not in pages:
            pages.append(page)
    if not pages:
        raise SystemExit(f"{source['id']}: у {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")
    items = []
    for page in pages:
        name = _name(page)

        def make(page=page):
            return _body(ctx.text(page, accept=accept), page, ctx.stamp, source)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
