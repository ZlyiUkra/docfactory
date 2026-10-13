"""Сторінка сайту biomejs.dev з репозиторію → markdown, яким її бачить читач сайту.

biomejs.dev збирається Astro Starlight: до квітня 2024 — з теки `website/` репозиторію biomejs/biome, далі — з
окремого репозиторію biomejs/website. Сторінка там — не лише markdown:
- вивід діагностики на сторінках правил лінтера: у Biome 1 — сирий HTML `<pre class="language-text">` з кольорами
  `<span style=…>`, з серпня 2024 — рядок `<Fragment set:html={"…"} />`, де той самий HTML лежить рядком JS. Без
  розбору від виводу лишалися б обірвані теги й екрановані лапки, і повідомлення діагностики («This variable a is
  unused.») не знаходилося б;
- `<Icon name=… label="This rule is recommended" />` у таблицях правил — властивості правила (рекомендоване,
  безпечне чи небезпечне виправлення) стоять лише в підписі іконки;
- компоненти сайту, чий текст лежить у файлі компонента, а не на сторінці: `<PackageManagerBiomeCommand
  command="check --write" />` (команда для npm, pnpm, yarn, bun, deno), `<PackageManagerCommand npm={[…]} />`,
  `<EditorAction action="source.fixAll.biome" />` (налаштування VS Code і Zed). Шаблон команди сайт міняв не раз
  (`npx @biomejs/biome` → `npx biome`), тож він читається з файла компонента того самого знімка, а редакція сторінки
  враховує й цей файл;
- згенеровані компоненти `@/components/generated/…`: число правил (`<NumberOfRules />`), перелік рекомендованих
  правил і груп — їхній текст лежить у файлі `.astro`; шматки `.md`/`.mdx` (типова конфігурація, приклади виводу
  діагностики) розкриває `_astromdx`;
- вкладки Starlight `<Tabs>`/`<TabItem label="npm">` — назва вкладки стає підписом, `<Code code={`…`} />` —
  блоком коду; `${version}` сторінок, що беруть найновішу версію на час збирання сайту (`getLatestVersion`), —
  найновіша версія документа.

`files` — {шлях: sha} файлів знімка, які сторінка може взяти (див. `WANTED`), `fetch(шлях, sha)` — вміст файла.
"""

import hashlib
import html
import json
import posixpath
import re

from engine.readers import _astromdx, _markup

WANTED = [re.compile(r"^(?:website/)?src/components/.+\.(?:astro|mdx?)$")]

_IMPORT = re.compile(r"^import\s+([A-Za-z_$][\w$]*)\s+from\s+['\"]([^'\"]+\.(?:astro|mdx?))['\"];?[ \t]*$",
                     re.M)
_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})")
_OPEN = re.compile(r"<([A-Z][\w.]*)\b")
_LINE_OPEN = re.compile(r"^\s*<([A-Z][\w.]*)\b")
_LINE_CLOSE = re.compile(r"^\s*</([A-Z][\w.]*)\s*>\s*$")
_PRE = re.compile(r"^\s*<pre\s+class=\"language-[\w-]+\"><code\s+class=\"language-[\w-]+\">")
_ICON = re.compile(r"<Icon\b[^<>]*?/>")
_LABEL = re.compile(r"\blabel=\"([^\"]*)\"")
_BR = re.compile(r"<br\s*/?>")
_TAGS = re.compile(r"</?[A-Za-z][^<>]*>")
_LATEST = re.compile(r"getLatestVersion\s*\(")
# Навігація й прикраси сайту: перемикач мов правила, посилання в пісочницю, спонсори, аватарки.
_DROP = {"RuleLanguageLinks", "RulePlaygroundLink", "Sponsors", "Netlify", "Community", "AwardBanner",
         "FeaturedUsers", "LinterExample", "ProgressBarContainer", "Avatar", "Contributor", "Contributors",
         "Image", "Picture", "EditorSettings", "Maintainers", "Badge", "LinkButton", "Button", "YouTube",
         "Tweet", "InlineSVG", "Script", "Inputf", "Outputf"}
