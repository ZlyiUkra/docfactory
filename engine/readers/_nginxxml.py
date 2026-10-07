"""Сторінка документації nginx.org у форматі XML → markdown для звичайного розбору.

Сайт nginx.org збирається з XML власного словника (dtd/module.dtd, dtd/article.dtd):
модуль — `<module>` із розділами `<section>` і директивами `<directive>`, у директиві —
`<syntax>`, `<default>`, `<context>` і `<appeared-in>`; стаття — `<article>`. Markdown з
цього потрібен, щоб далі все йшло тим самим шляхом, що й решта документації: розділи
за заголовками, код — огородженими блоками.

Що стає чим:
- назва модуля чи статті (атрибут `name`) — заголовок першого рівня, тобто назва документа;
- `<section name>` — «##», директива — «###» з її ім'ям, а під ним рядки «Syntax:», «Default:»,
  «Context:» і «This directive appeared in version …» — так, як їх показує сайт;
- `<example>` і `<programlisting>` — блок коду; `<list>` — пункти, `<tag-name>`/`<tag-desc>` —
  пункт «`назва` — опис»; `<note>` — абзац «Note:»; `<table>` — рядки клітинок через « | »;
- `<literal>`, `<var>`, `<path>`, `<command>`, `<header>`, `<c-def>`, `<c-func>` — `код`;
- `<link>` без тексту — ім'я, на яке він веде (`id` директиви чи файл сторінки).

Сутності `&nbsp;`, `&mdash;` та інші оголошено в DTD, якого розбір не читає, тож вони
підставляються до розбору: інакше XML не прочитався б зовсім.
"""

import re
import xml.etree.ElementTree as ET

_ENTITIES = {"nbsp": " ", "times": "×", "lsquo": "‘", "rsquo": "’",
             "ldquo": "“", "rdquo": "”", "mdash": " — ", "reg": "®"}
_ENTITY = re.compile(r"&(" + "|".join(_ENTITIES) + r");")
_DOCTYPE = re.compile(r"<!DOCTYPE[^>]*>")
_CODE_TAGS = {"literal", "var", "path", "command", "header", "c-def", "c-func"}
_VERSION_TAGS = {"mainline_version": "the mainline version", "stable_version": "the stable version"}


def _inline(el) -> str:
    """Текст елемента з вкладеною розміткою в один рядок markdown."""
    out = [el.text or ""]
    for ch in el:
        out.append(_span(ch))
        out.append(ch.tail or "")
    return "".join(out)


def _span(el) -> str:
    tag = el.tag
    inner = _inline(el)
    if tag in _CODE_TAGS:
        text = " ".join(inner.split())
        if tag == "c-func":
            text += "()"
        return f"`{text}`" if text else ""
    if tag == "link":
        text = " ".join(inner.split())
        return text or el.get("id") or re.sub(r"\.xml$", "", (el.get("doc") or "").rsplit("/", 1)[-1])
    if tag == "http-status":
        return f"{el.get('code', '')} ({el.get('text', '')})".strip()
    if tag == "br":
        return "\n"
    if tag in _VERSION_TAGS:
        return inner or _VERSION_TAGS[tag]
    return inner


def _syntax(el, name: str) -> str:
    text = " ".join(_raw(el).split())
    if el.get("block") == "yes":
        return f"`{name} {text} {{ ... }}`".replace("  ", " ")
    return f"`{name} {text};`".replace(" ;", ";") if text else f"`{name};`"


def _raw(el) -> str:
    """Текст без позначок коду: синтаксис директиви вже стоїть у лапках цілком."""
    out = [el.text or ""]
    for ch in el:
        out.append(_raw(ch))
        out.append(ch.tail or "")
    return "".join(out)


def _paragraph(text: str) -> str:
    lines = [" ".join(ln.split()) for ln in text.split("\n")]
    return " ".join(ln for ln in lines if ln)


