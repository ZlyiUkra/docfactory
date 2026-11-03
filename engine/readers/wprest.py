"""Читачі сайтів на WordPress через їхній власний REST API, і каталогу плагінів wordpress.org.

`wp-rest`        — `url` — перелік записів REST API (…/wp-json/wp/v2/plugin-handbook, можна з
                   умовами в запиті: `?tags=123`); сторінки дочитуються самі, документ — запис,
                   текст — з поля `content.rendered`. `version_from` — вираз над `slug` запису з
                   групами-числами («version-(\\d+)-(\\d+)» → 6.8); `tag_version` і `tags_url` —
                   вираз над іменем мітки та адреса переліку міток: версія запису береться з його
                   міток («dev-notes-6-8» → 6.8); `dated: true` дописує дату до назви.
`wp-rest-html`   — той самий перелік, але лише заради поля `link`: текст береться зі сторінки сайту,
                   поля розбору ті самі, що в `sitemap-html` (`end`, `drop`, `start`, `min_chars`).
                   `identifier_titles: true` робить назвою документа ім'я з сигнатури (`add_action`,
                   `WP_Query::get_posts`, `rest_api_init`), а сигнатура стає першим рядком тексту:
                   заголовок «do_action( 'rest_api_init', … )» не впізнається як назва на запит за іменем.
`wp-plugin-info` — `url` — відповідь каталогу про плагін (api.wordpress.org/plugins/info/1.2/…
                   action=plugin_information): опис, встановлення, запитання, журнал змін, вимоги й
                   перелік усіх випущених версій. Один документ на плагін.

Навіщо. У handbook-ів, статей і нотаток WordPress немає ні markdown-двійників, ні версій на різних
адресах, зате REST API віддає сто записів за один запит: тисячі сторінок приходять за десятки
звернень. Довідник коду (функції, класи, методи, хуки) в REST дає лише назву, бо сигнатуру, параметри
й журнал змін будує сторінка сайту, тому там текст береться зі сторінки.
"""

import hashlib
import json
import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.sitemaphtml import _fields, _items

_PER_PAGE = 100


def _pages(ctx, url: str):
    """Записи всіх сторінок. За останньою сторінкою REST API відповідає помилкою 400."""
    sep = "&" if "?" in url else "?"
    page = 1
    while True:
        try:
            rows = json.loads(ctx.text(f"{url}{sep}per_page={_PER_PAGE}&page={page}"))
        except (SystemExit, Exception):
            if page == 1:
                raise
            return
        if not isinstance(rows, list) or not rows:
            return
        yield from rows
        if len(rows) < _PER_PAGE:
            return
        page += 1


def _name(link: str) -> str:
    return _markup.slug(urlsplit(link).path)


def _distinct(items: list, pages: list, source: dict) -> list:
    """Різні адреси з однаковим іменем файла: `_wp_load` і `wp_load` дають один ключ, і друга сторінка
    мовчки затирала першу. Найкоротша адреса лишає ім'я, решта дістають суфікс із суми адреси."""
    by_name = {}
    for page in pages:
        by_name.setdefault(_name(page), []).append(page)
    keep = {min(group, key=lambda p: (len(p), p)) for group in by_name.values()}
    out = []
    for item, page in zip(items, pages):
        if page not in keep:
            name = f"{_name(page)}-{hashlib.sha1(page.encode()).hexdigest()[:6]}"
            item = Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                        make=item.make)
        out.append(item)
    return out


_HOOK = re.compile(r"^(?:do_action|apply_filters)\w*\(\s*[\u2018'\"]([^\u2019'\"]+)")
_CLASS = re.compile(r"^(?:final |abstract )*(?:class|interface|trait) (\S+)")
_CODE = re.compile(r"^([\w:\\]+)")


