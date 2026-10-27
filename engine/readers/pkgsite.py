"""Читач довідника пакетів Go з pkg.go.dev: кореневий пакет і його підпакети.

`pkgsite` — `url` — сторінка кореневого пакета на pkg.go.dev (без версії в адресі, тобто
            остання версія модуля). Документом стає сам пакет і кожен підпакет із розділу
            «Directories» його сторінки, чия адреса проходить поле `within`; `exclude` — вирази
            адрес, що не беруться (internal-пакети, допоміжні пакети тестів); `pages` —
            сторінки пакетів поза деревом кореня, без їхніх підпакетів (`pkg/buffer`, на якому
            стоять пакети мережевого стека). Обов'язкове `within`. `pause` — секунд між
            зверненнями до pkg.go.dev (типово 1.5): сайт пригальмовує частих клієнтів
            відповіддю 429, а пауза примірника для GitHub — нуль.

Навіщо. Netstack — мережевий стек gVisor (`gvisor.dev/gvisor/pkg/tcpip` і підпакети `stack`,
`header`, `link/…`, `network/…`, `transport/…`, `adapters/gonet`) — бібліотека, яку беруть і
поза gVisor, а її документація існує лише як коментарі коду, що їх показує pkg.go.dev. Сторінка
пакета там і є довідником: опис пакета, константи, змінні, функції, типи з конструкторами й
методами — з оголошенням кожного.

Документ — один пакет, назва «package <шлях імпорту>», версія — версія модуля, яку показує
сторінка (у gVisor це псевдоверсія гілки `go`: `0.0.0-<час>-<коміт>`; «v» знято, як у решті
корпусу). Розділи — як на сторінці: «Overview», «Constants», «Variables», «Functions»
(`### func Ім'я`, під ним оголошення блоком коду Go і опис), «Types» (`### type T` з
оголошенням і описом, конструктори й методи — підрозділами `#### func …`). Приклади стають
підписом «Example …:» з кодом і виводом усередині розділу своєї функції чи типу: окремим
розділом приклад відривався б від того, що він показує. Зміст сторінки (Index), кнопки,
«View Source» і перелік файлів — не текст документації й випадають.

Адреси підпакетів у «Directories» записано з версією (`/gvisor.dev/gvisor@v0.0.0-…/pkg/…`);
тут версія з адреси знімається, і підпакет береться з тієї самої адреси останньої версії, що
й корінь: так `within` лишається одним префіксом, а посилання у відповіді не старіє з кожним
днем.

Поле `versions` — об'єкт «мітка версії на pkg.go.dev → версія», від найновішої
(`{"go1.27.3": "1.27.3", …, "go1.0.3": "1.0.3"}`): дерево кореня береться на кожній мітці
(`std@go1.27.3`), і версія в адресах підпакетів лишається — це і є знімок тієї версії. `within`
і `exclude` перевіряють адресу без версії. Сторінка кореня без розділу документації (`std` —
перелік пакетів, а не пакет) документом не стає. Однаковий текст пакета на кількох мітках — один
документ з усіма їхніми версіями, а ім'я файла закінчується хешем тексту (`-<8 hex>`), як у
`ghdocs-history`: з `revision_suffix` незмінний розділ кількох редакцій — один фрагмент. Тому
текст читається вже під час переліку; рядка «Module version …» у ньому немає — версії стоять у
шапці документа. Без поля — усе, як було.

Навіщо. Стандартна бібліотека Go за 28 мінорних версій додавала функції й типи (`slices`,
`maps`, `iter`, `log/slog`) і міняла описи: питання «як це було в 1.18» потребує тексту 1.18, а
не позначки «added in go1.21» на сторінці останньої версії.
"""

import hashlib
import html as html_lib
import re
import time
from urllib.parse import unquote, urljoin, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.sitemap import _inside

_DIRS = re.compile(r'data-test-id="UnitDirectories-table"(.*?)</table>', re.S)
_HREF = re.compile(r'href="(/[^"#?]+)"')
_AT_VERSION = re.compile(r"@[^/]+")
_DEPSDEV = re.compile(r'href="https://deps\.dev/go/[^/"]+/([^"/]+)"')
_SHORT_VERSION = re.compile(r'data-test-id="UnitHeader-version">.*?Version:\s*</span>\s*([^<\s]+)',
                            re.S)
_PUBLISHED = re.compile(r'data-test-id="UnitHeader-commitTime">\s*Published:\s*([^<]+?)\s*<')
_KIND = re.compile(r'data-test-id="UnitHeader-title">[^<]*</h1>\s*'
                   r'<span class="go-Chip go-Chip--inverted">([^<]+)</span>')
_START = '<div class="Documentation-content js-docContent">'
_STOPS = ('<div class="UnitFiles', "<footer")

