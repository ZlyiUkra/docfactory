"""Читач сторінок, чия шапка YAML — частина змісту: дата запису блогу, посилання шаблону.

`sitemap-md-meta` — те саме, що `sitemap-md` з `title_from: "meta"`: перелік сторінок — із
                    sitemap.xml у межах поля `within`, текст — markdown-двійник сторінки (та
                    сама адреса з «.md»), назва — з шапки. Необов'язкові поля:
                    `label` — префікс назви («Blog: …», «Template: …»);
                    `date`  — поле шапки з датою: вона йде в дужках після назви;
                    `lead`  — поля шапки, що стають першими рядками тіла («Repository: …»);
                              вкладене поле пишеться через крапку (`links.repository`);
                    `end`   — вирази, на яких тіло закінчується (хвіст, спільний для всіх
                              сторінок сайту).

Навіщо. `sitemap-md` бере з шапки лише назву й дату з полів `date` чи `published`. Блог
nextjs.org пише дату в `publishedAt` («October 21st 2025»), і без неї запис «Next.js 13» не
відповідає на питання «коли це вийшло». Сторінка шаблону на vercel.com найкорисніше тримає
саме в шапці: `links.repository` — де лежить код шаблону, `links.demo` — де він працює; у тілі
цих адрес немає. А закінчується кожна з трьохсот таких сторінок однаковим блоком «Related
Templates» і «Additional documentation», який у пошуку лише відбирав би місця.

Шапка тут розбирається на один рівень вкладення («links:» і поля під ним з відступом; список
«- значення» — через кому): `_markup.front_matter` читає лише «ключ: значення» в один рядок.

Чому окремий модуль, а не поля в `sitemap-md`: примірники, зібрані ним, звірені, а правка
спільного читача — ризик зсуву в готовій роботі.
"""

import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.mdheading import _split_title
from engine.readers.sitemap import _LOC, _inside

_FRONT = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)


def _clean(value: str) -> str:
    return value.strip().strip('"').strip("'")


def _meta(text: str) -> dict:
    """Поля шапки з одним рівнем вкладення: «links.repository», «authors» (через кому)."""
    m = _FRONT.match(text.replace("\r\n", "\n").lstrip("﻿"))
    out: dict = {}
    parent = ""
    for ln in m.group(1).splitlines() if m else ():
        line = ln.strip()
        if not line:
            continue
        nested = ln[:1].isspace()
        if line.startswith("- "):
            if parent:
                out[parent] = ", ".join(v for v in (out.get(parent, ""), _clean(line[2:])) if v)
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        if not nested:
            parent = "" if value.strip() else key.strip()
            if value.strip():
                out[key.strip()] = _clean(value)
        elif parent:
            out[f"{parent}.{key.strip()}"] = _clean(value)
    return out


@register("sitemap-md-meta")
def sitemap_md_meta(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач sitemap-md-meta вимагає поле `within` — "
                         f"інакше сайтмап потягнув би весь сайт.")
    pages: list[str] = []
    for loc in _LOC.findall(ctx.text(source["url"])):
        page = loc.rstrip("/")
        md = page + ".md"
        if page not in pages and _inside(md, within) and ctx.allowed(md):
            pages.append(page)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")
    ends = [re.compile(r, re.M) for r in source.get("end") or ()]
    items = []
    for page in pages:
        name = _markup.slug(urlsplit(page).path)

        def make(page=page):
            md = page + ".md"
            text = ctx.text(md)
            _markup.refuse_html(text, md)
            meta = _meta(text)
            rest = _markup.front_matter(text)[1]
            title = meta.get("title", "")
            first, without = _split_title(rest)
            if not title:
                title, rest = first, without
            elif first.strip() == title.strip():
                # Той самий заголовок ще й першим рядком тіла — прибрати, щоб не дублювався.
                rest = without
            cut = [m.start() for m in (r.search(rest) for r in ends) if m]
            if cut:
                rest = rest[:min(cut)]
            lead = [f"{key.rsplit('.', 1)[-1].capitalize()}: {meta[key]}"
                    for key in source.get("lead") or () if meta.get(key)]
            body = _markup.markdown_body(rest)
            if lead:
                body = "\n".join(lead) + "\n\n" + body
            _markup.require(title, body, md, min_chars=1)
            if source.get("label"):
                title = f"{source['label']}: {title}"
            day = meta.get(source.get("date") or "", "")
            if day:
                title += f" ({day})"
            return _markup.document(title, page, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
