"""Читачі текстів вебстандартів: специфікації WHATWG і W3C, RFC та чернетки IETF, ERC.

`spec-html`  — `url` — специфікація однією сторінкою, зібрана Bikeshed чи ReSpec. Документ
               — розділ верхнього рівня (`<h2>`), підрозділи — заголовки «## 4.4 …»,
               «### 4.4.5 …» з номерами самої специфікації. `label` — назва стандарту в
               назві документа («Fetch Standard»).
`whatwg-html`— `url` — зміст багатосторінкового видання стандарту HTML (Wattsi): кожна
               сторінка видання — документ. `exclude` — вирази імен сторінок, що не
               беруться (покажчики, подяки, таблиця іменованих символів).
`ietf-text`  — `url` — текст RFC, чернетки IETF чи специфікації OpenID у форматі xml2rfc.
               Документ — розділ верхнього рівня. `cite` — HTML-видання, на розділ якого
               веде адреса документа; поле `anchors: false` — коли якорів «#section-N» у
               нього немає.
`erc-md`     — `url` — markdown ERC з репозиторію ethereum/ERCs, `page` — його сторінка на
               eips.ethereum.org.

Навіщо свій розбір HTML, а не `_markup.html_body`. Норма специфікацій — алгоритми: кроки
у вкладених `<ol>`, і посилаються на них номером («step 5 of main fetch»). Спільний
перетворювач ставить замість номера дефіс і не робить відступів, тоді «If …, then:
return failure.» читалося б як два незалежні речення. Тут кроки нумеруються, а вкладені
— зсуваються. Окремо від читача `bikeshed`: той збирає назад формули KaTeX WebAssembly,
а у вебстандартах формул немає; зате тут є ReSpec і Wattsi, яких там немає.

Що відкидається. Зміст, анотації MDN і тестів WPT, спливні панелі визначень, посилання
«¶» біля заголовків. Ненумеровані службові розділи — покажчики, список літератури,
подяки, шаблонний «Conformance» Bikeshed — не стають документами: це покажчики й
службовий текст, а не норма. Нумерований «Conformance» (WCAG, ARIA) — норма і лишається.
"""

import re
from html.parser import HTMLParser
from urllib.parse import urljoin

from engine.readers import Item, _markup, register

_SKIP = {"script", "style", "nav", "template", "svg", "button", "noscript", "iframe",
         "math"}
_SKIP_CLASS = {"self-link", "dfn-panel", "mdn-anno", "wpt-tests-block", "annotation",
               "toc", "head", "respec-tests-details", "caniuse-stat", "dfnPanel"}
_VOID = {"br", "img", "hr", "wbr", "meta", "link", "input", "col", "source", "area",
         "base", "embed", "param", "track"}
_BLOCK = {"p", "div", "section", "blockquote", "figure", "figcaption", "table", "thead",
          "tbody", "tfoot", "details", "summary", "main", "article", "header", "footer",
          "aside", "dl", "ul", "ol", "tr"}
_HEADINGS = {"h2", "h3", "h4", "h5", "h6"}
_LANGS = {"js", "javascript", "html", "css", "json", "http", "abnf", "yaml", "xml",
          "webidl", "idl", "shell", "sh", "bash", "text", "jsonc"}
# Ненумеровані розділи, що не стають документами: покажчики, бібліографія, подяки,
# шаблон Bikeshed. Нумерований розділ з такою назвою лишається — там норма.
_DROP = re.compile(r"^(index|.*\bindex|references|normative references|informative "
                   r"references|acknowledge?ments|conformance|intellectual property "
                   r"rights|terms defined.*|dedication|issues index|property index|"
                   r"table of contents|abstract|status of this document|status)$", re.I)
# Подяки, бібліографія й покажчики не стають документами, навіть нумеровані: у ReSpec
# це додатки з літерою («C. References»), а в CSP — «11. Acknowledgements».
_DROP_ALWAYS = re.compile(r"^(acknowledge?ments|references|index|issue summary)$", re.I)


def _norm(text: str) -> str:
    return " ".join(text.split())


