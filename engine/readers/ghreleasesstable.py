"""Читач нотаток релізів монорепозиторію: лише сталі релізи одного пакета.

`ghreleases-stable` — те саме, що `ghreleases-tagged` (обов'язкове поле `tag_prefix`, версія —
                      решта тега), але без передрелізів: тег, де за номером «1.2.3» стоїть
                      дефіс (`-alpha.4`, `-beta.30`, `-rc.8`), не береться.

Навіщо. У TanStack Router одним потоком ідуть 3 146 релізів, з них 579 — передрелізи: беты
0.0.1, альфи 1.121 і 1.132, лінія Solid 2.0 у rc. Примірник обіцяє лише сталі версії, тож
передрелізи мусять випасти ще до запису.

Друге — сторінки потоку. Пакетів у репозиторії чотири десятки, і кожне джерело
`ghreleases-tagged` гортало б ті самі 32 сторінки API заново: понад тисячу звернень заради
одного переліку. Тут сторінка, раз прочитана, лишається в пам'яті до кінця прогону, і решта
джерел того самого потоку бере її звідти.

Чому окремий читач, а не поле в `ghreleases-tagged`: примірники з тим читачем звірені, а правка
спільного читача — ризик зсуву в готовій роботі. Розбір той самий — його й викликано.
"""

import re

from engine.readers import register
from engine.readers.ghtagged import ghreleases_tagged

# адреса сторінки релізів → її текст; один прогін — один процес, тож живе до його кінця
_PAGES: dict = {}
_PRE = re.compile(r"\d+\.\d+\.\d+-")


class _Pages:
    """Обгортка контексту: сторінки релізів читає один раз, решту передає як є."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, gzip: bool = False) -> str:
        if url not in _PAGES:
            _PAGES[url] = self._ctx.text(url, gzip)
        return _PAGES[url]


@register("ghreleases-stable")
def ghreleases_stable(source: dict, ctx) -> list:
    items = ghreleases_tagged(source, _Pages(ctx))
    stable = [it for it in items if not _PRE.search(it.id.split("/", 1)[1])]
    if not stable:
        raise SystemExit(f"{source['url']}: жодного сталого релізу з тегом "
                         f"«{source['tag_prefix']}…».")
    return stable
