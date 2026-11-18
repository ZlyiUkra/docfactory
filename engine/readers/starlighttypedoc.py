"""Читач довідника API, який TypeDoc зібрав усередині сайту Astro Starlight (starlight-typedoc).

`sitemap-starlight-typedoc` — те саме, що `sitemap-starlight` (поля `within`, `match`, `exclude`,
                              `end`, `drop`, `start`, `min_chars`, `inline_titles`, `version`), і ще два:
                              `heading_floor` — найглибший рівень заголовка, що ще ділить сторінку
                              на розділи: глибші стають рядками жирним;
                              `skip_inherited: true` — розділ члена класу з підзаголовком «Inherited
                              from» у текст не йде, якщо предок має власну сторінку (його назва в
                              рядку походження — посилання); наприкінці сторінки лишається розділ
                              «Inherited members» з переліком імен і тим, звідки кожен успадковано.

Навіщо. Довідник Fabric.js 7 (fabricjs.com/api) збирає плагін starlight-typedoc під час збирання
сайту: markdown-сторінок немає ні в репозиторії, ні на сайті, є лише готовий HTML. Розмітка та
сама, що в довіднику TypeDoc деінде, і хвороби ті самі. Кожен член класу поділено на
«Parameters», «Returns», «Inherited from», «Overrides», а кожен параметр ще й має власний
заголовок: сторінка класу Canvas несе 161 член, 417 заголовків четвертого рівня і 143 п'ятого.
І багато на ній чужого: члени FabricObject стоять дослівно на сторінках Rect, Circle, Textbox
і ще двох десятків класів. Без відбору пошук знаходив би уривки з двох рядків і одну
властивість під десятком назв класів.

Не кожен предок має сторінку. Canvas успадковує 146 членів від SelectableCanvas, а цього класу
в довіднику немає: TypeDoc пише його назву в рядку походження простим текстом, без посилання.
Такий член лишається на сторінці нащадка, бо більше його ніде не описано. Викидається лише
член, чий предок названий посиланням, тобто описаний на власній сторінці.

Ті самі два поля вже є в читача `llms-typedoc` — для довідника, що віддає markdown. Тут те саме
робиться над HTML, до спільного розбору сторінки: розділ члена — це шматок від його обгортки
`sl-heading-wrapper level-h3` до наступної такої самої чи другого рівня. Конструктор лишається
завжди: TypeDoc позначає його успадкованим, коли клас свого не оголошує, але підпис і параметри
кажуть, як створити саме цей клас.

Чому окремий модуль, а не поля в `sitemap-starlight`: примірник із тим читачем зібраний і
звірений, а правка спільного читача — ризик зсуву в готовій роботі. Сторінка змінюється
обгорткою над `ctx`, як і там: сховище сирого тримає відповідь сайту такою, як вона прийшла.
"""

import re
from html import unescape

from engine.readers import register
from engine.readers.sitemap import _LOC, _inside
from engine.readers.sitemaphtml import _fields, _items
from engine.readers.starlight import clean

_BLOCK = re.compile(r'<div class="sl-heading-wrapper level-h([23])">')
_NAME = re.compile(r"<h3\b[^>]*>(.*?)</h3>", re.S)
_INHERITED = re.compile(r"<h4\b[^>]*>\s*Inherited from\s*</h4>(?:\s*</div>)?\s*<p>(.*?)</p>", re.S)
_TAIL = re.compile(r"</article>|</main>|<footer\b")
_TAG = re.compile(r"<[^>]+>")
_RULE = re.compile(r"(?:\s*<hr\b[^>]*>)+\s*$")


def _plain(fragment: str) -> str:
    return " ".join(unescape(_TAG.sub("", fragment)).split())


def skip_inherited(html: str) -> str:
    """Розділи членів з підзаголовком «Inherited from», чий предок має власну сторінку, — геть;
    їхні імена й походження лягають переліком «Inherited members» після останнього розділу."""
    starts = [m.start() for m in _BLOCK.finditer(html)]
    if not starts:
        return html
    tail = _TAIL.search(html, starts[-1])
    end = tail.start() if tail else len(html)
    bounds = starts + [end]
    out, inherited = [html[:starts[0]]], []
    for i, start in enumerate(starts):
        block = html[start:bounds[i + 1]]
        name = _NAME.search(block) if block.startswith('<div class="sl-heading-wrapper level-h3">') else None
        origin = _INHERITED.search(block) if name else None
        # Без посилання в рядку походження предок власної сторінки не має: опис члена стоїть
        # лише тут, і викинути його означало б втратити зовсім.
        if not origin or "<a " not in origin.group(1) or _plain(name.group(1)) == "Constructor":
            out.append(block)
            continue
        inherited.append(f"<li><code>{_plain(name.group(1))}</code> — from {_plain(origin.group(1))}</li>")
        # Лінія-роздільник перед викинутим членом лишилася б висіти без нього.
        out[-1] = _RULE.sub("", out[-1])
    if inherited:
        out.append('<div class="sl-heading-wrapper level-h2"><h2 id="inherited-members">Inherited members'
                   "</h2></div><p>Declared by a parent class or interface and described on its page:</p>"
                   f"<ul>{''.join(inherited)}</ul>")
    out.append(html[end:])
    return "".join(out)


def floor(html: str, level: int) -> str:
    """Заголовки глибші за `level` — абзацом жирним: ділити сторінку вони перестають."""
    deep = "".join(str(n) for n in range(level + 1, 7))
    if not deep:
        return html
    return re.sub(rf"<h([{deep}])\b[^>]*>(.*?)</h\1>", r"<p><strong>\2</strong></p>", html, flags=re.S)


class _Typedoc:
    """Той самий `ctx`, але сторінки віддає очищеними й без успадкованого: розбір спільний."""

    def __init__(self, ctx, source: dict):
        self._ctx = ctx
        self._skip = source.get("skip_inherited") is True
        self._floor = int(source.get("heading_floor") or 0)

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url, *args, **kwargs):
        html = clean(self._ctx.text(url, *args, **kwargs))
        if self._skip:
            html = skip_inherited(html)
        if self._floor:
            html = floor(html, self._floor)
        return html


@register("sitemap-starlight-typedoc")
def sitemap_starlight_typedoc(source: dict, ctx) -> list:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач sitemap-starlight-typedoc вимагає поле `within` — "
                         f"інакше сайтмап потягнув би весь сайт.")
    match = re.compile(source["match"]) if source.get("match") else None
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    pages: list[str] = []
    for loc in _LOC.findall(ctx.text(source["url"])):
        page = loc.rstrip("/")
        if page + "/" in within:
            page += "/"
        if (page not in pages and _inside(page, within) and ctx.allowed(page)
                and (not match or match.search(page))
                and not any(r.search(page) for r in exclude)):
            pages.append(page)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")
    return _items(source, _Typedoc(ctx, source), pages, *_fields(source))