class _Spec(HTMLParser):
    """Сторінка специфікації → розділи з текстом.

    `split` — ділити на документи по `<h2>` (одна сторінка Bikeshed чи ReSpec); інакше
    вся сторінка — один документ (видання HTML, де сторінка і є розділом). Wattsi
    опускає закривні теги `</p>`, `</li>`, `</dd>`, `</td>`, тож межі абзаців і пунктів
    беруться з відкривних тегів, а стек тегів лише для того, щоб знати, де кінчається
    пропущене піддерево."""

    def __init__(self, split: bool):
        super().__init__(convert_charrefs=True)
        self.split = split
        self.started = not split          # одна сторінка: усе до змісту — шапка
        self.chapters: list[dict] = []    # {"num", "title", "id", "paras", "base"}
        self.cur: dict | None = None
        self.stack: list[str] = []
        self.skip_at = 0                  # глибина стеку, де почався пропуск; 0 — ні
        self.buf: list[str] = []
        self.prefix = ""
        self.lists: list[list] = []       # [нумерований?, лічильник]
        self.pre: dict | None = None      # {"lang", "parts"}
        self.heading: dict | None = None  # {"tag", "id", "num", "parts", "in_num"}
        # Bikeshed не закриває </head> (HTML це дозволяє), тож усе до <body> — шапка
        # сторінки, а не піддерево з парним закриттям.
        self.body = False

    # --- вихід ---------------------------------------------------------------

    def _indent(self) -> str:
        return "   " * len(self.lists)

    def _flush(self) -> None:
        text = _norm("".join(self.buf))
        self.buf = []
        if not text or self.cur is None:
            return
        if re.match(r"#{1,6}\s", text):
            text = "\\" + text
        self.cur["paras"].append(self.prefix + text)
        self.prefix = self._indent()

    def _open(self, num: str, title: str, hid: str, tag: str) -> None:
        self._close()
        self.cur = {"num": num, "title": title, "id": hid, "paras": [],
                    "base": int(tag[1])}
        self.chapters.append(self.cur)

    def _close(self) -> None:
        self._flush()
        self.cur = None

    # --- розбір --------------------------------------------------------------

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if not self.body:
            self.body = tag == "body"
            return
        if tag in _VOID:
            if self.skip_at:
                return
            if tag == "br":
                self._data("\n" if self.pre else " ")
            elif tag == "img" and a.get("alt"):
                self._data(a["alt"])
            return
        self.stack.append(tag)
        if self.skip_at:
            return
        cls = set(a.get("class", "").split())
        if a.get("id") == "toc":
            self.started = True
        if tag in _SKIP or cls & _SKIP_CLASS or "hidden" in a:
            self.skip_at = len(self.stack)
            return
        if self.pre is not None:
            if tag == "code" and not self.pre["lang"]:
                self.pre["lang"] = _lang(cls)
            return
        if self.heading is not None:
            if "secno" in cls:
                self.heading["in_num"] = len(self.stack)
            return
        if tag in _HEADINGS:
            self._flush()
            self.heading = {"tag": tag, "id": a.get("id", ""), "num": [], "parts": [],
                            "in_num": 0}
        elif tag == "pre":
            self._flush()
            self.pre = {"lang": _lang(cls), "parts": []}
        elif tag == "li":
            self._flush()
            if not self.lists:
                self.lists.append([False, 0])
            top = self.lists[-1]
            top[1] += 1
            mark = f"{top[1]}. " if top[0] else "- "
            self.prefix = "   " * (len(self.lists) - 1) + mark
        elif tag in ("ol", "ul", "dl"):
            self._flush()
            self.lists.append([tag == "ol", int(a.get("start") or 1) - 1])
            self.prefix = self._indent()
        elif tag == "dt":
            self._flush()
            self.prefix = "   " * max(len(self.lists) - 1, 0) + "- "
        elif tag == "dd":
            self._flush()
            self.prefix = self._indent()
        elif tag in ("td", "th"):
            if self.buf and _norm("".join(self.buf)):
                self.buf.append(" | ")
        elif tag == "code":
            self.buf.append("`")
        elif tag in _BLOCK:
            self._flush()

    def handle_endtag(self, tag):
        if not self.body or tag in _VOID or tag not in self.stack:
            return
        while self.stack:
            top = self.stack.pop()
            if self.skip_at and len(self.stack) < self.skip_at:
                self.skip_at = 0
                if top == tag:
                    return
                continue
            if self.skip_at:
                if top == tag:
                    return
                continue
            self._end(top)
            if top == tag:
                return

    def _end(self, tag: str) -> None:
        if self.pre is not None:
            if tag == "pre":
                code = re.sub(r"\n{3,}", "\n\n", "".join(self.pre["parts"])).strip("\n")
                lang = self.pre["lang"]
                self.pre = None
                if code.strip() and self.cur is not None:
                    self.cur["paras"].append(f"```{lang}\n{code}\n```")
                    self.prefix = self._indent()
            return
        if self.heading is not None:
            h = self.heading
            if h["in_num"] and len(self.stack) < h["in_num"]:
                h["in_num"] = 0
            if tag == h["tag"]:
                self.heading = None
                self._heading(h)
            return
        if tag in ("ol", "ul", "dl"):
            self._flush()
            if self.lists:
                self.lists.pop()
            self.prefix = self._indent()
        elif tag == "code":
            self.buf.append("`")
        elif tag in _BLOCK or tag in ("li", "dt", "dd"):
            self._flush()

    def _heading(self, h: dict) -> None:
        num = _norm("".join(h["num"])).rstrip(".")
        title = _norm("".join(h["parts"])).replace("`", "")
        if not title and not num:
            return
        level = int(h["tag"][1])
        if self.split and h["tag"] == "h2":
            self._close()
            if (self.started and not _DROP_ALWAYS.match(title)
                    and (num or not _DROP.match(title))):
                self._open(num, title, h["id"], h["tag"])
            return
        if not self.split and not self.chapters:
            self._open(num, title, h["id"], h["tag"])
            return
        if self.cur is None:
            return
        self.lists, self.prefix = [], ""
        depth = min(max(level - self.cur["base"] + 1, 2), 6)
        self.cur["paras"].append("#" * depth + " " + (f"{num} {title}" if num else title))

    def handle_data(self, data):
        if self.skip_at or not self.body:
            return
        self._data(data)

    def _data(self, data: str) -> None:
        if self.pre is not None:
            self.pre["parts"].append(data)
        elif self.heading is not None:
            (self.heading["num"] if self.heading["in_num"] else
             self.heading["parts"]).append(data)
        else:
            self.buf.append(data)

    def close(self):
        super().close()
        self._close()