_INDEX = re.compile(r'<section class="Documentation-(?:index|examples)">.*?</section>', re.S)
_SOURCE_LINK = re.compile(r'<span class="Documentation-declarationLink">.*?</span>', re.S)
_BUTTONS = re.compile(r'<div class="Documentation-exampleButtonsContainer">.*?</div>', re.S)
_ANCHOR = re.compile(r'<a\b[^>]*>\s*¶\s*</a>')
_SINCE = re.compile(r'<span class="Documentation-sinceVersion">(.*?)</span>\s*\Z', re.S)
_SECTION_HEAD = re.compile(r'<h3\b[^>]*class="Documentation-\w+Header"[^>]*>(.*?)</h3>', re.S)
_MEMBER_HEAD = re.compile(r'<h4\b[^>]*class="Documentation-(function|type|typeFunc|typeMethod)'
                          r'Header"[^>]*>(.*?)</h4>', re.S)
_DOC_HEAD = re.compile(r'<h[3-6]\b[^>]*id="hdr-[^"]*"[^>]*>(.*?)</h[3-6]>', re.S)
_OVERVIEW = re.compile(r'(<section class="Documentation-overview">)(.*?)(</section>)', re.S)
_DECL_PRE = re.compile(r'(<div class="Documentation-declaration">\s*)<pre>')
_EXAMPLE_PRE = re.compile(r'<pre class="Documentation-exampleCode">\n?')
_OUTPUT_PRE = re.compile(r'<pre class="Documentation-exampleOutputContainer[^"]*">\s*'
                         r'<span class="Documentation-exampleOutputLabel">([^<]*)</span>\s*')
_EXAMPLE_HEAD = re.compile(r'<summary class="Documentation-exampleDetailsHeader">(.*?)</summary>',
                           re.S)
_EMPTY = re.compile(r"^## [^\n]+\n\nThis section is empty\.\n*", re.M)
# Тег, що лишився всередині заголовка після зняття якоря: посилання на код, span.
_TAGS = re.compile(r"<[^>]+>")


def _plain(fragment: str) -> str:
    """Текст фрагмента HTML одним рядком: заголовок члена «func (*Stack) AddAddress»."""
    return " ".join(html_lib.unescape(_TAGS.sub(" ", fragment)).split())


def _member(m) -> str:
    """Заголовок функції, типу, конструктора чи методу → h3/h4 з самим «func (T) Ім'я».
    Позначка «added in go1.21» (у стандартній бібліотеці; у gVisor порожня) стає рядком під
    заголовком, а не частиною назви: інакше ключ розділу мінявся б разом із нею."""
    level = "h3" if m.group(1) in ("function", "type") else "h4"
    head = m.group(2)
    since = _SINCE.search(head)
    label = _plain(head[:since.start()] if since else head)
    added = _plain(since.group(1)) if since else ""
    return f"<{level}>{label}</{level}>" + (f"<p>({added})</p>" if added else "")


def _body(doc: str) -> str:
    """Розділ документації сторінки → HTML, який `_markup.html_body` перетворить на
    заголовки «## / ### / ####», блоки коду й абзаци."""
    doc = _INDEX.sub("", doc)
    doc = _SOURCE_LINK.sub("", doc)
    doc = _BUTTONS.sub("", doc)
    doc = _ANCHOR.sub("", doc)
    # Заголовки всередині опису пакета (`# Heading` у коментарі) — підрозділи «Overview»;
    # такий самий заголовок в описі функції чи типу стає підписом, щоб не розривати розділ.
    doc = _OVERVIEW.sub(lambda m: m.group(1) + _DOC_HEAD.sub(r"<h3>\1</h3>", m.group(2))
                        + m.group(3), doc)
    doc = _DOC_HEAD.sub(r"<p><strong>\1</strong></p>", doc)
    doc = _SECTION_HEAD.sub(lambda m: f"<h2>{_plain(m.group(1))}</h2>", doc)
    doc = _MEMBER_HEAD.sub(_member, doc)
    doc = _DECL_PRE.sub(r'\1<pre class="language-go">', doc)
    doc = _EXAMPLE_PRE.sub('<pre class="language-go">', doc)
    doc = _OUTPUT_PRE.sub(lambda m: f"<p>{m.group(1)}</p><pre>", doc)
    doc = _EXAMPLE_HEAD.sub(lambda m: f"<p>{_plain(m.group(1))}:</p>", doc)
    # Порожній розділ сторінка підписує «This section is empty.»: фрагмент із самого підпису
    # нічого не каже, а в пакеті з одним типом таких було б три з п'яти.
    return _EMPTY.sub("", _markup.html_body(doc)).strip("\n")


