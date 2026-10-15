"""Читач старих файлів документації з одного знімка репозиторію: OpenOffice Writer, HTML, простий текст.

`gh-legacy-docs` — файли однієї гілки чи тега, які спільні читачі не беруть. `url` — префікс дерев через API
                   (…/repos/ВЛАСНИК/РЕПО/git/trees/), `ref` — гілка чи тег, `folders` — префікси шляхів,
                   `extensions` — розширення (`.sxw`, `.html`, `.htm`, `.txt`), `exclude` — вирази шляхів, що не
                   беруться, `name_prefix`, `version` — підпис версії для всіх документів, `cite` — шаблон
                   адреси для людей з `{path}`.

Навіщо. До ICU 65 посібник користувача жив не в репозиторії `icu`, а в `icu-docs` — файлами OpenOffice Writer
(`.sxw`, zip із `content.xml`), поруч — дизайн-документи в HTML. Спільних читачів для таких форматів немає.
`.sxw` розбирається так: заголовки `text:h` стають «##», абзаци зі стилем `icu-source` — блоком коду, пункти
списків — «-», таблиці — рядками «a | b». HTML — спільним `html_body`, назва — з `<title>` чи першого `<h1>`.
"""

import re
import zipfile
import io
from urllib.parse import quote, urlsplit
import json
import xml.etree.ElementTree as ET

from engine.readers import Item, _markup, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_NS = {"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"}


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _inline(el) -> str:
    """Текст абзацу: проміжки `text:s`, табуляції, розриви рядка."""
    out = [el.text or ""]
    for ch in el:
        name = _local(ch.tag)
        if name == "s":
            out.append(" " * int(next((v for k, v in ch.attrib.items() if k.endswith("}c")), "1")))
        elif name == "tab":
            out.append("\t")
        elif name == "line-break":
            out.append("\n")
        else:
            out.append(_inline(ch))
        out.append(ch.tail or "")
    return "".join(out)


def sxw_to_markdown(data: bytes) -> tuple[str, str]:
    """Вміст `.sxw` → (назва, markdown). Назва — перший заголовок."""
    xml = zipfile.ZipFile(io.BytesIO(data)).read("content.xml")
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        # Недійсні символи й неекрановані «&» трапляються в старих файлах: чистимо і пробуємо знову.
        text = xml.decode("utf-8", "replace")
        text = text.replace('xmlns:=""', "")
        text = re.sub("[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
        text = re.sub(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", "&amp;", text)
        root = ET.fromstring(text.encode("utf-8"))
    out: list[str] = []
    code: list[str] = []
    title = ""

    def flush():
        if code:
            out.extend(["", "```", "\n".join(code).rstrip(), "```", ""])
            code.clear()

    def walk(node, depth=0):
        nonlocal title
        for ch in node:
            name = _local(ch.tag)
            style = next((v for k, v in ch.attrib.items() if k.endswith("}style-name")), "")
            if name == "h":
                flush()
                text = " ".join(_inline(ch).split())
                if not text:
                    continue
                level = int(next((v for k, v in ch.attrib.items() if k.endswith("}level")), "1"))
                if not title:
                    title = text
                out.extend(["", "#" * min(level + 1, 6) + " " + text, ""])
            elif name == "p":
                text = _inline(ch)
                if "source" in style.lower() or "code" in style.lower() and "icu-code" not in style:
                    code.append(text.rstrip())
                    continue
                flush()
                text = " ".join(text.split())
                if text:
                    out.extend(["", ("- " if depth else "") + text, ""])
            elif name in ("list", "ordered-list", "unordered-list", "list-item", "list-header"):
                flush()
                walk(ch, depth + 1 if name != "list-item" else depth)
            elif name == "table":
                flush()
                for row in ch.iter():
                    if _local(row.tag) == "table-row":
                        cells = [" ".join(_inline(c).split()) for c in row
                                 if _local(c.tag) == "table-cell"]
                        if any(cells):
                            out.append("| " + " | ".join(cells) + " |")
                out.append("")
            elif name in ("body", "section", "text"):
                walk(ch, depth)
        flush()

    walk(root)
    # назва документа — перший заголовок; решту розкладає walk
    return title, "\n".join(out)


def _html(raw: str) -> tuple[str, str]:
    m = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I) or \
        re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S | re.I)
    title = " ".join(re.sub(r"<[^>]+>", "", m.group(1)).split()) if m else ""
    return title, _markup.html_body(raw)


@register("gh-legacy-docs")
def gh_legacy_docs(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев /repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    ref = source["ref"]
    folders = tuple(source["folders"])
    exts = tuple(source["extensions"])
    exclude = [re.compile(x) for x in source.get("exclude") or ()]
    version = source.get("version", "")
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""
    cite = source.get("cite") or f"https://github.com/{owner}/{repo}/blob/{ref}/{{path}}"
    url = f"{source['url']}{quote(ref, safe='@')}?recursive=1"
    tree = json.loads(ctx.text(url))
    if tree.get("truncated"):
        raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
    items = []
    for e in tree["tree"]:
        path = e.get("path", "")
        if (e.get("type") != "blob" or not path.startswith(folders) or not path.lower().endswith(exts)
                or any(r.search(path) for r in exclude)):
            continue
        raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{quote(ref, safe='@')}/{quote(path)}"
        if not ctx.allowed(raw):
            continue
        name = f"{lead}{_markup.slug(path)}"

        def make(path=path, raw=raw):
            low = path.lower()
            if low.endswith(".sxw"):
                title, body = sxw_to_markdown(ctx.bytes(raw))
            elif low.endswith((".html", ".htm")):
                title, body = _html(ctx.text(raw))
            else:
                text = ctx.text(raw).replace("\r\n", "\n")
                title, body = path.rsplit("/", 1)[-1], text
            title = title or path.rsplit("/", 1)[-1]
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(f"{title} ({path.rsplit('/', 1)[-1]})", cite.format(path=quote(path)),
                                    ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного файла за `folders` і `extensions`.")
    return items
