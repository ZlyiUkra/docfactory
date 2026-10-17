"""Читач файлів репозиторію LibreOffice/core на багатьох тегах: UNO IDL, фрагменти фільтрів, `soffice --help`.

`ghcode-history-lo` — `url` — префікс дерев (…/repos/ВЛАСНИК/РЕПО/git/trees/), `tags` — об'єкт
                      «тег → версія», від найновішого; `roots` — теки від кореня репозиторію, чиї
                      дерева беруться (`offapi`, `filter/source/config/fragments`…); `include` —
                      вирази повних шляхів, що беруться. Необов'язкові: `exclude`, `name_prefix`,
                      `max_file` — межа розміру файла в байтах (типово 200 000).

Навіщо окремий читач, а не `ghcode-history`. Дерево `core` з усіма теками GitHub віддає обрізаним
(понад сто тисяч файлів), тож дерево береться потеково — `тег:тека`. А сирий код тут погано
шукається: файл IDL — це інтерфейс з десятками методів, і поділений лише за довжиною, він дає
фрагменти, де опис методу відірвано від його імені. Тому:
- `.idl` — назва типу (`com.sun.star.frame.XStorable`), опис типу і по розділу на кожен член
  (метод, атрибут, властивість, експортований інтерфейс, поле структури, значення переліку чи
  константа): опис з коментаря `/** … */` текстом, з тегами `@param`, `@returns`, `@throws`,
  `@since` підписами, і оголошення блоком коду;
- фрагменти фільтрів і типів (`filter/source/config/fragments/{filters,types}/*.xcu`) — назва
  фільтра для `--convert-to` та `--infilter`, напрям (імпорт, експорт) і всі властивості таблицею;
- `desktop/source/app/cmdlinehelp.cxx` — текст, який друкує `soffice --help` у цій версії, з
  розділами за його рубриками.

Одиниця — пара «шлях, вміст» з усіма тегами, де файл лежав саме таким; читається з найновішого з них
(так само кладе його й `tools/seed_git_store.py`).
"""

import json
import re
from html import unescape
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_MAX_FILE = 200_000


# --- UNO IDL ---

_KINDS = r"(?:interface|service|struct|enum|constants|exception|typedef|singleton)"
_TOKENS = re.compile(r"/\*\*(?!/)(.*?)\*/|/\*.*?\*/|//[^\n]*|\{|\}|;|,|[^{};,/]+|/", re.S)
_DOC_TAGS = [
    (re.compile(r"<\s*(TRUE|FALSE|NULL|VOID)\s*/>", re.I), lambda m: m.group(1).lower()),
    (re.compile(r"<\s*br\s*/?>", re.I), lambda m: "\n"),
    (re.compile(r"<\s*/?\s*p\s*/?>", re.I), lambda m: "\n\n"),
    (re.compile(r"<\s*li\s*>", re.I), lambda m: "\n- "),
    (re.compile(r"<\s*/?\s*(ul|ol|dl)\s*>", re.I), lambda m: "\n"),
    (re.compile(r"<\s*dt\s*>", re.I), lambda m: "\n- "),
    (re.compile(r"<\s*dd\s*>", re.I), lambda m: ": "),
    (re.compile(r"<\s*/?\s*(pre|listing)\s*>", re.I), lambda m: "\n```\n"),
    (re.compile(r"</?[A-Za-z][^<>]*>"), lambda m: ""),
]
_AT = re.compile(r"^@(param|returns?|return|throws|exception|see|since|deprecated|author|version|"
                 r"todo|example)\b\s*", re.M)
_AT_LABEL = {"param": "Parameter", "returns": "Returns", "return": "Returns", "throws": "Throws",
             "exception": "Throws", "see": "See also", "since": "Since", "deprecated": "Deprecated",
             "author": "Author", "version": "Version", "todo": "To do", "example": "Example"}


def _doc_text(raw: str) -> str:
    """Коментар `/** … */` → текст: без зірочок на початку рядків, теги HTML і IDL — словами."""
    lines = [re.sub(r"^\s*\*?[ \t]?", "", ln) for ln in raw.split("\n")]
    text = "\n".join(lines)
    for rx, fn in _DOC_TAGS:
        text = rx.sub(fn, text)
    text = unescape(text)
    out = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip("\n")
        if not block.strip():
            continue
        if block.lstrip().startswith("```"):
            out.append(block.strip())
            continue
        parts = _AT.split(block)
        head = " ".join(parts[0].split())
        if head:
            out.append(head)
        for i in range(1, len(parts), 2):
            body = " ".join(parts[i + 1].split())
            label = _AT_LABEL.get(parts[i], parts[i].title())
            out.append(f"{label}: {body}" if body else f"{label}.")
    return "\n\n".join(out)


def _decl(code: str) -> str:
    return " ".join(code.split())


