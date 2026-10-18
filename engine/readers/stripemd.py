"""Читач документації docs.stripe.com: сторінки з варіантами й приклади коду кількома мовами.

`stripe-md` — `url` — sitemap.xml сайту; сторінкою стає кожна адреса з нього всередині `within`,
              шлях якої підходить під `match` (вираз, типово будь-який) і не підходить під жоден
              з `exclude`. Текст — markdown-двійник сторінки (та сама адреса з «.md»).
              `langs` — мови прикладів коду в порядку, перша — основна (`["node", "python"]`):
              сторінка, де є серверний код, читається з `?lang=` кожної мови, і в один документ
              лягає текст основної мови, а під ним у кожному розділі — блоки коду інших мов з
              підписом («Python:»). Розділи, яких в основній мові немає («#### Python» з
              установкою пакета), стають на своє місце після попереднього спільного розділу.
              Сторінка без серверного коду читається один раз. `variants: true` — сторінку, що
              є лише переліком варіантів («This article has multiple variants»), заміняють її
              варіанти: кожен — окремий документ з назвою «Сторінка (Checkout: Stripe-hosted
              page)». `path_version` — вираз із групами `d` (дата) і, необов'язково, `n` (назва
              випуску): документ дістає версію API «api-2025-01-27» з адреси журналу змін.

Навіщо. Stripe показує на одній сторінці приклади сервера мовою, яку вибрав читач (curl і Ruby
типово), а markdown-двійник віддає одну мову за запитом `?lang=`. Окремий документ на кожну мову
повторив би текст сторінки вісім разів і в індексі, і у векторах; тут текст один, а код — усіма
мовами. Інтеграції, що різняться не мовою, а самим шляхом (Checkout чи Elements, iOS чи Android),
сайт розводить на варіанти з власними адресами, і сторінка за основною адресою — лише їх перелік.

Чому окремий модуль: розмітка варіантів і мов — властивість саме цього сайту.
"""

import difflib
import re
from urllib.parse import parse_qsl, urlsplit

from engine.readers import Item, _markup, register

_LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")
_VARIANTS = "This article has multiple variants"
_VARIANT_ITEM = re.compile(r"^(\s*)-\s+(?:\[([^\]]+)\]\((https://[^)\s]+\.md\?[^)\s]+)\)|([^\n]+?):?)\s*$",
                           re.M)
_FENCE = re.compile(r"^\s*(```+|~~~+)\s*([\w#+.-]*)")
_HEADING = re.compile(r"^#{1,6}\s+\S")
# Назва — перший заголовок: довідник Stripe.js починає сторінку одразу з «## Confirm a payment».
_TITLE = re.compile(r"\A\s*#{1,2}\s+(.+)\n")
# Мітки огорож серверного коду: за ними видно, що сторінка міняється від `?lang=`.
_SERVER = {"node", "python", "go", "ruby", "java", "dotnet", "cli", "php", "curl"}
LABELS = {"node": "Node.js", "python": "Python", "go": "Go", "ruby": "Ruby", "java": "Java",
          "dotnet": ".NET", "cli": "Stripe CLI", "php": "PHP", "curl": "curl"}


def _sections(md: str) -> list[list]:
    """[[заголовок, [рядки тіла]], …]; заголовки всередині коду — не заголовки."""
    out: list[list] = [["", []]]
    fence = ""
    for line in md.split("\n"):
        m = _FENCE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2):
                fence = ""
            out[-1][1].append(line)
            continue
        if m:
            fence = m.group(1)
            out[-1][1].append(line)
            continue
        if _HEADING.match(line):
            out.append([line.strip(), []])
        else:
            out[-1][1].append(line)
    return out


def _split(lines: list[str]) -> tuple[list[str], list[str]]:
    """(рядки тексту без коду, блоки коду цілими рядками з огорожами)."""
    prose, blocks, cur, fence = [], [], [], ""
    for line in lines:
        m = _FENCE.match(line)
        if fence:
            cur.append(line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2):
                blocks.append("\n".join(cur))
                cur, fence = [], ""
            continue
        if m:
            fence, cur = m.group(1), [line]
            continue
        if line.strip():
            prose.append(line.strip())
    if cur:
        blocks.append("\n".join(cur))
    return prose, blocks


def _langs_in(md: str) -> set[str]:
    return {m.group(2) for m in map(_FENCE.match, md.split("\n")) if m and m.group(2)} & _SERVER


