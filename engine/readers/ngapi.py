"""Читач довідника API Angular з коду пакетів на тегах: символ публічного API — документ.

`ng-api-history` — `url` — префікс дерев через API (…/repos/angular/angular/git/trees/), `tags` —
                   об'єкт «тег → версія» від найновішого. `packages` — вираз імені пакета, чий API
                   береться (`core|common|router|…`); необов'язкове `exclude` — вирази шляхів файлів
                   коду, що не читаються (тести, схеми, приклади).

Навіщо. Довідник API сайтів Angular генерується з коду, і кожен сайт тримає лише останню мінорну
свого мажора, а v12–v17.angular.io сторінок core, common, router, forms уже не віддають зовсім
(404). Те, з чого їх генерували, лежить у репозиторії на кожному тезі: перелік публічних символів
кожної точки входу — «золоті» файли перевірки публічного API (`tools/public_api_guard/…` у 2.x–8.x,
`goldens/public-api/…` з 9.0: спершу `.d.ts`, з 14 — звіт API Extractor `.md`), а опис символу —
коментар JSDoc над його оголошенням у коді пакета. Разом це та сама сторінка довідника: назва, точка
входу, опис, примітки до використання, оголошення з членами і опис кожного члена.

Перелік символів — із золотого файла, а не з позначок у коді: `@publicApi` стоїть не на всьому
(у 22.x його немає, наприклад, над `signal`), а в 2.x–6.x замість нього `@stable`/`@experimental`.
Оголошення в документі — теж із золотого файла: там воно чисте, без тіла, саме таке, яке бачить
користувач пакета. Опис — з коду того самого тегу: усі файли `.ts` пакета (без тестів) читаються,
і коментар JSDoc шукається за ім'ям символу в межах пакета.

Документ — неповторний текст символу точки входу; у його версії лягають усі теги, де текст був
саме таким. Ім'я — «ngapi-<точка входу>-<символ>-<хеш>»: `revision_suffix` зрізає хеш, і редакції
одного символу зливаються. Ім'я, що починається з малої літери, дістає ще й вид оголошення
(`input` → «…-input-const»): в одній точці входу живуть і декоратор `Input`, і функція `input`, а
ключ розділу регістру не розрізняє.

Тексти документів зібрані вже під час переліку (щоб звести однакові, їх треба скласти), і в пам'яті
лежать стиснутими; файли коду читаються по одному разу на неповторний вміст (хеш blob).

Чому окремий модуль: читачі коду (`ghcode-history-ts`) дають код файлами, а не довідник символів,
і в інших примірниках уже звірені.
"""

import hashlib
import json
import posixpath
import re
import zlib
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_GOLDEN = re.compile(r"^(?:goldens/public-api|tools/public_api_guard)/(.+?)\.(?:api\.md|md|d\.ts)$")
_SRC_ROOT = re.compile(r"^(?:packages|modules/@angular)/([\w-]+)/")
_DECL = re.compile(r"^export\s+(?:declare\s+)?(?:default\s+)?(?:abstract\s+)?(?:async\s+)?"
                   r"(class|interface|function|const|let|var|type|enum|namespace)\s+([\w$]+)")
_DOC_DECL = re.compile(r"/\*\*((?:(?!\*/).)*)\*/\s*(?:@[\w.]+(?:\((?:[^()]|\([^()]*\))*\))?\s*)*"
                       r"export\s+(?:declare\s+)?(?:default\s+)?(?:abstract\s+)?(?:async\s+)?"
                       r"(class|interface|function|const|let|var|type|enum)\s+([\w$]+)", re.S)
_MEMBER = re.compile(r"/\*\*((?:(?!\*/).)*)\*/\s*(?:@[\w.]+(?:\((?:[^()]|\([^()]*\))*\))?\s*)*"
                     r"(?:(?:public|protected|readonly|static|abstract|override|declare|async|get|set)\s+)*"
                     r"([\w$]+)\s*[?!]?\s*[(:<=;]", re.S)
