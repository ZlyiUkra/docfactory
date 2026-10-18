"""Засів сховища сирого примірника з голих клонів — для джерел історії репозиторіїв GitHub.

    instances/<примірник>/.venv/bin/python tools/seed_git_store.py --instance opentelemetry \\
        --clone open-telemetry/opentelemetry-js=/шлях/до/opentelemetry-js.git [--clone …] [--dry-run]

Навіщо. Читачі `ghdocs-history`, `ghcode-history`, `ghcode-history-ts`, `ghcode-history-proto`,
`ghdocs-history-xhp` і `ghcode-history-lo` беруть
кожну неповторну редакцію файла з raw.githubusercontent.com по одному запиту. Код і тести
opentelemetry-js на 143 комітах випусків — десять тисяч файлів, js-contrib — ще п'ять, і мережею це
години; голий клон (`git clone --bare`) має всі blob-и локально, а GitHub віддає за адресою
raw.githubusercontent.com той самий blob байт у байт. Інструмент кладе кожен blob у сховище під тією
адресою, за якою його попросить читач, і далі `./df <примірник> build` збирає корпус без мережі.

Яка адреса. Читач називає документ парою «шлях, вміст» і тягне його з найновішого тегу (першого в
оголошеному порядку `tags`), де файл лежав саме таким: `…/<власник>/<репо>/<тег>/<шлях>`. Інструмент
іде тегами в тому самому порядку й кладе кожну пару під адресою її першого тегу. Відбір файлів — той
самий, що в читача: `folders`/`recursive`/`files`/`extensions`/`exclude` для `ghdocs-history` (і файли
вставок `otel_hugo`), `include`/`exclude` для читачів коду, `data/registry` коміту `ref` для
`otel-registry`. Інших полів розгортання (vitepress, vocs, astro_mdx…) інструмент не знає: такі джерела
лишаються мережі.

Дерева тегів (`git/trees/<тег>?recursive=1`) інструмент не кладе: їх бере `./df <примірник> list`
через API (кількасот запитів), і він же має бути першим кроком. Виняток — `ghdocs-history-xhp`: він
читає сторінки вже під час переліку, і `list` тягнув би кожну мережею. Для нього `--trees` кладе й
дерева `тег:тека?recursive=1` з повного клону (розміри blob-ів беруться з нього ж). Частковий клон (`--filter=blob:none`)
підходить теж: blob-и, яких бракує, інструмент докачує пачками (`git fetch --stdin origin`), і лише ті,
що потрапили до відбору.

Читач `docfx` (документація learn.microsoft.com з репозиторію) розгортає вставки й приклади коду
з будь-якого місця набору, тож для нього кладуться всі текстові blob-и головного репозиторію на коміті
з адреси дерева (зображення й інші двійкові файли — ні), саме дерево `git/trees/<коміт>?recursive=1`
(читач гортає сторінки вже під час переліку, і `list` тягнув би кожну мережею) і з залежних
репозиторіїв (поле `repos`: тека → «власник/репо/коміт») — лише файли, на які сторінки посилаються
шляхом «~/../<тека>/…». Клон залежного репозиторію може бути неглибоким частковим
(`--depth=1 --filter=blob:none`): потрібні blob-и докачуються пачкою.

Білий список не слабшає: беруться лише джерела з `sources.json`, лише оголошені в них теги й шляхи, і
лише з клонів, названих у `--clone власник/репо=шлях`. Нічого не видаляє й не перезаписує: запис, який
у сховищі вже є, лишається.
"""

import argparse
import json
import os
import pathlib
import posixpath
import re
import subprocess
import sys
import time
from urllib.parse import quote, urlsplit

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from engine import rawstore  # noqa: E402
from engine.readers._otelhugo import WANTED as OTEL_WANTED  # noqa: E402
from engine.readers.ghhistory import _LOCALE  # noqa: E402

RAW = "https://raw.githubusercontent.com"
TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/(.*)$")
READERS = {"ghdocs-history", "ghcode-history", "ghcode-history-ts", "ghcode-history-proto", "otel-registry",
           "ghdocs-history-xhp", "ghcode-history-lo", "docfx"}
# Двійкові файли, яких читач docfx ніколи не просить: зображення, архіви, бази для прикладів.
BINARY = (".png", ".gif", ".jpg", ".jpeg", ".svg", ".ico", ".bmp", ".tif", ".tiff", ".webp", ".zip", ".gz",
          ".7z", ".pdf", ".mp4", ".wmv", ".mov", ".pptx", ".docx", ".xlsx", ".vsdx", ".exe", ".dll", ".msi",
          ".nupkg", ".bak", ".bacpac", ".dacpac", ".mdf", ".ldf", ".jar", ".whl", ".ttf", ".woff", ".woff2")
