"""Розмітка сайту json-schema.org → текст (поле `jsonschema_org` читача `ghdocs-history`).

Сторінки сайту — markdown у теці `pages/` репозиторію json-schema-org/website, але з власними
вставками, які сайт малює компонентами:

- `<Star label="New in draft 6" />` і `<StarInline label="…"/>` — з якого випуску є ключове слово.
  Саме ця позначка відповідає на «а в draft-07 це вже було?», тож вона лишається рядком тексту;
- `<Infobox label="Draft-specific info">`, `<Warning>`, `<Danger>`, `<Tip>` — виноски з підписом;
- `[tabs-start "Language-specific info"]`, `[tab "Python"]`, `[tabs-end]` — вкладки. Без підписів
  пояснення для Python, Ruby і «Draft 4» злилися б в один абзац;
- перший рядок блоку коду `// props { "isSchema": true }` чи `{ "valid": false }` — сайт підписує
  ним приклад: схема, правильний чи неправильний екземпляр. Без підпису модель не відрізнила б
  приклад, що проходить перевірку, від прикладу, що її провалює;
- `<Keywords label="…" />` — записи покажчика ключових слів, тексту не несуть;
- `\\"keys\\"`, `don\\'t` — лапки, екрановані ще при перенесенні книги з reStructuredText. Сайт
  показує їх без зворотної риски, а в тексті вона заважала б шукати й цитувати.

Код не чіпається, крім рядка `// props` на початку блоку: компоненти-дженерики (`<T>`,
`<TKey, TValue>`) у прикладах лишаються як є.
"""

import json
import re

_FENCE = re.compile(r"^\s*(```|~~~)")
_PROPS = re.compile(r"^\s*//\s*props\s*(\{.*\})\s*$")
_KEYWORDS = re.compile(r"<Keywords\b[^>]*/>")
_STAR_INLINE = re.compile(r'<StarInline\s+label=\s*"([^"]*)"\s*/>\s*')
_STAR = re.compile(r'<Star\s+label=\s*"([^"]*)"\s*/>')
_BOX = re.compile(r'<(Infobox|InfoBox|Warning|Danger|Tip)\b(?:\s+label=\s*"([^"]*)")?\s*>\s*')
_BOX_END = re.compile(r"\s*</(?:Infobox|InfoBox|Warning|Danger|Tip|Bigquote|Regularquote)>")
_QUOTE = re.compile(r"<(?:Bigquote|Regularquote)>\s*")
_TABS = re.compile(r'^\s*\[tabs?(?:-start)?\s+"([^"]*)"\]\s*$')
_TABS_END = re.compile(r"^\s*\[tabs-end\]\s*$")
_ESCAPED_QUOTE = re.compile(r"""\\(["'])""")
# Одинокий «:::» — залишок виноски, якої сайт не малює (structuring.md).
_STRAY = re.compile(r"^\s*:::\s*$")
_DEFAULT = {"Infobox": "Note", "InfoBox": "Note", "Warning": "Warning", "Danger": "Danger",
            "Tip": "Tip"}


def _caption(props: str) -> str:
    """Підпис прикладу з `// props {…}`; порожній — коли властивості нічого не кажуть."""
    try:
        p = json.loads(props)
    except ValueError:
        return ""
    if not isinstance(p, dict):
        return ""
    if p.get("caption"):
        return str(p["caption"]).rstrip(".") + ":"
    if p.get("isSchema"):
        return "Schema:"
    if "valid" in p:
        return "Valid instance:" if p["valid"] else "Invalid instance:"
    return ""


def _line(line: str) -> str:
    line = _ESCAPED_QUOTE.sub(r"\1", _KEYWORDS.sub("", line))
    line = _STAR_INLINE.sub(lambda m: f"{m.group(1)}: ", line)
    line = _STAR.sub(lambda m: f"\n{m.group(1)}.\n", line)
    line = _BOX.sub(lambda m: f"\n{m.group(2) or _DEFAULT[m.group(1)]}: ", line)
    line = _BOX_END.sub("\n", line)
    line = _QUOTE.sub("", line)
    if m := _TABS.match(line):
        return f"\n{m.group(1)}:\n"
    if _TABS_END.match(line) or _STRAY.match(line):
        return ""
    return line


def expand(text: str) -> str:
    out: list[str] = []
    fence, opened = False, None
    for line in text.split("\n"):
        if _FENCE.match(line):
            fence = not fence
            opened = len(out) if fence else None
            out.append(line)
            continue
        if fence:
            if opened is not None and len(out) == opened + 1 and (m := _PROPS.match(line)):
                caption = _caption(m.group(1))
                if caption:
                    out[opened:opened] = ["", caption, ""]
                opened = None
                continue
            opened = None
            out.append(line)
            continue
        out.append(_line(line))
    return "\n".join(out)