def _merge(versions: list[tuple[str, str]]) -> str:
    """Тексти тієї самої сторінки різними мовами → один markdown (див. docstring модуля)."""
    base = _sections(versions[0][1])
    heads = [h for h, _ in base]
    extra: dict[int, list[str]] = {}      # номер розділу основи → дописане під ним
    inserted: dict[int, list[str]] = {}   # номер розділу основи → нові розділи після нього
    seen_blocks = [set(_split(body)[1]) for _, body in base]
    seen_secs: set[str] = set()
    for label, md in versions[1:]:
        secs = _sections(md)
        sm = difflib.SequenceMatcher(None, heads, [h for h, _ in secs], autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                for k in range(i2 - i1):
                    i, (_, body) = i1 + k, secs[j1 + k]
                    b_prose, _ = _split(base[i][1])
                    o_prose, o_blocks = _split(body)
                    if o_prose == b_prose:
                        new = [b for b in o_blocks if b not in seen_blocks[i]]
                        if new:
                            seen_blocks[i].update(new)
                            extra.setdefault(i, []).extend(["", f"{label}:", ""] + new)
                    elif "\n".join(body).strip() and "\n".join(body) != "\n".join(base[i][1]):
                        text = "\n".join(body).strip()
                        if text not in seen_blocks[i]:
                            seen_blocks[i].add(text)
                            extra.setdefault(i, []).extend(["", f"{label}:", "", text])
                continue
            anchor = max(i2 - 1, 0) if tag == "replace" else max(i1 - 1, 0)
            for h, body in secs[j1:j2]:
                text = (h + "\n" + "\n".join(body)).strip()
                if text and text not in seen_secs:
                    seen_secs.add(text)
                    inserted.setdefault(anchor, []).extend(["", text])
    out: list[str] = []
    for i, (h, body) in enumerate(base):
        if h:
            out.append(h)
        out.extend(body)
        out.extend(extra.get(i, []))
        out.extend(inserted.get(i, []))
    return "\n".join(out)


def _variants(text: str) -> list[tuple[str, str]]:
    """Перелік варіантів: [(підпис «Checkout: Stripe-hosted page», адреса .md?…)]."""
    out, parents = [], []
    for m in _VARIANT_ITEM.finditer(text.split(_VARIANTS, 1)[1]):
        depth = len(m.group(1).replace("\t", "  ")) // 2
        parents = parents[:depth]
        if m.group(3):
            out.append((": ".join(parents + [m.group(2).strip()]), m.group(3)))
        else:
            parents.append(m.group(4).strip())
    return out


def _with_lang(url: str, lang: str) -> str:
    return url + ("&" if "?" in url else "?") + f"lang={lang}"


def _document(ctx, source: dict, url: str, page: str, label: str = "") -> str:
    langs = list(source.get("langs") or [])
    first = _with_lang(url, langs[0]) if langs else url
    text = ctx.text(first)
    _markup.refuse_html(text, first)
    if len(langs) > 1 and _langs_in(text):
        versions = [(LABELS.get(langs[0], langs[0]), text)]
        for lang in langs[1:]:
            more = ctx.text(_with_lang(url, lang))
            _markup.refuse_html(more, _with_lang(url, lang))
            versions.append((LABELS.get(lang, lang), more))
        text = _merge(versions)
    meta, rest = _markup.front_matter(text)
    title = meta.get("title", "")
    head = _TITLE.match(rest)
    if head:
        title, rest = title or head.group(1).strip(), rest[head.end():]
    if label:
        title = f"{title} ({label})"
    body = _markup.markdown_body(rest)
    _markup.require(title, body, url, min_chars=1)
    version = source.get("version", "")
    pv = re.compile(source["path_version"]) if source.get("path_version") else None
    m = pv.search(urlsplit(page).path) if pv else None
    if m:
        named = m.groupdict().get("n")
        version = f"api-{m.group('d')}" + (f".{named}" if named else "")
    return _markup.document(title, page, ctx.stamp, body, version)


def _name(page: str) -> str:
    parts = urlsplit(page)
    tail = "-".join(v for _, v in parse_qsl(parts.query))
    return _markup.slug(parts.path + ("-" + tail if tail else ""))


@register("stripe-md")
def stripe_md(source: dict, ctx) -> list[Item]:
    within = source.get("within") or []
    if not within:
        raise SystemExit(f"{source['id']}: читач stripe-md вимагає поле `within`.")
    match = re.compile(source.get("match") or "")
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    langs = list(source.get("langs") or [])
    pages: list[str] = []
    for loc in _LOC.findall(ctx.text(source["url"])):
        # Частина розділів (`/cli/…`) є в сайтмапі двічі: сторінкою і її markdown-двійником.
        page = re.sub(r"\.md$", "", loc.rstrip("/"))
        path = urlsplit(page).path
        # Варіанти сторінок сайтмап теж несе (`?payment-ui=…&amp;ui=…`), але їх дає перелік
        # варіантів самої сторінки — з підписами й у формі, яку приймає markdown-двійник.
        if "?" in loc:
            continue
        if (page not in pages and any(page.startswith(w) for w in within) and match.search(path)
                and not any(r.search(path) for r in exclude) and ctx.allowed(page + ".md")):
            pages.append(page)
    if not pages:
        raise SystemExit(f"У сайтмапі {source['url']} не знайдено жодної сторінки під "
                         f"`match` — розмітка змінилася або вираз не той.")
    items: list[Item] = []
    for page in pages:
        url = page + ".md"
        if source.get("variants") is True:
            probe = _with_lang(url, langs[0]) if langs else url
            # Сторінка, якої не віддає двійник, — збій лише цього документа, не всього переліку.
            code, data = ctx.fetch(probe)
            text = data.decode("utf-8", errors="replace") if code == "200" else ""
            if _VARIANTS in text:
                for label, v_url in _variants(text):
                    if not ctx.allowed(v_url):
                        continue
                    v_page = v_url.replace(".md?", "?", 1)
                    name = _name(v_page)

                    def make(v_url=v_url, v_page=v_page, label=label):
                        return _document(ctx, source, v_url, v_page, label)

                    items.append(Item(id=f"{source['id']}/{name}",
                                      file=f"{source['id']}--{name}.txt", make=make))
                continue
        name = _name(page)

        def make(url=url, page=page):
            return _document(ctx, source, url, page)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
