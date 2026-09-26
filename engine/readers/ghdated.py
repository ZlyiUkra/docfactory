"""Читач історії сайту документації без тегів: знімок репозиторію на кожну версію пакета npm.

`ghsite-dated` — документація, що живе в окремому репозиторії сайту (або в теці репозиторію
                 бібліотеки), де версійних тегів немає. Версії й дати релізів береться з
                 реєстру npm (`versions` — адреса опису пакета), знімок — з гілки
                 репозиторію на мить перед наступним релізом тієї ж лінії.

Поля джерела:
- `versions` — https://registry.npmjs.org/ПАКЕТ; з нього беруться всі версії та їхні дати;
- `eras` — епохи сайту від найстарішої: `repo` («власник/назва»), `branch`, `before` (мить
  ISO, до якої діє епоха; в останньої немає), `include`/`exclude` — регулярні вирази шляхів;
- `line_marker` — вираз сегмента шляху, що позначає документацію старої лінії (`V5/`,
  `v6/`): група 1 — номер мажорної версії;
- `min_code_size` — найменший розмір файла коду (.ts/.tsx/.js/.jsx), що береться: обгортки
  сторінок на кілька сотень байтів тексту не несуть.

Лінія. Стабільні версії однієї мажорної — одна лінія (7.x). Передрелізи одного номера
(`8.0.0-alpha.5`, `8.0.0-beta.4`) — окрема лінія, і версією документа стає власний номер
передрелізу: фільтр «8» чи «8.0» його знаходить, бо номер починається з «8.0.».

Мить знімка версії — поява наступної версії тієї ж лінії: до того документація й
описувала цю версію, разом із правками, дописаними вже після її виходу. Передреліз
обмежує ще й вихід стабільного номера. Для останньої версії лінії мить — наступний реліз
пакета взагалі; для найновішої версії пакета — сьогоднішній стан гілки.

Документація старої лінії, що після виходу нової живе в теці з позначкою (`src/data/V6/`),
належить тільки своїй лінії: знімок версії 6.x, де такі теки є, бере лише їх, а решта
знімків ці теки відкидає. Без цього версія 6.15.8 від 2021 року отримала б текст v7.

Далі — як `ghdocs-history`: один документ на неповторну пару «шлях, вміст» (хеш blob із
дерева), у версії документа лягають усі версії, у знімку яких файл лежав саме таким.
Markdown і MDX розбираються як markdown; код сайту (JSX, дані в TSX, приклади в
шаблонних рядках) — через `_jsx`.
"""

import json
import re
import time
from urllib.parse import quote

from engine.readers import Item, _jsx, _markup, register

_SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-(.+))?$")
_CODE = (".ts", ".tsx", ".js", ".jsx")
_MARKDOWN = (".md", ".mdx")
_MDX_IMPORT = re.compile(r"^(import|export)\s.*$", re.M)
_SINCE = re.compile(r"<Since\s+version=\"([^\"]+)\"\s*/>")


def _line(version: str) -> str:
    m = _SEMVER.match(version)
    if not m:
        return version
    return f"{m.group(1)}.{m.group(2)}.{m.group(3)}-pre" if m.group(4) else m.group(1)


def _moments(packument: dict, now: str) -> dict:
    """версія → мить знімка (ISO); найновіша версія пакета дістає `now`."""
    times = packument.get("time") or {}
    known = [v for v in (packument.get("versions") or {}) if v in times]
    order = sorted(known, key=lambda v: times[v])
    lines: dict = {}
    for v in order:
        lines.setdefault(_line(v), []).append(v)
    moment = {}
    for line, vs in lines.items():
        for i, v in enumerate(vs):
            ends = []
            if i + 1 < len(vs):
                ends.append(times[vs[i + 1]])
            m = _SEMVER.match(v)
            if m and m.group(4):
                stable = f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
                if stable in times and times[stable] > times[v]:
                    ends.append(times[stable])
            if not ends:
                later = [times[w] for w in order if times[w] > times[v]]
                ends.append(later[0] if later else now)
            moment[v] = min(ends)
    return moment


def _chain(ctx, repo: str, branch: str, before: str) -> list:
    """[(мить коміту, sha)] першого батька гілки, від найновішого."""
    commits: dict = {}
    head = ""
    for page in range(1, 400):
        url = (f"https://api.github.com/repos/{repo}/commits?sha={quote(branch)}"
               f"&per_page=100&page={page}" + (f"&until={before}" if before else ""))
        try:
            batch = json.loads(ctx.text(url))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
        if not isinstance(batch, list):
            raise SystemExit(f"{url}: очікував список комітів.")
        for c in batch:
            head = head or c["sha"]
            commits[c["sha"]] = (c["commit"]["committer"]["date"],
                                 [p["sha"] for p in c.get("parents") or []])
        if len(batch) < 100:
            break
    out = []
    sha = head
    while sha in commits:
        date, parents = commits[sha]
        out.append((date, sha))
        sha = parents[0] if parents else ""
    if not out:
        raise SystemExit(f"{repo}@{branch}: жодного коміту.")
    return out


