"""Читачі markdown без шапки YAML: назву несе перший заголовок документа.

`llms-heading`   — те саме, що `llms`: перелік сторінок у форматі llms.txt, текст
                   кожної — її markdown-двійник із суфіксом «.md».
`ghdocs-heading` — те саме, що `ghdocs`: markdown-документація, що лежала в
                   репозиторії на момент тегу чи коміту.

Різниця з `mdsite.llms` і `github.ghdocs` рівно одна — звідки береться назва.
Ті два читачі беруть її з шапки YAML, і для сайтів на Jekyll це правильно. Але
шапку має не кожен генератор: docs.nestjs.com віддає сторінку, що починається
одразу заголовком «# Controllers», а репозиторій того самого сайту — заголовком
«### Controllers». Назва там є, просто лежить у першому заголовку, і чинні читачі
таку сторінку відхиляють як «без назви».

Чому окремий модуль, а не запасний шлях у тих двох. Примірники `ecmascript` і
`react` працюють, їхні корпуси зібрані й звірені, а будь-яка правка спільного
читача — це ризик зсуву в готовій роботі. Новий модуль реєструє нові імена й не
чіпає жодного наявного шляху виконання: хто не назвав ці імена в sources.json,
того ця копія не стосується взагалі.

Перший заголовок зі тіла знімається: назва документа й так стоїть у шапці, яку
пише `_markup.document`, і лишати її вдруге означало б дублювати її в кожному
фрагменті. Рівень заголовка при цьому не важливий — «#» на сайті й «###» у
репозиторії дають ту саму назву, а підрозділи в обох «####», тож той самий
розділ у різних версіях зберігає те саме ім'я й однаковий текст зливається.
"""

import json
import re
import sys
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register
from engine.readers.mdsite import _SITEMAP

_MD_LINK = re.compile(r"\((https://[^)\s]+\.md)\)")
# Модулі маршрутизації Angular, з яких будується таблиця «файл → адреса сайту».
_ROOT_ROUTING = "src/app/app-routing.module.ts"
_PAGES = "src/app/homepage/pages/"
_PAGE_MODULE = re.compile(r"^src/app/homepage/pages/([^/]+)/\1\.module\.ts$")
# import { XComponent } from './a/b/b.component';
_IMPORT = re.compile(r"import\s*\{\s*(\w+)Component\s*\}\s*from\s*'([^']+)'")
# { path: '...', component: XComponent }
_ROUTE = re.compile(r"path:\s*'([^']*)'\s*,\s*component:\s*(\w+)Component")
# { path: '...', ... import('./homepage/pages/x/x.module') }
_MOUNT = re.compile(r"path:\s*'([^']*)'[^}]*?import\('([^']+)'\)", re.S)
_HEADING = re.compile(r"^(#{1,6})[ \t]+(\S.*?)[ \t]*$")
_FENCE = re.compile(r"^(```|~~~)")
_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/([^/]+)$")
_LOCALE = re.compile(r"\.[a-z]{2}-[A-Z]{2}\.md$")
_POSITION = re.compile(r"(^|/)\d+(?:\.\d+)*-")


