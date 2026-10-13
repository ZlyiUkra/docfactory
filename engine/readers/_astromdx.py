"""Сторінка сайту на Astro з MDX із репозиторію → markdown, яким її бачить читач сайту.

orm.drizzle.team збирається Astro з теки `src/content`, і сторінка — не лише markdown:
- `import InstallPackages from '@mdx/get-started/InstallPackages.mdx'` і рядок
  `<InstallPackages lib='pg' devlib=' @types/pg'/>` — спільний шматок MDX (кроки «Get started» кожного
  драйвера), де `{props.lib}` — значення властивості з рядка вставки;
- `<Tabs items={['PostgreSQL', 'MySQL', 'SQLite']}>` з `<Tab>` усередині і `<CodeTabs items={…}>`, де
  вкладкою стає кожен блок коду, `<Section>` чи `<CodeTab>`, — той самий приклад для кожного діалекту чи
  файла; назви вкладок стоять лише в `items`;
- `<Npm>drizzle-orm pg</Npm>` — сайт показує `npm i drizzle-orm pg` (і те саме для yarn, pnpm, bun),
  `<Npx>drizzle-kit push</Npx>` — `npx drizzle-kit push`;
- `<IsSupportedChipGroup chips={{ PostgreSQL: true, MySQL: false }} />` — які діалекти мають можливість;
- `<Callout type="warning">` — виноска з підписом IMPORTANT, `type="error"` — WARNING, `title` — свій підпис;
- `<LinksList title links={[[назва, адреса], …]} />` — перелік посилань розділу;
- `<CodeWithProps name="x">` — код, де `$name$` стає значенням властивості.

Без цього приклади всіх діалектів злипалися б в один код без підписів, кроки встановлення були б порожніми,
а позначки підтримки зникали б, і на «чи є це в SQLite» корпус не мав би відповіді.

Псевдоніми шляхів сайт міняв: до листопада 2024 `@mdx/*` вів у `src/components/markdown/`, далі — у
`src/mdx/`. Тому псевдонім — перелік тек: береться перша, де файл на цьому тезі є. Шматок кроків
міняється частіше за сторінку, що його вставляє, тож редакція сторінки рахується разом зі вставками.

`files` — {шлях: sha} файлів тегу, які сторінка може взяти (див. `wanted`), `fetch(шлях, sha)` — вміст
файла. Вставка, файла якої на тезі немає, зникає, як зникла б і на сайті, що без неї не зібрався б.
"""

import hashlib
import posixpath
import re

_IMPORT = re.compile(r"^import\s+([A-Za-z_$][\w$]*)\s+from\s+['\"]([^'\"]+\.mdx?)['\"];?[ \t]*$", re.M)
_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})")
_OPEN = re.compile(r"^\s*<([A-Z$][\w$.]*)\b")
_ATTR = re.compile(r"([\w-]+)\s*=\s*(?:'([^']*)'|\"([^\"]*)\"|\{\s*['\"]([^'\"]*)['\"]\s*\})")
_STRINGS = re.compile(r"'([^']*)'|\"([^\"]*)\"")
_CHIP = re.compile(r"['\"]?([\w .+/-]+?)['\"]?\s*:\s*(true|false)")
_LINK = re.compile(r"\[\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\]")
_PROPS = re.compile(r"\{\s*props\.(\w+)\s*\}")
_RULE = re.compile(r"^#{1,6}[ \t]*-{3,}[ \t]*$")
# Обгортки без власного тексту: розмітка сітки й кроків.
_WRAPPERS = {"Section", "Steps", "Flex", "CenteredLayout", "TableWrapper", "Tag"}
# Навігація сайту: картки «що далі», хлібні крихти, відео — тексту сторінки не несуть.
_DROP = {"Breadcrumbs", "AnchorCards", "YoutubeCards", "SimpleLinkCards", "Button", "GetStartedLinks",
         "WhatsNextPostgres", "WhatsNextMySQL", "WhatsNextSQLite", "WhatsNextSingleStore",
         "WhatsNextMSSQL", "WhatsNextCockroach", "BlogCards", "CompanyLogos", "StudioHero",
         "ContactProductManager", "MdxBenchmark", "BenchmarkHeader", "LatestReleases", "Guides",
         "Tutorials", "LearnPage", "ThemeImage"}
