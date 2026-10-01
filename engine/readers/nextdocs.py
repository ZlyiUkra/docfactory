"""Читач історії документації Next.js: кожен неповторний текст сторінки один раз, з усіма версіями.

`nextdocs-history` — те саме, що `ghdocs-history` (документ — неповторна пара «шлях, вміст», а в
                     його версії лягають усі теги, де файл був саме таким), з тими самими полями
                     `url` (префікс дерев …/repos/ВЛАСНИК/РЕПО/git/trees/), `tags` («тег →
                     версія», від найновішого), `folders`, `extensions`, `exclude`. Теки завжди
                     беруться з вкладеними.

Навіщо окремий читач. У vercel/next.js три речі, яких `ghdocs-history` не знає.

1. Сторінки Pages Router — заглушки. Файл `docs/02-pages/…/image.mdx` — це шапка з полем
   `source: app/api-reference/components/image` і жодного тексту: сайт будує сторінку з файла
   App Router, де спільний текст лежить як є, а різне загорнуте в `<AppOnly>` і `<PagesOnly>`.
   Узяті як є, сторінки Pages Router були б порожні, а в сторінках App Router код обох роутерів
   стояв би впереміш без підпису — і відповідь про `pages/` цитувала б приклад для `app/`.
   Тут заглушка стає повною сторінкою: текст джерела на тому самому тегу, з блоками лише свого
   роутера. Сторінка App Router лишає `<AppOnly>` і губить `<PagesOnly>`. Спільна сторінка поза
   обома теками (у 13.4–15 це «Getting Started») тримає обидва блоки з підписом роутера.
   Документ-заглушка — пара «заглушка, джерело»: зміна будь-якого з двох файлів дає новий
   документ, а версії — теги, де обидва були саме такими.

2. Дерево репозиторію завелике. Рекурсивне дерево тегу — 50 тисяч записів і кілька мегабайтів,
   а тегів з документацією майже чотири тисячі: `ghdocs-history` тягнув би гігабайти заради
   п'ятисот файлів. Тут на тег береться лише корінь (без рекурсії, шістдесят записів), з нього
   — хеш піддерева теки, а саме піддерево читається один раз на хеш: між сусідніми canary
   документація здебільшого не змінюється, і хеш той самий.

3. Номери порядку в шляхах. `docs/01-app/03-api-reference/02-components/image.mdx` на сайті —
   /docs/app/api-reference/components/image, а номери з часом міняються (`02-app` стало
   `01-app`). В імені документа їх немає: інша нумерація того самого файла — той самий документ.

Дрібніше: ім'я файла з огорожі коду (```tsx filename="app/page.tsx"```) лишається рядком перед
блоком — без нього не видно, в який файл цей код класти; опис із шапки стає першим абзацом, бо
сторінки-рубрики, крім нього, тексту не мають; назва дістає префікс роутера («App Router: Image»
і «Pages Router: Image» — різні сторінки з однаковою назвою).

Чому окремий модуль, а не поля в `ghdocs-history`: примірники, зібрані ним, звірені, а правка
спільного читача — ризик зсуву в готовій роботі.
"""

import hashlib
import json
import re
from html import unescape
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.ghhistory import _atx, _split_title

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_LOCALE = re.compile(r"\.[a-z]{2}-[A-Z]{2}\.mdx?$")
_ORDER = re.compile(r"(^|/)\d+-")
_FENCE = re.compile(r"^\s*(```+|~~~+)\s*(.*)$")
_FILENAME = re.compile(r'\bfilename="([^"]+)"')
_ROUTER_TAG = re.compile(r"(</?(?:AppOnly|PagesOnly)>)")
_ROUTER = {"AppOnly": "app", "PagesOnly": "pages"}
_ROUTER_LABEL = {"app": "App Router:", "pages": "Pages Router:"}
_TITLE_PREFIX = {"app": "App Router: ", "pages": "Pages Router: "}
_FOLDED = (">", ">-", "|", "|-")
_TAG_OPEN = re.compile(r"^\s*<([A-Za-z][A-Za-z0-9.]*)(?=\s|$)")
_TAG_TITLE = re.compile(r'\btitle="([^"]*)"')

