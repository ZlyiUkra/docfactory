"""Читач каталогу функцій supabase.com/features.

`supabase-features` — `url` — sitemap.xml сайту; документом стає кожна адреса з
                      нього всередині поля `within` цього ж джерела
                      (`https://supabase.com/features/`). Текст береться з
                      `<script id="__NEXT_DATA__">` сторінки, поле
                      `props.pageProps.feature`: назва, підзаголовок, опис
                      markdown-ом, продукти, стадія (General Availability, Beta…),
                      чи доступно в self-hosted, адреса гайду.

Навіщо. Каталог функцій — єдине місце, де Supabase одним рядком каже, у якій
стадії функція і чи є вона в self-hosted, і де кожна функція зведена з адресою
свого гайду. Markdown-двійників ці сторінки не мають (`/features.md` — 404), а
чинний `nextdata` шукає вміст у `pageProps.content`, якого тут немає. Сторінка-
перелік `/features` власних даних не несе, тож кожна функція тягнеться окремо.

Чому окремий модуль: інші примірники зібрані й звірені, а правка спільного
читача — ризик зсуву в готовій роботі.
"""

import json
import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.sitemap import _LOC, _inside

_NEXT = re.compile(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
                   re.S)


def _document(html: str, url: str, stamp: str, version: str) -> str:
    m = _NEXT.search(html)
    if not m:
        raise SystemExit(f"На сторінці немає __NEXT_DATA__ ({url}) — документ не записую.")
    try:
        feature = json.loads(m.group(1))["props"]["pageProps"]["feature"]
    except (ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f"__NEXT_DATA__ не має опису функції ({url}): {exc}")
    title = str(feature.get("title") or "").strip()
    lines = []
    if feature.get("subtitle"):
        lines += [str(feature["subtitle"]).strip(), ""]
    status = feature.get("status") or {}
    facts = []
    if feature.get("products"):
        facts.append(f"- Products: {', '.join(map(str, feature['products']))}")
    if status.get("stage"):
        facts.append(f"- Stage: {status['stage']}")
    if "availableOnSelfHosted" in status:
        facts.append(f"- Available on self-hosted: "
                     f"{'yes' if status['availableOnSelfHosted'] else 'no'}")
    if feature.get("docsUrl"):
        facts.append(f"- Documentation: {feature['docsUrl']}")
    lines += facts + ([""] if facts else [])
    lines.append(str(feature.get("description") or ""))
    body = _markup.markdown_body("\n".join(lines))
    _markup.require(title, body, url)
    return _markup.document(f"Feature: {title}", url, stamp, body, version)


@register("supabase-features")
def supabase_features(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач supabase-features вимагає поле `within`.")
    pages: list[str] = []
    for loc in _LOC.findall(ctx.text(source["url"])):
        page = loc.rstrip("/")
        if page not in pages and _inside(page, within) and ctx.allowed(page):
            pages.append(page)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки функції — розмітка змінилася або `within` не той.")
    items = []
    for page in pages:
        name = _markup.slug(urlsplit(page).path)

        def make(page=page):
            return _document(ctx.text(page), page, ctx.stamp, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