def _blocks(el, depth: int) -> list[str]:
    """Блоки markdown з дочірніх елементів розділу, директиви, абзацу чи пункту."""
    out: list[str] = []
    lead = _paragraph(el.text or "") if el.tag in ("para", "listitem", "tag-desc", "note", "td") else ""
    if lead:
        out.append(lead)
    for ch in el:
        tag = ch.tag
        if tag == "section":
            name = ch.get("name")
            if name:
                out.append(f"{'#' * depth} {' '.join(name.split())}")
            out += _blocks(ch, depth + 1)
        elif tag == "directive":
            out += _directive(ch, depth)
        elif tag == "para":
            out += _para(ch, depth)
        elif tag in ("example", "programlisting"):
            code = _raw(ch).strip("\n")
            out.append(f"```\n{code}\n```")
        elif tag == "list":
            out.append(_list(ch, depth))
        elif tag == "note":
            body = _blocks(ch, depth)
            out.append("Note: " + " ".join(body) if body else "Note:")
        elif tag == "table":
            rows = [" | ".join(_paragraph(_inline(td)) for td in tr) for tr in ch.iter("tr")]
            out.append("\n".join(r for r in rows if r.strip(" |")))
        elif tag in ("tag-name", "tag-desc", "listitem"):
            out += _blocks(ch, depth)
        else:
            text = _paragraph(_span(ch))
            if text:
                out.append(text)
        tail = _paragraph(ch.tail or "")
        if tail and el.tag in ("para", "listitem", "tag-desc", "note", "td"):
            out.append(tail)
    return out


def _para(el, depth: int) -> list[str]:
    """Абзац: суцільний текст з інлайн-розміткою, а вкладені приклади й списки — окремими
    блоками там, де вони стоять."""
    out: list[str] = []
    buf = [el.text or ""]

    def flush():
        text = _paragraph("".join(buf))
        if text:
            out.append(text)
        buf.clear()

    for ch in el:
        if ch.tag in ("example", "programlisting", "list", "note", "table"):
            flush()
            out += _blocks(_wrap(ch), depth)
        else:
            buf.append(_span(ch))
        buf.append(ch.tail or "")
    flush()
    return out


def _wrap(el):
    holder = ET.Element("section")
    holder.append(el)
    return holder


def _list(el, depth: int) -> str:
    items: list[str] = []
    ordered = el.get("type") == "enum"
    pending = ""
    for ch in el:
        if ch.tag == "tag-name":
            name = _paragraph(_inline(ch))
            pending = f"{pending}, {name}" if pending else name
            continue
        body = _para(ch, depth)
        text = " ".join(b for b in body if not b.startswith("```")) if body else ""
        code = [b for b in body if b.startswith("```")]
        if ch.tag == "tag-desc":
            head = f"{pending} — {text}" if text else pending
            pending = ""
        else:
            head = text
        marker = f"{len(items) + 1}." if ordered else "-"
        entry = f"{marker} {head}".rstrip()
        if code:
            entry += "\n\n" + "\n\n".join(code)
        items.append(entry)
    if pending:
        items.append(f"- {pending}")
    return "\n".join(items)


def _directive(el, depth: int) -> list[str]:
    name = el.get("name", "")
    out = [f"{'#' * depth} {name}"]
    syntax = [_syntax(s, name) for s in el.findall("syntax")]
    if syntax:
        out.append("Syntax: " + " or ".join(syntax))
    default = el.find("default")
    if default is not None:
        text = " ".join(_raw(default).split())
        out.append(f"Default: `{name} {text};`" if text else "Default: —")
    contexts = [" ".join(_raw(c).split()) for c in el.findall("context")]
    if contexts:
        out.append("Context: " + ", ".join(contexts))
    appeared = el.find("appeared-in")
    if appeared is not None and _raw(appeared).strip():
        out.append(f"This directive appeared in version {_raw(appeared).strip()}.")
    for ch in el:
        if ch.tag in ("syntax", "default", "context", "appeared-in"):
            continue
        out += _blocks(_wrap(ch), depth + 1)
    return out


def to_markdown(text: str) -> str:
    """XML сторінки nginx.org → markdown із назвою першим рядком. Порожній рядок — XML
    не розібрався або це не сторінка документації (`<module>`/`<article>`)."""
    text = _ENTITY.sub(lambda m: _ENTITIES[m.group(1)], _DOCTYPE.sub("", text))
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return ""
    if root.tag not in ("module", "article"):
        return ""
    title = " ".join((root.get("name") or "").split())
    body = _blocks(root, 2)
    return f"# {title}\n\n" + "\n\n".join(b for b in body if b.strip()) + "\n"
