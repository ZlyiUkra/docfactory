"""Читачі сайтів Angular, яких не беруть наявні: angular.dev, v2.angular.io і документація AngularJS.

`adev-html`      — сайт angular.dev (і vNN.angular.dev): сторінки зібрані заздалегідь, повний текст
                   лежить у HTML. `url` — корінь сайту, `index` — сторінки, з яких починається обхід
                   (`https://angular.dev/api`, `…/cli`), `match` — вираз шляху сторінки, що береться
                   (`^/(api|cli)(/|$)`); посилання зі сторінок, що збіглися, обходяться далі, доки
                   нових не лишиться. `exclude` — вирази адрес, що не беруться; `version` — версія
                   всіх документів джерела.
`ng2-site`       — сайт v2.angular.io (Angular 2.x). `url` — корінь документації
                   (`https://v2.angular.io/docs/ts/latest/`), `index` — сторінки-змісти, посилання з
                   яких (усередині `url`, файли `.html`) стають документами, `api_list` — адреса
                   `api-list.json` довідника API; `version`.
`angularjs-docs` — документація AngularJS 1.x на code.angularjs.org. `url` — тека документації однієї
                   версії (`https://code.angularjs.org/1.8.3/docs/`), `version`. Перелік сторінок —
                   `js/pages-data.js` (1.2 і новіші) чи `docs-keywords.js` (1.0), текст — готові
                   шматки HTML `partials/<сторінка>.html`, які застосунок документації вставляє в
                   сторінку. `exclude` — вирази шляхів сторінок, що не беруться.

Навіщо. Посібники Angular лежать у репозиторії markdown-ом (їх бере `ghdocs-history` з полем
`ng_docs`), а довідник API і CLI — ні: його генерує збирання сайту з коду. На angular.dev
готові сторінки є лише в HTML, мапа сайту є не в кожній версії (v18 і v19 її не мають), а
сторінка-зміст `/api` перелічує не все, що є на сайті: обхід посилань від змісту знаходить і
решту. Сайти v4–v17 віддають ті самі сторінки JSON-ом — їх бере `aio-json`.

v2.angular.io — інший генератор (Harp): статичні сторінки, назва посібника — у «шапці-герої»
`<h1 class="hero-title">`, на сторінках API там стоїть просто «Angular», тож назва береться з
`api-list.json`. Приклади коду — `<code-example language="ts">` з екранованим текстом.

code.angularjs.org — односторінковий застосунок AngularJS: HTML сторінки — порожня оболонка,
текст лежить окремими шматками. Шлях сторінки 1.0 записаний як `api/ng.directive:ngModel`,
1.2+ — `api/ng/directive/ngModel`; ім'я документа — slug шляху, і обидва записи дають одне
«api-ng-directive-ngmodel», тож редакції різних версій сходяться в одну сторінку.

Чому окремий модуль: інші примірники зібрані й звірені, а правка спільного читача — ризик
зсуву в готовій роботі.
"""

import json
import re
from html import unescape
from urllib.parse import urljoin, urlsplit

from engine.readers import Item, _markup, register

_HREF = re.compile(r'href="([^"#?]*)')
_H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S)
_SCRIPTS = re.compile(r"<(style|script|svg)\b[^>]*>.*?</\1\s*>", re.S | re.I)
_NG_ATTRS = re.compile(r' (?:_ngcontent|_nghost)-[\w-]+(?:="")?| ngh="\d+"')
# «@param», ім'я параметра й тип стоять сусідніми <span> без пробілу: без нього «@paramoptions».
# «Value Type`string`Default`true`»: підпис і значення — сусідні елементи без пробілу.
_GLUE = re.compile(r"</(span|code)><(code|span)\b")
_PARAM_WORD = re.compile(r'<span class="docs-param-(?:keyword|name)">(.*?)</span>', re.S)
# Службове angular.dev: зміст сторінки, «View source», значки, кнопки копіювання.
_ADEV_DROP = [re.compile(p, re.S) for p in (
    r"<docs-table-of-contents\b.*?</docs-table-of-contents>",
    r"<a class=\"docs-github-links\".*?</a>",
    r"<docs-icon\b.*?</docs-icon>",
    r"<i\b[^>]*material-symbols[^>]*>.*?</i>",
    r"<button\b.*?</button>",
    r"<docs-breadcrumb\b.*?</docs-breadcrumb>",
)]
_ADEV_CATEGORY = re.compile(r'<span class="docs-reference-category">(.*?)</span>', re.S)
_ADEV_LABEL = re.compile(r'<div class="docs-api-item-label[^"]*"[^>]*>(.*?)</div>', re.S)
_STATE = re.compile(r'<script id="ng-state" type="application/json">(.*?)</script>', re.S)
_DATA_TAB = re.compile(r'<div data-tab="([^"]+)"[^>]*>')
_LINE_SPAN = re.compile(r'</span>(?=<span class="line")')


