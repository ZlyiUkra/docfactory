"""Читач документації Storybook: сторінки `docs/` репозиторію з прикладами коду на місці.

`storybook-docs` — сторінки MDX теки `docs/` репозиторію storybookjs/storybook на кожній
                   оголошеній гілці. Поля:
                   `url`      — префікс дерев (…/repos/ВЛАСНИК/РЕПО/git/trees/);
                   `refs`     — об'єкт «гілка → версія», від найновішого;
                   `site`     — об'єкт «гілка → шаблон адреси сторінки на сайті» (`{path}` —
                                шлях сторінки від `docs/` без розширення); гілка без шаблону
                                — версія, якої на сайті вже немає, і адресою стає файл на
                                GitHub;
                   `exclude`  — вирази шляхів від кореня, що не беруться;
                   `files`    — файли з кореня гілки, що беруться поруч зі сторінками
                                (README.md: таблиці фреймворків і аддонів версії), адреса —
                                файл на GitHub.

Навіщо. Приклади коду сторінок Storybook лежать не в самій сторінці, а окремими файлами
`docs/_snippets/<ім'я>.md`, і сторінка ставить лише `<CodeSnippets path="ім'я.md" />`. Без
розгортання в корпус лягли б сторінки без жодного рядка коду. Сайт віддає markdown-двійник
сторінки (`.md`), але той губить код: з прикладу декоратора зникають `import` і `<Story />`
— JSX у коді він зрізає як розмітку. До того ж сайт тримає лише три останні мажорні версії,
а 6.5 і 7.6 живуть тільки на гілках `release-6-5` і `release-7-6`.

Файл прикладу — кілька огорож коду, кожна з атрибутами: `renderer` (react, vue, angular,
svelte, web-components, solid, preact, html, ember або `common` — для всіх), `language` (ts,
js, mdx…), `tabTitle` (вкладка: «CSF 3», «CSF Next 🧪», «Svelte CSF»), `packageManager`
(npm, yarn, pnpm), `filename`. Береться кожен фреймворк; з двох мов однієї вкладки — лише
TypeScript, JavaScript лишається там, де варіанта TypeScript немає. Перед огорожею — рядок-
підпис з іменем файла й атрибутами: без нього двадцять однакових на вигляд прикладів
сторінки не казали б, до якого фреймворку кожен.

Блоки `<If renderer="…">` / `<IfRenderer renderer='…'>` / `<If notRenderer={[…]}>` — текст,
який сайт показує лише для обраного фреймворку. Беруться всі, з підписом «Only for react,
vue:» чи «Not for angular:». Коментарі JSX `{/* … */}` — геть. Сторінки з `draft: true` у
шапці сайт не показує — не беруться; сторінки розділу з однією шапкою — теж.

Одиниця — сторінка на гілці: приклади залежать від гілки, тож та сама сторінка двох версій
дає два документи, а незмінні розділи зливаються вже в корпусі (`revision_suffix`).

Чому окремий модуль, а не формат у `site-history`: інші примірники зібрані й звірені, а
правка спільного читача — ризик зсуву в готовій роботі.
"""

import hashlib
import posixpath
import re
from html import unescape
from urllib.parse import quote

from engine.readers import Item, _markup, register
from engine.readers.ghhistory import _atx, _split_title
from engine.readers.k8sdocs import _blobs, _Site, front

_DOCS = "docs"
_SNIPPETS = "docs/_snippets/"
_EXTS = (".md", ".mdx")

_FENCE = re.compile(r"^(\s*)(```+|~~~+)(.*)$")
_JSX_COMMENT = re.compile(r"\{/\*.*?\*/\}", re.S)
_IF_OPEN = re.compile(r"<(?:If|IfRenderer)\b(.*?)>", re.S)
_IF_CLOSE = re.compile(r"</(?:If|IfRenderer)\s*>")
_IF_ATTR = re.compile(r"\b(not)?[Rr]enderer\s*=\s*(\"[^\"]*\"|'[^']*'|\{[^}]*\})")
_NAME = re.compile(r"[\"']([\w-]+)[\"']")
_SNIPPET_TAG = re.compile(r"^([ \t]*)<CodeSnippets\b(.*?)/>", re.S | re.M)
_PATH_ATTR = re.compile(r"\bpaths?=\{?\[?\s*[\"']([^\"']+)[\"']")
_ATTRS = re.compile(r"(\w+)=\"([^\"]*)\"")
_TS = ("ts", "tsx", "ts-4-9")
_LANGS = {"ts": "TS", "tsx": "TSX", "ts-4-9": "TS 4.9", "js": "JS", "jsx": "JSX", "mdx": "MDX"}


