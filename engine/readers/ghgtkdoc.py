"""Читач довідника C API, записаного коментарями gtk-doc у коді: розділ на кожну описану функцію, тип і макрос.

`ghcode-history-gtkdoc` — файли `.c` і `.h` з багатьох тегів одного репозиторію разом. Поля ті самі, що в
                          `ghcode-history`: `url` — префікс дерев через API (…/repos/ВЛАСНИК/РЕПО/git/trees/),
                          `tags` — об'єкт «тег → версія» від найновішого, `include` — вирази шляхів, що
                          беруться; необов'язкові `exclude`, `name_prefix` і `max_file` — межа розміру файла в
                          байтах (типово 400 000).

Навіщо. Довідник функцій бібліотеки libvips ніде не лежить текстом: сайт libvips.org/API збирається з коментарів
над функціями в коді C (до 8.16 — засобом gtk-doc, далі — gi-docgen), і сайт віддає лише три останні лінії.
Опис `vips_resize()` стоїть у `libvips/resample/resize.c` коментарем «/** … */», перший рядок якого — ім'я
описаного («vips_resize:»), далі параметри («@in: input image»), порожній рядок і текст. `ghcode-history` поклав би
в корпус увесь файл коду, де цей опис — п'ята частина, а решта — реалізація, якої читач довідника не питає.

Що береться з файла. Лише коментарі gtk-doc: блок «/**», перший рядок якого — ім'я з двокрапкою. Кожен стає
розділом: назва — ім'я («vips_resize()» для функції й макроса з параметрами, «VipsKernel» для типу,
«VipsImage:width» для властивості, назва розділу для блоку «SECTION:»), під нею оголошення блоком коду, коли воно
стоїть одразу під коментарем і називає те саме ім'я, далі перелік параметрів чи значень і текст опису. Файл без
жодного такого коментаря документа не дає.

Розмітка. gtk-doc і gi-docgen пишуть посилання по-своєму, і читачеві вони заважають шукати: «@scale» стає
«`scale`», «%NULL» — «`NULL`», «#VipsKernel» — «`VipsKernel`», «[method@Image.shrink]» — «`Image.shrink()`»,
«[enum@Vips.Kernel.LANCZOS3]» — «`VIPS_KERNEL_LANCZOS3`», «[func@Vips.init]» — «`vips_init()`». Блок коду
«|[ … ]|» стає блоком markdown, рамка «::: seealso» — абзацом «See also:», теги DocBook знімаються, а їхній текст
лишається. Позначки для генератора прив'язок у дужках («(method)», «(out)», «(nullable)») відкидаються.

Документ — неповторна пара «шлях, текст довідника з цього файла». Тому перелік складається вже з прочитаних
файлів: правка самої реалізації нового документа не дає, і в його версії лягають усі теги, де описи у файлі були
саме такими. Файли читаються крізь сховище сирого, тож під час запису документа мережа вдруге не питається.
Адреса в шапці — blob на найновішому з цих тегів.
"""

import hashlib
import json
import re
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register

_MAX_FILE = 400_000
_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")

_BLOCK = re.compile(r"^/\*\*[ \t]*\n((?:[ \t]*\*(?!/)[^\n]*\n)+?)[ \t]*\*+/", re.M)
_HEAD = re.compile(r"^(SECTION\s*:\s*[\w-]+|[A-Za-z_]\w*(?::{1,2}[\w-]+)?)\s*:?\s*((?:\([^)]*\)\s*:?\s*)*)$")
_PARAM = re.compile(r"^@([\w.]+|\.\.\.)\s*:\s*(.*)$")
_ANNOT = re.compile(r"^(?:\([a-z][^)]*\)\s*)+:\s*")
_ADMON = re.compile(r"^:::\s*(\w+)\s*(?:\"([^\"]*)\")?\s*$")
_GI = re.compile(r"\[(\w+)@([\w.:-]+)\]")
_TAG = re.compile(r"</?(?:link|ulink|type|emphasis|para|listitem|itemizedlist|orderedlist|literal|function|"
                  r"informalexample|firstterm|code|filename|command|option)\b[^>]*>")
_CODE_SPLIT = re.compile(r"(`[^`\n]*`)")
_ADMON_TITLE = {"seealso": "See also", "note": "Note", "tip": "Tip", "warning": "Warning", "important": "Important"}


