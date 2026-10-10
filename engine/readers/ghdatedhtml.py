"""Читач історії зібраного сайту без тегів: знімок HTML-сторінок гілки на кожну версію npm.

`ghsite-dated-html` — те саме, що `ghsite-dated` (поля `versions`, `only`, `eras` з `repo`,
                      `branch`, `before`, `include`, `exclude`, `strip`), але сторінки — файли
                      `.html` зібраного сайту, а не markdown чи код. Необов'язкові поля:
                      `start` — вирази в порядку переваги: текст сторінки починається з
                      першого збігу першого виразу, що знайшовся (типово `<body`), — шапка з
                      меню стоїть раніше; `end` — вирази, на найранішому збігу яких текст
                      закінчується (типово `<footer`).

Навіщо. Сайт i18next 1.x жив на гілці gh-pages репозиторію бібліотеки, і за чотири роки
джерело сторінок мінялося двічі: спершу один markdown, з якого збиралася одна сторінка,
потім шаблони Jade, з яких збиралися сторінки документації браузерної версії й версії для
Node.js. Спільне в усіх епохах гілки — лише зібраний HTML, що лежить поруч із джерелами: саме
його й показував сайт. `ghsite-dated` бере тільки markdown і код, а HTML відкидає як помилку
адреси.

Мить знімка, лінії й версії документа — ті самі, що в `ghsite-dated` (функції звідти), тож
обидва читачі разом описують сайт однаково в усіх епохах. Документ — неповторна пара «шлях,
вміст» (хеш blob із дерева), у версії лягають усі версії, у знімку яких сторінка була саме
такою.

Назва документа — останній `<title>` сторінки: `<h1>` на сторінках документації 1.x немає, а
заголовок-герой («Documentation:») однаковий на всіх; деякі сторінки мають два `<title>`, і
точніший з них — другий.
"""

import json
import re
import time
from urllib.parse import quote

from engine.readers import Item, _markup, register
from engine.readers.ghdated import _at, _chain, _moments

_TITLE = re.compile(r"<title>(.*?)</title>", re.S | re.I)


@register("ghsite-dated-html")
def ghsite_dated_html(source: dict, ctx) -> list[Item]:
    eras = source.get("eras")
    if not isinstance(eras, list) or not eras:
        raise SystemExit(f"{source['id']}: читач ghsite-dated-html потребує поля eras.")
    try:
        packument = json.loads(ctx.text(source["versions"]))
    except ValueError as exc:
        raise SystemExit(f"{source['versions']}: відповідь не JSON ({exc}).")
    if source.get("only"):
        only = re.compile(source["only"])
        packument["versions"] = {v: m for v, m in (packument.get("versions") or {}).items()
                                 if only.search(v)}
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    moments = _moments(packument, now)
    times = packument["time"]
    starts = [re.compile(r) for r in source.get("start") or [r"<body\b"]]
    ends = [re.compile(r) for r in source.get("end") or [r"<footer\b"]]

    def key(era: dict) -> tuple:
        return era["repo"], era.get("branch", "master")

    chains = {key(e): _chain(ctx, e["repo"], e.get("branch", "master"), e.get("before", ""))
              for e in eras}
    trees: dict = {}

    def tree(era: dict, sha: str) -> list:
        k = (era["repo"], sha)
        if k not in trees:
            url = f"https://api.github.com/repos/{era['repo']}/git/trees/{sha}?recursive=1"
            try:
                data = json.loads(ctx.text(url))
            except ValueError as exc:
                raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
            if data.get("truncated"):
                raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
            inc = [re.compile(r) for r in era.get("include") or [r"."]]
            exc_ = [re.compile(r) for r in era.get("exclude") or []]
            trees[k] = [(e["path"], e["sha"]) for e in data.get("tree") or []
                        if e.get("type") == "blob" and e.get("size")
                        and e.get("path", "").endswith(".html")
                        and any(r.search(e["path"]) for r in inc)
                        and not any(r.search(e["path"]) for r in exc_)]
        return trees[k]

    # (репо, шлях, blob) → [найновіший sha, версії], від найновішої версії.
    seen: dict = {}
    for v in sorted(moments, key=lambda v: times[v], reverse=True):
        at = moments[v]
        era = next((e for e in eras if not e.get("before") or at < e["before"]), eras[-1])
        sha = _at(chains[key(era)], at)
        if not sha:
            continue
        for path, blob in tree(era, sha):
            seen.setdefault((era["repo"], path, blob), [sha, []])[1].append(v)

    items = []
    for (repo, path, blob), (sha, versions) in seen.items():
        era = next(e for e in eras if e["repo"] == repo)
        name = f"{_markup.slug(path.removesuffix('.html'))}-{blob[:8]}"
        raw = f"https://raw.githubusercontent.com/{repo}/{sha}/{quote(path)}"
        if not ctx.allowed(raw):
            continue
        cite = f"https://github.com/{repo}/blob/{sha}/{quote(path)}"
        short = path.removesuffix(".html")
        for prefix in era.get("strip") or ():
            short = short.removeprefix(prefix)

        def make(raw=raw, cite=cite, short=short, versions=versions):
            html = ctx.text(raw)
            titles = _TITLE.findall(html)
            title = _markup.html_body(titles[-1]).strip() if titles else ""
            title = f"{title} ({short})" if title else short
            begin = next((m.start() for m in (r.search(html) for r in starts) if m), 0)
            stop = min((m.start() for m in (r.search(html, begin) for r in ends) if m),
                       default=len(html))
            body = _markup.html_body(html[begin:stop])
            _markup.require(title, body, raw)
            vs = sorted(set(versions), key=lambda v: times[v], reverse=True)
            return _markup.document(title, cite, ctx.stamp, body, ", ".join(vs))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодної сторінки в жодному знімку.")
    return items
