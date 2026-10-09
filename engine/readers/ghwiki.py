"""Читач сторінки вікі GitHub: назва — ім'я сторінки, бо в самому тексті її немає.

`ghwiki-page` — одна сторінка вікі репозиторію. `url` — її сирий markdown
                (https://raw.githubusercontent.com/wiki/ВЛАСНИК/РЕПО/СТОРІНКА.md); у шапку
                документа лягає людська адреса https://github.com/ВЛАСНИК/РЕПО/wiki/СТОРІНКА.
                Необов'язкові: `label` — підпис перед назвою («node-argon2 wiki» →
                «node-argon2 wiki: Options»), `version` — версія документа.

Навіщо. GitHub показує назвою сторінки вікі її ім'я файла, де дефіси стають пробілами
(«Migrating-from-another-hash-function.md» → «Migrating from another hash function»), а сам
текст сторінки починається одразу абзацом, без «# заголовка». `mdfile` бере назву з шапки YAML
чи з першого заголовка і таку сторінку відхиляє як «без назви», хоча назва в неї є — у
адресі. Тут назва береться звідти ж, звідки її бере GitHub.

Підзаголовки вікі часто підкреслено («`hashLength`» і рядок «-----» під ним, setext). GitHub
показує їх заголовками, а поділ на розділи бачить лише «## …», тож вся сторінка Options лягла б
одним розділом. Такий заголовок переписується в «## …» (поза блоками коду): назва документа вже
стоїть у шапці, тож обидва рівні підкреслення стають другим рівнем.

Чому окремий модуль: спільні читачі вже звірено в готових примірниках, а новий домен додає
свого читача, не змінюючи спільного.
"""

import re
from urllib.parse import unquote, urlsplit

from engine.readers import Item, _markup, register

_RAW = re.compile(r"^/wiki/([^/]+)/([^/]+)/([^/]+)\.md$")
_UNDERLINE = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")
_FENCE = re.compile(r"^ {0,3}(```|~~~)")


def _atx(text: str) -> str:
    """Підкреслені заголовки (setext) — у «## …»; блоки коду не чіпаються."""
    out: list[str] = []
    fenced = False
    for line in text.split("\n"):
        if _FENCE.match(line):
            fenced = not fenced
        prev = out[-1] if out else ""
        if (not fenced and _UNDERLINE.match(line) and prev.strip()
                and not re.match(r"^ {0,3}([-*+>|#]|\d+[.)] |```|~~~)", prev)):
            out[-1] = "## " + prev.strip()
            continue
        out.append(line)
    return "\n".join(out)


@register("ghwiki-page")
def ghwiki_page(source: dict, ctx) -> list[Item]:
    url = source["url"]
    m = _RAW.match(urlsplit(url).path)
    if urlsplit(url).netloc != "raw.githubusercontent.com" or not m:
        raise SystemExit(f"{source['id']}: читач ghwiki-page чекає адресу "
                         f"https://raw.githubusercontent.com/wiki/ВЛАСНИК/РЕПО/СТОРІНКА.md.")
    owner, repo, leaf = m.groups()
    page = f"https://github.com/{owner}/{repo}/wiki/{leaf}"
    heading = unquote(leaf).replace("-", " ").strip()
    title = f"{source['label']}: {heading}" if source.get("label") else heading
    name = _markup.slug(urlsplit(page).path)

    def make():
        text = ctx.text(url).replace("\r\n", "\n")
        _markup.refuse_html(text, url)
        body = _markup.markdown_body(_atx(text))
        _markup.require(title, body, url, min_chars=1)
        return _markup.document(title, page, ctx.stamp, body, source.get("version", ""))

    return [Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make)]
