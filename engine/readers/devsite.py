"""Читач сайтів на Google DevSite, що віддають сторінку markdown-ом за адресою з «.md.txt».

`devsite-md` — `url` — sitemap.xml сайту: індекс частин або сам перелік. Документом стає
               кожна адреса з нього, що лежить усередині поля `within` цього ж джерела,
               крім адрес із рядком запиту (`?hl=de` — переклад тієї ж сторінки) і тих, що
               підпадають під вирази `exclude`. Текст — markdown за адресою сторінки з
               «.md.txt». Необов'язкові поля: `label` — {префікс адреси: підпис}, назва
               таких сторінок стає «Підпис: назва (дата)», дата — з рядка «Published: …»
               (блог); `groups` — префікси адрес, де наступний сегмент шляху — курс: назва
               глави стає «Назва курсу: назва глави», а назва курсу береться з його
               сторінки-змісту. `version` — версія всіх документів джерела.

Навіщо. web.dev віддає кожну сторінку чистим markdown-ом, але здебільшого без назви:
статті й записи блогу починаються блоком авторів, а глави курсів — одразу текстом. Назва
є лише в <title> HTML-сторінки, тож для таких сторінок читач звертається вдруге. Сторінка-
зміст курсу назву має — заголовок першого рівня, і друге звернення там не потрібне.
Назва глави без курсу («Box Model», «Welcome») у видачі не каже, звідки вона.

Повний перелік сторінок є тільки в сайтмапі: сторінки «Articles» і «Blog» складають
перелік скриптом, і markdown-двійник у них порожній. Частини сайтмапа сервер віддає лише
стиснутими (без цього — 500), тож звернення за ними йдуть із `gzip`.

Що вирізається з тексту: рядок авторів (фото й посилання на профілі; у старих статтях —
лише ім'я й посилання X, GitHub, Homepage без фото), банер підписки на
розсилку, кнопки згортання на сторінці-змісті курсу разом із підписом «Article», посилання
«Read article» і «Go back», розділи «Test your knowledge» (тест наприкінці статті) і «Check
your understanding» (тест наприкінці глави курсу) — запитання, варіанти й «Correct!»/
«Incorrect» там злиті в суцільні рядки, — і примітка про те, хто тест склав. Рядок «Published: …, Last updated: …» лишається: дата — половина
відповіді на «чи це ще чинне».
"""

import datetime
import html
import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.sitemap import _LOC, _inside

_H1 = re.compile(r"\A\s*# (.+?)[ \t]*\n")
_HTML_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
_PUBLISHED = re.compile(r"^Published: ([A-Z][a-z]+ \d{1,2}, \d{4})", re.M)
_QUIZ = re.compile(r"^(#{2,3}) (?:Test your knowledge|Check your understanding)[ \t]*$", re.M)
_QUIZ_NOTE = re.compile(r"^✨ \*This quiz was generated .*\n?", re.M)
_AUTHORS = re.compile(r"^!\[[^\]]*\]\(https://web\.dev/images/authors/[^)]*\).*\n?", re.M)
_AUTHOR_PHOTO = re.compile(r"!\[[^\]]*\]\(https://web\.dev/images/authors/[^)]*\)")
_PROFILE = re.compile(r"\[(?:X|Twitter|GitHub|LinkedIn|Mastodon|Bluesky|Threads|Homepage|Website|Blog)\]"
                      r"\(https?://[^)\s]*\)")
_NAMES = re.compile(r"[\w '’&,()–—-]*")
_NEWSLETTER = re.compile(r"\[!\[Sign up for the web\.dev newsletter\.\]\([^)]*\)\]\([^)]*\)")
_TOGGLE = re.compile(r'^<button class="toggle[^"]*"[^>]*>.*?</button>.*\n?', re.M)
_NAV = re.compile(r"^(?:Go back|\[Read article\]\([^)]*\))[ \t]*\n?", re.M)


def _pages(source: dict, ctx) -> list[str]:
    """Адреси сторінок джерела в порядку сайтмапа. Індекс сайтмапа розгортається в
    частини; кожна частина після розбору звільняється — розпакованою вона важить 80 МБ."""
    within = source["within"]
    skip = [re.compile(x) for x in source.get("exclude") or []]
    locs = _LOC.findall(ctx.text(source["url"], gzip=True))
    parts = [u for u in locs if u.endswith(".xml")] or [source["url"]]
    pages: list[str] = []
    seen: set = set()
    for part in parts:
        found = locs if part == source["url"] else _LOC.findall(ctx.text(part, gzip=True))
        for loc in found:
            page = loc.rstrip("/")
            if ("?" in page or page in seen or not _inside(page, within)
                    or any(x.search(page) for x in skip) or not ctx.allowed(page + ".md.txt")):
                continue
            seen.add(page)
            pages.append(page)
        del found
    return pages


