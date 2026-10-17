"""Читач сторінок із sitemap.xml, де адреси записано шляхами без хоста.

`sitemap-html-rel` — те саме, що `sitemap-html` (поля `within`, `match`, `exclude`, `end`,
                     `drop`, `start`, `doc_title`, `min_chars`, `inline_titles`, `version`),
                     але кожен `<loc>` спершу стає повною адресою відносно самого sitemap.xml,
                     і завершальна коса риска лишається, як її записав сайт.

Навіщо. Сайт gvisor.dev зібрано Jekyll без `site.url`, і його sitemap.xml пише
`<loc>/blog/2023/06/27/directfs/</loc>` — шлях, а не адресу. `sitemap-html` порівнює `<loc>`
з `within` як рядок, тож жодна сторінка такого сайтмапа не проходила, і джерело падало б
як «жодної дозволеної сторінки». Головна сторінка ще й мусить лишитися з рискою:
«https://gvisor.dev» без шляху білий список не впізнає як сторінку теки сайту.

Чому окремий модуль, а не поле в `sitemap-html`: інші примірники з тим читачем зібрані й
звірені, а правка спільного читача — ризик зсуву в готовій роботі. Розбір сторінки той
самий — його й викликано.
"""

import re
from urllib.parse import urljoin

from engine.readers import Item, register
from engine.readers.sitemap import _LOC, _inside
from engine.readers.sitemaphtml import _fields, _items


@register("sitemap-html-rel")
def sitemap_html_rel(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач sitemap-html-rel вимагає поле `within` — "
                         f"інакше сайтмап потягнув би весь сайт.")
    match = re.compile(source["match"]) if source.get("match") else None
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    ends, drops, start_at = _fields(source)
    pages: list[str] = []
    for loc in _LOC.findall(ctx.text(source["url"])):
        page = urljoin(source["url"], loc)
        if (page not in pages and _inside(page, within) and ctx.allowed(page)
                and (not match or match.search(page))
                and not any(r.search(page) for r in exclude)):
            pages.append(page)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")
    return _items(source, ctx, pages, ends, drops, start_at)