def _at(chain: list, moment: str) -> str:
    """Коміт, що був вершиною гілки перед миттю `moment` (або "", якщо гілки ще не було)."""
    for date, sha in chain:
        if date < moment:
            return sha
    return ""


def _title(path: str, era: dict) -> str:
    base = path
    for prefix in era.get("strip") or ():
        base = base.removeprefix(prefix)
    return re.sub(r"\.(mdx?|tsx?|jsx?)$", "", base)


@register("ghsite-dated")
def ghsite_dated(source: dict, ctx) -> list[Item]:
    eras = source.get("eras")
    if not isinstance(eras, list) or not eras:
        raise SystemExit(f"{source['id']}: читач ghsite-dated потребує поля eras.")
    try:
        packument = json.loads(ctx.text(source["versions"]))
    except ValueError as exc:
        raise SystemExit(f"{source['versions']}: відповідь не JSON ({exc}).")
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    moments = _moments(packument, now)
    times = packument["time"]
    marker = re.compile(source.get("line_marker") or r"(?!)")
    min_code = int(source.get("min_code_size") or 0)

    chains = {}
    for era in eras:
        chains[era["repo"]] = _chain(ctx, era["repo"], era.get("branch", "master"),
                                     era.get("before", ""))
    # (репо, sha) → [(шлях, blob, розмір)]
    trees: dict = {}

    def tree(era: dict, sha: str) -> list:
        key = (era["repo"], sha)
        if key not in trees:
            url = f"https://api.github.com/repos/{era['repo']}/git/trees/{sha}?recursive=1"
            try:
                data = json.loads(ctx.text(url))
            except ValueError as exc:
                raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
            if data.get("truncated"):
                raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
            inc = [re.compile(r) for r in era.get("include") or [r"."]]
            exc_ = [re.compile(r) for r in era.get("exclude") or []]
            files = []
            for e in data.get("tree") or []:
                path = e.get("path", "")
                if (e.get("type") != "blob" or not e.get("size")
                        or not path.endswith(_MARKDOWN + _CODE)
                        or not any(r.search(path) for r in inc)
                        or any(r.search(path) for r in exc_)
                        or (path.endswith(_CODE) and e["size"] < min_code)):
                    continue
                files.append((path, e["sha"], e["size"]))
            trees[key] = files
        return trees[key]

    def own_line(path: str) -> str:
        for seg in path.split("/"):
            m = marker.fullmatch(seg)
            if m:
                return m.group(1)
        return ""

    # (репо, шлях, blob) → [версії]; порядок першої появи — від найновішої версії.
    seen: dict = {}
    newest_first = sorted(moments, key=lambda v: times[v], reverse=True)
    for v in newest_first:
        at = moments[v]
        era = next((e for e in eras if not e.get("before") or at < e["before"]), eras[-1])
        sha = _at(chains[era["repo"]], at)
        if not sha:
            continue
        files = tree(era, sha)
        major = _line(v).split(".")[0]
        marked = [f for f in files if own_line(f[0]) == major]
        chosen = marked or [f for f in files if not own_line(f[0])]
        for path, blob, _size in chosen:
            seen.setdefault((era["repo"], path, blob), [sha, []])[1].append(v)

    items = []
    names: dict = {}
    for (repo, path, blob), (sha, versions) in seen.items():
        era = next(e for e in eras if e["repo"] == repo)
        name = f"{_markup.slug(re.sub(r'[.](mdx?|tsx?|jsx?)$', '', path))}-{blob[:8]}"
        if name in names:
            names[name].extend(versions)
            continue
        names[name] = versions
        raw = f"https://raw.githubusercontent.com/{repo}/{sha}/{quote(path)}"
        if not ctx.allowed(raw):
            continue
        cite = f"https://github.com/{repo}/blob/{sha}/{quote(path)}"

        def make(raw=raw, cite=cite, path=path, era=era, name=name):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            if path.endswith(_MARKDOWN):
                meta, rest = _markup.front_matter(text)
                rest = _SINCE.sub(r"(since \1)", rest)
                if path.endswith(".mdx"):
                    rest = _MDX_IMPORT.sub("", rest)
                title = meta.get("title", "") if meta else ""
                body = _markup.markdown_body(rest)
            else:
                title = _jsx.title_of(text)
                body = _markup.markdown_body(_jsx.text_of(text))
            short = _title(path, era)
            title = f"{title} ({short})" if title and title != short else short
            vs = sorted(set(names[name]), key=lambda v: times[v], reverse=True)
            return _markup.document(title, cite, ctx.stamp, body, ", ".join(vs))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла в жодному знімку.")
    return items
