"""Читач документації Snooty (MongoDB) з репозиторію: сторінка кожної версії.

`snooty-history` — сторінки `.txt` проєкту Snooty на кожній оголошеній гілці чи в кожній
                   теці версії. Поля:
                   `url`        — префікс дерев (…/repos/ВЛАСНИК/РЕПО/git/trees/);
                   `refs`       — об'єкт «гілка, тег чи коміт → версія», від найновішої;
                   `folders`    — теки проєктів (де лежать `snooty.toml` і `source/`) від
                                  кореня репозиторію; "" — сам корінь; або об'єкт «тека →
                                  версія», коли версії лежать теками на одній гілці (тоді в
                                  `refs` одна гілка, і її мітка не важить);
                   `source_dir` — тека сторінок усередині проєкту (типово `source`);
                   `label`      — префікс назви документа («mongosh», «Database Tools»),
                                  коли в корпусі кілька продуктів;
                   `shared_url` — префікс дерев репозиторію спільних вставок
                                  `.. sharedinclude::` (`sharedinclude_root` у snooty.toml:
                                  10gen/docs-shared), `shared_ref` — його гілка (типово main);
                   `exclude`    — вирази шляхів сторінок, що не беруться (типово — теки
                                  вставок, картинок і прикладів коду);
                   `name_prefix` — рядок перед іменем документа: у примірнику, де сторінки
                                  Snooty живуть поруч з іншими наборами, «limitations» чи
                                  «quick-start» інакше ділили б ключ розділу зі сторінками
                                  інших продуктів. Без поля ім'я те саме, що й було.

Навіщо. Посібник MongoDB лежить у `mongodb/docs` двояко: версії 2.2–8.0 — гілками `vX.Y` зі
`source/` у корені, 7.0–9.0 — теками `content/manual/<версія>/` на `main`; mongosh і Database
Tools — теками без версій. Сторінка — `.txt`, що вставляє `includes/*.rst`, YAML-кроки й
витяги, приклади коду з `code-examples/` і `driver-examples/`, константи зі `snooty.toml`
(у старих гілках — з `conf.py`). Розбір самої розмітки — у `_snooty`; тут — файли, версії,
YAML-покажчики та склад документа.

Одиниця — сторінка у версії; та сама сторінка з тим самим вмістом у двох версіях — два документи,
кожен зі своєю версією (вставки й константи залежать від версії), а однакові фрагменти
зливаються вже в корпусі (`revision_suffix`).
"""

import hashlib
import json
import os
import posixpath
import re
import sys
from html import unescape
from urllib.parse import quote

from engine.readers import Item, _markup, register
from engine.readers import _snooty
from engine.readers.ghhistory import _split_title
from engine.readers.k8sdocs import _MEMO_MAX, _Site, _blobs

_DEFAULT_EXCLUDE = (r"(^|/)includes/", r"(^|/)images/", r"(^|/)code-examples/",
                    r"(^|/)driver-examples/", r"(^|/)\.static/", r"(^|/)\.templates/")
_GENERATED = re.compile(r"^includes/(steps|extracts|release|toc)/([^/]+)\.rst$")
_TOC_PREFIX = re.compile(r"^(dfn-list-spec|table-spec|dfn-list|table|spec)-")
_DEBUG = os.environ.get("DF_SNOOTY_DEBUG")


class _Unit:
    """Одна версія: гілка, тека проєкту, мітка версії; файли проєкту — шлях від кореня
    репозиторію → (хеш, розмір)."""

    def __init__(self, ref: str, label: str, project: str, source_dir: str):
        self.ref, self.label, self.project = ref, label, project
        self.src = f"{project}/{source_dir}" if project else source_dir
        self.files: dict = {}
        self.links: dict = {}         # символьне посилання (шлях від кореня) → хеш blob із ціллю
        self.root: dict = {}          # файли кореня проєкту (snooty.toml, conf.py)
        self.shared_site = None       # _Site репозиторію спільних вставок
        self.shared_ref = "main"
        self._conf = None
        self._yaml: dict = {}