def _segments(text: str) -> list[tuple[bool, str]]:
    """Текст сторінки шматками «(код?, текст)»: правки розмітки не мають чіпати огорож."""
    out: list[tuple[bool, list]] = []
    fence = ""
    for ln in text.split("\n"):
        f = _FENCE.match(ln)
        if fence:
            out[-1][1].append(ln)
            if f and f.group(2)[0] == fence[0] and len(f.group(2)) >= len(fence) \
                    and not f.group(3).strip():
                fence = ""
            continue
        if f:
            fence = f.group(2)
            out.append((True, [ln]))
            continue
        if not out or out[-1][0]:
            out.append((False, []))
        out[-1][1].append(ln)
    return [(code, "\n".join(lines)) for code, lines in out]


def _fences(text: str) -> list[dict]:
    """Огорожі файла прикладу: атрибути шапки, мова огорожі й рядки коду."""
    found, cur, fence = [], None, ""
    for ln in text.split("\n"):
        f = _FENCE.match(ln)
        if cur is not None:
            if f and f.group(2)[0] == fence[0] and len(f.group(2)) >= len(fence) \
                    and not f.group(3).strip():
                found.append(cur)
                cur = None
            else:
                cur["code"].append(ln)
            continue
        if f:
            fence = f.group(2)
            info = f.group(3).strip()
            lang = info.split()[0] if info and not info.startswith(("{", "filename=")) else ""
            cur = {"lang": lang, "attrs": dict(_ATTRS.findall(info)), "code": []}
    return found


def _tab(title: str) -> str:
    """Вкладка без позначки мови: «ts-3» і «3», «story-function-ts» і «story-function-js»
    у старих прикладах — та сама вкладка двома мовами."""
    return "-".join(t for t in title.split("-") if t not in ("ts", "js"))


def _chosen(fences: list[dict]) -> list[dict]:
    """Усі фреймворки; з мов однієї вкладки — TypeScript, коли він є."""
    def key(f):
        a = f["attrs"]
        return a.get("renderer", ""), a.get("packageManager", ""), _tab(a.get("tabTitle", ""))
    typed = {key(f) for f in fences if f["attrs"].get("language", f["lang"]) in _TS}
    return [f for f in fences
            if not (key(f) in typed and f["attrs"].get("language", f["lang"]) in ("js", "jsx"))]


def _label(f: dict) -> str:
    a = f["attrs"]
    parts = []
    renderer = a.get("renderer", "")
    if renderer and renderer != "common":
        parts.append(renderer)
    lang = a.get("language", "")
    if lang:
        parts.append(_LANGS.get(lang, lang))
    for k in ("tabTitle", "packageManager"):
        if a.get(k):
            parts.append(a[k])
    name = a.get("filename", "")
    if name and parts:
        return f"`{name}` ({', '.join(parts)}):"
    if name:
        return f"`{name}`:"
    return f"{', '.join(parts)}:" if parts else ""


def _snippet(load, name: str, pad: str) -> str:
    text = load(name)
    if text is None:
        return ""
    out: list[str] = []
    for f in _chosen(_fences(text)):
        label = _label(f)
        if label:
            out.extend(["", pad + label])
        out.extend(["", f"{pad}```{f['lang']}"])
        out.extend(pad + x if x else x for x in f["code"])
        out.extend([f"{pad}```", ""])
    return "\n".join(out)


def _if_label(attrs: str) -> str:
    m = _IF_ATTR.search(attrs)
    if not m:
        return ""
    value = m.group(2)
    names = _NAME.findall(value) if value.startswith("{") else [value.strip("\"'")]
    if not names:
        return ""
    return f"{'Not' if m.group(1) else 'Only'} for {', '.join(names)}:"


def expand(text: str, load) -> str:
    """MDX сторінки Storybook у markdown: приклади на місці, блоки фреймворків з підписом."""
    out = []
    for code, part in _segments(text):
        if code:
            out.append(part)
            continue
        part = _JSX_COMMENT.sub("", part)
        part = _IF_OPEN.sub(lambda m: f"\n\n{_if_label(m.group(1))}\n\n", part)
        part = _IF_CLOSE.sub("\n\n", part)

        def snip(m):
            p = _PATH_ATTR.search(m.group(2))
            return _snippet(load, p.group(1), m.group(1)) if p else ""
        out.append(_SNIPPET_TAG.sub(snip, part))
    return "\n".join(out)


