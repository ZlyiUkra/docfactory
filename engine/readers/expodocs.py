"""Читачі документації Expo з історії репозиторію expo/expo: довідник кожного SDK і посібники
на кожен SDK.

`expo-sdk-history`    — теки версій сайту docs.expo.dev (`docs/pages/versions/v57.0.0`,
                        у 2018–2019 роках — `docs/versions/v31.0.0`) для кожного стабільного SDK.
`expo-guides-history` — сторінки сайту поза теками версій (посібники Expo Router, EAS,
                        Modules API, config plugins, tutorial) у стані на кінець кожного SDK.

Спільні поля:
- `url` — префікс дерев (…/repos/expo/expo/git/trees/), `branch` — гілка;
- `versions` — https://registry.npmjs.org/expo: SDK — мажорна версія пакета `expo`, найновіший
  стабільний — мажор мітки `latest` (мітка `next` — бета наступного SDK, не береться);
  `min_sdk` — найстаріший SDK, що береться;
- `exclude` — вирази відносних шляхів сторінок, що не беруться;
- `scan` — вирази відносних шляхів сторінок, чий текст залежить від файлів даних (див. нижче);
- `site` — адреса сторінки на сайті, `{path}` — шлях сторінки без розширення (і без `index`).

Звідки тека SDK. Та, що лежить на гілці, — з вершини; прибрана — зі знімка перед комітом, що
її видалив (як у `docusaurus-versions`, з тим самим кроком назад, якщо коміт лишив у теці
залишок). До 2019 року теки версій лежали в `docs/versions/`, потім — у `docs/pages/versions/`:
з двох місць береться те, де тека жила пізніше. Тека `react-native/` у старих SDK — копія
документації React Native, яка в цій фабриці має власний примірник; її відкидає `exclude`.

Посібники. До SDK ~37 посібники жили всередині теки версії (`guides/`, `workflow/`), і для
таких SDK окремого знімка не треба. Пізніше вони переїхали на верх сайту і версій не мають;
тут їхній стан для SDK X — останній коміт теки `docs/` перед виходом `expo@X+1.0.0`, а для
найновішого стабільного SDK — вершина гілки. Сторінка, що не змінювалася, — один документ з
усіма SDK, де вона була такою.

Файли даних. Сайт не пише API модулів у сторінці: `<APISection packageName="expo-camera" />`
малює розділ із JSON TypeDoc того самого SDK (`docs/public/static/data/v57.0.0/expo-camera.json`,
див. `_typedocjson`), а довідник `app.json` — з JSON Schema, імпортованої рядком `import schema
from '~/public/static/schemas/v57.0.0/app-config-schema.json'`. Однакова сторінка двох SDK з
різними даними — два різні тексти, а які файли сторінка бере, видно лише з її тексту. Тож
сторінки з `scan` у версіях, де файли даних є, — окремий документ на кожну версію; однакові
розділи різних версій зливаються вже в корпусі.

Розбір MDX. Крім виносок і вкладок, у текст розгортаються компоненти, чий зміст лежить у
властивостях: `<Terminal cmd={[…]}>` (команди терміналу), `<FileTree files={[…]}>`,
`<APIInstallSection />` (`npx expo install пакет`), `<ConfigPluginProperties properties={[…]}>`,
`<AndroidPermissions>`/`<IOSPermissions permissions={[…]}>`, підписи `<Tab label>`,
`<Collapsible summary>`, `<Step label>`, `<BoxLink title description>`.
"""

import json
import posixpath
import re
from html import unescape
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, _typedocjson, register
from engine.readers.ghhistory import _NotLiteral, _atx, _js_skip, _js_value, _split_title

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_STABLE = re.compile(r"^\d+\.\d+\.\d+$")
_PAGE = (".md", ".mdx")
_FOLDERS = ("pages/versions/v{sdk}.0.0", "versions/v{sdk}.0.0")
_DATA = "public/static/data/v{sdk}.0.0/"
_API = re.compile(r"<APISection\b([^>]*?)/?>", re.S)
_ATTR = re.compile(r"(\w+)=(?:\"([^\"]*)\"|'([^']*)'|\{([^{}]*)\})")
_IMPORT = re.compile(r"^import\s+(\w+)\s+from\s+['\"]~/((?:public/static|scripts)/[^'\"]+)['\"];?\s*$",
                     re.M)
