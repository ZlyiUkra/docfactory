"""Читач довідника API Angular з коду пакетів на тегах: символ публічного API — документ.

`ng-api-history` — `url` — префікс дерев через API (…/repos/angular/angular/git/trees/), `tags` —
                   об'єкт «тег → версія» від найновішого. `packages` — вираз імені пакета, чий API
                   береться (`core|common|router|…`); `registry` — початок адреси опису пакета в
                   реєстрі (типово `https://registry.npmjs.org/@angular/`).

Навіщо. Довідник API сайтів Angular генерується з коду, і кожен сайт тримає лише останню мінорну
свого мажора, а v12–v17.angular.io сторінок core, common, router, forms уже не віддають зовсім
(404). Те, з чого їх генерували, є для кожної версії: перелік публічних символів кожної точки
входу — «золоті» файли перевірки публічного API на тегах репозиторію (`tools/public_api_guard/…`
у 2.x–8.x, `goldens/public-api/…` з 9.0: спершу `.d.ts`, з 14 — звіт API Extractor `.md`), а опис
символу — коментар JSDoc у файлах типів (`.d.ts`) пакета npm тієї самої версії. Разом це та сама
сторінка довідника: назва, точка входу, опис, примітки до використання, оголошення з членами і
опис кожного члена.

Перелік символів — із золотого файла, а не з позначок: `@publicApi` стоїть не на всьому (у 22.x
його немає, наприклад, над `signal`), а в 2.x–6.x замість нього `@stable`/`@experimental`.
Оголошення — теж із золотого файла: там воно чисте, саме таке, яке бачить користувач пакета. Опис —
з тарбола, а не з коду репозиторію: типи пакета мають ті самі коментарі, а тарбол на пакет і версію
— один запит замість тисяч файлів коду. Тарбол читається по одному й одразу відпускається; маршрутизатор
2.x має власну нумерацію (`@angular/router` 3.4 — це Angular 2.4).

Документ — неповторний текст символу точки входу; у його версії лягають усі теги, де текст був
саме таким. Ім'я — «ngapi-<точка входу>-<символ>-<хеш>»: `revision_suffix` зрізає хеш, і редакції
одного символу зливаються. Ім'я, що починається з малої літери, дістає ще й вид оголошення
(`input` → «…-input-const»): в одній точці входу живуть і декоратор `Input`, і функція `input`, а
ключ розділу регістру не розрізняє. Адреса в шапці — сторінка довідника сайту мажора (v4–v11,
v18+); для 2.x і 12–17, де сайт її не віддає, — золотий файл на GitHub.

Тексти документів складено вже під час переліку (щоб звести однакові, їх треба скласти) і в пам'яті
лежать стиснутими.

Чому окремий модуль: читачі коду (`ghcode-history-ts`) дають код файлами, а не довідник символів,
і в інших примірниках уже звірені.
"""

import hashlib
import io
import json
import re
import sys
import tarfile
import zlib
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, _ngdocs, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_GOLDEN = re.compile(r"^(?:goldens/public-api|tools/public_api_guard)/(.+?)\.(?:api\.md|md|d\.ts)$")
_DECL = re.compile(r"^export\s+(?:declare\s+)?(?:default\s+)?(?:abstract\s+)?(?:async\s+)?"
                   r"(class|interface|function|const|let|var|type|enum|namespace)\s+([\w$]+)")
# Оголошення з коментарем у файлі типів пакета: `export declare class X` у 2.x–12.x, а в зведеному
# `index.d.ts` 13+ — `declare class X` без `export` (перелік експорту стоїть наприкінці файла).
_DOC_DECL = re.compile(r"/\*\*((?:(?!\*/).)*)\*/\s*(?:@[\w.]+(?:\((?:[^()]|\([^()]*\))*\))?\s*)*"
                       r"(?:export\s+)?(?:declare\s+)?(?:default\s+)?(?:abstract\s+)?(?:async\s+)?"
                       r"(class|interface|function|const|let|var|type|enum)\s+([\w$]+)", re.S)
_MEMBER = re.compile(r"/\*\*((?:(?!\*/).)*)\*/\s*(?:@[\w.]+(?:\((?:[^()]|\([^()]*\))*\))?\s*)*"
                     r"(?:(?:public|protected|readonly|static|abstract|override|declare|async|get|set)\s+)*"
                     r"([\w$]+)\s*[?!]?\s*[(:<=;]", re.S)