def _identified(document: str) -> str:
    """Назва документа довідника — ім'я, а сигнатура переходить у текст."""
    head, _, body = document.partition("\n\n")
    first, _, rest = head.partition("\n")
    signature = first.removeprefix("# ").strip()
    m = _HOOK.match(signature) or _CLASS.match(signature) or _CODE.match(signature)
    if not m:
        return document
    return f"# {m.group(1)}\n{rest}\n\n`{signature}`\n\n{body}"


def _tag_versions(ctx, source: dict) -> dict:
    if not source.get("tag_version"):
        return {}
    pattern = re.compile(source["tag_version"])
    found = {}
    for tag in _pages(ctx, source["tags_url"]):
        m = pattern.fullmatch(tag.get("slug", ""))
        if m:
            found[tag["id"]] = ".".join(m.groups())
    return found


@register("wp-rest")
def wp_rest(source: dict, ctx) -> list[Item]:
    version_from = re.compile(source["version_from"]) if source.get("version_from") else None
    by_tag = _tag_versions(ctx, source)
    min_chars = int(source.get("min_chars", _markup.MIN_BODY))
    items, links = [], []
    for row in _pages(ctx, source["url"]):
        link = row.get("link", "")
        name = _name(link)
        if not link or link in links or not (row.get("content") or {}).get("rendered"):
            continue
        links.append(link)

        def make(row=row, link=link):
            title = _markup.html_body(row["title"]["rendered"]).strip()
            if source.get("dated") and row.get("date"):
                title = f"{title} ({row['date'][:10]})"
            versions = [by_tag[t] for t in row.get("tags") or [] if t in by_tag]
            m = version_from.search(row.get("slug", "")) if version_from else None
            if m:
                versions.append(".".join(m.groups()))
            body = _markup.html_body(row["content"]["rendered"])
            _markup.require(title, body, link, min_chars)
            return _markup.document(title, link, ctx.stamp, body,
                                    ",".join(sorted(set(versions))) or source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    if not items:
        raise SystemExit(f"{source['url']}: REST API не віддав жодного запису з текстом.")
    return _distinct(items, links, source)


@register("wp-rest-html")
def wp_rest_html(source: dict, ctx) -> list[Item]:
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    pages = []
    for row in _pages(ctx, source["url"]):
        link = row.get("link", "")
        if link and ctx.allowed(link) and not any(r.search(link) for r in exclude):
            pages.append(link)
    if not pages:
        raise SystemExit(f"{source['url']}: у переліку немає жодної дозволеної сторінки.")
    items = _distinct(_items(source, ctx, pages, *_fields(source)), pages, source)
    if source.get("identifier_titles"):
        items = [item._replace(make=lambda make=item.make: _identified(make())) for item in items]
    return items


@register("wp-plugin-info")
def wp_plugin_info(source: dict, ctx) -> list[Item]:
    slug = source["slug"]
    page = f"https://wordpress.org/plugins/{slug}/"

    def make():
        info = json.loads(ctx.text(source["url"]))
        facts = [f"- {label}: {info[key]}" for label, key in (
            ("Current version", "version"), ("Requires WordPress", "requires"),
            ("Tested up to", "tested"), ("Requires PHP", "requires_php"),
            ("Active installs", "active_installs"), ("Last updated", "last_updated"),
            ("Homepage", "homepage")) if info.get(key)]
        parts = ["## Facts", "\n".join(facts)]
        for name, html in (info.get("sections") or {}).items():
            if name != "screenshots" and html:
                parts += [f"## {name.capitalize()}", _markup.html_body(html)]
        versions = [v for v in info.get("versions") or {} if v != "trunk"]
        if versions:
            parts += ["## Released versions", ", ".join(versions)]
        title = _markup.html_body(info.get("name", slug)).strip()
        return _markup.document(f"WordPress plugin: {title}", page, ctx.stamp, "\n\n".join(parts))

    return [Item(id=f"{source['id']}/{slug}", file=f"{source['id']}--plugin-{slug}.txt", make=make)]
