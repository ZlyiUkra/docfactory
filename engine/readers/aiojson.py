"""Читач сайтів на застосунку документації Angular (aio): текст сторінки лежить готовим JSON.

`aio-json` — сайт, зібраний генератором документації Angular (rxjs.dev, v6.rxjs.dev). Поля:
             `url`     — каталог `generated/` сайту (`https://rxjs.dev/generated/`): звідти беруться
                         `navigation.json`, `docs/api/api-list.json` і `docs/<сторінка>.json`;
             `site`    — адреса самого сайту (`https://rxjs.dev/`): її читач ставить у шапку
                         документа замість адреси JSON, щоб цитата вела на сторінку для людей;
             `version` — версія всіх документів джерела (сайт тримає лише одну);
             `exclude` — вирази адрес сторінок, що не беруться (оболонки без тексту: «team»,
                         «operator-decision-tree», список API, який малює браузер);
             `pages`   — адреси, яких немає ні в навігації, ні в списку API;
             `inline_titles` — вираз назви заголовка, що стає підписом усередині розділу: довідник
                         API пише «Parameters» і «Returns» під кожним перевантаженням, і без цього
                         вони ставали б розділами з одного рядка («`OperatorFunction<T, R>`»);
             `min_chars` — межа довжини тіла, нижче якої сторінка — не документ: сторінки псевдонімів
                         типів і констант справді куці.

Навіщо. rxjs.dev — односторінковий застосунок: HTML, який віддає сервер, це порожня оболонка на
вісім кілобайтів, мапи сайту немає, а текст кожної сторінки завантажується окремим JSON (`id`,
`title`, `contents` — готовий HTML статті). Читачі HTML такої оболонки не бачать. Перелік сторінок —
це дерево бічного меню (`navigation.json`) плюс список довідника API (`api-list.json`: триста з
гаком класів, функцій і операторів, яких меню не називає).

Розмітка статті — звичайна, крім одного власного елемента: приклади коду там `<code-example
language="ts">…</code-example>` з посиланнями `<a class="code-anchor">` на інші сторінки всередині
коду. Спільний розбір HTML знає лише `<pre>`, і приклад злипся б у один рядок: тому елемент
переписується в `<pre class="language-ts">`. Службове — кнопки «правити»/«джерело», якорі заголовків
(іконка з текстом `link` ставала б частиною назви розділу: «maplink»), зміст сторінки, сам заголовок
`<h1>` (назва йде в шапку документа) — знімається.
"""

import json
import re

from engine.readers import Item, _markup, register

_ABSOLUTE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
_H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S)
_HEADING = re.compile(r"<(h[2-6])\b[^>]*>(.*?)</\1>", re.S)
_CODE = re.compile(r"<code-example\b([^>]*)>(.*?)</code-example>", re.S)
_LANG = re.compile(r'\blanguage="([\w+#-]+)"')
_DROP = (
    re.compile(r'<div class="page-actions">.*?</div>', re.S),
    re.compile(r'<a\b[^>]*class="header-link"[^>]*>.*?</a>', re.S),
    re.compile(r"<aio-toc\b[^>]*>.*?</aio-toc>", re.S),
)


def _menu(nodes, out: dict) -> None:
    """Адреса → назва зі сторінок дерева меню; зовнішні посилання (інші версії сайту)
    пропускаються. Назва з меню — запасна: сторінки v6 віддають `title` порожнім і без `<h1>`."""
    for node in nodes or ():
        url = (node.get("url") or "").split("#")[0].split("?")[0].strip("/")
        if url and not _ABSOLUTE.match(url):
            out.setdefault(url, (node.get("title") or "").strip())
        _menu(node.get("children"), out)


def _code(m) -> str:
    lang = _LANG.search(m.group(1))
    return f'<pre class="language-{lang.group(1) if lang else ""}">{m.group(2).strip(chr(10))}</pre>'


def _document(raw: str, page: str, cite: str, stamp: str, version: str, inline=None,
              min_chars: int = _markup.MIN_BODY, fallback: str = "") -> str:
    try:
        data = json.loads(raw)
    except ValueError:
        raise SystemExit(f"{page}: замість JSON прийшло інше (сторінка помилки чи оболонка сайту) — "
                         f"документ не записую.")
    html = data.get("contents") or ""
    title = (data.get("title") or "").strip()
    if not title:
        m = _H1.search(html)
        title = _markup.html_body(m.group(1)).strip().lstrip("#").strip() if m else ""
    title = title or fallback
    for rx in _DROP:
        html = rx.sub("", html)
    html = _H1.sub("", html, count=1)
    if inline:
        html = _HEADING.sub(lambda h: f"<p><strong>{h.group(2)}</strong></p>"
                            if inline.fullmatch(_markup.html_body(h.group(2)).strip())
                            else h.group(0), html)
    body = _markup.html_body(_CODE.sub(_code, html))
    _markup.require(title, body, page, min_chars)
    return _markup.document(title, cite, stamp, body, version)


@register("aio-json")
def aio_json(source: dict, ctx) -> list[Item]:
    base = source["url"].rstrip("/") + "/"
    site = (source.get("site") or "").rstrip("/") + "/"
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    inline = re.compile(source["inline_titles"]) if source.get("inline_titles") else None
    min_chars = source.get("min_chars", _markup.MIN_BODY)
    paths: dict[str, str] = {}
    nav = json.loads(ctx.text(base + "navigation.json"))
    for key in ("TopBar", "SideNav"):
        _menu(nav.get(key), paths)
    for section in json.loads(ctx.text(base + "docs/api/api-list.json")):
        for i in section.get("items") or ():
            if i.get("path"):
                paths.setdefault(i["path"], (i.get("title") or "").strip())
    for p in source.get("pages") or ():
        paths.setdefault(p.strip("/"), "")
    if len(paths) < 10:
        raise SystemExit(f"{source['id']}: у навігації {base} знайдено лише {len(paths)} сторінок — "
                         f"розмітка меню змінилася.")

    items: list[Item] = []
    names: set[str] = set()
    for path, menu_title in paths.items():
        name = _markup.slug(path)
        if name in names or any(r.search(path) for r in exclude):
            continue
        page = f"{base}docs/{path}.json"
        if not ctx.allowed(page):
            raise SystemExit(f"{source['id']}: {page} поза білим списком — допишіть каталог у `within`.")
        names.add(name)

        def make(page=page, path=path, menu_title=menu_title):
            return _document(ctx.text(page), page, site + path, ctx.stamp,
                             source.get("version", ""), inline, min_chars, menu_title)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    return items