_LINK = re.compile(r"\{@link(?:Docs|plain|code)?\s+([^\s}]+)(?:\s+([^}]*))?\}")
_EXAMPLE_REF = re.compile(r"\{@example\s+([^\s}]+)([^}]*)\}")
_EX_ATTR = re.compile(r"""(\w+)\s*=\s*['"]([^'"]*)['"]""")
# Приклади JSDoc лежать у пакеті `examples` репозиторію: `modules/@angular/examples` у 2.x, далі
# `packages/examples`; шлях у `{@example}` — від цієї теки. Опис service-worker бере приклад посібника —
# з `aio/content/examples`, згодом `adev/src/content/examples`.
_EX_ROOTS = ("packages/examples/", "modules/@angular/examples/", "aio/content/examples/",
             "adev/src/content/examples/")
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


def _jsdoc(raw: str, example=None) -> str:
    """Сирий коментар JSDoc → markdown: теги стають підписами, `{@link X}` — назвою, а
    `{@example шлях region='…'}` — кодом цієї області з `packages/examples` того самого тегу
    (`example(шлях, область)` дає блок коду або None — тоді лишається рядок «Example: шлях»)."""
    lines = [re.sub(r"^\s*\* ?", "", ln) for ln in raw.replace("\r\n", "\n").split("\n")]
    text = "\n".join(lines).strip()
    text = _LINK.sub(lambda m: (m.group(2) or m.group(1)).strip(), text)

    def ex(m):
        attrs = dict(_EX_ATTR.findall(m.group(2) or ""))
        code = example(m.group(1), attrs.get("region", "")) if example else None
        return code if code else f"Example: `{m.group(1)}`"
    text = _EXAMPLE_REF.sub(ex, text)
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


def _npm_version(versions: dict, pkg: str, version: str) -> str:
    """Версія пакета npm, що відповідає тегу: та сама; у 2.x маршрутизатор має свою нумерацію
    (`@angular/router` 3.4 — це Angular 2.4); інакше — найновіший патч тієї самої мінорної."""
    if version in versions:
        return version
    major, minor = version.split(".")[:2]
    lines = [f"{major}.{minor}."] + (["3." + minor + "."] if pkg == "router" and major == "2" else [])
    for line in reversed(lines):
        same = [v for v in versions if v.startswith(line) and re.fullmatch(r"\d+\.\d+\.\d+", v)]
        if same:
            return max(same, key=lambda v: int(v.split(".")[2]))
    return ""


