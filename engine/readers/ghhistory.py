"""Читач історії документації репозиторію: один документ на кожен неповторний текст файла.

`ghdocs-history` — markdown-документація з багатьох тегів одного репозиторію разом.
                   `url` — префікс дерев через API
                   (…/repos/ВЛАСНИК/РЕПО/git/trees/), поле `tags` — об'єкт «тег →
                   версія», від найновішого. `folders` — теки, .md-файли яких
                   беруться (з `recursive: true` — і з вкладених тек), `files` —
                   окремі файли поза ними (напр. кореневий FAQ.md).

Навіщо. `ghdocs` дає знімок на тег: кожен тег — повна копія теки документації. У
React Router 820 тегів, у кожному 100–200 файлів, разом 88 тисяч файлів, а різних
текстів серед них лише 2 855: між сусідніми тегами змінюється один-два файли або
жодного. Знімки на тег означали б 88 тисяч завантажень і корпус, у якому 97% —
дослівні повтори, які злиття однаково зводить в один фрагмент.

Тут одиниця — пара «шлях, вміст» (вміст упізнається хешем blob із дерева тегу). Така
пара стає одним документом, а в його версії лягають усі теги, де цей файл лежав
саме таким. Фільтр `version: "6.4"` знаходить рівно ті тексти, що знайшов би серед
знімків, бо текст той самий, — різниця лише в тому, що кожен тягнеться й лежить
один раз. Адреса в шапці — blob на першому з тегів переліку, де файл такий був,
тобто на найновішому.

Версія — рядок із `tags`, а не номер, вирізаний із тегу. Так збірки, чий номер
нічого не каже (`v0.0.0-experimental-004e483a8`), дістають мітку `experimental`
і не змішуються з лінією 0.x, у якої номер той самий.

Назва документа — поле `title` шапки YAML; без шапки — заголовок, що стоїть першим
рядком; інакше — ім'я файла. Саме так і в 0.x: сторінка «Route.md» починається
одразу текстом, а перший заголовок у ній — підрозділ «Props», не назва. Стара документація (до v4) пише заголовки
підкресленням («Назва» і рядок «===» під нею), і `_markup` їх не знає: тут вони
стають «#»/«##» до розбору, інакше документ не ділився б на розділи.

Чому окремий модуль, а не поле в `ghdocs`: примірники, зібрані знімками на тег,
звірені, а правка спільного читача — ризик зсуву в готовій роботі.
"""

import json
import re
from html import unescape
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_LOCALE = re.compile(r"\.[a-z]{2}-[A-Z]{2}\.md$")
_FENCE = re.compile(r"^\s*(```|~~~)")
_ATX = re.compile(r"^(#{1,6})[ \t]+(\S.*?)[ \t]*#*[ \t]*$")
_SETEXT = re.compile(r"^(=+|-+)[ \t]*$")
# Рядок, що підкресленням заголовка бути не може: пункт списку, цитата, таблиця,
# інший заголовок. Інакше «---» під пунктом списку став би заголовком із пункту.
_NOT_TITLE = re.compile(r"^\s*([-*+>|#]|\d+[.)]\s|```|~~~)")


def _atx(text: str) -> str:
    """Заголовки-підкреслення → «#»/«##». Код і вже звичайні заголовки не
    чіпаються."""
    lines = text.split("\n")
    out: list[str] = []
    fence = False
    for ln in lines:
        if _FENCE.match(ln):
            fence = not fence
        elif (not fence and _SETEXT.match(ln) and out and out[-1].strip()
              and not _NOT_TITLE.match(out[-1])
              and (len(out) < 2 or not out[-2].strip())):
            out[-1] = ("# " if ln.lstrip()[0] == "=" else "## ") + out[-1].strip()
            continue
        out.append(ln)
    return "\n".join(out)


def _split_title(text: str) -> tuple[str, str]:
    """(назва з заголовка першого непорожнього рядка, текст без нього). Заголовок
    далі в тексті — підрозділ, а не назва."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        m = _ATX.match(line)
        if m:
            return m.group(2), "\n".join(lines[:i] + lines[i + 1:])
        break
    return "", text


@register("ghdocs-history")
def ghdocs_history(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or not tags:
        raise SystemExit(f"{source['id']}: читач ghdocs-history потребує поля tags — "
                         f"об'єкта «тег → версія».")
    folders = [f.strip("/") for f in source.get("folders") or ["docs"]]
    files = {f.strip("/") for f in source.get("files") or ()}
    recursive = source.get("recursive") is True

    # ім'я документа → [шлях, [теги]]; порядок ключів — порядок першої появи, тобто
    # від найновішого тегу, бо `tags` оголошено від найновішого. Ключ — ім'я, а не
    # шлях: у 2.x той самий файл лежав то як «Testing.md», то як «testing.md», і
    # дві такі пари з одним вмістом дали б одне ім'я файла — друга затерла б першій
    # перелік версій. Тут вони — один документ з версіями обох.
    seen: dict = {}
    for tag in tags:
        url = f"{source['url']}{tag}?recursive=1"
        try:
            tree = json.loads(ctx.text(url))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
        if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
            raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
        if tree.get("truncated"):
            raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
        for entry in tree["tree"]:
            path = entry.get("path", "")
            folder, _, leaf = path.rpartition("/")
            inside = path in files or (
                folder in folders if not recursive else
                any(folder == f or folder.startswith(f + "/") for f in folders))
            # Порожній файл — не документ і не історія: з нього нема чого читати.
            if (entry.get("type") == "blob" and inside and leaf.endswith(".md")
                    and not _LOCALE.search(leaf) and entry.get("size", 1) > 0):
                name = f"{_markup.slug(path.removesuffix('.md'))}-{entry['sha'][:8]}"
                seen.setdefault(name, [path, []])[1].append(tag)

    order = {t: i for i, t in enumerate(tags)}
    items = []
    for name, (path, found) in seen.items():
        found = sorted(set(found), key=order.get)
        tag = found[0]
        # У шляхах 0.x бувають пробіли («doc/04 Locations/…»): без екранування
        # такої адреси urllib не відправить зовсім.
        where = f"{owner}/{repo}/{quote(tag, safe='@')}/{quote(path)}"
        raw = f"https://raw.githubusercontent.com/{where}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{where.split('/', 2)[2]}"
        # Кілька тегів з однією міткою (усі experimental-збірки) — одна версія.
        version = ", ".join(dict.fromkeys(tags[t] for t in found))

        def make(raw=raw, blob=blob, path=path, version=version):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            meta, rest = _markup.front_matter(text)
            rest = _atx(rest)
            title = meta.get("title", "") if meta else ""
            if not title:
                title, rest = _split_title(rest)
            if not title:
                title = path.rsplit("/", 1)[-1].removesuffix(".md")
            # У 4.x–5.x назва пишеться «# &lt;Route>»: на сайті це «<Route>».
            title = unescape(title)
            body = _markup.markdown_body(rest)
            # Файл на закріпленому тезі — не сторінка помилки (від HTML захищає
            # refuse_html), тож і коротке тіло («сторінку перенесено»), і порожнє —
            # теж історія. Порожнє буває двох видів: рубрика меню сайту з самою
            # шапкою («title: Guides») і заготовка старих версій з самим заголовком
            # («# IndexLink»). Фрагментів такий документ не дасть, бо порожнього
            # тексту корпус не ділить, але те, що сторінка була, лишається.
            if body.strip():
                _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у теках {', '.join(folders)} жодного "
                         f"дозволеного .md на жодному з {len(tags)} тегів.")
    return items
