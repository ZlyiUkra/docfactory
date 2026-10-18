"""Читач сторінок man у розмітці roff з багатьох тегів одного репозиторію (c-ares).

`ghdocs-history-roff` — файли `.1`–`.8` з багатьох тегів разом. Поля ті самі, що в `ghdocs-history` (`url`, `tags`,
                      `folders`, `recursive`, `extensions`, `exclude`, `name_prefix` …). Текст кожного такого файла
                      перед звичайним розбором стає markdown тим самим перетворювачем groff, що й у читача
                      `man-pages` (`.SH` → розділ, `.TP` → пункт, `.BR`/`\\fB` → виділення, таблиці tbl).
                      Необов'язкові: `roff_match` — вираз імен файлів roff замість типового `.1`–`.8` (у file
                      сторінки звуться `file.man`, `magic.man`); `substitute` — пари «що → на що», які
                      підставляються в текст до розбору (заглушки збирання `__CSECTION__`, `__MAGIC__`).
                      Сторінка в mdoc (`.Dd`/`.Sh` без `.TH`, як у file) розбирається перетворювачем `_mdoc`.

Навіщо. Довідник c-ares — десятки сторінок `ares_*.3`, що лежать у репозиторії файлами roff: у ≤1.10 у корені, далі в
`docs/`. Спільні читачі markdown ці файли лишили б із макросами `.BR`, `.TP`.

Чому окремий модуль, а не поле в `ghdocs-history`: спільний читач звірено в багатьох готових примірниках, а тут
досить підмінити текст файла, перш ніж читач його розбере.
"""

import re

from engine.readers import _mdoc, register
from engine.readers.ghhistory import ghdocs_history
from engine.readers.manpages import to_markdown

_ROFF = re.compile(r"\.[1-8][a-z]?$")


class _Ctx:
    def __init__(self, ctx, source: dict | None = None):
        self._ctx = ctx
        source = source or {}
        self._match = re.compile(source["roff_match"]) if source.get("roff_match") else _ROFF
        self._subst = [tuple(p) for p in source.get("substitute") or ()]

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        if not self._match.search(url.split("?", 1)[0]):
            return text
        for old, new in self._subst:
            text = text.replace(old, new)
        title, body = (_mdoc.to_markdown if _mdoc.is_mdoc(text) else to_markdown)(text)
        head = f"# {title}\n\n" if title and not body.lstrip().startswith("# ") else ""
        return head + body


@register("ghdocs-history-roff")
def ghdocs_history_roff(source: dict, ctx):
    return ghdocs_history(source, _Ctx(ctx, source))
