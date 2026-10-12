"""Сторінка сайту на Vocs із репозиторію → markdown, яким її бачить читач сайту.

viem.sh від версії 2.0.10 збирається Vocs із теки `site/pages`, і частина тексту сторінки лежить в інших
файлах:
- `// [!include ~/snippets/publicClient.ts]` у блоці коду — файл від кореня сайту (`~`); з `:назва` — лише
  область між `// [!region назва]` і `// [!endregion назва]`; без `~` — файл поруч зі сторінкою або блок
  цієї ж сторінки з таким підписом (`ts [config.ts]`);
- `import WriteParameters from '../../snippets/tempo/write-parameters.mdx'` і рядок `<WriteParameters />` —
  спільний шматок MDX (параметри транзакції), однаковий для десятків дій.

Блоки коду — twoslash. `// @twoslash-cache: {…}` — кеш підказок типів на кілька кілобайтів; рядки до
`// ---cut---` сайт ховає (там налаштування клієнта, яке вставка поклала згори); `// ^?`, `// @noErrors`,
`// @filename: …` — службові; `// @log: …` сайт показує як вивід прикладу. Ще Vocs пише контейнери
`:::tip`, `:::warning[Назва]`, групи вкладок `:::code-group`, кроки `::::steps` і меню розділу картками
`<Card title description to />` у `<Cards>`.

Без цього сторінка дії мала б кеш типів замість прикладу, а розділ «Parameters» дій Tempo — порожній рядок.
Кеш twoslash перегенеровується разом із типами, тож відбиток редакції береться з тексту без нього: інакше
незмінна для читача сторінка давала б нову редакцію ледь не з кожним випуском.

`files` — {шлях: sha} файлів тегу, які сторінка може взяти (див. `wanted`), `fetch(шлях, sha)` — вміст
файла. Вставка, файла якої на тезі немає, просто зникає.
"""

import hashlib
import posixpath
import re

from engine.readers import _vitepress