class _Project:
    """Константи, підстановки й назви варіантів однієї версії."""

    def __init__(self, site: _Site, unit: _Unit):
        self.constants: dict = {}
        self.subs: dict = {}
        self.composables: dict = {}
        self.labels: dict | None = None
        self.docs: dict = {}          # шлях сторінки від кореня сторінок → її назва
        toml = unit.root.get("snooty.toml")
        if toml:
            text = site.text(unit.ref, f"{unit.project}/snooty.toml" if unit.project
                             else "snooty.toml", toml[0]) or ""
            self.constants = _snooty.toml_section(text, "constants")
            # Гілка 4.2 пише `release = "{+release+}"` — заглушка, що чекає на значення з
            # conf.py; така константа вважається невизначеною, щоб далі взялося справжнє.
            self.constants = {k: v for k, v in self.constants.items() if v != f"{{+{k}+}}"}
            self.subs = _snooty.toml_section(text, "substitutions")
            self.composables = _snooty.toml_composables(text)
        conf = unit.root.get("conf.py")
        if conf:
            text = site.text(unit.ref, f"{unit.project}/conf.py" if unit.project
                             else "conf.py", conf[0]) or ""
            consts, subs = _snooty.conf_py(text, _bare_version(unit.label), unit.ref)
            for k, v in consts.items():
                self.constants.setdefault(k, v)
            for k, v in subs.items():
                self.subs.setdefault(k, v)
        ver = _bare_version(unit.label)
        for key in ("version", "release", "pgp-version", "package-branch"):
            self.constants.setdefault(key, ver)
        self.constants.setdefault("package-name-org", "mongodb-org")
        self.constants.setdefault("package-name-enterprise", "mongodb-enterprise")
        self.constants.setdefault("branch", unit.ref)
        # Вбудовані підстановки Sphinx: |version|, |release|, |today|.
        self.subs.setdefault("version", _bare_version(unit.label))
        self.subs.setdefault("release", _bare_version(unit.label))
        self.subs.setdefault("today", getattr(getattr(site, "ctx", None), "stamp", "") or "")
        # `|arrow|` (U+27A4) сторінки визначають кожна собі, а вставки кроків уживають і там,
        # де визначення нема, — типове значення одне на всі гілки.
        self.subs.setdefault("arrow", "\u27a4")
        self.subs.setdefault("query-api", "MongoDB Query API")
        # У 7.1–7.3 `[substitutions]` стоїть вище за `[constants]` і каже `version = "{+version+}"`:
        # константи всередині підстановок розкриваються тут, бо `_substitute` їх уже не чіпає.
        self.subs = {k: _snooty._constants(v, self.constants) for k, v in self.subs.items()}


def _bare_version(label: str) -> str:
    m = re.search(r"\d+(?:\.\d+)*", label)
    return m.group(0) if m else label


_LABEL = re.compile(r"^\s*\.\.\s+_(`[^`]+`|[^:]+):\s*$")


def _first_title(lines: list[str]) -> str:
    """Перший підкреслений заголовок сторінки — її назва."""
    for i, ln in enumerate(lines[:80]):
        cur = ln.strip()
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if cur and not cur.startswith(("..", ":")) and _snooty._TITLE_UNDER.match(nxt) \
                and not _snooty._TITLE_UNDER.match(cur) and len(nxt) >= min(len(cur), 3):
            return cur
    return ""
_OBJECT = re.compile(r"^\s*\.\.\s+([\w-]+)::\s+(.+?)\s*$")