# Обгортки без власного тексту.
_WRAPPERS = {"Tabs", "Steps", "FileTree", "CardGrid", "LinkCard", "Fragment"}
_DEPTH = 4

# (шлях, sha сторінки) → (відбиток тексту, вставки); sha вставки → відбиток.
_PAGES: dict = {}
_DEPS: dict = {}


def _aliases(path: str) -> dict:
    root = "website/" if path.startswith("website/") else ""
    return {"@/": [f"{root}src/"]}


def _resolve(target: str, page: str, files: dict) -> str:
    return _astromdx._resolve(target, page, files, _aliases(page))


def _imports(text: str, path: str, files: dict) -> dict:
    return {name: _resolve(rel, path, files) for name, rel in _IMPORT.findall(text)}


def _deps(text: str, path: str, files: dict, fetch, depth: int = 0) -> list:
    out: list = []
    for where in _imports(text, path, files).values():
        if where in files and where not in out:
            out.append(where)
            if depth < _DEPTH and not where.endswith(".astro"):
                out += [p for p in _deps(fetch(where, files[where]), where, files, fetch, depth + 1)
                        if p not in out]
    return out


def revision(path: str, sha: str, files: dict, fetch, read_page, line: str = "") -> str:
    """Відбиток редакції сторінки разом із тим, що вона вставляє. Сторінка без вставок лишає sha blob:
    її редакцію й так визначає вміст файла. `line` — мажорна лінія знімка (див. нижче)."""
    info = _PAGES.get((path, sha))
    if info is None:
        text = read_page()
        info = (hashlib.sha1(text.encode()).hexdigest(), tuple(_deps(text, path, files, fetch)),
                bool(_LATEST.search(text)))
        _PAGES[(path, sha)] = info
    digest, deps, latest = info
    near = []
    for p in deps:
        if p in files:
            if files[p] not in _DEPS:
                _DEPS[files[p]] = hashlib.sha1(fetch(p, files[p]).encode()).hexdigest()
            near.append(f"{p}:{_DEPS[files[p]]}")
    if not near and not latest:
        return sha
    # `latest`: текст залежить від найновішої версії документа (адреса схеми, посилання на двійковий файл), тож
    # та сама сторінка двох ліній (1.9 і 2.x) — два документи, кожен із версією своєї лінії.
    return hashlib.sha1("\n".join([digest] + sorted(near) + ([f"latest:{line}"] if latest else []))
                        .encode()).hexdigest()


# --- вирази JS у шаблонах компонентів ----------------------------------------------------------