def _site(entry: str, name: str, version: str, fallback: str) -> str:
    """Сторінка довідника для людей: сайт мажора, якщо він її ще віддає, інакше — золотий файл."""
    major = int(version.split(".")[0])
    if 4 <= major <= 11:
        return f"https://v{major}.angular.io/api/{entry}/{name}"
    if 18 <= major <= 21:
        return f"https://v{major}.angular.dev/api/{entry}/{name}"
    if major >= 22:
        return f"https://angular.dev/api/{entry}/{name}"
    return fallback


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
    registry = str(source.get("registry") or "https://registry.npmjs.org/@angular/")
    golden_cache: dict = {}
    ex_seen: list = []   # (тег, версія, {шлях прикладу: sha}) пройдених тегів, від найновішого
    ex_cache: dict = {}  # sha файла прикладу → текст
    tarballs: dict = {}  # пакет → {версія: адреса тарбола}
    # (точка входу, ім'я, вид) → {хеш тексту: [версії]}; хеш → (стиснутий текст, адреса)
    found: dict = {}
    texts: dict = {}

    def raw(tag: str, path: str) -> str:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{quote(tag, safe='@')}/{quote(path)}"
        code, data = ctx.fetch(url) if ctx.allowed(url) else ("", b"")
        return data.decode("utf-8", errors="replace") if code == "200" else ""

    def package_docs(pkg: str, version: str) -> dict:
        """{ім'я: [(вид, JSDoc, {член: JSDoc}, шлях)]} з файлів типів тарбола пакета цієї версії."""
        if pkg not in tarballs:
            url = registry + pkg
            try:
                meta = json.loads(ctx.text(url, gzip=True)) if ctx.allowed(url) else {}
            except (SystemExit, ValueError) as exc:
                print(f"  {source['id']}: опис пакета {url} не прочитано ({exc})", flush=True)
                meta = {}
            tarballs[pkg] = {v: ((d or {}).get("dist") or {}).get("tarball", "")
                             for v, d in (meta.get("versions") or {}).items()}
        v = _npm_version(tarballs[pkg], pkg, version)
        url = tarballs[pkg].get(v, "")
        if not url or not ctx.allowed(url):
            return {}
        try:
            data = ctx.bytes(url)
        except SystemExit as exc:
            print(f"  {source['id']}: {exc}", flush=True)
            return {}
        out: dict = {}
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as tar:
            for member in tar:
                if not (member.isfile() and member.name.endswith(".d.ts")):
                    continue
                text = tar.extractfile(member).read().decode("utf-8", errors="replace")
                for name, decls in _source_docs(text).items():
                    out.setdefault(name, []).extend(
                        (k, d, mem, member.name.split("/", 1)[-1]) for k, d, mem in decls)
        return out

    for tag, version in tags.items():
        version = str(version)
        tree = json.loads(ctx.text(f"{source['url']}{tag}?recursive=1"))
        if tree.get("truncated"):
            raise SystemExit(f"{tag}: GitHub обрізав дерево — перелік був би неповним.")
        goldens = [(e["path"], e["sha"]) for e in tree.get("tree", []) if e.get("type") == "blob"
                   and _GOLDEN.match(e["path"])
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
        ex_files = {sys.intern(e["path"]): sys.intern(e["sha"]) for e in tree.get("tree", [])
                    if e.get("type") == "blob" and e["path"].startswith(_EX_ROOTS)}
        ex_seen.append((tag, version, ex_files))

        def example(rel: str, region_name: str, tag=tag, version=version) -> str | None:
            # Той самий тег, а як там файла немає — найближчий уже пройдений (новіший) тег.
            for t, v, files in reversed(ex_seen):
                for root in _EX_ROOTS:
                    path = root + rel
                    sha = files.get(path)
                    if not sha:
                        continue
                    if sha not in ex_cache:
                        ex_cache[sha] = raw(t, path)
                    if not ex_cache[sha]:
                        continue
                    code = _ngdocs.region(ex_cache[sha], region_name)
                    ext = rel.rsplit(".", 1)[-1]
                    head = rel + (f" ({region_name})" if region_name else "")
                    block = _ngdocs._fence(code, _ngdocs._LANG.get(ext, ext), head).strip("\n")
                    # Код не з тегу документа — так і сказано рядком над ним.
                    return block if t == tag else (
                        f"Example code from tag {v}: the file is not in tag {version}.\n\n{block}")
            # Посилання, за яким файла немає ні на цьому тезі, ні на жодному новішому (опис
            # NG_VALIDATORS у 2.x–4.0): сайт показував тут порожнє місце — так і сказано.
            return (f"The example file `{rel}` referenced here does not exist in the repository at "
                    f"tag {version} or any later tag.")

        # Описи — з типів тарбола кожного пакета цього тегу; тарбол читається один раз на тег.
        docs = {pkg: package_docs(pkg, version)
                for pkg in sorted({e.split("/", 1)[0] for e in entries})}
        for entry, (gpath, blocks) in entries.items():
            pkg = entry.split("/", 1)[0]
            by_name: dict = {}
            for kind, name, code, dep in blocks:
                if not name.startswith("ɵ"):
                    by_name.setdefault(name, []).append((kind, code, dep))
            golden_url = (f"https://github.com/{owner}/{repo}/blob/{quote(tag, safe='@')}/"
                          f"{quote(gpath)}")
            for name, decls in by_name.items():
                kinds = list(dict.fromkeys(k for k, _, _ in decls))
                # Найперше — оголошення з позначкою публічного API, далі решта того самого імені.
                src = sorted(docs[pkg].get(name, []),
                             key=lambda d: ("@publicApi" not in d[1] and "@stable" not in d[1], d[3]))
                parts = [f"Entry point: `@angular/{entry}`  ", f"Kind: {', '.join(kinds)}"]
                if any(dep for _, _, dep in decls):
                    parts.append("Status: deprecated")
                seen_docs = []
                for kind, doc, members, path in src:
                    rendered = _jsdoc(doc, example)
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
                        text = _jsdoc(mdocs[member], example)
                        if text:
                            body.append(f"## {member}\n\n{text}")
                text = "\n\n".join(body)
                digest = hashlib.sha1(f"{entry}\n{name}\n{text}".encode()).hexdigest()
                found.setdefault((entry, name, kinds[0]), {}).setdefault(digest, []).append(version)
                if digest not in texts:
                    texts[digest] = (zlib.compress(text.encode(), 6),
                                     _site(entry, name, version, golden_url))
        del docs
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
