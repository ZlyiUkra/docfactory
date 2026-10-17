"""Читач історії коду TypeScript: як `ghcode-history`, але розділи — за будовою коду TypeScript.

`ghcode-history-ts` — файли коду з багатьох тегів (чи комітів) одного репозиторію разом. Поля ті
                      самі, що в `ghcode-history`: `url` — префікс дерев через API
                      (…/repos/ВЛАСНИК/РЕПО/git/trees/), `tags` — об'єкт «тег або коміт → версія»
                      від найновішого, `include` — вирази шляхів, що беруться; необов'язкові
                      `exclude`, `name_prefix` і `max_file` — межа розміру файла в байтах
                      замість спільної (100 000). Поля `outline` немає: файли .ts, .tsx, .js
                      і .jsx ділиться на розділи завжди.

Навіщо окремий читач. `ghcode-history` ділить код за відступом у чотири пробіли й без
модифікаторів — так написано Alpine.js. Код partysocket відформатовано Prettier (згодом
Oxfmt): два пробіли, методи класу з `public`/`private`/`protected`, аксесори `get`/`set`,
типи й інтерфейси верхнього рівня, тести, вкладені в `describe` на два пробіли. Тамтешній
поділ лишив би клас ReconnectingWebSocket одним розділом на двадцять тисяч символів, і
вектор бачив би лише його початок. Поле в спільному читачі змінило б уже звірений примірник
alpine — новий домен додає свого читача.

Розділи. Межа — оголошення верхнього рівня (клас, функція, інтерфейс, тип, константа;
однорядкове оголошення, що закінчується «;», межею не стає), метод чи аксесор класу на
відступі в два пробіли (сигнатура перевантаження без тіла — ні) і виклик `describe`/`it`/
`test` з назвою-рядком (і `testDone` — обгортка тестів reconnecting-websocket, з якого
partysocket відгалузився). Коментар JSDoc, що стоїть упритул над оголошенням, переходить у
розділ цього оголошення: саме в ньому опис опції чи методу. Куций розділ (дрібний аксесор
`get OPEN()`) приклеюється до попереднього, щоб не плодити фрагментів на три рядки.

Далі все як у `ghcode-history`: документ — неповторна пара «шлях, вміст» (хеш blob із
дерева), у версії лягають усі теги, де файл лежав саме таким; адреса в шапці — blob на
найновішому з них.
"""

import json
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.ghcode import _lang

# Поріг `ghcode` (40 000) відсіює згенероване в навчальних репозиторіях; тут файли написано
# руками, а розділи ділять їх на фрагменти — тести React-хуків partysocket мають 52 тисячі.
_MAX_FILE = 100_000

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")

# Виклик тесту: `describe("…"`, `test.each(…)("…"`, `describe.skipIf(умова)("…"`; назва може стояти
# й на наступному рядку, коли Prettier переносить довгий виклик (`test(` і далі `"назва",`).
_CALL = r"""^( *)(?:describe|it|test|testDone)(?:\.\w+(?:\([^()\n]*\))?)*\(\s*"""
_TEST = re.compile(_CALL + r"""(['"`])(.+?)\2""")
_TEST_OPEN = re.compile(_CALL + "$")
_NAME_NEXT = re.compile(r"""^\s*(['"`])(.+?)\1""")
_DECL = re.compile(r"^(?:export\s+)?(?:default\s+)?(?:declare\s+)?(?:abstract\s+)?(?:async\s+)?"
                   r"(class|function|interface|type|enum|const|let)\s+([A-Za-z_$][\w$]*)")
_MEMBER = re.compile(r"^  ((?:(?:public|private|protected|static|readonly|override|async|get|set)"
                     r"\s+)*)(constructor|[A-Za-z_$][\w$]*)\s*(?:<[^>]*>)?\(")
_NOT_METHOD = {"if", "for", "while", "switch", "catch", "function", "return", "super"}
_COMMENT = re.compile(r"^\s*(?:/\*|\*|//|@[A-Za-z])")
# Розділ коротший за це приклеюється до попереднього (той самий поріг, що й у фрагментів).
_MIN_PART = 200


def _lang_ts(path: str) -> str:
    return {".tsx": "tsx", ".jsx": "jsx"}.get(path[path.rfind("."):], "") or _lang(path)


def _template_after(line: str, inside: bool) -> bool:
    """Чи лишається шаблонний рядок (`…`) відкритим після цього рядка коду.

    Текст у шаблонному рядку може стояти з першої колонки — підказка ReconnectingWebSocket про
    відсутній WebSocket має всередині приклад `const partysocket = new PartySocket(...)`, — і
    без цього він ставав би межею розділу, а решта класу лишалася б неподіленою. Коментарі не
    рахуються: зворотні лапки в них — розмітка, а не код."""
    if not inside and _COMMENT.match(line):
        return inside
    count = len(re.findall(r"(?<!\\)`", line))
    return inside != (count % 2 == 1)


def _outline(text: str, lang: str) -> str:
    """Тіло з розділами: заголовок markdown на кожній межі, під ним — блок коду до наступної."""
    parts: list = [["", []]]
    owner = ""
    in_template = False
    lines = text.rstrip().split("\n")
    for i, line in enumerate(lines):
        heading = ""
        inside, in_template = in_template, _template_after(line, in_template)
        if inside:
            pass
        elif m := _TEST.match(line):
            heading = f"{'#' * min(2 + len(m[1]) // 2, 6)} {m[3]}"
        elif (m := _TEST_OPEN.match(line)) and i + 1 < len(lines) \
                and (n := _NAME_NEXT.match(lines[i + 1])):
            heading = f"{'#' * min(2 + len(m[1]) // 2, 6)} {n[2]}"
        elif m := _DECL.match(line):
            single = m[1] in ("type", "const", "let") and line.rstrip().endswith(";")
            owner = m[2] if m[1] == "class" else ""
            if not single:
                heading = f"## {m[1]} {m[2]}"
        elif line.startswith("}"):
            owner = ""
        elif owner and (m := _MEMBER.match(line)) and m[2] not in _NOT_METHOD \
                and not line.rstrip().endswith(";"):
            mods = m[1].split()
            accessor = next((w for w in mods if w in ("get", "set")), "")
            static = "static " if "static" in mods else ""
            heading = (f"### {static}{accessor} {owner}.{m[2]}" if accessor
                       else f"### {static}{owner}.{m[2]}()")
        if heading:
            # JSDoc і коментарі впритул над оголошенням — частина нового розділу.
            prev = parts[-1][1]
            lead = []
            while prev and prev[-1].strip() and _COMMENT.match(prev[-1]):
                lead.insert(0, prev.pop())
            parts.append([heading, lead])
        parts[-1][1].append(line)

    merged: list = []
    for heading, lines in parts:
        code = "\n".join(lines).strip("\n")
        if not code.strip():
            continue
        if merged and heading and len(code) < _MIN_PART and not heading.startswith("## "):
            merged[-1][1] += "\n\n" + code
            continue
        merged.append([heading, code])
    out = [f"{h}\n\n```{lang}\n{c}\n```" if h else f"```{lang}\n{c}\n```" for h, c in merged]
    return "\n\n".join(out)


@register("ghcode-history-ts")
def ghcode_history_ts(source: dict, ctx) -> list[Item]:
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
    limit = int(source.get("max_file") or _MAX_FILE)

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
            if (entry.get("type") == "blob" and 0 < entry.get("size", 1) <= limit
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
            lang = _lang_ts(path)
            body = (_outline(text, lang) if lang in ("js", "ts", "tsx", "jsx")
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