# Посилання сторінки DocFX на файл залежного репозиторію: «~/../<тека>/<шлях>».
DEPENDENT = re.compile(r"~/\.\./([\w.-]+)/([^\s)\"'?#\]]+)")
PLAIN = {"vitepress", "vocs", "astro_mdx", "prisma_mdx", "biome_mdx", "mdbook", "base_ui", "jsx_sources",
         "hugo", "sphinx"}


def _selector(src: dict):
    """Вираз відбору шляхів джерела — той самий, що в читача."""
    exclude = [re.compile(r) for r in src.get("exclude") or ()]
    if src["reader"] == "ghdocs-history":
        folders = [f.strip("/") for f in src.get("folders") or ["docs"]]
        files = {f.strip("/") for f in src.get("files") or ()}
        recursive = src.get("recursive") is True
        exts = tuple(src.get("extensions") or (".md",))
        wanted = OTEL_WANTED if src.get("otel_hugo") is True else []

        def ok(path):
            if any(r.match(path) for r in wanted):
                return True
            folder, _, leaf = path.rpartition("/")
            inside = path in files or (folder in folders if not recursive else
                                       any(folder == f or folder.startswith(f + "/") for f in folders))
            return (inside and leaf.endswith(exts) and not _LOCALE.search(leaf)
                    and not any(r.search(path) for r in exclude))
        return ok
    if src["reader"] == "otel-registry":
        return lambda path: path.startswith("data/registry/") and path.endswith((".yml", ".yaml"))
    if src["reader"] == "ghdocs-history-xhp":
        roots = tuple(r.strip("/") + "/" for r in src.get("roots") or ["source/text"])
        return lambda path: path.startswith(roots) and path.endswith(".xhp")
    if src["reader"] == "docfx":
        return lambda path: not path.lower().endswith(BINARY)
    include = [re.compile(r) for r in src.get("include") or ()]
    return lambda path: any(r.search(path) for r in include) and not any(r.search(path) for r in exclude)


def _ls(clone: pathlib.Path, ref: str):
    out = subprocess.run(["git", "--git-dir", str(clone), "ls-tree", "-r", ref],
                         capture_output=True, text=True, errors="replace")
    if out.returncode:
        raise SystemExit(f"{clone}: git ls-tree {ref}: {out.stderr.strip()}")
    for ln in out.stdout.splitlines():
        meta, path = ln.split("\t", 1)
        _mode, typ, sha = meta.split()
        if typ == "blob":
            yield path, sha


def _missing(clone: pathlib.Path, shas: list[str]) -> list[str]:
    env = dict(os.environ, GIT_NO_LAZY_FETCH="1")
    out = subprocess.run(["git", "--git-dir", str(clone), "cat-file", "--batch-check"], input="\n".join(shas),
                         capture_output=True, text=True, env=env).stdout
    return [ln.split()[0] for ln in out.splitlines() if ln.endswith(" missing")]


def _fetch(clone: pathlib.Path, shas: list[str]) -> None:
    for i in range(0, len(shas), 5000):
        part = shas[i:i + 5000]
        out = subprocess.run(["git", "--git-dir", str(clone), "-c", "fetch.negotiationAlgorithm=noop", "fetch",
                              "--no-tags", "--no-write-fetch-head", "--filter=blob:none", "--stdin", "origin"],
                             input="\n".join(part), capture_output=True, text=True)
        if out.returncode:
            raise SystemExit(f"{clone}: git fetch пачки blob-ів: {out.stderr.strip()[-400:]}")
        print(f"  докачано blob-ів: {min(i + 5000, len(shas))} з {len(shas)}", flush=True)


