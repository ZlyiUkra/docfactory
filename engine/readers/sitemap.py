"""Читачі сайтів, чий повний перелік сторінок лежить лише в sitemap.xml.

`sitemap-md` — `url` — sitemap.xml сайту; документом стає кожна адреса з нього, що
               лежить усередині поля `within` цього ж джерела, а текст береться з
               її markdown-двійника — тієї ж адреси з «.md». Назва — перший
               заголовок сторінки, як у `llms-heading`.
`mdlinks`    — те саме, що `sitemap-md`, але перелік — посилання з markdown-сторінки
               `url`: supabase.com/docs/guides/troubleshooting.md перелічує 218 статей,
               а сайтмап — лише 51.
`mdfile`     — один markdown-файл за будь-якою адресою, не обов'язково з «.md»
               (`llms/js.txt`, README з raw.githubusercontent.com). Людська адреса
               для шапки — поле `page`: із самої адреси файла її не вивести.

Поля `sitemap-md` і `mdlinks`: `title_from: "meta"` бере назву з шапки YAML, а не з
першого заголовка; `label` ставить префікс назви й дату з шапки («Blog: … (2025-08-12)»).
Без цих полів документ той самий, що дає `llms-heading`.

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
from engine.readers.mdheading import _document, _split_title
from engine.readers.mdsite import _SITEMAP

_LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")
_LINK = re.compile(r"\]\((https://[^)\s#?]+)[^)]*\)")


def _meta_title(text: str, simple: str) -> str:
    """Назва з шапки YAML. `_markup.front_matter` читає лише «ключ: значення» в
    один рядок, а кейси supabase.com пишуть довгу назву складеним рядком
    («title: >-» і продовження з відступом нижче) — тоді назвою ставав би «>-»."""
    if simple not in (">", ">-", "|", "|-"):
        return simple
    lines = text.replace("\r\n", "\n").split("\n")
    for i, line in enumerate(lines):
        if line.startswith("title:"):
            tail = []
            for nxt in lines[i + 1:]:
                if not nxt[:1].isspace():
                    break
                tail.append(nxt.strip())
            return " ".join(t for t in tail if t)
    return ""


def _page(ctx, source: dict, md_url: str, page: str) -> str:
    """Документ однієї сторінки. Без полів `title_from` і `label` — рівно
    `mdheading._document`: назва з першого заголовка.

    `title_from: "meta"` — назва з шапки YAML. Блог і кейси несуть назву лише там,
    а тіло починають одразу з «## Вступ», і перший заголовок назвою був би хибною.
    `label` — префікс назви («Blog: …»), а дата з шапки йде в дужках: для запису
    блогу чи журналу змін дата — половина відповіді на «коли це з'явилося»."""
    version = source.get("version", "")
    if source.get("title_from") != "meta" and not source.get("label"):
        return _document(ctx, md_url, page, version)
    text = ctx.text(md_url)
    _markup.refuse_html(text, md_url)
    meta, rest = _markup.front_matter(text)
    title = (_meta_title(text, meta.get("title", ""))
             if source.get("title_from") == "meta" else "")
    if title:
        # Той самий заголовок ще й першим рядком тіла — прибрати, щоб не дублювався.
        first, without = _split_title(rest)
        if first.strip() == title.strip():
            rest = without
    else:
        title, rest = _split_title(rest)
    body = _markup.markdown_body(rest)
    _markup.require(title, body, md_url, min_chars=1)
    if source.get("label"):
        day = (meta.get("date") or meta.get("published") or "")[:10]
        title = f"{source['label']}: {title}" + (f" ({day})" if day else "")
    return _markup.document(title, page, ctx.stamp, body, version)


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
            return _page(ctx, source, page + ".md", page)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("mdlinks")
def mdlinks(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач mdlinks вимагає поле `within`.")
    pages: list[str] = []
    for link in _LINK.findall(ctx.text(source["url"])):
        page = link.rstrip("/")
        md = page + ".md"
        if page not in pages and _inside(md, within) and ctx.allowed(md):
            pages.append(page)
    if not pages:
        raise SystemExit(f"На сторінці {source['url']} не знайдено жодного дозволеного "
                         f"посилання — розмітка змінилася або `within` не той.")
    items = []
    for page in pages:
        name = _markup.slug(urlsplit(page).path)

        def make(page=page):
            return _page(ctx, source, page + ".md", page)

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
        url, version = source["url"], source.get("version", "")
        text = ctx.text(url)
        _markup.refuse_html(text, url)
        meta, rest = _markup.front_matter(text)
        if not meta.get("title"):
            # Без назви в шапці — рівно те, що робить _document, лише без другого
            # завантаження того самого файла.
            title, rest = _split_title(_SITEMAP.sub("\n", rest))
        else:
            # Запис блогу tanstack.com тримає назву в шапці YAML, а текст починає
            # картинкою чи одразу підрозділом: з першого заголовка назвою ставав
            # «How to install», а сам підрозділ зникав із тексту.
            title = meta["title"]
        body = _markup.markdown_body(rest)
        _markup.require(title, body, url, min_chars=1)
        return _markup.document(title, page, ctx.stamp, body, version)

    return [Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make)]
