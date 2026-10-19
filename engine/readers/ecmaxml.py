"""Читач ECMA XML: довідник API .NET з репозиторію dotnet/dotnet-api-docs.

`ecma-xml` — те, з чого learn.microsoft.com збирає сторінки dotnet/api/…: на кожен тип —
файл `xml/<простір імен>/<Тип>.xml` у форматі ECMA XML (mdoc) з підписами всіма мовами,
описом, зауваженнями й прикладами, на кожен простір імен — `xml/ns-<простір>.xml`, а в
`xml/FrameworksIndex/<монікер>.xml` — перелік типів і членів кожної версії («net-8.0»,
«netframework-4.8-pp», «windowsdesktop-9.0»…), з якого сайт пише «Applies to».

Поля джерела:
- `url` — дерево теки xml/ через API: …/repos/ВЛАСНИК/РЕПО/git/trees/КОМІТ:xml?recursive=1
  (повне дерево репозиторію GitHub обрізає — у ньому понад п'ятдесят тисяч записів);
- `languages` — мови прикладів коду, які вставляються з snippets/ (типово лише «csharp»);
  приклади інших мов випадають, щоб той самий приклад не лягав у фрагменти чотири рази;
- `skip_monikers` — вираз монікерів, яких наче немає (передрелізна «-11.0»): тип чи член,
  що є лише в них, не береться, і в «Applies to» вони не пишуться;
- `name_prefix` — перед іменем документа (типово «api», як у `nuget-xmldoc`).

Документ — тип: простір імен і збірки, підпис C#, базовий тип, опис, «Applies to», далі
розділ «Remarks» (його підзаголовки — підрозділами) і «Examples», а за ними — розділ на
кожен член з тим самим заголовком, що дає `nuget-xmldoc` («GetAsync(String) method»): ім'я
документа теж те саме, тож у спільному записі `families` сторінка типу з цього джерела і
опис того самого типу з XML пакетів NuGet займають у видачі одне місце. Зауваження
члена — текстом його розділу: підзаголовки всередині стають підписами, інакше вони
відривали б зауваження від члена. Версії документа — номери .NET з монікерів
(«net-8.0», «windowsdesktop-9.0» → «8.0», «9.0»); монікери .NET Framework і .NET Standard
мають власну нумерацію і пишуться лише в «Applies to».

Розмітка DocFX у markdown зауважень (CDATA): «<xref:…>» — коротким ім'ям, вставки
«[!INCLUDE]» з includes/, приклади «:::code … source="~/snippets/…" id="…":::» і
«[!code-csharp[…](…#Snippet1)]» — кодом з файла того самого коміту, виноски «[!NOTE]» —
підписами. Заглушки «To be added.» випадають.
"""

import json
import posixpath
import re
import textwrap
import xml.etree.ElementTree as ET
from html import unescape
from urllib.parse import unquote, urlsplit

from engine.readers import Item, _markup, docfx, nugetxml, register

