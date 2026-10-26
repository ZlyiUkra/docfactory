"""Читач сторінок Scribble — генератора документації Racket: книжка How to Design Programs
(htdp.org) і довідники docs.racket-lang.org.

`scribble` — явний перелік, як `html-list`: документом стає `url` і кожна адреса з `pages`,
             усі всередині `within`. Ім'я документа — `name_prefix` і ім'я файла сторінки без
             `.html` («htdp-» + part_one.html → «htdp-part-one»): дата випуску в шляху
             (htdp.org/2026-5-28/Book/…) у ім'я не потрапляє, і новий випуск лягає поверх
             тих самих документів. `version` — версія всіх документів джерела.

Навіщо окремий читач. Scribble пише код не в <pre>, а таблицею: рядок коду — <tr>, кожен
токен — <span class="Rkt…">, відступи — нерозривні пробіли в <span class="hspace">. Загальне
перетворення HTML у текст робило з такого блока стовпчик клітинок «|», і визначення функції
на кілька рядків злипалося в рядок без відступів. Тут кожен такий блок (`SCodeFlow`, таблиця
`RktBlk`) стає блоком коду racket з рядками й відступами як на сторінці. Так само граматика
мови в довіднику (таблиця без класу з клітинками `valign="baseline"`: «expr = (cond …)») і
дослівний текст (`SVerbatim`): клітинками «|» вони не читалися взагалі.

Рамка визначення довідника (`SVInsetFlow` з таблицею `RBoxed`: сигнатура, контракти
аргументів) — теж блок коду, а перед ним підзаголовок з іменем визначеного (`circle`,
`big-bang`): інакше опис функції не мав би назви, якою його питають, і лежав би в одному
розділі з десятками сусідніх функцій. Мітка рамки («procedure», «syntax») прибирається —
вона липла до першого рядка сигнатури.

Вправа книжки («Exercise 143.» жирним на початку абзацу) стає підзаголовком «Exercise 143
(ex143)»: читач книжки питає саме так, а вправа посеред великого розділу (9.2 Non-empty Lists —
десяток вправ і сторінки тексту) у видачі губилася серед сусідніх фрагментів того самого
розділу. Мітка `ex143` — одне слово для пошуку по словах: сам номер ним не є, бо «12» дають і
номери розділів («12.3 Word Games»), і числа в коді, і на запит «Exercise 12» перемагали вправи
глави 12. Промпт примірника велить шукати вправу міткою.
Розділ вправи триває до наступного заголовка, тож текст книжки між вправою й наступним
підрозділом лягає в нього; шлях розділу при цьому лишає назву підрозділу книжки.

Нотатки на полях книжки (`refelem` посеред речення, `refpara` між абзацами) стають
«(Margin note: …)» на своєму місці: без підпису вони вклинювалися в речення без меж.
Кнопки-якорі заголовків (🔗, ℹ), смуги навігації, рамка версії й таблиці змісту на
початку частини знімаються. Картинки (відрендерені зображення й формули) — без тексту, тож
випадають; їхній alt усюди «image».
"""

import html as _html
import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register

_MAIN = re.compile(r'<div class="main">')
_END = re.compile(r'<div class="navsetbottom"|<div id="contextindicator"')
_HEADING = re.compile(r"<(h[1-6])\b[^>]*>(.*?)</\1>", re.S)

_BOX = re.compile(r'<blockquote class="SVInsetFlow">')
_FLOW = re.compile(r'<blockquote class="SCodeFlow">')
_BLOCK = re.compile(r'<table[^>]*\bclass="RktBlk"[^>]*>')
_TABLE = re.compile(r"<table\b[^>]*>")
_REFELEM = re.compile(r'<span class="refelem">')
_REFPARA = re.compile(r'<(?:p|blockquote) class="refpara">')
_STRIP = [re.compile(r'<span class="button-group">'), re.compile(r'<div class="navsettop">'),
          re.compile(r'<div class="versionbox">'),
          re.compile(r'<div class="RBackgroundLabel[^"]*">')]
_DEF = re.compile(r'class="Rkt(?:Val|Stx)Def[^"]*"[^>]*>(.*?)</a>', re.S)
_EXERCISE = re.compile(r'<a name="\(counter\.[^"]*exercise[^"]*\)"></a>'
                       r'<span style="font-weight: bold">Exercise</span>(?:&nbsp;|\s)*(\d+)\.')
