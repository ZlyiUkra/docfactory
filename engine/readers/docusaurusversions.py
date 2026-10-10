"""Читач версійної документації Docusaurus з історії репозиторію: один документ на неповторний
текст сторінки, у версіях — усі мінорні лінії, де вона була саме такою.

`docusaurus-versions` — сайт Docusaurus, що тримає документацію кожної випущеної версії в теці
                        `versioned_docs/version-X` і з часом переносить старі теки на архівні
                        сайти, прибираючи їх з репозиторію. Поля:
- `url` — префікс дерев (…/repos/ВЛАСНИК/РЕПО/git/trees/), `branch` — гілка сайту;
- `versions` — https://registry.npmjs.org/ПАКЕТ: з нього беруться мінорні лінії (`0.81`);
  `only` — вираз версій, що рахуються (типово лише стабільні `X.Y.Z`);
- `folder` — шаблон теки версії (`website/versioned_docs/version-{minor}`);
- `sidebars` — шаблон файла меню версії Docusaurus 1 (`…/version-{minor}-sidebars.json`);
- `v1_until` — мить ISO переходу сайту на Docusaurus 2: тека, яку видалили не пізніше, ще
  жила за правилами Docusaurus 1 (див. нижче);
- `site` — адреса сторінки на сайті для версій, що й досі лежать на гілці (`{minor}`, `{id}`),
  `site_latest` — для найновішої з них: Docusaurus віддає її без номера версії;
- `exclude` — вирази відносних шляхів у теці версії, що не беруться;
- `label` — префікс назви документа.

Звідки тека кожної версії. Те, що лежить на гілці, — з її вершини. Теку, яку вже прибрали
(React Native переніс 0.5–0.59 на Docusaurus 2 не взявши, 0.60–0.72 переніс в архів у 2023-му,
0.73–0.76 — у 2025-му), — зі знімка перед комітом, що її видалив: останній коміт, який чіпав
теку, і є той, що її видалив, тож береться його перший батько. Так кожна версія читається в
останньому стані, з правками, дописаними вже після її виходу. Мінорна лінія, жоден коміт якої
не чіпав теки (0.1–0.4 React Native: сайт починається з 0.5), документації не має.

Docusaurus 1. Тека версії тримала лише сторінки, що змінилися відтоді, як зрізали попередню
версію; решту сайт брав із найближчої старшої версії, де сторінка була. Тут так само: для
версії X кожна сторінка — з найновішої теки ≤ X, де вона лежить. Сторінку, яку з версії
прибрали, Docusaurus 1 і далі знаходив би за адресою, але меню версії її вже не показувало,
тож лишаються тільки сторінки з меню (найновіший файл меню ≤ X). Файл тієї епохи названо
ідентифікатором сторінки: `flatlist.md` ↔ `version-0.59-flatlist` у меню.

Одиниця — пара «відносний шлях у теці версії, вміст» (хеш blob): однакова сторінка десяти
версій тягнеться й лежить раз, а в її версії лягають усі десять. Розбір MDX — той самий, що в
`site-history` для Docusaurus: виноски й вкладки стають підписами.
"""

import json
import posixpath
import re
from html import unescape
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.ghhistory import _atx, _split_title
from engine.readers.sitedocs import docusaurus

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_STABLE = r"^\d+\.\d+\.\d+$"
_EXTS = (".md", ".mdx")


def _key(minor: str) -> tuple:
    return tuple(int(p) for p in minor.split("."))


def _json(ctx, url: str):
    try:
        return json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")


def _menu_ids(node, prefix: str, out: set) -> None:
    """Ідентифікатори сторінок меню Docusaurus 1, хоч би як глибоко вкладені (підкатегорії —
    об'єкти з `ids`)."""
    if isinstance(node, str):
        if node.startswith(prefix):
            out.add(node[len(prefix):])
    elif isinstance(node, list):
        for x in node:
            _menu_ids(x, prefix, out)
    elif isinstance(node, dict):
        for x in node.values():
            _menu_ids(x, prefix, out)