_CACHE = re.compile(r"^[ \t]*//[ \t]*@twoslash-cache:.*$\n?", re.M)
_INCLUDE = re.compile(r"^([ \t]*)//[ \t]*\[!include[ \t]+([^\]\s:]+)(?::([\w-]+))?[ \t]*\][ \t]*$")
_REGION = re.compile(r"^[ \t]*(?://|#|<!--|\{/\*)[ \t]*\[!(?:region|endregion)\b[^\]]*\]")
_IMPORT = re.compile(r"^import\s+([A-Za-z_$][\w$]*)\s+from\s+['\"]([^'\"]+\.mdx?)['\"];?[ \t]*$", re.M)
_USE = re.compile(r"^[ \t]*<([A-Z][\w$]*)\b[^<>]*/>[ \t]*$")
_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})[ \t]*([\w+#.-]*)[ \t]*(.*?)[ \t]*$")
_DIRECTIVE = re.compile(r"^[ \t]*:{3,}[ \t]*([\w-]+)[ \t]*(?:\[([^\]]*)\])?[ \t]*(?:\{[^}]*\})?[ \t]*$")
_DIRECTIVE_END = re.compile(r"^[ \t]*:{3,}[ \t]*$")
_CUT = re.compile(r"^[ \t]*//[ \t]*---cut(?:-before)?---[ \t]*$")
_CUT_AFTER = re.compile(r"^[ \t]*//[ \t]*---cut-after---[ \t]*$")
_CUT_START = re.compile(r"^[ \t]*//[ \t]*---cut-start---[ \t]*$")
_CUT_END = re.compile(r"^[ \t]*//[ \t]*---cut-end---[ \t]*$")
# Службові рядки twoslash. `// @ts-expect-error` — справжня частина прикладу, вона лишається.
_TWOSLASH = re.compile(r"^[ \t]*//[ \t]*(?:\^[?|]|@(?!ts-|log:|warn:|error:)[\w-]+(?::.*)?)[ \t]*$")
_LOG = re.compile(r"^([ \t]*)//[ \t]*@(?:log|warn|error):[ \t]?(.*)$")
_SHIKI = re.compile(r"[ \t]*(?://|#|<!--)?[ \t]*\[!code [^\]]*\](?:[ \t]*-->)?")
_CARD = re.compile(r"<Card\b((?:[^<>\"{}]|\"[^\"]*\"|\{[^{}]*\})*?)/>", re.S)
_CARDS = re.compile(r"^[ \t]*</?Cards>[ \t]*$\n?", re.M)
_ATTR = re.compile(r"(\w+)\s*=\s*(?:\"([^\"]*)\"|\{\s*['\"]([^'\"]*)['\"]\s*\})")
_SKIP_KINDS = {"code-group", "steps"}
# Заголовок сторінки з підзаголовком Vocs: «# Public Client [A function to create a Public Client]».
_H1_SUBTITLE = re.compile(r"^#[ \t]+(.+?)[ \t]+\[([^\]]+)\][ \t]*$", re.M)

# (шлях, sha сторінки) → (відбиток тексту без кешу, шляхи можливих вставок). Та сама редакція
# сторінки стоїть у сотнях тегів, а читати її з диска щоразу заради відбитка — даремно.
_PAGES: dict = {}
_DEPS: dict = {}


def wanted(root: str) -> list:
    """Файли тегу, які сторінки можуть узяти: шматки й код прикладів під коренем сайту."""
    r = re.escape(root.strip("/"))
    return [re.compile(rf"^{r}/(?!public/|node_modules/).+\.(md|mdx|ts|tsx|js|json|sol)$")]


def _resolve(target: str, page: str, root: str) -> str:
    if target.startswith("~/"):
        return posixpath.normpath(f"{root.strip('/')}/{target[2:]}")
    return posixpath.normpath(posixpath.join(posixpath.dirname(page), target))


def _code_includes(text: str, path: str, root: str) -> list[str]:
    out = []
    for line in text.split("\n"):
        m = _INCLUDE.match(line)
        if m:
            out.append(_resolve(m.group(2), path, root))
    return out


def _deps(text: str, path: str, root: str, files: dict, fetch, depth: int = 0) -> list[str]:
    """Шляхи файлів, які сторінка тягне вставками, разом із вкладеними."""
    out = []
    for where in [_resolve(rel, path, root) for _, rel in _IMPORT.findall(text)]:
        if where not in out:
            out.append(where)
            if where in files and depth < 3:
                out += [p for p in _deps(fetch(where, files[where]), where, root, files, fetch,
                                         depth + 1) if p not in out]
    out += [p for p in _code_includes(text, path, root) if p not in out]
    return out


def _digest(text: str) -> str:
    return hashlib.sha1(_CACHE.sub("", text).encode()).hexdigest()


def revision(path: str, sha: str, files: dict, fetch, root: str, read_page) -> str:
    """Відбиток редакції сторінки разом із тим, що вона вставляє, без кешу twoslash.
    `read_page()` — текст сторінки; читається один раз на неповторний вміст."""
    info = _PAGES.get((path, sha))
    if info is None:
        text = read_page()
        info = (_digest(text), tuple(_deps(text, path, root, files, fetch)))
        _PAGES[(path, sha)] = info
    digest, deps = info
    near = []
    for p in deps:
        if p in files:
            if files[p] not in _DEPS:
                _DEPS[files[p]] = _digest(fetch(p, files[p]))
            near.append(f"{p}:{_DEPS[files[p]]}")
    return hashlib.sha1("\n".join([digest] + sorted(near)).encode()).hexdigest()


def _region(text: str, name: str | None) -> str:
    """Область `// [!region назва]` … `// [!endregion назва]`; позначки інших областей знімаються."""
    rows = text.split("\n")
    if name:
        out, inside = [], False
        for row in rows:
            if re.search(rf"\[!region\s+{re.escape(name)}\]", row):
                inside = True
            elif inside and re.search(rf"\[!endregion\s+{re.escape(name)}\]", row):
                break
            elif inside:
                out.append(row)
        rows = out or rows
    return "\n".join(r for r in rows if not _REGION.match(r)).strip("\n")


def _code(lines: list, path: str, root: str, files: dict, fetch, blocks: dict) -> list:
    """Рядки блоку коду twoslash → рядки, які сайт показує."""
    body = []
    for line in lines:
        if _CACHE.match(line):
            continue
        m = _INCLUDE.match(line)
        if m:
            where = _resolve(m.group(2), path, root)
            if where in files:
                piece = _CACHE.sub("", fetch(where, files[where]))
            else:
                piece = blocks.get(posixpath.basename(m.group(2)), "")
            piece = _region(piece, m.group(3))
            body += [m.group(1) + row if row else row for row in piece.split("\n")] if piece else []
            continue
        body.append(line)
    cuts = [i for i, row in enumerate(body) if _CUT.match(row)]
    if cuts:
        body = body[cuts[-1] + 1:]
    after = next((i for i, row in enumerate(body) if _CUT_AFTER.match(row)), None)
    if after is not None:
        body = body[:after]
    out, hidden = [], False
    for row in body:
        if _CUT_START.match(row):
            hidden = True
        elif _CUT_END.match(row):
            hidden = False
        elif not hidden and not _TWOSLASH.match(row):
            out.append(_SHIKI.sub("", _LOG.sub(r"\1// \2", row)))
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def _labelled(text: str) -> dict:
    """Блоки сторінки з підписом-файлом (`ts [config.ts]`) → їхній код: `[!include config.ts]` без
    `~` бере саме його, коли поруч зі сторінкою такого файла немає."""
    out, label, fence, rows = {}, "", "", []
    for line in text.split("\n"):
        m = _FENCE.match(line)
        if fence:
            if line.strip() and set(line.strip()) == {fence[0]} and len(line.strip()) >= len(fence):
                if label:
                    out.setdefault(label, "\n".join(r for r in rows if not _CACHE.match(r)))
                fence = ""
            else:
                rows.append(line)
        elif m:
            fence, rows = m.group(2), []
            hit = re.search(r"\[([^\]]+)\]", m.group(4))
            label = posixpath.basename(hit.group(1)) if hit else ""
    return out


def _card(m) -> str:
    attrs = {k: a or b for k, a, b in _ATTR.findall(m.group(1))}
    title, desc = attrs.get("title", "").strip(), attrs.get("description", "").strip()
    if not title:
        return ""
    return f"- {title}: {desc}" if desc else f"- {title}"


def _components(text: str, path: str, root: str, files: dict, fetch, depth: int = 0) -> str:
    """`<Назва />` імпортованого шматка MDX → його текст (рекурсивно); картки → пункти списку."""
    pieces = {name: _resolve(rel, path, root) for name, rel in _IMPORT.findall(text)}
    out, fence = [], ""
    for line in text.split("\n"):
        m = _FENCE.match(line)
        if fence:
            if line.strip() and set(line.strip()) == {fence[0]} and len(line.strip()) >= len(fence):
                fence = ""
        elif m:
            fence = m.group(2)
        elif (u := _USE.match(line)) and u.group(1) in pieces:
            where = pieces[u.group(1)]
            if where in files and depth < 3:
                piece = _vitepress._front_out(fetch(where, files[where]))
                piece = _components(piece, where, root, files, fetch, depth + 1)
                out += ["", piece, ""]
            continue
        out.append(line)
    text = "\n".join(out)
    return _CARDS.sub("", _CARD.sub(_card, text))


def expand(text: str, path: str, files: dict, fetch, root: str) -> str:
    """Тіло сторінки (без шапки YAML) з розкритими вставками, кодом і контейнерами."""
    text = _components(text, path, root, files, fetch)
    # Підзаголовок — опис під назвою, а не частина назви.
    text = _H1_SUBTITLE.sub(lambda m: f"# {m.group(1)}\n\n{m.group(2)}.", text, count=1)
    blocks = _labelled(text)
    out, fence, rows, info = [], "", [], None
    for line in text.split("\n"):
        if fence:
            if line.strip() and set(line.strip()) == {fence[0]} and len(line.strip()) >= len(fence):
                pad, lang = info
                out += [f"{pad}{fence}{lang}"] + _code(rows, path, root, files, fetch, blocks)
                out.append(f"{pad}{fence}")
                fence = ""
            else:
                rows.append(line)
            continue
        m = _FENCE.match(line)
        if m:
            pad, fence, lang, rest = m.groups()
            hit = re.search(r"\[([^\]]+)\]", rest)
            if hit:
                out += ["", f"{pad}{hit.group(1)}:"]
            rows, info = [], (pad, lang)
            continue
        m = _DIRECTIVE.match(line)
        if m:
            kind = m.group(1).lower()
            if kind not in _SKIP_KINDS:
                head = _vitepress._LABELS.get(kind, kind.capitalize())
                title = (m.group(2) or "").strip()
                out += ["", f"{head}: {title}" if title and title.lower() != kind else f"{head}:", ""]
            else:
                out.append("")
            continue
        if _DIRECTIVE_END.match(line):
            out.append("")
            continue
        out.append(line)
    if fence:
        out += [f"{info[0]}{fence}{info[1]}"] + _code(rows, path, root, files, fetch, blocks)
    return "\n".join(out)
