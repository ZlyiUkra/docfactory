"""Читач книжки EPUB, що лежить у користувача файлом: файл глави — документ.

`epub-local` — `file` — абсолютний шлях EPUB на цій машині; `title` — назва книжки, вона стоїть перед
               назвою кожного документа; `page` — людська адреса книжки для шапки (сторінка видавця).
               Необов'язкові: `skip` — вираз назв глав, що не беруться (зміст, покажчик); `name_prefix`
               — початок імені кожного документа; `version` — мітка версії; `min_chars` — найкоротше
               тіло.

Навіщо. Друге видання «Machine Learning for Algorithmic Trading» Стефана Янсена є в користувача лише
EPUB-ом. EPUB — це ZIP: файл `META-INF/container.xml` називає опис книжки (OPF), а той перелічує
глави XHTML у порядку читання (`spine`). Читач іде цим порядком і кожен файл глави розбирає спільним
`html_body`, як сторінку сайту; назва глави — перший заголовок у ній. До мережі читач не звертається:
білий список тут — сам шлях, оголошений у `sources.json`.
"""

import posixpath
import re
import zipfile

from engine.readers import Item, _markup, register

_SKIP = (r"^(Contents|Table of Contents|Index|Cover|Title Page|Copyright.*|Dedication|Other Books You May "
         r"Enjoy|Contributors|About Packt|Packt.*|Why subscribe\?|Share your thoughts|Leave a review.*)$")
_ROOTFILE = re.compile(r'full-path="([^"]+)"')
_ITEM = re.compile(r"<item\b[^>]*>", re.S)
_ATTR = re.compile(r'(\w[\w-]*)="([^"]*)"')
_ITEMREF = re.compile(r'<itemref\b[^>]*idref="([^"]+)"')
_HEADING = re.compile(r"<h[1-3][^>]*>(.*?)</h[1-3]>", re.S | re.I)
_BODY = re.compile(r"<body\b[^>]*>(.*)</body>", re.S | re.I)


@register("epub-local")
def epub_local(source: dict, ctx) -> list[Item]:
    path = source.get("file")
    if not path:
        raise SystemExit(f"{source['id']}: читач epub-local потребує поля file — шляху EPUB.")
    label = source.get("title") or source["id"]
    skip = re.compile(source.get("skip") or _SKIP, re.I)
    lead = f"{_markup.slug(source.get('name_prefix') or source['id'])}-"
    min_chars = int(source.get("min_chars", 200))
    page_url = source.get("page", "")
    try:
        book = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        raise SystemExit(f"{source['id']}: не відкрив {path}: {exc}")
    with book:
        root = _ROOTFILE.search(book.read("META-INF/container.xml").decode("utf-8", "replace"))
        if not root:
            raise SystemExit(f"{source['id']}: у {path} немає опису книжки (OPF).")
        opf_path = root.group(1)
        opf = book.read(opf_path).decode("utf-8", "replace")
        base = posixpath.dirname(opf_path)
        manifest = {}
        for tag in _ITEM.findall(opf):
            attrs = dict(_ATTR.findall(tag))
            if attrs.get("id") and attrs.get("href"):
                manifest[attrs["id"]] = posixpath.normpath(posixpath.join(base, attrs["href"]))
        items, names = [], {}
        for idref in _ITEMREF.findall(opf):
            member = manifest.get(idref)
            if not member or not member.endswith((".xhtml", ".html", ".htm")):
                continue
            html = book.read(member).decode("utf-8", "replace")
            head = _HEADING.search(html)
            title = _markup.html_body(head.group(1)).strip() if head else ""
            # Packt ставить номер глави окремим заголовком («<h1>11</h1>»), а назву — наступним.
            if head and re.fullmatch(r"\d+", title):
                second = _HEADING.search(html, head.end())
                if second:
                    title = f"{title} {_markup.html_body(second.group(1)).strip()}"
                    html = html[:second.start()] + html[second.end():]
            if not title or skip.search(title):
                continue
            body_match = _BODY.search(html)
            body_html = body_match.group(1) if body_match else html
            if head and head.start() > (body_match.start(1) if body_match else 0):
                body_html = body_html.replace(head.group(0), "", 1)
            body = _markup.html_body(body_html).strip()
            if len(body) < min_chars:
                continue
            slug = lead + _markup.slug(title)
            names[slug] = names.get(slug, 0) + 1
            if names[slug] > 1:
                slug = f"{slug}-{names[slug]}"
            full = f"{label}: {title}"

            def make(full=full, body=body):
                _markup.require(full, body, page_url, min_chars)
                return _markup.document(full, page_url, ctx.stamp, body, source.get("version", ""))

            items.append(Item(id=f"{source['id']}/{slug}", file=f"{source['id']}--{slug}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у {path} не знайдено жодної глави з текстом.")
    print(f"  {label}: документів {len(items)}", flush=True)
    return items