_COMMANDS = {"Npm": "npm i", "Npx": "npx", "NpxCompact": "npx"}
_DEPTH = 4

# (шлях, sha сторінки) → (відбиток тексту, шляхи вставок); sha шматка → відбиток. Та сама редакція
# сторінки стоїть у десятках знімків, а читати її заради відбитка щоразу — даремно.
_PAGES: dict = {}
_DEPS: dict = {}


def wanted(aliases: dict) -> list:
    """Файли тегу, які сторінки можуть вставити: MDX у теках псевдонімів."""
    dirs = sorted({d.strip("/") for targets in aliases.values() for d in targets if d.strip("/")})
    alt = "|".join(re.escape(d) for d in dirs) or r"(?!)"
    return [re.compile(rf"^(?:{alt})/.+\.mdx?$")]


def _resolve(target: str, page: str, files: dict, aliases: dict) -> str:
    for prefix in sorted(aliases, key=len, reverse=True):
        if target.startswith(prefix):
            tail = target[len(prefix):]
            options = [posixpath.normpath(f"{d.strip('/')}/{tail}") for d in aliases[prefix]]
            return next((p for p in options if p in files), options[0])
    return posixpath.normpath(posixpath.join(posixpath.dirname(page), target))


def _deps(text: str, path: str, files: dict, fetch, aliases: dict, depth: int = 0) -> list:
    out: list = []
    for _, rel in _IMPORT.findall(text):
        where = _resolve(rel, path, files, aliases)
        if where in files and where not in out:
            out.append(where)
            if depth < _DEPTH:
                out += [p for p in _deps(fetch(where, files[where]), where, files, fetch, aliases,
                                         depth + 1) if p not in out]
    return out


def revision(path: str, sha: str, files: dict, fetch, aliases: dict, read_page) -> str:
    """Відбиток редакції сторінки разом із тим, що вона вставляє. `read_page()` — текст сторінки;
    читається один раз на неповторний вміст."""
    info = _PAGES.get((path, sha))
    if info is None:
        text = read_page()
        info = (hashlib.sha1(text.encode()).hexdigest(), tuple(_deps(text, path, files, fetch, aliases)))
        _PAGES[(path, sha)] = info
    digest, deps = info
    near = []
    for p in deps:
        if p in files:
            if files[p] not in _DEPS:
                _DEPS[files[p]] = hashlib.sha1(fetch(p, files[p]).encode()).hexdigest()
            near.append(f"{p}:{_DEPS[files[p]]}")
    return hashlib.sha1("\n".join([digest] + sorted(near)).encode()).hexdigest()


def _attrs(tag: str) -> dict:
    return {k: next((v for v in vals if v), "") for k, *vals in _ATTR.findall(tag)}


def _items(tag: str) -> list:
    m = re.search(r"items\s*=\s*\{\s*\[(.*?)\]\s*\}", tag, re.S)
    return [a or b for a, b in _STRINGS.findall(m.group(1))] if m else []


def _end(tag: str) -> int:
    """Позиція `>`, що закриває відкривальний тег (поза дужками й лапками), або -1."""
    depth, quote = 0, ""
    for pos, ch in enumerate(tag):
        if quote:
            if ch == quote:
                quote = ""
        elif ch in "'\"`":
            quote = ch
        elif ch in "{[(":
            depth += 1
        elif ch in "}])":
            depth -= 1
        elif ch == ">" and depth <= 0:
            return pos
    return -1


def _closed(tag: str) -> bool:
    return _end(tag) >= 0


def _tail(tag: str, name: str) -> str:
    """Текст, що стоїть у рядку одразу за відкривальним тегом (`<Callout type="warning">Push …`)."""
    pos = _end(tag)
    tail = tag[pos + 1:] if pos >= 0 else ""
    return re.sub(rf"</{re.escape(name)}\s*>", "", tail).strip()


