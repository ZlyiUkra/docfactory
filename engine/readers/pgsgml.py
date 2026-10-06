"""Читач сирців документації PostgreSQL: DocBook у SGML (до 10) і в XML (з 11) з репозиторію.

`pg-sgml` — `url`     — префікс дерев GitHub (…/repos/ВЛАСНИК/РЕПО/git/trees/);
            `refs`    — об'єкт «гілка чи тег → версія», від найновішого;
            `folder`  — тека сирців («doc/src/sgml»), разом із вкладеними (`ref/`, `func/`);
            `exclude` — вирази шляхів, що не беруться (службові файли збирання);
            `site`    — необов'язковий корінь сайту документації («https://www.postgresql.org/docs»):
                        тоді джерелом документа стає сторінка сайту `САЙТ/ВЕРСІЯ/id.html`, а не
                        файл на GitHub. Сайт не читається — це лише адреса для посилань.

Навіщо окремий читач. Документація PostgreSQL пишеться в DocBook, і готового markdown у
репозиторії немає. До версії 10 включно це SGML, а не XML: скорочений кінцевий тег `</>`,
незакриті `<xref linkend="…">` і `<colspec>`, атрибути без лапок. Розбір XML
(`docbook-gh`) на таких файлах падає на першому ж абзаці. Тут розмітка читається потоком
тегів, без дерева: `</>` закриває останній відкритий елемент, порожні елементи (`xref`,
`colspec`, `anchor`…) не відкриваються зовсім, а кінцевий тег, якого немає нагорі стосу,
закриває все до свого відкривного. Так той самий код читає і SGML 9.x, і XML 11+.

Одиниця — неповторний файл: пара «шлях, вміст» (хеш blob із дерева гілки) — один
документ з усіма версіями, де файл був саме таким, як у `ghdocs-history`. Сирці кожної
версії — це 300–450 файлів по 10–12 МБ, але між сусідніми версіями більшість глав
(особливо довідник команд `ref/`) не змінюється або змінюється в кількох файлах.

Сутності на кшталт `&version;` чи `&mdash;` підставляються з невеликого переліку; невідома
лишається своєю назвою. Покажчик (`indexterm`) і службові шапки (`refmeta`, `*info`)
викидаються: без цього кожен розділ починався б переліком термінів покажчика.
"""

import json
import re
from html import unescape
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
_TOKEN = re.compile(
    r"<!--.*?-->"
    r"|<!\[CDATA\[(?P<cdata>.*?)\]\]>"
    r"|<![^>]*>|<\?.*?\?>"
    r"|</(?P<end>[\w:.-]*)\s*>"
    r"|<(?P<start>[\w:.-]+)(?P<attrs>(?:\s+[^<>]*?)?)\s*(?P<empty>/?)>",
    re.S)
_ATTR = re.compile(r'([\w:.-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))')
_ENTITY = re.compile(r"&([A-Za-z][\w.-]*);")
_ENTITIES = {"mdash": "—", "ndash": "–", "nbsp": " ", "hellip": "…", "copy": "©",
             "reg": "®", "trade": "™", "minus": "−", "times": "×", "plusmn": "±",
             "le": "≤", "ge": "≥", "ne": "≠", "deg": "°", "lsquo": "‘", "rsquo": "’",
             "ldquo": "“", "rdquo": "”", "dollar": "$", "percnt": "%", "num": "#",
             "lowbar": "_", "verbar": "|", "sol": "/", "ast": "*", "lsqb": "[", "rsqb": "]",
             "lcub": "{", "rcub": "}", "excl": "!", "quest": "?", "commat": "@"}

# Порожні в SGML-сирцях: кінцевого тегу немає ніколи.
# Корені, з яких сайт робить окрему сторінку з іменем за їхнім id.
_PAGES = {"chapter", "appendix", "preface", "part", "reference", "refentry", "sect1",
          "glossary", "bibliography"}
_VOID = {"xref", "colspec", "spanspec", "co", "footnoteref", "anchor", "void", "sbr",
         "area", "xi:include", "include", "imagedata", "graphic", "coref", "glossseealso"}
# Викидаються разом із вмістом.
_DROP = {"indexterm", "refmeta", "info", "bookinfo", "chapterinfo", "sectioninfo",
         "refentryinfo", "remark", "mediaobject", "imageobject", "titleabbrev",
         "keywordset", "comment", "refclass", "abstract-index"}
