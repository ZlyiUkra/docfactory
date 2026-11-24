"""Читач сайту з markdown на заголовок Accept, де назва сторінки — не в шапці YAML, а в першому «# …».
`sitemap-accept-heading` — ті самі поля, що й у `sitemap-accept` (`url`, `within`, `match`,
                           `exclude`, `drop`, `accept`, `version`). Назва — поле `title` шапки
                           YAML, а якщо його немає — перший заголовок «# …» до першої огорожі
                           коду; цей рядок з тексту прибирається. `date_published: true` —
                           дата з рядка «**Published:** July 29, 2026» іде в назву в дужках
                           («… (2026-07-29)»), як дата JSON-LD у `sitemap-accept`.
                           `md_suffix` — рядок, що дописується до адреси сторінки («.md»):
                           тоді markdown береться за цією адресою, а не на заголовок Accept.
Навіщо. vercel.com віддає markdown кожної сторінки на `Accept: text/markdown`, але шапку YAML
з полем `title` мають лише документація (`/docs/…`) і уроки Academy. Статті довідки
(`/kb/…`), записи журналу змін і блогу починаються одразу з «# Назва», а шапка, якщо є, несе
лише підказки для агентів («search_vercel_guides: …»). `sitemap-accept` на таких сторінках
зупиняє прогін: назви в шапці немає. Дата публікації запису журналу змін стоїть рядком під
назвою; у назві документа вона відповідає на «коли це з'явилося» вже у видачі пошуку.
Сторінки кодів помилок (`/docs/errors/…`) на `Accept: text/markdown` віддають HTML, а markdown —
лише за адресою з «.md»; для них і є `md_suffix`.
Чому окремий модуль, а не поле в `sitemap-accept`: інші примірники з тим читачем зібрані й
звірені, а правка спільного читача — ризик зсуву в готовій роботі. Модуль лише реєструє нове
ім'я й перевикористовує помічники.
"""
import html
import re
from datetime import datetime
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.mdheading import _split_title
from engine.readers.sitemap import _LOC, _inside
from engine.readers.sitemapaccept import _drops

_PUBLISHED = re.compile(r"\*\*Published:\*\*\s*([A-Z][a-z]+ \d{1,2}, \d{4})")


def _day(text: str) -> str:
    """«July 29, 2026» → «2026-07-29»; порожньо, якщо рядка немає чи дата не розібралася."""
    m = _PUBLISHED.search(text)
    if not m:
        return ""
    try:
        return datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return ""


def _page(ctx, source: dict, page: str, drops: list) -> str:
    if source.get("md_suffix"):
        text = ctx.text(page + source["md_suffix"])
    else:
        text = ctx.text(page, accept=source.get("accept") or "text/markdown")
    _markup.refuse_html(text, page)
    meta, rest = _markup.front_matter(text.replace("\r\n", "\n"))
    title = html.unescape(meta.get("title", "")).strip().strip('"')
    day = _day(rest) if source.get("date_published") is True else ""
    for pattern, repl in drops:
        rest = pattern.sub(repl, rest)
    if not title:
        title, rest = _split_title(rest)
        title = html.unescape(title).strip()
    if title and day:
        title = f"{title} ({day})"
    body = _markup.markdown_body(rest)
    _markup.require(title, body, page, min_chars=1)
    return _markup.document(title, page, ctx.stamp, body, source.get("version", ""))


@register("sitemap-accept-heading")
def sitemap_accept_heading(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач sitemap-accept-heading вимагає поле `within` — "
                         f"інакше сайтмап потягнув би весь сайт.")
    match = [re.compile(p) for p in source.get("match") or []]
    exclude = [re.compile(p) for p in source.get("exclude") or []]
    drops = _drops(source)
    pages: list[str] = []
    seen = set()
    for loc in _LOC.findall(ctx.text(source["url"])):
        page = loc.rstrip("/")
        if (page in seen or not _inside(page, within) or not ctx.allowed(page)
                or (match and not any(m.search(page) for m in match))
                or any(x.search(page) for x in exclude)):
            continue
        seen.add(page)
        pages.append(page)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")
    items = []
    for page in pages:
        name = _markup.slug(urlsplit(page).path) or "index"

        def make(page=page):
            return _page(ctx, source, page, drops)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
