"""Читач MDN Web Docs: перелік сторінок — з мапи сайту, текст — з `index.json` кожної сторінки.

`mdn-json` — `url` — мапа сайту developer.mozilla.org (`sitemap.xml.gz`; стиснена gzip чи
             ні — байдуже). `section` — розділ документації, шлях після `/docs/`
             («Web/API», «Glossary»): документом стає сторінка самого розділу й кожна
             сторінка під ним. `exclude` — вирази шляхів, що не беруться. Поле `within`
             обов'язкове: адреси `index.json` мусять лежати всередині нього.

Навіщо. Сирий markdown MDN (репозиторій mdn/content) тримає текст у макросах KumaScript
(`{{domxref("Event")}}`, `{{Compat}}`, `{{CSSSyntax}}`), а частину сторінки — формальний
синтаксис і визначення властивості CSS, підсумок підтримки браузерами — макроси генерують з
окремих даних лише під час збирання сайту. Зібрана сторінка віддається ще й як `index.json`:
тіло, поділене на розділи з готовим HTML, плюс специфікації й підсумок Baseline окремими
полями. Це рівно те, що бачить читач сайту, і в рази легше за HTML сторінки з меню.

Що лягає в документ. Розділи прози — як є, з рівнем заголовка з JSON; навігація уроків Learn
(«Previous / Overview / Next») і підпис мови над блоком коду вирізаються, а мова переходить
в огорожу «```js». Розділ «Specifications» — назва й адреса кожної специфікації: адреса тут і
є вміст, за нею звіряються. Розділ «Browser compatibility» на сайті — таблиця, яку браузер
дотягує окремо з browser-compat-data; у JSON від неї лише ключ даних. Замість таблиці сюди
лягає підсумок Baseline тієї ж сторінки: статус, дати й перша версія кожного з основних
браузерів, а браузер, якого в підсумку немає, названо явно. Що повної таблиці по кожному
методу в тексті немає, сказано в ньому самому — інакше відсутність рядка читалася б як
відсутність підтримки.

Ім'я документа — шлях усередині розділу. `*` у шляху стає `-star`: `function*` і `function` —
різні сторінки, а `_markup.slug` звів би обидві до одного імені. Два шляхи з одним іменем —
відмова всього джерела, а не тихе перезаписування одного документа іншим.

Мапа сайту одна на всі розділи, тож вона читається раз за прогін, а не раз на джерело.
"""

import gzip
import json
import re

from engine.readers import Item, _markup, register
from engine.readers.sitemap import _LOC

_DOCS = "https://developer.mozilla.org/en-US/docs/"
_SITEMAPS: dict[str, list[str]] = {}

_PREV_NEXT = re.compile(r'<ul class="prev-next">.*?</ul>', re.S)
_EXAMPLE_HEADER = re.compile(r'<div class="example-header">.*?</div>', re.S)
_BRUSH = re.compile(r'<pre class="brush:\s*([\w+#]+)(?:-nolint)?[^"]*"')

# Порядок і назви — як у підсумку Baseline на самому сайті.
_BROWSERS = (
    ("chrome", "Chrome"), ("chrome_android", "Chrome Android"), ("edge", "Edge"),
    ("firefox", "Firefox"), ("firefox_android", "Firefox for Android"),
    ("safari", "Safari"), ("safari_ios", "Safari on iOS"),
)


def _locs(ctx, url: str) -> list[str]:
    if url not in _SITEMAPS:
        data = ctx.bytes(url)
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        _SITEMAPS[url] = _LOC.findall(data.decode("utf-8", errors="replace"))
    return _SITEMAPS[url]


def _plain(html: str) -> str:
    return " ".join(_markup.html_body(html).split())


def _prose(html: str) -> str:
    html = _PREV_NEXT.sub("", html)
    html = _EXAMPLE_HEADER.sub("", html)
    html = _BRUSH.sub(lambda m: f'<pre class="language-{m.group(1)}"', html)
    return _markup.html_body(html)


def _specs(specs: list) -> str:
    if not specs:
        return "This feature does not appear to be defined in any specification."
    return "\n".join(f"- {' '.join((s.get('title') or '').split())}: "
                     f"{s.get('bcdSpecificationURL') or ''}".rstrip(": ") for s in specs)