# Розділи: їхній <title> стає заголовком на рівень, глибший за батьківський.
_SECTIONS = {"book", "part", "reference", "chapter", "appendix", "preface", "article",
             "refentry", "sect1", "sect2", "sect3", "sect4", "sect5", "section",
             "refsect1", "refsect2", "refsect3", "refsynopsisdiv", "simplesect",
             "glossary", "glossdiv", "bibliography", "bibliodiv", "partintro", "sidebar",
             "example", "informalexample", "table", "informaltable", "figure",
             "procedure", "qandaset", "qandadiv"}
_PRE = {"programlisting", "screen", "synopsis", "literallayout", "cmdsynopsis",
        "funcsynopsis", "programlistingco", "screenco"}
_BLOCK = {"para", "simpara", "formalpara", "listitem", "varlistentry", "term", "glossterm",
          "glossdef", "glossentry", "step", "substeps", "row", "entry", "blockquote",
          "itemizedlist", "orderedlist", "variablelist", "simplelist", "member",
          "segmentedlist", "seglistitem", "calloutlist", "callout", "question", "answer",
          "qandaentry", "tgroup", "thead", "tbody", "tfoot", "biblioentry", "bibliomixed",
          "refnamediv", "refpurpose", "attribution", "epigraph", "msgset", "msgentry",
          "note", "tip", "warning", "caution", "important", "footnote"}
_ADMON = {"note": "Note", "tip": "Tip", "warning": "Warning", "caution": "Caution",
          "important": "Important"}


def _attrs(text: str) -> dict:
    return {m.group(1).lower(): m.group(2) or m.group(3) or m.group(4) or ""
            for m in _ATTR.finditer(text or "")}


def _entities(text: str, extra: dict) -> str:
    def sub(m):
        name = m.group(1)
        return extra.get(name) or _ENTITIES.get(name) or name
    return unescape(_ENTITY.sub(sub, text)) if "&" in text else text


