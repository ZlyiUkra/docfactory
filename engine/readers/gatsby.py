"""Читачі сайтів на Gatsby, які поруч зі сторінкою віддають її дані JSON-ом.

Для сторінки `/docs/x.html` Gatsby тримає `/page-data/docs/x.html/page-data.json`,
а в ньому — HTML самої статті (`markdownRemark.html`) і назву, без меню й підвалу.
Тягнеться саме цей JSON; HTML сторінки потрібен лише для переліку.

`gatsby`      — документація: перелік — посилання зі сторінки `url` (меню) плюс поле
                `pages` — адреси сторінок, живих на сайті, але прибраних із меню
                (застарілі розділи, попередження): мапи сайту Gatsby-архіви не мають,
                і без явного переліку такі сторінки в корпус не потрапляли.
`gatsby-blog` — блог: перелік — посилання на записи виду /РРРР/ММ/ДД/назва.html
                зі сторінки архіву; поле `before` (РРРР-ММ-ДД) лишає лише записи,
                старші за цю дату, — новіші живуть на іншому сайті й другий раз
                у корпус не потрапляють.

Кожна адреса page-data мусить проходити поле `within` джерела; посилання поза
ним пропускаються, а не завантажуються.
"""

import json
import re
from urllib.parse import urljoin, urlsplit

from engine.readers import Item, _markup, register

_HREF = re.compile(r'href="([^"#?]+\.html)"')
_DATED = re.compile(r"/(\d{4})/(\d{2})/(\d{2})/([^/]+)\.html$")
# Банер «цей сайт архівовано», який legacy-сайт вставляє в тіло кожного запису.
_ARCHIVED = re.compile(r'<div class="scary">.*?</div>', re.S)


def _page_data(url: str) -> str:
    p = urlsplit(url)
    return f"{p.scheme}://{p.netloc}/page-data{p.path}/page-data.json"


def _article(ctx, url: str) -> tuple[str, dict, str]:
    """(назва, frontmatter, текст статті) з page-data сторінки."""
    pd = _page_data(url)
    try:
        remark = json.loads(ctx.text(pd))["result"]["data"]["markdownRemark"]
        title = str(remark["frontmatter"]["title"] or "")
        html = _ARCHIVED.sub("", remark["html"], count=1)
    except (ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f"page-data без статті ({pd}): {exc}")
    return title, remark.get("frontmatter") or {}, _markup.html_body(html)


def _links(source: dict, ctx) -> list[str]:
    urls: list[str] = []
    hrefs = _HREF.findall(ctx.text(source["url"])) + list(source.get("pages", []))
    for href in hrefs:
        url = urljoin(source["url"], href)
        if url not in urls and ctx.allowed(_page_data(url)):
            urls.append(url)
    return urls


@register("gatsby")
def gatsby(source: dict, ctx) -> list[Item]:
    urls = _links(source, ctx)
    if not urls:
        raise SystemExit(f"На сторінці {source['url']} не знайдено посилань на "
                         f"сторінки документації — розмітка змінилася.")
    items = []
    for url in urls:
        name = _markup.slug(urlsplit(url).path.removesuffix(".html"))

        def make(url=url):
            title, _, body = _article(ctx, url)
            _markup.require(title, body, url)
            return _markup.document(title, url, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("gatsby-blog")
def gatsby_blog(source: dict, ctx) -> list[Item]:
    before = source.get("before", "")
    items = []
    for url in _links(source, ctx):
        m = _DATED.search(url)
        if not m:
            continue
        y, mo, d, tail = m.groups()
        day = f"{y}-{mo}-{d}"
        if before and day >= before:
            continue
        name = _markup.slug(f"{day}-{tail}")

        def make(url=url, day=day):
            title, front, body = _article(ctx, url)
            _markup.require(title, body, url)
            authors = ", ".join(
                str((a.get("frontmatter") or {}).get("name", ""))
                for a in (front.get("author") or []) if isinstance(a, dict))
            byline = f"{day}" + (f", by {authors}" if authors else "")
            label = source.get("label", "Blog")
            return _markup.document(f"{label}: {title} ({day})", url, ctx.stamp,
                                    f"{byline}\n\n{body}", source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"На сторінці {source['url']} не знайдено жодного запису "
                         f"блогу — розмітка змінилася, читача треба поправити.")
    return items