def _split_title(text: str) -> tuple[str, str]:
    """(назва з першого заголовка, текст без того рядка).

    Заголовок шукається лише до першої огорожі коду: рядок «# коментар» усередині
    прикладу назвою документа не є. Якщо заголовка немає, назва порожня — і
    `_markup.require` відмовить, як і належить сторінці, якої читач не впізнав.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    for i, line in enumerate(lines):
        if _FENCE.match(line):
            break
        m = _HEADING.match(line)
        if m:
            return m.group(2), "\n".join(lines[:i] + lines[i + 1:])
    return "", text


def _document(ctx, md_url: str, page: str, version: str) -> str:
    text = ctx.text(md_url)
    _markup.refuse_html(text, md_url)
    _, rest = _markup.front_matter(text)
    # Той самий хвіст «## Sitemap», що й у react.dev: у clerk.com він закінчує кожну
    # сторінку документації й давав 2487 фрагментів без змісту. Вираз точний, тож
    # сторінкам без такого хвоста (nestjs, supabase) нічого не змінюється.
    rest = _SITEMAP.sub("\n", rest)
    title, rest = _split_title(rest)
    body = _markup.markdown_body(rest)
    _markup.require(title, body, md_url, min_chars=1)
    return _markup.document(title, page, ctx.stamp, body, version)



def _component_paths(text: str) -> dict:
    """{ім'я компонента: шлях теки з його імпорту}. Шлях теки — це і є ім'я файлу
    в `content/`: сайт складається так, що кожній главі відповідає тека компонента.

    Береться саме шлях імпорту, а не кебаб від імені класу: `RabbitMQComponent`
    лежить у теці `rabbitmq`, а кебаб дав би `rabbit-m-q`. Такої сторінки немає, і
    зведення тихо не спрацювало б — рівно та хибна відповідь, проти якої все це.
    """
    out = {}
    for name, path in _IMPORT.findall(text):
        parts = path.split("/")
        if len(parts) < 2:
            continue
        folder = "/".join(parts[:-1]).lstrip("./")
        if folder.startswith(_PAGES.removeprefix("src/app/")):
            folder = folder[len("homepage/pages/"):]
        out[name] = folder
    return out


def _route_map(ctx, base: str, paths: list) -> dict:
    """Таблиця «шлях у content/ → адреса сайту», зібрана з модулів маршрутизації
    того самого коміту, на якому стоїть знімок.

    Навіщо вона. Файли в репозиторії сайту звуться по-старому — `unit-testing.md`,
    `sql.md`, `dependency-injection.md`, — а сторінка вже сім років живе за адресою
    `fundamentals/testing`, `techniques/database`, `fundamentals/custom-providers`.
    Без зведення той самий текст лежить у корпусі двома документами під різними
    іменами, і питання «з якої версії це так» дістає хибну відповідь.

    Таблиця будується, а не пишеться руками: коміт закріплений, отже при будь-якому
    повторному завантаженні вийде те саме. Перейменовувати нічого й ніколи не треба.

    Помилка тут гірша за відсутність зведення, тому кожна непевність — відмова:
    немає кореневого модуля, не розібралося жодного маршруту, два файли зводяться
    на одну адресу. Сторінка, якої в маршрутах немає, лишає ім'я файлу.
    """
    root = next((p for p in paths if p == _ROOT_ROUTING), None)
    if root is None:
        raise SystemExit(f"{base}: немає {_ROOT_ROUTING} — таблицю маршрутів не "
                         f"побудувати, а без неї імена документів розійдуться з адресами "
                         f"сайту. Зніміть `route_map` або поправте читач.")
    modules = [(None, root)] + [(m.group(1), p) for p in sorted(paths)
                                if (m := _PAGE_MODULE.match(p))]
    mounts, table = {}, {}
    text_root = ctx.text(base + root)
    for mount, mod in _MOUNT.findall(text_root):
        folder = mod.rstrip("/").split("/")[-2] if "/" in mod else mod
        mounts[folder] = mount
    for folder, path in modules:
        text = text_root if folder is None else ctx.text(base + path)
        comps = _component_paths(text)
        prefix = "" if folder is None else (mounts.get(folder, folder) + "/")
        for route, name in _ROUTE.findall(text):
            src = comps.get(name)
            if not src or not route:
                continue
            if folder is not None and not src.startswith(folder + "/"):
                src = f"{folder}/{src}"
            dest = route if "/" in route or folder is None else prefix + route
            table.setdefault(src, []).append(dest)
    # Одна сторінка буває під кількома адресами: у NestJS «enterprise» доступна ще й
    # як «consulting», і та друга — зовнішнє перенаправлення. Вгадувати, яка з них
    # головна, не можна, тому правило просте й без здогадів: єдина адреса — беремо
    # її; серед кількох є та, що дорівнює імені файлу, — лишаємо ім'я файлу; інакше
    # не зводимо взагалі й кажемо про це. Незведене ім'я нічого не псує, воно лише
    # не зіллється з тією самою сторінкою сусідньої версії. Вгадане — псує.
    ambiguous = []
    for src, dests in list(table.items()):
        uniq = list(dict.fromkeys(dests))
        if len(uniq) == 1:
            table[src] = uniq[0]
        elif src in uniq:
            table[src] = src
        else:
            ambiguous.append(f"{src} -> {', '.join(uniq)}")
            table[src] = src
    if ambiguous:
        print(f"  таблиця маршрутів: {len(ambiguous)} сторінок мають кілька адрес і "
              f"лишені під іменем файлу: {'; '.join(ambiguous)}", file=sys.stderr)
    if not table:
        raise SystemExit(f"{base}: у модулях маршрутизації не розібралося жодної пари "
                         f"«адреса — компонент». Схоже, Angular змінив спосіб опису "
                         f"маршрутів; поправте _ROUTE і _IMPORT у цьому читачі.")
    back = {}
    for src, dest in table.items():
        if dest in back:
            raise SystemExit(f"{base}: адреса {dest} належить і {back[dest]}, і {src} — "
                             f"два документи зіллися б в один, нічого не зводжу.")
        back[dest] = src
    return table


@register("llms-heading")
def llms_heading(source: dict, ctx) -> list[Item]:
    links: list[str] = []
    for url in _MD_LINK.findall(ctx.text(source["url"])):
        if url not in links and ctx.allowed(url):
            links.append(url)
    if not links:
        raise SystemExit(f"У переліку {source['url']} не знайдено жодної дозволеної "
                         f"сторінки .md — розмітка змінилася або `within` не той.")
    items = []
    for url in links:
        page = url[:-3]
        name = _markup.slug(urlsplit(page).path)

        def make(url=url, page=page):
            return _document(ctx, url, page, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("ghdocs-heading")
def ghdocs_heading(source: dict, ctx) -> list[Item]:
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
    folders = [f.strip("/") for f in source.get("folders") or ["docs"]]
    recursive = source.get("recursive") is True
    root = source.get("root", "").strip("/")
    all_paths = [e.get("path", "") for e in tree["tree"] if e.get("type") == "blob"]
    base = f"https://raw.githubusercontent.com/{owner}/{repo}/{tag}/"
    routes = _route_map(ctx, base, all_paths) if source.get("route_map") is True else {}
    renamed = 0
    paths = []
    for entry in tree["tree"]:
        path = entry.get("path", "")
        folder, _, leaf = path.rpartition("/")
        inside = (folder in folders if not recursive else
                  any(folder == f or folder.startswith(f + "/") for f in folders))
        if (entry.get("type") == "blob" and inside and leaf.endswith(".md")
                and not _LOCALE.search(leaf)):
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
        stem = re.sub(r"(^|/)index$", "", rel.removesuffix(".md")) or "index"
        if stem in routes:
            if routes[stem] != stem:
                renamed += 1
            stem = routes[stem]
        name = _markup.slug(_POSITION.sub(r"\1", stem))

        def make(raw=raw, blob=blob):
            return _document(ctx, raw, blob, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['url']}: у теках {', '.join(folders)} немає жодного "
                         f"дозволеного .md.")
    if routes:
        print(f"  {source['id']}: таблиця маршрутів на {len(routes)} сторінок, "
              f"зведено імен {renamed}", file=sys.stderr)
    return items
