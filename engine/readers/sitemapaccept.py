"""Читач сайту, що віддає markdown сторінки лише на заголовок Accept, а не за адресою з «.md».

`sitemap-accept` — `url` — sitemap.xml сайту; документом стає кожна адреса з нього, що лежить
                   усередині поля `within` цього ж джерела. Сторінка береться за своєю ж адресою
                   із заголовком `accept` (типово `text/markdown`). `match` — вирази, з яких
                   адреса мусить збігтися хоч з одним; `exclude` — вирази адрес, що не беруться.
                   Назва — поле `title` шапки YAML; `title_strip` — вираз, що з неї вирізається
                   (назва сайту в кінці: «Arrow link | Motion UI components»). `drop` — вирази
                   (рядок або пара [вираз, заміна]), що вирізаються з тексту до розбору:
                   навігація, рекламні вставки, перелік схожих сторінок, JSON-LD.
                   `lead_meta` — поле шапки YAML (`description`), що стає першим абзацом:
                   у закритого прикладу Motion+ це весь його опис. `date_jsonld: true` — дата
                   `datePublished` з блоку JSON-LD сторінки йде в назву в дужках, як у блогах
                   інших примірників: для статті й прикладу це відповідь на «коли з'явилося».
                   `version` — версія всіх документів джерела.

Навіщо. motion.dev віддає документацію (`/docs/…`) двійником із «.md» — її бере `sitemap-md`.
Приклади, сторінки Motion UI, журнал помилок (`/troubleshooting/…`), журнал змін і статті
magazine двійника з «.md» не мають (404), але ту саму сторінку сервер віддає markdown-ом, коли
запит просить `Accept: text/markdown`. HTML тих самих сторінок — це оболонка застосунку з
меню, і текст із нього гірший, ніж markdown, який сайт готує сам.

У markdown цих сторінок сайт лишає службові вставки: «Skip to example», банер «Unlock all
490+ examples» над закритим кодом прикладів Motion+, список схожих прикладів з картинками і
блок JSON-LD для пошуковиків. Вони однакові на сотнях сторінок і без `drop` стали б
фрагментами, що відгукуються на будь-який запит про Motion+.

Чому окремий модуль, а не поле в `sitemap-md`: інші примірники зібрані й звірені, а правка
спільного читача — ризик зсуву в готовій роботі. Модуль лише реєструє нове ім'я й
перевикористовує помічники.
"""

import html
import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.sitemap import _LOC, _inside


def _drops(source: dict) -> list:
    """Пари (скомпільований вираз, заміна). Вирази — з прапорцями M і S: вставка займає
    кілька рядків і прив'язується до їхніх початків."""
    out = []
    for entry in source.get("drop") or []:
        pattern, repl = (entry, "") if isinstance(entry, str) else (entry[0], entry[1])
        out.append((re.compile(pattern, re.M | re.S), repl))
    return out


_PUBLISHED = re.compile(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})')


def _page(ctx, source: dict, page: str, drops: list, strip) -> str:
    text = ctx.text(page, accept=source.get("accept") or "text/markdown")
    _markup.refuse_html(text, page)
    meta, rest = _markup.front_matter(text.replace("\r\n", "\n"))
    title = html.unescape(meta.get("title", "")).strip().strip('"')
    if strip:
        title = strip.sub("", title).strip()
    if not title:
        raise SystemExit(f"{page}: у шапці YAML немає title — розмітка сайту змінилася.")
    if source.get("date_jsonld") is True:
        # Дата — до вирізання: блок JSON-LD сам іде під `drop`.
        day = _PUBLISHED.search(rest)
        if day:
            title = f"{title} ({day.group(1)})"
    for pattern, repl in drops:
        rest = pattern.sub(repl, rest)
    lead = html.unescape(str(meta.get(source.get("lead_meta") or "", "") or "")).strip().strip('"')
    if lead:
        rest = f"{lead}\n\n{rest}"
    body = _markup.markdown_body(rest)
    _markup.require(title, body, page, min_chars=1)
    return _markup.document(title, page, ctx.stamp, body, source.get("version", ""))


@register("sitemap-accept")
def sitemap_accept(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач sitemap-accept вимагає поле `within` — "
                         f"інакше сайтмап потягнув би весь сайт.")
    match = [re.compile(p) for p in source.get("match") or []]
    exclude = [re.compile(p) for p in source.get("exclude") or []]
    strip = re.compile(source["title_strip"]) if source.get("title_strip") else None
    drops = _drops(source)
    pages: list[str] = []
    for loc in _LOC.findall(ctx.text(source["url"])):
        page = loc.rstrip("/")
        if (page in pages or not _inside(page, within) or not ctx.allowed(page)
                or (match and not any(m.search(page) for m in match))
                or any(x.search(page) for x in exclude)):
            continue
        pages.append(page)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")
    items = []
    for page in pages:
        name = _markup.slug(urlsplit(page).path)

        def make(page=page):
            return _page(ctx, source, page, drops, strip)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
