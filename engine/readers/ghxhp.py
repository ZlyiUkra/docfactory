"""Читач довідки LibreOffice з репозиторію: сторінки `.xhp` на багатьох тегах разом.

`ghdocs-history-xhp` — `url` — префікс дерев (…/repos/ВЛАСНИК/РЕПО/git/trees/), `tags` — об'єкт
                       «тег → версія», від найновішого; `roots` — теки сторінок від кореня
                       репозиторію, перша наявна на тезі (`source/text`, а в 3.x —
                       `helpcontent2/source/text`). Необов'язкові: `exclude` — вирази шляхів
                       (від `text/…`), що не беруться; `site` — шаблон адреси сторінки на сайті з
                       `{version}` і `{page}` (шлях від `text/…` без `.xhp`), `site_since` — перша
                       версія, яку сайт ще тримає; старшим лишається blob на GitHub.

Навіщо. help.libreoffice.org зібрано з `LibreOffice/help`, але сайт тримає лише лінії 6.0–26.8, і на
кожну з них — тисячі сторінок HTML. Репозиторій має всі лінії з 3.3 одним клоном. Сторінка там — XML
`helpdocument` (розбір — у `_xhp`), що вставляє розділи інших сторінок (`<embed>`): синтаксис і приклад
функцій Calc, рядки «To access this command», назви колонок таблиць.

Одиниця, як у `ghdocs-history`, — сторінка з однаковим текстом у кількох версіях. Але текст залежить і
від вставок, тож редакція — це відбиток сторінки разом із відбитками вставлених елементів (не цілих
файлів: файл-збірник рядків меню міняється з кожним випуском, а вставлений з нього рядок — рідко).
Вставки беруться з того самого тегу. Кожна пара «шлях, вміст» читається з найновішого тегу, де вона
була, — саме під цією адресою її кладе й `tools/seed_git_store.py`.
"""

import hashlib
import json
import re
from collections import OrderedDict
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, _xhp, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")