@register("docusaurus-versions")
def docusaurus_versions(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    if "{minor}" not in source.get("folder", ""):
        raise SystemExit(f"{source['id']}: поле folder — шаблон теки з {{minor}}.")
    branch = source.get("branch", "main")
    api = f"https://api.github.com/repos/{owner}/{repo}"
    folder_rx = re.compile("^" + re.escape(source["folder"]).replace(
        re.escape("{minor}"), r"(\d+\.\d+)") + "/(.+)$")
    menu_rx = (re.compile("^" + re.escape(source["sidebars"]).replace(
        re.escape("{minor}"), r"\d+\.\d+") + "$") if source.get("sidebars") else None)
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    label = source.get("label", "")
    v1_until = source.get("v1_until", "")

    packument = _json(ctx, source["versions"])
    only = re.compile(source.get("only") or _STABLE)
    minors = sorted({".".join(v.split(".")[:2]) for v in packument.get("versions") or {}
                     if only.search(v)}, key=_key, reverse=True)

    # знімок → {мінорна: {відносний шлях: blob}}; дерево кожного знімка — один раз
    folders: dict = {}

    def snapshot(ref: str) -> dict:
        if ref not in folders:
            data = _json(ctx, f"{source['url']}{ref}?recursive=1")
            if data.get("truncated"):
                raise SystemExit(f"{source['url']}{ref}: GitHub обрізав дерево — перелік був би "
                                 f"неповним.")
            # Під ключем "" — лише файли меню: дерево сайту — десятки тисяч шляхів, і
            # тримати їх усі на кожен знімок означало б сотні мегабайтів у пам'яті.
            found: dict = {"": {}}
            for e in data.get("tree") or []:
                if e.get("type") != "blob":
                    continue
                hit = folder_rx.match(e.get("path", ""))
                if hit:
                    found.setdefault(hit.group(1), {})[hit.group(2)] = e["sha"]
                elif menu_rx and menu_rx.match(e.get("path", "")):
                    found[""][e["path"]] = e["sha"]
            folders[ref] = found
        return folders[ref]

    head = _json(ctx, f"{api}/commits?sha={quote(branch)}&per_page=1")
    if not head:
        raise SystemExit(f"{owner}/{repo}@{branch}: жодного коміту.")
    head = head[0]["sha"]
    at_head = [v for v in minors if v in snapshot(head)]

    # мінорна → (знімок, чи це Docusaurus 1)
    where: dict = {}
    prev = 0
    for v in minors:
        if v in at_head:
            where[v] = (head, False)
            prev = len(snapshot(head)[v])
            continue
        folder = source["folder"].format(minor=v)
        last = _json(ctx, f"{api}/commits?sha={quote(branch)}&path={quote(folder)}&per_page=5")
        for commit in last or ():
            sha = commit["sha"]
            if v not in snapshot(sha):
                if not commit.get("parents"):
                    continue
                sha = commit["parents"][0]["sha"]
            date = commit["commit"]["committer"]["date"]
            v1 = bool(v1_until) and date <= v1_until
            where[v] = (sha, v1)
            # Залишок теки, а не версія: коміт, що переносив 0.60–0.68 в архів, забув у теці
            # 0.69 один файл, і прибрав його вже наступний коміт. Знімок перед ним — одна
            # сторінка; тоді крок назад, до знімка, де тека ще повна. Теки Docusaurus 1 малі
            # за самою будовою, тож їх це не стосується.
            if v1 or not prev or len(snapshot(sha).get(v, {})) >= prev / 2:
                break
        if v in where and not where[v][1]:
            prev = len(snapshot(where[v][0]).get(v, {}))

    def pages(v: str) -> dict:
        ref, v1 = where[v]
        snap = snapshot(ref)
        if not v1:
            return dict(snap.get(v, {}))
        older = sorted((w for w in snap if w and _key(w) <= _key(v)), key=_key)
        files: dict = {}
        for w in older:
            files.update(snap[w])
        menus = [w for w in older if source.get("sidebars", "").format(minor=w) in snap[""]]
        if not menus:
            return files
        menu = source["sidebars"].format(minor=menus[-1])
        raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{quote(menu)}"
        ids: set = set()
        if ctx.allowed(raw):
            try:
                _menu_ids(json.loads(ctx.text(raw)), f"version-{menus[-1]}-", ids)
            except ValueError:
                ids = set()
        if not ids:
            return files
        return {rel: sha for rel, sha in files.items()
                if re.sub(r"\.mdx?$", "", rel) in ids}

    # (відносний шлях, blob) → [знімок, [мінорні]]; порядок — від найновішої версії
    seen: dict = {}
    for v in minors:
        if v not in where:
            continue
        for rel, sha in pages(v).items():
            if not rel.endswith(_EXTS) or any(r.search(rel) for r in exclude):
                continue
            seen.setdefault((rel, sha), [where[v][0], []])[1].append(v)
    if not seen:
        raise SystemExit(f"{source['id']}: жодної сторінки в жодній теці версії.")

    newest = at_head[0] if at_head else ""
    items = []
    for (rel, sha), (ref, versions) in seen.items():
        top = versions[0]
        # Тека, з якої сторінка береться: у Docusaurus 1 це найновіша тека ≤ версії, де файл є.
        snap = snapshot(ref)
        owner_v = next((w for w in sorted(snap, key=lambda w: _key(w) if w else (-1,),
                                          reverse=True)
                        if w and _key(w) <= _key(top) and snap[w].get(rel) == sha), top)
        path = f"{source['folder'].format(minor=owner_v)}/{rel}"
        raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{quote(path)}"
        if not ctx.allowed(raw):
            continue
        stem = re.sub(r"\.mdx?$", "", rel)
        name = f"{_markup.slug(stem)}-{sha[:8]}"
        cite = f"https://github.com/{owner}/{repo}/blob/{ref}/{quote(path)}"

        def make(raw=raw, cite=cite, rel=rel, stem=stem, top=top,
                 version=", ".join(versions)):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            meta, rest = _markup.front_matter(text)
            meta = meta or {}
            rest = _atx(docusaurus(rest, None, {}))
            title = meta.get("title") or meta.get("sidebar_label") or ""
            if not title:
                title, rest = _split_title(rest)
            if not title:
                title = posixpath.basename(stem)
            url = cite
            if top in at_head and source.get("site"):
                page = str(meta.get("original_id") or meta.get("id") or posixpath.basename(stem))
                page = posixpath.join(posixpath.dirname(stem), page.rsplit("/", 1)[-1])
                url = (source.get("site_latest") if top == newest and source.get("site_latest")
                       else source["site"]).format(minor=top, id=page)
            title = unescape(str(title))
            if label:
                title = f"{label}: {title}"
            body = _markup.markdown_body(rest)
            if body.strip():
                _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, url, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
