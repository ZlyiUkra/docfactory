"""Сторінка сайту на VitePress із репозиторію → markdown, яким її бачить читач сайту.

Сторінка wagmi.sh у репозиторії — лише каркас, а текст збирається з кількох файлів:
- `<!--@include: @shared/query-options.md-->` — спільний шматок (опції TanStack Query, перелік
  повернених полів), однаковий для десятків хуків; `@` — корінь сайту, без нього шлях — від
  теки сторінки;
- `<<< @/snippets/react/config.ts[config.ts]` — файл коду прикладу, вставлений блоком коду;
- `{{TData}}`, `{{packageName}}`, `{{viemVersion}}` — змінні з `<script setup>` сторінки:
  рядки (`const TData = '{ … }'`) і поля `package.json` пакета
  (`const viemVersion = packageJson.peerDependencies.viem`).

Без цього сторінка «useBalance» не мала б ні опцій запиту, ні полів результату, ні коду
конфігу, а тип даних стояв би словом `{{TData}}`. Ще VitePress пише контейнери `::: tip` …
`:::`, групи вкладок `::: code-group` з підписами блоків (`ts [config.ts]`), а мову блоку
з підстановкою змінних — з суфіксом `-vue` (`bash-vue`); тут вони стають підписами й звичайними
блоками коду.

`files` — {шлях: sha} файлів тегу, які сторінка може вставити (див. `wanted`), `fetch(шлях,
sha)` — вміст файла. Вставка, файла якої на тезі немає, просто зникає; невідома змінна
лишається як є: вигадувати значення читач не стане.
"""

import hashlib
import json
import posixpath
import re

_INCLUDE = re.compile(r"<!--\s*@include:\s*([^\s>{#]+)(#[\w-]+)?(\{\d*,?\d*\})?\s*-->")
_SNIPPET = re.compile(r"^[ \t]*<<<[ \t]+(\S+?)(#[\w-]+)?(\{[^}]*\})?(?:[ \t]*\[([^\]]*)\])?[ \t]*$",
                      re.M)
_BLOCK_OPEN = re.compile(r"^<(script|style)\b[^>]*>[ \t]*$")
_CONST = re.compile(r"^[ \t]*const\s+([A-Za-z_$][\w$]*)\s*=\s*", re.M)
_IMPORT_JSON = re.compile(r"^\s*import\s+(\w+)\s+from\s+['\"]([^'\"]+\.json)['\"]", re.M)
_MUSTACHE = re.compile(r"\{\{\s*(.+?)\s*\}\}")
_NAME = re.compile(r"\s*([A-Za-z_$][\w$]*)")
_STEP = re.compile(r"\s*(?:(?:\?\.|\.)\s*([A-Za-z_$][\w$]*)"
                   r"|(?:\?\.)?\s*\[\s*(?:(\d+)|'([^']*)'|\"([^\"]*)\")\s*\])")
