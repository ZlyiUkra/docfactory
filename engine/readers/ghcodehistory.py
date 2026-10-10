"""Читач історії коду репозиторію: один документ на кожен неповторний вміст файла з багатьох тегів.

`ghcode-history` — файли коду (не markdown) з багатьох тегів одного репозиторію разом.
                   `url` — префікс дерев через API (…/repos/ВЛАСНИК/РЕПО/git/trees/), поле
                   `tags` — об'єкт «тег → версія», від найновішого; `include` — вирази шляхів,
                   що беруться. Необов'язкові: `exclude` — вирази шляхів, що не беруться,
                   `name_prefix` — рядок перед іменем документа; `outline: true` — файл
                   JavaScript ділиться на розділи (див. `_outline`).

Навіщо. `ghcode` бере дерево одного тегу, а `ghdocs-history` бере багато тегів, але читає
кожен файл як markdown. CSP-збірка Alpine.js описана на сайті однією сторінкою, і та
відстає від коду: що саме приймає розбирач виразів і з якої версії, видно лише з
`packages/csp/src` і тестів розбирача. Знімок на одному тезі не відповідає на «чи працює
це в 3.15.2», а знімок на кожному з сотні тегів — сотня дослівних повторів.

Тут, як і в `ghdocs-history`, одиниця — пара «шлях, вміст» (вміст упізнається хешем blob
із дерева тегу): така пара стає одним документом, а в його версії лягають усі теги, де
файл лежав саме таким. Фільтр `version: "3.15"` знаходить рівно ту редакцію коду, що
стояла в лінії. Адреса в шапці — blob на найновішому з цих тегів. Текст лягає блоком коду
з мовою за розширенням, як у `ghcode`; файли понад той самий поріг не беруться.

Навіщо `outline`. Цілий файл — один фрагмент: тести розбирача CSP — 32 тисячі символів, і
вектор бачить лише їхній початок, а `read_section` віддає все разом. Поділені на розділи
`describe`/`it`/`test`, тести стають переліком «що підтримується» з назвою кожного випадку,
а злиття однакових фрагментів між редакціями (`revision_suffix`) лишає кожному тестові
версії, у яких він був, — тобто з якої версії збірка це вміє. Код ділиться так само за
оголошеннями верхнього рівня й методами класів.
"""

import json
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.ghcode import _MAX_FILE, _lang

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")

# Межі розділів: виклик набору тестів чи тесту з назвою-рядком (рівень — за відступом),
# оголошення верхнього рівня і метод класу на відступі в чотири пробіли.
_TEST = re.compile(r"""^( *)(?:describe|it|test)(?:\.\w+)?\(\s*(['"`])(.+?)\2""")
_DECL = re.compile(r"^(?:export\s+(?:default\s+)?)?(?:async\s+)?(class|function)\s+([A-Za-z_$][\w$]*)")
_METHOD = re.compile(r"^    (?:static\s+|async\s+|get\s+|set\s+)*([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{\s*$")
_NOT_METHOD = {"if", "for", "while", "switch", "catch", "function", "return"}


def _outline(text: str, lang: str) -> str:
    """Тіло з розділами: заголовок markdown на кожній межі, під ним — блок коду до наступної."""
    parts: list = [["", []]]
    owner = ""
    for line in text.rstrip().split("\n"):
        heading = ""
        if m := _TEST.match(line):
            heading = f"{'#' * min(2 + len(m[1]) // 4, 6)} {m[3]}"
        elif m := _DECL.match(line):
            owner = m[2] if m[1] == "class" else ""
            heading = f"## {m[1]} {m[2]}"
        elif owner and (m := _METHOD.match(line)) and m[1] not in _NOT_METHOD:
            heading = f"### {owner}.{m[1]}()"
        if heading:
            parts.append([heading, []])
        parts[-1][1].append(line)
    out = []
    for heading, lines in parts:
        code = "\n".join(lines).strip("\n")
        if not code.strip():
            continue
        out.append(f"{heading}\n\n```{lang}\n{code}\n```" if heading else f"```{lang}\n{code}\n```")
    return "\n\n".join(out)


@register("ghcode-history")
def ghcode_history(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or not tags:
        raise SystemExit(f"{source['id']}: поле `tags` — об'єкт «тег → версія».")
    include = [re.compile(x) for x in source.get("include") or ()]
    if not include:
        raise SystemExit(f"{source['id']}: поле `include` — вирази шляхів, що беруться.")
    exclude = [re.compile(x) for x in source.get("exclude") or ()]
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    outline = source.get("outline") is True

    # ім'я документа → [шлях, [теги]]; порядок — від найновішого тегу, як оголошено в `tags`
    seen: dict = {}
    for tag in tags:
        url = f"{source['url']}{quote(tag, safe='@')}?recursive=1"
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
            if (entry.get("type") == "blob" and 0 < entry.get("size", 1) <= _MAX_FILE
                    and any(r.search(path) for r in include)
                    and not any(r.search(path) for r in exclude)):
                name = f"{lead}{_markup.slug(path)}-{entry['sha'][:8]}"
                seen.setdefault(name, [path, []])[1].append(tag)

    order = {t: i for i, t in enumerate(tags)}
    items = []
    for name, (path, found) in seen.items():
        found = sorted(set(found), key=order.get)
        where = f"{owner}/{repo}/{quote(found[0], safe='@')}/{quote(path)}"
        raw = f"https://raw.githubusercontent.com/{where}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{where.split('/', 2)[2]}"
        version = ", ".join(dict.fromkeys(tags[t] for t in found))

        def make(path=path, raw=raw, blob=blob, version=version):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            lang = _lang(path)
            body = (_outline(text, lang) if outline and lang in ("js", "ts")
                    else f"```{lang}\n{text.rstrip()}\n```")
            title = f"{repo}: {path}"
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла за `include` на жодному з "
                         f"{len(tags)} тегів.")
    return items
