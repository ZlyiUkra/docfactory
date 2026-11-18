"""Читач довідника API, який TypeDoc віддає markdown-ом, а перелік сторінок лежить у llms.txt.

`llms-typedoc` — те саме, що `llms` (поля `url`, `within`, `version`, `title_prefix`), і ще чотири:
                 `heading_floor` — найглибший рівень заголовка, що ще ділить документ на розділи:
                 глибші стають рядками жирним (поза блоками коду), як у `sitemap-md-suffix`;
                 `skip_inherited: true` — розділ члена класу, що несе підзаголовок «Inherited from»,
                 у текст не йде; наприкінці документа лишається розділ «Inherited members» з
                 переліком імен і тим, звідки кожен успадковано;
                 `drop` — перелік виразів (рядкових, `re.M`), збіги яких прибираються до розбору;
                 `min_chars` — найкоротше тіло сторінки без заголовків, що ще вважається
                 документом (типово спільна межа `_markup.MIN_BODY`).
                 Сторінка береться, лише якщо її адреса лежить у `within` цього ж джерела: перелік
                 llms.txt спільний на посібник і довідник, і дозволу іншого джерела тут не досить.

Навіщо. Довідник PixiJS 8 (pixijs.download/v8.23.0/docs) і PixiJS 3D зібрано TypeDoc, а
markdown-двійники сторінок перелічує llms.txt сайту. TypeDoc ділить кожен член класу ще на
«#### Parameters», «#### Returns», «#### Default», «#### Example», «#### Inherited from»: 268
сторінок довідника несуть 28 850 таких підзаголовків, і розбір за ними дав би десятки тисяч
фрагментів по два-три рядки. На запит «Sprite anchor» відгукувалися б уривки «Returns» і
«Default», а не опис властивості. `heading_floor: 3` лишає фрагментом цілий член класу.

Друге — успадковане. TypeDoc розгортає на сторінці кожного класу всі члени його предків разом
з їхніми описами: з 6 865 членів довідника PixiJS 8 успадкованих 4 765, тобто `alpha`,
`position` чи `destroy` контейнера стоять дослівно на сторінках Sprite, Graphics, Text і ще
сотні класів. У видачі це ті самі слова під різними назвами, які займають усі місця. З
`skip_inherited` опис члена лишається один раз, на сторінці класу, що його оголосив, а
нащадок каже, що член у нього є і чий він.

Чому окремий модуль, а не поля в `llms`: примірники з тим читачем зібрані й звірені, а правка
спільного читача — ризик зсуву в готовій роботі. Перелік сторінок складається так само, як у
`llms`, поділ заголовків — тим самим `_floor`, що в `sitemap-md-suffix`.
"""

import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.mdheading import _split_title
from engine.readers.mdsite import _MD_LINK
from engine.readers.sitemap import _inside
from engine.readers.sitemapmdsuffix import _FENCE, _floor

_MEMBER = re.compile(r"^###[ \t]+(.+?)[ \t#]*$")
_SECTION = re.compile(r"^#{1,2}[ \t]+\S")
_INHERITED = re.compile(r"^####[ \t]+Inherited from[ \t]*$")
_RULE = re.compile(r"^\*{3,}[ \t]*$")


def _skip_inherited(text: str) -> str:
    """Розділи третього рівня з підзаголовком «Inherited from» — геть; їхні імена й походження
    складаються в розділ «Inherited members» наприкінці. Рядки в огорожах коду не розбираються."""
    blocks: list[list[str]] = [[]]
    fence = ""
    for line in text.split("\n"):
        m = _FENCE.match(line)
        if m and (not fence or m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence)):
            fence = "" if fence else m.group(1)
        elif not fence and (_MEMBER.match(line) or _SECTION.match(line)):
            blocks.append([])
        blocks[-1].append(line)
    out: list[str] = []
    inherited: list[str] = []
    for block in blocks:
        head = _MEMBER.match(block[0]) if block else None
        at = next((i for i, line in enumerate(block) if _INHERITED.match(line)), -1) if head else -1
        # Конструктор TypeDoc теж позначає успадкованим, коли клас свого не оголошує, але його
        # підпис і параметри — це те, як створити саме цей клас: він лишається на сторінці.
        if at < 0 or head.group(1).strip() == "Constructor":
            out.extend(block)
            continue
        origin = next((line.strip() for line in block[at + 1:] if line.strip()), "")
        origin = origin.replace("`", "")
        inherited.append(f"- `{head.group(1).strip()}`" + (f" — from {origin}" if origin else ""))
        # Лінія-роздільник перед наступним членом належала викинутому: без нього вона зайва.
        while out and (not out[-1].strip() or _RULE.match(out[-1])):
            out.pop()
        out.append("")
    if inherited:
        out += ["", "## Inherited members", "",
                "Declared by a parent class or interface and described on its page:", ""] + inherited
    return "\n".join(out)


@register("llms-typedoc")
def llms_typedoc(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач llms-typedoc вимагає поле `within` — "
                         f"інакше перелік потягнув би чужі сторінки.")
    drop = [re.compile(p, re.M) for p in source.get("drop") or []]
    prefix = source.get("title_prefix", "")
    floor = int(source.get("heading_floor") or 0)
    least = int(source.get("min_chars") or _markup.MIN_BODY)
    links: list[str] = []
    for url in _MD_LINK.findall(ctx.text(source["url"])):
        if url not in links and url != source["url"] and _inside(url, within) and ctx.allowed(url):
            links.append(url)
    if not links:
        raise SystemExit(f"У переліку {source['url']} не знайдено жодної дозволеної "
                         f"сторінки .md — розмітка змінилася або `within` не той.")
    items = []
    for url in links:
        page = url[:-3]
        name = _markup.slug(urlsplit(page).path)

        def make(url=url, page=page):
            text = ctx.text(url)
            _markup.refuse_html(text, url)
            for pattern in drop:
                text = pattern.sub("", text)
            if source.get("skip_inherited") is True:
                text = _skip_inherited(text)
            if floor:
                text = _floor(text, floor)
            _, rest = _markup.front_matter(text)
            title, rest = _split_title(rest)
            body = _markup.markdown_body(rest)
            _markup.require(title, body, url, min_chars=least)
            if prefix and prefix.lower() not in title.lower():
                title = f"{prefix}: {title}"
            return _markup.document(title, page, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