@register("storybook-docs")
def storybook_docs(source: dict, ctx) -> list[Item]:
    refs = source.get("refs")
    if not isinstance(refs, dict) or not refs:
        raise SystemExit(f"{source['id']}: читач storybook-docs потребує поля refs — об'єкта "
                         f"«гілка → версія».")
    sites = source.get("site") or {}
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    extra = [f.strip("/") for f in source.get("files") or ()]
    site = _Site(source, ctx)

    items = []
    for ref, version in refs.items():
        root = site.entries(ref)
        sha = site.subtree(root, _DOCS)
        if not sha:
            raise SystemExit(f"{source['id']}: на гілці {ref} немає теки {_DOCS}/.")
        files = _blobs(site.entries(sha, recursive=True), _DOCS + "/")
        files.update({e["path"]: (e["sha"], e.get("size", 0)) for e in root
                      if e.get("path") in extra and e.get("type") == "blob"})
        snippets = {p[len(_SNIPPETS):]: s for p, (s, _) in files.items()
                    if p.startswith(_SNIPPETS)}

        def load(name, ref=ref, snippets=snippets):
            name = posixpath.basename(name.strip())
            hit = snippets.get(name)
            return site.text(ref, _SNIPPETS + name, hit) if hit else None

        for path, (blob_sha, size) in sorted(files.items()):
            if (not path.endswith(_EXTS) or path.startswith(_SNIPPETS) or size == 0
                    or any(r.search(path) for r in exclude)):
                continue
            raw = site.raw(ref, path)
            if not ctx.allowed(raw):
                continue
            # Шапку видно лише в тексті: чернетку сайт не показує, і в корпус вона не йде.
            # Сторінка розділу без тексту (лише шапка — сайт малює під нею перелік
            # підсторінок) документом не стає. Текст лишається в пам'яті _Site — make()
            # бере його звідти.
            meta, rest, _ = front(site.text(ref, path, blob_sha) or "")
            if meta.get("draft", "").lower() == "true" or not rest.strip():
                continue
            rel = path[len(_DOCS) + 1:] if path not in extra else path
            stem = re.sub(r"\.mdx?$", "", rel)
            page_path = re.sub(r"(^|/)index$", "", stem)
            template = sites.get(ref) if path not in extra else None
            url = (template.format(path=page_path).rstrip("/") if template else
                   f"https://github.com/{site.owner}/{site.repo}/blob/"
                   f"{quote(ref, safe='@')}/{quote(path)}")
            key = f"{path}\0{blob_sha}\0{ref}"
            name = (f"{_markup.slug(page_path or 'index')}-"
                    f"{hashlib.sha1(key.encode()).hexdigest()[:8]}")

            def make(ref=ref, path=path, blob_sha=blob_sha, url=url, raw=raw, rel=rel,
                     version=str(version), load=load):
                meta, rest, _ = front(site.text(ref, path, blob_sha) or "")
                rest = _markup.mdx_statements_out(expand(rest, load))
                rest = _atx(rest)
                title = meta.get("title") or ""
                if not title:
                    title, rest = _split_title(rest)
                if not title:
                    title = posixpath.splitext(posixpath.basename(rel))[0]
                    if path in extra:
                        title = f"Storybook {title}"
                body = _markup.markdown_body(rest)
                title = unescape(title)
                _markup.require(title, body, raw, min_chars=1)
                return _markup.document(title, url, ctx.stamp, body, version)

            items.append(Item(id=f"{source['id']}/{name}",
                              file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: на жодній із {len(refs)} гілок не знайдено сторінок.")
    return items


# ── посібник з переходу ───────────────────────────────────────────────────────

_MIGRATION_HEAD = re.compile(r"^## +(From version +(\S+) +to +(\S+?))\s*$", re.M)


@register("storybook-migration")
def storybook_migration(source: dict, ctx) -> list[Item]:
    """`storybook-migration` — MIGRATION.md репозиторію, одна секція «## From version A to B» —
    один документ з версією B; зміст на початку файла (перелік посилань на всі секції) не
    береться. Поля: `url` — сирий файл, `cite` — адреса для людей, `min_major` — найменша
    мажорна версія B, що береться.

    Навіщо. Посібник — один файл на 400 КБ від 3.x до поточної, а його зміст — тисяча рядків
    посилань: одним документом він дав би десятки фрагментів-змістів, що відгукуються на
    будь-яку назву API, і жодна секція не мала б своєї версії."""
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    heads = list(_MIGRATION_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодної секції «## From version A to B» — формат "
                         f"змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Migration")
    min_major = int(source.get("min_major", 0))
    items = []
    for i, head in enumerate(heads):
        target = re.sub(r"(\.x)+$", "", head.group(3))
        if int(target.split(".")[0]) < min_major:
            continue
        heading = head.group(1)
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        name = _markup.slug(heading)

        def make(chunk=chunk, heading=heading, version=target):
            body = _markup.markdown_body(chunk)
            _markup.require(heading, body, f"{source['url']} {heading}", min_chars=1)
            url = f"{cite}#{_markup.github_anchor(heading)}"
            return _markup.document(f"{label}: {heading}", url, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
