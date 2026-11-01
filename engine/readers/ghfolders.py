"""Читач документації, що тримає кожну версію в окремій теці одного коміту: один документ на неповторний текст.

`ghdocs-folders` — `url` — префікс дерев через API (…/repos/ВЛАСНИК/РЕПО/git/trees/), `tags` — об'єкт з одним
                   комітом («SHA → ""»), `root` — тека, де лежать теки версій (`guides`), `folder_version` —
                   вираз над іменем теки з групою `v`, що дає мітку версії (`^v(?P<v>\\d+\\.\\d+)\\.\\d+$`):
                   тека, ім'я якої не збіглося, не береться (`release` — копія найновішої). Необов'язкові:
                   `extensions` (типово `.md`), `name_prefix`, `site` — шаблон адреси сторінки з `{folder}` і
                   `{path}` (шлях у теці версії без розширення й без кінцевого `/index`); `title_from: "path"` —
                   назва сторінки без шапки YAML береться зі шляху («Components / Component arguments»),
                   а не з першого заголовка: гайди Ember тримають назви окремо (`pages.yml`), і першим
                   заголовком сторінки рецептів був «Problem».

Навіщо. Гайди Ember (ember-learn/guides-source) тримають кожну мінорну окремою текою — `guides/v1.10.0` …
`guides/v7.2.0`, 94 теки й 14 тисяч файлів на одному коміті master. Тегів немає, тож `ghdocs-history` бере
їх лише джерелом на теку, а там шлях кожної версії свій (`guides/v5.0.0/components/…`), і однакові тексти
сусідніх версій завантажуються й лежать стільки разів, скільки тек: 14 127 завантажень, хоча різних текстів
серед них 4 558.

Тут одиниця — пара «шлях усередині теки версії, вміст» (вміст упізнається хешем blob із дерева). Така пара
стає одним документом, а в його версії лягають усі теки, де файл лежав саме таким; текст береться з
найновішої з них. Ім'я документа — шлях у теці з хешем blob, тож `revision_suffix` зрізає хеш, і редакції
однієї сторінки мають спільне ім'я. Перетворення markdown те саме, що в `ghdocs-history` для простих
`.md`: шапка YAML дає назву, заголовки підкресленням стають «#», рядки з самою картинкою знімаються.
"""

import json
import re
from html import unescape
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.ghhistory import _ATTRS, _IMAGE, _IMAGE_LINE, _atx, _split_title

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")


def _num(text: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", text)) or (0,)


def _path_title(rel: str) -> str:
    """Назва зі шляху сторінки: «components/component-arguments.md» → «Components / Component arguments»."""
    parts = re.sub(r"\.[a-z]+$", "", rel).split("/")
    if len(parts) > 1 and parts[-1] == "index":
        parts = parts[:-1]
    return " / ".join(p.replace("-", " ").replace("_", " ").capitalize() for p in parts)


@register("ghdocs-folders")
def ghdocs_folders(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев /repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or len(tags) != 1:
        raise SystemExit(f"{source['id']}: поле `tags` — один коміт («SHA → \"\"»).")
    commit = next(iter(tags))
    root = source["root"].strip("/") + "/"
    folder_rx = re.compile(source["folder_version"])
    exts = tuple(source.get("extensions") or [".md"])
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    site = source.get("site") or ""
    url = f"{source['url']}{quote(commit, safe='')}?recursive=1"
    try:
        tree = json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
    if tree.get("truncated"):
        raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")

    # (шлях у теці, blob) → [(мітка версії, тека)]
    seen: dict = {}
    for entry in tree.get("tree") or []:
        path = entry.get("path", "")
        if entry.get("type") != "blob" or not path.startswith(root) or not path.endswith(exts):
            continue
        folder, _, rel = path[len(root):].partition("/")
        fm = folder_rx.match(folder)
        if not fm or not rel or entry.get("size", 1) <= 0:
            continue
        seen.setdefault((rel, entry["sha"]), []).append((fm.group("v"), folder))

    items = []
    for (rel, sha), where in seen.items():
        where.sort(key=lambda vf: _num(vf[1]), reverse=True)
        folder = where[0][1]
        path = f"{root}{folder}/{rel}"
        raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{quote(path)}"
        if not ctx.allowed(raw):
            continue
        page = re.sub(r"(?:/index)?\.[a-z]+$", "", rel)
        cite = (site.replace("{folder}", folder).replace("{path}", page) if site
                else f"https://github.com/{owner}/{repo}/blob/{commit}/{quote(path)}")
        version = ", ".join(dict.fromkeys(v for v, _ in where))
        stem = re.sub(r"\.[a-z]+$", "", rel)
        name = f"{lead}{_markup.slug(stem)}-{sha[:8]}"

        def make(raw=raw, cite=cite, rel=rel, version=version):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            meta, rest = _markup.front_matter(text)
            rest = _atx(_IMAGE_LINE.sub("", rest))
            title = (meta.get("title", "") if meta else "")
            if not title and source.get("title_from") == "path":
                title = _path_title(rel)
            if not title:
                title, rest = _split_title(rest)
            title = unescape(_ATTRS.sub("", _IMAGE.sub("", title)).strip()) or _path_title(rel)
            body = _markup.markdown_body(rest)
            if body.strip():
                _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, cite, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у {root} немає жодної теки версії за `folder_version`.")
    return items