_LINK = re.compile(r"\{@link(?:Docs|plain|code)?\s+([^\s}]+)(?:\s+([^}]*))?\}")
_EXAMPLE_REF = re.compile(r"\{@example\s+([^\s}]+)[^}]*\}")
_DROP_TAGS = {"publicApi", "stable", "Annotation", "nodoc", "codeGenApi", "internal", "docsNotRequired",
              "docs-private", "ngInjectableDef", "globalApi", "docs-public", "breaking-change", "suppress",
              "ngModule", "overriddenImplementation", "pureOrBreakMyCode", "nocollapse"}
_SKIP_DOC = re.compile(r"@(?:internal|nodoc|codeGenApi|docs-private)\b")
_SKIP_ENTRY = re.compile(r"^(?:compiler|compiler-cli|bazel|language-service|benchpress|private|zone\.js|"
                         r"localize/tools|core/primitives)(?:/|$)")


def _entry(golden_path: str) -> str:
    """`goldens/public-api/core/testing/index.api.md` → «core/testing»; `…/core/core.d.ts` → «core»."""
    m = _GOLDEN.match(golden_path)
    parts = [p for p in m.group(1).split("/") if p not in ("index", "typings")] if m else []
    if len(parts) >= 2 and parts[-1] == parts[-2]:
        parts.pop()
    return "/".join(parts)


def _golden_blocks(text: str) -> list[tuple[str, str, str, bool]]:
    """(вид, ім'я, оголошення, застаріле) кожного верхнього `export` золотого файла."""
    m = re.search(r"```ts\n(.*?)```", text, re.S)
    body = m.group(1) if m else text
    out, cur, notes, depth = [], None, [], 0
    for line in body.split("\n"):
        if depth == 0:
            d = _DECL.match(line)
            if d:
                if cur:
                    out.append(cur)
                deprecated = any("@deprecated" in n for n in notes)
                cur = [d.group(1), d.group(2), [line], deprecated]
                notes = []
            elif line.startswith("//") or line.strip().startswith(("/**", "*")):
                if cur and depth == 0:
                    out.append(cur)
                    cur = None
                notes.append(line)
                continue
            elif not line.strip():
                if cur and depth == 0:
                    out.append(cur)
                    cur = None
                continue
            elif cur:
                cur[2].append(line)
        elif cur:
            cur[2].append(line)
        depth += line.count("{") - line.count("}")
        depth = max(depth, 0)
    if cur:
        out.append(cur)
    result = []
    for kind, name, lines, dep in out:
        code = "\n".join(ln for ln in lines if not ln.strip().startswith("// (undocumented)"))
        result.append((kind, name, code.strip(), dep))
    return result


def _body_of(text: str, start: int) -> str:
    """Тіло класу чи інтерфейсу від `{` після `start` до парної `}` (рядки й коментарі — грубо)."""
    i = text.find("{", start)
    if i < 0:
        return ""
    depth, j, n = 0, i, len(text)
    while j < n:
        c = text[j]
        if c in "\"'`":
            q, j = c, j + 1
            while j < n and text[j] != q:
                j += 2 if text[j] == "\\" else 1
        elif c == "/" and text.startswith("//", j):
            j = text.find("\n", j)
            j = n if j < 0 else j
        elif c == "/" and text.startswith("/*", j):
            j = text.find("*/", j)
            j = n if j < 0 else j + 1
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1:j]
        j += 1
    return text[i + 1:]


def _source_docs(text: str) -> dict:
    """{ім'я: [(вид, сирий JSDoc, {член: сирий JSDoc})]} — оголошення з коментарем у файлі коду."""
    out: dict = {}
    for m in _DOC_DECL.finditer(text):
        doc, kind, name = m.group(1), m.group(2), m.group(3)
        if _SKIP_DOC.search(doc) and "@publicApi" not in doc:
            continue
        members = {}
        if kind in ("class", "interface"):
            for mm in _MEMBER.finditer(_body_of(text, m.end())):
                if not _SKIP_DOC.search(mm.group(1)):
                    members.setdefault(mm.group(2), mm.group(1))
        out.setdefault(name, []).append((kind, doc, members))
    return out