class _PageCtx(_snooty.Ctx):
    def __init__(self, site: _Site, unit: _Unit, project: _Project):
        self.site, self.unit = site, unit
        self.constants = project.constants
        self.composables = project.composables
        self._subs = project.subs
        self._project = project

    def substitutions(self) -> dict:
        return self._subs

    def label_title(self, label: str) -> str:
        """Назва розділу за міткою `.. _label:` — по всіх сторінках і вставках версії (раз
        на версію). Без неї `:ref:`write-op-insert-behavior`` лишалося б міткою."""
        if self._project.labels is None:
            self._project.labels = self._scan_labels()
        return self._project.labels.get(label.strip().lower(), "")

    def doc_title(self, path: str) -> str:
        """Назва сторінки за її шляхом від кореня сторінок (`/reference/method/find` → «find»)."""
        if self._project.labels is None:
            self._project.labels = self._scan_labels()
        return self._project.docs.get(path.strip().strip("/").removesuffix(".txt"), "")

    def _scan_labels(self) -> dict:
        labels: dict = {}
        docs: dict = self._project.docs
        src = self.unit.src + "/"
        for path, (sha, size) in self.unit.files.items():
            if not path.endswith((".txt", ".rst")) or size == 0:
                continue
            text = self.site.text(self.unit.ref, path, sha)
            if not text:
                continue
            lines = text.split("\n")
            if path.endswith(".txt") and path.startswith(src):
                first = _first_title(lines)
                if first:
                    docs[path[len(src):-4]] = _snooty._constants(first, self.constants)
            pending: list = []
            for i, ln in enumerate(lines):
                m = _LABEL.match(ln)
                if m:
                    pending.append(m.group(1).strip("`").strip().lower())
                    continue
                if not pending or not ln.strip() or ln.lstrip().startswith(".. ") and not _OBJECT.match(ln):
                    if ln.strip() and not ln.lstrip().startswith(".."):
                        pending = []
                    continue
                title = ""
                nxt = (lines[i + 1] if i + 1 < len(lines) else "").strip()
                cur = ln.strip()
                if _snooty._TITLE_UNDER.match(nxt) and not _snooty._TITLE_UNDER.match(cur):
                    title = cur
                elif _snooty._TITLE_UNDER.match(cur) and i + 2 < len(lines) \
                        and _snooty._TITLE_UNDER.match(lines[i + 2].strip()):
                    title = lines[i + 1].strip()
                else:
                    o = _OBJECT.match(ln)
                    if o and o.group(1) in _snooty.OBJECTS:
                        title = o.group(2)
                if title:
                    title = _snooty._constants(title, self.constants)
                    for lab in pending:
                        labels.setdefault(lab, title)
                pending = []
        return labels

    def _resolve(self, target: str, page_dir: str) -> str:
        target = target.strip()
        if target.startswith("/"):
            rel = target.lstrip("/")
        else:
            rel = posixpath.normpath(posixpath.join(page_dir, target)) if page_dir else target
        return posixpath.normpath(rel)

    def _read(self, rel: str, depth: int = 0) -> str | None:
        full = f"{self.unit.src}/{rel}"
        hit = self.unit.files.get(full)
        if hit and full not in self.unit.links:
            return self.site.text(self.unit.ref, full, hit[0])
        if depth > 4:
            return None
        # Символьне посилання на шляху (`code-examples/tested` → `../../code-examples/tested`):
        # ланка замінюється ціллю, і пошук іде знову — у теці сторінок або деінде в репозиторії.
        parts = rel.split("/")
        for i in range(len(parts), 0, -1):
            link = f"{self.unit.src}/{'/'.join(parts[:i])}"
            if link in self.unit.links:
                target = (self.site.text(self.unit.ref, link, self.unit.links[link]) or "").strip()
                if not target:
                    return None
                new = posixpath.normpath(posixpath.join(posixpath.dirname(link), target))
                if i < len(parts):
                    new = f"{new}/{'/'.join(parts[i:])}"
                return self._repo_read(new, depth + 1)
        return None

    def _repo_read(self, path: str, depth: int) -> str | None:
        """Файл за шляхом від кореня репозиторію: у теці сторінок — звичайним шляхом, поза нею —
        через дерево тієї теки (раз на гілку)."""
        if path.startswith(self.unit.src + "/"):
            return self._read(path[len(self.unit.src) + 1:], depth)
        top = "/".join(path.split("/")[:2])
        blobs = _tree_blobs(self.site, self.unit.ref, top)
        hit = blobs.get(path)
        return self.site.text(self.unit.ref, path, hit[0]) if hit else None

    def include(self, target: str, page_dir: str) -> str | None:
        rel = self._resolve(target, page_dir)
        cands = [rel, rel + ".rst", rel + ".txt"]
        if rel.endswith(".txt"):
            cands.append(rel[:-4] + ".rst")     # сторінка просить .txt, а файл лежить як .rst
        elif rel.endswith(".rst"):
            cands.append(rel[:-4] + ".txt")
        for cand in cands:
            text = self._read(cand)
            if text is not None:
                return text
        g = _GENERATED.match(rel)
        if g:
            return self._generated(g.group(1), g.group(2))
        return None

    def literal(self, target: str, page_dir: str) -> str | None:
        return self._read(self._resolve(target, page_dir))

    def shared(self, target: str) -> str | None:
        if not self.unit.shared_site:
            return None
        rel = target.strip().lstrip("/")
        hit = _tree_blobs(self.unit.shared_site, self.unit.shared_ref, "").get(rel)
        if not hit:
            return None
        return self.unit.shared_site.text(self.unit.shared_ref, rel, hit[0])

    # ── YAML giza ────────────────────────────────────────────────────────

    def _yaml_file(self, name: str) -> list:
        """Документи YAML файла `includes/<name>` (кеш на версію)."""
        cache = self.unit._yaml
        if name in cache:
            return cache[name]
        text = self._read(f"includes/{name}")
        docs: list = []
        if text:
            try:
                import yaml
                docs = [d for d in yaml.safe_load_all(text) if isinstance(d, dict)]
            except Exception as exc:   # YAML з помилкою — як відсутній, не падіння прогону
                if _DEBUG:
                    print(f"snooty: {self.unit.ref} includes/{name}: {exc}", file=sys.stderr)
                docs = []
        cache[name] = docs
        return docs

    def _index(self, prefix: str) -> dict:
        """ref → запис по всіх файлах `includes/<prefix>-*.yaml` версії."""
        key = f"#{prefix}"
        cache = self.unit._yaml
        if key in cache:
            return cache[key]
        index: dict = {}
        head = f"{self.unit.src}/includes/{prefix}-"
        for path in self.unit.files:
            if path.startswith(head) and path.endswith((".yaml", ".yml")):
                name = path[len(self.unit.src) + len("/includes/"):]
                for d in self._yaml_file(name):
                    ref = str(d.get("ref", "")).strip()
                    if ref:
                        index.setdefault(ref, (name, d))
        cache[key] = index
        return index

    def _loader(self, prefix: str):
        def load(file: str, ref: str) -> dict | None:
            file = file.strip().lstrip("/")
            if file.startswith("includes/"):
                file = file[len("includes/"):]
            if file:
                for d in self._yaml_file(file):
                    if str(d.get("ref", "")).strip() == ref:
                        return d
            hit = self._index(prefix).get(ref)
            return hit[1] if hit else None
        return load

    def _generated(self, kind: str, name: str) -> str | None:
        if kind == "toc":
            spec = "spec" in (_TOC_PREFIX.match(name).group(1) if _TOC_PREFIX.match(name) else "")
            base = _TOC_PREFIX.sub("", name)
            names = ([f"toc-spec-{base}.yaml"] if spec else []) + [
                f"toc-{base}.yaml", f"ref-toc-{base}.yaml", f"{base}.yaml"]
            for fname in names:
                docs = self._yaml_file(fname)
                if docs:
                    return _snooty.toc_rst(docs, self.doc_title)
            return None
        if kind == "steps":
            docs = self._yaml_file(f"steps-{name}.yaml")
            return _snooty.steps_rst(docs, self._loader("steps")) if docs else None
        index = self._index(kind)
        hit = index.get(name)
        if not hit:
            return None
        if kind == "extracts":
            return _snooty.extract_rst(hit[1], self._loader("extracts"))
        return _snooty.release_rst(hit[1], self._loader("release"))


