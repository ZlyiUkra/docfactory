"""Читачі документації PHP: архів посібника, вікі RFC і текстові журнали сирців.

`php-manual`  — `url`     — архів `php_manual_en.tar.gz` із сайту php.net;
                `page`    — початок адреси сторінки на сайті («…/manual/en/»);
                `exclude` — вирази імен файлів без `.html`, що не беруться.
`dokuwiki`    — `url`     — сторінка-зміст вікі в простому HTML («…/rfc?do=export_xhtmlbody»);
                `prefix`  — початок посилань на сторінки («/rfc/»);
                `exclude` — вирази імен сторінок, що не беруться.
`php-text`    — `url`     — префікс сирих файлів (https://raw.githubusercontent.com/php/php-src/);
                `tags`    — об'єкт «тег → версія», від найновішого;
                `files`   — імена файлів; файла, якого в тегу немає, просто не буде.

Навіщо окремі читачі. Посібник PHP лежить у DocBook зі сотнями підстановок, а php.net сам
публікує його зібраним: один архів на всі сторінки дає готові тексти за одне звернення,
без коментарів читачів і без обходу 12 тисяч адрес. Вікі на DokuWiki віддає тіло сторінки
запитом `do=export_xhtmlbody`, без меню, а зміст відрізняє наявну сторінку від порожньої
класом посилання. Файли `UPGRADING` і `NEWS` — звичайний текст зі своїми позначками
заголовків: без їхнього перетворення на markdown великий файл лишився б одним розділом.
"""

import hashlib
import io
import re
import tarfile
from urllib.parse import quote

from engine.readers import Item, _markup, register

_BODY = 'id="layout-content">'
_BODY_END = '<script type="text/javascript" src="search-combined.js"'
_REFNAME = re.compile(r'<h1 class="refname">(.*?)</h1>', re.S)
_PURPOSE = re.compile(r'<span class="dc-title">(.*?)</span></p>', re.S)
_HEAD = re.compile(r"<h[1-3]\b[^>]*>(.*?)</h[1-3]>", re.S)
_WIKI_H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S)


def _plain(html: str) -> str:
    return " ".join(_markup.html_body(html).lstrip("#").split())


# Сотні книг посібника мають сторінку з однаковою назвою: «Installation», «Requirements».
_GENERIC = {"Installing/Configuring", "Installation", "Predefined Constants", "Requirements",
            "Runtime Configuration", "Examples", "Resource Types", "Basic usage", "Introduction"}
_MIGRATION = re.compile(r"migration(\d)(\d+)\b")


def _manual_title(title: str, stem: str) -> str:
    """Назва, за якою сторінку можна знайти: глава міграції каже свою версію, а типова сторінка
    книги — свою книгу. Без цього «Backward Incompatible Changes» однакова в усіх версіях."""
    moved = _MIGRATION.match(stem)
    if moved:
        return f"Migrating to PHP {moved.group(1)}.{moved.group(2)}: {title}"
    if title in _GENERIC and "." in stem:
        return f"{stem.split('.', 1)[0]}: {title}"
    return title


def _manual_page(html: str, url: str, stamp: str) -> str:
    start = html.find(_BODY)
    if start < 0:
        raise SystemExit(f"{url}: у сторінці немає основного блока — документ не записую.")
    start += len(_BODY)
    stop = html.find(_BODY_END, start)
    part = html[start:stop if stop > 0 else len(html)]
    name, purpose = _REFNAME.search(part), _PURPOSE.search(part)
    if name and purpose:
        # Сторінка функції: одна назва «array_map» нічого не каже пошуку про призначення.
        title = f"{_plain(name.group(1))}: {_plain(purpose.group(1))}"
        part = part[name.end():]
    else:
        head = _HEAD.search(part)
        if not head:
            raise SystemExit(f"{url}: на сторінці немає заголовка — документ не записую.")
        title = _manual_title(_plain(head.group(1)), url.rsplit("/", 1)[-1][:-4])
        part = part[head.end():]
    body = _markup.html_body(part)
    _markup.require(title, body, url, min_chars=1)
    return _markup.document(title, url, stamp, body)