class _Conv:
    """Потік тегів → рядки markdown корпусу."""

    def __init__(self, extra: dict):
        self.extra = extra
        self.lines: list[str] = []
        self.buf: list[str] = []
        self.stack: list[str] = []
        self.depth = 0            # глибина розділів
        self.base = None          # глибина розділу, чия назва — назва документа
        self.title = ""
        self.cap = None           # збір тексту назви: [глибина, частини]
        self.drop = 0             # глибина викинутого вмістом елемента
        self.pre = None           # [ім'я, вкладеність, частини]
        self.lists: list[str] = []  # префікси вкладених списків
        self.item = ""            # префікс першого абзацу пункту
        self.refname: list[str] = []
        self.refpurpose: list[str] = []
        self.mode = ""            # refname / refpurpose — куди йде текст
        self.anchored = []        # стос: чи має відкритий varlistentry власний id
        self.page = None          # id кореневого елемента — ім'я сторінки на сайті

    # --- виведення
    def flush(self):
        text = " ".join("".join(self.buf).split())
        self.buf = []
        if not text:
            return
        indent = "  " * max(len(self.lists) - 1, 0)
        if self.item:
            self.lines.append(f"{indent}{self.item}{text}")
            self.item = ""
        else:
            self.lines.append(f"{indent}{'  ' if self.lists else ''}{text}")
        self.lines.append("")

    def heading(self, text: str):
        text = " ".join(text.split())
        if not text:
            return
        if self.base is None:
            self.base = self.depth
            self.title = text
            return
        if not self.title:
            self.title = text
            return
        level = min(max(self.depth - self.base + 1, 2), 6)
        self.lines.append(f"{'#' * level} {text}")
        self.lines.append("")

    def text(self, s: str):
        if self.drop:
            return
        s = _entities(s, self.extra)
        if self.pre is not None:
            self.pre[2].append(s)
        elif self.cap is not None:
            self.cap[1].append(s)
        elif self.mode == "refname":
            self.refname.append(s)
        elif self.mode == "refpurpose":
            self.refpurpose.append(s)
        else:
            self.buf.append(s)

    # --- теги
    def start(self, name: str, attrs: dict, empty: bool):
        if self.page is None:
            self.page = (attrs.get("id") or "").lower() if name in _PAGES else ""
        if self.drop:
            if name not in _VOID and not empty:
                self.stack.append(name)
                self.drop += 1
            return
        if self.pre is not None:
            if name == self.pre[0] and not empty:
                self.pre[1] += 1
            if name not in _VOID and not empty:
                self.stack.append(name)
            return
        if name in ("xref", "footnoteref"):
            ref = attrs.get("endterm") or attrs.get("linkend", "")
            self.text(f"[{ref}]" if ref else "")
            return
        if name in _VOID or empty:
            return
        self.stack.append(name)
        # Посилання з адресою-сутністю — це «§» на коміт у нотатках релізів
        # (`&commit_baseurl;…`): для пошуку шум, і адреса нікуди не веде.
        if name in _DROP or (name in ("ulink", "link")
                             and attrs.get("url", "").startswith("&")):
            self.drop = 1
            return
        if name in _PRE:
            self.flush()
            self.pre = [name, 1, []]
            return
        if name in ("title", "refentrytitle"):
            self.flush()
            self.cap = [len(self.stack), []]
            return
        if name == "refname":
            self.mode = "refname"
            if self.refname:
                self.refname.append(", ")
            return
        if name == "refpurpose":
            self.mode = "refpurpose"
            return
        if name in _SECTIONS:
            self.flush()
            self.depth += 1
            if name == "refsynopsisdiv":
                self.heading("Synopsis")
            return
        if name in ("itemizedlist", "orderedlist", "variablelist", "simplelist",
                    "calloutlist", "segmentedlist", "procedure"):
            self.flush()
            self.lists.append("1. " if name in ("orderedlist", "procedure") else "- ")
            return
        if name in ("listitem", "step", "callout", "member", "seglistitem"):
            self.flush()
            # Опис терміна у variablelist — абзац під термом, а не новий пункт.
            parent = self.stack[-2].split("|", 1)[0] if len(self.stack) > 1 else ""
            self.item = "" if parent == "varlistentry" else (self.lists[-1] if self.lists else "")
            return
        if name == "varlistentry":
            self.flush()
            self.anchored.append(bool(attrs.get("id")))
            return
        if name in ("term", "glossterm"):
            self.flush()
            if self.anchored and self.anchored[-1]:
                # Параметр сервера (`guc-work-mem`) і подібне з власним id — розділ:
                # інакше `config` — 200 тисяч символів під півтора десятка заголовків.
                self.cap = [len(self.stack), []]
                self.stack[-1] = "term|#"
                return
            self.item = self.lists[-1] if self.lists else ""
            self.buf.append("**")
            return
        if name in _ADMON:
            self.flush()
            self.buf.append(f"**{_ADMON[name]}.** ")
            return
        if name == "footnote":
            self.buf.append(" (")
            return
        if name == "row":
            self.flush()
            return
        if name == "entry":
            if self.buf and "".join(self.buf).strip():
                self.buf.append(" | ")
            return
        if name in _BLOCK:
            self.flush()
            return
        if name in ("ulink", "link") and attrs.get("url"):
            self.stack[-1] = f"{name}|{attrs['url']}"

    def end(self, name: str):
        if not self.stack:
            return
        if not name:
            name = self.stack[-1].split("|", 1)[0]
        names = [s.split("|", 1)[0] for s in self.stack]
        if name not in names:
            return
        # Закриває все до свого відкривного: незакриті всередині (SGML) — теж.
        while self.stack:
            top = self.stack.pop()
            self._close(top)
            if top.split("|", 1)[0] == name:
                break

    def _close(self, top: str):
        name, _, url = top.partition("|")
        if self.drop:
            self.drop -= 1
            return
        if self.pre is not None:
            if name == self.pre[0]:
                self.pre[1] -= 1
                if self.pre[1] == 0:
                    body = "".join(self.pre[2]).strip("\n")
                    body = "\n".join(ln.rstrip() for ln in body.split("\n"))
                    indent = "  " * len(self.lists)
                    if body.strip():
                        self.lines.append(f"{indent}```")
                        self.lines.extend(f"{indent}{ln}" if ln else "" for ln in body.split("\n"))
                        self.lines.append(f"{indent}```")
                        self.lines.append("")
                    self.pre = None
            return
        if name in ("title", "refentrytitle") and self.cap is not None:
            text = "".join(self.cap[1])
            self.cap = None
            if name == "title":
                self.heading(text)
            return
        if name in ("refname", "refpurpose"):
            self.mode = ""
            if name == "refpurpose":
                head = " ".join("".join(self.refname).split())
                purpose = " ".join("".join(self.refpurpose).split())
                self.refname, self.refpurpose = [], []
                self.heading(f"{head} — {purpose}" if purpose else head)
            return
        if name in _SECTIONS:
            self.flush()
            self.depth -= 1
            return
        if name in ("itemizedlist", "orderedlist", "variablelist", "simplelist",
                    "calloutlist", "segmentedlist", "procedure"):
            self.flush()
            if self.lists:
                self.lists.pop()
            return
        if name == "term" and url == "#":
            text = "".join(self.cap[1]) if self.cap is not None else ""
            self.cap = None
            self.depth += 1
            self.heading(text)
            self.depth -= 1
            return
        if name == "varlistentry":
            self.flush()
            if self.anchored:
                self.anchored.pop()
            return
        if name in ("term", "glossterm"):
            self.buf = ["".join(self.buf).rstrip() + "**"]
            self.flush()
            return
        if name == "footnote":
            self.buf.append(")")
            return
        if name == "entry":
            return
        if name in _BLOCK or name in _ADMON:
            self.flush()
            return
        if url:
            self.buf.append(f" ({url})")

    def feed(self, text: str):
        pos = 0
        for m in _TOKEN.finditer(text):
            if m.start() > pos:
                self.text(text[pos:m.start()])
            pos = m.end()
            if m.group("cdata") is not None:
                self.text(m.group("cdata"))
            elif m.group("end") is not None:
                self.end(m.group("end").lower())
            elif m.group("start"):
                self.start(m.group("start").lower(), _attrs(m.group("attrs")),
                           bool(m.group("empty")))
        if pos < len(text):
            self.text(text[pos:])
        while self.stack:
            self._close(self.stack.pop())
        self.flush()