def _member_name(decl: str, kind: str) -> str:
    d = re.sub(r"\[[^\]]*\]", " ", decl)
    if "(" in d:
        m = re.search(r"([A-Za-z_]\w*)\s*\(", d)
        return m.group(1) if m else d
    if kind == "enum":
        return d.split("=")[0].strip()
    if kind == "constants":
        m = re.search(r"([A-Za-z_]\w*)\s*=", d)
        return m.group(1) if m else d
    words = re.findall(r"[A-Za-z_][\w:]*", d)
    return words[-1].split("::")[-1] if words else d


def idl_markdown(text: str, path: str) -> tuple[str, str]:
    """(назва типу, тіло) файла IDL."""
    module = ".".join(re.findall(r"\bmodule\s+(\w+)", text))
    top_doc, top_decl, kind, name = "", "", "", ""
    members: list[tuple[str, str]] = []
    module_docs: list[str] = []
    pending_doc, buf, depth = "", [], 0
    for m in _TOKENS.finditer(text):
        tok = m.group(0)
        if m.group(1) is not None:
            pending_doc = m.group(1)
            continue
        if tok.startswith(("/*", "//")) or (tok.strip().startswith("#") and "\n" not in tok.strip()):
            continue
        if tok == "{":
            code = _decl(re.sub(r"^\s*#.*$", "", "".join(buf), flags=re.M))
            hit = re.search(rf"(?:published\s+)?\b({_KINDS})\s+(\w+)", code)
            if hit and not kind:
                kind, name, top_decl, top_doc = hit.group(1), hit.group(2), code, pending_doc
            elif code.startswith("module") and pending_doc:
                # `modules.idl` описує самі модулі: коментар стоїть над `module drawing {}`.
                module_docs.append(_doc_text(pending_doc))
            depth += 1
            buf, pending_doc = [], ""
            continue
        if tok == "}":
            if depth and kind and buf and _decl("".join(buf)) and kind == "enum":
                members.append((_decl("".join(buf)), pending_doc))
            depth -= 1
            buf, pending_doc = [], ""
            continue
        if tok in (";", ","):
            code = _decl(re.sub(r"^\s*#.*$", "", "".join(buf), flags=re.M))
            if tok == "," and not (kind == "enum" and depth >= 1 and code):
                buf.append(tok)
                continue
            if code:
                inside = kind and depth > len(module.split(".")) if module else depth > 0
                hit = re.search(rf"(?:published\s+)?\b({_KINDS})\s+(\w+)", code)
                if not kind and hit:
                    # Тип без тіла: `service Foo : XFoo;`, `typedef long Bar;`, `singleton …;`.
                    kind, name, top_decl, top_doc = hit.group(1), hit.group(2), code, pending_doc
                elif inside and not code.startswith("module"):
                    members.append((code, pending_doc))
            buf, pending_doc = [], ""
            continue
        buf.append(tok)
    qual = ".".join(x for x in (module, name) if x) or path.rsplit("/", 1)[-1]
    parts = []
    if not kind and module_docs:
        parts.append(f"UNO module `{module}`")
        parts += module_docs
    if kind:
        parts.append(f"UNO {kind} `{qual}`" + (f" (module `{module}`)" if module else ""))
    if top_doc:
        parts.append(_doc_text(top_doc))
    if top_decl:
        parts.append(f"```idl\n{top_decl}\n```")
    seen: dict = {}
    for decl, doc in members:
        member = _member_name(decl, kind)
        seen[member] = seen.get(member, 0) + 1
        head = member if seen[member] == 1 else f"{member} ({seen[member]})"
        sec = [f"## {head}"]
        if doc:
            sec.append(_doc_text(doc))
        sec.append(f"```idl\n{decl}{';' if kind != 'enum' else ''}\n```")
        parts.append("\n\n".join(sec))
    return qual, "\n\n".join(p for p in parts if p.strip())


# --- фрагменти фільтрів і типів ---

_NODE = re.compile(r'<node\s+oor:name="([^"]+)"')
_PROP = re.compile(r'<prop\s+oor:name="([^"]+)"[^>]*?(?:/>|>(.*?)</prop>)', re.S)
_VALUE = re.compile(r"<value(?:\s+xml:lang=\"([^\"]+)\")?[^>]*?(?:/>|>(.*?)</value>)", re.S)


