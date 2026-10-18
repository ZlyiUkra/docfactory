"""Читач історії документації, де частина сторінок — зошити Jupyter (`.ipynb`).

`ghdocs-history-ipynb` — те саме, що `ghdocs-history` (усі його поля), плюс файл `.ipynb`
                         перед розбором стає markdown-ом: клітинки markdown — як є, клітинки
                         коду — блоками коду мови зошита, а з виводу лишається тільки текст
                         (потік і `text/plain`), обрізаний до `output_chars` знаків (типово
                         1500). Картинки, HTML і віджети виводу відкидаються. `extensions`
                         треба вказати з `.ipynb`, інакше зошити не потраплять у перелік.

Навіщо. Рецепти claude-cookbooks — зошити: пояснення в клітинках markdown, код — у клітинках
коду, а результат запуску — у виводі. Сирий JSON зошита розбирач markdown не прочитає, а в
22 МБ зошитів більша частина — картинки base64 і HTML у виводі, яким у корпусі не місце.

Чому окремий модуль, а не поле в `ghdocs-history`: примірники з тим читачем зібрані й
звірені; розбір той самий — його й викликано, а перетворення робить обгортка контексту.
"""

import json
import re

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_RAW_NOTEBOOK = re.compile(r"^https://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/.+\.ipynb$")
# Кольори терміналу у виводі (`[32mINFO[0m`) — не текст.
_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def _joined(value) -> str:
    return "".join(value) if isinstance(value, list) else (value or "")


def _fence(text: str) -> str:
    """Огорожа, довша за будь-яку послідовність «`» усередині тексту."""
    longest = max((len(m) for m in re.findall(r"`{3,}", text)), default=2)
    return "`" * max(3, longest + 1)


def _notebook(raw: str, limit: int) -> str:
    nb = json.loads(raw)
    lang = (nb.get("metadata", {}).get("kernelspec", {}).get("language")
            or nb.get("metadata", {}).get("language_info", {}).get("name") or "python")
    parts: list[str] = []
    for cell in nb.get("cells", []):
        source = _joined(cell.get("source")).strip("\n")
        kind = cell.get("cell_type")
        if kind == "markdown":
            if source.strip():
                parts.append(source)
        elif kind == "code":
            if source.strip():
                fence = _fence(source)
                parts.append(f"{fence}{lang}\n{source}\n{fence}")
            out = []
            for o in cell.get("outputs", []):
                if o.get("output_type") == "stream":
                    out.append(_joined(o.get("text")))
                elif o.get("output_type") in ("execute_result", "display_data"):
                    out.append(_joined(o.get("data", {}).get("text/plain")))
                elif o.get("output_type") == "error":
                    out.append(f"{o.get('ename', '')}: {o.get('evalue', '')}")
            text = _ANSI.sub("", "".join(x if x.endswith("\n") else x + "\n"
                                         for x in out if x.strip())).strip("\n")
            if text:
                if len(text) > limit:
                    text = text[:limit].rstrip() + "\n…"
                fence = _fence(text)
                parts.append(f"Output:\n\n{fence}text\n{text}\n{fence}")
        elif kind == "raw" and source.strip():
            parts.append(source)
    return "\n\n".join(parts) + "\n"


class _Notebooks:
    """Обгортка контексту: зошити віддає вже markdown-ом, усе інше — як є."""

    def __init__(self, ctx, limit: int):
        self._ctx, self._limit = ctx, limit

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, gzip: bool = False, accept: str = "") -> str:
        text = self._ctx.text(url, gzip, accept)
        return _notebook(text, self._limit) if _RAW_NOTEBOOK.match(url) else text


@register("ghdocs-history-ipynb")
def ghdocs_history_ipynb(source: dict, ctx) -> list:
    return ghdocs_history(source, _Notebooks(ctx, int(source.get("output_chars", 1500))))