@register("php-manual")
def php_manual(source: dict, ctx) -> list[Item]:
    url, page = source["url"], source["page"]
    if not ctx.allowed(url):
        raise SystemExit(f"{source['id']}: адреса {url} поза білим списком.")
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    pages: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(ctx.bytes(url)), mode="r:gz") as tar:
        for member in tar:
            if not member.isfile() or not member.name.endswith(".html"):
                continue
            stem = member.name.rsplit("/", 1)[-1][:-5]
            if not any(r.search(stem) for r in exclude):
                pages[stem] = tar.extractfile(member).read()
    items, names = [], set()
    for stem in sorted(pages):
        name = _markup.slug(stem.replace(".", "-"))
        if name in names:
            name = f"{name}-{hashlib.sha1(stem.encode()).hexdigest()[:6]}"
        names.add(name)

        def make(stem=stem):
            return _manual_page(pages[stem].decode("utf-8", "replace"), f"{page}{stem}.php",
                                ctx.stamp)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items


@register("dokuwiki")
def dokuwiki(source: dict, ctx) -> list[Item]:
    url, prefix = source["url"], source["prefix"]
    site = re.match(r"https://[^/]+", url).group(0)
    tail = url.split("?", 1)[1]
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    # wikilink2 — посилання на сторінку, якої у вікі немає.
    found = re.findall(rf'href="{re.escape(prefix)}([^"#?]+)"\s+class="wikilink1"', ctx.text(url))
    items, names = [], set()
    for page in sorted(set(found)):
        if any(r.search(page) for r in exclude):
            continue
        name = _markup.slug(page.replace(":", "-"))
        if name in names:
            name = f"{name}-{hashlib.sha1(page.encode()).hexdigest()[:6]}"
        names.add(name)
        link = f"{site}{prefix}{page}"
        address = f"{link}?{tail}"
        if not ctx.allowed(address):
            continue

        def make(address=address, link=link, page=page):
            html = ctx.text(address)
            head = _WIKI_H1.search(html)
            title = _plain(head.group(1)) if head else page
            body = _markup.html_body(html[head.end():] if head else html)
            _markup.require(title, body, link, min_chars=1)
            return _markup.document(title, link, ctx.stamp, body)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items


_UP_HEAD = re.compile(r"^(\d+)\.\s+(\S.*)$")
_UP_SUB = re.compile(r"^-\s+([A-Z][\w /.+-]*):\s*$")
_NEWS_HEAD = re.compile(r"^(?:\?\?\s*\?\?\?|\d{1,2}\s+\w+\s*\.?,?\s*\d{4}),?\s*(?:PHP\s+|Version\s+)?(\d\S*.*)$")
_RULE = re.compile(r"^[=\-|_*]{5,}\s*$")


def text_to_markdown(text: str, kind: str) -> str:
    """Позначки заголовків стають заголовками markdown, решта лишається дослівно.
    Абзаци не переносяться: у цих файлах відступ несе вкладеність."""
    out = []
    for raw in text.replace("\r\n", "\n").split("\n"):
        line = raw.rstrip()
        if _RULE.match(line):
            continue
        if kind == "NEWS":
            head = _NEWS_HEAD.match(line)
            if head and not line.startswith((" ", "\t")):
                out += ["", f"## {line.strip()}", ""]
                continue
        else:
            head = _UP_HEAD.match(line)
            if head:
                out += ["", f"## {head.group(1)}. {head.group(2)}", ""]
                continue
        sub = _UP_SUB.match(line)
        if sub:
            out += ["", f"### {sub.group(1)}", ""]
            continue
        out.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


@register("php-text")
def php_text(source: dict, ctx) -> list[Item]:
    base = source["url"].rstrip("/") + "/"
    owner, repo = re.match(r"https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/$", base).groups()
    items = []
    for tag, version in source["tags"].items():
        for path in source["files"]:
            url = f"{base}{quote(tag)}/{path}"
            if not ctx.allowed(url):
                continue
            code, data = ctx.fetch(url)
            if code != "200" or not data.strip():
                continue
            digest = hashlib.sha1(data).hexdigest()[:8]
            name = f"{_markup.slug(path)}-{digest}"

            def make(url=url, tag=tag, path=path, version=version):
                body = text_to_markdown(ctx.text(url), path)
                title = f"PHP {version} {path}"
                link = f"https://github.com/{owner}/{repo}/blob/{quote(tag)}/{path}"
                _markup.require(title, body, url, min_chars=1)
                return _markup.document(title, link, ctx.stamp, body, version)

            items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                              make=make))
    return items