def _jsdoc(raw: str) -> str:
    """Сирий коментар JSDoc → markdown: теги стають підписами, `{@link X}` — назвою."""
    lines = [re.sub(r"^\s*\* ?", "", ln) for ln in raw.replace("\r\n", "\n").split("\n")]
    text = "\n".join(lines).strip()
    text = _LINK.sub(lambda m: (m.group(2) or m.group(1)).strip(), text)
    text = _EXAMPLE_REF.sub(lambda m: f"Example: `{m.group(1)}`", text)
    out, params, fence = [], [], False
    for ln in text.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
            out.append(ln)
            continue
        m = None if fence else re.match(r"^@([\w-]+)\s*(.*)$", ln.strip())
        if not m:
            out.append(ln)
            continue
        tag, rest = m.group(1), m.group(2).strip()
        if tag in _DROP_TAGS:
            continue
        if tag == "description" or tag == "whatItDoes":
            out.append(rest)
        elif tag == "usageNotes":
            out += ["", "## Usage notes", "", rest]
        elif tag == "howToUse":
            out += ["", "## How to use", "", rest]
        elif tag == "param":
            p = re.match(r"^(?:\{[^}]*\}\s*)?\[?([\w$.]+)\]?\s*-?\s*(.*)$", rest)
            params.append(f"- `{p.group(1)}` — {p.group(2)}" if p else f"- {rest}")
            out.append("\x00param")
        elif tag in ("returns", "return"):
            out.append(f"Returns: {rest}")
        elif tag == "throws":
            out.append(f"Throws: {rest}")
        elif tag == "deprecated":
            out.append(f"**Deprecated:** {rest}")
        elif tag == "see":
            out.append(f"See also: {rest}")
        elif tag == "experimental":
            out.append("Stability: experimental" + (f" — {rest}" if rest else ""))
        elif tag == "developerPreview":
            out.append("Stability: developer preview" + (f" — {rest}" if rest else ""))
        elif tag == "example":
            out += ["", "Example:", rest]
        else:
            out.append(f"{tag}: {rest}" if rest else tag)
    # Параметри — одним переліком на місці першого @param.
    res, done = [], False
    for ln in out:
        if ln == "\x00param":
            if not done:
                res += ["", "Parameters:", *params, ""]
                done = True
            continue
        res.append(ln)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(res)).strip()


def _member_names(code: str) -> list[str]:
    names = []
    for ln in code.split("\n")[1:]:
        m = re.match(r"^\s{4}(?:(?:protected|readonly|static|abstract|get|set)\s+)*([\w$]+)\s*[?!]?\s*[(:<]",
                     ln)
        if m and m.group(1) not in names:
            names.append(m.group(1))
    return names


