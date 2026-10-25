"""Читач сайтів, чий markdown-двійник сторінки лежить не за адресою «сторінка + .md».

`sitemap-md-suffix` — те саме, що `sitemap-md` (поля `url`, `within`, `version`), і ще два:
                      `md_suffix` — що дописується до адреси з `<loc>` без завершальної
                      риски, щоб отримати markdown-двійник (змовчання «.md»);
                      `drop` — перелік виразів (рядкових, `re.M`), збіги яких
                      прибираються з тексту до розбору; `heading_floor` — найглибший
                      рівень заголовка, що ще ділить документ на розділи: глибші стають
                      рядками жирним (поза блоками коду).

Навіщо. Довідник API reference.sanity.io (TypeDoc) пише в sitemap.xml теки
(`…/_sanity/client/index/ObservableSanityClient/`), а markdown віддає за адресою
`…/ObservableSanityClient/index.html.md`; «.md» до адреси дає сторінку 404. Кожна
сторінка довідника ще й несе рядки «Defined in: [src/…](github.com/…)» біля кожного
члена класу, а кожна сторінка sanity.io/docs починається однаковою цитатою «> For AI
agents: …llms.txt»: без `drop` перший фрагмент кожного документа відгукувався б на
«llms.txt», а рядки шляхів розбавляли б розділи довідника. TypeDoc ділить кожну
властивість ще на «#### Type Parameters», «##### LenientFieldValue», «#### Returns»: 3612
сторінок давали 30 тисяч фрагментів по кілька рядків, і на загальні слова («reference
type field») відгукувалися вони, а не сторінка сайту «Reference». `heading_floor: 3`
лишає фрагментом цілу властивість.

Чому окремий модуль, а не поля в `sitemap-md`: інші примірники з тим читачем зібрані й
звірені, а правка спільного читача — ризик зсуву в готовій роботі. Розбір сторінки той
самий, що в `mdheading._document`, — до нього лише додано чистку.
"""

import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.mdheading import _split_title
from engine.readers.mdsite import _SITEMAP
from engine.readers.sitemap import _LOC, _inside

_FENCE = re.compile(r"^\s*(```+|~~~+)")
_HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t#]*$")


def _floor(text: str, level: int) -> str:
    """Заголовки глибші за `level` — рядком жирним; рядки в огорожах коду не чіпаються:
    «# коментар» у прикладі shell заголовком не є."""
    out, fence = [], ""
    for line in text.split("\n"):
        m = _FENCE.match(line)
        if m and (not fence or m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence)):
            fence = "" if fence else m.group(1)
        elif not fence:
            h = _HEADING.match(line)
            if h and len(h.group(1)) > level:
                line = f"**{h.group(2).strip()}**"
        out.append(line)
    return "\n".join(out)


def _page(ctx, source: dict, md_url: str, page: str, drop: list) -> str:
    text = ctx.text(md_url)
    _markup.refuse_html(text, md_url)
    for pattern in drop:
        text = pattern.sub("", text)
    if source.get("heading_floor"):
        text = _floor(text, int(source["heading_floor"]))
    _, rest = _markup.front_matter(text)
    rest = _SITEMAP.sub("\n", rest)
    title, rest = _split_title(rest)
    body = _markup.markdown_body(rest)
    _markup.require(title, body, md_url, min_chars=1)
    return _markup.document(title, page, ctx.stamp, body, source.get("version", ""))


@register("sitemap-md-suffix")
def sitemap_md_suffix(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач sitemap-md-suffix вимагає поле `within` — "
                         f"інакше сайтмап потягнув би весь сайт.")
    suffix = source.get("md_suffix") or ".md"
    drop = [re.compile(p, re.M) for p in source.get("drop") or []]
    pages: list[tuple[str, str]] = []
    seen = set()
    for loc in _LOC.findall(ctx.text(source["url"])):
        md = loc.rstrip("/") + suffix
        if md not in seen and _inside(md, within) and ctx.allowed(md):
            seen.add(md)
            pages.append((loc, md))
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")
    items = []
    for page, md in pages:
        name = _markup.slug(urlsplit(page).path) or "index"

        def make(page=page, md=md):
            return _page(ctx, source, md, page, drop)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
