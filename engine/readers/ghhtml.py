"""Читач HTML-сторінок документації з багатьох тегів одного репозиторію (ImageMagick, Ghostscript, ExifTool).

`ghdocs-history-html` — файли `.html`/`.htm` з багатьох тегів разом. Поля ті самі, що в `ghdocs-history` (`url`,
                      `tags`, `folders`, `recursive`, `files`, `extensions`, `exclude`, `name_prefix`, `site` …).
                      Необов'язкові: `start` — вирази в порядку переваги: текст сторінки починається з першого
                      збігу першого виразу, що знайшовся (типово `<body`), — меню й шапка стоять раніше; `end` —
                      вирази, на найранішому збігу яких текст закінчується (типово `<footer`); `drop` — вирази
                      шматків, що вирізаються всередині тексту (бічне меню, рядок «назад до змісту»);
                      `title_strip` — вирази, що зрізаються з назви («ImageMagick – » перед назвою сторінки);
                      `title_heading` — рівень чи перелік рівнів («h2», `["h2", "h3"]`): сторінка без <h1> бере
                      назву з першого такого заголовка, а не з <title> (документація NUnit 2: <title> кожної
                      сторінки — «NUnit.org», назва — у <h2> чи <h3>).

Навіщо. Сайт ImageMagick до 7.1.2 жив у теці `www/` самого репозиторію, документація Ghostscript до 10.0 — у
`doc/*.htm`, сайт ExifTool і досі — тека `html/` репозиторію. Ці теки — готовий HTML, і саме його показував сайт
кожної версії, тож історія тегів дає сайт на кожен випуск. Спільний `ghdocs-history` бере лише markdown і HTML
відкидає як сторінку помилки.

Чому обгортка, а не поле в `ghdocs-history`: спільний читач звірено в багатьох готових примірниках, а тут досить
перетворити текст файла на markdown, перш ніж читач його розбере (так само зроблено `ghdocs-history-roff`).
"""

import re

from engine.readers import _markup, register
from engine.readers.ghhistory import ghdocs_history

_HTML = re.compile(r"\.html?$", re.I)
_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)


class _Ctx:
    def __init__(self, ctx, source: dict):
        self._ctx = ctx
        self._start = [re.compile(r, re.S | re.I) for r in source.get("start") or (r"<body",)]
        self._end = [re.compile(r, re.S | re.I) for r in source.get("end") or (r"<footer",)]
        self._drop = [re.compile(r, re.S | re.I) for r in source.get("drop") or ()]
        self._title_strip = [re.compile(r) for r in source.get("title_strip") or ()]
        # `title_heading: "h2"` — сторінка без <h1>, чия назва стоїть у першому <h2> (документація NUnit 2 на
        # docs.nunit.org: <title> у всіх 323 сторінок — «NUnit.org»). Без поля — як було.
        levels = source.get("title_heading") or []
        levels = [levels] if isinstance(levels, str) else list(levels)
        levels = [lv for lv in levels if re.fullmatch(r"h[2-6]", str(lv))]
        self._title_h = (re.compile(rf"<({'|'.join(levels)})\b[^>]*>(.*?)</\1>", re.S | re.I)
                         if levels else None)

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        if not _HTML.search(url.split("?", 1)[0]):
            return text
        return self.convert(text)

    def convert(self, html: str) -> str:
        # Сторінка Jekyll (чинний сайт ImageMagick): шапка YAML з назвою, далі — саме тіло без меню.
        named = ""
        if html.startswith("---\n") and (close := html.find("\n---", 4)) > 0:
            m = re.search(r"^title:\s*[\"']?(.*?)[\"']?\s*$", html[4:close], re.M)
            named = m.group(1) if m else ""
            html = html[close + 4:]
        begin = 0
        for rx in self._start:
            if m := rx.search(html):
                begin = m.start()
                break
        stops = [m.start() for rx in self._end if (m := rx.search(html, begin + 1))]
        part = html[begin:min(stops) if stops else len(html)]
        for rx in self._drop:
            part = rx.sub("", part)
        # Назва — перший <h1> тексту, а як його немає — <title> сторінки: у <title> старих сторінок
        # ImageMagick і Ghostscript стоїть назва сайту разом з назвою сторінки.
        h1 = None if named else _H1.search(part)
        if h1 is None and not named and self._title_h is not None:
            hx = self._title_h.search(part)
            if hx:
                named = _markup.html_body(hx.group(2))
                part = part[:hx.start()] + part[hx.end():]
        title = named or (_markup.html_body(h1.group(1)) if h1 else "")
        if h1:
            part = part[:h1.start()] + part[h1.end():]
        if not title.strip():
            # Перший <title> — назва сторінки; далі бувають <title> іконок SVG («Twitter»).
            found = _TITLE.findall(html)
            title = _markup.html_body(found[0]) if found else ""
        title = " ".join(title.replace("#", " ").split())
        for rx in self._title_strip:
            title = rx.sub("", title).strip()
        body = _markup.html_body(part)
        return (f"# {title}\n\n" if title else "") + body


@register("ghdocs-history-html")
def ghdocs_history_html(source: dict, ctx):
    return ghdocs_history(source, _Ctx(ctx, source))