@register("ng-api-history")
def ng_api_history(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев /repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or not tags:
        raise SystemExit(f"{source['id']}: читач ng-api-history потребує поля tags.")
    packages = re.compile(rf"^(?:{source.get('packages') or 'core'})$")
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    parsed: dict = {}   # sha файла коду → _source_docs
    golden_cache: dict = {}
    # (точка входу, ім'я) → {хеш тексту: [версії]}; хеш → (стиснутий текст, адреса)
    found: dict = {}
    texts: dict = {}

    def raw(tag: str, path: str) -> str:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{quote(tag, safe='@')}/{quote(path)}"
        code, data = ctx.fetch(url) if ctx.allowed(url) else ("", b"")
        return data.decode("utf-8", errors="replace") if code == "200" else ""

    for tag, version in tags.items():
        tree = json.loads(ctx.text(f"{source['url']}{tag}?recursive=1"))
        if tree.get("truncated"):
            raise SystemExit(f"{tag}: GitHub обрізав дерево — перелік був би неповним.")
        blobs = [e for e in tree.get("tree", []) if e.get("type") == "blob"]
        goldens = [(e["path"], e["sha"]) for e in blobs if _GOLDEN.match(e["path"])
                   and not e["path"].endswith(("errors.api.md", "errors.md", "global_utils.api.md",
                                               "global_utils.md", "global_utils.d.ts"))]
        entries: dict = {}
        for path, sha in goldens:
            entry = _entry(path)
            pkg = entry.split("/", 1)[0]
            if not entry or not packages.match(pkg) or _SKIP_ENTRY.match(entry):
                continue
            if sha not in golden_cache:
                golden_cache[sha] = _golden_blocks(raw(tag, path))
            entries[entry] = (path, golden_cache[sha])
        if not entries:
            continue
        # Описи — з коду пакетів, чиї точки входу є в золотих файлах цього тегу.
        wanted = {e.split("/", 1)[0] for e in entries}
        docs: dict = {}   # пакет → ім'я → [(вид, doc, members, шлях)]
        for e in blobs:
            path = e["path"]
            r = _SRC_ROOT.match(path)
            if (not r or r.group(1) not in wanted or not path.endswith(".ts")
                    or path.endswith(".d.ts") or any(x.search(path) for x in exclude)):
                continue
            if e["sha"] not in parsed:
                parsed[e["sha"]] = _source_docs(raw(tag, path))
            for name, decls in parsed[e["sha"]].items():
                for kind, doc, members in decls:
                    docs.setdefault(r.group(1), {}).setdefault(name, []).append(
                        (kind, doc, members, path))
        for entry, (gpath, blocks) in entries.items():
            pkg = entry.split("/", 1)[0]
            by_name: dict = {}
            for kind, name, code, dep in blocks:
                if name.startswith("ɵ"):
                    continue
                by_name.setdefault(name, []).append((kind, code, dep))
            for name, decls in by_name.items():
                kinds = list(dict.fromkeys(k for k, _, _ in decls))
                src = docs.get(pkg, {}).get(name, [])
                # Найперше — оголошення з позначкою публічного API, далі решта того самого імені.
                src = sorted(src, key=lambda d: ("@publicApi" not in d[1] and "@stable" not in d[1],
                                                 d[3]))
                parts = [f"Entry point: `@angular/{entry}`  ", f"Kind: {', '.join(kinds)}"]
                if any(dep for _, _, dep in decls):
                    parts.append("Status: deprecated")
                seen_docs = []
                for kind, doc, members, path in src:
                    rendered = _jsdoc(doc)
                    if rendered and rendered not in seen_docs:
                        seen_docs.append(rendered)
                body = ["\n".join(parts), *seen_docs]
                code = "\n\n".join(c for _, c, _ in decls)
                body.append(f"```ts\n{code}\n```")
                mdocs: dict = {}
                for kind, doc, members, path in src:
                    for k, v in members.items():
                        mdocs.setdefault(k, v)
                for member in _member_names(code):
                    if member in mdocs:
                        text = _jsdoc(mdocs[member])
                        if text:
                            body.append(f"## {member}\n\n{text}")
                text = "\n\n".join(body)
                where = src[0][3] if src else gpath
                url = f"https://github.com/{owner}/{repo}/blob/{quote(tag, safe='@')}/{quote(where)}"
                digest = hashlib.sha1(f"{entry}\n{name}\n{text}".encode()).hexdigest()
                key = (entry, name, kinds[0])
                found.setdefault(key, {}).setdefault(digest, []).append(str(version))
                if digest not in texts:
                    texts[digest] = (zlib.compress(text.encode(), 6), url)
    if not found:
        raise SystemExit(f"{source['id']}: на жодному з {len(tags)} тегів не знайдено золотих файлів API.")
    items = []
    for (entry, name, kind), revs in found.items():
        tail = _markup.slug(name) + (f"-{kind}" if name[:1].islower() else "")
        for digest, versions in revs.items():
            doc = f"ngapi-{_markup.slug(entry)}-{tail}-{digest[:8]}"

            def make(digest=digest, versions=versions, entry=entry, name=name):
                blob, url = texts[digest]
                body = zlib.decompress(blob).decode()
                return _markup.document(f"{name} (@angular/{entry})", url, ctx.stamp, body,
                                        ", ".join(dict.fromkeys(versions)))

            items.append(Item(id=f"{source['id']}/{doc}", file=f"{source['id']}--{doc}.txt", make=make))
    return items
