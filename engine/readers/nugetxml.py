"""Читач NuGet: довідник API з XML-документації пакетів.

`nuget-xmldoc` — пакет NuGet (.nupkg — це zip) несе поруч зі збірками файли XML з
коментарями документації: тими самими, з яких learn.microsoft.com генерує сторінки
довідника API (dotnet/api/…?view=aspnetcore-8.0). Документом стає кожен тип: опис, а
далі розділ на кожен член — конструктор, властивість, метод, поле, подію — з
параметрами, значенням, винятками, зауваженнями й прикладами.

Поля джерела:
- `url` — адреса .nupkg на api.nuget.org (v3-flatcontainer); `packages` — замість неї
  перелік «ідентифікатор/версія», коли тип набору розкиданий по багатьох пакетах (ASP.NET
  Core 1.x–2.x, класичний ASP.NET); адреси тоді дозволяє `within`;
- `assemblies` — вирази імен збірок, які беруться (без поля — усі), `exclude` — які ні:
  у пакеті-довіднику спільного фреймворку лежать і збірки інших продуктів;
- `view` — назва версії довідника на сайті для посилань («aspnetcore-10.0»);
- `name_prefix` — перед іменем документа; `version` — у шапку;
- `folder` — каталог XML у пакеті, коли він не ref/ і не lib/ (еталонні збірки .NET
  Framework: «build/.NETFramework/v4.8.1/»);
- `exclude_types` — вираз повного імені типу, що не береться: таблиці рядків ресурсів
  (Resources, CoreStrings) і простори імен `.Internal`, публічні лише формально.

Каталог збірок у пакеті обирається сам: `ref/` переважає `lib/`, бо це контракт, який
бачить код; серед цільових платформ — найновіша .NET, потім .NET Standard, потім .NET
Framework. Тип з тим самим повним ім'ям у різних версіях дає те саме ім'я документа,
тож незмінний опис члена сусідніх версій зливається в один фрагмент.
"""

import io
import re
import xml.etree.ElementTree as ET
import zipfile

from engine.readers import Item, _markup, register

_FLAT = "https://api.nuget.org/v3-flatcontainer/"
_TFM = re.compile(r"^(ref|lib)/([^/]+)/([^/]+)\.xml$", re.I)
_KINDS = {"M": "method", "P": "property", "F": "field", "E": "event"}
_ORDER = {"constructor": 0, "property": 1, "method": 2, "operator": 3, "event": 4, "field": 5}
_SPACE = re.compile(r"\s+")

# Розібраний набір останнього джерела: (id джерела) → дані. Оновлювач робить документи
# джерела одне за одним одразу після переліку, тож досить пам'ятати одне джерело —
# машина не тримає в пам'яті довідники всіх версій разом.
_CACHE: dict = {}


def _tfm_rank(folder: str, tfm: str) -> tuple:
    """Чим більше, тим краще: ref над lib, далі .NET 5+ (за номером), .NET Core App,
    .NET Standard, .NET Framework (net45, net461…)."""
    t = tfm.lower()
    m = re.fullmatch(r"net(\d+)\.(\d+)(?:-[\w.]+)?", t)
    if m:
        fam, num = 4, (int(m.group(1)), int(m.group(2)))
    elif t.startswith("netcoreapp"):
        fam, num = 3, tuple(int(x) for x in re.findall(r"\d+", t))
    elif t.startswith("netstandard"):
        fam, num = 2, tuple(int(x) for x in re.findall(r"\d+", t))
    elif re.fullmatch(r"net\d+", t):
        fam, num = 1, (int(t[3:].ljust(3, "0")),)
    else:
        fam, num = 0, ()
    return (folder.lower() == "ref", fam, num)