_STRING = re.compile(r"\s*(['\"`])((?:\\.|(?!\1).)*)\1", re.S)
_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})[ \t]*([\w+#.-]*)[ \t]*(.*?)[ \t]*$")
_CONTAINER = re.compile(r"^[ \t]*:::+[ \t]*([\w-]+)[ \t]*(.*?)[ \t]*$")
_CONTAINER_END = re.compile(r"^[ \t]*:::+[ \t]*$")
_SHIKI = re.compile(r"[ \t]*(?://|#|<!--)?[ \t]*\[!code [^\]]*\](?:[ \t]*-->)?")
_TOC = re.compile(r"^[ \t]*\[\[toc\]\][ \t]*$\n?", re.M)
_LABELS = {"tip": "Tip", "info": "Info", "warning": "Warning", "danger": "Danger",
           "caution": "Caution", "note": "Note", "details": "Details", "important": "Important"}


def wanted(root: str) -> list:
    """Файли тегу, які сторінки можуть узяти: спільні шматки й код прикладів кореня сайту і
    `package.json` пакетів і кореня репозиторію (з них — версії залежностей у командах
    встановлення, версія Node і менеджер пакетів у правилах для розробників)."""
    r = re.escape(root.strip("/"))
    return [re.compile(rf"^{r}/(?!\.vitepress/|public/).+\.(md|ts|tsx|js|jsx|mjs|vue|json|sol|sh)$"),
            re.compile(r"^(?:packages/[^/]+/)?package\.json$")]


def _resolve(target: str, page: str, root: str) -> str:
    if target.startswith("@"):
        return posixpath.normpath(f"{root.strip('/')}/{target[1:].lstrip('/')}")
    return posixpath.normpath(posixpath.join(posixpath.dirname(page), target))


def _deps(text: str, path: str, root: str, files: dict, read, depth: int = 0) -> list[str]:
    """Шляхи файлів, які сторінка тягне вставками, разом із вкладеними."""
    out = []
    for m in _INCLUDE.finditer(text):
        where = _resolve(m.group(1), path, root)
        if where in files and where not in out:
            out.append(where)
            if depth < 4:
                out += [p for p in _deps(read(where), where, root, files, read, depth + 1)
                        if p not in out]
    for m in _SNIPPET.finditer(text):
        where = _resolve(m.group(1), path, root)
        if where in files and where not in out:
            out.append(where)
    return out


def revision(path: str, sha: str, files: dict, fetch, root: str) -> str:
    """Відбиток редакції сторінки разом із тим, що вона вставляє. Документ корпусу —
    неповторний вміст файла, а сторінка хука часто не міняється між версіями, тоді як спільний
    `query-options.md` міняється: без цього сторінка 2.5 показувала б опції 2.19. З `package.json`
    сторінка бере одне-два поля (версію viem), а сам файл міняється з кожним випуском, тож у
    відбиток іде не він, а підставлені значення."""
    def read(where):
        return fetch(where, files[where])

    text = read(path)
    deps = _deps(text, path, root, files, read)
    near = sorted(f"{p}:{files[p]}" for p in deps)
    texts = [text] + [read(p) for p in deps if p.endswith(".md")]
    env = _environment(texts, path, root, files, fetch)
    used = {e.strip() for t in texts for e in _MUSTACHE.findall(t)}
    for expr in sorted(used):
        value = _scalar(_eval(expr, env))
        if value is not None:
            near.append(f"{expr}={value}")
    if not near:
        return sha
    return hashlib.sha1("\n".join([sha] + near).encode()).hexdigest()


def _eval(expr: str, env: dict):
    """Значення виразу `name`, `a.b`, `a?.['k']`, `a?.[1]` — або None, якщо його не обчислити."""
    m = _NAME.match(expr)
    if not m or m.group(1) not in env:
        return None
    node, pos, end = env[m.group(1)], m.end(), len(expr.rstrip())
    while pos < end:
        s = _STEP.match(expr, pos)
        if not s or s.end() == pos:
            return None
        key = (s.group(1) if s.group(1) is not None else int(s.group(2)) if s.group(2) is not None
               else s.group(3) if s.group(3) is not None else s.group(4))
        if isinstance(node, dict) and isinstance(key, str):
            node = node.get(key)
        elif isinstance(node, list) and isinstance(key, int) and key < len(node):
            node = node[key]
        else:
            return None
        pos = s.end()
    return node


def _scalar(value) -> str | None:
    if isinstance(value, bool) or value is None:
        return None
    return str(value) if isinstance(value, (str, int, float)) else None


def _value_at(code: str, pos: int, env: dict):
    """(значення, кінець) виразу, що починається в `code[pos]`: рядок, масив або шлях."""
    m = _STRING.match(code, pos)
    if m:
        if "${" in m.group(2):
            return None, m.end()
        return m.group(2).replace("\\'", "'").replace('\\"', '"'), m.end()
    i = pos
    while i < len(code) and code[i] in " \t\n":
        i += 1
    if i < len(code) and code[i] == "[":
        items, i = [], i + 1
        while i < len(code):
            while i < len(code) and code[i] in " \t\n,":
                i += 1
            if i < len(code) and code[i] == "]":
                return items, i + 1
            value, j = _value_at(code, i, env)
            if j <= i:
                return None, i
            items.append(value)
            i = j
        return None, i
    m = _NAME.match(code, pos)
    if not m:
        return None, pos
    end = m.end()
    while (s := _STEP.match(code, end)) and s.end() > end:
        end = s.end()
    return _eval(code[pos:end], env), end


def _variables(script: str, path: str, root: str, files: dict, fetch, env: dict) -> dict:
    """Змінні `<script setup>`: імпортований JSON і константи — рядки, масиви, шляхи в JSON чи в
    інших константах (`packageJson.peerDependencies.viem`, `[packageJson.peerDependencies['…']]`)."""
    env = dict(env)
    for name, rel in _IMPORT_JSON.findall(script):
        where = _resolve(rel, path, root)
        if where in files:
            try:
                env[name] = json.loads(fetch(where, files[where]) or "null")
            except ValueError:
                pass
    for m in _CONST.finditer(script):
        value, _ = _value_at(script, m.end(), env)
        if value is not None:
            env[m.group(1)] = value
    return env


def _environment(texts: list, path: str, root: str, files: dict, fetch) -> dict:
    """Змінні сторінки поверх змінних її вставок: спільний шматок задає свої значення за
    замовчуванням (`const TData = 'TData'`), а сторінка, що його вставляє, — справжні."""
    env: dict = {}
    for text in texts[1:]:
        env = _variables(_blocks_out(text)[1], path, root, files, fetch, env)
    return _variables(_blocks_out(texts[0])[1], path, root, files, fetch, env)


def _lines(text: str, spec: str | None) -> str:
    """Рядки `{3,10}` вставки: з якого по який, обидва включно, з одиниці."""
    if not spec:
        return text
    a, _, b = spec.strip("{}").partition(",")
    rows = text.split("\n")
    start = int(a) - 1 if a else 0
    end = int(b) if b else len(rows)
    return "\n".join(rows[start:end])


def _region(text: str, name: str | None) -> str:
    """Частина файла між `#region назва` і `#endregion` (у будь-якому коментарі)."""
    if not name:
        return text
    rows, out, inside = text.split("\n"), [], False
    for row in rows:
        if re.search(rf"#region\s+{re.escape(name)}\b", row):
            inside = True
        elif inside and re.search(r"#endregion\b", row):
            break
        elif inside:
            out.append(row)
    return "\n".join(out) if out else text


def _front_out(text: str) -> str:
    m = re.match(r"\A---[ \t]*\n.*?\n---[ \t]*(?:\n|\Z)", text, re.S)
    return text[m.end():] if m else text


def _includes(text: str, path: str, root: str, files: dict, fetch, depth: int = 0) -> str:
    def put(m):
        where = _resolve(m.group(1), path, root)
        if where not in files or depth >= 4:
            return ""
        piece = _front_out(fetch(where, files[where]))
        piece = _lines(_region(piece, (m.group(2) or "")[1:] or None), m.group(3))
        return _includes(piece, where, root, files, fetch, depth + 1)

    return _INCLUDE.sub(put, text)


def _blocks_out(text: str) -> tuple[str, str]:
    """(текст без блоків `<script>`/`<style>` верхнього рівня, код скриптів). Блок усередині
    огорожі коду — частина прикладу (`<script type="module">` у розділі про CDN), він лишається."""
    out, code, fence, block = [], [], "", ""
    for line in text.split("\n"):
        if block:
            if line.strip() == f"</{block}>":
                block = ""
            elif block == "script":
                code.append(line)
            continue
        m = _FENCE.match(line)
        if fence:
            if line.strip() and set(line.strip()) == {fence[0]} and len(line.strip()) >= len(fence):
                fence = ""
        elif m:
            fence = m.group(2)
        elif (b := _BLOCK_OPEN.match(line)):
            block = b.group(1)
            continue
        out.append(line)
    return "\n".join(out), "\n".join(code)


def _snippets(text: str, path: str, root: str, files: dict, fetch) -> str:
    seen = set()

    def put(m):
        where = _resolve(m.group(1), path, root)
        # Той самий файл (`config.ts`) сайт ставить вкладкою біля кожного прикладу сторінки;
        # у тексті він потрібен один раз, а повтори лише топили б розділи в однаковому коді.
        if where not in files or (where, m.group(2)) in seen:
            return ""
        seen.add((where, m.group(2)))
        code = _region(fetch(where, files[where]), (m.group(2) or "")[1:] or None).strip("\n")
        lang = where.rsplit(".", 1)[-1]
        for token in (m.group(3) or "").strip("{}").split():
            token = token.split(":", 1)[0]
            if token and not re.fullmatch(r"[\d,\-]+", token):
                lang = token
        label = f" [{m.group(4)}]" if m.group(4) else ""
        return f"```{lang}{label}\n{code}\n```"

    return _SNIPPET.sub(put, text)


def _markup(text: str, values: dict) -> str:
    """Змінні, контейнери, підписи блоків коду й позначки підсвічування → звичайний markdown.
    Змінні VitePress підставляє в тексті й у блоках із мовою `…-vue`, а в решті блоків коду
    `{{…}}` — буквальний текст прикладу, тож і тут лишається."""
    def sub(line):
        return _MUSTACHE.sub(lambda m: _value(m, values), line)

    out, fence, vue, stack = [], "", False, []
    for line in text.split("\n"):
        if fence:
            if line.strip() and set(line.strip()) == {fence[0]} and len(line.strip()) >= len(fence):
                fence = ""
                out.append(line)
                continue
            line = _SHIKI.sub("", line)
            out.append(sub(line) if vue else line)
            continue
        m = _FENCE.match(line)
        if m:
            pad, fence, lang, info = m.groups()
            vue = lang.endswith("-vue")
            lang = lang[:-4] if vue else lang
            label = re.search(r"\[([^\]]+)\]", info.replace("\\[", "["))
            if label:
                out += ["", f"{pad}{label.group(1)}:"]
            out.append(f"{pad}{fence}{lang}")
            continue
        m = _CONTAINER.match(line)
        if m:
            kind = m.group(1).lower()
            stack.append(kind)
            if kind != "code-group":
                head = _LABELS.get(kind, kind.capitalize())
                title = sub(m.group(2))
                out += ["", f"{head}: {title}" if title else f"{head}:", ""]
            continue
        if _CONTAINER_END.match(line) and stack:
            stack.pop()
            out.append("")
            continue
        out.append(sub(line))
    return "\n".join(out)


def _value(m, values: dict) -> str:
    value = _scalar(_eval(m.group(1), values))
    return m.group(0) if value is None else value


def expand(text: str, path: str, files: dict, fetch, root: str) -> str:
    """Тіло сторінки (без шапки YAML) з розкритими вставками, кодом і змінними."""
    page, script = _blocks_out(text)
    # Спільний шматок буває зі своїм `<script setup>`: його змінні — значення за замовчуванням,
    # сторінка, що його вставляє, їх перекриває.
    text, pieces = _blocks_out(_includes(page, path, root, files, fetch))
    values = _variables(script, path, root, files, fetch,
                        _variables(pieces, path, root, files, fetch, {}))
    text = _snippets(text, path, root, files, fetch)
    return _markup(_TOC.sub("", text), values)