def _state_body(html: str) -> str:
    """Шматок HTML статті з кешу передачі стану (`<script id="ng-state">`): застосунок, зібраний
    заздалегідь, кладе туди відповідь, з якої намалював сторінку. У v18–v19 довідник API —
    вкладки «API / Description / Usage Notes», і в готовому HTML намальована лише перша; повний
    текст усіх вкладок є тільки тут. Без кешу — порожній рядок."""
    m = _STATE.search(html)
    if not m:
        return ""
    try:
        state = json.loads(m.group(1))
    except ValueError:
        return ""
    bodies = [v["b"] for v in state.values()
              if isinstance(v, dict) and isinstance(v.get("b"), str) and "<h1" in v["b"]]
    return max(bodies, key=len, default="")


def _adev_text(html: str, url: str, stamp: str, version: str) -> str:
    part = _state_body(html)
    if not part:
        # v20+ кладе статтю в <main>, v18–v19 — у <adev-reference-page>/<docs-viewer> без <main>.
        found = [i for i in (html.find(t) for t in ("<main", "<adev-reference-page",
                                                     "<docs-viewer")) if i >= 0]
        if not found:
            raise SystemExit(f"На сторінці немає статті ({url}) — документ не записую.")
        start = min(found)
        stop = min((i for i in (html.find("</main>", start), html.find("<footer", start))
                    if i > 0), default=len(html))
        part = html[start:stop]
    part = _NG_ATTRS.sub("", _SCRIPTS.sub("", part))
    # Вкладка стає розділом: інакше «Usage Notes» v18 лишалися б текстом розділу «API».
    part = _DATA_TAB.sub(lambda t: f"<h2>{t.group(1)}</h2>{t.group(0)}", part)
    part = _GLUE.sub(r"</\1> <\2", _PARAM_WORD.sub(r"\1 ", part))
    for r in _ADEV_DROP:
        part = r.sub("", part)
    m = _H1.search(part)
    if not m:
        raise SystemExit(f"На сторінці немає <h1> ({url}) — документ не записую.")
    title = _markup.html_body(m.group(1)).strip()
    head = []
    cat = _ADEV_CATEGORY.search(part)
    if cat:
        head.append(f"Entry point: `{_markup.html_body(cat.group(1)).strip()}`")
    label = _ADEV_LABEL.search(part)
    if label:
        head.append(f"API kind: {_markup.html_body(label.group(1)).strip()}")
    part = _ADEV_LABEL.sub("", _ADEV_CATEGORY.sub("", part[:m.start()] + part[m.end():]))
    body = _markup.html_body(_LINE_SPAN.sub("</span>\n", part)).strip()
    if head:
        body = "\n\n".join(["  \n".join(head), body])
    _markup.require(title, body, url, min_chars=40)
    return _markup.document(title, url, stamp, body, version)


def _page_key(url: str, root: str) -> str:
    return urlsplit(url).path[len(urlsplit(root).path):].strip("/")


