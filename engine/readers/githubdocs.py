"""Читач GitHub Docs: сторінки репозиторію github/docs з розібраним шаблоном Liquid.

`github-docs` — `url`     — префікс дерев GitHub (…/repos/github/docs/git/trees/);
                `ref`     — гілка чи коміт (типово «main»);
                `folders` — теки `content/…`, сторінки яких беруться (з вкладеними);
                `files`   — окремі сторінки поза ними;
                `exclude` — вирази шляхів, що не беруться;
                `version` — мітка версії документів (у GitHub Docs немає версій github.com:
                            сторінка описує поточний стан, тож мітка одна на джерело).

Навіщо окремий читач. Сторінки docs.github.com — markdown, але кожна третя фраза в них
шаблон: `{% data reusables.actions.… %}` вставляє спільний абзац з `data/reusables`,
`{% data variables.product.prodname_actions %}` — назву продукту з `data/variables/*.yml`,
`{% ifversion ghes %}…{% else %}…{% endif %}` — гілку для GitHub Enterprise Server чи для
github.com, а посилання пишуться `[AUTOTITLE](/actions/…)` — назву підставляє сайт. Без
розбору текст у корпусі діравий: замість синтаксису workflow — рядок
`{% data reusables.actions.workflows.workflow-syntax-name %}`.

Що робить читач:
- бере лише сторінки, які сайт показує для github.com (`versions` шапки містить `fpt` —
  Free, Pro і Team, — прямо чи через функцію з `data/features`);
- у гілках `ifversion` лишає ту, що діє для github.com: `fpt` — так, `ghes`, `ghec` і
  порівняння версій GHES — ні, функція з `data/features` — за її `versions`;
- підставляє спільні абзаци (вкладені теж) і змінні, кожен файл читає один раз;
- `[AUTOTITLE](/шлях)` замінює назвою сторінки з того ж джерела, інакше — останнім
  сегментом шляху;
- вміст `{% raw %}` лишає як є: там приклади workflow з `${{ … }}`;
- коментарі, піктограми й службові теги викидає;
- сторінка-зміст (`index.md`) без власного тексту дістає перелік назв дочірніх сторінок.

Перелік складається з самих сторінок: щоб знати, чи показує сайт сторінку на github.com, треба
прочитати її шапку. Тексти сторінок тримаються в пам'яті до запису — це кількасот файлів по
кілька кілобайтів.
"""

import json
import re
from urllib.parse import quote, urlsplit

import yaml

from engine.readers import Item, _markup, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_FRONT = re.compile(r"\A---\n(.*?)\n---\n?", re.S)
_TAG = re.compile(r"\{%-?\s*(\w+)(.*?)-?%\}", re.S)
_AUTOTITLE = re.compile(r"\[AUTOTITLE\]\(([^)\s]+)\)")
_SITE = "https://docs.github.com/en"
_BLOCKS = {"ifversion": "endif", "if": "endif", "unless": "endunless", "comment": "endcomment",
           "raw": "endraw", "capture": "endcapture", "for": "endfor"}
# Теги, що лише обгортають текст: сам текст лишається.
_WRAPPERS = {"note", "endnote", "tip", "endtip", "warning", "endwarning", "danger", "enddanger",
             "caution", "endcaution", "important", "endimportant", "prompt", "endprompt",
             "rowheaders", "endrowheaders", "mac", "endmac", "windows", "endwindows", "linux",
             "endlinux", "webui", "endwebui", "cli", "endcli", "desktop", "enddesktop",
             "vscode", "endvscode", "visualstudio", "endvisualstudio", "jetbrains",
             "endjetbrains", "javascript", "endjavascript", "curl", "endcurl"}
_DEPTH = 12