def _compat(base, keys: list) -> str:
    lines = []
    if isinstance(base, dict):
        feature = base.get("feature") or {}
        level = base.get("baseline")
        low = base.get("baseline_low_date") or ""
        high = base.get("baseline_high_date") or ""
        discouraged = feature.get("discouraged")
        if discouraged:
            reason = _plain(discouraged.get("reason_html") or "")
            lines.append("Discouraged: this feature is not recommended for use."
                         + (f" Reason: {reason}" if reason else ""))
        elif level == "high":
            lines.append(f"Baseline: widely available. This feature is well established and "
                         f"works across many devices and browser versions. It has been "
                         f"available across browsers since {low} and widely available "
                         f"since {high}.")
        elif level == "low":
            year = (re.search(r"\d{4}", low) or [""])[0]
            lines.append(f"Baseline {year}: newly available. Since {low} this feature works "
                         f"across the latest devices and browser versions. It might not "
                         f"work in older devices or browsers.")
        else:
            lines.append("Limited availability: this feature is not Baseline, because it "
                         "does not work in some of the most widely-used browsers.")
        support = base.get("support") or {}
        have = [f"{name} {support[k]}" for k, name in _BROWSERS if support.get(k)]
        miss = [name for k, name in _BROWSERS if not support.get(k)]
        if have:
            lines.append("Supported since: " + ", ".join(have) + ".")
        if miss:
            lines.append("No support recorded in: " + ", ".join(miss) + ".")
        if base.get("asterisk"):
            lines.append("Some parts of this feature may have varying levels of support.")
        alts = [f"{a.get('name')} ({_DOCS[:-1]}{(a.get('mdn_url') or '')[5:]}): "
                f"{a.get('description') or ''}".rstrip(": ")
                for a in base.get("alternatives") or ()]
        if alts:
            lines.append("Alternatives:\n" + "\n".join(f"- {a}" for a in alts))
        if feature.get("name"):
            lines.append(f"Web feature: {feature['name']}.")
    else:
        lines.append("This page carries no Baseline summary of browser support.")
    if keys:
        lines.append("The detailed per-browser table is not part of this text; its data in "
                     "browser-compat-data: " + ", ".join(f"`{k}`" for k in keys) + ".")
    return "\n\n".join(lines)


def _document(raw: str, page: str, stamp: str) -> str:
    try:
        doc = json.loads(raw)["doc"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit(f"Замість сторінки MDN прийшло щось інше ({page}) — документ не "
                         f"записую.")
    title = " ".join((doc.get("title") or "").split())
    keys = list(doc.get("browserCompat") or ())
    parts, compat = [], False
    for block in doc.get("body") or ():
        kind, value = block.get("type"), block.get("value") or {}
        head = " ".join((value.get("title") or "").split())
        if kind == "specifications":
            text = _specs(value.get("specifications") or [])
        elif kind == "browser_compatibility":
            text = _compat(doc.get("baseline"), [value["query"]] if value.get("query")
                           else keys)
            compat = True
        else:
            text = _prose(value.get("content") or "")
        mark = "### " if value.get("isH3") else "## "
        parts.append((f"{mark}{head}\n\n" if head else "") + text)
    if not compat and doc.get("baseline"):
        parts.append("## Browser compatibility\n\n" + _compat(doc["baseline"], keys))
    body = _markup.tidy("\n\n".join(p for p in parts if p.strip()), strip=False)
    _markup.require(title, body, page)
    return _markup.document(title, page, stamp, body)


@register("mdn-json")
def mdn_json(source: dict, ctx) -> list[Item]:
    section = (source.get("section") or "").strip("/")
    if not section or not source.get("within"):
        raise SystemExit(f"{source['id']}: читач mdn-json вимагає поля `section` і `within` — "
                         f"інакше мапа сайту потягнула б увесь MDN.")
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    items: list[Item] = []
    seen: dict[str, str] = {}
    for loc in _locs(ctx, source["url"]):
        if not loc.startswith(_DOCS):
            continue
        path = loc[len(_DOCS):].rstrip("/")
        if path != section and not path.startswith(section + "/"):
            continue
        if any(r.search(path) for r in exclude):
            continue
        page = _DOCS + path
        if not ctx.allowed(page + "/index.json"):
            raise SystemExit(f"{source['id']}: {page}/index.json поза білим списком — "
                             f"допишіть розділ у `within`.")
        name = _markup.slug(path[len(section):].replace("*", "-star"))
        if name in seen:
            if seen[name] == path:
                continue
            raise SystemExit(f"{source['id']}: дві сторінки дають одне ім'я «{name}»: "
                             f"{seen[name]} і {path}.")
        seen[name] = path

        def make(page=page):
            return _document(ctx.text(page + "/index.json"), page, ctx.stamp)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"У мапі сайту {source['url']} немає жодної сторінки розділу "
                         f"«{section}» — розмітка змінилася або розділ перейменовано.")
    return items
