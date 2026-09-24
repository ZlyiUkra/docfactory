"""Читачі сайтів, чий повний перелік сторінок лежить лише в sitemap.xml.

`sitemap-md` — `url` — sitemap.xml сайту; документом стає кожна адреса з нього, що
               лежить усередині поля `within` цього ж джерела, а текст береться з
               її markdown-двійника — тієї ж адреси з «.md». Назва — перший
               заголовок сторінки, як у `llms-heading`.
`mdfile`     — один markdown-файл за будь-якою адресою, не обов'язково з «.md»
               (`llms/js.txt`, README з raw.githubusercontent.com). Людська адреса
               для шапки — поле `page`: із самої адреси файла її не вивести.

Навіщо. supabase.com віддає кожну сторінку документації чистим markdown-ом, але
його llms.txt перелічує лише двадцять верхніх сторінок розділів, а не сімсот
глав. Повний перелік є тільки в sitemap.xml. Референс SDK, CLI й API на тому ж
сайті — окремі файли `.txt`, по одному на мову, і `mdpage` їх не прийме: він
чекає адресу з «.md» і назву з шапки YAML, якої там немає.

Чому окремий модуль, а не поля в `llms` чи `mdpage`: інші примірники зібрані й
звірені, а правка спільного читача — ризик зсуву в готовій роботі. Цей модуль
лише реєструє нові імена й перевикористовує помічники, нічого в них не змінюючи.
"""

import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.mdheading import _document

_LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")


def _inside(url: str, within: list) -> bool:
    """Чи лежить адреса всередині `within` саме цього джерела. Загальний білий
    список примірника ширший — він об'єднує всі джерела, — а сайтмап несе адреси
    всіх розділів сайту, тож без цієї межі гайди потягнули б і чужий референс."""
    return any(url.startswith(w) if w.endswith("/") else url == w for w in within)


@register("sitemap-md")
def sitemap_md(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач sitemap-md вимагає поле `within` — "
                         f"інакше сайтмап потягнув би весь сайт.")
    pages: list[str] = []
    for loc in _LOC.findall(ctx.text(source["url"])):
        page = loc.rstrip("/")
        md = page + ".md"
        if page not in pages and _inside(md, within) and ctx.allowed(md):
            pages.append(page)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")
    items = []
    for page in pages:
        name = _markup.slug(urlsplit(page).path)

        def make(page=page):
            return _document(ctx, page + ".md", page, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("mdfile")
def mdfile(source: dict, ctx) -> list[Item]:
    page = source.get("page", "")
    if not page.startswith("https://"):
        raise SystemExit(f"{source['id']}: читач mdfile вимагає поле `page` — людську "
                         f"https-адресу, яку лишити в шапці документа.")
    name = _markup.slug(urlsplit(page).path)

    def make():
        return _document(ctx, source["url"], page, source.get("version", ""))

    return [Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make)]
