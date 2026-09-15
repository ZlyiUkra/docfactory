"""Читачі GitHub: документація на тезі репозиторію, CHANGELOG і нотатки релізів.

`ghdocs`     — markdown-документація, що лежала в репозиторії на момент тегу чи
               коміту. `url` — дерево через API
               (…/repos/ВЛАСНИК/РЕПО/git/trees/ТЕГ-або-SHA?recursive=1), поле
               `folders` — теки, .md-файли яких стають документами: прямі, а з
               `recursive: true` — і з вкладених тек. Поле `root` — префікс шляху,
               що знімається з імені документа (типово — перша тека шляху), щоб та
               сама сторінка в різних джерелах мала те саме ім'я. Переклади
               (`*.ko-KR.md`) пропускаються: корпус англійський. Текст береться з
               raw.githubusercontent.com, а в шапку лягає людська адреса blob.
`changelog`  — CHANGELOG.md, поділений на версії: кожен заголовок «## 18.2.0 (…)»
               дає окремий документ із цією версією; спільний заголовок двох
               ліній («## 0.5.2, 0.4.2 (…)») — один документ з обома. Файл
               тягнеться один раз.
`ghreleases` — нотатки релізів через API: сторінки `url` гортаються параметром
               page, доки не прийде неповна; кожен реліз — документ.
`ghcommit`   — один коміт через API (…/repos/ВЛАСНИК/РЕПО/commits/SHA): повідомлення,
               автор, дата, склад файлів; поле `files` — шляхи, текст яких на цьому
               коміті додається в документ (напр. тодішній README.md).

Номер у ідентифікаторі й шапці — сама версія, без «v», бо саме нею фільтрує пошук.
"""

import collections
import json
import re
from urllib.parse import parse_qs, urlsplit

from engine.readers import Item, _markup, register

_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/([^/]+)$")
_LOCALE = re.compile(r"\.[a-z]{2}-[A-Z]{2}\.md$")
_POSITION = re.compile(r"(^|/)\d+(?:\.\d+)*-")
# Заголовок версії CHANGELOG. Буває спільним для двох ліній, випущених одним днем —
# «## 0.5.2, 0.4.2 (December 18, 2013)»; без цього текст такого релізу приклеювався
# до сусіднього документа й лежав під чужою версією.
_VERSION_HEAD = re.compile(
    r"^## +(\d+\.\d+[\w.-]*(?:, *\d+\.\d+[\w.-]*)*)[ \t]*(\([^)\n]*\))?[ \t]*$", re.M)
_RELEASE_TAG = re.compile(r"^v?(\d+\.\d+\.\d+(?:-[\w.]+)?)$")


def _json(ctx, url: str):
    try:
        return json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")


@register("ghdocs")
def ghdocs(source: dict, ctx) -> list[Item]:
    m = _TREE.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував адресу дерева тегу "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/ТЕГ.")
    owner, repo, tag = m.groups()
    tree = _json(ctx, source["url"])
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        raise SystemExit(f"{source['url']}: у відповіді немає дерева файлів.")
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")
    folders = [f.strip("/") for f in source.get("folders") or ["docs"]]
    recursive = source.get("recursive") is True
    root = source.get("root", "").strip("/")
    paths = []
    for entry in tree["tree"]:
        path = entry.get("path", "")
        folder, _, leaf = path.rpartition("/")
        inside = (folder in folders if not recursive else
                  any(folder == f or folder.startswith(f + "/") for f in folders))
        if (entry.get("type") == "blob" and inside and leaf.endswith(".md")
                and not _LOCALE.search(leaf)):
            paths.append(path)
    items = []
    for path in paths:
        raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{tag}/{path}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{tag}/{path}"
        # Позиція у старому змісті («02.1-jsx-in-depth») зі слага знімається: та
        # сама сторінка в сусідніх версіях мусить мати те саме ім'я.
        if root and path.startswith(root + "/"):
            rel = path[len(root) + 1:]
        else:
            rel = path.split("/", 1)[1] if "/" in path else path
        # «learn/index.md» на сайті — сторінка «/learn»: без зрізаного «/index» ім'я
        # розходилося з тим самим документом живого сайту, і незмінний текст не зливався.
        stem = re.sub(r"(^|/)index$", "", rel.removesuffix(".md")) or "index"
        name = _markup.slug(_POSITION.sub(r"\1", stem))

        def make(raw=raw, blob=blob, leaf=path.rsplit("/", 1)[-1]):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            meta, rest = _markup.front_matter(text)
            body = _markup.markdown_body(rest)
            # Переадресація старого сайту («layout: redirect») тіла не має, але сама є
            # фактом історії: розділ переїхав. Її текст — куди саме.
            if meta.get("layout") == "redirect" and meta.get("dest_url"):
                body = body or f"This page redirects to {meta['dest_url']}."
            title = _markup.title_of(meta, blob) if meta else ""
            # Файл на закріпленому тезі — не сторінка помилки, тож коротке тіло не
            # підозріле: «модуль застарів» чи «сторінку перенесено» — теж історія.
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['url']}: у теках {', '.join(folders)} немає жодного "
                         f"дозволеного .md.")
    return items


