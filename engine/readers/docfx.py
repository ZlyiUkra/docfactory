"""Читач DocFX: документація learn.microsoft.com з її репозиторію GitHub.

`docfx` — набір сторінок learn.microsoft.com, зібраний з markdown репозиторію
(dotnet/AspNetCore.Docs, dotnet/AspNetDocs). `url` — дерево гілки через API
(…/repos/ВЛАСНИК/РЕПО/git/trees/ГІЛКА?recursive=1), поле `docset` — тека набору в
репозиторії («aspnetcore»), `site` — адреса набору на сайті
(«https://learn.microsoft.com/en-us/aspnet/core/»). Документом стає кожен .md набору,
крім вставок (`includes/`) і прикладів (`samples/`, `snippets/`). Поле `name_prefix`
стає перед іменем документа — щоб сторінки двох наборів одного примірника не ділили ключ.

Версії. DocFX тримає всі версії продукту в одному файлі: блок
«:::moniker range=">= aspnetcore-8.0"» … «:::moniker-end» сайт показує лише у версіях,
що підпадають під вираз, а поле шапки `monikerRange` каже, в яких версіях сторінка є
взагалі. Поле джерела `moniker` («aspnetcore-8.0») розгортає кожну сторінку так, як сайт
показує її з `?view=aspnetcore-8.0`: чужі блоки випадають, сторінки поза `monikerRange` у
перелік не потрапляють. Кожна версія — окреме джерело однієї родини (families у
config.json): незмінний розділ сусідніх версій зливається в один фрагмент з версіями
обох, і вектор для нього рахується раз. Без поля `moniker` лишається текст усіх блоків.
Поле `link: "github"` — для версій, яких сайт уже не показує: посилання документа веде
на файл у репозиторії на тому коміті, з якого він узятий.

Розмітка DocFX, яку читач розгортає до тексту:
- «[!INCLUDE[…](шлях)]» — вставка, теж зі своїми блоками версій і вставками;
- «[!code-csharp[](шлях?name=snippet_1)]» і «:::code … source="шлях" id="snippet_1":::» —
  приклад коду з файла репозиторію: фрагмент між позначками «<snippet_1>» … «</snippet_1>»
  чи «#region snippet_1» … «#endregion», рядки `range`, або файл цілком. Шлях
  «~/../ТЕКА/…» веде в залежний репозиторій (поле `repos`: тека → «власник/репо/гілка»):
  так DocFX кладе їх поруч із головним під час збирання сайту;
- «<xref:uid>» і «[текст](xref:uid)» — назва статті з тим самим `uid` у шапці або ім'я
  типу чи члена API, як його показує сайт (`displayProperty=nameWithType` — «Тип.Член»,
  `fullName` — повне ім'я);
- вкладки «# [Visual Studio](#tab/visual-studio)» … «---» — підписи, а не заголовки: як
  заголовки вони різали б статтю на розділи «Visual Studio» і «.NET CLI»;
- «:::zone pivot="…"» — кожен варіант з підписом; «:::image …:::», «[!div …]», «[!VIDEO …]»
  випадають; «> [!NOTE]» стає «> Note:».
"""

import posixpath
import re
import textwrap
from urllib.parse import unquote, urlsplit

from engine.readers import Item, _markup, register

_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/([^/]+)$")
_MONIKER = re.compile(r'^[ \t]*:::[ \t]*moniker[ \t]+range="([^"]*)"[ \t]*$'
                      r"|^[ \t]*:::[ \t]*moniker-end[ \t]*$", re.M)