class _Docs:
    """Дані сайту: змінні, функції й спільні абзаци, кожен файл — одне звернення."""

    def __init__(self, owner: str, repo: str, ref: str, paths: set, ctx):
        self.raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{quote(ref, safe='')}/"
        self.paths, self.ctx = paths, ctx
        self.vars: dict = {}
        self.features: dict = {}
        self.reusables: dict = {}
        self.titles: dict = {}

    def _yaml(self, path: str):
        if path not in self.paths:
            return None
        try:
            return yaml.safe_load(self.ctx.text(self.raw + quote(path)))
        except yaml.YAMLError:
            return None

    def variable(self, dotted: str) -> str:
        name, _, rest = dotted.partition(".")
        if name not in self.vars:
            self.vars[name] = self._yaml(f"data/variables/{name}.yml") or {}
        node = self.vars[name]
        for key in rest.split(".") if rest else ():
            node = node.get(key) if isinstance(node, dict) else None
        return node if isinstance(node, str) else ""

    def feature_on(self, name: str) -> bool:
        if name not in self.features:
            data = self._yaml(f"data/features/{name}.yml") or {}
            self.features[name] = on_dotcom(data.get("versions"), self) if data else False
        return self.features[name]

    def reusable(self, dotted: str) -> str | None:
        path = "data/reusables/" + dotted.replace(".", "/") + ".md"
        if path not in self.reusables:
            self.reusables[path] = (self.ctx.text(self.raw + quote(path))
                                    if path in self.paths else None)
        return self.reusables[path]


def on_dotcom(versions, docs: _Docs) -> bool:
    """Чи показує сайт сторінку (чи функцію) на github.com."""
    if isinstance(versions, str):
        return docs.feature_on(versions)
    if not isinstance(versions, dict):
        return False
    if "fpt" in versions:
        return True
    feature = versions.get("feature")
    names = feature if isinstance(feature, list) else [feature] if feature else []
    return any(docs.feature_on(n) for n in names)


def _cond(expr: str, docs: _Docs) -> bool:
    """Умова ifversion для github.com: `fpt or ghec`, `ghes > 3.10`, `not ghes`, функції."""
    expr = expr.strip()
    if " or " in expr:
        return any(_cond(e, docs) for e in expr.split(" or "))
    if " and " in expr:
        return all(_cond(e, docs) for e in expr.split(" and "))
    if expr.startswith("not "):
        return not _cond(expr[4:], docs)
    words = expr.split()
    if not words:
        return False
    if len(words) > 1:          # порівняння версії: ghes < 3.12, ghec = …
        return words[0] == "fpt"
    name = words[0]
    if name == "fpt":
        return True
    if name in ("ghes", "ghec", "ghae", "enterprise"):
        return False
    return docs.feature_on(name)


def render(text: str, docs: _Docs, depth: int = 0) -> str:
    """Liquid сторінки → markdown для github.com."""
    if depth > _DEPTH:
        return ""
    out: list[str] = []
    pos = 0
    while True:
        m = _TAG.search(text, pos)
        if not m:
            out.append(text[pos:])
            break
        out.append(text[pos:m.start()])
        name, arg = m.group(1), m.group(2).strip()
        pos = m.end()
        if name in _BLOCKS:
            body, branches, pos = _block(text, pos, name)
            if name == "raw":
                out.append(body)
            elif name in ("ifversion", "if", "unless"):
                for cond, chunk in branches:
                    hit = cond is None or _cond(cond if cond is not True else arg, docs)
                    if name == "unless" and cond is True:
                        hit = not hit
                    if hit:
                        out.append(render(chunk, docs, depth + 1))
                        break
            elif name == "for":
                out.append(render(body, docs, depth + 1))
            continue
        if name == "data":
            out.append(_data(arg.split()[0] if arg else "", docs, depth))
        elif name == "indented_data_reference":
            parts = arg.split()
            spaces = next((int(p.split("=")[1]) for p in parts[1:] if p.startswith("spaces=")
                           and p.split("=")[1].isdigit()), 0)
            chunk = _data(parts[0] if parts else "", docs, depth)
            out.append("\n".join((" " * spaces + ln) if ln.strip() else ln
                                 for ln in chunk.split("\n")))
        elif name in ("link", "link_in_list", "link_with_intro", "homepage_link_with_intro",
                      "link_as_article_card", "link_with_short_title"):
            path = arg.split()[0] if arg else ""
            out.append(("- " if name == "link_in_list" else "") + _title_of(path, docs))
        # Решта тегів (піктограми, службові обгортки, невідомі) зникає, текст лишається.
    return "".join(out)