def _split_top(expr: str, op: str) -> list:
    """Розбити вираз за оператором верхнього рівня (поза лапками й дужками)."""
    parts, depth, quote, start, i = [], 0, "", 0, 0
    while i < len(expr):
        ch = expr[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = ""
        elif ch in "'\"`":
            quote = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif depth == 0 and expr.startswith(op, i):
            parts.append(expr[start:i])
            i += len(op)
            start = i
            continue
        i += 1
    parts.append(expr[start:])
    return parts


def _unescape(s: str) -> str:
    return re.sub(r"\\(.)", lambda m: {"n": "\n", "t": "\t"}.get(m.group(1), m.group(1)), s)


def _template(body: str, env: dict) -> str:
    out, i = [], 0
    while i < len(body):
        if body.startswith("${", i):
            depth, j = 1, i + 2
            while j < len(body) and depth:
                depth += {"{": 1, "}": -1}.get(body[j], 0)
                j += 1
            value = _eval(body[i + 2:j - 1], env)
            out.append("" if value is None or value is False else str(value))
            i = j
        elif body[i] == "\\" and i + 1 < len(body):
            out.append(_unescape(body[i:i + 2]))
            i += 2
        else:
            out.append(body[i])
            i += 1
    return "".join(out)


def _eval(expr: str, env: dict):
    expr = expr.strip()
    if not expr:
        return None
    q = _split_top(expr, "?")
    # `?` — тернарний оператор, якщо це не `??`
    if len(q) > 1 and "??" not in expr:
        cond, rest = q[0], "?".join(q[1:])
        branches = _split_top(rest, ":")
        if len(branches) == 2:
            return _eval(branches[0] if _eval(cond, env) else branches[1], env)
    parts = _split_top(expr, "??")
    if len(parts) > 1:
        for p in parts:
            v = _eval(p, env)
            if v is not None:
                return v
        return None
    parts = _split_top(expr, "===")
    if len(parts) == 2:
        return _eval(parts[0], env) == _eval(parts[1], env)
    if expr[0] == "(" and expr[-1] == ")":
        return _eval(expr[1:-1], env)
    if expr[0] == "`" and expr[-1] == "`":
        return _template(expr[1:-1], env)
    if expr[0] in "'\"" and expr[-1] == expr[0]:
        return _unescape(expr[1:-1])
    if expr == "true":
        return True
    if expr == "false":
        return False
    if re.fullmatch(r"-?\d+(\.\d+)?", expr):
        return expr
    m = re.fullmatch(r"Astro\.props\.(\w+)", expr)
    if m:
        return env.get("$props", {}).get(m.group(1))
    if re.fullmatch(r"[A-Za-z_$][\w$]*", expr):
        return env.get(expr)
    return None


def _props(tag: str) -> dict:
    """Властивості рядка-компонента: `a="x"`, `a={"x"}`, `a={["x", "y"]}`, `a={true}`, голе `a`."""
    m = re.match(r"\s*<[\w.]+", tag)
    rest = tag[m.end():] if m else tag
    rest = re.sub(r"/?>\s*$", "", rest.strip())
    props, i = {}, 0
    while i < len(rest):
        m = re.compile(r"\s*([\w:-]+)").match(rest, i)
        if not m:
            break
        name, i = m.group(1), m.end()
        if i < len(rest) and rest[i] == "=":
            i += 1
            if rest[i] in "'\"":
                end = rest.index(rest[i], i + 1)
                props[name], i = rest[i + 1:end], end + 1
            elif rest[i] == "{":
                depth, j = 0, i
                quote = ""
                while j < len(rest):
                    ch = rest[j]
                    if quote:
                        if ch == "\\":
                            j += 2
                            continue
                        if ch == quote:
                            quote = ""
                    elif ch in "'\"`":
                        quote = ch
                    elif ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                value = rest[i + 1:j].strip()
                i = j + 1
                if value.startswith("["):
                    props[name] = [a or b for a, b in re.findall(r'"((?:[^"\\]|\\.)*)"|\'([^\']*)\'', value)]
                else:
                    props[name] = _eval(value, {})
        else:
            props[name] = True
    return props


def _frontmatter(src: str) -> tuple:
    m = re.match(r"\s*---\n(.*?)\n---\n?(.*)\Z", src, re.S)
    return (m.group(1), m.group(2)) if m else ("", src)


def _render(src: str, props: dict) -> list:
    """Компонент-шаблон (вкладки команд, налаштування редактора) → рядки markdown."""
    front, body = _frontmatter(src)
    env = dict(props)
    env["$props"] = props
    for m in re.finditer(r"const\s+(\w+)\s*=\s*(`(?:[^`\\]|\\.)*`|\"[^\"\n]*\"|'[^'\n]*')\s*;?", front):
        env[m.group(1)] = _eval(m.group(2), env)
    # `let npmCommand = npm.reduce((acc, command) => { return `${acc}npm ${command}\n`; }, "");`
    for m in re.finditer(r"(?:let|const)\s+(\w+)\s*=\s*(\w+)\.reduce\(\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*=>"
                         r"\s*\{?\s*(?:return\s*)?(`(?:[^`\\]|\\.)*`)", front):
        name, arr, acc, item, tmpl = m.groups()
        text = ""
        for value in env.get(arr) or ():
            text = _eval(tmpl, {**env, acc: text, item: value})
        env[name] = text
    blocks = re.findall(r"<TabItem\b([^>]*)>(.*?)</TabItem>", body, re.S)
    blocks = [(_LABEL.search(a).group(1) if _LABEL.search(a) else "", inner) for a, inner in blocks]
    if not blocks:
        blocks = re.findall(r"<pre\b[^>]*\bdata-name=\"([^\"]+)\"[^>]*>(.*?)</pre>", body, re.S)
    out: list = []
    for label, inner in blocks:
        out += ["", f"{label}:", ""] if label else [""]
        code = re.search(r"<Code\b(.*?)/>", inner, re.S)
        if code:
            attrs = code.group(1)
            m = re.search(r"\bcode=\{", attrs)
            value = ""
            if m:
                expr = attrs[m.end():]
                depth, j = 1, 0
                quote = ""
                while j < len(expr) and depth:
                    ch = expr[j]
                    if quote:
                        if ch == "\\":
                            j += 2
                            continue
                        if ch == quote:
                            quote = ""
                    elif ch in "'\"`":
                        quote = ch
                    else:
                        depth += {"{": 1, "}": -1}.get(ch, 0)
                    j += 1
                value = _eval(expr[:j - 1], env) or ""
            lang = re.search(r"\blang=\"([^\"]*)\"", attrs)
            title = re.search(r"\btitle=\"([^\"]*)\"", attrs)
            if title:
                out += [f"{title.group(1)}:", ""]
            out += [f"```{lang.group(1) if lang else ''}", str(value).strip("\n"), "```", ""]
        else:
            text = re.sub(r"\{([^{}]*)\}", lambda e: str(_eval(e.group(1), env) or ""), inner)
            text = re.sub(r"<code>(.*?)</code>", r"`\1`", text)
            text = " ".join(_TAGS.sub("", text).split())
            if text:
                out += [text, ""]
    return out


def _generated(src: str) -> list:
    """Згенерований `.astro` (число правил, перелік рекомендованих правил, груп) → рядки тексту."""
    _, body = _frontmatter(src)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S).strip()
    if not body or re.fullmatch(r"<ul>\s*</ul>", body):
        return []
    if re.fullmatch(r"[\w.,]+", body):
        return [body]
    return [r for r in _markup.html_body(body).split("\n")]