def convert(text: str, extra: dict) -> tuple[str, str, str]:
    """(назва, тіло markdown, ім'я сторінки на сайті чи «») одного файла сирців."""
    conv = _Conv(extra)
    conv.feed(text)
    body = "\n".join(conv.lines)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    # Порожній жирний від терміна без тексту.
    body = body.replace("****", "")
    return conv.title, body, conv.page or ""


@register("pg-sgml")
def pg_sgml(source: dict, ctx) -> list[Item]:
    m = _TREES.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував префікс дерев "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
    owner, repo = m.groups()
    refs = source.get("refs")
    if not isinstance(refs, dict) or not refs:
        raise SystemExit(f"{source['id']}: читач pg-sgml потребує поля refs — "
                         f"об'єкта «гілка → версія».")
    folder = source.get("folder", "doc/src/sgml").strip("/")
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    extra = {k: str(v) for k, v in (source.get("entities") or {}).items()}
    site = (source.get("site") or "").rstrip("/")

    seen: dict = {}
    for ref in refs:
        url = f"{source['url']}{quote(ref, safe='')}?recursive=1"
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
            if (entry.get("type") == "blob" and path.startswith(folder + "/")
                    and path.endswith(".sgml") and entry.get("size", 1) > 0
                    and not any(r.search(path) for r in exclude)):
                stem = path[len(folder) + 1:-len(".sgml")]
                name = f"{_markup.slug(stem)}-{entry['sha'][:8]}"
                seen.setdefault(name, [path, []])[1].append(ref)

    order = {r: i for i, r in enumerate(refs)}
    items = []
    for name, (path, found) in seen.items():
        found = sorted(set(found), key=order.get)
        ref = found[0]
        where = f"{owner}/{repo}/{quote(ref, safe='')}/{quote(path)}"
        raw = f"https://raw.githubusercontent.com/{where}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{where.split('/', 2)[2]}"
        version = ", ".join(dict.fromkeys(refs[r] for r in found))
        major = refs[ref]

        def make(raw=raw, blob=blob, path=path, version=version, major=major):
            text = ctx.text(raw)
            title, body, page = convert(text, {"version": major, "majorversion": major,
                                               **extra})
            # Посилання — на сторінку сайту найновішої версії файла: сайт збирається з
            # тих самих сирців, а версію в адресі модель міняє на ту, про яку відповідь.
            if page and site:
                blob = f"{site}/{major}/{page}.html"
            if not title:
                title = path.rsplit("/", 1)[-1][:-len(".sgml")]
            if body.strip():
                _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: у теці {folder} жодного файла .sgml "
                         f"на жодній з {len(refs)} гілок.")
    return items
