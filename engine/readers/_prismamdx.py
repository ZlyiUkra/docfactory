"""Сторінка документації Prisma з репозиторію prisma/docs (тепер prisma/web) → markdown, яким її бачить
читач сайту.

Сайт тричі міняв рушій, і кожен приніс свої компоненти MDX:
- Gatsby (2020–2022, тека `content/`): `<TabbedContent tabs={[<FileWithIcon text="SQL" …/>, …]}>` з
  вкладками `<tab>`, чиї назви стоять лише в `tabs`; `<SwitchTech technologies={['node', 'postgresql']}>`
  — шматок сторінки для однієї мови й однієї бази (сайт перемикав їх згори сторінки);
  `<CodeWithResult>` з `<cmd>` і `<cmdResult>` — команда та її вивід; `<ParallelBlocks>` з
  `<block content="Prisma Client (v1)">` — два варіанти поруч; `<Admonition type="warning">`, `<Tip>`;
  `<NavigationLinksContainer>` — кнопки «назад / далі»;
- Docusaurus (2022–2026, та сама тека): `<TabbedContent code>` з `<TabItem value="MongoDB">`, спільні
  шматки `import PrismaInitPartial from './_prisma-init-partial.mdx'` і рядок
  `<PrismaInitPartial datasource="MySQL" />`;
- Fumadocs (з лютого 2026, `apps/docs/content/docs`): `<Tabs items>` з `<Tab value>`, картки
  `<Card title href>`, `<Accordion title>`, згенеровані сторінки REST API, де замість тексту стоїть
  `<APIPage operations={…} />`, а метод і шлях — у шапці.

Без цього приклади для PostgreSQL і MongoDB злипалися б в один код без підписів, кроки «Get started»
десятків сторінок були б порожніми, а вивід команди не відрізнявся б від самої команди.

Назва блоку коду (`file=prisma/schema.prisma` у Gatsby й Docusaurus, `title="prisma.config.ts"` у
Fumadocs) стає рядком перед кодом: відповідь «у якому файлі» без неї не мала б опори.

Спільний шматок буває з умовою на властивість (`{props.database && (<ul>…</ul>)}`): без властивості
сайт цей шматок не показує, і тут він теж випадає, а не лишається сирим JSX.

Документація Prisma 1 (репозиторій prisma/prisma1, теки `docs/1.0` … `docs/1.34`) з 1.15 пише назву
не в шапці YAML, а в `export const meta = {title: '…'}`, і має сторінку на кожну мову чи базу
(`…-TYPESCRIPT-a003.mdx`, `…-MYSQL-knul.mdx`) з однаковою назвою: назва стає заголовком сторінки з
мовою чи базою в дужках, а виноски `<Info>` і `<Warning>` — підписами.

`files` — {шлях: sha} файлів знімка, які сторінка може вставити (див. `WANTED`), `fetch(шлях, sha)` —
вміст файла.
"""

import re

from engine.readers import _astromdx

# Спільні шматки живуть поруч зі сторінками під іменем із «_»; сайт сторінками їх не показує.
WANTED = [re.compile(r"^content/(?:.+/)?_[^/]+\.mdx?$")]

_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
_OPEN = re.compile(r"^\s*<([A-Za-z][\w.]*)\b")
_CLOSE = re.compile(r"^\s*</([A-Za-z][\w.]*)\s*>")
_FILE = re.compile(r"""\b(?:file|title)\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s"']+))""")
_TECH = {"node": "Node.js", "typescript": "TypeScript", "postgresql": "PostgreSQL", "mysql": "MySQL",
         "sqlite": "SQLite", "sqlserver": "SQL Server", "mongodb": "MongoDB",
         "cockroachdb": "CockroachDB", "planetscale": "PlanetScale",
         "prismaPostgres": "Prisma Postgres", "prisma-postgres": "Prisma Postgres"}
_ADMONITION = {"info": "Info", "warning": "Warning", "alert": "Warning", "tip": "Tip",
               "success": "Success", "danger": "Danger", "note": "Note", "error": "Error"}