def _snake(name: str) -> str:
    """«ForeignPngFilter» → «FOREIGN_PNG_FILTER»."""
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).upper()


def _gi(m: re.Match) -> str:
    """Посилання gi-docgen звичайним іменем: те, що читач шукає й бачить у коді."""
    kind, target = m.group(1), m.group(2)
    parts = target.split(".")
    ns = "Vips"
    if len(parts) > 1 and parts[0] in ("Vips", "GObject", "GLib", "Gio"):
        ns, parts = parts[0], parts[1:]
    own = "Vips" if ns == "Vips" else ("G" if ns in ("GObject", "GLib", "Gio") else ns)
    rest = ".".join(parts)
    if kind in ("method", "ctor", "vfunc"):
        return f"`{rest}()`"
    if kind == "func":
        if len(parts) == 1:
            return f"`{own.lower()}_{rest}()`" if ns == "Vips" else f"`g_{rest}()`"
        return f"`{rest}()`"
    if kind == "const":
        return f"`{own.upper()}_{rest}`" if ns == "Vips" else f"`G_{rest}`"
    if kind in ("enum", "flags", "error") and len(parts) == 2:
        return f"`{own.upper()}_{_snake(parts[0])}_{parts[1]}`"
    if kind == "id":
        return f"`{target}`"
    return f"`{own}{rest}`"


def _inline(line: str, gtk: bool = True) -> str:
    """Посилання gtk-doc і gi-docgen у рядку тексту; вміст «`…`» не чіпається. Без `gtk` — лише gi-docgen:
    так читаються сторінки посібника, де «@», «%» і «#» — звичайні знаки."""
    out = []
    for piece in _CODE_SPLIT.split(line):
        if piece.startswith("`") and piece.endswith("`") and len(piece) > 1:
            out.append(piece)
            continue
        piece = _GI.sub(_gi, piece)
        if not gtk:
            out.append(piece)
            continue
        piece = _TAG.sub("", piece)
        piece = re.sub(r"(?<![\w`])@(\w+)", r"`\1`", piece)
        piece = re.sub(r"(?<![\w`])%(-?\w+)", r"`\1`", piece)
        piece = re.sub(r"(?<![\w`&])#([A-Za-z_]\w*(?:(?:::?|\.)[\w-]+)?)", r"`\1`", piece)
        out.append(piece)
    return "".join(out)


def _text(lines: list[str], gtk: bool = True) -> str:
    """Тіло коментаря → markdown: блоки коду, рамки gi-docgen, посилання."""
    out, code, admon = [], "", False
    for line in lines:
        bare = line.strip()
        if code:
            if (code == "gtk" and bare.startswith("]|")) or (code == "md" and bare.startswith("```")):
                out.append("```")
                code = ""
            else:
                out.append(line)
            continue
        if gtk and bare.startswith("|["):
            out.append("```c")
            code = "gtk"
            continue
        if bare.startswith("```"):
            out.append(bare if len(bare) > 3 or not gtk else "```c")
            code = "md"
            continue
        if m := _ADMON.match(bare):
            kind = m.group(1).lower()
            title = m.group(2) or _ADMON_TITLE.get(kind, kind.capitalize())
            out += ["", title[:1].upper() + title[1:] + ":", ""]
            admon = True
            continue
        if admon:
            if not bare:
                out.append("")
                continue
            if line.startswith(("    ", "\t")):
                line = line[4:] if line.startswith("    ") else line[1:]
            else:
                admon = False
        out.append(_inline(line, gtk))
    if code:
        out.append("```")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def _declaration(after: str, name: str) -> tuple[str, str]:
    """Оголошення під коментарем, якщо воно про те саме ім'я: (текст, вид) — «fn», «macro», «const» чи «»."""
    chunk = after.lstrip("\n")
    if chunk.startswith("#define") or chunk.startswith("# define"):
        lines = []
        for line in chunk.split("\n"):
            lines.append(line)
            if not line.rstrip().endswith("\\"):
                break
        text = "\n".join(lines)
        m = re.match(r"#\s*define\s+(\w+)(\()?", text)
        if m and m.group(1) == name:
            return text, "macro" if m.group(2) else "const"
        return "", ""
    end = re.search(r"^\{|;[ \t]*$|^[ \t]*$", chunk, re.M)
    head = chunk[:end.start()].rstrip() if end else ""
    if head and len(head) < 1500 and re.search(rf"\b{re.escape(name)}\s*\(", head) and "/*" not in head:
        return " ".join(head.split()).replace("( ", "(") + ";", "fn"
    return "", ""