def _vkey(v: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", v))


@register("ghdocs-history-xhp")
def ghdocs_history_xhp(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев /repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or not tags:
        raise SystemExit(f"{source['id']}: поле `tags` — об'єкт «тег → версія».")
    roots = [r.strip("/") for r in source.get("roots") or ["source/text"]]
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    site = source.get("site") or ""
    since = _vkey(str(source.get("site_since") or "0"))

    def raw_url(tag: str, path: str) -> str:
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{quote(tag, safe='@')}/{quote(path)}"

    # тег → {шлях від text/…: (повний шлях, sha)}
    trees: dict = {}
    # (повний шлях, sha) → найновіший тег, де пара була
    first: dict = {}
    for tag in tags:
        tree = None
        for root in roots:
            url = f"{source['url']}{quote(tag, safe='@')}:{quote(root)}?recursive=1"
            if not ctx.allowed(url):
                continue
            code, data = ctx.fetch(url)
            if code == "200":
                tree = (root, json.loads(data))
                break
        if tree is None:
            raise SystemExit(f"{source['id']}: на тезі {tag} немає жодної з тек {', '.join(roots)}.")
        root, data = tree
        if data.get("truncated"):
            raise SystemExit(f"{source['id']}: GitHub обрізав дерево {tag}:{root} — перелік був би неповним.")
        base = root[: -len("text")]  # «source/» чи «helpcontent2/source/»
        files = {}
        for e in data.get("tree", []):
            if e.get("type") != "blob" or not e["path"].endswith(".xhp") or not e.get("size"):
                continue
            rel = f"text/{e['path']}"
            full = f"{base}{rel}"
            files[rel] = (full, e["sha"])
            first.setdefault((full, e["sha"]), tag)
        trees[tag] = files

    # Тексти вставлених файлів і розібрані дерева — кеш на прогін: сторінок десятки тисяч, а
    # файлів, з яких вставляють, — кілька сотень на тег, і більшість однакові між тегами.
    texts: dict = {}
    parsed: OrderedDict = OrderedDict()

    def blob(full: str, sha: str) -> str:
        if sha not in texts:
            url = raw_url(first[(full, sha)], full)
            code, data = ctx.fetch(url) if ctx.allowed(url) else ("", b"")
            texts[sha] = data.decode("utf-8", errors="replace") if code == "200" else ""
        return texts[sha]

    def index_of(full: str, sha: str):
        if sha in parsed:
            parsed.move_to_end(sha)
            return parsed[sha]
        root = _xhp.parse(blob(full, sha))
        parsed[sha] = _xhp.ids(root) if root is not None else {}
        if len(parsed) > 400:
            parsed.popitem(last=False)
        return parsed[sha]

    # (sha, id) → (відбиток елемента, його вставки); (sha сторінки) → її вставки
    marks: dict = {}
    page_refs: dict = {}

    def mark(tag: str, rel: str, ident: str, depth: int) -> str:
        hit = trees[tag].get(rel)
        if hit is None:
            return f"{rel}#{ident}:-"
        full, sha = hit
        key = (sha, ident)
        if key not in marks:
            el = index_of(full, sha).get(ident)
            marks[key] = ("-", ()) if el is None else (_xhp.fingerprint(el), tuple(_xhp.refs(el)))
        print_, nested = marks[key]
        parts = [f"{rel}#{ident}:{print_}"]
        if depth < 4:
            parts += [mark(tag, r, i, depth + 1) for r, i in nested]
        return "|".join(parts)

    seen: dict = {}
    for tag, files in trees.items():
        for rel, (full, sha) in files.items():
            if any(r.search(rel) for r in exclude):
                continue
            if sha not in page_refs:
                page_refs[sha] = tuple(dict.fromkeys(
                    (p, i) for p, i in _xhp.EMBED.findall(blob(full, sha)) if not p.startswith("http")))
                # Текст самої сторінки в кеші не тримаємо: make прочитає його ще раз зі сховища.
                if not any(p == rel for p, _ in page_refs[sha]):
                    texts.pop(sha, None)
            rev = sha
            if page_refs[sha]:
                chain = sha + "".join(mark(tag, p, i, 0) for p, i in page_refs[sha])
                rev = hashlib.sha1(chain.encode()).hexdigest()
            stem = rel[: -len(".xhp")]
            name = f"{_markup.slug(stem)}-{rev[:8]}"
            seen.setdefault(name, [rel, full, sha, []])[3].append(tag)

    items = []
    for name, (rel, full, sha, found) in seen.items():
        tag = found[0]
        raw = raw_url(first[(full, sha)], full)
        if not ctx.allowed(raw):
            continue
        version = ", ".join(dict.fromkeys(str(tags[t]) for t in found))
        newest = str(tags[tag])
        cite = f"https://github.com/{owner}/{repo}/blob/{quote(tag, safe='@')}/{quote(full)}"
        if site and _vkey(newest) >= since:
            cite = site.replace("{version}", newest).replace("{page}", rel[: -len(".xhp")])

        def make(rel=rel, full=full, sha=sha, tag=tag, raw=raw, cite=cite, version=version,
                 newest=newest):
            text = ctx.text(raw)
            root = _xhp.parse(text)
            if root is None:
                raise SystemExit(f"{raw}: XML сторінки не розбирається — документ не записую.")

            def resolve(path: str, ident: str, tag=tag):
                hit = trees[tag].get(path)
                if hit is None:
                    return None
                if hit[1] == sha:
                    return local.get(ident)
                return index_of(*hit).get(ident)

            local = _xhp.ids(root)
            title, body = _xhp.to_markdown(root, resolve, newest)
            if not title:
                title = rel.rsplit("/", 1)[-1]
            if body.strip():
                _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, cite, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодної сторінки .xhp на жодному з {len(tags)} тегів.")
    return items
