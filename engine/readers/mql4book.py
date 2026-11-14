"""Читач книжки MQL4 Tutorial (book.mql4.com), сторінки якої людина зберегла браузером у теку.

`mql4-book-local` — `folder` — абсолютний шлях теки зі збереженими сторінками; ім'я файла — хост і шлях
                    адреси, де `/` замінено на `_` (`book.mql4.com_trading_ordersend.html`, головна —
                    `book.mql4.com.html`); `url` — адреса книжки (`https://book.mql4.com/`), від неї
                    відновлюється адреса кожної сторінки; `contents` — ім'я файла сторінки змісту, з якої
                    береться порядок сторінок; `title` — назва книжки, вона стоїть перед назвою кожного
                    документа. Необов'язкові: `name_prefix` — початок імені кожного документа; `version` —
                    мітка версії; `code_lang` — мова блоків коду; `min_chars` — найкоротше тіло.

Навіщо. Умови mql4.com забороняють заходити на сайт програмами й копіювати вміст, тож завантажувач туди
не ходить: сторінки книжки людина зберігає сама, а читач читає їх з диска без мережі. Білий список тут —
сам шлях теки, оголошений у `sources.json`.

Що робить. Текст сторінки — блок `<div class="book-content">`; меню сайту, бічний перелік розділу й
підвал лишаються поза ним. Порядок сторінок — порядок посилань на сторінці змісту; сторінка теки, на яку
зміст не посилається (головна), іде після них за іменем файла, а сама сторінка змісту документом не стає:
вона лише перелік посилань. Адреса сторінки — з `og:url`, без нього — з імені файла. Першим рядком тіла
стоїть шлях розділів із «хлібних крихт» сторінки («Section: MQL4 Book › Programming of Trade Operations»),
як у читачі `chm-local`. Назва — перший `<h1>` блоку, і з тіла вона прибирається. Дві сторінки `<h1>` не
мають, а починаються з `<h2>`; їхня назва — перша частина `<title>` до « - », а `<h2>` лишається в тілі.

Поправки розмітки сайту. Сайт двічі екранує частину сутностей: у тексті стоїть `&amp;quot;` і
`&amp;lt;`, і без поправки в коді було б `Dist_SL &lt; Min_Dist`, а в тексті — `&quot;EURUSD&quot;`;
тому `&amp;` перед `quot`, `lt`, `gt`, `amp` знімається, доки є що знімати. Підсвітка коду на сайті
розрізала ще й такі сутності на кілька `<span>` (`&amp;` + `amp` + `;`), і сайт сам показує `&amp;&amp;`
замість `&&`; тому сутність, що лишилася в готовому тексті, розкодовується теж. Примітка «зверніть увагу» — таблиця з іконкою й
одним текстом (`<table class="attention">`); без поправки вона стала б рядком таблиці з порожньою
клітинкою, тому лишається абзацом. Абзаци, `<div>` і `<br>` усередині клітинок таблиць стають пробілами: інакше
кожна клітинка розпадалася б на окремі рядки, і рядок таблиці перестав би бути рядком. Посилання «попередня / наступна сторінка» внизу блоку прибирається, а
так само порожні заголовки (`<h2><br></h2>` чи лише з якорем, якими сайт робить відступ): вони дали б
розділи без назви.
"""

import html as _html
import os
import re

from engine.readers import Item, _markup, register

_CONTENT = re.compile(r'<div\b[^>]*class="book-content"[^>]*>', re.I)
_DIV = re.compile(r"<div\b|</div>", re.I)
_H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S | re.I)
_TITLE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
_OG_URL = re.compile(r'<meta property="og:url" content="([^"]+)"', re.I)
_CRUMBS = re.compile(r'<p class="dochead">(.*?)</p>', re.S | re.I)
_HREF = re.compile(r'<a\b[^>]*href="([^"#?]*)[^"]*"', re.I)
_ENTITY = re.compile(r"&amp;(quot|lt|gt|amp);")
_LEFT = re.compile(r"&(?:quot|lt|gt|amp);")
_ATTENTION = re.compile(r'<table class="attention"[^>]*>(.*?)</table>', re.S | re.I)
_TABLE = re.compile(r"<table\b.*?</table>", re.S | re.I)
_CELL_BREAK = re.compile(r"</?(?:p|div)\b[^>]*>|<br\s*/?>", re.I)
_CELL = re.compile(r"<td\b[^>]*>(.*?)</td>", re.S | re.I)
_NAV = re.compile(r'<div[^>]*>\s*<span[^>]*>\s*<img[^>]*tnarrowleft.*?</div>\s*$', re.S | re.I)
_EMPTY_HEAD = re.compile(r"<h([2-6])\b[^>]*>(?:\s|<br\s*/?>|&nbsp;|<a\b[^>]*>\s*</a>)*</h\1>", re.I)
_PRE = re.compile(r"<pre\b[^>]*>", re.I)
_TAG = re.compile(r"<[^>]+>")


