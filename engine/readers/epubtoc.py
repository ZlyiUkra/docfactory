"""Читач книжки EPUB за її змістом (toc.ncx): пункт змісту з власним файлом — документ, пункт з якорем — розділ.

`epub-toc` — `file` — абсолютний шлях EPUB на цій машині; `title` — назва книжки, вона стоїть перед назвою
             кожного документа; `page` — людська адреса книжки для шапки. Необов'язкові: `skip` — вираз назв
             пунктів змісту, що не беруться (обкладинка, зміст, покажчик); `name_prefix` — початок імені
             кожного документа; `version` — мітка версії; `min_chars` — найкоротше тіло.

Навіщо. `epub-local` бере назву глави з першого тегу `<h1>`–`<h3>` у її файлі. Книжка Тарпа «Trade Your
Way to Financial Freedom» (EPUB, перетворений calibre) заголовків-тегів не має зовсім: назва глави й
підзаголовки — це `<div>` з класами на кшталт `heading_sb`, `heading_s9u`, щоразу іншими, тож `epub-local`
не знаходить у ній жодної глави. Зміст `toc.ncx` при цьому повний: кожна глава названа й указує на свій файл,
а кожен розділ — на якір усередині цього файла («part0015.xhtml#a4JU» — «8. Determine What Your Initial 1R
Risk Will Be»). Тому межі й назви беруться зі змісту, а не з розмітки.

Що робить. Пункти змісту йдуть по порядку. Пункт без якоря відкриває документ — увесь його файл. Пункт з
якорем у тому самому файлі стає підзаголовком `## Назва` на місці елемента з цим `id`; сам елемент, якщо
його текст і є назвою, прибирається, щоб назва не стояла двічі. Текст файла розбирає спільний `html_body`.
До мережі читач не звертається: білий список тут — сам шлях, оголошений у `sources.json`.
"""

import posixpath
import re
import zipfile

from engine.readers import Item, _markup, register
from engine.readers.epublocal import _BODY, _ROOTFILE

_SKIP = (r"^(Cover( Page)?|Title Page|Copyright( Page)?|Dedication|Contents|Table of Contents|Index|About the "
         r"Author|A Personal Invitation.*)$")
_NAVPOINT = re.compile(r'<navPoint\b[^>]*>\s*<navLabel>\s*<text>(.*?)</text>\s*</navLabel>\s*'
                       r'<content\s+src="([^"]+)"', re.S)
_NCX_ITEM = re.compile(r'<item\b[^>]*media-type="application/x-dtbncx\+xml"[^>]*>')
_HREF = re.compile(r'href="([^"]+)"')


def _element_at(html: str, anchor: str) -> tuple[int, int, str]:
    """(початок, кінець, текст) елемента з `id="anchor"`; (-1, -1, "") — якщо такого немає."""
    m = re.search(rf'<(\w+)\b[^>]*\bid="{re.escape(anchor)}"[^>]*>', html)
    if not m:
        return -1, -1, ""
    close = html.find(f"</{m.group(1)}>", m.end())
    if close < 0:
        return m.start(), m.end(), ""
    end = close + len(m.group(1)) + 3
    return m.start(), end, _markup.html_body(html[m.end():close]).strip()


@register("epub-toc")
def epub_toc(source: dict, ctx) -> list[Item]:
    path = source.get("file")
    if not path:
        raise SystemExit(f"{source['id']}: читач epub-toc потребує поля file — шляху EPUB.")
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
        item = _NCX_ITEM.search(opf)
        href = _HREF.search(item.group(0)).group(1) if item else ""
        ncx_path = posixpath.normpath(posixpath.join(posixpath.dirname(opf_path), href)) if href else ""
        if not ncx_path or ncx_path not in book.namelist():
            raise SystemExit(f"{source['id']}: у {path} немає змісту toc.ncx.")
        base = posixpath.dirname(ncx_path)
        # Документ — [назва, файл, [(якір, назва розділу)…]] у порядку змісту.
        docs: list[list] = []
        for text, src in _NAVPOINT.findall(book.read(ncx_path).decode("utf-8", "replace")):
            title = " ".join(_markup.html_body(text).split())
            member, _, anchor = src.partition("#")
            member = posixpath.normpath(posixpath.join(base, member))
            if anchor and docs and docs[-1][1] == member:
                docs[-1][2].append((anchor, title))
            elif not anchor:
                docs.append([title, member, []])
        items, names = [], {}
        for title, member, sections in docs:
            if skip.search(title) or member not in book.namelist():
                continue
            html = book.read(member).decode("utf-8", "replace")
            body_match = _BODY.search(html)
            html = body_match.group(1) if body_match else html
            # З кінця до початку: вставка не зсуває позицій ще не оброблених якорів.
            marks = []
            for anchor, sub in sections:
                start, end, text = _element_at(html, anchor)
                if start >= 0:
                    marks.append((start, end, text, sub))
            for start, end, text, sub in sorted(marks, reverse=True):
                same = re.sub(r"\W+", " ", text).strip().lower() == re.sub(r"\W+", " ", sub).strip().lower()
                html = html[:start] + f"<h2>{sub}</h2>" + (html[end:] if same else html[start:])
            body = _markup.html_body(html).strip()
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
        raise SystemExit(f"{source['id']}: зміст {path} не назвав жодної глави з текстом.")
    print(f"  {label}: документів {len(items)}", flush=True)
    return items