# Компоненти без власного тексту: розмітка, пошукові мітки, кнопки.
_DROP = {"APIPage", "AlgoliaTerm", "Subsections", "Youtube", "ConceptAnimation", "Cards",
         "Accordions", "ParallelBlocks", "CodeWithResult", "TopBlock", "FootNote", "Steps", "Step",
         "cmd"}
_JSX_COMMENT = re.compile(r"\{/\*.*?\*/\}", re.S)
_COND = re.compile(r"\{\s*props\.(\w+)\s*(?:(===|!==)\s*['\"]([^'\"]*)['\"]\s*)?&&")
_META = re.compile(r"^export\s+const\s+meta\s*=\s*\{", re.M)
_META_TITLE = re.compile(r"""\btitle\s*:\s*(?:'((?:[^'\\]|\\.)*)'|"((?:[^"\\]|\\.)*)")""")
_VARIANT = re.compile(r"-(JAVASCRIPT|TYPESCRIPT|FLOW|GO|MYSQL|POSTGRES|MONGO)-\w+\.mdx?$")
_VARIANTS = {"JAVASCRIPT": "JavaScript", "TYPESCRIPT": "TypeScript", "FLOW": "Flow", "GO": "Go",
             "MYSQL": "MySQL", "POSTGRES": "PostgreSQL", "MONGO": "MongoDB"}


def revision(path: str, sha: str, files: dict, fetch, read_page) -> str:
    """Відбиток редакції сторінки разом зі шматками, які вона вставляє. Шматок може взяти лише
    сторінка того самого розділу (`content/100-getting-started/…`), тож решта сторінок під час
    переліку не читається: її редакція — сам blob."""
    top = "/".join(path.split("/")[:2]) + "/"
    if not any(p.startswith(top) for p in files if WANTED[0].match(p)):
        return sha
    return _astromdx.revision(path, sha, files, fetch, {}, read_page)


def _label(text: str) -> list:
    text = " ".join(text.split())
    return ["", f"{text}:", ""] if text else [""]


def _attr(tag: str, name: str) -> str:
    m = re.search(rf"\b{name}\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|\{{\s*[\"']([^\"']*)[\"']\s*\}})", tag)
    return next((g for g in m.groups() if g), "") if m else ""


def _tab_names(tag: str) -> list:
    """Назви вкладок контейнера: `tabs={[<FileWithIcon text="SQL"/>, …]}` чи `items={['a', 'b']}`."""
    m = re.search(r"\btabs\s*=\s*\{\s*\[(.*)\]\s*\}", tag, re.S)
    if m:
        return re.findall(r"\btext\s*=\s*[\"']([^\"']*)[\"']", m.group(1))
    return _astromdx._items(tag)


def _tech(tag: str) -> list:
    m = re.search(r"technologies\s*=\s*\{\s*\[(.*?)\]\s*\}", tag, re.S)
    names = [a or b for a, b in _astromdx._STRINGS.findall(m.group(1))] if m else []
    names = [_TECH.get(n, n) for n in names if n and n != "*"]
    return _label(", ".join(names))


def _code_name(rest: str) -> list:
    """Рядок «File `schema.prisma`:» з `file=` чи `title=` у рядку відкриття коду."""
    m = _FILE.search(rest)
    name = next((g for g in m.groups() if g), "") if m else ""
    return ["", f"File `{name}`:", ""] if name else []


def _uncomment(rows: list) -> list:
    """Коментарі JSX `{/* … */}` поза кодом (бувають і на кілька рядків) → нічого. У коді вони —
    частина прикладу React, і там лишаються."""
    out, fence, i = [], "", 0
    while i < len(rows):
        line = rows[i]
        m = _FENCE.match(line)
        if fence:
            if line.strip().startswith(fence) and not line.strip().strip(fence[0]):
                fence = ""
        elif m:
            fence = m.group(2)
        elif "{/*" in line:
            j = i
            while "*/}" not in line[line.index("{/*"):] and j + 1 < len(rows):
                j += 1
                line += "\n" + rows[j]
            line = _JSX_COMMENT.sub("", line)
            out += line.split("\n") if line.strip() else []
            i = j + 1
            continue
        out.append(line)
        i += 1
    return out