# --- вивід діагностики ---------------------------------------------------------------------------

def _diagnostic(markup: str) -> list:
    text = _BR.sub("\n", markup)
    text = re.sub(r"</?(?:pre|code)\b[^>]*>", "", text)
    text = html.unescape(_TAGS.sub("", text))
    rows = [r.rstrip() for r in text.split("\n")]
    while rows and not rows[-1]:
        rows.pop()
    while rows and not rows[0]:
        rows.pop(0)
    return ["", "```text"] + rows + ["```", ""]


def _fragment(line: str) -> list | None:
    m = re.search(r"<Fragment\s+set:html=\{", line)
    if not m:
        return None
    rest = line[m.end():].lstrip()
    try:
        value, _ = json.JSONDecoder().raw_decode(rest)
    except ValueError:
        return None
    return _diagnostic(value) if isinstance(value, str) else None


# --- компоненти рядка ----------------------------------------------------------------------------

def _tag_end(text: str, start: int) -> int:
    """Позиція одразу за `>`, що закриває тег від `start` (поза дужками й лапками), або -1."""
    pos = _astromdx._end(text[start:])
    return start + pos + 1 if pos >= 0 else -1


def _inline(line: str, comps: dict, files: dict, fetch, env: dict) -> str:
    """Компоненти посеред рядка: іконки з підписом, згенероване число, навігація — геть."""
    line = _ICON.sub(lambda m: f"[{_LABEL.search(m.group(0)).group(1)}]"
                     if _LABEL.search(m.group(0)) else "", line)
    out, pos = [], 0
    for m in _OPEN.finditer(line):
        if m.start() < pos:
            continue
        name = m.group(1)
        if name not in _DROP and name not in comps:
            continue
        end = _tag_end(line, m.start())
        if end < 0:
            continue
        out.append(line[pos:m.start()])
        if name in comps and comps[name] in files:
            src = fetch(comps[name], files[comps[name]])
            if "/generated/" in comps[name]:
                rows = _generated(src)
                out.append(" ".join(r.strip() for r in rows if r.strip()))
            else:
                out.append(" ".join(r for r in _render(src, _props(line[m.start():end])) if r.strip()))
        pos = end
    out.append(line[pos:])
    if "{version}" in line and env.get("version"):
        return "".join(out).replace("{version}", env["version"])
    return "".join(out)


