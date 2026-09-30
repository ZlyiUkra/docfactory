"""Читач сайту документації, чий повний текст є лише у зібраному HTML сторінок.

`html-pages` — `url` і необов'язковий список `index` — сторінки-змісти: посилання з
               них, що проходять поле `within`, стають документами. `pages` — адреси,
               яких у змістах немає (вкладки посібника, що живуть окремими адресами).
               `exclude` — вирази адрес, що не беруться (їх дає інше джерело).
               `end` — вирази, на яких текст сторінки закінчується; типово — `<footer`.
               `version` — версія всіх документів джерела.

Навіщо. Сайти tailwindcss.com усіх версій зібрано з MDX, але головного в MDX немає:
таблиця класів сторінки («p-4 → padding: 1rem») у v1–v3 генерується з коду самого
tailwindcss під час збирання сайту, у v4 — обчислюється виразом JS просто в розмітці, а
спільні блоки («Responsive design», «Using a custom value») — окремі компоненти. Усе це
є тільки в готовому HTML. Мапи сайту немає ні в одній версії, тож перелік — бічне меню.

Текст сторінки — від заголовка `<h1>` до кінця статті: меню стоїть раніше, підвал і
«On this page» — пізніше. Підсвітка коду (Shiki у v4, рядки-термінал у v3) кладе кожен
рядок у свій `<span>` без символу переносу: без вставленого тут переносу весь блок коду
злипся б в один рядок.
"""

import re
from urllib.parse import urljoin, urlsplit

from engine.readers import Item, _markup, register

_HREF = re.compile(r'href="([^"#?]+)"')
_H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S)
# Підсвічений рядок має додаткові класи («line -mx-5 … bg-sky-300/15»), тож клас «line»
# упізнається як перше слово атрибута, а не як увесь атрибут.
_LINE = re.compile(r'</span>(?=<span class="(?:line|flex)(?:\s[^"]*)?")')


def _text(html: str, url: str, stamp: str, version: str, ends: list) -> str:
    m = _H1.search(html)
    if not m:
        raise SystemExit(f"На сторінці немає <h1> ({url}) — документ не записую.")
    title = _markup.html_body(m.group(1)).strip().lstrip("#").strip()
    start = m.end()
    stop = min((e.start() for e in (r.search(html, start) for r in ends) if e),
               default=len(html))
    body = _markup.html_body(_LINE.sub("</span>\n", html[start:stop]))
    _markup.require(title, body, url)
    return _markup.document(title, url, stamp, body, version)


@register("html-pages")
def html_pages(source: dict, ctx) -> list[Item]:
    index = [source["url"]] + list(source.get("index", []))
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    ends = [re.compile(r) for r in source.get("end") or [r"<footer\b"]]
    cache: dict[str, str] = {}
    urls: list[str] = []
    names: set[str] = set()

    def add(url: str) -> None:
        url = url.rstrip("/")
        name = _markup.slug(urlsplit(url).path)
        if (name not in names and ctx.allowed(url)
                and not any(r.search(url) for r in exclude)):
            names.add(name)
            urls.append(url)

    for page in index:
        html = ctx.text(page)
        cache[page.rstrip("/")] = html
        for href in [page] + _HREF.findall(html):
            add(urljoin(page, href))
    if len(urls) <= len(index):
        raise SystemExit(f"На сторінках-змістах {', '.join(index)} не знайдено "
                         f"посилань на сторінки документації — розмітка змінилася.")
    for page in source.get("pages") or ():
        add(page)

    items = []
    for url in urls:
        name = _markup.slug(urlsplit(url).path)

        def make(url=url):
            html = cache.pop(url, None) or ctx.text(url)
            return _text(html, url, ctx.stamp, source.get("version", ""), ends)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