def _components(text: str) -> str:
    out: list = []
    stack: list = []          # кадри вкладок: {"items", "i"}
    fence, skip = "", 0
    rows = _uncomment(text.split("\n"))

    def next_label(own: str = "") -> list:
        if not stack:
            return _label(own)
        frame = stack[-1]
        name = frame["items"][frame["i"]] if frame["i"] < len(frame["items"]) else ""
        frame["i"] += 1
        return _label(own or name)

    i = 0
    while i < len(rows):
        line = rows[i]
        if fence:
            if line.strip().startswith(fence) and not line.strip().strip(fence[0]):
                fence = ""
            if not skip:
                out.append(line)
            i += 1
            continue
        m = _FENCE.match(line)
        if m:
            fence = m.group(2)
            if not skip:
                out += _code_name(m.group(3))
                out.append(f"{m.group(1)}{m.group(2)}{m.group(3)}")
            i += 1
            continue
        c = _CLOSE.match(line)
        if c:
            name = c.group(1)
            if name == "NavigationLinksContainer":
                skip = max(0, skip - 1)
            elif name in ("TabbedContent", "Tabs") and stack:
                stack.pop()
            if not skip:
                out.append("")
            i += 1
            continue
        u = _OPEN.match(line)
        if not u:
            if not skip:
                out.append(line)
            i += 1
            continue
        name = u.group(1)
        tag, j = line, i
        while not _astromdx._closed(tag) and j + 1 < len(rows):
            j += 1
            tag += "\n" + rows[j]
        i = j + 1
        if name == "NavigationLinksContainer":
            if not tag.rstrip().endswith("/>"):
                skip += 1
            continue
        if skip:
            continue
        tail = "" if tag.rstrip().endswith("/>") else _astromdx._tail(tag, name)
        if name in ("TabbedContent", "Tabs"):
            stack.append({"items": _tab_names(tag), "i": 0})
            out.append("")
        elif name in ("tab", "TabItem", "Tab"):
            out += next_label(_attr(tag, "label") or _attr(tag, "value"))
        elif name == "SwitchTech":
            out += _tech(tag)
        elif name == "Admonition":
            kind = _attr(tag, "type")
            out += _label(_ADMONITION.get(kind, kind.capitalize()))
        elif name in ("Tip", "Info", "Warning"):
            out += _label(name)
        elif name == "cmdResult":
            out += _label("Output")
        elif name == "block":
            out += _label(_attr(tag, "content"))
        elif name == "Card":
            title = _attr(tag, "title")
            desc = _attr(tag, "description")
            body = re.sub(r"</Card\s*>", "", tail).strip()
            if not tag.rstrip().endswith("/>") and not re.search(r"</Card\s*>", tag):
                parts = []
                while i < len(rows):
                    row = rows[i]
                    i += 1
                    if re.search(r"</Card\s*>", row):
                        parts.append(re.sub(r"</Card\s*>.*", "", row).strip())
                        break
                    parts.append(row.strip())
                body = " ".join(p for p in [body] + parts if p)
            text = " — ".join(p for p in (title, desc or body) if p)
            out += ["", f"- {text}", ""] if text else [""]
            continue
        elif name == "Accordion":
            out += _label(_attr(tag, "title"))
        elif name in _DROP:
            out.append("")
        else:
            # Невідомий компонент — лишається рядком: його обробить загальний розбір MDX.
            out.append(tag)
            continue
        if tail:
            out += [tail, ""]
    return "\n".join(out)


def _endpoint(meta: dict) -> str:
    """Метод і шлях згенерованої сторінки REST API з її шапки (`metaTitle: 'DELETE /v1/… | …'`)."""
    if "_openapi" not in meta:
        return ""
    head = meta.get("metaTitle", "").split(" | ", 1)[0].strip()
    return f"Endpoint: `{head}`.\n\n" if re.match(r"^[A-Z]+ /", head) else ""


def _matching(text: str, start: int) -> int:
    """Позиція `}`, що закриває `{` на `start` (поза лапками), або -1."""
    depth, quote = 0, ""
    for pos in range(start, len(text)):
        ch = text[pos]
        if quote:
            if ch == quote:
                quote = ""
        elif ch in "'\"`":
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return pos
    return -1


