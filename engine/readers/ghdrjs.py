"""Читач довідника API, зібраного dr.js: одна сторінка HTML на весь довідник, запис на кожен метод.

`ghdocs-history-drjs` — те саме, що `ghdocs-history` (поля `url`, `tags`, `files`, `folders`, `path_title`,
                        `site`, `name_prefix` …), і одна різниця: файл `.html` з raw.githubusercontent.com
                        перед розбором стає markdown, по розділу «##» на кожен запис довідника.

Навіщо. Snap.svg збирає довідник інструментом dr.js із коментарів у коді й кладе в репозиторій одним файлом
`doc/reference.html` на 660 КБ: меню на шістсот посилань, а далі двісті блоків `<article id="Element.attr">`.
Спільний читач HTML узяв би меню як текст і поділив би сторінку за її заголовками, а ті в кожній версії
інші: запис методу — `<h4>` у 0.1.0, `<h3>` у 0.3.0, `<h2>` у 0.5.1, тоді як підпис «Parameters» усередині
запису — завжди `<h3>`. У 0.3.0 метод і його параметри мали б один рівень, і параметри стали б окремим
розділом без назви методу.

Тут рівень не важить: назва запису — перший заголовок у `<header>` блоку `<article>` (без якоря «⚓» і
посилання на рядок коду), і вона стає «##». Заголовки всередині запису («Parameters», «Usage») — рядки
жирним, тож фрагмент пошуку — цілий метод із параметрами, значенням, що повертається, і прикладом. Ім'я
параметра й тип значення, що повертається, стають кодом, типи параметра беруться в дужки. Блок без тексту (назва об'єкта перед його методами)
не береться.

Чому обгортка, а не поле в `ghdocs-history`: перелік тегів, імена документів і версії той читач складає
сам і звірений у десятках примірників. Тут лише текст файла міняється дорогою: об'єкт `ctx`, який він
отримує, віддає сторінку довідника вже як markdown.
"""

import html as html_lib
import re
from urllib.parse import urlsplit

from engine.readers import _markup, register
from engine.readers.ghhistory import ghdocs_history

_ARTICLE = re.compile(r"<article\b[^>]*>(.*?)</article>", re.S)
_HEADER = re.compile(r"<header\b[^>]*>\s*<h[1-6]\b[^>]*>(.*?)</h[1-6]>\s*</header>", re.S)
_ANCHOR = re.compile(r"<a\b[^>]*class=\"dr-(?:hash|sourceline)\"[^>]*>.*?</a>", re.S)
_HEADING = re.compile(r"<h[1-6]\b[^>]*>(.*?)</h[1-6]>", re.S)
_PARAM = re.compile(r"<span class=\"dr-param\">(.*?)</span>", re.S)
_TYPE = re.compile(r"<span class=\"dr-type\">(.*?)</span>", re.S)
_OPTIONAL = re.compile(r"<span class=\"dr-optional\">(.*?)</span>", re.S)
_PRE = re.compile(r"<pre class=\"javascript code\">")
_TITLE = re.compile(r"<strong class=\"dr-title\">(.*?)</strong>", re.S)
_RETURN_TYPE = re.compile(r"<em class=\"dr-type-[^\"]*\">(.*?)</em>", re.S)
_TAG = re.compile(r"<[^>]+>")


def _plain(fragment: str) -> str:
    return " ".join(html_lib.unescape(_TAG.sub("", fragment)).split())


def drjs_to_markdown(page: str) -> str:
    """Сторінка довідника dr.js → markdown; сторінка без жодного `<article>` повертається як була."""
    out = []
    for block in _ARTICLE.findall(page):
        head = _HEADER.search(block)
        if not head:
            continue
        name = _plain(_ANCHOR.sub("", head.group(1)))
        body = block[head.end():]
        body = _HEADING.sub(lambda h: f"<p>**{_plain(h.group(1))}**</p>", body)
        body = _PARAM.sub(lambda p: f"<code>{_plain(p.group(1))}</code>", body)
        body = _OPTIONAL.sub(lambda o: f"({_plain(o.group(1))})", body)
        body = _TYPE.sub(lambda t: f"({', '.join(_plain(t.group(1)).split())})", body)
        body = _PRE.sub("<pre class=\"language-js\">", body)
        body = _TITLE.sub(lambda t: f"**{_plain(t.group(1))}**", body)
        body = _RETURN_TYPE.sub(lambda t: f"<code>{_plain(t.group(1))}</code>", body)
        text = _markup.html_body(body)
        if name and text.strip():
            out.append(f"## {name}\n\n{text.strip()}")
    return "\n\n".join(out) + "\n" if out else page


class _DrjsCtx:
    """`ctx`, що віддає сторінку довідника з GitHub уже як markdown; решта звернень — до справжнього."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        parts = urlsplit(url)
        if parts.netloc == "raw.githubusercontent.com" and parts.path.endswith((".html", ".htm")):
            return drjs_to_markdown(text)
        return text


@register("ghdocs-history-drjs")
def ghdocs_history_drjs(source: dict, ctx) -> list:
    return ghdocs_history(source, _DrjsCtx(ctx))