# Заглушка — шапка з кількох рядків; найдовші (з блоком `related`) не дотягують і до
# кілобайта. Файл, більший за цю межу, заглушкою бути не може, і його шапку під час
# складання переліку читати не треба.
_STUB_MAX = 2000
# Обхід тисяч тегів триває години, і без рядка поступу його не відрізнити від зависання.
_PROGRESS = 250
# Найдовший відкривний тег у документації — два з половиною десятки рядків. Якщо «>» не
# знайшовся й за вісімдесят, це не тег, а текст, де рядок почався з «<», і чіпати його не можна.
_TAG_MAX = 80


def _plain(path: str) -> str:
    """Шлях без номерів порядку: «01-app/03-api-reference» → «app/api-reference»."""
    return _ORDER.sub(r"\1", path)


def _router_of(folder: str, plain_rel: str) -> str:
    """Чий це файл: «app», «pages» або спільний (порожній рядок)."""
    top = plain_rel.split("/", 1)[0]
    return top if folder == "docs" and top in _TITLE_PREFIX and "/" in plain_rel else ""


def _blocks(text: str, keep: str) -> str:
    """Текст сторінки для одного роутера. `keep` — «app» чи «pages»: блоки чужого роутера
    зникають, свого — лишаються без тегів. Порожній `keep` — спільна сторінка: обидва блоки
    лишаються з підписом роутера. Код між огорожами не чіпається; ім'я файла з огорожі
    стає рядком перед блоком; багаторядковий коментар MDX зникає."""
    out: list[str] = []
    fence, skip, comment = "", "", False
    for ln in text.split("\n"):
        m = _FENCE.match(ln)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) \
                    and not m.group(2).strip():
                fence = ""
            if not skip:
                out.append(ln)
            continue
        if comment:
            if "*/}" not in ln:
                continue
            ln, comment = ln.split("*/}", 1)[1], False
            if not ln.strip():
                continue
        if m:
            fence = m.group(1)
            if not skip:
                name = _FILENAME.search(m.group(2))
                if name:
                    out.extend([f"`{name.group(1)}`", ""])
                out.append(ln)
            continue
        if "{/*" in ln and "*/}" not in ln.split("{/*", 1)[1]:
            ln, comment = ln.split("{/*", 1)[0], True
        if "Only>" not in ln:
            if not skip:
                out.append(ln)
            continue
        # Підпис роутера — лише блокові, що стоїть окремим рядком; тег посеред речення
        # на спільній сторінці просто знімається, інакше підпис розірвав би речення.
        alone = bool(_ROUTER_TAG.fullmatch(ln.strip()))
        kept, tagged = "", False
        for part in _ROUTER_TAG.split(ln):
            t = re.fullmatch(r"<(/?)(AppOnly|PagesOnly)>", part)
            if not t:
                if not skip:
                    kept += part
                continue
            tagged = True
            which = _ROUTER[t.group(2)]
            if t.group(1):
                if skip == which:
                    skip = ""
                elif not keep and not skip and not alone:
                    kept += " "
            elif keep and which != keep:
                skip = skip or which
            elif not keep and not skip and alone:
                out.extend(["", _ROUTER_LABEL[which], ""])
        if kept.strip() or not tagged:
            out.append(kept)
    return "\n".join(out)


def _tag_end(lines: list[str], start: int, pos: int) -> tuple[int, int] | None:
    """Де закривається тег, відкритий у рядку `start`: (рядок, позиція «>»); `pos` — позиція
    одразу за іменем тегу. «>» у лапках чи фігурних дужках тег не закриває: значення атрибута
    — довільний JavaScript, і стрілка функції чи JSX рядком там звичайні. None — це не тег:
    до «>» трапився другий «<» чи огорожа коду, або кінця немає й за `_TAG_MAX` рядків."""
    quote, depth = "", 0
    for i in range(start, min(start + _TAG_MAX, len(lines))):
        if i > start and _FENCE.match(lines[i]):
            return None
        for j in range(pos, len(lines[i])):
            ch = lines[i][j]
            if quote:
                quote = "" if ch == quote else quote
            elif ch in "'\"`":
                quote = ch
            elif ch in "{}":
                depth += 1 if ch == "{" else -1
            elif ch in "<>" and depth <= 0:
                return (i, j) if ch == ">" else None
        pos = 0
    return None