def _components(text: str, path: str, files: dict, fetch, version: str) -> str:
    comps = {n: w for n, w in _imports(text, path, files).items() if w.endswith(".astro")}
    latest = bool(_LATEST.search(text))
    env = {"version": version if latest else ""}
    out: list = []
    rows = text.split("\n")
    fence = ""
    i = 0
    while i < len(rows):
        line = rows[i]
        m = _FENCE.match(line)
        if fence:
            if line.strip().startswith(fence) and not line.strip().strip(fence[0]):
                fence = ""
            out.append(line.replace("${version}", version) if latest else line)
            i += 1
            continue
        if m:
            fence = m.group(2)
            out.append(line)
            i += 1
            continue
        frag = _fragment(line)
        if frag is not None:
            out += frag
            i += 1
            continue
        if _PRE.match(line):
            block = [line]
            while "</code></pre>" not in block[-1] and i + 1 < len(rows):
                i += 1
                block.append(rows[i])
            out += _diagnostic("\n".join(block))
            i += 1
            continue
        close = _LINE_CLOSE.match(line)
        if close:
            out.append("")
            i += 1
            continue
        u = _LINE_OPEN.match(line)
        if u:
            name = u.group(1)
            tag, j = line, i
            while _astromdx._end(tag.lstrip()) < 0 and j + 1 < len(rows):
                j += 1
                tag += "\n" + rows[j]
            whole = tag.strip()
            end = _tag_end(whole, 0)
            rest = whole[end:].strip() if end > 0 else ""
            if name in comps and (not rest or rest.startswith("</")):
                where = comps[name]
                if where in files:
                    src = fetch(where, files[where])
                    if "/generated/" in where:
                        if not re.search(r"Community|Contributors|Sponsors", where):
                            out += [""] + _generated(src) + [""]
                    else:
                        out += _render(src, _props(whole[:end]))
                i = j + 1
                continue
            if name in _DROP and not rest:
                out.append("")
                i = j + 1
                continue
            if name == "TabItem":
                label = _LABEL.search(whole[:end] if end > 0 else whole)
                out += ["", f"{label.group(1)}:", ""] if label else [""]
                if rest and not rest.startswith("</"):
                    out.append(rest)
                i = j + 1
                continue
            if name == "Code" and "code={" in whole:
                rendered = _render(f"<TabItem>{whole}</TabItem>", {"version": env["version"]})
                out += [r.replace("${version}", version) if latest else r for r in rendered]
                i = j + 1
                continue
            if name in _WRAPPERS and not rest:
                out.append("")
                i = j + 1
                continue
        out.append(_inline(line, comps, files, fetch, env))
        i += 1
    return "\n".join(out)


_REFDEF = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s+\S+.*$")


def _references(text: str) -> str:
    """Посилання-виноски (`[standalone executable]` у тексті й `[standalone executable]: /guides/…` нижче) →
    сам текст посилання: рядок-визначення — розмітка, а не зміст сторінки."""
    names, out, fence = set(), [], ""
    for line in text.split("\n"):
        m = _FENCE.match(line)
        if fence:
            if line.strip().startswith(fence) and not line.strip().strip(fence[0]):
                fence = ""
        elif m:
            fence = m.group(2)
        elif _REFDEF.match(line):
            names.add(_REFDEF.match(line).group(1).lower())
            continue
        out.append(line)
    if not names:
        return text
    rx = re.compile(r"\[([^\]\n]+)\](?![(\[:])")
    return "\n".join(rx.sub(lambda m: m.group(1) if m.group(1).lower() in names else m.group(0), ln)
                     if not ln.lstrip().startswith(("```", "~~~")) else ln for ln in out)


def expand(text: str, path: str, files: dict, fetch, version: str = "") -> str:
    """Тіло сторінки (без шапки YAML) з розкритими вставками й компонентами. `version` — найновіша версія
    документа: її підставляють сторінки, що беруть версію сайту на час збирання."""
    newest = version.split(",")[0].strip()
    text = _astromdx._partials(text, path, files, fetch, _aliases(path))
    return _references(_components(text, path, files, fetch, newest))
