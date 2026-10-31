"""Читач історії файлів оголошень TypeScript (.d.ts): розділ на кожне оголошення, і в просторах імен.

`ghcode-history-dts` — файли `.d.ts` з багатьох тегів (чи комітів) одного репозиторію разом. Поля
                       ті самі, що в `ghcode-history-ts`: `url` — префікс дерев через API
                       (…/repos/ВЛАСНИК/РЕПО/git/trees/), `tags` — об'єкт «тег або коміт → версія»
                       від найновішого, `include` — вирази шляхів, що беруться; необов'язкові
                       `exclude`, `name_prefix` і `max_file` — межа розміру файла в байтах
                       (типово 100 000).

Навіщо. Довідник API Deno (docs.deno.com/api/deno) генерується з файлів `lib.deno.*.d.ts`, і весь
простір `Deno` у них — один блок `declare namespace Deno { … }` на двісті тисяч символів, де кожна
функція, інтерфейс і клас стоять на відступі в два пробіли (`  export function readFile(…)`).
`ghcode-history-ts` ділить лише оголошення верхнього рівня й методи класу з тілом: у такому файлі
він дає кілька розділів на весь простір, фрагменти ріжуться за довжиною, і жоден не називає
функції, яку описує. Веб-API в тих самих файлах написано інакше: `declare var Response: {…}` і
`interface Response {…}` — `var` спільний читач теж не знає.

Розділи. Межа — оголошення на будь-якому відступі (функція, інтерфейс, клас, тип, перелік,
константа, змінна), з назвою, повною від кореня: `## function Deno.readFile`, `## interface
Deno.ServeOptions`, `## class Deno.errors.NotFound`. Простір імен (`declare namespace Deno`,
вкладений `export namespace errors`) розділу не дає, а лише додає своє ім'я до назв усередині;
`declare global` і `declare module "…"` імені не додають. Член інтерфейсу чи класу — метод або
властивість на відступі на крок глибшому за власника — стає підрозділом: `### Deno.Kv.atomic()`,
`### Deno.ServeOptions.port`. Сигнатури перевантаження в `.d.ts` усі без тіла, тож тут вони межі
й дають, а сусідні розділи з однаковою назвою зливаються в один — як `join_same` спільного
читача. JSDoc упритул над оголошенням іде в його розділ, куций підрозділ (менше 200 символів)
приклеюється до попереднього.

Фігурні дужки рахуються лише в коді: у коментарях JSDoc стоять приклади з `{`, і без цього
простір «закривався» б посеред файла.

Чому окремий модуль: `ghcode-history-ts` звірено в готових примірниках (alpine, partysocket,
typeorm), правка його поділу — ризик зсуву там.
"""

import json
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.ghcodehistoryts import _COMMENT, _MAX_FILE, _MIN_PART, _TREES

_DECL = re.compile(r"^( *)(?:export\s+)?(?:default\s+)?(?:declare\s+)?(?:abstract\s+)?"
                   r"(?:async\s+)?(function|interface|class|type|enum|const|let|var|namespace|module)"
                   r"\s+([A-Za-z_$][\w$.]*|\"[^\"]+\"|'[^']+')")
_GLOBAL = re.compile(r"^ *(?:export\s+)?declare\s+global\s*\{")
_MEMBER = re.compile(r"^( *)(?:(?:public|private|protected|static|readonly|abstract|override|get|set)"
                     r"\s+)*(\[[^\]]+\]|[A-Za-z_$][\w$]*|\"[^\"]+\")\??\s*(\(|<|:)")
_NOT_MEMBER = {"if", "for", "while", "switch", "catch", "return", "new"}


def _code(line: str, in_comment: bool) -> tuple[str, bool]:
    """Частина рядка поза коментарями і рядковими літералами; і чи блоковий коментар іде далі."""
    out, i = [], 0
    while i < len(line):
        if in_comment:
            end = line.find("*/", i)
            if end < 0:
                return "".join(out), True
            in_comment, i = False, end + 2
        elif line.startswith("/*", i):
            in_comment, i = True, i + 2
        elif line.startswith("//", i):
            break
        elif line[i] in "\"'`":
            q, i = line[i], i + 1
            while i < len(line) and line[i] != q:
                i += 2 if line[i] == "\\" else 1
            i += 1
        else:
            out.append(line[i])
            i += 1
    return "".join(out), in_comment


def _outline(text: str) -> str:
    """Тіло з розділами: заголовок markdown на кожне оголошення, під ним — блок коду."""
    parts: list = [["", []]]
    # Відкриті блоки: (глибина дужок до відкриття, вид, повне ім'я, відступ рядка оголошення).
    stack: list = []
    depth = 0
    in_comment = False
    for line in text.rstrip().split("\n"):
        was_comment = in_comment
        code, in_comment = _code(line, in_comment)
        heading = ""
        kind = name = ""
        if not was_comment and code.strip():
            owner = stack[-1] if stack and depth == stack[-1][0] + 1 else None
            if _GLOBAL.match(code):
                kind, name = "global", ""
            elif m := _DECL.match(code):
                kind, own = m[2], m[3].strip("\"'")
                prefix = next((s[2] for s in reversed(stack) if s[1] == "namespace" and s[2]), "")
                if kind == "module" and m[3][0] in "\"'":
                    kind, name = "global", ""
                else:
                    kind = "namespace" if kind == "module" else kind
                    name = f"{prefix}.{own}" if prefix else own
                    if kind != "namespace":
                        heading = f"## {kind} {name}"
            elif owner and owner[1] in ("interface", "class") and (m := _MEMBER.match(code)) \
                    and m[2] not in _NOT_MEMBER and len(m[1]) > owner[3]:
                call = "()" if m[3] in "(<" else ""
                heading = f"### {owner[2]}.{m[2].strip(chr(34))}{call}"
        opened = code.count("{") - code.count("}")
        if kind and opened > 0:
            indent = len(line) - len(line.lstrip(" "))
            stack.append((depth, kind, name, indent))
        depth += opened
        while stack and depth <= stack[-1][0]:
            stack.pop()
        if heading:
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
        if merged and heading and heading == merged[-1][0]:
            merged[-1][1] += "\n\n" + code
            continue
        if merged and heading and len(code) < _MIN_PART and not heading.startswith("## "):
            merged[-1][1] += "\n\n" + code
            continue
        merged.append([heading, code])
    out = [f"{h}\n\n```ts\n{c}\n```" if h else f"```ts\n{c}\n```" for h, c in merged]
    return "\n\n".join(out)


@register("ghcode-history-dts")
def ghcode_history_dts(source: dict, ctx) -> list[Item]:
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
            if (entry.get("type") == "blob" and path.endswith(".d.ts")
                    and 0 < entry.get("size", 1) <= limit
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
            body = _outline(text)
            title = f"{repo}: {path}"
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла за `include` на жодному з "
                         f"{len(tags)} тегів.")
    return items
