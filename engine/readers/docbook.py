"""Читачі DocBook XML: man-сторінки systemd з GitHub і Debian Administrator's Handbook з salsa.

`docbook-gh`     — `url`     — префікс дерев GitHub (…/repos/ВЛАСНИК/РЕПО/git/trees/);
                   `refs`    — «тег → версія», від найновішого;
                   `folder`  — тека з файлами XML («man»); `exclude` — вирази шляхів;
                   `label`   — префікс назви документа.
`docbook-gitlab` — `url`     — API проєкту GitLab за числовим id (…/api/v4/projects/12779/):
                                у формі ВЛАСНИК%2FРЕПО білий список розкодовує %2F і адреси
                                не впізнає;
                   `raw`     — префікс сирих файлів (…/ВЛАСНИК/РЕПО/-/raw/);
                   `refs`, `folder`, `match` (вираз імен файлів), `label` — як вище.

Навіщо. Man-сторінки systemd пишуться в DocBook (`man/*.xml`), а не в groff: готових сторінок
у репозиторії немає, вони збираються під час збирання systemd. Debian Administrator's
Handbook — вільна книжка (GPL-2.0+ або CC-BY-SA-3.0), теж DocBook, по файлу на розділ і по
гілці на випуск Debian. Без розбору лишилися б розмітка й покажчик (`<indexterm>` — понад
триста в одному розділі книжки), а вставки `xi:include` («Added in version 252», спільні
описи опцій) — порожніми місцями.

Одиниця — неповторний файл: той самий файл у кількох версіях (хеш вмісту однаковий) — один
документ з усіма цими версіями. Вставки беруться з того самого тегу, що й сам файл;
сутності, які systemd підставляє лише під час збирання (`&MOUNT_PATH;`), лишаються назвою.
"""

import re
import xml.etree.ElementTree as ET
from urllib.parse import quote

from engine.readers import Item, _markup, register
from engine.readers.k8sdocs import _Site

_XI = "{http://www.w3.org/2001/XInclude}include"
_BLOCK_DROP = {"indexterm", "chapterinfo", "sectioninfo", "bookinfo", "refentryinfo",
               "mediaobject", "figure", "keywordset", "remark", "refmeta", "info",
               "imageobject", "screenshot"}
_SECTIONS = {"refsect1": 2, "refsect2": 3, "refsect3": 4, "section": 2, "sect1": 2,
             "sect2": 3, "sect3": 4, "sect4": 5, "simplesect": 4}
_PRE = {"programlisting", "screen", "literallayout", "synopsis"}
_ADMON = {"note": "Note", "tip": "Tip", "warning": "Warning", "caution": "Caution",
          "important": "Important"}


def _clean_xml(text: str) -> str:
    """XML без DOCTYPE і з назвами замість невідомих сутностей: стандартний розбір інакше
    падає на `&MOUNT_PATH;`."""
    text = re.sub(r"<!DOCTYPE[^\[>]*(\[.*?\])?\s*>", "", text, count=1, flags=re.S)
    return re.sub(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)([A-Za-z][\w.-]*);",
                  r"\1", text)


def _local(tag) -> str:
    return tag.split("}", 1)[1] if isinstance(tag, str) and "}" in tag else (tag or "")