def _lang(cls: set) -> str:
    if cls & {"idl", "webidl"}:
        return "webidl"
    for c in cls:
        c = re.sub(r"^(?:lang|language|highlight)-", "", c)
        if c in _LANGS:
            return {"javascript": "js", "idl": "webidl"}.get(c, c)
    return ""


def _parse(html: str, split: bool) -> list[dict]:
    parser = _Spec(split)
    parser.feed(html)
    parser.close()
    return parser.chapters


def _chapter_doc(ch: dict, label: str, base: str, stamp: str) -> str:
    head = f"{ch['num']} {ch['title']}".strip()
    title = f"{label}: {head}"
    where = f"{base}#{ch['id']}" if ch["id"] else base
    body = "\n\n".join(ch["paras"]).strip()
    _markup.require(title, body, where, min_chars=1)
    return _markup.document(title, where, stamp, body)


def _items(source: dict, chapters: list[dict], label: str, base: str, ctx) -> list[Item]:
    items, seen = [], set()
    for ch in chapters:
        name = _markup.slug(f"{ch['num']} {ch['title']}")
        if name in seen:
            raise SystemExit(f"{source['id']}: два розділи дають одне ім'я «{name}».")
        seen.add(name)

        def make(ch=ch):
            return _chapter_doc(ch, label, base, ctx.stamp)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


@register("spec-html")
def spec_html(source: dict, ctx) -> list[Item]:
    url = source["url"]
    chapters = _parse(ctx.text(url), split=True)
    if not chapters:
        raise SystemExit(f"{url}: жодного розділу після змісту — розмітка не Bikeshed і "
                         f"не ReSpec або змінилася.")
    return _items(source, chapters, source.get("label") or source["title"],
                  source.get("cite") or url, ctx)


_PAGE = re.compile(r"href=\"?([a-z0-9-]+\.html)[\"#> ]")


@register("whatwg-html")
def whatwg_html(source: dict, ctx) -> list[Item]:
    index = source["url"]
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    pages = []
    for page in _PAGE.findall(ctx.text(index)):
        if page not in pages and not any(r.search(page) for r in exclude):
            pages.append(page)
    if not pages:
        raise SystemExit(f"{index}: у змісті немає посилань на сторінки видання — "
                         f"розмітка змінилася.")
    label = source.get("label") or source["title"]
    items = []
    for page in pages:
        url = urljoin(index, page)
        if not ctx.allowed(url):
            raise SystemExit(f"{source['id']}: {url} поза білим списком.")
        name = _markup.slug(page[:-5])

        def make(url=url):
            chapters = _parse(ctx.text(url), split=False)
            if not chapters:
                raise SystemExit(f"{url}: на сторінці немає заголовка — документ не "
                                 f"записую.")
            return _chapter_doc(chapters[0], label, url, ctx.stamp)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