def _partials(text: str, path: str, files: dict, fetch, aliases: dict, depth: int = 0) -> str:
    """`<Назва власт='…'/>` імпортованого шматка MDX → його текст з підставленими `{props.…}`."""
    pieces = {name: _resolve(rel, path, files, aliases) for name, rel in _IMPORT.findall(text)}
    if not pieces:
        return text
    out, fence, rows = [], "", text.split("\n")
    i = 0
    while i < len(rows):
        line = rows[i]
        m = _FENCE.match(line)
        if fence:
            if line.strip().startswith(fence):
                fence = ""
            out.append(line)
            i += 1
            continue
        if m:
            fence = m.group(2)
            out.append(line)
            i += 1
            continue
        u = _OPEN.match(line)
        if u and u.group(1) in pieces:
            tag, j = line, i
            while not _closed(tag) and j + 1 < len(rows):
                j += 1
                tag += "\n" + rows[j]
            where = pieces[u.group(1)]
            if where in files and depth < _DEPTH:
                props = _attrs(tag)
                piece = _props(fetch(where, files[where]), props)
                piece = _partials(piece, where, files, fetch, aliases, depth + 1)
                out += ["", piece, ""]
            i = j + 1
            continue
        # Шматок посеред рядка — у клітинці таблиці (`| type | <Dialects/> |`): текст в один рядок.
        line = re.sub(r"<([A-Z$][\w$]*)\s*/>", lambda t: _inline_piece(t, pieces, files, fetch), line)
        out.append(line)
        i += 1
    return "\n".join(out)


def _props(text: str, props: dict) -> str:
    """`{props.x}` → значення. У властивості вкладеного компонента (`env_variable={props.env_variable}`
    для `<CodeWithProps>`) значення стає рядком у лапках, інакше його не прочитає розбір властивостей."""
    text = re.sub(r"=\s*\{\s*props\.(\w+)\s*\}",
                  lambda p: '="' + props.get(p.group(1), "").replace('"', "'") + '"', text)
    return _PROPS.sub(lambda p: props.get(p.group(1), ""), text)


def _inline_piece(m, pieces: dict, files: dict, fetch) -> str:
    where = pieces.get(m.group(1))
    if not where:
        return m.group(0)
    if where not in files:
        return ""
    text = re.sub(r"^import\s.*$", "", fetch(where, files[where]), flags=re.M)
    return " ".join(r.strip() for r in text.split("\n") if r.strip())


def _command(word: str, body: str) -> list:
    rows = [r.strip().replace("—", "--") for r in body.split("\n") if r.strip()]
    return ["", "```bash"] + [f"{word} {r}" for r in rows] + ["```", ""]


def _callout(tag: str) -> list:
    a = _attrs(tag)
    label = a.get("title") or {"warning": "Important", "error": "Warning"}.get(a.get("type", ""), "")
    return ["", f"{label}:", ""] if label else [""]


def _chips(tag: str) -> list:
    yes = [n.strip() for n, v in _CHIP.findall(tag) if v == "true"]
    no = [n.strip() for n, v in _CHIP.findall(tag) if v == "false"]
    parts = []
    if yes:
        parts.append("Supported: " + ", ".join(yes) + ".")
    if no:
        parts.append("Not supported: " + ", ".join(no) + ".")
    return ["", " ".join(parts), ""] if parts else [""]


def _links(tag: str) -> list:
    title = _attrs(tag).get("title", "")
    rows = [f"- {name}" for name, _ in _LINK.findall(tag)]
    return ["", f"{title}:", ""] + rows + [""] if title else [""] + rows + [""]


