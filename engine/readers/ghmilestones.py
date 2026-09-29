"""Читач історії сайту без тегів і без пакета npm: знімок гілки на кожну версію з переліку дат.

`ghsite-milestones` — сайт у репозиторії, де версійних тегів немає, а версії продукту
                      виходять за розкладом, якого реєстр npm не знає (V8 іде з Chrome:
                      V8 12.4 — це Chrome 124). Дати версій оголошуються в самому джерелі,
                      тож білий список лишається самим GitHub.

Поля джерела:
- `url` — префікс дерев через API (…/repos/ВЛАСНИК/РЕПО/git/trees/), як у `ghdocs-history`;
- `branch` — гілка сайту;
- `milestones` — об'єкт «версія → дата виходу (РРРР-ММ-ДД)»; нова версія — новий рядок;
- `folders`, `files`, `exclude` — як у `ghdocs-history`: теки, окремі файли, вирази шляхів,
  що не беруться;
- `own_version` — `{"pattern": вираз шляху, "version": шаблон}`: файл, що сам називає свою
  версію (пост «V8 release v9.9» — `v8-release-99.md`). Такий файл несе лише свою версію і
  рік з поля `date` шапки, а не всі знімки, у яких лежав: інакше фільтр «9.9» давав би
  рівно так само пости 4.5–9.8, що лежали в тому ж знімку.

Мітки. Знімок версії — стан гілки на мить виходу наступної версії: до того сайт і
описував цю версію. Для найновішої версії мить — сьогодні. Знімок дістає дві мітки:
версію («12.4») і рік своєї миті («2024»). Фільтр «12.4» дає сайт часу V8 12.4, а
«2019» — усі тексти, що лежали на сайті хоч в одному знімку 2019 року. Версія, чия мить
раніша за перший коміт гілки, знімка не має.

Далі — як `ghdocs-history`: один документ на неповторну пару «шлях, вміст» (хеш blob із
дерева), у версії документа лягають усі мітки знімків, де файл лежав саме таким.
"""

import json
import re
import time
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.ghdated import _at, _chain

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _key(version: str) -> tuple:
    return tuple(int(p) for p in version.split("."))


@register("ghsite-milestones")
def ghsite_milestones(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
    repo = f"{m.group(1)}/{m.group(2)}"
    stones = source.get("milestones")
    if not isinstance(stones, dict) or not stones:
        raise SystemExit(f"{source['id']}: читач ghsite-milestones потребує поля "
                         f"milestones — об'єкта «версія → дата».")
    bad = [v for v, d in stones.items() if not _DAY.match(str(d))
           or not re.fullmatch(r"\d+(\.\d+)*", v)]
    if bad:
        raise SystemExit(f"{source['id']}: у milestones хибні записи: {', '.join(bad)}.")
    folders = [f.strip("/") for f in source.get("folders") or ["docs"]]
    files = {f.strip("/") for f in source.get("files") or ()}
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    own = source.get("own_version") or {}
    own_re = re.compile(own["pattern"]) if own.get("pattern") else None

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    ordered = sorted(stones, key=_key)
    # версія → мить знімка: вихід наступної версії, для найновішої — сьогодні.
    moments = {v: (f"{stones[ordered[i + 1]]}T00:00:00Z" if i + 1 < len(ordered) else now)
               for i, v in enumerate(ordered)}
    chain = _chain(ctx, repo, source.get("branch", "main"), "")

    # (шлях, blob) → [sha найновішого знімка, [мітки]]; порядок — від найновішої версії.
    seen: dict = {}
    for v in reversed(ordered):
        sha = _at(chain, moments[v])
        if not sha:
            continue
        url = f"{source['url']}{sha}?recursive=1"
        try:
            tree = json.loads(ctx.text(url))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
        if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
            raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
        if tree.get("truncated"):
            raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
        labels = [v, moments[v][:4]]
        for entry in tree["tree"]:
            path = entry.get("path", "")
            folder = path.rpartition("/")[0]
            if (entry.get("type") == "blob" and (path in files or folder in folders)
                    and path.endswith(".md") and entry.get("size", 1) > 0
                    and not any(r.search(path) for r in exclude)):
                seen.setdefault((path, entry["sha"]), [sha, []])[1].extend(labels)

    items = []
    for (path, blob), (sha, labels) in seen.items():
        name = f"{_markup.slug(path.removesuffix('.md'))}-{blob[:8]}"
        where = f"{repo}/{sha}/{quote(path)}"
        raw = f"https://raw.githubusercontent.com/{where}"
        if not ctx.allowed(raw):
            continue
        cite = f"https://github.com/{repo}/blob/{sha}/{quote(path)}"
        mine = own_re.search(path) if own_re else None
        version = (mine.expand(own["version"]) if mine else
                   ", ".join(dict.fromkeys(labels)))

        def make(raw=raw, cite=cite, path=path, version=version, mine=mine):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            meta, rest = _markup.front_matter(text)
            # Шапка буває з розміткою («<i>Elements kinds</i> in V8»): сайт її рендерить,
            # а в назві документа й видачі вона лише шум.
            title = re.sub(r"<[^>]+>", "", _markup.title_of(meta, cite)) if meta else ""
            body = _markup.markdown_body(rest)
            if not title:
                title = path.rsplit("/", 1)[-1].removesuffix(".md")
            if mine and _DAY.match(meta.get("date", "")[:10]):
                version = f"{version}, {meta['date'][:4]}"
            if body.strip():
                _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, cite, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла в жодному знімку.")
    return items