# ── IETF: текст xml2rfc ────────────────────────────────────────────────────

_FOOTER = re.compile(r"\[Page \d+\]\s*$")
_IETF_HEADING = re.compile(r"^(?:Appendix )?((?:\d+|[A-Z])(?:\.\d+)*)\.?\s{1,3}(\S.*)$")
_IETF_DROP = re.compile(r"^(acknowledge?ments|authors?'? addresses|index|contributors|"
                        r"notices|(normative |informative )?references|copyright notice|"
                        r"full copyright statement|intellectual property)$", re.I)


def _ietf_lines(text: str) -> list[str]:
    """Текст без колонтитулів: нижній — рядок із «[Page N]», верхній — перший непорожній
    рядок сторінки після розриву (у RFC після 8650 сторінок і колонтитулів немає)."""
    out = []
    for i, page in enumerate(text.split("\f")):
        lines = page.splitlines()
        if i:
            while lines and not lines[0].strip():
                lines.pop(0)
            if lines:
                lines.pop(0)
        out.extend(ln.rstrip() for ln in lines if not _FOOTER.search(ln))
    return out


def _ietf_chapters(lines: list[str]) -> list[dict]:
    chapters, cur = [], None
    for ln in lines:
        if ln and not ln[0].isspace():
            m = _IETF_HEADING.match(ln)
            if m and (ln.startswith("Appendix ") or re.match(r"[\dA-Z]+\.", ln)):
                num, title = m.group(1), _norm(m.group(2))
                if "." not in num:
                    cur = None
                    if not _IETF_DROP.match(title):
                        cur = {"num": num, "title": title, "lines": []}
                        chapters.append(cur)
                elif cur is not None:
                    depth = min(num.count(".") + 1, 6)
                    cur["lines"] += ["", "#" * depth + f" {num} {title}", ""]
                continue
            cur = None          # ненумерований заголовок: подяки, адреси, покажчик
            continue
        if cur is not None:
            cur["lines"].append(re.sub(r"^ {1,3}", "", ln))
    return chapters


@register("ietf-text")
def ietf_text(source: dict, ctx) -> list[Item]:
    url = source["url"]
    chapters = _ietf_chapters(_ietf_lines(ctx.text(url)))
    if not chapters:
        raise SystemExit(f"{url}: жодного нумерованого розділу — це не текст xml2rfc.")
    label = source.get("label") or source["title"]
    cite = source.get("cite") or url
    anchors = source.get("anchors", True)
    items, seen = [], set()
    for ch in chapters:
        name = _markup.slug(f"{ch['num']} {ch['title']}")
        if name in seen:
            raise SystemExit(f"{source['id']}: два розділи дають одне ім'я «{name}».")
        seen.add(name)

        def make(ch=ch):
            kind = "appendix" if ch["num"].isalpha() else "section"
            where = f"{cite}#{kind}-{ch['num']}" if anchors else cite
            body = re.sub(r"\n{3,}", "\n\n", "\n".join(ch["lines"])).strip("\n")
            title = f"{label}: {ch['num']} {ch['title']}"
            _markup.require(title, body, where, min_chars=1)
            return _markup.document(title, where, ctx.stamp, body)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items


# ── ERC: markdown з шапкою ─────────────────────────────────────────────────

@register("erc-md")
def erc_md(source: dict, ctx) -> list[Item]:
    page = source.get("page", "")
    if not page.startswith("https://"):
        raise SystemExit(f"{source['id']}: читач erc-md вимагає поле `page`.")

    def make():
        text = ctx.text(source["url"])
        _markup.refuse_html(text, source["url"])
        meta, rest = _markup.front_matter(text)
        num = meta.get("eip") or meta.get("erc")
        if not num or not meta.get("title"):
            raise SystemExit(f"{source['url']}: у шапці немає номера чи назви ERC.")
        title = f"ERC-{num}: {meta['title']}"
        facts = [f"{k.capitalize()}: {meta[k].rstrip('.')}." for k in
                 ("description", "status", "type", "category", "created", "requires")
                 if meta.get(k)]
        body = " ".join(facts) + "\n\n" + _markup.markdown_body(rest)
        _markup.require(title, body, page)
        return _markup.document(title, page, ctx.stamp, body)

    name = _markup.slug(page.rsplit("/", 1)[-1])
    return [Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt",
                 make=make)]