def _html_title(ctx, page: str) -> str:
    """Назва з <title>: «Box Model &nbsp;|&nbsp; Articles &nbsp;|&nbsp; web.dev» → «Box Model»."""
    m = _HTML_TITLE.search(ctx.text(page))
    return html.unescape(m.group(1).split("&nbsp;|&nbsp;")[0]).strip() if m else ""


def _published(text: str) -> str:
    m = _PUBLISHED.search(text)
    if not m:
        return ""
    try:
        return datetime.datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return ""


def _quiz_out(text: str) -> str:
    """Без розділу-тесту: від його заголовка до наступного заголовка того самого чи
    вищого рівня, а без такого — до кінця сторінки."""
    while (m := _QUIZ.search(text)):
        level = len(m.group(1))
        nxt = re.compile(rf"^#{{1,{level}}} ", re.M).search(text, m.end())
        text = text[:m.start()] + (text[nxt.start():] if nxt else "")
    return text


def _byline(line: str) -> bool:
    """Рядок авторів без фото: «Matt Gaunt [X](…) [Homepage](…)». Після профілів у ньому
    лишаються самі імена й посади — без крапок і решти речення, до чотирьох слів на профіль.
    Фото другого автора може стояти посеред рядка першого, без фото."""
    links = len(_PROFILE.findall(line))
    rest = _PROFILE.sub("", _AUTHOR_PHOTO.sub("", line)).strip()
    return (links > 0 and not line.startswith("|") and bool(_NAMES.fullmatch(rest))
            and len(rest.split()) <= 4 * links)


def _bylines_out(text: str) -> str:
    """Рядки авторів шукаються лише в шапці — до першого заголовка сторінки."""
    lines = text.split("\n")
    head = next((i for i, ln in enumerate(lines) if ln.startswith("#")), len(lines))
    return "\n".join(ln for i, ln in enumerate(lines) if i >= head or not _byline(ln))


def _clean(text: str) -> str:
    text = _quiz_out(text)
    for rx in (_QUIZ_NOTE, _AUTHORS, _TOGGLE, _NAV):
        text = rx.sub("", text)
    return _NEWSLETTER.sub("", _bylines_out(text))


@register("devsite-md")
def devsite_md(source: dict, ctx) -> list[Item]:
    if not source.get("within"):
        raise SystemExit(f"{source['id']}: читач devsite-md вимагає поле `within` — "
                         f"інакше сайтмап потягнув би весь сайт.")
    pages = _pages(source, ctx)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної дозволеної "
                         f"сторінки — розмітка змінилася або `within` не той.")
    labels = source.get("label") or {}
    groups = source.get("groups") or []
    version = source.get("version", "")
    titles: dict = {}

    def read(page: str) -> tuple[str, str]:
        """(назва, markdown без назви)."""
        md = page + ".md.txt"
        text = ctx.text(md).replace("\r\n", "\n")
        _markup.refuse_html(text, md)
        head = _H1.match(text)
        if head:
            return head.group(1).strip(), text[head.end():]
        return _html_title(ctx, page), text

    def course(page: str) -> str:
        for prefix in groups:
            rest = page[len(prefix):].split("/") if page.startswith(prefix) else []
            if len(rest) > 1:
                index = prefix + rest[0]
                if index not in titles:
                    titles[index] = read(index)[0]
                return titles[index]
        return ""

    items = []
    for page in pages:
        name = _markup.slug(urlsplit(page).path)

        def make(page=page):
            title, text = read(page)
            titles[page] = title
            text = _clean(text)
            body = _markup.markdown_body(text)
            _markup.require(title, body, page + ".md.txt")
            group = course(page)
            if group and group != title:
                title = f"{group}: {title}"
            for prefix, label in labels.items():
                if page.startswith(prefix):
                    day = _published(text)
                    title = f"{label}: {title}" + (f" ({day})" if day else "")
            return _markup.document(title, page, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