class _ShaSite(_Site):
    """Сирі файли — раз на хеш blob, а не раз на адресу. Той самий файл лежить у двох десятках
    гілок посібника під різними адресами (`.../v6.0/source/x.rst`, `.../v5.3/source/x.rst`): без
    цього кожна редакція тягла б його знову. Перша адреса, за якою файл із цим хешем узято,
    запам'ятовується в `raw/snooty-blobs.json` поруч зі сховищем сирого — так і `build` без мережі
    знаходить файл у сховищі, хоч би з якої гілки його просили."""

    def __init__(self, source: dict, ctx):
        super().__init__(source, ctx)
        self.by_sha: dict = {}
        self.path = None
        store = getattr(ctx, "store", None)
        if store is not None and getattr(store, "root", None) is not None:
            self.path = store.root / "snooty-blobs.json"
            try:
                self.by_sha = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                self.by_sha = {}
        self._dirty = 0

    def text(self, ref: str, path: str, sha: str = "") -> str | None:
        if not sha:
            return super().text(ref, path, sha)
        if sha in self.memo:
            return self.memo[sha]
        url = self.by_sha.get(sha) or self.raw(ref, path)
        if not self.ctx.allowed(url):
            return None
        text = self.ctx.text(url).replace("\r\n", "\n")
        if sha not in self.by_sha:
            self.by_sha[sha] = url
            self._dirty += 1
            if self._dirty >= 200:
                self.flush()
        if len(self.memo) >= _MEMO_MAX:
            self.memo.clear()
        self.memo[sha] = text
        return text

    def page(self, ref: str, path: str, sha: str) -> str:
        text = self.text(ref, path, sha)
        return text if text is not None else super().page(ref, path, sha)

    def flush(self) -> None:
        if self.path is None or not self._dirty:
            return
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.by_sha, indent=0), encoding="utf-8")
            self._dirty = 0
        except OSError:
            pass


_TREES: dict = {}


def _tree_blobs(site: _Site, ref: str, folder: str) -> dict:
    """Файли теки репозиторію (шлях від кореня → (хеш, розмір)) — раз на гілку й теку."""
    key = (site.owner, site.repo, ref, folder)
    if key not in _TREES:
        if not folder:
            _TREES[key] = _blobs(site.entries(ref, recursive=True))
        else:
            root = site.entries(ref)
            sha = site.subtree(root, folder)
            _TREES[key] = _blobs(site.entries(sha, recursive=True), folder + "/") if sha else {}
    return _TREES[key]


