"""Читач історії документації TypeDoc у репозиторії: як `ghdocs-history`, але підзаголовки членів — підписи.

`ghdocs-history-typedoc` — markdown-документація з багатьох тегів одного репозиторію разом. Поля ті
                           самі, що в `ghdocs-history` (`url`, `tags`, `folders`, `files`,
                           `recursive`, `exclude`, `name_prefix` …), і ще два:
                           `inline_titles` — вираз назви заголовка (будь-якого рівня ##–######), що
                           стає рядком-підписом «**Назва**» усередині розділу, а не окремим розділом;
                           `drop_titles` — вираз назви заголовка, чий розділ (до наступного
                           заголовка того самого чи вищого рівня) вирізається цілком.
                           Назва порівнюється без розмітки посилання: «[💗 Help the project](…)» —
                           це «💗 Help the project».

Навіщо. Довідник jose згенеровано TypeDoc у markdown, і кожен член там ділиться заголовками
«Parameters», «Returns», «Type Parameters», «Call Signature». Окремим розділом вони ставали
фрагментами з одного рядка («`Promise`<`JWTVerifyResult`>»), а опис методу відривався від його
параметрів. Підписом метод лишається одним фрагментом з усім, що про нього сказано, — те саме
робить поле `inline_titles` читача `sitemap-html` для HTML-довідника TypeDoc.

`drop_titles` — для розділу, що стоїть на кожній сторінці однаковим: «💗 Help the project»
(прохання підтримати автора) відкриває кожну з півтори сотні сторінок jose. Він не відповідає ні
на яке питання, а у видачі займав би місце.

Чому окремий модуль, а не поля в `ghdocs-history`: спільний читач звірено в багатьох готових
примірниках, а тут досить обробити вже готовий текст документа.
"""

import re

from engine.readers import Item, register
from engine.readers.ghhistory import ghdocs_history

_HEADING = re.compile(r"^(#{2,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
_FENCE = re.compile(r"^[ \t]*(```|~~~)")
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def _name(raw: str) -> str:
    """Назва заголовка без розмітки посилання й зворотних лапок."""
    return _LINK.sub(r"\1", raw).replace("`", "").strip()


def _rework(text: str, inline, drop) -> str:
    """Підзаголовки з `inline` — підписи, розділи з `drop` — геть; код у блоках не чіпається."""
    out, fence, cut = [], "", 0
    for line in text.split("\n"):
        f = _FENCE.match(line)
        if fence:
            if f and f.group(1) == fence:
                fence = ""
            if not cut:
                out.append(line)
            continue
        h = _HEADING.match(line)
        if h:
            level, name = len(h.group(1)), _name(h.group(2))
            if cut and level <= cut:
                cut = 0
            if not cut and drop and drop.fullmatch(name):
                cut = level
                continue
            if not cut and inline and inline.fullmatch(name):
                out.append(f"**{name}**")
                continue
        if f:
            fence = f.group(1)
        if not cut:
            out.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out))


@register("ghdocs-history-typedoc")
def ghdocs_history_typedoc(source: dict, ctx) -> list[Item]:
    inline = re.compile(source["inline_titles"]) if source.get("inline_titles") else None
    drop = re.compile(source["drop_titles"]) if source.get("drop_titles") else None
    items = []
    for item in ghdocs_history(source, ctx):
        def make(orig=item.make):
            return _rework(orig(), inline, drop)
        items.append(Item(id=item.id, file=item.file, make=make))
    return items
