"""Сторінка документації Base UI (`mui/base-ui`) з її вставками → markdown із кодом і таблицями API.

Сайт Base UI збирає сторінку компонента з кількох файлів, а в самій `page.mdx` лишаються лише
теги на їхньому місці:
- демо — `<DemoDialogHero />` з `import { DemoDialogHero } from './demos/hero'`; код лежить у
  `demos/hero/tailwind/index.tsx` (той самий приклад на CSS Modules — у `css-modules/`);
- таблиці API до 1.3 — `<Reference component="Dialog" parts="Root, Trigger" />`: пропси, атрибути
  `data-*` і змінні CSS кожної частини — у `docs/reference/generated/dialog-root.json`;
- таблиці API з 1.4 — `<TypesDialog.Root />` з `import { TypesDialog } from './types'`: ті самі дані
  вже згенеровано в `types.md` поруч зі сторінкою, розділом «### Root».

Без цього сторінка «Dialog» не мала б ні рядка коду прикладів, ні жодного пропса, тобто якраз
того, про що питають. Таблиці стають списками в тому ж вигляді, що й таблиці Radix у цьому ж
примірнику: «Props:» з рядками «`open` (boolean, default: false) — опис», «Data attributes:»,
«CSS variables:», для функцій — «Parameters:» і «Return value:».

`files` — {шлях: sha} файлів тегу, які можуть знадобитися (див. `WANTED`), `fetch(шлях, sha)` —
вміст файла. Вставка, файла якої на тезі немає, лишає назву текстом (демо) або зникає (таблиця).
"""

import hashlib
import json
import posixpath
import re
from html import unescape

# Файли тегу, які вставки можуть узяти: код демо, згенеровані типи, довідка JSON.
WANTED = [re.compile(r"^docs/src/app/.*/demos/.+\.tsx$"),
          re.compile(r"^docs/src/app/.*/types\.md$"),
          re.compile(r"^docs/reference/generated/[^/]+\.json$")]

_IMPORT = re.compile(r"^import\s*\{([\w\s,]+)\}\s*from\s*['\"](\.[^'\"]+)['\"];?[ \t]*$", re.M)
_TAG = re.compile(r"^[ \t]*<(\w+)(?:\.(\w+))?((?:\s+\w+)*)\s*/>[ \t]*$", re.M)
_REFERENCE = re.compile(r"^[ \t]*<Reference\b((?:[^<>\"]|\"[^\"]*\")*?)/>[ \t]*$", re.M)
_ATTR = re.compile(r"(\w+)=\"([^\"]*)\"")
_SECTION = re.compile(r"^(#{2,3}) (.+?)[ \t]*$", re.M)
_BOLD_LABEL = re.compile(r"^\*\*(.+?):\*\*[ \t]*$", re.M)
_LABEL = re.compile(r"^(?:[\w.]+ )?(?:Props|Parameters|Return Value|Data Attributes|CSS Variables):",
                    re.M)
_VARIANTS = ("tailwind/index.tsx", "css-modules/index.tsx", "index.tsx")


def _kebab(name: str) -> str:
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name).lower()


def _one_line(text) -> str:
    return " ".join(str(text or "").split())


def _row(name: str, bits: list, desc: str) -> str:
    name = name if name.startswith("`") else f"`{name}`"
    return f"- {name}" + (f" ({', '.join(bits)})" if bits else "") + (f" — {desc}" if desc else "")


def _json_block(data: dict, part: str | None) -> list[str]:
    """Довідка JSON однієї частини (1.0–1.3) → опис і списки, з тими самими підписами, що
    `types.md` з 1.4 («Root Props:», «Popup Data Attributes:»), щоб редакції читалися однаково.
    Тип — кодом: без лапок `RefObject<Dialog.Root.Actions | null>` розмітка прийняла б за тег."""
    out = [_one_line(data.get("description"))] if data.get("description") else []
    lead = f"{part} " if part else ""
    for key, head in (("props", f"{lead}Props:"), ("parameters", "Parameters:")):
        rows = []
        for name, p in (data.get(key) or {}).items():
            if not isinstance(p, dict):
                continue
            bits = [f"`{_one_line(p['type'])}`"] if p.get("type") else []
            if p.get("required"):
                bits.append("required")
            if p.get("default") not in (None, "", "undefined"):
                bits.append(f"default: `{_one_line(p['default'])}`")
            rows.append(_row(name, bits, _one_line(p.get("description"))))
        if rows:
            out += ["", head, ""] + rows
    for key, head in (("dataAttributes", f"{lead}Data Attributes:"),
                      ("cssVariables", f"{lead}CSS Variables:")):
        rows = [_row(name, [f"`{_one_line(a['type'])}`"] if a.get("type") else [],
                     _one_line(a.get("description")))
                for name, a in (data.get(key) or {}).items() if isinstance(a, dict)]
        if rows:
            out += ["", head, ""] + rows
    ret = data.get("returnValue")
    if isinstance(ret, dict) and ret.get("type"):
        out += ["", f"Return Value: `{_one_line(ret['type'])}`"
                + (f" — {_one_line(ret['description'])}" if ret.get("description") else "")]
    elif isinstance(ret, str) and ret:
        out += ["", f"Return Value: `{_one_line(ret)}`"]
    return out


def _cell(text: str) -> str:
    text = unescape(text.replace("\\|", "|").replace("&#xA;", " ")).strip()
    return "" if text == "-" else _one_line(text)