def _multiline_tags(text: str) -> str:
    """Текст без відкривних тегів JSX на кілька рядків, з якими не дає ради спільний розбір
    markdown. Той знає лише компонент з великої літери й закриває тег на першому ж рядку з
    «>»: від `<div style={{…}}>` у тексті лишалися рядки CSS, від `<FixCard snippets={[…]} />`
    — хвіст масиву за першим «>» у рядку-значенні. Від такого тегу тут лишається `title`
    окремим рядком і те, що стоїть за «>». Тег, який спільний розбір знімає сам
    (`<Image … />`), не чіпається: що з нього лишати, вирішено там. Код між огорожами — теж."""
    lines = text.split("\n")
    out: list[str] = []
    fence, i = "", 0
    while i < len(lines):
        ln = lines[i]
        m = _FENCE.match(ln)
        if fence:
            if m and m.group(1).startswith(fence) and not m.group(2).strip():
                fence = ""
        elif m:
            fence = m.group(1)
        else:
            tag = _TAG_OPEN.match(ln)
            last, pos = (_tag_end(lines, i, tag.end()) if tag else None) or (i, 0)
            # Спільний розбір дає раду, лише коли ім'я з великої літери, за ним у першому
            # рядку немає «<» і «>», а далі «>» уперше трапляється в останньому рядку тегу.
            if last > i and (tag.group(1)[0].islower() or re.search("[<>]", ln[tag.end():])
                             or any(">" in x for x in lines[i + 1:last])):
                title = _TAG_TITLE.search("\n".join(lines[i:last] + [lines[last][:pos]]))
                if title:
                    out.extend(["", title.group(1), ""])
                out.append(lines[last][pos + 1:])
                i = last + 1
                continue
        out.append(ln)
        i += 1
    return "\n".join(out)


def _tree(ctx, url: str) -> list:
    try:
        data = json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(data, dict) or not isinstance(data.get("tree"), list):
        raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
    if data.get("truncated"):
        raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
    return data["tree"]


