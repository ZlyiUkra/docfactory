"""Читач документації, що лежить у репозиторії як сторінки Kirby CMS: поля «Title:», «Text:» через «----».

`ghdocs-kirby` — те саме, що `ghdocs-history` (поля `url`, `tags`, `folders`, `recursive`, `extensions`,
                 `exclude`, `site`, `name_prefix` …), і одна різниця: файл `.txt` з raw.githubusercontent.com
                 перед розбором стає markdown. З полів сторінки береться `Text` — сам текст — і `Title` —
                 назва, коли текст не починається заголовком «#». Решта полів відкидається: `Description`
                 — опис для пошукових систем, що повторює перший абзац тексту іншими словами. Посилання
                 розмітки Kirby «(link: /plugins/svg-draw-js/ text: svg.draw.js)» стає звичайним
                 «[svg.draw.js](/plugins/svg-draw-js/)», а рядки з самим `<br>`, `<iframe>` чи кнопкою
                 GitHub знімаються.

Навіщо. Сайт svgjs.dev зібрано Kirby: кожна сторінка — тека з файлом `default.txt`, де поля стоять
підряд, розділені рядком «----» (`Title: Other Elements`, `----`, `Text:` і далі markdown). Без
перетворення ці рядки йшли б у текст першого розділу кожної сторінки, а рядок «----» під «Title:»
markdown читає як підкреслення заголовка: назвою сторінки ставало б «Title: Other Elements». Опис
сторінки (`Description: SVG.Element is the base prototype…`) стоїть наприкінці файла, після тексту, і
ліг би в останній розділ, до якого він не має стосунку.

Чому обгортка, а не поле в `ghdocs-history`: перелік тегів, імена документів, версії й адреси сайту
той читач складає сам і звірений у десятках примірників. Тут лише текст файла міняється дорогою:
об'єкт `ctx`, який він отримує, віддає сторінку Kirby вже як markdown.
"""

import re
from urllib.parse import urlsplit

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_SEP = re.compile(r"^----[ \t]*$", re.M)
_FIELD = re.compile(r"\s*([A-Za-z][\w-]*):[ \t]*(.*)\Z", re.S)
_LINK = re.compile(r"\(link:\s*(\S+)\s+text:\s*([^)]+?)\s*\)")
_NOISE = re.compile(r"^[ \t]*(?:<br\s*/?>|<iframe\b.*?</iframe>|<a class=\"github-button\".*?</a>)[ \t]*\n?",
                    re.M | re.I)


def kirby_to_markdown(text: str) -> str:
    """Сторінка Kirby → markdown; текст, у якому немає поля `Text`, повертається як був."""
    fields: dict = {}
    for chunk in _SEP.split(text.replace("\r\n", "\n")):
        m = _FIELD.match(chunk)
        if m:
            fields.setdefault(m.group(1).lower(), m.group(2).strip())
    if "text" not in fields:
        return text
    body = _NOISE.sub("", _LINK.sub(r"[\2](\1)", fields["text"])).strip()
    title = fields.get("title", "").strip()
    if not body.startswith("# ") and title:
        body = f"# {title}\n\n{body}"
    return body + "\n"


class _KirbyCtx:
    """`ctx`, що віддає сторінки Kirby з GitHub уже як markdown; решта звернень — до справжнього."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        parts = urlsplit(url)
        if parts.netloc == "raw.githubusercontent.com" and parts.path.endswith(".txt"):
            return kirby_to_markdown(text)
        return text


@register("ghdocs-kirby")
def ghdocs_kirby(source: dict, ctx) -> list:
    return ghdocs_history(source, _KirbyCtx(ctx))