def _tables(text: str) -> str:
    """Таблиці markdown `types.md` → списки «- `ім'я` (тип, default: …) — опис»."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        if (lines[i].lstrip().startswith("|") and i + 1 < len(lines)
                and re.match(r"^\s*\|\s*:?-", lines[i + 1])):
            head = [_cell(c).lower() for c in lines[i].strip().strip("|").split("|")]
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [_cell(c) for c in re.split(r"(?<!\\)\|", lines[i].strip().strip("|"))]
                row = dict(zip(head, cells))
                name = cells[0] if cells else ""
                bits = [f"`{row['type'].strip('`')}`" if row.get("type") else ""]
                bits = [b for b in bits if b]
                if row.get("default"):
                    bits.append(f"default: {row['default']}")
                if name:
                    out.append(_row(name, bits, row.get("description", "")))
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return _BOLD_LABEL.sub(r"\1:", "\n".join(out))


def _types_part(md: str, part: str | None) -> str:
    """Розділ `types.md` для `<TypesX.Part />`: «### Part» і його «### Part.State» тощо;
    без частини — усе під «## API Reference»."""
    heads = list(_SECTION.finditer(md))
    chunks = []
    for n, m in enumerate(heads):
        end = heads[n + 1].start() if n + 1 < len(heads) else len(md)
        level, name = len(m.group(1)), m.group(2)
        body = md[m.end():end].strip()
        if level != 3 or body.startswith("Re-export of"):
            continue
        if part is None:
            chunks.append((name, body))
        elif name == part:
            chunks.append(("", body))
        elif name.startswith(part + "."):
            chunks.append((name, body))
    out = []
    for name, body in chunks:
        out.append(f"{name}:\n\n{body}" if name else body)
    return _tables("\n\n".join(out))


def revision(path: str, sha: str, files: dict) -> str:
    """Відбиток редакції сторінки разом із файлами, які вона вставляє. Документ корпусу —
    неповторний вміст файла, а `page.mdx` компонента часто не міняється між мінорними, тоді як
    його `types.md`, демо чи довідка JSON міняються: без цього сторінка 1.6 показувала б пропси
    1.8. Сусідні файли — `types.md` і `demos/` теки сторінки та довідка `docs/reference/generated`,
    чиє ім'я починається з імені теки (`dialog-root.json` для `components/dialog`)."""
    folder = posixpath.dirname(path)
    leaf = posixpath.basename(folder)
    near = sorted(f"{p}:{s}" for p, s in files.items()
                  if p == f"{folder}/types.md" or p.startswith(f"{folder}/demos/")
                  or (p.startswith("docs/reference/generated/")
                      and (posixpath.basename(p) == f"{leaf}.json"
                           or posixpath.basename(p).startswith(f"{leaf}-"))))
    if not near:
        return sha
    return hashlib.sha1("\n".join([sha] + near).encode()).hexdigest()


def expand(text: str, path: str, files: dict, fetch) -> str:
    folder = posixpath.dirname(path)
    imports = {name.strip(): posixpath.normpath(posixpath.join(folder, rel))
               for names, rel in _IMPORT.findall(text) for name in names.split(",") if name.strip()}

    def read(where):
        return fetch(where, files[where]) if where in files else ""

    def tag(m):
        target = imports.get(m.group(1))
        if not target:
            return m.group(0)
        if posixpath.basename(target) == "types":
            md = read(target + ".md")
            part = m.group(2)
            if part is None and m.group(1).startswith("Types"):
                # `<TypesMergeProps />` утиліти — розділ «### mergeProps» її `types.md`.
                own = m.group(1)[5:]
                names = {h.group(2) for h in _SECTION.finditer(md)}
                part = next((n for n in (own[:1].lower() + own[1:], own) if n in names), None)
            body = _types_part(md, part)
            if "hideDescription" in (m.group(3) or "").split():
                # Опис уже стоїть на сторінці її ж словами — лишаються таблиці.
                cut = _LABEL.search(body)
                body = body[cut.start():] if cut else body
            return f"\n{body}\n" if md else ""
        if "/demos/" in target + "/" and m.group(2) is None:
            name = target.split("/demos/", 1)[1]
            code = next((c for c in (read(f"{target}/{v}") for v in _VARIANTS) if c), "") \
                or read(target + ".tsx")
            if not code:
                return f"\nExample `{name}`.\n"
            return f"\nExample `{name}`:\n\n```tsx\n{code.strip()}\n```\n"
        return m.group(0)

    def reference(m):
        attrs = dict(_ATTR.findall(m.group(1)))
        component = attrs.get("component", "")
        parts = [p.strip() for p in attrs.get("parts", "").split(",") if p.strip()]
        out = []
        for part in parts or [None]:
            data = None
            for base in filter(None, (attrs.get("as"), component)):
                where = (f"docs/reference/generated/{_kebab(base)}"
                         + (f"-{_kebab(part)}" if part else "") + ".json")
                raw = read(where)
                if raw:
                    try:
                        data = json.loads(raw)
                    except ValueError:
                        data = None
                    break
            if not isinstance(data, dict):
                continue
            block = _json_block(data, part)
            out.append("\n".join(([f"### {part}", ""] if part else []) + block))
        return "\n" + "\n\n".join(out) + "\n" if out else ""

    text = _REFERENCE.sub(reference, text)
    return _TAG.sub(tag, text)
