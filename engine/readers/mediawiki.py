"""Читач сторінок MediaWiki (wiki.documentfoundation.org) — готовий HTML змісту через `action=render`.

`mediawiki-render` — `url` — корінь вікі («https://wiki.documentfoundation.org/»), `pages` — назви
                     сторінок («ReleaseNotes/26.8», «Documentation/DevGuide/First_Steps»).
                     Необов'язкові: `version_from` — вираз з однією групою над назвою сторінки, що
                     дає версію документа (`^ReleaseNotes/(.+)$`); `start` — вираз, з якого
                     починається текст (усе раніше — шаблони навігації); `title_prefix` — рядок
                     перед назвою документа.

Навіщо. Вікі пише сторінки вікірозміткою з шаблонами (`{{Menu|…}}`, навігація версій, таблиці
мов), і розгорнути їх може лише сама MediaWiki. `?action=render` віддає вже розгорнутий HTML лише
змісту — без меню сайту, бічної панелі й посилань «edit» у заголовках. Нагорі змісту лишаються
шаблони навігації (рядок версій release notes, «Other languages»): їх відрізає `start`.
"""

import re
from urllib.parse import quote

from engine.readers import Item, _markup, register

_FIGURE_DUP = re.compile(r"<figcaption\b.*?</figcaption>", re.S)


@register("mediawiki-render")
def mediawiki_render(source: dict, ctx) -> list[Item]:
    base = source["url"].rstrip("/") + "/"
    pages = list(source.get("pages") or ())
    if not pages:
        raise SystemExit(f"{source['id']}: поле `pages` — назви сторінок вікі.")
    version_rx = re.compile(source["version_from"]) if source.get("version_from") else None
    start = re.compile(source["start"]) if source.get("start") else None
    prefix = source.get("title_prefix", "")

    items = []
    for page in pages:
        url = f"{base}{quote(page)}?action=render"
        if not ctx.allowed(url):
            continue
        cite = f"{base}{quote(page)}"
        m = version_rx.search(page) if version_rx else None
        version = m.group(1) if m else ""
        title = f"{prefix}{page.rsplit('/', 1)[-1].replace('_', ' ')}"
        name = _markup.slug(page)

        def make(url=url, cite=cite, version=version, title=title):
            html = ctx.text(url)
            if start:
                hit = start.search(html)
                if hit:
                    html = html[hit.start():]
            # Підпис картинки MediaWiki повторює її alt — у тексті він виходив двічі поспіль.
            body = _markup.html_body(_FIGURE_DUP.sub("", html))
            _markup.require(title, body, url)
            return _markup.document(title, cite, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("html-details")
def html_details(source: dict, ctx) -> list[Item]:
    """`html-details` — одна сторінка, де кожен запис — `<details><summary>назва</summary>…</details>`
    (бюлетені безпеки libreoffice.org: CVE на запис). `url`, `title`, необов'язкові `begin` і `end` —
    вирази меж змісту. Кожен `<summary>` стає заголовком розділу `###`, тож запис ділиться окремо,
    а групи `<h2>` («Addressed in LibreOffice 26.2.5/26.8.0») лишаються розділами над ними."""
    url = source["url"]
    begin = re.compile(source.get("begin") or r"</h1>")
    end = re.compile(source.get("end") or r"<footer\b")

    def make():
        html = ctx.text(url)
        b = begin.search(html)
        html = html[b.end():] if b else html
        e = end.search(html)
        html = html[: e.start()] if e else html
        html = re.sub(r"<summary\b[^>]*>(.*?)</summary>", r"<h3>\1</h3>", html, flags=re.S)
        html = re.sub(r"</?details\b[^>]*>", "", html)
        body = _markup.html_body(html)
        _markup.require(source["title"], body, url)
        return _markup.document(source["title"], url, ctx.stamp, body)

    return [Item(id=f"{source['id']}/{_markup.slug(url.split('//', 1)[-1])}",
                 file=f"{source['id']}--{_markup.slug(url.split('//', 1)[-1])}.txt", make=make)]