@register("changelog")
def changelog(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    heads = list(_VERSION_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «## X.Y.Z (дата)» — "
                         f"формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    items = []
    for i, head in enumerate(heads):
        versions = [v.strip() for v in head.group(1).split(",")]
        version = ", ".join(versions)
        heading = f"{version} {head.group(2) or ''}".strip()
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        name = re.sub(r"[^\w.-]+", "-", "-".join(versions))

        def make(chunk=chunk, heading=heading, version=version):
            body = _markup.markdown_body(chunk)
            _markup.require(heading, body, f"{source['url']} {heading}", min_chars=1)
            url = f"{cite}#{_markup.github_anchor(heading)}"
            return _markup.document(f"{label}: {heading}", url, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("ghreleases")
def ghreleases(source: dict, ctx) -> list[Item]:
    base = source["url"]
    per_page = int((parse_qs(urlsplit(base).query).get("per_page") or ["30"])[0])
    releases: list = []
    for page in range(1, 101):
        url = base if page == 1 else f"{base}{'&' if '?' in base else '?'}page={page}"
        batch = _json(ctx, url)
        if not isinstance(batch, list):
            raise SystemExit(f"{url}: очікував список релізів.")
        releases.extend(batch)
        if len(batch) < per_page:
            break
    if not releases:
        raise SystemExit(f"{base}: жодного релізу.")
    label = source.get("label", "Release")
    items = []
    for rel in releases:
        if not isinstance(rel, dict) or rel.get("draft") or not rel.get("tag_name"):
            continue
        tag = str(rel["tag_name"])
        m = _RELEASE_TAG.match(tag)
        name = re.sub(r"[^\w.-]+", "-", tag).strip("-")

        def make(rel=rel, tag=tag, version=m.group(1) if m else ""):
            day = str(rel.get("published_at") or rel.get("created_at") or "")[:10]
            pre = ", pre-release" if rel.get("prerelease") else ""
            notes = _markup.markdown_body(str(rel.get("body") or "")) or "No release notes."
            body = f"Tag {tag}, published {day}{pre}.\n\n{notes}"
            title = f"{label}: {rel.get('name') or tag}"
            return _markup.document(title, str(rel.get("html_url") or base), ctx.stamp,
                                    body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


_COMMIT = re.compile(r"^/repos/([^/]+)/([^/]+)/commits/([0-9a-f]{7,40})$")


@register("ghcommit")
def ghcommit(source: dict, ctx) -> list[Item]:
    m = _COMMIT.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував адресу коміту "
                         f"/repos/ВЛАСНИК/РЕПО/commits/SHA.")
    owner, repo, sha = m.groups()

    def make():
        data = _json(ctx, source["url"])
        if not isinstance(data, dict) or not isinstance(data.get("commit"), dict):
            raise SystemExit(f"{source['url']}: у відповіді немає коміту.")
        full = str(data.get("sha") or sha)
        author = data["commit"].get("author") or {}
        message = str(data["commit"].get("message") or "").strip()
        stats = data.get("stats") or {}
        files = [f for f in data.get("files") or [] if isinstance(f, dict)]
        # Склад коміту GitHub віддає сторінками по 300 файлів (усього до 3000): без
        # гортання перший публічний коміт React, 317 файлів, обривався на трьохсотому.
        batch, page = len(data.get("files") or []), 1
        while batch >= 300 and page < 10:
            page += 1
            more = _json(ctx, f"{source['url']}{'&' if '?' in source['url'] else '?'}page={page}")
            extra = [f for f in (more.get("files") or [] if isinstance(more, dict) else [])
                     if isinstance(f, dict)]
            files += extra
            batch = len(extra)
        tops = collections.Counter(
            f.get("filename", "").split("/", 1)[0] if "/" in f.get("filename", "") else "(root)"
            for f in files)
        parts = [f"Commit {full} in {owner}/{repo}, authored by {author.get('name', '?')} "
                 f"on {author.get('date', '?')}.",
                 "", "## Message", "", message or "(empty)",
                 "", "## Files", "",
                 f"{len(files)} files in the commit listing, +{stats.get('additions', '?')} / "
                 f"-{stats.get('deletions', '?')} lines.",
                 "", "By top-level directory:", ""]
        parts += [f"- {top}: {count}" for top, count in sorted(tops.items())]
        parts += ["", "Every file:", ""]
        parts += [f"- {f.get('status', '?')} {f.get('filename', '?')} (+{f.get('additions', 0)})"
                  for f in files]
        for path in source.get("files") or []:
            raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{full}/{path}"
            if ctx.allowed(raw):
                _, rest = _markup.front_matter(ctx.text(raw))
                parts += ["", f"## {path} at this commit", "", _markup.markdown_body(rest)]
        body = _markup.tidy("\n".join(parts), strip=False)
        _markup.require(message, body, source["url"])
        day = str(author.get("date") or "")[:10]
        title = f"{source.get('label', 'Commit')}: {message.splitlines()[0]} ({day})"
        return _markup.document(title, str(data.get("html_url") or source["url"]), ctx.stamp,
                                body, source.get("version", ""))

    return [Item(id=f"{source['id']}/commit-{sha[:7]}",
                 file=f"{source['id']}--commit-{sha[:7]}.txt", make=make)]
