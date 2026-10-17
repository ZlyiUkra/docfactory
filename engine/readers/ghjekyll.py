"""Читач історії документації, яку сайт збирає Jekyll із тегами Liquid і маркером `[TOC]`.

`ghdocs-history-jekyll` — те саме, що `ghdocs-history` (усі його поля), плюс перед розбором
                          кожна сторінка `.md` проходить три заміни:
                          - рядок `[TOC]` (місце, куди сайт ставить зміст сторінки) зникає;
                          - вставка графіка `{% include graph.html … title="…" %}`, також
                            розірвана на кілька рядків, стає рядком «Graph: …»;
                          - позначки `{% raw %}` і `{% endraw %}` зникають, а текст між ними
                            лишається як є.

Навіщо. Тека g3doc репозиторію gVisor — джерело сторінок gvisor.dev, які збирає Jekyll. Майже
кожна сторінка посібника починається рядком `[TOC]`, і в корпусі він ставав першим рядком
тексту розділу. Сторінка продуктивності вставляє графіки бенчмарків тегом Liquid, розірваним на
два рядки, — розбирач markdown ядра знає лише однорядкові теги, тож тег лягав у текст сирим.
У прикладі команди Docker (`--format='{% raw %}{{.ID}}{% endraw %}'`) позначки `raw` лише
ховають від Jekyll дужки шаблону Go: людина на сайті бачить `{{.ID}}`.

Чому окремий модуль, а не поле в `ghdocs-history`: примірники з тим читачем зібрані й
звірені, а правка спільного читача — ризик зсуву в готовій роботі. Розбір той самий — його й
викликано; заміни робить обгортка контексту, через яку читач бере текст сторінки.
"""

import re

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_RAW_PAGE = re.compile(r"^https://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/.+\.md$")
_TOC = re.compile(r"^[ \t]*\[TOC\][ \t]*\n?", re.M)
_GRAPH = re.compile(r"\{%\s*include\s+graph\.html\b(.*?)%\}", re.S)
_RAW_TAG = re.compile(r"\{%\s*(?:raw|endraw)\s*%\}")


def _clean(text: str) -> str:
    def graph(m):
        title = re.search(r'title="([^"]*)"', m.group(1))
        return f"Graph: {' '.join(title.group(1).split())}" if title else ""

    return _RAW_TAG.sub("", _GRAPH.sub(graph, _TOC.sub("", text.replace("\r\n", "\n"))))


class _Jekyll:
    """Обгортка контексту: сторінки `.md` віддає вже без `[TOC]` і тегів Liquid, усе інше
    (дерева тегів) — як є."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, gzip: bool = False, accept: str = "") -> str:
        text = self._ctx.text(url, gzip, accept)
        return _clean(text) if _RAW_PAGE.match(url) else text


@register("ghdocs-history-jekyll")
def ghdocs_history_jekyll(source: dict, ctx) -> list:
    return ghdocs_history(source, _Jekyll(ctx))