_TERM = re.compile(r"(>=|<=|>|<|=)?\s*([a-z][a-z-]*?)-(\d+(?:\.\d+)*)")
_INCLUDE = re.compile(r"\[!INCLUDE\s*\[[^\]]*\]\(\s*<?([^)\s>]+)>?[^)]*\)\]", re.I)
_CODE_REF = re.compile(r"\[!code-([\w+#.-]+)\s*\[[^\]]*\]\(\s*<?([^)\s>]+)>?[^)]*\)\]")
_CODE_TRIPLE = re.compile(r":::code\s+(.*?):::", re.S)
_ATTR = re.compile(r'([\w-]+)="([^"]*)"')
_XREF_TAG = re.compile(r"<xref:([^>\s]+)>")
# Текст посилання сам буває з дужками в коді: «[`[JSImport]` attribute](xref:…)».
_XREF_LINK = re.compile(r"\[((?:`[^`\n]*`|\[[^\]\n]*\]|[^\]`\n])*)\]\(<?xref:([^)\s>]+)>?\)")
_TAB = re.compile(r"^#{1,6}\s*\[([^\]]+)\]\(#tab/[^)]*\)\s*$")
_ZONE = re.compile(r'^\s*:::\s*zone\s+(pivot|target)="([^"]*)"\s*:?:?:?\s*$')
_ZONE_END = re.compile(r"^\s*:::\s*zone-end\s*:?:?:?\s*$")
_IMAGE_COMPLEX = re.compile(r'^\s*:::image\s+type="complex".*?:::image-end:::\s*$', re.S | re.M)
_TRIPLE_LINE = re.compile(r"^\s*:::[\w-]+(?:\s.*)?:::\s*$|^\s*:::[\w-]+:::\s*$")
_NO_LOC = re.compile(r':::no-loc\s+text="((?:\\.|[^"\\])*)":::')
_ALERT = re.compile(r"\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", re.I)
_DIV = re.compile(r"^\s*>?\s*\[!(?:div|VIDEO)\b[^\]]*\]\s*$", re.I)
_FENCE = re.compile(r"^\s*(```+|~~~+)")
_HR = re.compile(r"^\s*-{3,}\s*$")
_PIVOT = re.compile(r"^\s*-\s+id:\s*(\S+)\s*\n\s+title:\s*(.+?)\s*$", re.M)
# Позначка фрагмента в коментарі будь-якої мови прикладу: «// <snippet_1>»,
# «<!-- </snippet_1> -->», «@* <snippet_1> *@», «# <snippet_1>». Без коментаря рядок
# «<div>» — це розмітка самого прикладу, і він лишається.
_SNIPPET_MARK = re.compile(r"^\s*(?://|#|<!--|@\*|/\*|'|--|;|\{/\*)\s*</?[\w.-]+>\s*"
                           r"(?:-->|\*@|\*/|\*/\})?\s*$")
_REGION_MARK = re.compile(r"^\s*#\s*(?:end)?region\b.*$", re.I)
# Приклад, узятий файлом цілком, може бути завдовжки в сотні рядків; хвіст за межею
# лишається у файлі, а документ каже, де його шукати.
MAX_CODE_LINES = 400
MAX_DEPTH = 6
_LANG = {"cshtml": "cshtml", "razor": "razor", "csharp": "csharp", "javascript": "javascript",
         "typescript": "typescript", "json": "json", "xml": "xml", "html": "html"}


def _version_key(text: str) -> tuple:
    return tuple(int(x) for x in text.split("."))


def in_range(expr: str, moniker: str) -> bool:
    """Чи показує сайт у версії `moniker` блок з виразом `expr`. Вираз — альтернативи
    через «||», кожна з умов через пробіл («>= aspnetcore-6.0 < aspnetcore-8.0»); умова
    без знака — рівність. Номер без мінорної частини («aspnetcore-9») — те саме, що
    «.0»: так автори іноді пишуть. Умова про інший продукт альтернативу не справджує."""
    product, _, number = moniker.rpartition("-")
    have = _version_key(number)
    have += (0,) * (3 - len(have))
    for alt in expr.split("||"):
        terms = _TERM.findall(alt)
        if not terms:
            continue
        ok = True
        for op, name, num in terms:
            want = _version_key(num)
            want += (0,) * (3 - len(want))
            if name != product:
                ok = False
            elif not {">=": have >= want, "<=": have <= want, ">": have > want,
                      "<": have < want}.get(op, have == want):
                ok = False
        if ok:
            return True
    return False


def _monikers(text: str, moniker: str) -> str:
    """Текст без блоків, яких сайт у цій версії не показує. Блоки DocFX не вкладаються,
    тож досить пройти позначки по черзі."""
    if not moniker:
        return _MONIKER.sub("", text)
    out, pos, keep = [], 0, True
    for m in _MONIKER.finditer(text):
        if keep:
            out.append(text[pos:m.start()])
        keep = in_range(m.group(1), moniker) if m.group(1) is not None else True
        pos = m.end()
    if keep:
        out.append(text[pos:])
    return "".join(out)


def _dedent_block(lines: list[str]) -> list[str]:
    body = textwrap.dedent("\n".join(lines)).split("\n")
    while body and not body[-1].strip():
        body.pop()
    while body and not body[0].strip():
        body.pop(0)
    return body


