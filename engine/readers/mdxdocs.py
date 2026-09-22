"""Читач документації MDX із репозиторію: те саме, що `ghdocs`, але для `.mdx`.

`ghdocs-mdx` — markdown-документація на тезі чи коміті репозиторію, де сторінки
               лежать не `.md`, а `.mdx`: приймаються обидва розширення, решта
               полів та сама, що в `ghdocs` (`folders`, `recursive`, `root`).

Навіщо. Чинний `ghdocs` бере лише `.md` — рівно одна умова в переліку файлів, — і
для документації Astro це означає порожній перелік: усі 422 англійські глави
`withastro/docs` мають розширення `.mdx`, і так від другої лінії. Перша лінія ще
писалася `.md`, тож обидва розширення потрібні одному й тому самому джерелу.

Чому копія, а не умова в `ghdocs`. Примірники `ecmascript`, `react` і `nestjs`
зібрані й звірені, а правка спільного читача — ризик зсуву в готовій роботі; хто
не назвав ім'я `ghdocs-mdx` у sources.json, того цей модуль не стосується. Так
само зроблено з `mdheading` і `ngpages`.

Дві особливості MDX, яких немає в markdown і які інакше лягли б у корпус текстом:

1. Рядки імпорту на початку сторінки — `import ReadMore from '~/components/…'`.
   Це код збірки, а не текст глави; у Astro їх до двох десятків на сторінку, і в
   уривку вони виглядали б як частина відповіді.

2. Виноски Starlight — `:::note`, `:::tip[Своя назва]`, `:::caution`. Це не
   компоненти MDX, а власна розмітка, тож `_markup` про них не знає й лишив би
   двокрапки в тексті. Тут вони стають підписом («Note:»), а зміст виноски лишається
   абзацом — рівно так, як `_markup` чинить із компонентами react.dev.
"""

import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register

_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/([^/]+)$")
# Переклад: «astro-components.ko-KR.mdx». Корпус англійський.
_LOCALE = re.compile(r"\.[a-z]{2}-[A-Z]{2}\.mdx?$")
# Позиція у старому змісті: «02.1-jsx-in-depth», «1-setup». Зі слага знімається,
# щоб та сама сторінка сусідніх ліній мала те саме ім'я й незмінний текст зливався.
_POSITION = re.compile(r"(^|/)\d+(?:\.\d+)*-")
_IMPORT = re.compile(r"^import\s+.+\s+from\s+['\"].+['\"];?\s*$")
_ASIDE = re.compile(r"^:::(\w+)(?:\[([^\]]*)\])?\s*$")
_ASIDE_END = re.compile(r"^:::\s*$")
_ASIDE_LABELS = {
    "note": "Note:", "tip": "Tip:", "caution": "Caution:", "danger": "Danger:",
    "warning": "Warning:",
}


def _plain_mdx(text: str) -> str:
    """Текст MDX без рядків імпорту й без двокрапок виносок Starlight."""
    out = []
    for raw in text.replace("\r\n", "\n").split("\n"):
        line = raw.rstrip()
        if _IMPORT.match(line.strip()):
            continue
        m = _ASIDE.match(line.strip())
        if m:
            label = m.group(2) or _ASIDE_LABELS.get(m.group(1).lower())
            out += ["", f"{label.rstrip(':')}:" if label else "", ""]
            continue
        if _ASIDE_END.match(line.strip()):
            out.append("")
            continue
        out.append(line)
    return "\n".join(out)


@register("ghdocs-mdx")
def ghdocs_mdx(source: dict, ctx) -> list[Item]:
    m = _TREE.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував адресу дерева тегу "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/ТЕГ.")
    owner, repo, tag = m.groups()
    try:
        import json
        tree = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        raise SystemExit(f"{source['url']}: у відповіді немає дерева файлів.")
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")
    folders = [f.strip("/") for f in source.get("folders") or ["docs"]]
    recursive = source.get("recursive") is True
    root = source.get("root", "").strip("/")
    paths = []
    for entry in tree["tree"]:
        path = entry.get("path", "")
        folder, _, leaf = path.rpartition("/")
        inside = (folder in folders if not recursive else
                  any(folder == f or folder.startswith(f + "/") for f in folders))
        if (entry.get("type") == "blob" and inside
                and leaf.endswith((".md", ".mdx")) and not _LOCALE.search(leaf)):
            paths.append(path)
    items = []
    for path in paths:
        raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{tag}/{path}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{tag}/{path}"
        if root and path.startswith(root + "/"):
            rel = path[len(root) + 1:]
        else:
            rel = path.split("/", 1)[1] if "/" in path else path
        stem = rel.removesuffix(".mdx").removesuffix(".md")
        # «tutorial/0-introduction/index.mdx» — сторінка «/tutorial/0-introduction»:
        # без зрізаного «/index» ім'я розходилося б із тим самим документом сусідньої лінії.
        stem = re.sub(r"(^|/)index$", "", stem) or "index"
        name = _markup.slug(_POSITION.sub(r"\1", stem))

        def make(raw=raw, blob=blob):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            meta, rest = _markup.front_matter(text)
            body = _markup.markdown_body(_plain_mdx(rest))
            title = _markup.title_of(meta, blob) if meta else ""
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['url']}: у теках {', '.join(folders)} немає жодного "
                         f"дозволеного .md або .mdx.")
    return items
