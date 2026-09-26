"""Читач прикладів із репозиторію: одна тека прикладу — один документ із кодом.

`ghexamples` — приклади з теки `examples/` на тезі чи коміті. `url` — дерево тегу
               /repos/ВЛАСНИК/РЕПО/git/trees/ТЕГ?recursive=1; прикладом вважається
               кожна тека всередині `examples/`, де лежить власний `package.json`.

Навіщо. Сторінка прикладу на сайті TanStack Query (…/examples/simple) markdown-двійника
не має: вона показує код, який підтягує з теки прикладу в репозиторії. Тож приклад
береться звідти ж, звідки його бере сайт, і стає документом: назва й README, далі
кожен файл коду окремим розділом «## шлях» із блоком коду. Так уривок про
`useQuery` у прикладі веде до файла, де той рядок стоїть.

Що береться. Код (`.ts`, `.tsx`, `.js`, `.jsx`, `.mjs`, `.vue`, `.svelte`, `.astro`),
шаблони `.html` — в Angular це справжній код компонентів, — README і з JSON лише
`package.json`: з нього видно, на якій версії бібліотеки написано приклад. Що ні:
кореневий `index.html` (однакова заготовка Vite), конфіги збірки й лінтера,
оголошення типів `.d.ts`, стилі, картинки й файли понад _MAX_FILE — це згенероване,
а не написане людиною. Прикладами за структурою тек не вгадується: `package.json`
і в старих тегах, де приклади лежать без теки фреймворку (`examples/basic`), і в
нових (`examples/react/basic`).
"""

import json
import posixpath
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register

_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/(.+)$")
_MAX_FILE = 40_000
_CODE = {".ts": "ts", ".tsx": "tsx", ".js": "js", ".jsx": "jsx", ".mjs": "js",
         ".vue": "vue", ".svelte": "svelte", ".astro": "astro", ".html": "html"}
_SKIP = re.compile(r"(^\.|(^|[.-])config\.|^tsconfig|\.d\.ts$|lock)")


def _wanted(rel: str, size: int) -> str | None:
    """Мова блоку коду для файла прикладу, «» для README, None — файл не береться."""
    leaf = rel.rsplit("/", 1)[-1]
    if size > _MAX_FILE or _SKIP.search(leaf) or rel.startswith(("public/", "node_modules/")):
        return None
    if rel == "README.md":
        return ""
    if rel == "package.json":
        return "json"
    if rel == "index.html":
        return None
    return _CODE.get(posixpath.splitext(leaf)[1])


@register("ghexamples")
def ghexamples(source: dict, ctx) -> list[Item]:
    m = _TREE.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував адресу дерева тегу "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/ТЕГ.")
    owner, repo, tag = m.groups()
    try:
        tree = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        raise SystemExit(f"{source['url']}: у відповіді немає дерева файлів.")
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")
    blobs = {e["path"]: e.get("size", 0) for e in tree["tree"]
             if e.get("type") == "blob" and e.get("path", "").startswith("examples/")}
    roots = sorted(posixpath.dirname(p) for p in blobs if p.endswith("/package.json"))
    # Тека прикладу всередині іншого прикладу (рідко, але буває) — окремий приклад, і
    # її файли не мусять удруге лягти в зовнішній.
    nested = lambda path, root: any(r != root and r.startswith(root + "/")
                                    and path.startswith(r + "/") for r in roots)
    ref = quote(tag, safe="@")
    items = []
    for root in roots:
        files = []
        for path in sorted(blobs):
            if not path.startswith(root + "/") or nested(path, root):
                continue
            lang = _wanted(path[len(root) + 1:], blobs[path])
            if lang is not None:
                files.append((path, lang))
        raws = [f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{quote(p)}"
                for p, _ in files]
        if not files or not all(ctx.allowed(r) for r in raws):
            continue
        page = f"https://github.com/{owner}/{repo}/tree/{ref}/{quote(root)}"
        name = _markup.slug(root)

        def make(root=root, files=files, raws=raws, page=page):
            title = f"Example: {root.removeprefix('examples/')}"
            parts = []
            for (path, lang), raw in zip(files, raws):
                text = ctx.text(raw)
                # Шаблон Angular сам є HTML, тож перевірка «прийшла сторінка помилки
                # замість файла» для нього означала б відмову від справжнього коду.
                if lang != "html":
                    _markup.refuse_html(text, raw)
                rel = path[len(root) + 1:]
                if lang == "":
                    meta, rest = _markup.front_matter(text)
                    parts.append(_markup.markdown_body(rest).strip())
                else:
                    parts.append(f"## {rel}\n\n```{lang}\n{text.rstrip()}\n```")
            body = "\n\n".join(p for p in parts if p)
            _markup.require(title, body, page, min_chars=1)
            return _markup.document(title, page, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['url']}: у теці examples/ жодного прикладу з package.json.")
    return items
