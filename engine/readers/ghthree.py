"""Читач сайту three.js з тегів репозиторію mrdoob/three.js: довідник, посібник і приклади.

`ghdocs-history-three` — те саме, що `ghdocs-history` (документація з тегів одного репозиторію), але
                         сторінки — файли `.html` сайту threejs.org, що лежать у самому репозиторії
                         (`docs/`, `manual/`, `examples/`). Поля ті самі (`tags`, `folders`, `recursive`,
                         `extensions`, `exclude`…).

Навіщо. Сайт threejs.org — це теки репозиторію, і довідник там завжди писали HTML, а не markdown,
трьома способами:
- **Довідник r54–r180** (`docs/api`, з r96 — `docs/api/en`; доповнення — `docs/examples/en`) — HTML із
  власною розміткою у квадратних дужках: `[name]` — назва сторінки, `[page:Vector3 v]` і
  `[link:адреса текст]` — посилання, `[method:this add]( [param:Vector3 v] )` — підпис методу з типом
  результату попереду, `[property:Float x]` — властивість із типом. Тут дужки стають звичайним
  текстом: `.add( v : Vector3 ) : this`, `.x : Float`; блок `<code>` з кількома рядками стає `<pre>`,
  бо спільний розбір бачить у `<code>` лише рядковий код і зліплює приклад в один рядок.
- **Довідник з r181** (`docs/pages`) — сторінки, згенеровані з JSDoc у коді: назва в `<h1>`, підписи
  методів у `<h3 class="name">`, параметри — таблицею `<table class="params">`. Таблиця стає
  рядками «**ім'я** — опис», інакше спільний розбір лишає від неї порожні клітинки.
- **Посібник** (`docs/manual/en` до r160, `manual/en` з r140, `manual/pages` з r181) — звичайні
  статті HTML з `<h1>` і `<pre class="prettyprint">`; їх спільний розбір бере як є.
- **Приклади** (`examples/*.html`) — сторінка прикладу: назва в `<title>`, підпис у `<div id="info">`
  і весь код у `<script type="module">`. Спільний розбір сценарії викидає, а тут код прикладу — і є
  документ: назва, підпис і код огорожею ```js.

Чому окремий модуль: інших читачів цього сайту немає, а спільні вже звірено в готових примірниках.
"""

import re

from engine.readers import _markup, register
from engine.readers.ghhistory import ghdocs_history

_HTML = re.compile(r"\.html?$", re.I)
_EXAMPLE = re.compile(r"/examples/[^/]+\.html$")
_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)
_INFO = re.compile(r'<div id="info"[^>]*>(.*?)</div>', re.S | re.I)
_MODULE = re.compile(r'<script type="module"[^>]*>(.*?)</script>', re.S | re.I)
# Дужкова розмітка довідника r54–r180; `]` у слові типу не буває, тож `[page:Float]` без тексту
# не з'їдає сусідній підпис.
_TOKEN = r"[^\]\s]+"
_PAGE_TEXT = re.compile(rf"\[(?:page|link|example):{_TOKEN}\s+([^\]]+)\]")
_PAGE = re.compile(rf"\[(?:page|link|example):({_TOKEN})\]")
_METHOD_ARGS = re.compile(rf"\[method:({_TOKEN})\s+({_TOKEN})\]\s*\(([^)]*)\)")
_METHOD = re.compile(rf"\[method:({_TOKEN})\s+({_TOKEN})\]")
_PROPERTY = re.compile(rf"\[property:({_TOKEN})\s+({_TOKEN})\]")
_PARAM = re.compile(rf"\[param:({_TOKEN})\s+({_TOKEN})\]")
_LEFTOVER = re.compile(rf"\[(?:page|link|example|param|method|property):{_TOKEN}\s*")
# Рядок-хлібна крихта над назвою («[page:Controls] &rarr;») — навігація, не текст сторінки.
_CRUMB = re.compile(r"^[ \t]*\[page:[^\]]+\][ \t]*&rarr;[ \t]*$", re.M)
_CODE_BLOCK = re.compile(r"<code>(.*?)</code>", re.S)
_PARAM_ROW = re.compile(r'<tr>\s*<td class="name">\s*<strong[^>]*>(.*?)</strong>\s*</td>\s*'
                        r'<td class="description last">(.*?)</td>\s*</tr>', re.S)
_PARAMS_TABLE = re.compile(r'<table class="params">\s*<tbody>(.*?)</tbody>\s*</table>', re.S)


def _brackets(html: str, name: str) -> str:
    html = _CRUMB.sub("", html).replace("[name]", name)
    html = _PAGE_TEXT.sub(r"\1", html)
    html = _PAGE.sub(r"\1", html)
    html = _METHOD_ARGS.sub(r".\2(\3) : \1", html)
    html = _METHOD.sub(r".\2() : \1", html)
    html = _PROPERTY.sub(r".\2 : \1", html)
    html = _PARAM.sub(r"\2 : \1", html)
    html = _LEFTOVER.sub("", html)
    return _CODE_BLOCK.sub(lambda m: f"<pre>{m.group(1)}</pre>" if "\n" in m.group(1)
                           else m.group(0), html)


def _params(html: str) -> str:
    def table(m):
        rows = _PARAM_ROW.findall(m.group(1))
        return "".join(f"<p><strong>{n.strip()}</strong> — {d}</p>" for n, d in rows)
    return _PARAMS_TABLE.sub(table, html)


def _example(html: str) -> str:
    title = _markup.html_body(_TITLE.search(html).group(1)) if _TITLE.search(html) else ""
    info = _INFO.search(html)
    code = _MODULE.search(html)
    parts = []
    if info:
        parts.append(_markup.html_body(info.group(1)))
    if code:
        parts.append("```js\n" + code.group(1).strip("\n") + "\n```")
    return f"# {title}\n\n" + "\n\n".join(p for p in parts if p.strip())


def _page(html: str, url: str) -> str:
    stem = url.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    html = _params(_brackets(html, stem))
    body = html[html.find("<body"):] if "<body" in html else html
    h1 = _H1.search(body)
    title = _markup.html_body(h1.group(1)) if h1 else stem
    if h1:
        body = body[:h1.start()] + body[h1.end():]
    return f"# {' '.join(title.split())}\n\n" + _markup.html_body(body)


class _Ctx:
    """Той самий контекст завантаження, лише файли `.html` стають markdown."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        path = url.split("?", 1)[0]
        if not _HTML.search(path):
            return text
        return _example(text) if _EXAMPLE.search(path) else _page(text, path)


@register("ghdocs-history-three")
def ghdocs_history_three(source: dict, ctx):
    return ghdocs_history(source, _Ctx(ctx))
