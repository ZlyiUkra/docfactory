"""Читач коду з репозиторію: один файл — один документ із блоком коду.

`ghcode` — усі файли дерева гілки чи тегу, крім тих, що відкидає `exclude`. `url` —
           дерево /repos/ВЛАСНИК/РЕПО/git/trees/ГІЛКА?recursive=1; `exclude` —
           вирази шляхів, що не беруться (службові файли, згенероване, markdown,
           який уже бере інше джерело).

Навіщо. `ghexamples` вміє лише приклади JavaScript із власним `package.json`, а
навчальний репозиторій на кшталт `danbev/learning-v8` тримає код інакше: тести
вбудовування V8 на C++ (`test/*_test.cc`), програми поруч із README, Torque,
приклад на Rust, команди lldb. Нотатки посилаються саме на ці файли, тож без них
пояснення «як виглядає Handle» лишається без коду, який його показує.

Документ — один файл, а не тека: у шапку лягає адреса самого файла, і уривок про
`HandleScope` веде точно туди, де той рядок стоїть. Назва — «репозиторій: шлях»,
щоб у видачі код не плутався зі сторінками сайту з тією самою темою. Markdown, що
потрапив у перелік (README теки прикладу), розбирається як markdown; решта лягає
блоком коду з мовою за розширенням. Файли понад _MAX_FILE не беруться: таке в
навчальному репозиторії — згенероване, а не написане людиною.
"""

import json
import posixpath
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register

_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/(.+)$")
_MAX_FILE = 40_000
_LANG = {".cc": "cpp", ".h": "cpp", ".cpp": "cpp", ".c": "c", ".js": "js", ".mjs": "js",
         ".ts": "ts", ".tq": "torque", ".rs": "rust", ".py": "python", ".toml": "toml",
         ".patch": "diff", ".sh": "sh", ".json": "json", ".md": ""}
_NAMED = {"Makefile": "make", "BUILD.gn": "gn"}


def _lang(path: str) -> str:
    """Мова блоку коду: за іменем файла, за розширенням, інакше простий текст."""
    leaf = path.rsplit("/", 1)[-1]
    return _NAMED.get(leaf) or _LANG.get(posixpath.splitext(leaf)[1], "text")


@register("ghcode")
def ghcode(source: dict, ctx) -> list[Item]:
    m = _TREE.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував адресу дерева гілки "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/ГІЛКА.")
    owner, repo, ref = m.groups()
    try:
        tree = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        raise SystemExit(f"{source['url']}: у відповіді немає дерева файлів.")
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")
    exclude = [re.compile(x) for x in source.get("exclude") or []]
    ref = quote(ref, safe="@")
    items = []
    for entry in tree["tree"]:
        path = entry.get("path", "")
        if (entry.get("type") != "blob" or entry.get("size", 0) > _MAX_FILE
                or any(x.search(path) for x in exclude)):
            continue
        raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{quote(path)}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{ref}/{quote(path)}"
        name = _markup.slug(path)

        def make(path=path, raw=raw, blob=blob):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            lang = _lang(path)
            if lang == "":
                _, rest = _markup.front_matter(text)
                body = _markup.markdown_body(rest).strip()
            else:
                body = f"```{lang}\n{text.rstrip()}\n```"
            title = f"{repo}: {path}"
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['url']}: жодного дозволеного файла поза `exclude`.")
    return items