def _lines_range(lines: list[str], spec: str) -> list[str]:
    """Рядки за переліком DocFX «5-10,12,20-»: з одиниці, кінці включно."""
    out = []
    for part in spec.split(","):
        a, dash, b = part.strip().partition("-")
        if not a.strip().isdigit():
            continue
        start = int(a)
        end = (int(b) if b.strip().isdigit() else len(lines)) if dash else start
        out.extend(lines[start - 1:end])
    return out


def snippet(text: str, name: str = "", rng: str = "", start: str = "", end: str = "") -> list | None:
    """Рядки прикладу коду, як їх вставляє DocFX. `name` — позначка фрагмента (теги в
    коментарі чи #region, без різниці в регістрі; кілька однойменних ділянок
    склеюються), `rng` — рядки, `start`/`end` — межі рядків. Нічого не знайдено — None:
    документ без прикладу кращий за чужий шматок файла."""
    lines = text.replace("\r\n", "\n").split("\n")
    if name:
        n = re.escape(name)
        open_tag = re.compile(r"<\s*" + n + r"\s*>", re.I)
        close_tag = re.compile(r"<\s*/\s*" + n + r"\s*>", re.I)
        region = re.compile(r"^\s*#\s*region\s+" + n + r"\s*$", re.I)
        picked, inside = [], False
        for ln in lines:
            if not inside and open_tag.search(ln) and _SNIPPET_MARK.match(ln):
                inside = True
                continue
            if inside and close_tag.search(ln) and _SNIPPET_MARK.match(ln):
                inside = False
                continue
            if inside:
                picked.append(ln)
        if not picked:
            depth, inside = 0, False
            for ln in lines:
                if not inside:
                    if region.match(ln):
                        inside, depth = True, 1
                    continue
                if re.match(r"^\s*#\s*region\b", ln, re.I):
                    depth += 1
                elif re.match(r"^\s*#\s*endregion\b", ln, re.I):
                    depth -= 1
                    if depth == 0:
                        inside = False
                        continue
                picked.append(ln)
        if not picked:
            return None
        lines = picked
    elif rng:
        lines = _lines_range(lines, rng)
    elif start.isdigit():
        lines = lines[int(start) - 1:int(end) if end.isdigit() else len(lines)]
    lines = [ln for ln in lines if not (_SNIPPET_MARK.match(ln) or _REGION_MARK.match(ln))]
    body = _dedent_block(lines)
    return body or None


def _strip_front(text: str) -> str:
    return _markup.front_matter(text)[1]


def _drop_comments(text: str) -> str:
    """Текст без коментарів HTML поза огорожами коду. Прибрати їх треба до вставок:
    у коментарі вставки not-latest-version.md записано, як її вставляти, — разом із
    самою «[!INCLUDE]», і розгорнута вона вставляла себе в себе. Коментар усередині
    прикладу коду — частина прикладу і лишається."""
    out, fence, comment = [], "", False
    for ln in text.split("\n"):
        fm = _FENCE.match(ln)
        if fence and not comment:
            out.append(ln)
            if fm and not ln.strip()[len(fence):].strip():
                fence = ""
            continue
        if comment:
            if "-->" not in ln:
                continue
            ln, comment = ln.split("-->", 1)[1], False
        while "<!--" in ln:
            before, _, after = ln.partition("<!--")
            if "-->" in after:
                ln = before + after.split("-->", 1)[1]
            else:
                ln, comment = before, True
        if not fence and fm:
            fence = fm.group(1)
        out.append(ln)
    return "\n".join(out)


