"""Читач сайту, чий перелік сторінок не віддається зовсім: сторінки знаходяться обходом
посилань між їхніми markdown-двійниками.

`mdcrawl` — `url` — markdown-двійник першої сторінки (адреса з «.md»); `pages` —
            ще адреси сторінок (без «.md»), з яких обхід теж починається; `within` —
            обов'язкове: префікси адрес «.md», куди обходу можна. Кожна сторінка,
            знайдена так, стає документом; текст — її markdown-двійник.
            Необов'язкові: `root` — початок шляху, що знімається з імені документа
            (`/developers/docs/`); `hosts` — інші початки адрес того самого сайту
            (`https://contentful.com/`), що в посиланнях замінюються початком `url`;
            `not_found` — перший рядок сторінки-заглушки, яку сайт віддає з кодом 200
            на неіснуючу адресу: така сторінка не документ, але посилання з неї
            («Similar pages») обходяться; `lead_quote: true` — блок цитат перед першим
            рядком тексту (службова шапка «> For clean Markdown of any page…»)
            знімається; `max_pages` — стеля обходу (типово 5000).

Навіщо. contentful.com/developers/docs стоїть за перевіркою Vercel: llms.txt, sitemap.xml
і самі сторінки відповідають 429 «This request requires a challenge», і пропускаються
лише markdown-двійники сторінок документації. Переліку сторінок, отже, немає ніде, крім
посилань у самих двійниках. Обхід бере лише адреси всередині `within`, тож принцип
білого списку той самий: поза оголошеними префіксами не йде жодне звернення.

Сторінка без заголовка «# …» (вступ до розділу довідника API починається одразу текстом і
«## Space») дістає назву з останньої частини шляху — інакше назвою став би перший
підрозділ. Однаковий текст за різними адресами (стара адреса, переведена на нову, чи адреса
підрозділу, яку сайт розв'язує як сторінку-батька) дає один документ; його адреса
обирається за назвою сторінки (див. `_canon`).

Обхід іде вже на кроці переліку: інакше переліку немає. Зі сховищем сирого кожна сторінка
питається раз за прогін, тож документи потім будуються зі збереженого, а крок build
обходить те саме без мережі.
"""

import hashlib
import re
from collections import deque
from urllib.parse import urlsplit

from engine import net
from engine.readers import Item, _markup, register

_LINK = re.compile(r"\]\(((?:https://[^)\s#?]+)|(?:/[^)\s#?]*))[^)]*\)")
_HEADING = re.compile(r"^#\s+(.+?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(```+|~~~+)")


def _origin(url: str) -> str:
    s = urlsplit(url)
    return f"{s.scheme}://{s.netloc}"


def _page_of(link: str, origin: str, hosts: list) -> str:
    """Адреса сторінки з посилання: абсолютна, без «.md», «/» у кінці й чужого
    початку того самого сайту."""
    if link.startswith("/"):
        link = origin + link
    for host in hosts:
        if link.startswith(host):
            link = origin + "/" + link[len(host):].lstrip("/")
    link = link.rstrip("/")
    return link[:-3] if link.endswith(".md") else link


def _inside(url: str, within: list) -> bool:
    return any(url.startswith(w) if w.endswith("/") else url == w for w in within)


def _strip_lead(text: str) -> str:
    """Без блоку цитат і порожніх рядків на початку сторінки."""
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith(">")):
        i += 1
    return "\n".join(lines[i:])


def _title(text: str, page: str, root: str) -> tuple[str, str]:
    """(назва, текст без неї): перший рядок «# …», якщо він іде першим після шапки;
    інакше — остання частина шляху («content-delivery-api» → «Content delivery api»)."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        m = _HEADING.match(line)
        if m and not _FENCE.match(line):
            return m.group(1).strip(), "\n".join(lines[i + 1:])
        break
    tail = urlsplit(page).path.rstrip("/").rsplit("/", 1)[-1] or root.strip("/")
    words = tail.replace("-", " ").strip()
    return (words[:1].upper() + words[1:]), text


def _canon(page: str, body: str, root: str) -> tuple:
    """Ключ вибору адреси для тексту, який сайт віддає за кількома адресами: менший —
    кращий. Сайт розв'язує адресу підрозділу як сторінку-батька, і вся сторінка
    «Search parameters» приходить і за «…/full-text-search-on-a-field», а «API basics» —
    і за «concepts/apis». Перевага — адресі, чия остання частина збігається з назвою
    сторінки, далі — коротшому шляху й коротшій останній частині; інакше документ
    діставав би ім'я й посилання тієї адреси, яку обхід зустрів першою."""
    title, _ = _title(body, page, root)
    path = urlsplit(page).path.rstrip("/")
    tail = path.rsplit("/", 1)[-1]
    return (tail != _markup.slug(title), path.count("/"), len(tail), path)


@register("mdcrawl")
def mdcrawl(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач mdcrawl вимагає поле `within` — "
                         f"інакше обхід пішов би всім сайтом.")
    origin = _origin(source["url"])
    hosts = [h.rstrip("/") + "/" for h in source.get("hosts", [])]
    root = source.get("root", "")
    stub = source.get("not_found", "")
    lead = bool(source.get("lead_quote"))
    cap = int(source.get("max_pages", 5000))

    first = _page_of(source["url"], origin, hosts)
    queue = deque([first] + [_page_of(p, origin, hosts) for p in source.get("pages", [])])
    seen = set(queue)
    pages: list[str] = []
    texts: dict = {}
    stubs = 0
    failed: list[str] = []
    while queue and len(pages) + stubs + len(failed) < cap:
        page = queue.popleft()
        md = page + ".md"
        if not (_inside(md, within) and ctx.allowed(md)):
            continue
        try:
            code, data = ctx.fetch(md)
        except net.Refused:
            # Редирект за межі оголошення (стара адреса, переведена на Help Center):
            # туди обходу не можна, а сама адреса документом не є.
            code, data = "refused", b""
        if code != "200":
            failed.append(f"{md} ({code})")
            continue
        text = data.decode("utf-8", errors="replace")
        for link in _LINK.findall(text):
            nxt = _page_of(link, origin, hosts)
            if nxt not in seen and _inside(nxt + ".md", within):
                seen.add(nxt)
                queue.append(nxt)
        body = _strip_lead(text) if lead else text
        if stub and body.lstrip().startswith(stub):
            stubs += 1
            continue
        digest = hashlib.sha1(body.encode("utf-8")).hexdigest()
        if digest in texts:
            at = texts[digest]
            if _canon(page, body, root) < _canon(pages[at], body, root):
                pages[at] = page
            continue
        texts[digest] = len(pages)
        pages.append(page)
    print(f"  {source['id']}: обхід — {len(pages)} сторінок, заглушок {stubs}, "
          f"збоїв {len(failed)}, у черзі лишилося {len(queue)}", flush=True)
    for line in failed[:20]:
        print(f"    збій: {line}", flush=True)
    if not pages:
        raise SystemExit(f"{source['id']}: обхід від {source['url']} не дав жодної "
                         f"сторінки — сайт змінився або `within` не той.")

    items = []
    for page in pages:
        path = urlsplit(page).path
        name = _markup.slug(path[len(root):] if root and path.startswith(root) else path)

        def make(page=page):
            md = page + ".md"
            text = ctx.text(md)
            _markup.refuse_html(text, md)
            if lead:
                text = _strip_lead(text)
            title, rest = _title(text, page, root)
            body = _markup.markdown_body(rest)
            _markup.require(title, body, md, min_chars=1)
            return _markup.document(title, page, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