_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/([^/:%]+)(?::|%3A)([^?]+)$")
_PLACEHOLDER = re.compile(r"^\s*To be added\.?\s*$", re.I)
_XREF_TAG = re.compile(r"<xref:([^>\s]+)>")
_XREF_LINK = re.compile(r"\[((?:`[^`\n]*`|\[[^\]\n]*\]|[^\]`\n])*)\]\(<?xref:([^)\s>]+)>?\)")
_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(```+|~~~+)")
_LANG = {"csharp": "csharp", "cs": "csharp", "vb": "vb", "visualbasic": "vb", "fsharp": "fsharp",
         "cpp": "cpp", "xaml": "xml", "xml": "xml"}
MAX_DEPTH = 3
_MEMBER_KINDS = {"Constructor": "constructor", "Method": "method", "Property": "property",
                 "Field": "field", "Event": "event", "Operator": "operator"}

# Перелік монікерів останнього джерела: один прогін — одне джерело, тож пам'ятати
# досить його (кілька десятків мегабайтів індексів не тримаються довше, ніж треба).
_CACHE: dict = {}


def _short(uid: str, query: str = "") -> str:
    """Посилання xref як ім'я в тексті — так, як його показує сайт: коротке ім'я,
    «Тип.Член» з displayProperty=nameWithType, повне — з fullName."""
    name = re.sub(r"\(.*\)$", "", unquote(uid)).rstrip("*").replace("%23", "#")
    name = re.sub(r"`+\d+", "", name).replace("+", ".")
    segs = name.split(".")
    if segs and segs[-1] in ("#ctor", "#cctor"):
        segs[-1] = segs[-2] if len(segs) > 1 else "ctor"
    if "displayProperty=fullName" in query:
        shown = ".".join(segs)
    elif "displayProperty=nameWithType" in query and len(segs) > 1:
        shown = ".".join(segs[-2:])
    else:
        shown = segs[-1]
    return f"`{shown}`" if shown else uid


def _xref(uid: str) -> str:
    uid, _, query = uid.partition("?")
    return _short(uid.split("#", 1)[0].strip('"'), query)


def _framework(moniker: str) -> tuple[str, str] | None:
    """Монікер → (продукт, номер): «net-8.0-pp» → (".NET", "8.0")."""
    m = re.fullmatch(r"(net|netframework|netstandard|windowsdesktop|netcore)-([\d.]+)(?:-pp)?", moniker)
    if not m:
        return None
    name = {"net": ".NET", "netcore": ".NET Core", "netframework": ".NET Framework",
            "netstandard": ".NET Standard", "windowsdesktop": "Windows Desktop"}[m.group(1)]
    return name, m.group(2)


def _applies(monikers) -> tuple[str, str]:
    """(рядок «Applies to», версії документа через кому — новіші першими)."""
    by: dict = {}
    for mk in monikers:
        got = _framework(mk)
        if got:
            by.setdefault(got[0], set()).add(got[1])
    key = lambda v: tuple(int(x) for x in v.split(".") if x.isdigit())  # noqa: E731
    order = [".NET", ".NET Core", ".NET Framework", ".NET Standard", "Windows Desktop"]
    line = "; ".join(f"{p} {', '.join(sorted(by[p], key=key))}" for p in order if p in by)
    versions = sorted(by.get(".NET", set()) | by.get("Windows Desktop", set()), key=key, reverse=True)
    return line, ", ".join(versions)


_RX_NS = re.compile(rb'<Namespace\b[^>]*?\bName="([^"]*)"')
_RX_TYPE = re.compile(rb'<Type\b[^>]*?\bId="([^"]*)"')
_RX_MEMBER = re.compile(rb'<Member\b[^>]*?\bId="([^"]*)"')


def _index(ctx, raw: str, files: list[str], skip) -> dict:
    """Монікери типів і просторів імен з FrameworksIndex і члени, що є лише в
    пропущених монікерах: {"types": {id: set}, "ns": {ім'я: set}, "only_skipped": set}.
    Індекси — десятки мегабайтів XML правильної форми, тож вони читаються виразами по
    байтах, а не деревом: дерево всіх членів усіх версій зайняло б гігабайт. Пропущені
    монікери йдуть першими — тоді в пам'яті лише їхні члени, з яких викреслюються ті,
    що знайшлися в інших версіях."""
    types: dict = {}
    spaces: dict = {}
    only: set = set()
    files = sorted(files, key=lambda p: not (skip and skip.search(posixpath.basename(p)[:-4])))
    for path in files:
        moniker = posixpath.basename(path)[:-4]
        if not ctx.allowed(raw + path):
            continue
        code, data = ctx.fetch(raw + path)
        if code != "200":
            continue
        dec = lambda b: unescape(b.decode("utf-8", errors="replace"))  # noqa: E731
        if skip and skip.search(moniker):
            for tm in _RX_TYPE.finditer(data):
                types.setdefault(dec(tm.group(1)), set())
            only.update(dec(mm.group(1)) for mm in _RX_MEMBER.finditer(data))
            continue
        for nm in _RX_NS.finditer(data):
            spaces.setdefault(dec(nm.group(1)), set()).add(moniker)
        for tm in _RX_TYPE.finditer(data):
            types.setdefault(dec(tm.group(1)), set()).add(moniker)
        if only:
            only.difference_update(dec(mm.group(1)) for mm in _RX_MEMBER.finditer(data))
    return {"types": types, "ns": spaces, "only_skipped": only}


def _sig(el, lang: str = "C#") -> str:
    for s in el.findall("TypeSignature") + el.findall("MemberSignature"):
        if s.get("Language") == lang:
            return s.get("Value", "")
    return ""


class _Page:
    """Розгортання markdown зауважень одного файла: вставки й приклади з того самого коміту."""

    def __init__(self, ctx, raw: str, path: str, languages: set):
        self.ctx, self.raw, self.base, self.languages = ctx, raw, posixpath.dirname(path), languages

    def _get(self, path: str) -> str | None:
        url = self.raw + path
        if path.startswith("../") or not self.ctx.allowed(url):
            return None
        code, data = self.ctx.fetch(url)
        if code != "200":
            return None
        return data.decode("utf-8", errors="replace").replace("\r\n", "\n").lstrip("﻿")

    def _resolve(self, ref: str, base: str) -> str:
        ref = unquote(ref.split("?", 1)[0].split("#", 1)[0]).strip()
        if ref.startswith("~/"):
            return posixpath.normpath(ref[2:])
        if ref.startswith("/"):
            return posixpath.normpath(ref.lstrip("/"))
        return posixpath.normpath(posixpath.join(base, ref))

    def _code(self, lang: str, ref: str, base: str, attrs: dict) -> str:
        lang = _LANG.get(lang.lower(), lang.lower())
        if lang not in self.languages:
            return ""
        text = self._get(self._resolve(ref, base))
        if text is None:
            return ""
        lines = docfx.snippet(text, attrs.get("name", ""), attrs.get("range", ""),
                              attrs.get("start", ""), attrs.get("end", ""), "Snippet")
        if not lines:
            return ""
        if len(lines) > docfx.MAX_CODE_LINES:
            lines = lines[:docfx.MAX_CODE_LINES] + [f"// … (далі — у файлі {ref})"]
        return "\n".join(["", "```" + lang, *lines, "```", ""])

    def expand(self, text: str, base: str = None, depth: int = 0) -> str:
        base = self.base if base is None else base
        text = docfx._drop_comments(text)

        def include(m):
            target = self._resolve(m.group(1), base)
            inner = self._get(target) if depth < MAX_DEPTH else None
            if inner is None:
                return ""
            return self.expand(_markup.front_matter(inner)[1].strip("\n"), posixpath.dirname(target),
                               depth + 1)

        def code_ref(m):
            ref = m.group(2)
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
            return self._code(m.group(1), ref, base, attrs)

        def code_triple(m):
            attrs = dict(docfx._ATTR.findall(m.group(1)))
            if "source" not in attrs:
                return ""
            if attrs.get("id"):
                attrs["name"] = attrs["id"]
            return self._code(attrs.get("language", ""), attrs["source"], base, attrs)

        text = docfx._INCLUDE.sub(include, text)
        text = docfx._CODE_REF.sub(code_ref, text)
        return docfx._CODE_TRIPLE.sub(code_triple, text)


def _clean(text: str, headings: str, drop: tuple = ()) -> str:
    """Решта розмітки поза огорожами коду: xref — іменами, виноски — підписами.
    `headings` — що робити з заголовками: «sub» — на рівень нижче (не вище «###»),
    «label» — жирним підписом (зауваження члена лишаються в його розділі). Заголовки
    з `drop` («Remarks», «Examples» — назва самого блоку) випадають."""
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
        hm = _HEADING.match(ln)
        if hm:
            title = hm.group(2).strip()
            if title.lower() in drop:
                continue
            title = _XREF_TAG.sub(lambda xm: _xref(xm.group(1)), title)
            if headings == "label":
                out.extend(["", f"**{title}**", ""])
            else:
                out.extend(["", "#" * max(3, min(6, len(hm.group(1)) + 1)) + " " + title, ""])
            continue
        if docfx._DIV.match(ln) or docfx._TRIPLE_LINE.match(ln):
            continue
        ln = docfx._NO_LOC.sub(lambda nm: nm.group(1).replace('\\"', '"'), ln)
        ln = _XREF_LINK.sub(lambda xm: xm.group(1) or _xref(xm.group(2)), ln)
        ln = _XREF_TAG.sub(lambda xm: _xref(xm.group(1)), ln)
        ln = docfx._ALERT.sub(lambda am: am.group(1).capitalize() + ":", ln)
        out.append(ln)
    return "\n".join(out)


def _block(el, page: _Page, headings: str, drop: tuple = ()) -> str:
    """Текст елемента документації: markdown з <format type="text/markdown"> або
    звичайний XML-коментар (<see>, <para>, <list>, <code>)."""
    if el is None:
        return ""
    fmt = el.find("format")
    if fmt is not None:
        md = textwrap.dedent((fmt.text or "").replace("\r\n", "\n")).strip("\n")
        text = _clean(page.expand(md), headings, drop).strip()
    else:
        text = nugetxml._inline(el).strip()
    return "" if _PLACEHOLDER.match(text) else text


def _member_body(docs, page: _Page) -> list[str]:
    lines = []
    if docs is None:
        return lines
    s = _block(docs.find("summary"), page, "label")
    if s:
        lines += [s, ""]
    for tag, label in (("typeparam", "Type parameters"), ("param", "Parameters")):
        items = []
        for p in docs.findall(tag):
            d = _block(p, page, "label")
            items.append(f"- `{p.get('name', '')}`" + (f" — {d}" if d else ""))
        if items:
            lines += [f"{label}:", *items, ""]
    for tag, label in (("returns", "Returns"), ("value", "Value")):
        d = _block(docs.find(tag), page, "label")
        if d:
            lines += [f"{label}: {d}", ""]
    exc = docs.findall("exception")
    if exc:
        lines.append("Exceptions:")
        for x in exc:
            d = _block(x, page, "label")
            lines.append(f"- `{nugetxml._cref(x.get('cref', ''))}`" + (f" — {d}" if d else ""))
        lines.append("")
    r = _block(docs.find("remarks"), page, "label", ("remarks",))
    if r:
        lines += ["Remarks:", "", r, ""]
    e = _block(docs.find("example"), page, "label", ("examples", "example"))
    if e:
        lines += ["Example:", "", e, ""]
    return lines


@register("ecma-xml")
def ecma_xml(source: dict, ctx) -> list[Item]:
    m = _TREE.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував адресу дерева теки "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/КОМІТ:xml.")
    owner, repo, ref, folder = m.groups()
    folder = unquote(folder).strip("/")
    raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/"
    prefix = source.get("name_prefix", "api")
    languages = set(source.get("languages") or ["csharp"])
    skip = re.compile(source["skip_monikers"]) if source.get("skip_monikers") else None
    try:
        tree = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}) — перелік не складено.")
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")
    paths = [f"{folder}/{e['path']}" for e in tree.get("tree", []) if e.get("type") == "blob"
             and e.get("path", "").endswith(".xml")]
    index_files = [p for p in paths if p.startswith(f"{folder}/FrameworksIndex/")]
    if source["id"] not in _CACHE:
        _CACHE.clear()
        _CACHE[source["id"]] = _index(ctx, raw, index_files, skip)
    idx = _CACHE[source["id"]]

    def make_type(path: str, ns: str, docid: str, url: str):
        def make():
            root = ET.fromstring(page_text(path))
            page = _Page(ctx, raw, path, languages)
            short = nugetxml._strip_generic(docid.rpartition(".")[2])
            title = (root.get("FullName") or nugetxml._type_title(docid)).replace("+", ".")
            asms = []
            for a in root.findall("AssemblyInfo"):
                n = a.findtext("AssemblyName") or ""
                if n and n not in asms:
                    asms.append(n)
            applies, versions = _applies(idx["types"].get("T:" + docid, ()))
            lines = [f"Namespace: {ns} · Assemblies: {', '.join(asms)}", ""]
            sig = _sig(root)
            if sig:
                lines += ["```csharp", sig, "```", ""]
            base = root.findtext("Base/BaseTypeName")
            if base:
                lines += [f"Inheritance: {nugetxml._short_type(base)}", ""]
            docs = root.find("Docs")
            if docs is not None:
                s = _block(docs.find("summary"), page, "sub")
                if s:
                    lines += [s, ""]
                tp = [f"- `{p.get('name', '')}` — {d}" if (d := _block(p, page, "label")) else
                      f"- `{p.get('name', '')}`" for p in docs.findall("typeparam")]
                if tp:
                    lines += ["Type parameters:", *tp, ""]
            if applies:
                lines += [f"Applies to: {applies}", ""]
            if docs is not None:
                r = _block(docs.find("remarks"), page, "sub", ("remarks",))
                if r:
                    lines += ["## Remarks", "", r, ""]
                e = _block(docs.find("example"), page, "sub", ("examples", "example"))
                if e:
                    lines += ["## Examples", "", e, ""]
            sections = []
            members = root.find("Members")
            for grp in (members.findall("MemberGroup") if members is not None else ()):
                body = _member_body(grp.find("Docs"), page)
                if body:
                    mname = grp.get("MemberName", "")
                    head = f"{short} constructors" if mname == ".ctor" else f"{mname} overloads"
                    sections.append((-1, head, body))
            for mem in (members.findall("Member") if members is not None else ()):
                mid = _sig(mem, "DocId")
                if not mid or mid in idx["only_skipped"]:
                    continue
                kind = mem.findtext("MemberType") or ""
                if mid[:1] in nugetxml._KINDS:
                    order, head = nugetxml._member_heading(mid, short)
                else:
                    order, head = 9, f"{mem.get('MemberName', '')} {_MEMBER_KINDS.get(kind, kind.lower())}"
                body = []
                csig = _sig(mem)
                if csig:
                    body += ["```csharp", csig, "```", ""]
                body += _member_body(mem.find("Docs"), page)
                sections.append((order, head, body))
            seen: dict = {}
            for order, head, body in sorted(sections, key=lambda x: (x[0], x[1])):
                n = seen.get(head, 0)
                seen[head] = n + 1
                lines += [f"## {head}" + (f" ({n + 1})" if n else ""), "", *body]
            body = _markup.markdown_body("\n".join(lines))
            return _markup.document(title, url, ctx.stamp, body, versions)
        return make

    def make_ns(path: str, ns: str, url: str):
        def make():
            root = ET.fromstring(page_text(path))
            page = _Page(ctx, raw, path, languages)
            applies, versions = _applies(idx["ns"].get(ns, ()))
            lines = [f"Namespace {ns}.", ""]
            docs = root.find("Docs")
            if docs is not None:
                s = _block(docs.find("summary"), page, "sub")
                if s:
                    lines += [s, ""]
            if applies:
                lines += [f"Applies to: {applies}", ""]
            if docs is not None:
                r = _block(docs.find("remarks"), page, "sub", ("remarks",))
                if r:
                    lines += ["## Remarks", "", r, ""]
            body = _markup.markdown_body("\n".join(lines))
            return _markup.document(f"{ns} Namespace", url, ctx.stamp, body, versions)
        return make

    def page_text(path: str) -> str:
        code, data = ctx.fetch(raw + path)
        if code != "200":
            raise SystemExit(f"{raw + path}: {code}")
        return data.decode("utf-8", errors="replace").lstrip("﻿")

    api = "https://learn.microsoft.com/en-us/dotnet/api/"
    items, used = [], set()
    for path in sorted(paths):
        rel = path[len(folder) + 1:]
        if rel.startswith(("FrameworksIndex/", "SourceLinkInformation/")):
            continue
        leaf = posixpath.basename(rel)[:-4]
        if "/" not in rel and leaf.startswith("ns-"):
            ns = leaf[3:]
            mons = idx["ns"].get(ns)
            if mons is not None and not mons and skip:
                continue
            name = f"{prefix}-ns-{_markup.slug(ns)}"
            items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                              make=make_ns(path, ns, api + ns.lower())))
            continue
        # Ім'я типу — з DocId, як його пише XML пакетів: «System.Collections.Generic.List`1»,
        # вкладений — через крапку. Файл його не несе (List`1.xml, Environment+SpecialFolder.xml),
        # тож id береться з назви файла й теки так само, як його будує mdoc.
        space = posixpath.dirname(rel)
        docid = f"{space}.{leaf.replace('+', '.')}" if space else leaf.replace("+", ".")
        mons = idx["types"].get("T:" + docid)
        if mons is not None and not mons:
            continue  # є лише в пропущених монікерах (передреліз)
        name = f"{prefix}-{_markup.slug(docid.replace('`', '-'))}"
        if name in used:
            continue
        used.add(name)
        url = api + docid.lower().replace("`", "-")
        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make_type(path, space, docid, url)))
    if not items:
        raise SystemExit(f"{source['url']}: у теці {folder} немає жодного типу.")
    return items
