"""Читач сторінок man у розмітці roff з багатьох тегів одного репозиторію (c-ares).

`ghdocs-history-roff` — файли `.1`–`.8` з багатьох тегів разом. Поля ті самі, що в `ghdocs-history` (`url`, `tags`,
                      `folders`, `recursive`, `extensions`, `exclude`, `name_prefix` …). Текст кожного такого файла
                      перед звичайним розбором стає markdown тим самим перетворювачем groff, що й у читача
                      `man-pages` (`.SH` → розділ, `.TP` → пункт, `.BR`/`\\fB` → виділення, таблиці tbl).

Навіщо. Довідник c-ares — десятки сторінок `ares_*.3`, що лежать у репозиторії файлами roff: у ≤1.10 у корені, далі в
`docs/`. Спільні читачі markdown ці файли лишили б із макросами `.BR`, `.TP`.

Чому окремий модуль, а не поле в `ghdocs-history`: спільний читач звірено в багатьох готових примірниках, а тут
досить підмінити текст файла, перш ніж читач його розбере.
"""

import re

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history
from engine.readers.manpages import to_markdown

_ROFF = re.compile(r"\.[1-8][a-z]?$")


class _Ctx:
    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        if not _ROFF.search(url.split("?", 1)[0]):
            return text
        title, body = to_markdown(text)
        head = f"# {title}\n\n" if title and not body.lstrip().startswith("# ") else ""
        return head + body


@register("ghdocs-history-roff")
def ghdocs_history_roff(source: dict, ctx):
    return ghdocs_history(source, _Ctx(ctx))
