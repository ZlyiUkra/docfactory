"""Читачі сайтів, що віддають сторінки markdown-ом за тією самою адресою з «.md».

`llms`   — перелік сторінок у форматі llms.txt: посилання на `.md` кожної
           сторінки документації; кожна стає документом.
`mdblog` — сторінка-перелік блогу (HTML): з неї беруться адреси записів виду
           …/РРРР/ММ/ДД/назва, а текст кожного запису — з тієї ж адреси з «.md».
`mdpage` — одна сторінка: `url` — її адреса з «.md». З `keep_links: true`
           посилання лишаються в тексті адресами — для сторінки-мапи, де
           посилання і є змістом.

Адреса в шапці документа — людська сторінка, без «.md»: саме її відкриває той,
хто звіряє цитату. Тягнуться лише адреси, які дозволяє поле `within` джерела;
посилання поза ним у переліку пропускаються, а не завантажуються.
"""

import re
from urllib.parse import urljoin, urlsplit

from engine.readers import Item, _markup, register

_MD_LINK = re.compile(r"\((https://[^)\s]+\.md)\)")
_HREF = re.compile(r'href="([^"#?]+)"')
_DATED = re.compile(r"/(\d{4})/(\d{2})/(\d{2})/([^/]+)$")
# Кожна markdown-сторінка react.dev закінчується тим самим посиланням на мапу сайту.
# У корпусі це двісті фрагментів «Overview of all docs pages» без жодного змісту, і
# злитися в один вони не можуть: лежать у різних документах.
_SITEMAP = re.compile(r"\n-{3,}[ \t]*\n+## Sitemap[ \t]*\n+"
                      r"\[Overview of all docs pages\]\([^)\n]*\)\s*\Z")


def _md_document(ctx, md_url: str, page: str, version: str, prefix: str = "",
                 keep_links: bool = False) -> str:
    text = ctx.text(md_url)
    _markup.refuse_html(text, md_url)
    meta, rest = _markup.front_matter(text)
    rest = _SITEMAP.sub("\n", rest)
    body = _markup.markdown_body(rest, page if keep_links else None)
    title = _markup.title_of(meta, page) if meta else ""
    _markup.require(title, body, md_url)
    if prefix:
        day = meta.get("date", "").replace("/", "-")
        title = f"{prefix}: {title}" + (f" ({day})" if day else "")
    return _markup.document(title, page, ctx.stamp, body, version)


@register("llms")
def llms(source: dict, ctx) -> list[Item]:
    links: list[str] = []
    for url in _MD_LINK.findall(ctx.text(source["url"])):
        if url not in links and ctx.allowed(url):
            links.append(url)
    if not links:
        raise SystemExit(f"У переліку {source['url']} не знайдено жодної дозволеної "
                         f"сторінки .md — розмітка змінилася або `within` не той.")
    items = []
    for url in links:
        page = url[:-3]
        name = _markup.slug(urlsplit(page).path)

        def make(url=url, page=page):
            return _md_document(ctx, url, page, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("mdblog")
def mdblog(source: dict, ctx) -> list[Item]:
    base = source["url"].rstrip("/")
    posts: list[str] = []
    for href in _HREF.findall(ctx.text(source["url"])):
        url = urljoin(base + "/", href)
        if (url.startswith(base + "/") and _DATED.search(url) and url not in posts
                and ctx.allowed(url + ".md")):
            posts.append(url)
    if not posts:
        raise SystemExit(f"На сторінці {source['url']} не знайдено жодного запису "
                         f"блогу — розмітка змінилася, читача треба поправити.")
    items = []
    for url in posts:
        y, m, d, tail = _DATED.search(url).groups()
        name = _markup.slug(f"{y}-{m}-{d}-{tail}")

        def make(url=url):
            return _md_document(ctx, url + ".md", url, source.get("version", ""),
                                prefix=source.get("label", "Blog"))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("mdpage")
def mdpage(source: dict, ctx) -> list[Item]:
    url = source["url"]
    if not url.endswith(".md"):
        raise SystemExit(f"{url}: читач mdpage чекає адресу сторінки з «.md».")
    page = url[:-3]
    name = _markup.slug(urlsplit(page).path)

    def make():
        return _md_document(ctx, url, page, source.get("version", ""),
                            keep_links=source.get("keep_links") is True)

    return [Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make)]