def _links(entries: list, prefix: str = "") -> dict:
    return {prefix + e["path"]: e["sha"] for e in entries
            if e.get("type") == "blob" and e.get("mode") == "120000"}


@register("snooty-history")
def snooty_history(source: dict, ctx) -> list[Item]:
    refs = source.get("refs")
    if not isinstance(refs, dict) or not refs:
        raise SystemExit(f"{source['id']}: читач snooty-history потребує поля refs — об'єкта "
                         f"«гілка, тег чи коміт → версія».")
    folders = source.get("folders")
    if folders is None:
        folders = [""]
    by_folder = isinstance(folders, dict)
    if by_folder and len(refs) != 1:
        raise SystemExit(f"{source['id']}: теки з версіями (folders-об'єкт) — лише на одній гілці.")
    source_dir = (source.get("source_dir") or "source").strip("/")
    label = source.get("label", "")
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    exclude = [re.compile(r) for r in source.get("exclude") or _DEFAULT_EXCLUDE]
    site = _ShaSite(source, ctx)
    shared_site = None
    if source.get("shared_url"):
        # Той самий blob може лежати і в репозиторії спільних вставок, і в посібнику: мапа
        # «хеш → адреса» одна на обидва, пише її лише головне джерело.
        shared_site = _ShaSite({"url": source["shared_url"]}, ctx)
        shared_site.by_sha, shared_site.path = site.by_sha, None
    shared_ref = source.get("shared_ref") or "main"

    units: list[_Unit] = []
    for ref, ref_label in refs.items():
        root = site.entries(ref)
        pairs = folders.items() if by_folder else [(f, str(ref_label)) for f in folders]
        for folder, folder_label in pairs:
            unit = _Unit(ref, str(folder_label), folder.strip("/"), source_dir)
            proj_entries = root if not unit.project else (
                site.entries(site.subtree(root, unit.project)) if site.subtree(root, unit.project)
                else [])
            unit.root = _blobs(proj_entries)
            sha = site.subtree(root, unit.src)
            if not sha:
                print(f"snooty: {source['id']}: {ref} {unit.src}: теки сторінок немає — "
                      f"версію {unit.label} пропущено.", file=sys.stderr)
                continue
            entries = site.entries(sha, recursive=True)
            unit.files = _blobs(entries, unit.src + "/")
            unit.links = _links(entries, unit.src + "/")
            unit.shared_site, unit.shared_ref = shared_site, shared_ref
            units.append(unit)

    items: list[Item] = []
    names: set = set()
    projects: dict = {}
    for unit in units:
        for path, (sha, size) in sorted(unit.files.items()):
            rel = path[len(unit.src) + 1:]
            if not rel.endswith(".txt") or size == 0 or any(r.search(rel) for r in exclude):
                continue
            raw = site.raw(unit.ref, path)
            if not ctx.allowed(raw):
                continue
            stem = rel[:-4]
            stem = re.sub(r"(^|/)_?index$", "", stem) or "index"
            key = f"{path}\0{sha}\0{unit.ref}\0{unit.project}"
            name = f"{lead}{_markup.slug(stem)}-{hashlib.sha1(key.encode()).hexdigest()[:8]}"
            if name in names:
                continue
            names.add(name)
            blob = (f"https://github.com/{site.owner}/{site.repo}/blob/"
                    f"{quote(unit.ref, safe='@')}/{quote(path)}")

            def make(unit=unit, path=path, sha=sha, blob=blob, raw=raw, rel=rel, stem=stem):
                if unit not in projects:
                    site.flush()
                    projects[unit] = _Project(site, unit)
                pctx = _PageCtx(site, unit, projects[unit])
                text = site.page(unit.ref, path, sha)
                body, misses = _snooty.render(text, pctx, posixpath.dirname(rel))
                if misses and _DEBUG:
                    print(f"snooty: {unit.ref} {rel}: не знайдено {sorted(set(misses))[:6]}",
                          file=sys.stderr)
                title, rest = _split_title(body)
                if not title:
                    title = posixpath.basename(stem).replace("-", " ")
                title = unescape(" ".join(title.split()))
                if label:
                    title = f"{label}: {title}"
                rest = _markup.markdown_body(rest)
                _markup.require(title, rest, raw, min_chars=1)
                return _markup.document(title, blob, ctx.stamp, rest, unit.label)

            items.append(Item(id=f"{source['id']}/{name}",
                              file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: на жодній із {len(refs)} гілок не знайдено "
                         f"дозволених сторінок.")
    return items
