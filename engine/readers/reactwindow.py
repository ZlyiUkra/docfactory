"""Читачі сайтів документації react-window: текст сторінок живе в коді репозиторію, а не в markdown.

`react-window-site-v1` — сайт лінії 1.x (react-window.now.sh, згодом react-window-v1.vercel.app; перша
                         тепер веде на сайт 2.x, друга віддає 404): сторінки тек
                         `website/src/routes/api/` і `website/src/routes/examples/`.
`react-window-site-v2` — сайт лінії 2.x (react-window.vercel.app): сторінки з карти маршрутів
                         `src/routes.ts`. Поле `site` — адреса сайту: сторінка, чий маршрут є в
                         карті найновішого тегу, цитується на сайті, решта — blob на GitHub.

Спільні поля: `url` — префікс дерев (…/repos/ВЛАСНИК/РЕПО/git/trees/), `tags` — об'єкт «тег або
коміт → версія», від найновішого. Версія, що вийшла в npm без тегу (1.2.3, 1.8.7, 1.8.8),
береться комітом `gitHead` з реєстру: дерево й сирі файли GitHub віддає і за комітом.

Навіщо. Markdown у сайтів немає, і загальний сканер `_jsx` сам по собі їх не прочитає:
- у 1.x довідник компонента — масиви `PROPS` і `METHODS` об'єктів `{ name: 'children',
  type: 'component', defaultValue: '""', isRequired: true, description: (<p>…</p>) }`.
  Сканер бере рядки в лапках лише прозою, тож «children» і «component» губилися б — лишався б
  опис без назви властивості. Тут кожен об'єкт стає розділом «## children» з типом і
  значенням за замовчуванням;
- код прикладів на обох сайтах вставляється з інших файлів: у 1.x `<CodeBlock value={CODE} />`
  з модуля `website/src/code/*.js`, у 2.x `<Code html={…} />` чи `<FormattedCode url=… />` з
  JSON, який скрипт сайту збирає з `src/routes/**/examples/*` між позначками `// <begin>` і
  `// <end>`. Код береться з тих самих вихідних файлів і стає блоком на місці вставки;
- сторінки властивостей 2.x (`<ComponentProps>`, `<ImperativeHandle>`) показують довідку,
  згенеровану з JSDoc: до 2.2.3 — JSON react-docgen-typescript (`public/generated/js-docs/`),
  з 2.2.4 — власний формат сайту (`public/generated/docs/`). Обидва стають розділами
  «## властивість»; атрибути DOM, успадковані з @types/react, відкидаються;
- заголовок сторінки 2.x — атрибут `<Header section="Lists" title="…" />`, а атрибути тегів
  сканер не читає.

Одиниця — як у `ghdocs-history`: сторінка разом з усім, що вона вставляє. Її ревізія — хеш
blob-ів сторінки й вставок, і однакова ревізія на кількох тегах — один документ з усіма їхніми
версіями. Щоб знати вставки, сторінка читається вже під час переліку (раз на кожен свій blob);
вставки тягнуться в `make`.
"""

import hashlib
import json
import posixpath
import re
from html import unescape
from urllib.parse import quote, urlsplit

from engine.readers import Item, _jsx, _markup, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_MARK = re.compile(r"@@(CODE|DOCS)@(\d+)@@")