def _xml_files(data: bytes, where: str, folder: str = "") -> list[tuple[str, bytes]]:
    """Файли XML документації з найкращого каталогу пакета: [(збірка, вміст)]. Збірка
    береться лише та, поруч із якою в тому ж каталозі є .dll — інакше це не документація,
    а, скажімо, файл ресурсів."""
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        raise SystemExit(f"{where}: не zip — пакет не прочитався.")
    names = z.namelist()
    if folder:
        # Каталог, названий у джерелі: пакети еталонних збірок .NET Framework кладуть їх у
        # build/.NETFramework/v4.8.1/, поза ref/ і lib/.
        return [(n[len(folder):-4], z.read(n)) for n in sorted(names)
                if n.startswith(folder) and n.endswith(".xml") and "/" not in n[len(folder):]]
    dlls = {n.lower()[:-4] for n in names if n.lower().endswith(".dll")}
    groups: dict = {}
    for n in names:
        m = _TFM.match(n)
        if m and n.lower()[:-4] in dlls:
            groups.setdefault((m.group(1), m.group(2)), []).append((m.group(3), n))
    if not groups:
        return []
    best = max(groups, key=lambda k: _tfm_rank(*k))
    return [(asm, z.read(n)) for asm, n in sorted(groups[best])]


def _strip_generic(name: str) -> str:
    return re.sub(r"`+\d+", "", name)


def _split_member(mid: str) -> tuple[str, str, str]:
    """«M:Ns.Type.Method(System.String)~Ret» → («M», «Ns.Type.Method», «System.String»)."""
    kind, _, rest = mid.partition(":")
    rest = rest.split("~", 1)[0]
    name, _, params = rest.partition("(")
    return kind, name, params.rstrip(")")


def _owner(name: str) -> tuple[str, str]:
    """Ім'я члена → (тип, коротке ім'я). Крапку всередині {…} параметрів узагальнення
    не рахуємо: членів ідентифікатор без параметрів, тож досить останньої крапки."""
    head, _, tail = name.rpartition(".")
    return head, tail


def _short_type(t: str) -> str:
    """Тип параметра в підписі так, як його пише сайт: без простору імен, узагальнення
    кутовими дужками («IEnumerable<Int32>»), «``0» — параметр методу."""
    t = re.sub(r"``(\d+)", r"TMethod\1", t)
    t = re.sub(r"`(\d+)", r"T\1", t)
    t = t.replace("{", "<").replace("}", ">").replace("@", "&")
    return re.sub(r"(?:[\w]+\.)+(\w+)", r"\1", t)


def _params(params: str) -> list[str]:
    out, depth, cur = [], 0, ""
    for ch in params:
        if ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur:
        out.append(cur)
    return [_short_type(p) for p in out]


def _cref(cref: str) -> str:
    """Посилання <see cref> як ім'я в тексті: тип — коротким ім'ям, член — «Тип.Член»."""
    kind, _, rest = cref.partition(":")
    if not rest:
        rest = kind
    rest = rest.split("(", 1)[0]
    parts = _strip_generic(rest).split(".")
    if kind in ("T", "N") or len(parts) < 2:
        return parts[-1]
    member = parts[-1].replace("#ctor", parts[-2])
    return f"{parts[-2]}.{member}"


def _inline(el) -> str:
    """Текст елемента документації з вкладеними <see>, <c>, <paramref> тощо. Абзаци
    (<para>) і списки дають порожні рядки й пункти, код (<code>) — огорожу."""
    out = [el.text or ""]
    for ch in el:
        tag = ch.tag
        if tag == "seealso":
            pass
        elif tag == "see":
            if ch.get("langword"):
                out.append(f"`{ch.get('langword')}`")
            elif ch.get("cref"):
                label = "".join(ch.itertext()).strip()
                out.append(label or f"`{_cref(ch.get('cref'))}`")
            elif ch.get("href"):
                label = "".join(ch.itertext()).strip()
                out.append(label or ch.get("href"))
        elif tag in ("paramref", "typeparamref"):
            out.append(f"`{ch.get('name', '')}`")
        elif tag == "c":
            out.append(f"`{''.join(ch.itertext()).strip()}`")
        elif tag == "code":
            code = "\n".join(ln.rstrip() for ln in "".join(ch.itertext()).strip("\n").split("\n"))
            out.append("\n\n```" + (ch.get("language") or "") + "\n" + _dedent(code) + "\n```\n\n")
        elif tag == "para":
            out.append("\n\n" + _inline(ch).strip() + "\n\n")
        elif tag == "br":
            out.append("\n")
        elif tag == "list":
            items = []
            for it in ch:
                term = it.find("term")
                desc = it.find("description")
                text = " — ".join(x for x in ((_inline(term).strip() if term is not None else ""),
                                              (_inline(desc).strip() if desc is not None else ""))
                                  if x) or _inline(it).strip()
                if text:
                    items.append("- " + _SPACE.sub(" ", text))
            out.append("\n\n" + "\n".join(items) + "\n\n")
        elif tag == "inheritdoc":
            src = ch.get("cref")
            out.append(f"(Documentation inherited from `{_cref(src)}`.)" if src
                       else "(Documentation inherited from the base member.)")
        else:
            out.append(_inline(ch))
        out.append(ch.tail or "")
    return _normalize("".join(out))


