"""Читач сторінок посібника, написаних для gi-docgen і для gtk-doc через pandoc: як `ghdocs-history`, без їхньої службової розмітки.

`ghdocs-history-gidocgen` — те саме, що `ghdocs-history` (усі його поля), і три заміни в кожному файлі `.md`
                            з raw.githubusercontent.com перед розбором:
                            - перший рядок «Title: Using > At the command-line» (так gi-docgen задає назву
                              й місце сторінки в змісті) стає заголовком «# Using: At the command-line»;
                            - блок `<refmeta>…</refmeta>` і `<refnamediv>…</refnamediv>` на початку файла
                              (так сторінку для gtk-doc підписували до переходу на gi-docgen) стає
                              заголовком з `<refentrytitle>` і рядком з `<refpurpose>`;
                            - посилання gi-docgen «[method@Image.thumbnail]», «[enum@Vips.Kernel.LANCZOS3]»
                              стають звичайними іменами («`Image.thumbnail()`», «`VIPS_KERNEL_LANCZOS3`»), а
                              рамка «::: note» — абзацом «Note:», як у читачі `ghcode-history-gtkdoc`.

Навіщо. Посібник libvips лежить у теці `doc` репозиторію. З лінії 8.17 сайт збирає gi-docgen: назва сторінки —
рядок «Title:», а не заголовок markdown, і посилання на функції записано у квадратних дужках з видом
(«[method@Image.resize]») — у корпусі це був би текст, якого ніхто не шукає. У лініях 8.5–8.16 ті самі сторінки
починаються блоком XML для gtk-doc: без заміни він лягав би сирою розміткою в перший абзац, а назвою документа
ставало б ім'я файла.

Чому обгортка, а не поле в `ghdocs-history`: перелік тегів, імена документів, версії й адреси сайту той читач
складає сам і звірений у десятках примірників. Тут лише текст файла міняється дорогою.
"""

import re
from urllib.parse import urlsplit

from engine.readers import register
from engine.readers.ghgtkdoc import _text
from engine.readers.ghhistory import ghdocs_history

_TITLE = re.compile(r"\A\s*Title:[ \t]*(.+)\n")
_REFHEAD = re.compile(r"\A\s*<refmeta>.*?</refmeta>\s*(?:<refnamediv>.*?</refnamediv>\s*)?", re.S)
_REFTITLE = re.compile(r"<refentrytitle>(.*?)</refentrytitle>", re.S)
_REFPURPOSE = re.compile(r"<refpurpose>(.*?)</refpurpose>", re.S)


def gidocgen_to_markdown(text: str) -> str:
    """Сторінка посібника → звичайний markdown."""
    text = text.replace("\r\n", "\n")
    head = []
    if m := _TITLE.match(text):
        head.append("# " + m.group(1).strip().replace(" > ", ": "))
        text = text[m.end():]
    elif m := _REFHEAD.match(text):
        title = _REFTITLE.search(m.group(0))
        purpose = _REFPURPOSE.search(m.group(0))
        if title:
            head.append("# " + " ".join(title.group(1).split()))
        if purpose:
            head.append(" ".join(purpose.group(1).split()) + ".")
        text = text[m.end():]
    body = _text(text.split("\n"), gtk=False)
    return "\n\n".join(head + [body]) + "\n"


class _GiDocgenCtx:
    """`ctx`, що віддає сторінки посібника з GitHub уже звичайним markdown; решта звернень — до справжнього."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        parts = urlsplit(url)
        if parts.netloc == "raw.githubusercontent.com" and parts.path.endswith(".md"):
            return gidocgen_to_markdown(text)
        return text


@register("ghdocs-history-gidocgen")
def ghdocs_history_gidocgen(source: dict, ctx) -> list:
    return ghdocs_history(source, _GiDocgenCtx(ctx))