_IMG = re.compile(r"<img\b[^>]*>")
_TAGS = re.compile(r"<[^>]+>")


def _close(page: str, start: int) -> int:
    """Індекс одразу за закривальним тегом елемента, що відкривається в `start`."""
    tag = re.compile(r"<(\w+)").match(page, start).group(1)
    depth = 0
    for m in re.compile(rf"<(/?){tag}\b[^>]*>").finditer(page, start):
        if m.group(0).endswith("/>"):
            continue
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end()
    return len(page)


def _each(page: str, opener: re.Pattern, fn) -> str:
    """Кожен елемент, що починається збігом `opener`, разом із вкладеними — через `fn`."""
    out, pos = [], 0
    while m := opener.search(page, pos):
        end = _close(page, m.start())
        out += [page[pos:m.start()], fn(page[m.start():end])]
        pos = end
    return "".join(out + [page[pos:]])


def _lines(block: str) -> str:
    """Таблиця чи абзац коду Scribble → рядки тексту з відступами."""
    text = re.sub(r"</tr>|</p>|<br\s*/?>", "\n", block)
    text = _html.unescape(_TAGS.sub("", text)).replace("\xa0", " ")
    return "\n".join(line.rstrip() for line in text.split("\n")).strip("\n")


def _pre(block: str) -> str:
    """Блок коду racket. `<br>` попереду — для блока, яким починається пункт списку: без
    нього огорожа лягала в рядок маркера («- ```racket»), не відкривалася, і закривальна
    «```» відкривала натомість новий блок, що ковтав заголовки до кінця сторінки."""
    code = _lines(block)
    return f'<br><pre class="language-racket">{_html.escape(code)}</pre>' if code.strip() else ""


def _box(block: str) -> str:
    names = []
    for raw in _DEF.findall(block):
        name = _html.unescape(_TAGS.sub("", raw)).strip()
        if name and name not in names:
            names.append(name)
    head = f"<h5>{_html.escape(', '.join(names))}</h5>" if names else ""
    return head + _pre(block)


def _table(block: str) -> str:
    head = block[:block.find(">") + 1]
    if 'class="toclink"' in block:
        return ""
    if "SVerbatim" in head or ('valign="baseline"' in block and "RktVar" in block):
        return _pre(block)
    return block


def _note(block: str, inline: bool) -> str:
    text = _markup.html_body(block).strip()
    if not text:
        return ""
    note = _html.escape(f"(Margin note: {' '.join(text.split())})")
    return f" {note} " if inline else f"<p>{note}</p>"


def _text(page: str, url: str, stamp: str, version: str) -> str:
    start = _MAIN.search(page)
    if not start:
        raise SystemExit(f"Сторінка не схожа на Scribble ({url}): немає <div class=\"main\"> — "
                         f"документ не записую.")
    stop = _END.search(page, start.end())
    part = page[start.end():stop.start() if stop else len(page)]
    for opener in _STRIP:
        part = _each(part, opener, lambda _: "")
    part = _each(part, _BOX, _box)
    part = _each(part, _FLOW, _pre)
    part = _each(part, _BLOCK, _pre)
    part = _each(part, _TABLE, _table)
    part = _each(part, _REFELEM, lambda b: _note(b, True))
    part = _each(part, _REFPARA, lambda b: _note(b, False))
    part = _IMG.sub("", part)
    part = _EXERCISE.sub(r"<h6>Exercise \1 (ex\1)</h6>", part)
    head = _HEADING.search(part)
    if not head:
        raise SystemExit(f"На сторінці немає заголовка ({url}) — документ не записую.")
    title = _markup.html_body(head.group(2)).strip()
    body = _markup.html_body(part[head.end():])
    _markup.require(title, body, url)
    return _markup.document(title, url, stamp, body, version)


@register("scribble")
def scribble(source: dict, ctx) -> list[Item]:
    pages = [source["url"]] + list(source.get("pages") or ())
    items = []
    for page in pages:
        if not ctx.allowed(page):
            raise SystemExit(f"{source['id']}: адреса {page} поза білим списком — "
                             f"допишіть її в `within`.")
        stem = urlsplit(page).path.rsplit("/", 1)[-1].removesuffix(".html")
        name = _markup.slug(source.get("name_prefix", "") + stem)

        def make(page=page):
            return _text(ctx.text(page), page, ctx.stamp, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items
