"""Читач довідника API, згенерованого TypeDoc: сторінка на кожну сутність.

`typedoc` — `url` — сторінка-перелік пакетів (modules.html); звідти по посиланнях
            обходяться сторінки пакетів, а з них — сторінки функцій, інтерфейсів,
            типів, змінних і класів. Обхід іде лише адресами з `within` джерела, і
            кожна сторінка тягнеться один раз: HTML, прочитаний при складанні
            переліку, і стає документом.

Навіщо обхід, а не sitemap.xml. У api.reactrouter.com мапа сайту є, але і в /v7/, і
в /v8/ вона перелічує адреси /dev/ — нічних збірок, а не того видання, що лежить
поруч. Узяти її означало б тягнути не ту версію, і білий список цього не пропустив
би. Посилання самих сторінок завжди ведуть у своє видання.

Текст — вміст `col-content` без рядка навігації і заголовка: навігація однакова на
всіх сторінках, а заголовок («Function useNavigate») лягає назвою документа. Рядки
«Defined in packages/…:377» лишаються: це адреса вихідного коду на тому самому
коміті, з якого зібрано довідник, і для звірки цитати вона корисніша за будь-що.
"""

import re
from collections import deque
from html import unescape
from urllib.parse import urljoin, urlsplit

from engine.readers import Item, _markup, register

_HREF = re.compile(r'href="([^"#?]+\.html)(?:#[^"]*)?"')
_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
_CONTENT = re.compile(r'<div class="col-content">(.*?)<div class="col-sidebar"', re.S)
_PAGE_TITLE = re.compile(r'<div class="tsd-page-title">.*?</h1>\s*</div>', re.S)


@register("typedoc")
def typedoc(source: dict, ctx) -> list[Item]:
    start = source["url"]
    base = start.rsplit("/", 1)[0] + "/"
    pages: dict = {}
    queue = deque([start])
    while queue:
        url = queue.popleft()
        if url in pages:
            continue
        html = ctx.text(url)
        pages[url] = html
        for href in _HREF.findall(html):
            nxt = urljoin(url, href)
            if nxt not in pages and nxt.startswith(base) and ctx.allowed(nxt):
                queue.append(nxt)
    items = []
    names: set = set()
    for url, html in pages.items():
        # Перелік пакетів і титульна — зміст сайту, а не довідка; їхній текст
        # повторює назви, що й так є назвами документів.
        if url in (start, base + "index.html"):
            continue
        rel = urlsplit(url).path[len(urlsplit(base).path):].removesuffix(".html")
        name = _markup.slug(rel)
        # Пакет «react-router-dom» і підмодуль «react-router.dom» дають те саме
        # ім'я, і другий файл затер би перший. Тоді ім'я бере крапку з адреси.
        if name in names:
            name = re.sub(r"[^a-z0-9.]+", "-", rel.lower()).strip("-")
        if name in names:
            raise SystemExit(f"{url}: ім'я документа «{name}» уже зайняте іншою "
                             f"сторінкою — один файл затер би другий.")
        names.add(name)

        def make(url=url, html=html):
            m = _CONTENT.search(html)
            if not m:
                raise SystemExit(f"{url}: немає col-content — розмітка TypeDoc змінилася.")
            h1 = _H1.search(m.group(1))
            title = unescape(re.sub(r"<[^>]+>", "", h1.group(1))).strip() if h1 else ""
            body = _markup.html_body(_PAGE_TITLE.sub("", m.group(1), count=1))
            _markup.require(title, body, url, min_chars=1)
            return _markup.document(title, url, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{start}: жодної сторінки довідника в межах {base}.")
    return items
