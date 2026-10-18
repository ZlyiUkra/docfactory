"""Читач сторінки-змісту в markdown, чиї посилання ведуть на `.md` інших сторінок.

`md-index` — `url` — сторінка-зміст з «.md» (`…/docs/en/api/python.md`); кожне посилання
             на `.md` у ній — абсолютне, від кореня сайту (`/docs/en/api/python/messages.md`)
             чи відносне — береться від адреси змісту і стає документом, якщо його дозволяє
             `within`. Сам зміст документом не стає: у ньому лише посилання.

Навіщо. Довідник API platform.claude.com має окрему редакцію для кожної мови SDK (Python,
TypeScript…): ті самі ендпоінти з назвами методів і типами цієї мови. У llms.txt і sitemap.xml
їх немає — лише сторінка-зміст кожної мови, де пункти вкладені (відступ) і заголовки теж є
посиланнями. Читач `llms` бере або абсолютні адреси, або відносні пункти верхнього рівня, тож
вкладені й кореневі він пропустив би; міняти його поведінку для зібраних примірників — ризик
зсуву, тож це окремий модуль. Текст сторінки готує той самий `_md_document`, що й у `llms`.
"""

import re
from urllib.parse import urljoin, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.mdsite import _md_document

_LINK = re.compile(r"\]\(([^)\s#?]+\.md)\)")


@register("md-index")
def md_index(source: dict, ctx) -> list[Item]:
    links: list[str] = []
    for href in _LINK.findall(ctx.text(source["url"])):
        url = urljoin(source["url"], href)
        if url != source["url"] and url not in links and ctx.allowed(url):
            links.append(url)
    if not links:
        raise SystemExit(f"У змісті {source['url']} не знайдено жодної дозволеної "
                         f"сторінки .md — розмітка змінилася або `within` не той.")
    items = []
    for url in links:
        page = url[:-3]
        name = _markup.slug(urlsplit(page).path)

        def make(url=url, page=page):
            return _md_document(ctx, url, page, source.get("version", ""),
                                source.get("title_prefix", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