def _parts(html: str, url: str, versions: str = "") -> tuple[str, str, str]:
    """(назва, тіло, версія) сторінки пакета. `versions` — версії документа з поля
    `versions` джерела: тоді рядка «Module version …» у тілі немає, і тіло однакове на всіх
    мітках, де пакет не мінявся."""
    path = _AT_VERSION.sub("", urlsplit(url).path, count=1).strip("/")
    m = _DEPSDEV.search(html) or _SHORT_VERSION.search(html)
    version = unquote(m.group(1)).lstrip("v") if m else ""
    start = html.find(_START)
    if start < 0:
        raise SystemExit(f"На сторінці {url} немає розділу документації — документ не записую.")
    start += len(_START)
    stop = min((i for i in (html.find(s, start) for s in _STOPS) if i >= 0), default=len(html))
    kind = _KIND.search(html)
    published = _PUBLISHED.search(html)
    lead = [f"Import path: `{path}`."]
    if kind and kind.group(1).strip() != "package":
        lead.append(f"Kind: {kind.group(1).strip()}.")
    if version and not versions:
        lead.append(f"Module version {version}"
                    + (f", published {published.group(1)}." if published else "."))
    body = "\n\n".join([" ".join(lead), _body(html[start:stop])])
    return f"package {path}", body, versions or version


def _document(html: str, url: str, stamp: str, versions: str = "") -> str:
    title, body, version = _parts(html, url, versions)
    _markup.require(title, body, url)
    return _markup.document(title, url, stamp, body, version)


def _versioned(source: dict, ctx, root: str, within: list, exclude: list, fetch) -> list[Item]:
    """Поле `versions`: знімок дерева пакетів на кожній мітці, однакові тексти — один документ."""
    versions = source["versions"]
    if not isinstance(versions, dict) or not versions:
        raise SystemExit(f"{source['id']}: поле versions — об'єкт «мітка → версія».")
    # ім'я документа → [адреса найновішої мітки, [мітки]]; від найновішої, як оголошено
    seen: dict = {}
    for tag in versions:
        top = f"{root}@{tag}"
        if not ctx.allowed(top):
            raise SystemExit(f"{source['id']}: адреса {top} поза білим списком.")
        html = fetch(top)
        pages = [top] if _START in html else []
        table = _DIRS.search(html)
        for href in _HREF.findall(table.group(1) if table else ""):
            url = urljoin(top, href).rstrip("/")
            bare = _AT_VERSION.sub("", url, count=1)
            if (url not in pages and _inside(bare, within) and ctx.allowed(url)
                    and not any(r.search(bare) for r in exclude)):
                pages.append(url)
        for url in pages:
            # Одна сторінка без документації чи з відповіддю 404 серед тисяч не мусить зупиняти перелік
            # усіх 28 версій: її пропущено вголос, решта береться.
            try:
                page = html if url == top else fetch(url)
                _, body, _ = _parts(page, url, versions[tag])
            except SystemExit as exc:
                print(f"  пропущено: {exc}", flush=True)
                continue
            digest = hashlib.sha1(body.encode("utf-8")).hexdigest()[:8]
            path = _AT_VERSION.sub("", urlsplit(url).path, count=1)
            seen.setdefault(f"{_markup.slug(path)}-{digest}", [url, []])[1].append(tag)
    items = []
    for name, (url, tags) in seen.items():
        version = ", ".join(dict.fromkeys(versions[t] for t in tags))

        # Сторінку вже прочитано під час переліку: у тому самому прогоні ctx.text бере її зі
        # сховища, тож пауза pkg.go.dev тут не потрібна.
        def make(url=url, version=version):
            return _document(ctx.text(url), url, ctx.stamp, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("pkgsite")
def pkgsite(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач pkgsite вимагає поле `within` — інакше "
                         f"«Directories» повели б на будь-який пакет модуля.")
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    pause = float(source.get("pause", 1.5))
    last = [0.0]

    def fetch(url: str) -> str:
        # Пауза — лише коли буде мережа: крок build читає сховище, і чекати там нема чого.
        if not getattr(ctx, "offline", False):
            gap = last[0] + pause - time.monotonic()
            if gap > 0:
                time.sleep(gap)
        try:
            return ctx.text(url)
        finally:
            last[0] = time.monotonic()

    root = source["url"].rstrip("/")
    if "versions" in source:
        return _versioned(source, ctx, root, within, exclude, fetch)
    if not ctx.allowed(root):
        raise SystemExit(f"{source['id']}: адреса {root} поза білим списком.")
    cache = {root: fetch(root)}
    pages = [root]
    table = _DIRS.search(cache[root])
    for href in _HREF.findall(table.group(1) if table else ""):
        url = urljoin(root, _AT_VERSION.sub("", href, count=1)).rstrip("/")
        if (url not in pages and _inside(url, within) and ctx.allowed(url)
                and not any(r.search(url) for r in exclude)):
            pages.append(url)
    for page in source.get("pages") or ():
        url = page.rstrip("/")
        if not ctx.allowed(url):
            raise SystemExit(f"{source['id']}: адреса {url} поза білим списком — "
                             f"допишіть її в `within`.")
        if url not in pages:
            pages.append(url)

    items = []
    for url in pages:
        name = _markup.slug(urlsplit(url).path)

        def make(url=url):
            html = cache.pop(url, None) or fetch(url)
            return _document(html, url, ctx.stamp)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