def _put_trees(store, sources: list[dict], clones: dict) -> None:
    """Дерева `тег:тека?recursive=1` у вигляді відповіді API — перша наявна тека з `roots` на кожному тезі."""
    for src in sources:
        if src.get("reader") != "ghdocs-history-xhp":
            continue
        m = TREES.match(urlsplit(src["url"]).path)
        clone = clones.get(f"{m.group(1)}/{m.group(2)}") if m else None
        if clone is None:
            continue
        git = ["git", "--git-dir", str(clone)]
        n = 0
        for tag in src.get("tags") or {}:
            for root in src.get("roots") or ["source/text"]:
                sha = subprocess.run(git + ["rev-parse", "--verify", "-q", f"{tag}:{root}"],
                                     capture_output=True, text=True).stdout.strip()
                if not sha:
                    continue
                out = subprocess.run(git + ["ls-tree", "-r", "-t", "-l", f"{tag}:{root}"],
                                     capture_output=True, text=True, check=True).stdout
                tree = []
                for ln in out.splitlines():
                    meta, path = ln.split("\t", 1)
                    mode, typ, blob, size = meta.split()
                    tree.append({"path": path, "mode": mode, "type": typ, "sha": blob,
                                 **({"size": int(size)} if typ == "blob" else {})})
                url = f"{src['url']}{quote(tag, safe='@')}:{quote(root)}?recursive=1"
                if store.meta(url) is not None:
                    break  # запис, що вже є, лишається як був
                store.put(url, "", json.dumps({"sha": sha, "tree": tree, "truncated": False}).encode(), {})
                n += 1
                break
        print(f"  {src['id']}: дерев тегів {n}", flush=True)


def _docfx_tree(store, src: dict, clone: pathlib.Path, ref: str) -> None:
    """Дерево коміту у вигляді відповіді API — те, що читач docfx бере першим зверненням."""
    if store.meta(src["url"]) is not None:
        return  # запис, що вже є, лишається як був
    out = subprocess.run(["git", "--git-dir", str(clone), "ls-tree", "-r", "-t", ref],
                         capture_output=True, text=True, check=True).stdout
    tree = []
    for ln in out.splitlines():
        meta, path = ln.split("\t", 1)
        mode, typ, blob = meta.split()
        tree.append({"path": path, "mode": mode, "type": typ, "sha": blob})
    sha = subprocess.run(["git", "--git-dir", str(clone), "rev-parse", f"{ref}^{{tree}}"],
                         capture_output=True, text=True).stdout.strip()
    store.put(src["url"], "", json.dumps({"sha": sha, "tree": tree, "truncated": False}).encode(), {})
    print(f"  {src['id']}: дерево {ref[:12]} ({len(tree)} записів)", flush=True)