def xcu_markdown(text: str, path: str) -> tuple[str, str]:
    m = _NODE.search(text)
    node = m.group(1) if m else path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    rows = []
    props = {}
    for pm in _PROP.finditer(text):
        name, inner = pm.group(1), pm.group(2) or ""
        vals = []
        for vm in _VALUE.finditer(inner):
            lang, val = vm.group(1), unescape(re.sub(r"<[^>]+>", "", vm.group(2) or "")).strip()
            if lang and lang not in ("en-US", "x-default"):
                continue
            if val:
                vals.append(val)
        value = " ".join(vals)
        props[name] = value
        rows.append(f"| {name} | {value.replace('|', chr(92) + '|')} |")
    is_filter = "/filters/" in path or "FilterService" in props or "Flags" in props
    if is_filter:
        flags = props.get("Flags", "").split()
        way = [w for w, f in (("import", "IMPORT"), ("export", "EXPORT")) if f in flags]
        lead = (f"Filter name `{node}` — the name `--convert-to <ext>:{node}` and `--infilter={node}` take."
                f" UI name: {props.get('UIName') or '—'}. Direction: {', '.join(way) or '—'}."
                f" File type: `{props.get('Type') or '—'}`. Document service: "
                f"`{props.get('DocumentService') or '—'}`.")
        title = f"Filter {node}"
    else:
        lead = (f"File type `{node}` (type detection). Extensions: {props.get('Extensions') or '—'}."
                f" Media type: {props.get('MediaType') or '—'}. Preferred filter: "
                f"`{props.get('PreferredFilter') or '—'}`. UI name: {props.get('UIName') or '—'}.")
        title = f"File type {node}"
    table = "| Property | Value |\n| --- | --- |\n" + "\n".join(rows) if rows else ""
    return title, "\n\n".join(x for x in (lead, table) if x)


# --- soffice --help ---

_CSTR = re.compile(r'"((?:[^"\\\n]|\\.)*)"|/\*.*?\*/|//[^\n]*|^[ \t]*#[^\n]*', re.S | re.M)


def cmdline_markdown(text: str) -> tuple[str, str]:
    """Рядкові літерали довідки командного рядка, склеєні в те, що друкує `soffice --help`."""
    pieces = []
    for m in _CSTR.finditer(text):
        s = m.group(1)
        if s is None:
            continue  # коментар чи `#include` — лапки там не текст довідки
        s = s.replace("\\n", "\n").replace("\\t", "    ").replace('\\"', '"').replace("\\\\", "\\")
        pieces.append(s)
    out = "".join(pieces)
    out = re.sub(r" ?%(PRODUCTVERSION|PRODUCTEXTENSION|BUILDID)", "", out)
    out = re.sub(r"%PRODUCTNAME|%CMDNAME", lambda m: "LibreOffice" if "PRODUCT" in m.group(0)
                 else "soffice", out)
    lines, sections, cur = out.split("\n"), [], ("Usage", [])
    for ln in lines:
        if re.match(r"^[A-Z][^:\-]{2,60}:\s*$", ln.strip()) and not ln.startswith(" "):
            sections.append(cur)
            cur = (ln.strip().rstrip(":"), [])
        else:
            cur[1].append(ln.rstrip())
    sections.append(cur)
    parts = []
    for head, body in sections:
        txt = "\n".join(body).strip("\n")
        if txt.strip():
            parts.append(f"## {head}\n\n```text\n{txt}\n```")
    return "soffice --help: command line parameters", "\n\n".join(parts)


@register("ghcode-history-lo")
def ghcode_history_lo(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев /repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or not tags:
        raise SystemExit(f"{source['id']}: поле `tags` — об'єкт «тег → версія».")
    roots = [r.strip("/") for r in source.get("roots") or ()]
    include = [re.compile(x) for x in source.get("include") or ()]
    if not roots or not include:
        raise SystemExit(f"{source['id']}: потрібні поля `roots` і `include`.")
    exclude = [re.compile(x) for x in source.get("exclude") or ()]
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    max_file = int(source.get("max_file") or _MAX_FILE)

    seen: dict = {}
    for tag in tags:
        for root in roots:
            url = f"{source['url']}{quote(tag, safe='@')}:{quote(root)}?recursive=1"
            code, data = ctx.fetch(url) if ctx.allowed(url) else ("", b"")
            if code != "200":
                continue  # теки на цьому тезі ще (чи вже) немає
            tree = json.loads(data)
            if tree.get("truncated"):
                raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
            for e in tree.get("tree", []):
                full = f"{root}/{e.get('path', '')}"
                if (e.get("type") == "blob" and 0 < e.get("size", 1) <= max_file
                        and any(r.search(full) for r in include)
                        and not any(r.search(full) for r in exclude)):
                    name = f"{lead}{_markup.slug(full)}-{e['sha'][:8]}"
                    seen.setdefault(name, [full, []])[1].append(tag)

    order = {t: i for i, t in enumerate(tags)}
    items = []
    for name, (path, found) in seen.items():
        found = sorted(set(found), key=order.get)
        where = f"{owner}/{repo}/{quote(found[0], safe='@')}/{quote(path)}"
        raw = f"https://raw.githubusercontent.com/{where}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{where.split('/', 2)[2]}"
        version = ", ".join(dict.fromkeys(str(tags[t]) for t in found))

        def make(path=path, raw=raw, blob=blob, version=version):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            if path.endswith(".idl"):
                title, body = idl_markdown(text, path)
                title = f"UNO API: {title}"
            elif path.endswith(".xcu"):
                title, body = xcu_markdown(text, path)
            elif path.endswith("cmdlinehelp.cxx"):
                title, body = cmdline_markdown(text)
            else:
                title, body = f"{repo}: {path}", f"```text\n{text.rstrip()}\n```"
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла за `include` на жодному з {len(tags)} тегів.")
    return items
