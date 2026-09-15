"""Читач `nextdata` — сайт документації на Next.js, де вміст сторінки лежить у
`<script id="__NEXT_DATA__">` серіалізованим деревом елементів.

Дерево чистіше за HTML: у ньому немає бічного меню, підвалу й кнопок, а блоки
коду стоять цілими рядками. Перелік сторінок — посилання зі сторінок-змістів
(`url` джерела плюс список `index`), обмежені полем `within`; кожна сторінка
стає документом. Сторінки-змісти й самі документи, тож їхній HTML, уже
завантажений для переліку, вдруге не тягнеться.
"""

import json
import re
from urllib.parse import urljoin, urlsplit

from engine.readers import Item, _markup, register

_NEXT = re.compile(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
                   re.S)
_HREF = re.compile(r'href="([^"#?]+)"')


def _document(html: str, url: str, stamp: str, version: str) -> str:
    m = _NEXT.search(html)
    if not m:
        raise SystemExit(f"На сторінці немає __NEXT_DATA__ ({url}) — документ не записую.")
    try:
        props = json.loads(m.group(1))["props"]["pageProps"]
        content = props["content"]
        tree = json.loads(content) if isinstance(content, str) else content
    except (ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f"__NEXT_DATA__ не має вмісту сторінки ({url}): {exc}")
    # Та сама друкарська помилка шапки, що в markdown react.dev («script:» замість
    # «title:»), доїжджає й сюди — назва береться тим самим запасним шляхом.
    meta = props.get("meta") or {}
    title = str(_markup.title_of(meta, url) if isinstance(meta, dict) and meta else "")
    body = _markup.tree_body(tree)
    _markup.require(title, body, url)
    return _markup.document(title, url, stamp, body, version)


@register("nextdata")
def nextdata(source: dict, ctx) -> list[Item]:
    pages = [source["url"]] + list(source.get("index", []))
    cache: dict[str, str] = {}
    urls: list[str] = []
    names: set[str] = set()
    for page in pages:
        html = ctx.text(page)
        cache[page.rstrip("/")] = html
        for href in [page] + _HREF.findall(html):
            # «/learn» і «/learn/» — одна сторінка: без зрізаної риски вона
            # потрапляла в перелік двічі з тим самим іменем файла.
            url = urljoin(page, href).rstrip("/")
            name = _markup.slug(urlsplit(url).path)
            if name not in names and ctx.allowed(url):
                names.add(name)
                urls.append(url)
    # Сторінка-зміст сама по собі — ще не перелік: без жодного посилання, крім
    # себе, це не зміст, а заглушка чи сторінка помилки.
    if len(urls) <= len(pages):
        raise SystemExit(f"На сторінках-змістах {', '.join(pages)} не знайдено "
                         f"посилань на сторінки документації — розмітка змінилася.")
    items = []
    for url in urls:
        name = _markup.slug(urlsplit(url).path)

        def make(url=url):
            html = cache.pop(url, None) or ctx.text(url)
            return _document(html, url, ctx.stamp, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