def _dedent(code: str) -> str:
    import textwrap
    return textwrap.dedent(code)


def _normalize(text: str) -> str:
    """Пробіли всередині абзаців — одним; абзаци, пункти списку й код — як були."""
    out = []
    for part in re.split(r"(\n```[^\n]*\n[\s\S]*?\n```\n)", text):
        if part.startswith("\n```"):
            out.append(part.strip("\n"))
            continue
        for para in re.split(r"\n\s*\n", part):
            merged: list[str] = []
            for ln in para.split("\n"):
                ln = _SPACE.sub(" ", ln).strip()
                if not ln:
                    continue
                if ln.startswith("- ") or not merged:
                    merged.append(ln)
                else:
                    merged[-1] += " " + ln
            if merged:
                out.append("\n".join(merged))
    return "\n\n".join(out)


def _body_of(el, skip=("summary",)) -> list[str]:
    """Блоки документації члена після опису: параметри, значення, винятки, зауваження,
    приклади — у порядку сторінки сайту."""
    lines = []
    tparams = [(p.get("name", ""), _inline(p)) for p in el.findall("typeparam")]
    params = [(p.get("name", ""), _inline(p)) for p in el.findall("param")]
    if tparams:
        lines += ["Type parameters:", *[f"- `{n}` — {d}" if d else f"- `{n}`" for n, d in tparams], ""]
    if params:
        lines += ["Parameters:", *[f"- `{n}` — {d}" if d else f"- `{n}`" for n, d in params], ""]
    for tag, label in (("returns", "Returns"), ("value", "Value")):
        x = el.find(tag)
        if x is not None and _inline(x):
            lines += [f"{label}: {_inline(x)}", ""]
    exc = el.findall("exception")
    if exc:
        lines += ["Exceptions:"]
        for x in exc:
            d = _inline(x)
            lines.append(f"- `{_cref(x.get('cref', ''))}`" + (f" — {d}" if d else ""))
        lines.append("")
    for tag, label in (("remarks", "Remarks"), ("example", "Example")):
        x = el.find(tag)
        if x is not None and _inline(x):
            lines += [f"{label}:", "", _inline(x), ""]
    inherited = el.find("inheritdoc")
    if inherited is not None and el.find("summary") is None:
        src = inherited.get("cref")
        lines += [f"(Documentation inherited from `{_cref(src)}`.)" if src
                  else "(Documentation inherited from the base member.)", ""]
    return lines