def _components(text: str) -> str:
    """Компоненти сайту → текст: підписи вкладок, команди встановлення, позначки підтримки."""
    out: list = []
    stack: list = []          # кадри вкладок: {"kind", "items", "i", "inner"}
    subst: list = []          # властивості відкритих <CodeWithProps>
    fence = ""
    rows = text.split("\n")

    def label():
        frame = stack[-1]
        name = frame["items"][frame["i"]] if frame["i"] < len(frame["items"]) else ""
        frame["i"] += 1
        return ["", f"{name}:", ""] if name else [""]

    i = 0
    while i < len(rows):
        line = rows[i]
        if fence:
            if line.strip().startswith(fence) and not line.strip().strip(fence[0]):
                fence = ""
            for props in subst:
                for k, v in props.items():
                    line = line.replace(f"${k}$", v)
            out.append(line)
            i += 1
            continue
        m = _FENCE.match(line)
        if m:
            if stack and stack[-1]["kind"] == "codetabs" and stack[-1]["inner"] == 0:
                out += label()
            fence = m.group(2)
            out.append(line)
            i += 1
            continue
        if _RULE.match(line):
            # `## ---` — роздільник між групами розділів (у select, column-types): на сайті риска, а в
            # тексті — заголовок без назви, під яким опинилися б усі наступні розділи сторінки.
            out.append("")
            i += 1
            continue
        u = _OPEN.match(line) or re.match(r"^\s*</([A-Z$][\w$.]*)\s*>", line)
        if not u:
            out.append(line)
            i += 1
            continue
        name = u.group(1)
        closing = line.lstrip().startswith("</")
        tag, j = line, i
        if not closing:
            while not _closed(tag) and j + 1 < len(rows):
                j += 1
                tag += "\n" + rows[j]
        rest = tag.strip()
        self_closing = rest.endswith("/>")
        inline = None
        i = j + 1
        if closing:
            if name in ("Tabs", "CodeTabs") and stack:
                stack.pop()
            elif name in ("Section", "CodeTab", "Tab") and stack and stack[-1]["inner"] > 0:
                stack[-1]["inner"] -= 1
            elif name == "CodeWithProps" and subst:
                subst.pop()
            out.append("")
            continue
        if name in ("Tabs", "CodeTabs"):
            stack.append({"kind": name.lower(), "items": _items(tag), "i": 0, "inner": 0})
            out.append("")
        elif name == "Tab":
            if stack and stack[-1]["kind"] == "tabs":
                out += label()
                stack[-1]["inner"] += 1
            else:
                out.append("")
        elif name in ("Section", "CodeTab"):
            if stack and stack[-1]["kind"] == "codetabs":
                if stack[-1]["inner"] == 0:
                    out += label()
                stack[-1]["inner"] += 1
            elif stack:
                stack[-1]["inner"] += 1
            # Однорядковий `<Section>…</Section>` не трапляється; закриття — окремим рядком.
            out.append("")
        elif name in _COMMANDS:
            word = _COMMANDS[name]
            inline = re.match(rf"^\s*<{name}\b[^>]*>(.*?)</{name}>\s*$", tag, re.S)
            if inline:
                out += _command(word, inline.group(1))
            else:
                body = []
                while i < len(rows) and not re.match(rf"^\s*</{name}>", rows[i]):
                    body.append(rows[i])
                    i += 1
                i += 1
                out += _command(word, "\n".join(body))
        elif name == "Callout":
            inline = re.match(r"^\s*(<Callout\b[^>]*>)(.*?)</Callout>\s*$", tag, re.S)
            if inline:
                out += _callout(inline.group(1)) + [inline.group(2).strip(), ""]
            else:
                out += _callout(tag)
        elif name == "Prerequisites":
            out += ["", "Prerequisites:", ""]
        elif name == "IsSupportedChipGroup":
            out += _chips(tag)
        elif name == "LinksList":
            out += _links(tag)
        elif name == "CodeWithProps":
            subst.append({k: v for k, v in _attrs(tag).items()})
            out.append("")
        elif name in _WRAPPERS or name in _DROP:
            out.append("")
        else:
            # Невідомий компонент — лишається рядком: його обробить загальний розбір MDX.
            out.append(tag)
            continue
        tail = "" if self_closing or name in _COMMANDS else _tail(tag, name)
        if tail and not (name == "Callout" and inline):
            out += [tail, ""]
    return "\n".join(out)


def expand(text: str, path: str, files: dict, fetch, aliases: dict) -> str:
    """Тіло сторінки (без шапки YAML) з розкритими вставками й компонентами."""
    return _components(_partials(text, path, files, fetch, aliases))