def _docfx_dependent(src: dict, clone: pathlib.Path, ref: str, clones: dict) -> dict:
    """{адреса: sha} файлів залежних репозиторіїв, на які посилаються сторінки й вставки
    головного (текстові файли коміту `ref`)."""
    key = (str(clone), ref, json.dumps(src.get("repos") or {}, sort_keys=True))
    if key in _DEPENDENT_SEEN:
        return _DEPENDENT_SEEN[key]
    pages = [sha for path, sha in _ls(clone, ref) if path.endswith((".md", ".yml"))]
    lost = _missing(clone, sorted(set(pages)))
    if lost:
        _fetch(clone, lost)
    wanted: set = set()
    proc = subprocess.Popen(["git", "--git-dir", str(clone), "cat-file", "--batch"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, env=dict(os.environ, GIT_NO_LAZY_FETCH="1"))
    for sha in pages:
        proc.stdin.write((sha + "\n").encode())
        proc.stdin.flush()
        head = proc.stdout.readline().decode().split()
        if len(head) < 3 or head[1] == "missing":
            continue
        text = proc.stdout.read(int(head[2])).decode("utf-8", errors="replace")
        proc.stdout.read(1)
        wanted.update(DEPENDENT.findall(text))
    proc.stdin.close()
    proc.wait()
    urls: dict = {}
    by_head = {h: r for h, r in (src.get("repos") or {}).items()}
    listed: dict = {}
    for head, rest in sorted(wanted):
        spec = by_head.get(head)
        if not spec:
            continue
        owner, repo, dep_ref = spec.split("/", 2)
        dep = clones.get(f"{owner}/{repo}")
        if dep is None:
            continue
        if spec not in listed:
            listed[spec] = dict(_ls(dep, dep_ref))
        path = posixpath.normpath(rest)
        if path in listed[spec]:
            urls[f"{RAW}/{spec}/{quote(path)}"] = listed[spec][path]
    _DEPENDENT_SEEN[key] = urls
    return urls


_DEPENDENT_SEEN: dict = {}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--instance", required=True, help="назва примірника (тека в instances/)")
    ap.add_argument("--clone", action="append", default=[], metavar="власник/репо=шлях",
                    help="голий клон репозиторію; повторюваний")
    ap.add_argument("--dry-run", action="store_true", help="лише порахувати, нічого не писати")
    ap.add_argument("--trees", action="store_true",
                    help="ще й дерева тегів для джерел ghdocs-history-xhp (потрібен повний клон)")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    inst = root / "instances" / args.instance
    if not (inst / "sources.json").exists():
        raise SystemExit(f"{inst}: немає sources.json")
    data = json.loads((inst / "sources.json").read_text(encoding="utf-8"))
    sources = data["sources"] if isinstance(data, dict) else data
    clones = {}
    for item in args.clone:
        repo, _, path = item.partition("=")
        if not path or not pathlib.Path(path).exists():
            raise SystemExit(f"--clone {item}: немає такої теки")
        clones[repo] = pathlib.Path(path)

    # репо → {адреса: sha}; порядок джерел і тегів — як у sources.json
    plan: dict[str, dict[str, str]] = {}
    skipped = []
    docfx: list = []
    for src in sources:
        if src.get("reader") not in READERS:
            continue
        m = TREES.match(urlsplit(src["url"]).path)
        if not m:
            continue
        repo = f"{m.group(1)}/{m.group(2)}"
        if repo not in clones:
            continue
        if PLAIN & set(src):
            skipped.append(src["id"])
            continue
        ok = _selector(src)
        tags = [src["ref"]] if src["reader"] == "otel-registry" else list(src.get("tags") or {})
        if src["reader"] == "docfx":
            tags = [m.group(3)]
            docfx.append((src, clones[repo], m.group(3)))
        first: dict = {}
        for tag in tags:
            for path, sha in _ls(clones[repo], tag):
                if (path, sha) not in first and ok(path):
                    first[(path, sha)] = tag
        urls = plan.setdefault(repo, {})
        for (path, sha), tag in first.items():
            urls.setdefault(f"{RAW}/{repo}/{quote(tag, safe='@')}/{quote(path)}", sha)
        print(f"  {src['id']}: {len(first)} пар «шлях, вміст» на {len(tags)} тегах", flush=True)
    for src, clone, ref in docfx:
        dep = _docfx_dependent(src, clone, ref, clones)
        for url, sha in dep.items():
            owner, repo = urlsplit(url).path.split("/")[1:3]
            plan.setdefault(f"{owner}/{repo}", {}).setdefault(url, sha)
        print(f"  {src['id']}: файлів залежних репозиторіїв {len(dep)}", flush=True)
    for sid in skipped:
        print(f"  {sid}: поля розгортання, яких інструмент не знає, — лишається мережі", flush=True)
    if not plan:
        raise SystemExit("жодного джерела з клонів --clone не збіглося з sources.json")

    store = None if args.dry_run else rawstore.of(inst, time.strftime("%Y-%m-%d"))
    if args.trees and store is not None:
        _put_trees(store, sources, clones)
    for src, clone, ref in docfx if store is not None else ():
        _docfx_tree(store, src, clone, ref)
    if store is None and not args.dry_run:
        raise SystemExit(f"{inst}: сховище сирого вимкнено (raw_store: false)")
    t0 = time.time()
    written = present = 0
    for repo, urls in plan.items():
        clone = clones[repo]
        todo = {u: s for u, s in urls.items() if args.dry_run or store.meta(u) is None}
        present += len(urls) - len(todo)
        if args.dry_run:
            written += len(todo)
            print(f"  {repo}: адрес {len(urls)}, записав би {len(todo)}", flush=True)
            continue
        need = sorted(set(todo.values()))
        lost = _missing(clone, need)
        if lost:
            _fetch(clone, lost)
        proc = subprocess.Popen(["git", "--git-dir", str(clone), "cat-file", "--batch"],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                env=dict(os.environ, GIT_NO_LAZY_FETCH="1"))
        for url, sha in todo.items():
            proc.stdin.write((sha + "\n").encode())
            proc.stdin.flush()
            head = proc.stdout.readline().decode().split()
            if len(head) < 3 or head[1] == "missing":
                continue
            blob = proc.stdout.read(int(head[2]))
            proc.stdout.read(1)
            store.put(url, "", blob, {})
            written += 1
            if written % 5000 == 0:
                print(f"  {written} записів, {time.time() - t0:.0f} с", flush=True)
        proc.stdin.close()
        proc.wait()
        print(f"  {repo}: адрес {len(urls)}, записано {len(todo)}", flush=True)
    verb = "записав би" if args.dry_run else "записано"
    print(f"готово: {verb} {written}, уже були в сховищі {present}, {time.time() - t0:.0f} с")
    return 0


if __name__ == "__main__":
    sys.exit(main())