def _parse(source: dict, ctx) -> dict:
    """{повне ім'я типу: {"asm": збірка, "type": XML типу чи "", "members": [XML]}}."""
    if source["id"] in _CACHE:
        return _CACHE[source["id"]]
    _CACHE.clear()
    include = [re.compile(x) for x in source.get("assemblies") or [".*"]]
    exclude = [re.compile(x) for x in source.get("exclude") or []]
    urls = [source["url"]] if not source.get("packages") else [
        f"{_FLAT}{p.split('/')[0].lower()}/{p.split('/')[1].lower()}/"
        f"{p.split('/')[0].lower()}.{p.split('/')[1].lower()}.nupkg" for p in source["packages"]]
    types: dict = {}
    for url in urls:
        if not ctx.allowed(url):
            continue
        code, data = ctx.fetch(url)
        if code != "200":
            if source.get("packages"):
                continue
            raise SystemExit(f"{url}: {code}")
        for asm, raw in _xml_files(data, url, source.get("folder", "")):
            if not any(r.fullmatch(asm) for r in include) or any(r.fullmatch(asm) for r in exclude):
                continue
            try:
                root = ET.fromstring(raw)
            except ET.ParseError as e:
                print(f"  {url}: {asm}.xml не розібрався ({e}) — пропускаю", flush=True)
                continue
            for mem in root.iter("member"):
                mid = mem.get("name", "")
                kind, name, _ = _split_member(mid)
                if kind == "T":
                    entry = types.setdefault(name, {"asm": asm, "type": "", "members": []})
                    entry["type"] = ET.tostring(mem, encoding="unicode")
                elif kind in _KINDS:
                    owner, _ = _owner(name)
                    entry = types.setdefault(owner, {"asm": asm, "type": "", "members": []})
                    entry["members"].append(ET.tostring(mem, encoding="unicode"))
    _CACHE[source["id"]] = types
    return types


def _type_title(full: str) -> str:
    return re.sub(r"`(\d+)", lambda m: "<" + ", ".join(
        ["T"] if m.group(1) == "1" else [f"T{i + 1}" for i in range(int(m.group(1)))]) + ">", full)


def _member_heading(mid: str, type_short: str) -> tuple[int, str]:
    kind, name, params = _split_member(mid)
    _, short = _owner(name)
    if short in ("#ctor", "#cctor"):
        what, short = "constructor", type_short
    elif short.startswith("op_"):
        what = "operator"
        short = short[3:]
    else:
        what = _KINDS[kind]
    short = _strip_generic(short)
    if kind == "M" or (kind == "P" and params):
        sig = f"{short}({', '.join(_params(params))})" if kind == "M" else f"{short}[{', '.join(_params(params))}]"
    else:
        sig = short
    return _ORDER.get(what, 9), f"{sig} {what}"


@register("nuget-xmldoc")
def nuget_xmldoc(source: dict, ctx) -> list[Item]:
    view = source.get("view", "")
    prefix = source.get("name_prefix", "api")
    drop = re.compile(source["exclude_types"]) if source.get("exclude_types") else None
    types = _parse(source, ctx)
    if not types:
        raise SystemExit(f"{source['url']}: у пакеті немає XML-документації потрібних збірок.")
    items = []
    for full in sorted(types):
        if not full or (drop and drop.search(full)):
            continue
        name = f"{prefix}-{_markup.slug(full.replace('`', '-'))}"
        url = ("https://learn.microsoft.com/en-us/dotnet/api/"
               + full.lower().replace("`", "-") + (f"?view={view}" if view else ""))

        def make(full=full, url=url):
            entry = _parse(source, ctx)[full]
            ns, _, short = full.rpartition(".")
            short_shown = _strip_generic(short)
            title = _type_title(full)
            lines = [f"Namespace: {ns} · Assembly: {entry['asm']}.dll", ""]
            if entry["type"]:
                t = ET.fromstring(entry["type"])
                s = t.find("summary")
                if s is not None and _inline(s):
                    lines += [_inline(s), ""]
                lines += _body_of(t)
            sections = []
            for raw in entry["members"]:
                m = ET.fromstring(raw)
                order, heading = _member_heading(m.get("name", ""), short_shown)
                body = []
                s = m.find("summary")
                if s is not None and _inline(s):
                    body += [_inline(s), ""]
                body += _body_of(m)
                sections.append((order, heading, body))
            seen: dict = {}
            for order, heading, body in sorted(sections, key=lambda x: (x[0], x[1])):
                # Перевантаження з тим самим підписом у різних збірках трапляються рідко,
                # але однаковий заголовок склеїв би два розділи в один ключ.
                n = seen.get(heading, 0)
                seen[heading] = n + 1
                lines += [f"## {heading}" + (f" ({n + 1})" if n else ""), "", *body]
            body = _markup.tidy("\n".join(lines), strip=False)
            return _markup.document(title, url, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                          make=make))
    return items