def _conditions(text: str, props: dict) -> str:
    """`{props.x && (…)}` і `{props.x === 'y' && (…)}` → вміст, коли умова справджується, інакше
    нічого; обгортки `(`…`)` і `<>`…`</>` знімаються."""
    out, i = [], 0
    while (m := _COND.search(text, i)):
        end = _matching(text, m.start())
        if end < 0:
            break
        value = props.get(m.group(1), "")
        ok = (value == m.group(3)) if m.group(2) == "===" else (
            value != m.group(3)) if m.group(2) == "!==" else bool(value)
        body = text[m.end():end].strip()
        if body.startswith("(") and body.endswith(")"):
            body = body[1:-1].strip()
        if body.startswith("<>") and body.endswith("</>"):
            body = body[2:-3]
        out += [text[i:m.start()], _conditions(body, props) if ok else ""]
        i = end + 1
    return "".join(out) + text[i:]


_CODEBLOCK = re.compile(r"<CodeBlock\b([^>]*)>\s*\{`(.*?)`\}\s*</CodeBlock>", re.S)


def _codeblock(m) -> str:
    """`<CodeBlock language="prisma" metastring="file=…">{`…`}</CodeBlock>` шматка → блок коду."""
    head = " ".join(v for v in (_attr(m.group(1), "language"), _attr(m.group(1), "metastring")) if v)
    return f"\n```{head}\n{m.group(2).strip(chr(10))}\n```\n"


def _partials(text: str, path: str, files: dict, fetch, depth: int = 0) -> str:
    """Як у `_astromdx`, але з умовами на властивості: їх треба зважити до підстановки
    `{props.…}`, бо після неї від умови лишається порожнє місце."""
    def read(where, sha, props):
        piece = _conditions(fetch(where, sha), props)
        piece = re.sub(r"\$?\{\s*props\.(\w+)\.toLowerCase\(\)\s*\}",
                       lambda p: props.get(p.group(1), "").lower(), piece)
        piece = re.sub(r"\$\{\s*props\.(\w+)\s*\}", lambda p: props.get(p.group(1), ""), piece)
        piece = _CODEBLOCK.sub(_codeblock, piece)
        piece = re.sub(r"<code>([^<>]*)</code>", r"`\1`", piece)
        return _astromdx._props(piece, props)

    pieces = {name: _astromdx._resolve(rel, path, files, {})
              for name, rel in _astromdx._IMPORT.findall(text)}
    if not pieces:
        return text
    out, fence, rows, i = [], "", text.split("\n"), 0
    while i < len(rows):
        line = rows[i]
        m = _FENCE.match(line)
        if fence:
            if line.strip().startswith(fence) and not line.strip().strip(fence[0]):
                fence = ""
            out.append(line)
            i += 1
            continue
        if m:
            fence = m.group(2)
            out.append(line)
            i += 1
            continue
        u = re.match(r"^\s*<([A-Z$][\w$.]*)\b", line)
        if u and u.group(1) in pieces:
            tag, j = line, i
            while not _astromdx._closed(tag) and j + 1 < len(rows):
                j += 1
                tag += "\n" + rows[j]
            where = pieces[u.group(1)]
            if where in files and depth < 4:
                piece = read(where, files[where], _astromdx._attrs(tag))
                out += ["", _partials(piece, where, files, fetch, depth + 1), ""]
            i = j + 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def _prisma1(text: str, path: str) -> str:
    """`export const meta = {title: '…', …}` сторінки Prisma 1 → заголовок «# Назва (MySQL)»."""
    m = _META.search(text)
    if not m:
        return text
    end = _matching(text, m.end() - 1)
    block = text[m.start():end + 1] if end >= 0 else text[m.start():]
    t = _META_TITLE.search(block)
    title = (t.group(1) or t.group(2) or "").replace("\\'", "'") if t else ""
    v = _VARIANT.search(path)
    if title and v:
        title += f" ({_VARIANTS[v.group(1)]})"
    rest = text[:m.start()] + text[m.start() + len(block):]
    return f"# {title}\n\n{rest.lstrip()}" if title else rest


def expand(text: str, path: str, files: dict, fetch, meta: dict) -> str:
    """Тіло сторінки (без шапки YAML) з розкритими шматками й компонентами."""
    text = _partials(_prisma1(text, path), path, files, fetch)
    return _endpoint(meta) + _components(text)