class _Conv:
    def __init__(self, include):
        self.include = include      # (href, xpointer) → елемент або None
        self.out: list[str] = []

    def inline(self, el) -> str:
        """Текст елемента в рядок: розмітка всередині абзацу знімається, посилання на
        сторінку man стає «ім'я(розділ)»."""
        tag = _local(el.tag)
        if tag in _BLOCK_DROP or tag == "footnote":
            return el.tail or ""
        if tag == _local(_XI):
            inc = self.include(el.get("href", ""), el.get("xpointer", ""))
            body = "".join(self.inline(c) for c in inc) if inc is not None else ""
            return (inc.text or "" if inc is not None else "") + body + (el.tail or "")
        if tag == "citerefentry":
            title = el.findtext("refentrytitle") or ""
            vol = el.findtext("manvolnum") or ""
            return f"{title}({vol})" + (el.tail or "")
        if tag == "arg":
            inner = (el.text or "") + "".join(self.inline(c) for c in el)
            choice, rep = el.get("choice", "opt"), el.get("rep", "")
            inner = inner.strip() + ("…" if rep == "repeat" else "")
            inner = f"[{inner}]" if choice == "opt" else (f"{{{inner}}}" if choice == "req"
                                                           else inner)
            return f" {inner}" + (el.tail or "")
        if tag in ("ulink", "link") and el.get("url") and not (el.text or len(el)):
            return el.get("url") + (el.tail or "")
        text = (el.text or "") + "".join(self.inline(c) for c in el)
        if tag == "replaceable":
            text = f"<{text.strip()}>" if text.strip() else text
        elif tag == "keycap":
            text = text.strip()
        return text + (el.tail or "")

    def para(self, text: str) -> None:
        text = " ".join(text.split())
        if text:
            self.out.extend([text, ""])

    def block(self, el, depth: int = 0) -> None:
        tag = _local(el.tag)
        if tag in _BLOCK_DROP:
            return
        if tag == _local(_XI):
            inc = self.include(el.get("href", ""), el.get("xpointer", ""))
            if inc is not None:
                self.block(inc, depth)
            return
        if tag in _SECTIONS:
            level = min(6, _SECTIONS[tag] + (depth if tag == "section" else 0))
            title = el.find("title")
            if title is not None:
                self.out.extend([f"{'#' * level} {' '.join(self.inline(title).split())}", ""])
            for child in el:
                if child is not title:
                    self.block(child, depth + (1 if tag == "section" else 0))
            return
        if tag in ("title", "refentrytitle", "manvolnum", "titleabbrev"):
            return
        if tag in ("para", "simpara", "formalpara", "highlights", "abstract", "refpurpose"):
            if tag in ("formalpara", "highlights", "abstract"):
                for child in el:
                    if _local(child.tag) == "title":
                        self.para(self.inline(child))
                    else:
                        self.block(child, depth)
                return
            # Абзац із вкладеними блоками (список, приклад усередині <para>).
            nested = [c for c in el if _local(c.tag) in _PRE | {"itemizedlist",
                      "orderedlist", "variablelist", "table", "informaltable", "example",
                      "note", "tip", "warning", "caution", "important"}]
            if not nested:
                self.para(self.inline(el))
                return
            buf = el.text or ""
            for child in el:
                if child in nested:
                    self.para(buf)
                    buf = ""
                    self.block(child, depth)
                    buf += child.tail or ""
                else:
                    buf += self.inline(child)
            self.para(buf)
            return
        if tag in _PRE:
            text = (el.text or "") + "".join(self.inline(c) for c in el)
            text = text.strip("\n")
            if text.strip():
                self.out.extend(["```", text.rstrip(), "```", ""])
            return
        if tag in ("cmdsynopsis", "funcsynopsis"):
            text = " ".join(self.inline(el).split())
            if text:
                self.out.extend(["```", text, "```", ""])
            return
        if tag in ("itemizedlist", "orderedlist"):
            for i, item in enumerate(el.findall("listitem"), 1):
                mark = f"{i}." if tag == "orderedlist" else "-"
                start = len(self.out)
                for child in item:
                    self.block(child, depth)
                if len(self.out) > start:
                    self.out[start] = f"{mark} {self.out[start]}"
            return
        if tag == "variablelist":
            for entry in el.findall("varlistentry"):
                terms = [" ".join(self.inline(t).split()) for t in entry.findall("term")]
                if terms:
                    self.out.extend([", ".join(terms), ""])
                item = entry.find("listitem")
                if item is not None:
                    for child in item:
                        self.block(child, depth)
            return
        if tag in _ADMON or tag == "sidebar":
            title = el.find("title")
            head = (" ".join(self.inline(title).split()) if title is not None
                    else _ADMON.get(tag, ""))
            if head:
                self.out.extend([f"{_ADMON.get(tag, 'Note')}: {head}" if tag == "sidebar"
                                 else f"{head}:", ""])
            for child in el:
                if child is not title:
                    self.block(child, depth)
            return
        if tag in ("table", "informaltable"):
            title = el.find("title")
            if title is not None:
                self.para(self.inline(title))
            rows = []
            for row in el.iter("row"):
                rows.append(" | ".join(" ".join(self.inline(e).split())
                                       for e in row.findall("entry")))
            if rows:
                self.out.extend(["```", *rows, "```", ""])
            return
        if tag == "example":
            title = el.find("title")
            if title is not None:
                self.para(self.inline(title))
            for child in el:
                if child is not title:
                    self.block(child, depth)
            return
        if tag == "refnamediv":
            names = ", ".join(n.text or "" for n in el.findall("refname"))
            purpose = el.findtext("refpurpose") or ""
            self.out.extend(["## Name", "", " ".join(f"{names} — {purpose}".split()), ""])
            return
        if tag == "refsynopsisdiv":
            self.out.extend(["## Synopsis", ""])
            for child in el:
                self.block(child, depth)
            return
        # Решта — обгортки (chapter, refentry, partintro…): заходимо всередину.
        if el.text and el.text.strip() and not len(el):
            self.para(el.text)
            return
        for child in el:
            self.block(child, depth)


def convert(xml_text: str, include=lambda href, xp: None) -> tuple[str, str, str]:
    """XML DocBook → (назва, призначення, markdown)."""
    root = ET.fromstring(_clean_xml(xml_text))
    conv = _Conv(include)
    title = ""
    purpose = ""
    if _local(root.tag) == "refentry":
        title = root.findtext("refmeta/refentrytitle") or ""
        vol = root.findtext("refmeta/manvolnum") or ""
        title = f"{title}({vol})" if vol else title
        purpose = " ".join((root.findtext("refnamediv/refpurpose") or "").split())
    else:
        t = root.find("title")
        title = " ".join(conv.inline(t).split()) if t is not None else ""
    for child in root:
        conv.block(child)
    body = "\n".join(conv.out)
    return title, purpose, re.sub(r"\n{3,}", "\n\n", body).strip()