# Схеми app.json і eas.json: до ~SDK 45 сайт тримав їх у `docs/scripts/schemas/` модулями JS
# (`export default {…}`), потім — у `docs/public/static/schemas/`.
_SCHEMAS = ("public/static/schemas/", "scripts/schemas/")
_SCHEMA_TAG = re.compile(r"<(\w+)\b[^<>]*?\bschema=\{(\w+)\}[^<>]*?/>", re.S)
_OLD_GUIDES = ("guides/", "workflow/")
_IMPORT_END = re.compile(r"(\bfrom\s+|^import\s+)['\"][^'\"]+['\"];?[ \t]*$")
# Позначки підсвічування коду сайту: `/* @info Пояснення */ … /* @end */`, `/* @hide … */`.
_CODE_MARK = re.compile(r"[ \t]*/\* @(?:info|end|hide|tutinfo)\b.*?\*/")


def _key(v: str) -> int:
    return int(v)


def _json(ctx, url: str):
    try:
        return json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")


class _Repo:
    """Знімки теки `docs/` репозиторію: шлях від `docs/` → blob. Тримаються лише сторінки,
    дані API й схеми: решта дерева (картинки, код сайту) — тисячі шляхів, які не потрібні."""

    def __init__(self, source: dict, ctx):
        m = _TREES.match(urlsplit(source["url"]).path)
        if not m:
            raise SystemExit(f"{source['url']}: очікував префікс дерев "
                             f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
        self.owner, self.repo = m.groups()
        self.source, self.ctx = source, ctx
        self.branch = source.get("branch", "main")
        self.api = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        self.snaps: dict = {}

    def commits(self, path: str = "docs", until: str = "", n: int = 1) -> list:
        url = (f"{self.api}/commits?sha={quote(self.branch)}&path={quote(path)}&per_page={n}"
               + (f"&until={until}" if until else ""))
        return _json(self.ctx, url) or []

    def snapshot(self, ref: str) -> dict:
        if ref not in self.snaps:
            root = _json(self.ctx, f"{self.source['url']}{ref}")
            docs = next((e["sha"] for e in root.get("tree") or ()
                         if e.get("path") == "docs" and e.get("type") == "tree"), "")
            files: dict = {}
            if docs:
                data = _json(self.ctx, f"{self.source['url']}{docs}?recursive=1")
                if data.get("truncated"):
                    raise SystemExit(f"{ref}: GitHub обрізав дерево docs/ — перелік був би "
                                     f"неповним.")
                for e in data.get("tree") or ():
                    p = e.get("path", "")
                    if e.get("type") == "blob" and (
                            (p.startswith(("pages/", "versions/")) and p.endswith(_PAGE))
                            or (p.startswith("public/static/data/") and p.endswith(".json"))
                            or p.startswith(_SCHEMAS)):
                        files[p] = e["sha"]
            self.snaps[ref] = files
        return self.snaps[ref]

    def raw(self, ref: str, path: str) -> str:
        return (f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{ref}/docs/"
                f"{quote(path)}")


def _sdks(source: dict, ctx) -> list[str]:
    pack = _json(ctx, source["versions"])
    latest = str((pack.get("dist-tags") or {}).get("latest", "0")).split(".")[0]
    low = int(source.get("min_sdk") or 0)
    majors = {v.split(".")[0] for v in pack.get("versions") or {} if _STABLE.match(v)}
    keep = [m for m in majors if low <= int(m) <= int(latest)]
    return sorted(keep, key=_key, reverse=True)


def _times(source: dict, ctx) -> dict:
    """SDK → мить виходу `expo@SDK.0.0` (ISO)."""
    pack = _json(ctx, source["versions"])
    times = pack.get("time") or {}
    return {v.split(".")[0]: times[v] for v in pack.get("versions") or {}
            if re.fullmatch(r"\d+\.0\.0", v) and v in times}


def _folders(repo: _Repo, sdks: list, head: str) -> dict:
    """SDK → (знімок, тека від docs/) для кожного SDK, чия тека версії є в історії."""
    where: dict = {}
    prev = 0
    for sdk in sdks:
        found = None
        snap = repo.snapshot(head)
        for f in _FOLDERS:
            folder = f.format(sdk=sdk)
            if any(p.startswith(folder + "/") for p in snap):
                found = (head, folder)
                break
        if not found:
            best = None
            for f in _FOLDERS:
                folder = f.format(sdk=sdk)
                last = repo.commits(f"docs/{folder}", n=5)
                if last and (not best or last[0]["commit"]["committer"]["date"] > best[0]):
                    best = (last[0]["commit"]["committer"]["date"], folder, last)
            if best:
                _, folder, last = best
                for commit in last:
                    ref = commit["sha"]
                    if not any(p.startswith(folder + "/") for p in repo.snapshot(ref)):
                        if not commit.get("parents"):
                            continue
                        ref = commit["parents"][0]["sha"]
                    found = (ref, folder)
                    count = sum(p.startswith(folder + "/") for p in repo.snapshot(ref))
                    # Залишок теки після архівного коміту — крок назад, до повної теки.
                    if not prev or count >= prev / 2:
                        break
        if found:
            where[sdk] = found
            prev = sum(p.startswith(found[1] + "/") for p in repo.snapshot(found[0]))
    return where


def _attrs(tag: str) -> dict:
    return {m.group(1): next(g for g in m.groups()[1:] if g is not None) for m in _ATTR.finditer(tag)}


def _deps(text: str) -> tuple[list, dict]:
    """(пакети `<APISection>`, {ім'я імпорту: шлях файла даних від docs/})."""
    pkgs = [_attrs(m.group(1)).get("packageName", "") for m in _API.finditer(text)]
    imports = {m.group(1): m.group(2) for m in _IMPORT.finditer(text)}
    return [p for p in pkgs if p], imports


# ── розбір сторінки ─────────────────────────────────────────────────────────────

def _prop(text: str, start: int, name: str):
    """Значення JSX-властивості `name={…}` елемента, що починається з `start`: (значення,
    кінець елемента) або (None, кінець). Значення — літерал JS, розібраний `_js_value`."""
    end = _tag_end(text, start)
    m = re.compile(rf"\b{name}\s*=\s*\{{").search(text, start, end)
    if not m:
        return None, end
    try:
        value, j = _js_value(text, m.end())
    except (_NotLiteral, IndexError):
        return None, end
    return value, end


def _tag_end(text: str, start: int) -> int:
    """Кінець відкривального тегу JSX (після `>`), з урахуванням `{…}` і рядків у властивостях."""
    depth, i, quote_ = 0, start, ""
    while i < len(text):
        c = text[i]
        if quote_:
            if c == "\\":
                i += 1
            elif c == quote_:
                quote_ = ""
        elif c in "\"'`" and depth:
            quote_ = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == ">" and depth <= 0:
            return i + 1
        i += 1
    return len(text)


def _lines(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out = []
        for v in value:
            out += _lines(v)
        return out
    return []


def _terminal(value) -> str:
    if isinstance(value, dict):
        value = value.get("npm") or next(iter(value.values()), [])
    cmds = [ln for ln in _lines(value) if ln.strip()]
    return "\n```sh\n" + "\n".join(cmds) + "\n```\n" if cmds else ""


def _file_tree(value) -> str:
    rows = []
    for row in value if isinstance(value, list) else ():
        if isinstance(row, list) and row:
            rows.append(f"{row[0]}" + (f"  # {row[1]}" if len(row) > 1 and row[1] else ""))
        elif isinstance(row, str):
            rows.append(row)
    return "\n```\n" + "\n".join(rows) + "\n```\n" if rows else ""


def _props_table(value) -> str:
    rows = []
    for row in value if isinstance(value, list) else ():
        if not isinstance(row, dict) or not row.get("name"):
            continue
        bits = []
        if row.get("platform"):
            bits.append(f"platform: {row['platform']}")
        if row.get("default") not in (None, "", "-"):
            bits.append(f"default: `{row['default']}`")
        desc = " ".join(" ".join(_lines(row.get("description"))).split())
        rows.append(f"- `{row['name']}`" + (f" ({', '.join(bits)})" if bits else "")
                    + (f" — {desc}" if desc else ""))
    return "\n" + "\n".join(rows) + "\n" if rows else ""


def _schema_rows(node, depth: int = 0, heads: bool = False) -> list[str]:
    """JSON Schema (`app-config-schema.json`) чи масив властивостей eas.json → вкладений список.
    `heads` — властивості верхнього рівня схеми стають підрозділами `### назва`."""
    rows: list[str] = []
    pad = "  " * depth
    # Схема app.json сайту — уже сама мапа «властивість → опис», без обгортки `properties`.
    if (isinstance(node, dict) and not isinstance(node.get("properties"), dict) and node
            and all(isinstance(v, dict) for v in node.values())):
        node = {"properties": node}
    if isinstance(node, dict) and isinstance(node.get("properties"), dict):
        for name, spec in node["properties"].items():
            if not isinstance(spec, dict):
                continue
            meta = spec.get("meta") or {}
            if meta.get("hidden") or meta.get("deprecated") and depth > 2:
                continue
            kind = spec.get("type") or ("enum" if spec.get("enum") else "")
            kind = " | ".join(kind) if isinstance(kind, list) else kind
            bits = [f"`{kind}`"] if kind else []
            if spec.get("enum"):
                bits.append("one of " + ", ".join(f"`{e}`" for e in spec["enum"][:12]))
            if meta.get("deprecated"):
                bits.append("deprecated")
            if meta.get("bareWorkflow"):
                bits.append(f"bare workflow: {' '.join(str(meta['bareWorkflow']).split())}")
            desc = " ".join(str(spec.get("markdownDescription") or spec.get("description")
                                or "").split())
            if heads:
                # Окремий розділ на властивість, як якір на сайті: інакше весь довідник
                # app.json (~35 тис. символів) — один розділ «Properties», і запит про
                # ios.bundleIdentifier у ньому тоне.
                about = " — ".join(x for x in ("; ".join(bits), desc) if x)
                rows += ["", f"### {name}", ""] + ([about, ""] if about else [])
                rows += _schema_rows(spec)
                if isinstance(spec.get("items"), dict):
                    rows += _schema_rows(spec["items"])
                continue
            rows.append(f"{pad}- `{name}`" + (f" ({'; '.join(bits)})" if bits else "")
                        + (f" — {desc}" if desc else ""))
            if depth < 4:
                rows += _schema_rows(spec, depth + 1)
                if isinstance(spec.get("items"), dict):
                    rows += _schema_rows(spec["items"], depth + 1)
    elif isinstance(node, list):
        for spec in node:
            if not isinstance(spec, dict) or not spec.get("name"):
                continue
            kind = spec.get("type")
            kind = " | ".join(kind) if isinstance(kind, list) else kind
            bits = [f"`{kind}`"] if kind else []
            if spec.get("enum"):
                bits.append("one of " + ", ".join(f"`{e}`" for e in spec["enum"][:12]))
            desc = " ".join(" ".join(_lines(spec.get("description"))).split())
            rows.append(f"{pad}- `{spec['name']}`" + (f" ({'; '.join(bits)})" if bits else "")
                        + (f" — {desc}" if desc else ""))
            if depth < 4 and spec.get("properties"):
                rows += _schema_rows(spec["properties"], depth + 1)
    return rows


# Модуль схеми eas.json розгортає чужі константи («enum: ['default',
# ...ResourceClasses.android]»): їхніх значень у знімку немає, а одне розгортання валило
# розбір усього модуля. Тож розгортання стає рядком «…»: у переліку видно, що значень
# більше, а серед властивостей рядок пропускається, бо це не опис.
_JS_SPREAD = re.compile(r"(?<=[\[{,])(\s*)\.\.\.[A-Za-z_$][\w$.]*(?=\s*[,\]}])")


def _js_default(text: str):
    """`export default [ … ]` модуля схеми eas.json → значення."""
    m = re.search(r"export\s+default\s+", text)
    if not m:
        return None
    text = text[:m.end()] + _JS_SPREAD.sub(r"\1'…'", text[m.end():])
    try:
        return _js_value(text, _js_skip(text, m.end()))[0]
    except (_NotLiteral, IndexError):
        return None


_LABEL_TAGS = {"Tab": "label", "Collapsible": "summary", "Step": "label",
               "Requirement": "title", "Prerequisites": "summary", "PaddedAPIBox": "header"}
_DATA_TAGS = ("Terminal", "FileTree", "ConfigPluginProperties", "AndroidPermissions",
              "IOSPermissions", "APIInstallSection", "APISection", "BoxLink")


def _expand(text: str, meta: dict, api, schemas: dict) -> str:
    """Компоненти MDX сайту Expo → текст (див. опис модуля). `api(пакет)` — markdown розділу
    API або ""; `schemas` — {ім'я імпорту: розібрані дані}."""
    out, i = [], 0
    rx = re.compile(r"<(" + "|".join(_DATA_TAGS + tuple(_LABEL_TAGS)) + r")\b"
                    r"|<(\w+)\b(?=[^<>]*?\bschema=\{)")
    fence = re.compile(r"^\s*(```|~~~)", re.M)
    # Огорожі коду: усередині них теги — приклад, а не компонент.
    spans, open_at = [], None
    for m in fence.finditer(text):
        if open_at is None:
            open_at = m.start()
        else:
            spans.append((open_at, m.end()))
            open_at = None
    for m in rx.finditer(text):
        if m.start() < i or any(a <= m.start() < b for a, b in spans):
            continue
        tag = m.group(1) or m.group(2)
        end = _tag_end(text, m.start())
        attrs = _attrs(text[m.start():end])
        repl = None
        if tag == "Terminal":
            value, end = _prop(text, m.start(), "cmd")
            repl = _terminal(value)
        elif tag == "FileTree":
            value, end = _prop(text, m.start(), "files")
            repl = _file_tree(value)
        elif tag == "ConfigPluginProperties":
            value, end = _prop(text, m.start(), "properties")
            repl = _props_table(value)
        elif tag in ("AndroidPermissions", "IOSPermissions"):
            value, end = _prop(text, m.start(), "permissions")
            names = _lines(value)
            label = "Android permissions" if tag.startswith("Android") else "iOS permissions"
            repl = f"\n{label}: {', '.join(f'`{n}`' for n in names)}.\n" if names else ""
        elif tag == "APIInstallSection":
            pkg = attrs.get("packageName") or meta.get("packageName") or ""
            cmd = attrs.get("cmd") or (f"npx expo install {pkg}" if pkg else "")
            repl = f"\n```sh\n{cmd}\n```\n" if cmd else ""
        elif tag == "APISection":
            repl = "\n" + api(attrs.get("packageName", "")) + "\n"
        elif tag == "BoxLink":
            title = attrs.get("title", "")
            desc = attrs.get("description", "")
            repl = f"\n{title}" + (f" — {desc}" if desc else "") + "\n" if title else ""
        elif tag in _LABEL_TAGS:
            label = attrs.get(_LABEL_TAGS[tag], "")
            repl = f"\n\n{label}:\n\n" if label else "\n\n"
        else:
            name = re.search(r"\bschema=\{(\w+)\}", text[m.start():end])
            rows = _schema_rows(schemas.get(name.group(1)), heads=True) if name else []
            repl = "\n" + "\n".join(rows) + "\n" if rows else ""
        out += [text[i:m.start()], repl]
        i = end
    return "".join(out) + text[i:]


def _imports_out(text: str) -> str:
    """Імпорти MDX поза кодом — геть, разом із багаторядковими (`import {⏎ A,⏎ B,⏎} from '…'`):
    mdx_statements_out знімає лише перший рядок, і решта списку лишалася в тексті. Рядки
    `import` усередині блоків коду — частина прикладу, вони лишаються; з коду знімаються
    тільки позначки підсвічування."""
    out, fence, inside = [], False, False
    for line in text.split("\n"):
        if re.match(r"^\s*(```|~~~)", line) and not inside:
            fence = not fence
            out.append(line)
            continue
        if fence:
            out.append(_CODE_MARK.sub("", line))
            continue
        if inside or re.match(r"^import\s", line):
            inside = not _IMPORT_END.search(line.strip())
            continue
        out.append(line)
    return "\n".join(out)


def _document(repo: _Repo, source: dict, ref: str, path: str, rel: str, version: str,
              data: dict, url: str) -> str:
    """`data` — {шлях файла даних від docs/: blob} знімка: з нього розгортаються APISection і
    схеми."""
    ctx = repo.ctx
    raw = repo.raw(ref, path)
    text = ctx.text(raw)
    _markup.refuse_html(text, raw)
    meta, rest = _markup.front_matter(text)
    meta = meta or {}
    sdk = version.split(", ")[0]
    _pkgs, imports = _deps(rest)

    def load(where: str):
        if where not in data:
            return None
        url_ = repo.raw(ref, where)
        if not ctx.allowed(url_):
            return None
        body = ctx.text(url_)
        if where.endswith(".json"):
            try:
                return json.loads(body)
            except ValueError:
                return None
        return _js_default(body)

    def api(pkg: str) -> str:
        found = load(_DATA.format(sdk=sdk) + pkg + ".json") if pkg else None
        return _typedocjson.render(found) if found else ""

    schemas = {name: load(where) for name, where in imports.items()}
    rest = _expand(_imports_out(rest), meta, api, schemas)
    rest = _atx(_markup.mdx_statements_out(_docusaurus(rest)))
    title = str(meta.get("title") or meta.get("sidebar_title") or "")
    if not title:
        title, rest = _split_title(rest)
    if not title:
        title = posixpath.basename(re.sub(r"\.mdx?$", "", rel))
    lead = str(meta.get("description") or "")
    if lead:
        rest = f"{lead}\n\n{rest}"
    label = source.get("label", "")
    title = unescape(title)
    if label:
        title = f"{label}: {title}"
    body = _markup.markdown_body(rest)
    if body.strip():
        _markup.require(title, body, raw, min_chars=1)
    return _markup.document(title, url, ctx.stamp, body, version)


def _docusaurus(text: str) -> str:
    # Виноски `> **info** …` і `:::`-блоки сайт Expo теж має; спільний розбір Docusaurus
    # перетворює `:::` на підписи, решту лишає як є.
    from engine.readers.sitedocs import docusaurus
    return docusaurus(text, None, {})


def _site_path(rel: str) -> str:
    stem = re.sub(r"\.mdx?$", "", rel)
    stem = re.sub(r"(^|/)index$", "", stem)
    return stem


def _group(repo: _Repo, source: dict, units: list) -> dict:
    """units — [(версія, знімок, тека від docs/, {відносний шлях: blob}, дані)] від
    найновішої версії. Повертає {(шлях, blob, хеші даних): [знімок, тека, [версії], дані]}."""
    scan = [re.compile(r) for r in source.get("scan") or ()]
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    seen: dict = {}
    for version, ref, folder, files, data in units:
        for rel, sha in files.items():
            if not rel.endswith(_PAGE) or any(r.search(rel) for r in exclude):
                continue
            # Сторінка, що бере файли даних, — окремий документ на кожну версію, де дані є:
            # однаковий текст сторінки з різним API — різні тексти, а які саме файли вона
            # бере, видно лише з її тексту, і читати тисячі сторінок ще під час переліку
            # означало б тягнути кожну двічі. Однакові розділи різних версій усе одно
            # зливаються вже в корпусі.
            key_data: tuple = ()
            # Окремий документ на версію — лише там, де є дані API чи схеми нового сайту; старі
            # схеми `scripts/schemas/` стоять у шляху імпорту з номером SDK, тож сторінка з ними
            # і так своя в кожному SDK.
            if any(not k.startswith("scripts/") for k in data) and any(r.search(rel) for r in scan):
                key_data = (("version", version),)
            seen.setdefault((rel, sha, key_data), [ref, folder, [], data])[2].append(version)
    return seen


def _items(repo: _Repo, source: dict, seen: dict, url_of) -> list[Item]:
    items = []
    names: set = set()
    for (rel, sha, key_data), (ref, folder, versions, data) in seen.items():
        path = f"{folder}/{rel}" if folder else rel
        raw = repo.raw(ref, path)
        if not repo.ctx.allowed(raw):
            continue
        stem = re.sub(r"\.mdx?$", "", rel)
        tail = sha[:8]
        if key_data:
            import hashlib
            tail += "-" + hashlib.sha1(repr(key_data).encode()).hexdigest()[:6]
        name = f"{_markup.slug(stem)}-{tail}"
        if name in names:
            continue
        names.add(name)
        url = url_of(ref, path, rel, versions)

        def make(ref=ref, path=path, rel=rel, version=", ".join(versions), data=data, url=url):
            return _document(repo, source, ref, path, rel, version, data, url)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


def _head(repo: _Repo) -> str:
    last = repo.commits("docs")
    if not last:
        raise SystemExit(f"{repo.owner}/{repo.repo}@{repo.branch}: жодного коміту в docs/.")
    return last[0]["sha"]


def _data_of(snap: dict, sdk: str) -> dict:
    prefix = _DATA.format(sdk=sdk)
    return {p: s for p, s in snap.items() if p.startswith((prefix,) + _SCHEMAS)}


@register("expo-sdk-history")
def expo_sdk_history(source: dict, ctx) -> list[Item]:
    repo = _Repo(source, ctx)
    sdks = _sdks(source, ctx)
    head = _head(repo)
    where = _folders(repo, sdks, head)
    newest = max(where, key=_key) if where else ""
    units = []
    for sdk in sorted(where, key=_key, reverse=True):
        ref, folder = where[sdk]
        snap = repo.snapshot(ref)
        files = {p[len(folder) + 1:]: s for p, s in snap.items() if p.startswith(folder + "/")}
        units.append((sdk, ref, folder, files, _data_of(snap, sdk)))
    seen = _group(repo, source, units)
    site = source.get("site", "")

    def url_of(ref, path, rel, versions):
        top = versions[0]
        if ref == head and site:
            where_ = "latest" if top == newest else f"v{top}.0.0"
            return site.format(path=f"versions/{where_}/{_site_path(rel)}".rstrip("/"))
        return f"https://github.com/{repo.owner}/{repo.repo}/blob/{ref}/docs/{quote(path)}"

    items = _items(repo, source, seen, url_of)
    if not items:
        raise SystemExit(f"{source['id']}: жодної сторінки в жодній теці SDK.")
    return items


@register("expo-guides-history")
def expo_guides_history(source: dict, ctx) -> list[Item]:
    repo = _Repo(source, ctx)
    sdks = _sdks(source, ctx)
    times = _times(source, ctx)
    head = _head(repo)
    where = _folders(repo, sdks, head)
    newest = sdks[0] if sdks else ""
    units = []
    for sdk in sdks:
        # SDK, чиї посібники лежали в теці версії, окремого знімка не потребує.
        if sdk in where:
            ref, folder = where[sdk]
            if any(p.startswith(tuple(f"{folder}/{g}" for g in _OLD_GUIDES))
                   for p in repo.snapshot(ref)):
                continue
        if sdk == newest:
            ref = head
        else:
            moment = times.get(str(int(sdk) + 1))
            if not moment:
                continue
            last = repo.commits("docs", until=moment)
            if not last:
                continue
            ref = last[0]["sha"]
        snap = repo.snapshot(ref)
        files = {p[len("pages/"):]: s for p, s in snap.items()
                 if p.startswith("pages/") and not p.startswith("pages/versions/")}
        units.append((sdk, ref, "pages", files,
                      {p: s for p, s in snap.items() if p.startswith(_SCHEMAS)}))
    seen = _group(repo, source, units)
    site = source.get("site", "")

    def url_of(ref, path, rel, versions):
        if ref == head and site:
            return site.format(path=_site_path(rel)).rstrip("/") + "/"
        return f"https://github.com/{repo.owner}/{repo.repo}/blob/{ref}/docs/{quote(path)}"

    items = _items(repo, source, seen, url_of)
    if not items:
        raise SystemExit(f"{source['id']}: жодної сторінки посібників у жодному знімку.")
    return items