@register("adev-html")
def adev_html(source: dict, ctx) -> list[Item]:
    root = source["url"].rstrip("/") + "/"
    host = urlsplit(root).netloc
    match = re.compile(source.get("match") or r"^/(api|cli)(/|$)")
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    version = str(source.get("version", ""))
    queue = [u.rstrip("/") for u in source.get("index") or [root + "api", root + "cli"]]
    seen, pages = set(queue), []
    while queue:
        page = queue.pop(0)
        if not ctx.allowed(page):
            continue
        try:
            html = ctx.text(page)
        except SystemExit as exc:
            print(f"  {page}: {exc}", flush=True)
            continue
        if match.search(urlsplit(page).path):
            pages.append(page)
        for href in _HREF.findall(html):
            # Сайт стоїть на <base href="/">: відносне посилання («cli/generate») — від кореня.
            link = urljoin(root, href).rstrip("/")
            if (urlsplit(link).netloc == host and link not in seen
                    and match.search(urlsplit(link).path)
                    and not any(r.search(link) for r in exclude)):
                seen.add(link)
                queue.append(link)
    if not pages:
        raise SystemExit(f"{source['id']}: обхід від {queue or source.get('index')} не дав жодної "
                         f"сторінки — розмітка змінилася або `match` не той.")
    items = []
    for page in pages:
        name = _markup.slug(_page_key(page, root))

        def make(page=page):
            return _adev_text(ctx.text(page), page, ctx.stamp, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items


_HERO = re.compile(r'<h1 class="hero-title[^"]*">(.*?)</h1>', re.S)
_NG2_CODE = re.compile(r'<code-(?:example|pane)\b([^>]*)>(.*?)</code-(?:example|pane)>', re.S)
_NG2_LANG = re.compile(r'language="([\w+#-]+)"')
_NG2_HEAD = re.compile(r'(?:title|name)="([^"]+)"')


def _ng2_code(m) -> str:
    lang = _NG2_LANG.search(m.group(1))
    head = _NG2_HEAD.search(m.group(1))
    caption = f"<p>{head.group(1)}:</p>" if head else ""
    cls = f' class="language-{lang.group(1)}"' if lang else ""
    return f"{caption}<pre{cls}><code>{m.group(2)}</code></pre>"


def _ng2_text(html: str, url: str, stamp: str, version: str, title: str) -> str:
    hero = _HERO.search(html)
    start = hero.end() if hero else html.find("<article")
    if start < 0:
        raise SystemExit(f"На сторінці немає статті ({url}) — документ не записую.")
    if not title:
        title = _markup.html_body(hero.group(1)).strip() if hero else ""
    stop = html.find("</article>", start)
    part = _SCRIPTS.sub("", html[start:stop if stop > 0 else len(html)])
    part = _NG2_CODE.sub(_ng2_code, part)
    part = re.sub(r"</?code-tabs\b[^>]*>", "", part)
    body = _markup.html_body(part).strip()
    _markup.require(title, body, url, min_chars=40)
    return _markup.document(title, url, stamp, body, version)


@register("ng2-site")
def ng2_site(source: dict, ctx) -> list[Item]:
    root = source["url"].rstrip("/") + "/"
    version = str(source.get("version", ""))
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    pages: dict = {}
    for index in source.get("index") or [root]:
        for href in _HREF.findall(ctx.text(index)):
            link = urljoin(index, href)
            if (link.startswith(root) and link.endswith(".html") and "/api/" not in link
                    and link not in pages and ctx.allowed(link)
                    and not any(r.search(link) for r in exclude)):
                pages[link] = ""
    if source.get("api_list"):
        listing = json.loads(ctx.text(source["api_list"]))
        for barrel, entries in listing.items():
            for e in entries:
                link = urljoin(root + "api/", e["path"])
                if ctx.allowed(link) and not any(r.search(link) for r in exclude):
                    pages[link] = f"{e['title']} ({barrel})"
    if not pages:
        raise SystemExit(f"{source['id']}: у змістах жодної сторінки — розмітка змінилася.")
    items = []
    for page, title in pages.items():
        name = _markup.slug(re.sub(r"\.html$", "", page[len(root):]))

        def make(page=page, title=title):
            return _ng2_text(ctx.text(page), page, ctx.stamp, version, title)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items


_NG_PATH = re.compile(r'"path":\s*"([^"]+)"')
_NG_KEYWORD = re.compile(r'\{"section":"([^"]+)","id":"([^"]+)"')
_AJS_DROP = [re.compile(p, re.S) for p in (
    r"<a\b[^>]*class=['\"][^'\"]*(?:improve-docs|view-source)[^'\"]*['\"][^>]*>.*?</a>",
    r'<span class="hint">.*?</span>',
)]


def _ajs_text(html: str, url: str, stamp: str, version: str) -> str:
    for r in _AJS_DROP[:1]:
        html = r.sub("", html)
    # Шапка API 1.2+: «<li>- directive in module ng</li>» — тире вже є маркером пункту.
    html = re.sub(r"(<li>\s*)-\s+", r"\1", html)
    m = _H1.search(html)
    if not m:
        raise SystemExit(f"У шматку сторінки немає <h1> ({url}) — документ не записую.")
    hint = re.search(r'<span class="hint">\((.*?)\)</span>', m.group(1), re.S)
    title = _markup.html_body(_AJS_DROP[1].sub("", m.group(1))).replace("`", "").strip()
    body = _markup.html_body(html[m.end():]).strip()
    if hint:
        body = f"{_markup.html_body(hint.group(1)).strip()}\n\n{body}"
    _markup.require(title, body, url, min_chars=20)
    return _markup.document(title, url, stamp, body, version)


@register("angularjs-docs")
def angularjs_docs(source: dict, ctx) -> list[Item]:
    root = source["url"].rstrip("/") + "/"
    version = str(source.get("version", ""))
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    code, data = ctx.fetch(root + "js/pages-data.js")
    text = data.decode("utf-8", errors="replace") if code == "200" else ""
    if "NG_PAGES" in text:
        paths = _NG_PATH.findall(text)
    else:
        text = ctx.text(root + "docs-keywords.js")
        paths = [f"{s}/{i}" for s, i in _NG_KEYWORD.findall(text)]
    paths = [p for p in dict.fromkeys(paths) if not any(r.search(p) for r in exclude)]
    if not paths:
        raise SystemExit(f"{source['id']}: у переліку сторінок нічого — розмітка змінилася.")
    items = []
    for path in paths:
        partial = root + "partials/" + path + ".html"
        if not ctx.allowed(partial):
            continue
        name = "angularjs-" + _markup.slug(path)

        def make(partial=partial, cite=root + path):
            return _ajs_text(ctx.text(partial), cite, ctx.stamp, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items
