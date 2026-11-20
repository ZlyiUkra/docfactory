"""Читач сайту, що лежить у репозиторії сторінками системи woods: власні теги замість markdown.

`ghdocs-woods` — те саме, що `ghdocs-history` (поля `url`, `tags`, `folders`, `recursive`, `extensions`,
                 `exclude`, `site`, `path_title`, `name_prefix` …), і одна різниця: файл `.txt` з
                 raw.githubusercontent.com перед розбором стає markdown. Необов'язкове `woods_site` —
                 початок адреси сайту (`https://paperjs.org`), яким доповнюються посилання `<page "/…/" />`.

Навіщо. Сайт paperjs.org зібрано woods — системою авторів Paper.js: сторінка — тека з файлом
`tutorial.txt`, `page.txt` чи `example.txt`, а текст розмічено тегами, яких markdown не знає:
`<title>Circle Shaped Paths</title>` — заголовок розділу, `<api Path.Circle(center,radius) />` —
посилання на довідник, `<paperscript height=140>…</paperscript>` — приклад, що запускається на сторінці,
`<note>`, `<tip>`, `<page "/tutorials/…/" />`, `<url "…">`, `<code>`. Без перетворення сторінка лишалася б
одним розділом без заголовків, приклади коду зливалися б з текстом, а на місці кожного посилання на довідник
стояла б розмітка тегу.

Що з чого стає: `<title>` — заголовок «##»; `<paperscript>` і багаторядковий `<code>` — блок коду; `<code>`
в один рядок, короткий запис `<code x />` і `<api …>` — код у рядку (`<api Item#position />` — «item.position», як показує сайт);
`<note>`, `<warning>`, `<tip>` — абзац з підписом сайту («Please note:», «Warning:», «Did you know?»);
`<page>` і `<url>` — посилання markdown; `<image>`, `<hide>` і `<nop>` знімаються; `<html>…</html>` (сирий HTML сторінки) — блок коду; `<b>`, `<i>`, `<em>`
стають зірочками. Шапка між рядками `---` (головна сторінка) відкидається.

Чому обгортка, а не поле в `ghdocs-history`: перелік тегів, імена документів, версії й адреси сайту той
читач складає сам і звірений у десятках примірників. Тут лише текст файла міняється дорогою: об'єкт `ctx`,
який він отримує, віддає сторінку woods уже як markdown.
"""

import re
from urllib.parse import urlsplit

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_FRONT = re.compile(r"\A---\n.*?\n---\n", re.S)
_SCRIPT = re.compile(r"<paperscript\b[^>]*>\n?(.*?)\n?[ \t]*</paperscript>", re.S)
_CODE = re.compile(r"<code\b([^>]*?)(?:/>|>(.*?)</code>)", re.S)
_RAW_HTML = re.compile(r"<html>\n?(.*?)\n?</html>", re.S)
_TITLE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.S)
_API = re.compile(r"<api\s+([^>]*?)\s*(?:/>|>(.*?)</api>)", re.S)
_NOTE = re.compile(r"<(note|warning|tip)\b[^>]*>(.*?)</\1>", re.S)
_PAGE = re.compile(r"<page\s+\"?([^\">\s]+)\"?[^>]*?(?:/>|>(.*?)</page>)", re.S)
_URL = re.compile(r"<url\s+\"?([^\">\s]+)\"?[^>]*?(?:/>|>(.*?)</url>)", re.S)
_DROP = re.compile(r"<(hide|nop)\b[^>]*>.*?</\1>|<(?:image|img|nop|template)\b[^>]*/>", re.S)
_IMAGE = re.compile(r"<(image|img)\b[^>]*>(.*?)</\1>", re.S)
_BOLD = re.compile(r"</?b>")
_ITALIC = re.compile(r"</?(?:i|em)>")
_WRAP = re.compile(r"</?(?:block|column)\b[^>]*>")
_NOTES = {"note": "Please note:", "warning": "Warning:", "tip": "Did you know?"}


def _api_name(ref: str) -> str:
    """Як сайт показує посилання на довідник: `Item#position` — «item.position», решта — як написано."""
    cls, sep, member = ref.partition("#")
    if sep and cls:
        return f"{cls[0].lower()}{cls[1:]}.{member}"
    return ref


def _page_title(href: str) -> str:
    leaf = href.strip("/").rsplit("/", 1)[-1]
    return leaf.replace("-", " ").strip().capitalize() or href


def woods_to_markdown(text: str, site: str = "") -> str:
    """Сторінка woods → markdown."""
    text = _FRONT.sub("", text.replace("\r\n", "\n"), count=1)
    kept: list[str] = []

    def keep(block: str) -> str:
        kept.append(block)
        return f"\x00{len(kept) - 1}\x00"

    def script(m):
        return keep(f"\n\n```js\n{m.group(1).strip(chr(10))}\n```\n\n")

    def code(m):
        attrs, body = m.group(1).strip(), m.group(2)
        if body is None:
            # `<code x />` — короткий запис коду в рядку: значення стоїть на місці атрибута.
            return keep(f"`{attrs}`")
        if "\n" in body.strip():
            lang = "html" if "html" in attrs else ""
            return keep(f"\n\n```{lang}\n{body.strip(chr(10))}\n```\n\n")
        return keep(f"`{body.strip()}`")

    text = _SCRIPT.sub(script, text)
    text = _CODE.sub(code, text)
    # `<html>…</html>` у woods — сирий HTML сторінки (підключення допоміжного скрипта перед прикладом).
    text = _RAW_HTML.sub(lambda m: keep(f"\n\n```html\n{m.group(1).strip(chr(10))}\n```\n\n"), text)
    text = _DROP.sub("", text)
    text = _IMAGE.sub(lambda m: m.group(2).strip(), text)
    text = _WRAP.sub("", text)
    text = _TITLE.sub(lambda m: f"\n\n## {' '.join(m.group(1).split())}\n\n", text)
    text = _API.sub(lambda m: keep(f"`{(m.group(2) or _api_name(m.group(1))).strip()}`"), text)
    text = _PAGE.sub(lambda m: f"[{(m.group(2) or _page_title(m.group(1))).strip()}]"
                               f"({site if m.group(1).startswith('/') else ''}{m.group(1)})", text)
    text = _URL.sub(lambda m: f"[{(m.group(2) or m.group(1)).strip()}]({m.group(1)})", text)
    text = _NOTE.sub(lambda m: f"\n\n**{_NOTES[m.group(1)]}** {m.group(2).strip()}\n\n", text)
    text = _ITALIC.sub("*", _BOLD.sub("**", text))
    text = re.sub(r"\x00(\d+)\x00", lambda m: kept[int(m.group(1))], text)
    # Самотній закривний тег, що лишився від помилки розмітки («</code>» без пари), — не текст.
    text = re.sub(r"^[ \t]*</(?:code|paperscript|note|title)>[ \t]*\n", "", text, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


class _WoodsCtx:
    """`ctx`, що віддає сторінки woods з GitHub уже як markdown; решта звернень — до справжнього."""

    def __init__(self, ctx, site: str):
        self._ctx = ctx
        self._site = site

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        parts = urlsplit(url)
        if parts.netloc == "raw.githubusercontent.com" and parts.path.endswith(".txt"):
            return woods_to_markdown(text, self._site)
        return text


@register("ghdocs-woods")
def ghdocs_woods(source: dict, ctx) -> list:
    return ghdocs_history(source, _WoodsCtx(ctx, str(source.get("woods_site") or "").rstrip("/")))