def _block(html: str) -> str:
    """Внутрішність `<div class="book-content">` з урахуванням вкладених `<div>`."""
    m = _CONTENT.search(html)
    if not m:
        return ""
    depth = 1
    for d in _DIV.finditer(html, m.end()):
        depth += 1 if d.group(0).lower() == "<div" else -1
        if depth == 0:
            return html[m.end():d.start()]
    return html[m.end():]


def _attention(m: re.Match) -> str:
    """Примітка без таблиці: текст клітинок, крім клітинки з іконкою, одним абзацом."""
    cells = [c for c in _CELL.findall(m.group(1)) if _TAG.sub("", c).strip()]
    return f"<p>{' '.join(cells)}</p>"


def _text(fragment: str) -> str:
    return " ".join(_markup.html_body(_TAG.sub(" ", fragment)).split())


def _file_of(host: str, path: str) -> str:
    path = path.strip("/")
    return f"{host}_{path.replace('/', '_')}.html" if path else f"{host}.html"


@register("mql4-book-local")
def mql4_book_local(source: dict, ctx) -> list[Item]:
    folder = source.get("folder")
    if not folder or not os.path.isdir(folder):
        raise SystemExit(f"{source['id']}: читач mql4-book-local потребує поля folder — теки зі "
                         f"збереженими сторінками; {folder!r} не тека.")
    base = source.get("url", "").rstrip("/") + "/"
    host = re.sub(r"^https?://", "", base).strip("/")
    files = sorted(n for n in os.listdir(folder) if n.lower().endswith(".html"))
    contents = source.get("contents", "")
    if contents not in files:
        raise SystemExit(f"{source['id']}: у {folder} немає сторінки змісту {contents!r}.")
    with open(os.path.join(folder, contents), encoding="utf-8") as fh:
        toc = _block(fh.read())
    order = []
    for href in _HREF.findall(toc):
        name = _file_of(host, re.sub(r"^https?://[^/]+", "", href))
        if name in files and name != contents and name not in order:
            order.append(name)
    order += [n for n in files if n not in order and n != contents]
    label = source.get("title") or source["id"]
    lead = f"{_markup.slug(source.get('name_prefix') or source['id'])}-"
    min_chars = int(source.get("min_chars", 80))
    lang = f' class="language-{source["code_lang"]}"' if source.get("code_lang") else ""
    items = []
    for name in order:
        with open(os.path.join(folder, name), encoding="utf-8") as fh:
            html = fh.read()
        m = _OG_URL.search(html)
        page_url = m.group(1) if m else base + name[len(host):-5].lstrip("_").replace("_", "/")
        part, before = _block(html), ""
        while part != before:
            before, part = part, _ENTITY.sub(r"&\1;", part)
        h1 = _H1.search(part)
        title = _text(h1.group(1)) if h1 else ""
        if h1:
            part = part[:h1.start()] + part[h1.end():]
        else:
            t = _TITLE.search(html)
            title = _text(t.group(1)).split(" - ")[0] if t else ""
        part = _ATTENTION.sub(_attention, part)
        part = _EMPTY_HEAD.sub("", part)
        part = _TABLE.sub(lambda m: _CELL_BREAK.sub(" ", m.group(0)), part)
        part = _NAV.sub("", part.rstrip())
        part = _PRE.sub(f"<pre{lang}>", part)
        body, before = _markup.html_body(part).strip(), ""
        while body != before:
            before, body = body, _LEFT.sub(lambda e: _html.unescape(e.group(0)), body)
        crumbs = _CRUMBS.search(html)
        path = [s for s in (_text(c) for c in re.split(r"<img\b[^>]*>", crumbs.group(1)))
                if s][:-1] if crumbs else []
        if path:
            body = f"Section: {' › '.join(path)}\n\n{body}"
        slug = lead + (_markup.slug(page_url[len(base):]) or "index")

        def make(title=f"{label}: {title}" if title else "", body=body, page_url=page_url):
            _markup.require(title, body, page_url, min_chars)
            return _markup.document(title, page_url, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{slug}", file=f"{source['id']}--{slug}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у {folder} немає жодної сторінки книжки.")
    print(f"  {label}: документів {len(items)}", flush=True)
    return items