def _block(text: str, pos: int, name: str):
    """(тіло, [(умова, гілка)…], позиція за кінцем блоку). Умова першої гілки — True
    (аргумент самого тегу), `elsif` дає свій вираз, `else` — None."""
    end = _BLOCKS[name]
    depth, start, cond = 1, pos, True
    branches = []
    body_start = pos
    while True:
        m = _TAG.search(text, pos)
        if not m:
            branches.append((cond, text[start:]))
            return text[body_start:], branches, len(text)
        tag = m.group(1)
        if name == "raw":
            if tag == "endraw":
                return text[body_start:m.start()], [], m.end()
            pos = m.end()
            continue
        if tag == name or (tag in _BLOCKS and _BLOCKS[tag] == end and tag != name
                           and name in ("ifversion", "if")):
            depth += 1
        elif tag == end:
            depth -= 1
            if depth == 0:
                branches.append((cond, text[start:m.start()]))
                return text[body_start:m.start()], branches, m.end()
        elif depth == 1 and tag in ("elsif", "else") and name in ("ifversion", "if", "unless"):
            branches.append((cond, text[start:m.start()]))
            cond = m.group(2).strip() if tag == "elsif" else None
            start = m.end()
        pos = m.end()


def _data(dotted: str, docs: _Docs, depth: int) -> str:
    if dotted.startswith("variables."):
        return render(docs.variable(dotted[len("variables."):]), docs, depth + 1)
    if dotted.startswith("reusables."):
        text = docs.reusable(dotted[len("reusables."):])
        return render(text.rstrip("\n"), docs, depth + 1) if text else ""
    return ""


def _title_of(link: str, docs: _Docs) -> str:
    path = link.split("#", 1)[0].rstrip("/")
    path = re.sub(r"^/(en/)?", "", path)
    if path in docs.titles:
        return docs.titles[path]
    tail = path.rsplit("/", 1)[-1] or path
    return tail.replace("-", " ").capitalize()


def _page_path(path: str) -> str:
    """content/actions/x/index.md → actions/x; content/actions/x/y.md → actions/x/y."""
    p = path[len("content/"):-len(".md")]
    return p[:-len("/index")] if p.endswith("/index") else p


@register("github-docs")
def github_docs(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев /repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    ref = source.get("ref") or "main"
    label = str(source.get("version") or "")
    folders = [f.strip("/") + "/" for f in source.get("folders") or ()]
    files = {f.strip("/") for f in source.get("files") or ()}
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    url = f"{source['url']}{quote(ref, safe='')}?recursive=1"
    try:
        tree = json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}).")
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
    if tree.get("truncated"):
        raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
    paths = {e["path"] for e in tree["tree"] if e.get("type") == "blob"}
    docs = _Docs(owner, repo, ref, paths, ctx)
    wanted = sorted(p for p in paths if p.endswith(".md")
                    and (p in files or any(p.startswith(f) for f in folders))
                    and not any(r.search(p) for r in exclude))

    pages = []
    for path in wanted:
        raw = ctx.text(docs.raw + quote(path)).replace("\r\n", "\n")
        fm = _FRONT.match(raw)
        try:
            meta = yaml.safe_load(fm.group(1)) if fm else {}
        except yaml.YAMLError:
            meta = {}
        meta = meta if isinstance(meta, dict) else {}
        if not on_dotcom(meta.get("versions"), docs):
            continue
        body = raw[fm.end():] if fm else raw
        title = " ".join(render(str(meta.get("title") or ""), docs).split())
        docs.titles[_page_path(path)] = title
        pages.append((path, meta, body, title))
    skipped = len(wanted) - len(pages)
    if skipped:
        print(f"  {source['id']}: {skipped} сторінок лише для GitHub Enterprise — не беру")

    items = []
    for path, meta, body, title in pages:
        name = _markup.slug(_page_path(path))
        page = f"{_SITE}/{_page_path(path)}"

        def make(path=path, meta=meta, body=body, title=title, page=page):
            text = render(body, docs)
            text = _AUTOTITLE.sub(lambda mm: _title_of(mm.group(1), docs), text)
            intro = " ".join(render(str(meta.get("intro") or ""), docs).split())
            md = _markup.markdown_body(text)
            if not re.search(r"\w", md) and meta.get("children"):
                base = _page_path(path)
                md = "\n".join("- " + _title_of(f"/{base}{c}" if c.startswith("/") else c, docs)
                               for c in meta["children"])
            md = (intro + "\n\n" + md).strip() if intro else md.strip()
            _markup.require(title or path, md, path, min_chars=1)
            return _markup.document(title or path, page, ctx.stamp, md, label)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодної сторінки для github.com.")
    return items