@register("docfx")
def docfx(source: dict, ctx) -> list[Item]:
    parts = urlsplit(source["url"])
    m = _TREE.match(parts.path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував адресу дерева гілки "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/ГІЛКА.")
    owner, repo, branch = m.groups()
    docset = source["docset"].strip("/")
    site = source["site"].rstrip("/") + "/"
    moniker = source.get("moniker", "")
    view = f"?view={moniker}" if moniker else ""
    prefix = source.get("name_prefix", "")
    repos = source.get("repos") or {}
    tree = _markup_json(ctx, source["url"])
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")

    def raw_of(path: str) -> str | None:
        """Адреса файла за шляхом від кореня головного репозиторію. Перша тека, названа в
        `repos`, — залежний репозиторій; шлях, що виходить за корінь, — ні до чого."""
        path = posixpath.normpath(path)
        if path.startswith("../") or path == "..":
            return None
        head, _, rest = path.partition("/")
        if head in repos:
            return f"https://raw.githubusercontent.com/{repos[head]}/{rest}"
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

    def resolve(ref: str, base_dir: str) -> str | None:
        ref = unquote(ref.split("?", 1)[0].split("#", 1)[0]).strip()
        if not ref or re.match(r"^[a-z]+://", ref):
            return None
        if ref.startswith("~/"):
            return posixpath.normpath(posixpath.join(docset, ref[2:]))
        if ref.startswith("/"):
            return posixpath.normpath(ref.lstrip("/"))
        return posixpath.normpath(posixpath.join(base_dir, ref))

    def get(path: str) -> str | None:
        url = raw_of(path)
        if url is None or not ctx.allowed(url):
            return None
        code, data = ctx.fetch(url)
        if code != "200":
            return None
        return data.decode("utf-8", errors="replace").replace("\r\n", "\n").lstrip("﻿")

    # Підписи варіантів «:::zone pivot» — з переліку набору; без нього підписом стає id.
    pivots: dict = {}
    pivots_text = get(f"{docset}/zone-pivot-groups.yml") if source.get("pivots", True) else None
    for pm in _PIVOT.finditer(pivots_text or ""):
        pivots[pm.group(1)] = pm.group(2).strip().strip('"')

    paths = []
    for entry in tree["tree"]:
        path = entry.get("path", "")
        if (entry.get("type") != "blob" or not path.startswith(docset + "/")
                or not path.endswith(".md")):
            continue
        segs = path.split("/")
        if any(s in ("includes", "samples", "snippets", "_includes") for s in segs[:-1]):
            continue
        if segs[-1].lower() in ("readme.md", "license.md", "toc.md"):
            continue
        paths.append(path)

    # Шапки всіх сторінок читаються вже під час переліку: `monikerRange` вирішує, чи є
    # сторінка в цій версії, а `uid` → назва потрібні посиланням xref з інших сторінок.
    titles: dict = {}
    pages = []
    for path in paths:
        text = get(path)
        if text is None:
            continue
        meta, _ = _markup.front_matter(text)
        if meta.get("uid"):
            titles[meta["uid"]] = _markup.title_of(meta, path)
        rng = meta.get("monikerRange", "")
        if moniker and rng and not in_range(rng, moniker):
            continue
        pages.append(path)

    def xref(uid: str, display: str = "") -> str:
        uid = unquote(uid)
        query = ""
        if "?" in uid:
            uid, _, query = uid.partition("?")
        uid = uid.split("#", 1)[0].strip('"')
        if uid in titles:
            return titles[uid]
        name = re.sub(r"\(.*\)$", "", uid).rstrip("*")
        name = re.sub(r"`+\d+", "", name)
        segs = name.split(".")
        if "displayProperty=fullName" in query:
            shown = name
        elif "displayProperty=nameWithType" in query:
            shown = ".".join(segs[-2:])
        else:
            shown = segs[-1]
        return f"`{shown}`" if shown else uid

    def code_block(lang: str, ref_path: str | None, attrs: dict) -> str:
        if ref_path is None:
            return ""
        text = get(ref_path)
        if text is None:
            return ""
        lines = snippet(text, attrs.get("name", ""), attrs.get("range", ""),
                        attrs.get("start", ""), attrs.get("end", ""))
        if lines is None:
            return ""
        tail = []
        if len(lines) > MAX_CODE_LINES:
            lines = lines[:MAX_CODE_LINES]
            tail = [f"// … (далі — у файлі {ref_path})"]
        lang = _LANG.get(lang, lang)
        return "\n".join(["", "```" + lang, *lines, *tail, "```", ""])

    def expand(text: str, path: str, depth: int, stack: tuple = ()) -> str:
        """Текст файла `path` (сторінки чи вставки) з розгорнутими версіями, вставками й
        прикладами коду. Шляхи вставки — від її власної теки, як у DocFX."""
        base = posixpath.dirname(path)
        text = _monikers(_drop_comments(text), moniker)
        text = _IMAGE_COMPLEX.sub("", text)

        def include(im):
            target = resolve(im.group(1), base)
            if target is None or depth >= MAX_DEPTH or target in stack:
                return ""
            inner = get(target)
            if inner is None:
                return ""
            return expand(_strip_front(inner).strip("\n"), target, depth + 1, stack + (path,))

        text = _INCLUDE.sub(include, text)

        def code_ref(cm):
            ref = cm.group(2)
            attrs = {}
            if "?" in ref:
                for kv in ref.split("?", 1)[1].split("#", 1)[0].split("&"):
                    k, _, v = kv.partition("=")
                    attrs[k] = unquote(v)
            frag = ref.split("#", 1)[1] if "#" in ref else ""
            lm = re.fullmatch(r"L(\d+)(?:-L(\d+))?", frag)
            if lm:
                attrs["range"] = f"{lm.group(1)}-{lm.group(2) or lm.group(1)}"
            elif frag and not attrs.get("name"):
                attrs["name"] = frag
            return code_block(cm.group(1), resolve(ref, base), attrs)

        def code_triple(cm):
            attrs = dict(_ATTR.findall(cm.group(1)))
            if "source" not in attrs:
                return ""
            if attrs.get("id"):
                attrs["name"] = attrs["id"]
            return code_block(attrs.get("language", ""), resolve(attrs["source"], base), attrs)

        text = _CODE_REF.sub(code_ref, text)
        return _CODE_TRIPLE.sub(code_triple, text)

    def clean(text: str) -> str:
        """Решта розмітки DocFX поза огорожами коду: вкладки, варіанти, зображення,
        позначки на кшталт «[!div]»; посилання xref — назвами."""
        out, fence = [], ""
        for ln in text.split("\n"):
            fm = _FENCE.match(ln)
            if fence:
                out.append(ln)
                if fm and ln.strip().startswith(fence[0] * len(fence)) and not ln.strip()[len(fence):].strip():
                    fence = ""
                continue
            if fm:
                fence = fm.group(1)
                out.append(ln)
                continue
            tm = _TAB.match(ln)
            if tm:
                out.extend(["", f"**{tm.group(1).strip()}**", ""])
                continue
            zm = _ZONE.match(ln)
            if zm:
                if zm.group(1) == "pivot":
                    names = [pivots.get(p.strip(), p.strip()) for p in zm.group(2).split(",")]
                    out.extend(["", f"**{', '.join(names)}**", ""])
                continue
            if _ZONE_END.match(ln) or _HR.match(ln) or _DIV.match(ln):
                continue
            ln = _NO_LOC.sub(lambda nm: nm.group(1).replace('\\"', '"'), ln)
            if _TRIPLE_LINE.match(ln):
                continue
            ln = _XREF_LINK.sub(lambda xm: xm.group(1) or xref(xm.group(2)), ln)
            ln = _XREF_TAG.sub(lambda xm: xref(xm.group(1)), ln)
            ln = _ALERT.sub(lambda am: am.group(1).capitalize() + ":", ln)
            out.append(ln)
        return "\n".join(out)

    items, used = [], set()
    for path in pages:
        rel = path[len(docset) + 1:].removesuffix(".md")
        page = re.sub(r"(^|/)index$", r"\1", rel)
        # Версій, яких сайт уже не показує, адреса з ?view= не відкриє — вона переводить
        # на найновішу; тоді посилання веде на сам файл того коміту.
        url = (f"https://github.com/{owner}/{repo}/blob/{branch}/{path}"
               if source.get("link") == "github" else site + page + view)
        name = _markup.slug(re.sub(r"(^|/)index$", "", rel) or "index")
        if name in used:
            name = _markup.slug(rel)
        used.add(name)
        if prefix:
            name = f"{prefix}-{name}"

        def make(path=path, url=url):
            text = get(path)
            if text is None:
                raise SystemExit(f"{path}: файл не прочитався — документ не записую.")
            meta, rest = _markup.front_matter(text)
            title = _markup.title_of(meta, url)
            body = _markup.markdown_body(clean(expand(rest, path, 0)))
            _markup.require(title, body, url, min_chars=1)
            return _markup.document(title, url, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    if not items:
        raise SystemExit(f"{source['url']}: у наборі {docset} немає жодної сторінки"
                         f"{' для ' + moniker if moniker else ''}.")
    return items


def _markup_json(ctx, url: str) -> dict:
    import json
    try:
        data = json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(data, dict) or not isinstance(data.get("tree"), list):
        raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
    return data