class _Repo:
    """Дерева тегів і вміст blob-ів одного репозиторію; вміст — один раз на sha."""

    def __init__(self, source: dict, ctx):
        m = _TREES.match(urlsplit(source["url"]).path)
        if not m:
            raise SystemExit(f"{source['url']}: очікував префікс дерев "
                             f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
        self.owner, self.repo = m.groups()
        self.tags = source.get("tags")
        if not isinstance(self.tags, dict) or not self.tags:
            raise SystemExit(f"{source['id']}: потрібне поле tags — об'єкт «тег → версія».")
        self.source, self.ctx = source, ctx
        self.cache: dict = {}

    def trees(self):
        for tag in self.tags:
            url = f"{self.source['url']}{tag}?recursive=1"
            try:
                tree = json.loads(self.ctx.text(url))
            except ValueError as exc:
                raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
            if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
                raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
            if tree.get("truncated"):
                raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
            yield tag, {e["path"]: e["sha"] for e in tree["tree"] if e.get("type") == "blob"}

    def raw(self, tag: str, path: str) -> str:
        return (f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/"
                f"{quote(tag, safe='@')}/{quote(path)}")

    def blob(self, tag: str, path: str) -> str:
        return f"https://github.com/{self.owner}/{self.repo}/blob/{quote(tag, safe='@')}/{quote(path)}"

    def text(self, tag: str, path: str, sha: str) -> str:
        if sha not in self.cache:
            url = self.raw(tag, path)
            if not self.ctx.allowed(url):
                raise SystemExit(f"{url}: поза білим списком джерела.")
            text = self.ctx.text(url).replace("\r\n", "\n")
            _markup.refuse_html(text, url)
            self.cache[sha] = text
        return self.cache[sha]

    def version(self, found: list) -> str:
        # Кілька тегів з однією міткою — одна версія.
        return ", ".join(dict.fromkeys(str(self.tags[t]) for t in found))


def _revision(path: str, sha: str, deps: dict) -> str:
    key = " ".join([f"{path}:{sha}"] + [f"{p}:{s}" for p, s in sorted(deps.items())])
    return hashlib.sha1(key.encode()).hexdigest()[:8]


def _name(path: str, root: str, sha: str, deps: dict) -> str:
    """Ім'я документа: шлях сторінки без спільної теки сайту й без суфікса «Route» у 2.x
    (`api-fixedsizelist`, `list-dynamicrowheights`) плюс ревізія."""
    stem = re.sub(r"Route$", "", posixpath.splitext(path.removeprefix(root))[0])
    return f"{_markup.slug(stem)}-{_revision(path, sha, deps)}"


def _fence(code: str, lang: str) -> str:
    return f"\n\n```{lang}\n{code.strip(chr(10))}\n```\n\n"


def _with_marks(text: str, blocks: dict) -> str:
    """Позначки `@@CODE@n@@` / `@@DOCS@n@@` у тексті сканера → вставлені блоки."""
    out = _MARK.sub(lambda m: blocks.get(f"{m.group(1)}{m.group(2)}", ""), text)
    return re.sub(r"\n{3,}", "\n\n", out).strip()


# ── лінія 1.x ─────────────────────────────────────────────────────────────

_V1_PAGE = re.compile(r"^website/src/routes/(api|examples)/[^/]+\.js$")
_V1_IMPORT = re.compile(r"^import\s+(\w+)\s+from\s+['\"](\.[^'\"]+)['\"];?[ \t]*$", re.M)
_V1_CODEBLOCK = re.compile(r"<CodeBlock\s+value=\{(\w+)\}\s*/>")
_V1_TEMPLATE = re.compile(r"^\s*export\s+default\s*`(.*)`;?\s*$", re.S)


def _v1_imports(src: str, path: str, blobs: dict) -> dict:
    """Ідентифікатор → шлях модуля коду, який сторінка імпортує з `website/src/code/`."""
    out = {}
    for ident, spec in _V1_IMPORT.findall(src):
        target = posixpath.normpath(posixpath.join(posixpath.dirname(path), spec))
        if "/code/" in target and target in blobs:
            out[ident] = target
    return out


def _v1_code(text: str) -> str:
    # Ранні теги тримали приклад рядком-шаблоном модуля, пізні — сирим файлом для raw-loader.
    m = _V1_TEMPLATE.match(text)
    return m.group(1).replace("\\`", "`").replace("\\${", "${") if m else text


def _js_string(value: str) -> str:
    value = value.strip().rstrip(",").strip()
    parts = re.findall(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"", value)
    if not parts:
        return value
    return "".join(a or b for a, b in parts).replace("\\'", "'").replace('\\"', '"')


def _v1_entries(src: str, const: str) -> list:
    """Об'єкти масиву `const PROPS = [ … ];` за відступами prettier: об'єкт — від «  {» до
    «  },», поле — рядок з відступом у чотири пробіли, продовження поля — глибші рядки."""
    m = re.search(rf"^const {const} = \[\n(.*?)^\];", src, re.M | re.S)
    if not m:
        return []
    out = []
    for chunk in re.split(r"^  \},?[ \t]*$", m.group(1), flags=re.M):
        fields: dict = {}
        current = None
        for line in chunk.split("\n"):
            fm = re.match(r"^    (\w+):\s?(.*)$", line)
            if fm:
                current = fm.group(1)
                fields[current] = [fm.group(2)]
            elif current and line.startswith("     "):
                fields[current].append(line)
        if fields:
            out.append({k: "\n".join(v).strip() for k, v in fields.items()})
    return out


def _jsx_text(jsx: str, codes: dict, blocks: dict) -> str:
    """Шматок JSX → текст; `<CodeBlock value={X} />` → блок коду модуля X."""
    def mark(m):
        key = f"CODE{len(blocks)}"
        blocks[key] = _fence(codes.get(m.group(1), ""), "jsx")
        return f"<p>@@CODE@{len(blocks) - 1}@@</p>"
    return unescape(_jsx.text_of(_V1_CODEBLOCK.sub(mark, jsx)))


def _v1_nav(app: str) -> dict:
    """Назви сторінок з меню сайту (`App.js`): шлях файла сторінки → назва пункту. Заголовок
    `<h1>` сторінки прикладу назвою не годиться: сторінка мемоізованих рядків — копія базового
    прикладу й теж каже «Basic List»."""
    files = {ident: posixpath.normpath(posixpath.join("website/src", spec)) + ".js"
             for ident, spec in re.findall(r"^import\s+(\w+)\s+from\s+'(\./routes/[^']+)'", app, re.M)}
    out = {}
    for title, ident in re.findall(r"title:\s*'([^']+)',\s*component:\s*(\w+)", app):
        if ident in files:
            out[files[ident]] = title
    return out


def _v1_render(src: str, codes: dict, stem: str, nav_title: str = "") -> tuple[str, str]:
    blocks: dict = {}
    start = src.find("<ComponentApi")
    if start >= 0:
        # Атрибути елемента тягнуться на кілька рядків і містять JSX (`propsIntro={<p>…</p>}`),
        # тож межа елемента — кінець виразу `export default () => (…);`.
        end = src.find("\n);", start)
        element = src[start:end if end > 0 else len(src)]
        name = re.search(r'\bname="(\w+)"', element)
        parts = []
        for key in ("propsIntro", "methodsIntro"):
            intro = re.search(rf"\b{key}=\{{(.*?)\n    \}}", element, re.S)
            if intro:
                parts.append(_jsx_text("x = (" + intro.group(1) + ");", codes, blocks))
        for entry in _v1_entries(src, "PROPS"):
            prop = _js_string(entry.get("name", ""))
            facts = []
            if entry.get("type"):
                facts.append(f"type `{_js_string(entry['type'])}`")
            if entry.get("defaultValue"):
                facts.append(f"default `{_js_string(entry['defaultValue'])}`")
            facts.append("required" if entry.get("isRequired", "").startswith("true")
                         else "optional")
            desc = entry.get("description", "")
            desc = re.sub(r"^\(\s*|\s*\)\s*,?$", "", desc.rstrip(","))
            parts.append(f"## {prop}\n\nProp: {', '.join(facts)}.\n\n"
                         f"{_jsx_text('x = (' + desc + ');', codes, blocks)}")
        for entry in _v1_entries(src, "METHODS"):
            signature = _js_string(entry.get("signature", ""))
            desc = re.sub(r"^\(\s*|\s*\)\s*,?$", "", entry.get("description", "").rstrip(","))
            parts.append(f"## {signature}\n\nMethod.\n\n"
                         f"{_jsx_text('x = (' + desc + ');', codes, blocks)}")
        title = name.group(1) if name else nav_title or stem
        return title, _with_marks("\n\n".join(parts), blocks)
    method = re.search(r'<Method\b[^>]*\bname="(\w+)"', src)
    if method:
        return method.group(1), _with_marks(_jsx_text(src, codes, blocks), blocks)
    # Сторінка прикладу: над `export default` лежать живі демо-компоненти, і їхній JSX
    # («{item.label} is {…}») — не текст сторінки.
    body = src[src.find("export default"):] if "export default" in src else src
    text = _jsx_text(body, codes, blocks)
    h1 = re.search(r"<h1\b[^>]*>\s*([^<{]+?)\s*</h1>", src)
    heading = nav_title or (h1.group(1) if h1 else stem)
    # Заголовок сторінки — назвою з меню і розділом, як у 2.x: `<h1>` сторінки мемоізованих
    # рядків — копія базового прикладу («Basic List»).
    text = re.sub(r"^#{1,2}\s+.*\n?", "", text.lstrip("\n"), count=1) if h1 else text
    return f"Example: {heading}", _with_marks(f"## {heading}\n\n{text}", blocks)


@register("react-window-site-v1")
def react_window_site_v1(source: dict, ctx) -> list[Item]:
    repo = _Repo(source, ctx)
    seen: dict = {}
    for tag, blobs in repo.trees():
        for path in sorted(p for p in blobs if _V1_PAGE.match(p)):
            sha = blobs[path]
            src = repo.text(tag, path, sha)
            deps = {p: blobs[p] for p in _v1_imports(src, path, blobs).values()}
            name = _name(path, "website/src/routes/", sha, deps)
            # Меню (`App.js`) дає лише назву і в ревізію не входить: інакше кожен новий пункт
            # меню робив би нову редакцію всіх сторінок.
            entry = seen.setdefault(name, {"path": path, "sha": sha, "deps": deps, "tag": tag,
                                           "app": blobs.get("website/src/App.js"), "tags": []})
            entry["tags"].append(tag)

    items = []
    for name, e in seen.items():
        def make(e=e):
            tag, path = e["tag"], e["path"]
            src = repo.text(tag, path, e["sha"])
            imports = _v1_imports(src, path, e["deps"])
            codes = {ident: _v1_code(repo.text(tag, p, e["deps"][p]))
                     for ident, p in imports.items()}
            nav = _v1_nav(repo.text(tag, "website/src/App.js", e["app"])) if e["app"] else {}
            stem = posixpath.splitext(posixpath.basename(path))[0]
            title, body = _v1_render(src, codes, stem, nav.get(path, ""))
            url = repo.blob(tag, path)
            _markup.require(title, body, url, min_chars=1)
            return _markup.document(title, url, ctx.stamp, body, repo.version(e["tags"]))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодної сторінки website/src/routes/ на жодному тезі.")
    return items


# ── лінія 2.x ─────────────────────────────────────────────────────────────

_V2_LAZY = re.compile(r'"(/[^"]*)"\s*:\s*lazy\(\s*\(\)\s*=>\s*import\(\s*"\./([^"]+)"\s*\)\s*\)')
_V2_IDENT = re.compile(r'"(/[^"]*)"\s*:\s*([A-Z]\w*)\s*(?=[,}\n])')
_V2_NAMED = re.compile(r'import\s*\{\s*(\w+)\s*\}\s*from\s*"\./([^"]+)"')
_V2_JSON_IMPORT = re.compile(
    r'^import\s+(?:(\w+)|\{\s*html\s+as\s+(\w+)\s*\})\s+from\s+"([^"]*public/generated/[^"]+\.json)"',
    re.M)
_V2_URL = re.compile(r'url="/(generated/[^"]+\.json)"')
_V2_CODE_EL = re.compile(r"<(?:Code|FormattedCode)\b([^>]*?)/>", re.S)
_V2_DOCS_EL = re.compile(r"<(ComponentProps|ImperativeHandle)\b([^>]*?)/>", re.S)
_V2_HEADER = re.compile(r"<Header\b([^>]*?)/>", re.S)
_SNIPPET_DIRS = ("public/generated/code-snippets/", "public/generated/examples/")
_DOCS_DIRS = ("public/generated/js-docs/", "public/generated/docs/")


def _v2_routes(src: str) -> dict:
    """Карта маршрутів → {шлях файла сторінки: маршрут}. Два вигляди карти: `lazy(() =>
    import("./routes/…"))` (з 2.0.1) і ім'я компонента з іменованим імпортом (2.0.0)."""
    named = {ident: mod for ident, mod in _V2_NAMED.findall(src)}
    pairs = list(_V2_LAZY.findall(src))
    pairs += [(route, named[ident]) for route, ident in _V2_IDENT.findall(src) if ident in named]
    out: dict = {}
    for route, module in pairs:
        if route in ("*", "/test") or not route.startswith("/"):
            continue
        out.setdefault(f"src/{module}", route)
    return out


def _v2_page_file(module: str, blobs: dict) -> str | None:
    return next((module + ext for ext in (".tsx", ".ts") if module + ext in blobs), None)


def _v2_refs(src: str, path: str) -> tuple[dict, list]:
    """Ідентифікатори імпортованих JSON → шлях у дереві; і всі JSON, на які сторінка посилається
    (імпортом чи атрибутом `url`), у порядку появи."""
    idents, refs = {}, []
    for default, html_as, spec in _V2_JSON_IMPORT.findall(src):
        target = posixpath.normpath(posixpath.join(posixpath.dirname(path), spec))
        idents[default or html_as] = target
        refs.append(target)
    refs += [f"public/{u}" for u in _V2_URL.findall(src)]
    return idents, list(dict.fromkeys(refs))


def _v2_snippet_source(json_path: str, page: str, blobs: dict) -> str | None:
    """Вихідний файл прикладу, з якого зібрано JSON сніпета: `…/examples/X.example.tsx`
    (до 2.2.3) чи `…/examples/X.tsx` (з 2.2.4). Спершу — у теці розділу самої сторінки."""
    name = re.escape(posixpath.splitext(posixpath.basename(json_path))[0])
    rx = re.compile(rf"^src/routes/(?:.+/)?examples/{name}(?:\.example)?\.(?:tsx|ts|html)$")
    hits = sorted(p for p in blobs if rx.match(p))
    near = [p for p in hits if p.startswith(posixpath.dirname(page) + "/")]
    return (near or hits or [None])[0]


def _v2_deps(src: str, path: str, blobs: dict) -> dict:
    """JSON-посилання → шлях, з якого береться вміст: для сніпета — вихідний приклад (або сам
    JSON, якщо прикладу не знайшлося), для довідки — JSON."""
    out = {}
    for ref in _v2_refs(src, path)[1]:
        if ref.startswith(_SNIPPET_DIRS):
            out[ref] = _v2_snippet_source(ref, path, blobs) or (ref if ref in blobs else None)
        elif ref.startswith(_DOCS_DIRS) and ref in blobs:
            out[ref] = ref
    return {k: v for k, v in out.items() if v}


def _code_html(html: str) -> str:
    """Підсвічений код сайту (рядок — `<div>`, токен — `<span>`) → сирий код."""
    html = re.sub(r"</div>\s*", "\n", html)
    html = re.sub(r"<br\s*/?>", "\n", html)
    return unescape(re.sub(r"<[^>]+>", "", html)).rstrip()


def _snippet(text: str, path: str) -> tuple[str, str]:
    """Вміст сніпета й мова блоку. Приклад показується на сайті лише між позначками."""
    if path.endswith(".json"):
        data = json.loads(text)
        html = data.get("html") or data.get("typeScript") or data.get("javaScript") or ""
        return _code_html(html), "tsx"
    # Позначки бувають і поодинці: лише `// <end>` (усе до неї) чи лише `// <begin>`.
    marks = list(re.finditer(r"^[ \t]*//\s*<(begin|end)>[^\n]*\n?", text, re.M))
    if not marks:
        code = text
    else:
        pieces, start = [], 0 if marks[0].group(1) == "end" else None
        for m in marks:
            if m.group(1) == "begin":
                start = m.end()
            elif start is not None:
                pieces.append(text[start:m.start()])
                start = None
        if start is not None:
            pieces.append(text[start:])
        code = "\n\n".join(p.strip("\n") for p in pieces)
    return code, {".html": "html", ".ts": "ts"}.get(posixpath.splitext(path)[1], "tsx")


def _notes(items) -> str:
    """Опис у власному форматі довідки: список шматків HTML з необов'язковим `intent`."""
    out = []
    for piece in items or []:
        if isinstance(piece, dict):
            text = _markup.html_body(str(piece.get("content") or ""))
            lead = {"warning": "Warning: ", "danger": "Warning: "}.get(piece.get("intent"), "")
            out.append(lead + text)
        elif isinstance(piece, str):
            out.append(piece.strip())
    return "\n\n".join(p for p in out if p)


def _docs(text: str) -> tuple[str, str]:
    """Довідка JSON → (ім'я сутності, markdown). Атрибути, оголошені лише в node_modules
    (HTMLAttributes з @types/react), — не властивості react-window."""
    data = json.loads(text)
    parts = []
    if "displayName" in data:
        name = str(data.get("displayName") or "")
        if data.get("description"):
            parts.append(str(data["description"]).strip())
        for key, prop in (data.get("props") or {}).items():
            decls = prop.get("declarations") or []
            if decls and all("node_modules" in str(d.get("fileName", "")) for d in decls):
                continue
            kind = prop.get("type") or {}
            facts = ["required" if prop.get("required") else "optional"]
            if kind.get("raw") or kind.get("name"):
                facts.insert(0, f"type `{kind.get('raw') or kind.get('name')}`")
            default = (prop.get("defaultValue") or {}).get("value") \
                if isinstance(prop.get("defaultValue"), dict) else None
            if default not in (None, ""):
                facts.append(f"default `{default}`")
            parts.append(f"## {key}\n\nProp of {name}: {', '.join(facts)}.\n\n"
                         f"{str(prop.get('description') or '').strip()}")
        for method in data.get("methods") or []:
            parts.append(f"## {method.get('name', '')}\n\n{method.get('docblock') or ''}")
    else:
        name = str(data.get("name") or "")
        if data.get("description"):
            parts.append(_notes(data["description"]))
        for key, prop in (data.get("props") or {}).items():
            signature = _code_html(str(prop.get("html") or ""))
            parts.append(f"## {key}\n\nProp of {name}: "
                         f"{'required' if prop.get('required') else 'optional'}."
                         f"{_fence(signature, 'ts') if signature else ''}"
                         f"{_notes(prop.get('description'))}")
        for method in data.get("methods") or []:
            signature = _code_html(str(method.get("html") or ""))
            mname = method.get("name") or (re.match(r"\s*(\w+)", signature) or [""])[0].strip()
            parts.append(f"## {mname}\n\nMethod of {name}."
                         f"{_fence(signature, 'ts') if signature else ''}"
                         f"{_notes(method.get('description'))}")
    return name, "\n\n".join(p.strip() for p in parts if p.strip())


def _attr(attrs: str, key: str) -> str:
    m = re.search(rf'\b{key}=(?:"([^"]*)"|\{{\s*"([^"]*)"\s*\}})', attrs)
    return (m.group(1) or m.group(2) or "") if m else ""


def _v2_render(src: str, path: str, route: str, texts: dict) -> tuple[str, str]:
    """Сторінка 2.x → (назва, текст). `texts` — {JSON-посилання: (вміст, шлях вмісту)}."""
    idents, _ = _v2_refs(src, path)
    blocks: dict = {}
    head = _V2_HEADER.search(src)
    section, title = (_attr(head.group(1), "section"), _attr(head.group(1), "title")) \
        if head else ("", "")

    def ref_of(attrs: str) -> str:
        url = _V2_URL.search(attrs)
        if url:
            return f"public/{url.group(1)}"
        ident = re.search(r"=\{\s*(\w+)", attrs)
        return idents.get(ident.group(1), "") if ident else ""

    def code(m):
        ref = ref_of(m.group(1))
        if ref not in texts:
            return ""
        body, lang = _snippet(*texts[ref])
        blocks[f"CODE{len(blocks)}"] = _fence(body, lang)
        return f"<p>@@CODE@{len(blocks) - 1}@@</p>"

    doc_names = []

    def docs(m):
        ref = ref_of(m.group(2))
        if ref not in texts:
            return ""
        name, body = _docs(texts[ref][0])
        doc_names.append(name)
        blocks[f"DOCS{len(blocks)}"] = f"\n\n{body}\n\n"
        return f"<p>@@DOCS@{len(blocks) - 1}@@</p>"

    s = _V2_HEADER.sub(lambda m: f"<h1>{_attr(m.group(1), 'title')}</h1>", src)
    s = re.sub(r"<(/?)SectionHeader\b[^>]*>", r"<\1h2>", s)
    # Підзаголовок сторінки — блок із великим шрифтом, а не тег заголовка.
    s = re.sub(r'<div className="text-(?:lg|xl|2xl)\b[^"]*">\s*([^<{]+?)\s*</div>', r"<h2>\1</h2>", s)
    # Посилання «далі» внизу сторінки — навігація, а не текст.
    s = re.sub(r"<ContinueLink\b[^>]*?/>", "", s, flags=re.S)
    s = re.sub(r"<Callout\b([^>]*)>",
               lambda m: "<div>" + ("Warning: " if "warning" in m.group(1) else "Note: "), s)
    s = s.replace("</Callout>", "</div>")
    s = _V2_CODE_EL.sub(code, s)
    s = _V2_DOCS_EL.sub(docs, s)
    text = unescape(_jsx.text_of(s))
    if title:
        # Заголовок `<Header>` лишається і розділом: без жодного розділу сторінка була б для
        # пошуку самою «шапкою», а на ціль заміру годиться лише розділ із текстом.
        title = f"{section}: {title}" if section else title
    else:
        words = [w for w in route.strip("/").split("/") if w]
        title = (f"{words[0].capitalize()}: {' '.join(words[1:]).replace('-', ' ')}"
                 if len(words) > 1 else (doc_names[0] if doc_names else route))
    return title, _with_marks(text, blocks)


@register("react-window-site-v2")
def react_window_site_v2(source: dict, ctx) -> list[Item]:
    repo = _Repo(source, ctx)
    site = str(source.get("site") or "").rstrip("/")
    newest_routes: set = set()
    seen: dict = {}
    for tag, blobs in repo.trees():
        if "src/routes.ts" not in blobs:
            continue
        mapping = _v2_routes(repo.text(tag, "src/routes.ts", blobs["src/routes.ts"]))
        files = {}
        for module, route in mapping.items():
            page = _v2_page_file(module, blobs)
            if page:
                files[page] = route
        # Сайт показує лише найновіше видання: на нього посилаються маршрути, що в ньому є.
        if not newest_routes:
            newest_routes.update(files.values())
        for path in sorted(files):
            sha = blobs[path]
            # Ключ вставки — «посилання>шлях вмісту»: той самий приклад може стояти за двома
            # JSON (до і після перейменування тек), а ревізію визначає саме вміст.
            deps = {f"{ref}>{where}": blobs[where] for ref, where in
                    _v2_deps(repo.text(tag, path, sha), path, blobs).items()}
            name = _name(path, "src/routes/", sha, deps)
            entry = seen.setdefault(name, {"path": path, "sha": sha, "deps": deps, "tag": tag,
                                           "route": files[path], "tags": []})
            entry["tags"].append(tag)

    items = []
    for name, e in seen.items():
        def make(e=e):
            tag, path, route = e["tag"], e["path"], e["route"]
            src = repo.text(tag, path, e["sha"])
            texts = {}
            for key, sha in e["deps"].items():
                ref, where = key.split(">", 1)
                texts[ref] = (repo.text(tag, where, sha), where)
            title, body = _v2_render(src, path, route, texts)
            url = f"{site}{route}" if site and route in newest_routes else repo.blob(tag, path)
            _markup.require(title, body, repo.blob(tag, path), min_chars=1)
            return _markup.document(title, url, ctx.stamp, body, repo.version(e["tags"]))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодної сторінки з карти src/routes.ts на жодному тезі.")
    return items