def _includes(load):
    """Вставки xi:include одного тегу: файл — раз, елемент — за id з xpointer. Рядок
    «Added in version N» systemd тримає у version-info.xml під id «vN»."""
    files: dict = {}

    def get(href: str, xpointer: str):
        if not href or "/" in href or not href.endswith(".xml"):
            return None
        if href not in files:
            try:
                files[href] = ET.fromstring(_clean_xml(load(href) or "<x/>"))
            except ET.ParseError:
                files[href] = ET.fromstring("<x/>")
        root = files[href]
        if not xpointer:
            return root
        m = re.fullmatch(r"(?:xpointer\()?(?:id\(['\"])?([\w.-]+)(?:['\"]\))?\)?(?:/.*)?", xpointer)
        wanted = m.group(1) if m else xpointer
        return next((e for e in root.iter() if e.get("id") == wanted), None)
    return get


def _vkey(v: str) -> tuple:
    return tuple(int(n) for n in re.findall(r"\d+", v))


def _items(source: dict, ctx, groups: dict, fetch, raw_url) -> list[Item]:
    """Документ на неповторний файл; groups: (шлях, хеш) → [(ref, версія)]."""
    label = source.get("label", "")
    includes_by_ref: dict = {}
    items = []
    for (path, sha), found in sorted(groups.items()):
        found = sorted(found, key=lambda rv: _vkey(rv[1]), reverse=True)
        ref = found[0][0]
        versions = ", ".join(dict.fromkeys(v for _, v in found if v))
        stem = re.sub(r"\.xml$", "", path.rsplit("/", 1)[-1])
        doc = f"{_markup.slug(stem)}-{sha[:8]}"
        url = raw_url(ref, path)
        if not ctx.allowed(url):
            continue

        def make(path=path, sha=sha, ref=ref, url=url, versions=versions):
            folder = path.rsplit("/", 1)[0]
            if ref not in includes_by_ref:
                includes_by_ref[ref] = _includes(lambda href: fetch(ref, f"{folder}/{href}"))
            title, purpose, body = convert(fetch(ref, path, sha), includes_by_ref[ref])
            title = title + (f" — {purpose}" if purpose else "")
            if label:
                title = f"{label}: {title}"
            _markup.require(title, body, url)
            return _markup.document(title, url, ctx.stamp, body, versions)

        items.append(Item(id=f"{source['id']}/{doc}", file=f"{source['id']}--{doc}.txt",
                          make=make))
    return items


@register("docbook-gh")
def docbook_gh(source: dict, ctx) -> list[Item]:
    refs = source.get("refs") or {}
    folder = (source.get("folder") or "").strip("/")
    if not refs or not folder:
        raise SystemExit(f"{source['id']}: читач docbook-gh потребує полів refs і folder.")
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    site = _Site(source, ctx)
    groups: dict = {}
    for ref, version in refs.items():
        sha = site.subtree(site.entries(ref), folder)
        if not sha:
            continue
        for e in site.entries(sha):
            path = f"{folder}/{e.get('path')}"
            if (e.get("type") == "blob" and path.endswith(".xml")
                    and not any(r.search(path) for r in exclude)):
                groups.setdefault((path, e["sha"]), []).append((ref, str(version)))

    def fetch(ref, path, sha=""):
        return site.text(ref, path, sha) or ""
    return _items(source, ctx, groups, fetch, site.raw)


@register("docbook-gitlab")
def docbook_gitlab(source: dict, ctx) -> list[Item]:
    refs = source.get("refs") or {}
    folder = (source.get("folder") or "").strip("/")
    api = source["url"].rstrip("/") + "/"
    raw = source.get("raw", "").rstrip("/") + "/"
    match = re.compile(source.get("match") or r"\.xml$")
    if not refs or not folder or not source.get("raw"):
        raise SystemExit(f"{source['id']}: читач docbook-gitlab потребує полів refs, folder "
                         f"і raw.")
    import json
    groups: dict = {}
    for ref, version in refs.items():
        url = (f"{api}repository/tree?path={quote(folder)}&ref={quote(ref, safe='')}"
               f"&per_page=100")
        for e in json.loads(ctx.text(url)):
            if e.get("type") == "blob" and match.search(e.get("name", "")):
                groups.setdefault((e["path"], e["id"]), []).append((ref, str(version)))

    def raw_url(ref, path):
        return f"{raw}{quote(ref, safe='/')}/{quote(path)}"

    memo: dict = {}

    def fetch(ref, path, sha=""):
        key = sha or (ref, path)
        if key not in memo:
            url = raw_url(ref, path)
            memo[key] = ctx.text(url) if ctx.allowed(url) else ""
        return memo[key]
    return _items(source, ctx, groups, fetch, raw_url)