def gtkdoc_to_markdown(text: str) -> str:
    """Код C → довідник: розділ на кожен коментар gtk-doc; порожній рядок, коли їх немає."""
    text = text.replace("\r\n", "\n")
    parts = []
    for block in _BLOCK.finditer(text):
        lines = [re.sub(r"^[ \t]*\*(?: |\t|$)", "", ln) for ln in block.group(1).split("\n")[:-1]]
        lines = [ln.rstrip() for ln in lines]
        if not lines or not (m := _HEAD.match(lines[0].strip())):
            continue
        name = m.group(1)
        section = name.startswith("SECTION")
        if section:
            name = name.split(":", 1)[1].strip()
        params, i = [], 1
        while i < len(lines):
            line = lines[i]
            if p := _PARAM.match(line.strip()):
                params.append([p.group(1), _ANNOT.sub("", p.group(2)).strip()])
            elif line.strip() and params and (line.startswith((" ", "\t")) or section):
                params[-1][1] = (params[-1][1] + " " + line.strip()).strip()
            else:
                break
            i += 1
        body = _text(lines[i:])
        decl, kind = _declaration(text[block.end():].split("\n", 1)[1] if "\n" in text[block.end():] else "", name)
        out = []
        if section:
            meta = dict(params)
            title = _inline(meta.get("title") or name)
            out.append(f"## {title}")
            if meta.get("short_description"):
                out.append(_inline(meta["short_description"]).strip().capitalize() + ".")
            if meta.get("include"):
                out.append(f"Include: `{meta['include']}`")
            if meta.get("see_also"):
                out.append("See also: " + _inline(meta["see_also"]))
        else:
            is_fn = kind in ("fn", "macro") or (not kind and re.match(r"[a-z]\w*_\w+$", name) is not None)
            out.append(f"## {name}{'()' if is_fn else ''}")
            if decl:
                out.append(f"```c\n{decl}\n```")
            if params:
                label = "Parameters" if is_fn else "Members"
                out.append(label + ":\n\n" + "\n".join(
                    f"- `{n}`" + (f": {_inline(d)}" if d else "") for n, d in params))
        if body:
            out.append(body)
        if len(out) > 1:
            parts.append("\n\n".join(out))
    return "\n\n".join(parts) + ("\n" if parts else "")


@register("ghcode-history-gtkdoc")
def ghcode_history_gtkdoc(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев /repos/ВЛАСНИК/РЕПО/git/trees/.")
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

    # blob → [шлях, [теги]]: той самий вміст файла на багатьох тегах читається раз
    blobs: dict = {}
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
                blobs.setdefault((path, entry["sha"]), []).append(tag)

    def raw_of(path: str, tag: str) -> str:
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{quote(tag, safe='@')}/{quote(path)}"

    # ім'я документа → [шлях, [теги]]: файли з тим самим текстом довідника — один документ
    order = {t: i for i, t in enumerate(tags)}
    seen: dict = {}
    for n, ((path, _sha), found) in enumerate(blobs.items(), 1):
        raw = raw_of(path, found[0])
        if not ctx.allowed(raw):
            continue
        body = gtkdoc_to_markdown(ctx.text(raw))
        if n % 250 == 0:
            print(f"  {source['id']}: прочитано {n} із {len(blobs)} файлів, з описами — {len(seen)}", flush=True)
        if not body:
            continue
        digest = hashlib.sha1(body.encode("utf-8")).hexdigest()[:8]
        seen.setdefault(f"{lead}{_markup.slug(path)}-{digest}", [path, []])[1].extend(found)

    items = []
    for name, (path, found) in seen.items():
        found = sorted(set(found), key=order.get)
        raw = raw_of(path, found[0])
        blob = f"https://github.com/{owner}/{repo}/blob/{quote(found[0], safe='@')}/{quote(path)}"
        version = ", ".join(dict.fromkeys(tags[t] for t in found))

        def make(path=path, raw=raw, blob=blob, version=version):
            body = gtkdoc_to_markdown(ctx.text(raw))
            title = f"{repo}: {path}"
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла з коментарями gtk-doc на жодному з {len(tags)} тегів.")
    return items