@register("nextdocs-history")
def nextdocs_history(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or not tags:
        raise SystemExit(f"{source['id']}: читач nextdocs-history потребує поля tags — "
                         f"об'єкта «тег → версія».")
    folders = [f.strip("/") for f in source.get("folders") or ["docs"]]
    exts = tuple(source.get("extensions") or (".md", ".mdx"))
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    raw_base = f"https://raw.githubusercontent.com/{owner}/{repo}"

    # ім'я документа → [шлях, шлях джерела заглушки або "", [теги]]. Порядок ключів —
    # порядок першої появи, тобто від найновішого тегу; шлях теж із найновішого.
    seen: dict = {}
    records: dict = {}     # хеш піддерева теки → імена документів у ньому
    stubs: dict = {}       # хеш малого файла → куди вказує його `source` ("" — нікуди)

    def record(folder: str, sha: str, tag: str) -> tuple:
        files = []
        for entry in _tree(ctx, f"{source['url']}{sha}?recursive=1"):
            path = f"{folder}/{entry.get('path', '')}"
            leaf = path.rsplit("/", 1)[-1]
            if (entry.get("type") == "blob" and leaf.endswith(exts)
                    and not _LOCALE.search(leaf) and entry.get("size", 1) > 0
                    and not any(r.search(path) for r in exclude)):
                files.append((path, entry["sha"], entry.get("size", 0)))
        # Куди може вказувати `source`: шлях від теки без номерів і розширення.
        by_key = {_plain(re.sub(r"\.mdx?$", "", p))[len(folder) + 1:]: (p, s)
                  for p, s, _ in files}
        names = []
        for path, blob, size in files:
            stem = _plain(re.sub(r"\.mdx?$", "", path))
            target = ""
            if path.endswith(".mdx") and size <= _STUB_MAX:
                if blob not in stubs:
                    raw = f"{raw_base}/{quote(tag, safe='@')}/{quote(path)}"
                    meta = _markup.front_matter(ctx.text(raw))[0] if ctx.allowed(raw) else {}
                    stubs[blob] = meta.get("source", "").strip().strip("/")
                target = stubs[blob]
            origin = by_key.get(target) or by_key.get(f"{target}/index") if target else None
            if origin and origin[0] != path:
                pair = hashlib.sha1(f"{blob}{origin[1]}".encode()).hexdigest()[:8]
                name = f"{_markup.slug(stem)}-{pair}"
                seen.setdefault(name, [path, origin[0], []])
            else:
                name = f"{_markup.slug(stem)}-{blob[:8]}"
                seen.setdefault(name, [path, "", []])
            names.append(name)
        return tuple(dict.fromkeys(names))

    for n, tag in enumerate(tags, 1):
        for entry in _tree(ctx, f"{source['url']}{quote(tag, safe='@')}"):
            folder = entry.get("path", "")
            if entry.get("type") != "tree" or folder not in folders:
                continue
            sha = entry["sha"]
            if sha not in records:
                records[sha] = record(folder, sha, tag)
            for name in records[sha]:
                seen[name][2].append(tag)
        if n % _PROGRESS == 0:
            print(f"  {source['id']}: пройдено {n} із {len(tags)} тегів, різних піддерев "
                  f"{len(records)}, документів {len(seen)}", flush=True)

    items = []
    for name, (path, origin, found) in seen.items():
        found = list(dict.fromkeys(found))
        if not found:
            continue
        tag = quote(found[0], safe="@")
        raw = f"{raw_base}/{tag}/{quote(path)}"
        raw_origin = f"{raw_base}/{tag}/{quote(origin)}" if origin else ""
        if not ctx.allowed(raw) or (raw_origin and not ctx.allowed(raw_origin)):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{tag}/{quote(path)}"
        # Кілька тегів з однією міткою (canary одного циклу) — одна версія.
        version = ", ".join(dict.fromkeys(tags[t] for t in found))
        folder = path.split("/", 1)[0]
        stem = _plain(re.sub(r"\.mdx?$", "", path))
        router = _router_of(folder, stem[len(folder) + 1:])

        def make(raw=raw, raw_origin=raw_origin, blob=blob, path=path, version=version,
                 router=router):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            meta, rest = _markup.front_matter(text)
            if raw_origin:
                origin_text = ctx.text(raw_origin)
                _markup.refuse_html(origin_text, raw_origin)
                origin_meta, origin_rest = _markup.front_matter(origin_text)
                # Назва й опис заглушки — свої: сторінка Pages Router описує себе сама.
                meta = {**origin_meta, **{k: v for k, v in meta.items() if v}}
                rest = f"{origin_rest}\n\n{rest}"
            if path.endswith(".mdx"):
                # Імпорти й експорти MDX — код сторінки, а не її текст.
                rest = _markup.mdx_statements_out(rest)
            rest = _multiline_tags(_blocks(_atx(rest), router))
            title = meta.get("title", "")
            if not title:
                title, rest = _split_title(rest)
            if not title:
                title = re.sub(r"\.mdx?$", "", path.rsplit("/", 1)[-1])
            title = unescape(title)
            lead = meta.get("description", "")
            if lead and lead not in _FOLDED:
                rest = f"{lead}\n\n{rest}"
            body = _markup.markdown_body(rest)
            # Як і в ghdocs-history: файл на закріпленому тезі — не сторінка помилки, тож
            # і куце тіло, і порожнє (рубрика меню з самою назвою) — теж історія.
            if body.strip():
                _markup.require(title, body, raw, min_chars=1)
            return _markup.document(_TITLE_PREFIX.get(router, "") + title, blob, ctx.stamp,
                                    body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у теках {', '.join(folders)} жодного "
                         f"дозволеного файла на жодному з {len(tags)} тегів.")
    return items
