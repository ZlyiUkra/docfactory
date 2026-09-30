"""Читач специфікації, зібраної Bikeshed, з формулами KaTeX: одна сторінка — документ на розділ.

`bikeshed` — `url` — сторінка специфікації однією сторінкою (Bikeshed: заголовки з
             `data-level="2.2.1"` і `<span class="secno">`), поле `version` — мітка
             видання, `label` — назва специфікації в назві документа («WebAssembly
             Core»), `prefix` — початок імені документа («core»): у core, JS API і
             Web API є свій «1 Introduction», а ім'я — ключ, за яким той самий
             розділ різних видань зливається. Кожен нумерований розділ верхнього
             рівня (`<h2 data-level="4">`) стає документом «core-4-execution»;
             підрозділи — заголовками «## 4.4 …»,
             «### 4.4.5 …» з номерами, як у самій специфікації. Ненумеровані розділи
             (Abstract, Status, Index, References) не беруться: там покажчики й
             службовий текст, а не норма.

Навіщо окремий читач. Специфікація WebAssembly (і core, і JS API) пише правила
формулами, і на сторінці вони вже відрендерені KaTeX-ом у HTML — вихідного TeX поруч
немає. Прочитати таку сторінку як звичайний HTML означало б отримати «premise1premise2
…conclusion» замість правила виведення: KaTeX розкладає формулу вертикальними списками
(`vlist`) зі зсувом `top`, і лише за зсувом видно, що над чим. Тут формула збирається
назад у рядок:

- верхній і нижній індекси (`msupsub`) — за знаком зсуву відносно базової лінії:
  `t*`, `t^(n)`, `t_1`; зірочка, плюс і знак питання після символу лишаються як є —
  саме так специфікація пише послідовність, непорожню послідовність і необов'язкове;
- дріб (`mfrac`) у виносній формулі — правило виведення: «засновки ⟹ висновок»; у
  рядку тексту — звичайний дріб `(a)/(b)`;
- таблиця (`mtable`, граматики й групи правил) — рядок таблиці на рядок тексту,
  клітинки через пробіл;
- решта вертикальних списків (надписи над стрілкою, межі) — згори донизу через пробіл.

Сторінки великі (core 2.0 — 18 МБ), тому розбір потоковий: у дерево збирається лише
одна формула за раз, а готовий текст розділів пишеться в тимчасові файли й читається
знову під час запису, як у `npm-versions`.
"""

import os
import re
import tempfile
from html.parser import HTMLParser
from urllib.parse import urldefrag

from engine.readers import Item, _markup, register

_SKIP = {"script", "style", "nav", "template", "svg", "button"}
_SKIP_CLASS = {"self-link", "dfn-panel", "katex-mathml", "mdn-anno", "wpt-tests-block",
               "annotation", "toc"}
_VOID = {"br", "img", "hr", "wbr", "meta", "link", "input", "col", "source", "area"}
_BLOCK = {"p", "div", "section", "blockquote", "figure", "figcaption", "table", "thead",
          "tbody", "tfoot", "dl", "details", "summary", "main", "article",
          "header", "footer", "aside"}
_ROW_SEP = " | "
_TOP = re.compile(r"top:\s*(-?[\d.]+)em")
_HEIGHT = re.compile(r"height:\s*(-?[\d.]+)em")
_SPACE = re.compile(r"[ \t    ]+")
# Позначки, що після символу стоять верхнім індексом, але читаються як частина
# імені: t* — послідовність, t+ — непорожня, t? — необов'язкова, t′ — штрих.
_PUNCT = re.compile(r" ([.,;:!?)])")
_APPENDIX = re.compile(r"^([A-Z])\.?\s+(\S.*)$")
_BARE_SUP = {"∗", "*", "+", "?", "′", "″", "'"}


def _classes(attrs: dict) -> set:
    return set((attrs.get("class") or "").split())


class _Node:
    __slots__ = ("tag", "attrs", "children")

    def __init__(self, tag: str, attrs: dict):
        self.tag = tag
        self.attrs = attrs
        self.children: list = []


def _vlist_rows(node: "_Node") -> list[tuple[float, float, "_Node"]]:
    """Рядки вертикального списку KaTeX: (top, зсув від базової лінії, вузол).
    Зсув < 0 — вище базової лінії (верхній індекс, чисельник), > 0 — нижче."""
    rows = []

    def walk(n):
        for c in n.children:
            if not isinstance(c, _Node):
                continue
            cls = _classes(c.attrs)
            if "vlist" in cls:
                for r in c.children:
                    if not isinstance(r, _Node):
                        continue
                    m = _TOP.search(r.attrs.get("style") or "")
                    if not m:
                        continue
                    top = float(m.group(1))
                    height = 0.0
                    for s in r.children:
                        if isinstance(s, _Node) and "pstrut" in _classes(s.attrs):
                            h = _HEIGHT.search(s.attrs.get("style") or "")
                            height = float(h.group(1)) if h else 0.0
                    rows.append((top, top + height, r))
            elif cls & {"vlist-t", "vlist-r", "vlist-t2"}:
                walk(c)

    walk(node)
    rows.sort(key=lambda r: r[0])
    return rows


def _has_vlist(node: "_Node") -> bool:
    return any(isinstance(c, _Node) and "vlist-t" in _classes(c.attrs) for c in node.children)


def _tight(text: str) -> str:
    return _SPACE.sub(" ", text).strip()


def _math(node, display: bool) -> str:
    """Формула KaTeX (вузол `katex-html`) — рядком тексту."""
    if not isinstance(node, _Node):
        return node.replace("​", "")
    cls = _classes(node.attrs)
    if cls & {"strut", "pstrut", "vlist-s", "frac-line", "katex-mathml"}:
        return ""
    if cls & {"mspace", "arraycolsep"}:
        return " "
    if "msupsub" in cls:
        # Нижній індекс — першим: специфікація пише t_1*, «перша послідовність t».
        sub = sup = ""
        for _top, shift, row in _vlist_rows(node):
            piece = _tight("".join(_math(c, display) for c in row.children))
            if not piece:
                continue
            if shift < 0:
                sup += piece if piece in _BARE_SUP else (
                    f"^{piece}" if len(piece) == 1 else f"^({piece})")
            else:
                sub += f"_{piece}" if len(piece) == 1 else f"_({piece})"
        return sub + sup
    if "mfrac" in cls:
        above, below = [], []
        for _top, shift, row in _vlist_rows(node):
            piece = _tight("".join(_math(c, display) for c in row.children))
            if piece:
                (above if shift < 0 else below).append(piece)
        num, den = " ".join(above), " ".join(below)
        if display:
            return f"{num} ⟹ {den}" if num else f"⟹ {den}"
        return f"({num})/({den})"
    if "mtable" in cls:
        cells: dict = {}
        for col in node.children:
            if not isinstance(col, _Node):
                continue
            if not any(k.startswith("col-align") for k in _classes(col.attrs)):
                continue
            for top, _shift, row in _vlist_rows(col):
                piece = _tight("".join(_math(c, display) for c in row.children))
                if piece:
                    cells.setdefault(round(top, 1), []).append(piece)
        return "\n".join("  ".join(cells[t]) for t in sorted(cells))
    if _has_vlist(node):
        rows = _vlist_rows(node)
        if rows:
            text = " ".join(_tight("".join(_math(c, display) for c in r.children))
                            for _t, _s, r in rows)
            rest = "".join(_math(c, display) for c in node.children
                           if not (isinstance(c, _Node) and "vlist-t" in _classes(c.attrs)))
            return rest + text
    return "".join(_math(c, display) for c in node.children)


class _Page(HTMLParser):
    """Потоковий розбір сторінки Bikeshed: текст нумерованих розділів верхнього
    рівня, кожен — у свій тимчасовий файл."""

    def __init__(self, store: str):
        super().__init__(convert_charrefs=True)
        self.store = store
        self.chapters: list[dict] = []   # {"num", "title", "id", "path"}
        self.fh = None
        self.skip = 0                     # глибина пропущеного піддерева
        self.stack: list[str] = []        # відкриті теги поза формулами
        self.skip_at: list[int] = []      # глибини, де почався пропуск
        self.math: list[_Node] | None = None
        self.math_display = False
        self.display_depth = -1
        self.line: list[str] = []
        self.pre = 0
        self.heading: dict | None = None  # {"level", "num", "id", "parts"}
        self.prefix = ""
        # Bikeshed не закриває </head> (HTML це дозволяє), тож усе до <body> —
        # шапка сторінки, а не пропуск із парним закриттям.
        self.body = False
        # Відкриті списки: [нумерований?, лічильник]. Кроки алгоритмів специфікації —
        # вкладені <ol>, і без номерів і відступів «If …, then: Trap.» читалося б як
        # два незалежні речення.
        self.lists: list[list] = []

    # --- вихід ---------------------------------------------------------------

    def _emit(self, text: str) -> None:
        if self.heading is not None:
            self.heading["parts"].append(text)
        elif self.fh is not None:
            self.line.append(text)

    def _flush(self) -> None:
        if self.fh is None or self.pre:
            return
        # Формула в реченні дістає пробіли з обох боків; перед розділовим знаком
        # пробіл зайвий.
        text = _PUNCT.sub(r"\1", _tight("".join(self.line)))
        self.line = []
        if text:
            # Префікс пункту списку витрачається лише на перший непорожній абзац
            # пункту: <li><p>…</p></li> спершу скидає порожній рядок.
            self.fh.write(self.prefix + text + "\n\n")
            self.prefix = "   " * len(self.lists) if self.lists else ""

    def _open_chapter(self, num: str, title: str, hid: str) -> None:
        self._close_chapter()
        path = os.path.join(self.store, f"{len(self.chapters):03d}.txt")
        self.fh = open(path, "w", encoding="utf-8")
        self.chapters.append({"num": num, "title": title, "id": hid, "path": path})

    def _close_chapter(self) -> None:
        if self.fh is not None:
            self._flush()
            self.fh.close()
            self.fh = None

    # --- розбір --------------------------------------------------------------

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if self.math is not None:
            node = _Node(tag, a)
            self.math[-1].children.append(node)
            if tag not in _VOID:
                self.math.append(node)
            return
        if not self.body:
            self.body = tag == "body"
            return
        if tag in _VOID:
            if tag == "br" and not self.skip:
                self._emit("\n" if self.pre else " ")
            return
        self.stack.append(tag)
        cls = _classes(a)
        if self.skip or tag in _SKIP or cls & _SKIP_CLASS:
            if not self.skip:
                self.skip_at.append(len(self.stack))
                self.skip = 1
            return
        if "katex-display" in cls:
            self.math_display = True
            self.display_depth = len(self.stack)
            return
        if "katex-html" in cls:
            self.math = [_Node(tag, a)]
            return
        m = re.fullmatch(r"h([2-6])", tag)
        if m:
            level = int(m.group(1))
            num = a.get("data-level", "")
            if level == 2:
                if num:
                    self.heading = {"level": 2, "num": num, "id": a.get("id", ""),
                                    "parts": []}
                else:
                    # Ненумерований розділ верхнього рівня — покажчик чи службовий
                    # текст: усе до наступного нумерованого розділу пропускається.
                    self._close_chapter()
                    self.heading = {"level": 2, "num": "", "id": a.get("id", ""),
                                    "parts": []}
                return
            self._flush()
            self.heading = {"level": level, "num": num, "id": a.get("id", ""), "parts": []}
            return
        if tag == "pre":
            self._flush()
            self.pre += 1
            self._emit("```\n")
            return
        if tag == "code" and not self.pre:
            self._emit("`")
            return
        if tag in ("ol", "ul"):
            self._flush()
            self.lists.append([tag == "ol", 0])
            return
        if tag == "li":
            self._flush()
            depth = max(len(self.lists), 1)
            mark = "-"
            if self.lists:
                self.lists[-1][1] += 1
                if self.lists[-1][0]:
                    mark = f"{self.lists[-1][1]}."
            self.prefix = "   " * (depth - 1) + mark + " "
            return
        if tag in ("dt", "dd", "tr"):
            self._flush()
            return
        if tag in ("td", "th"):
            if self.line:
                self._emit(_ROW_SEP)
            return
        if tag in _BLOCK:
            self._flush()

    def handle_endtag(self, tag):
        if self.math is not None:
            if len(self.math) == 1 and self.math[0].tag == tag:
                node = self.math[0]
                self.math = None
                text = _math(node, True)
                # Bikeshed загортає в katex-display і формули посеред речення.
                # Окремим рядком іде лише справжня виносна формула: правило
                # виведення (дріб) чи таблиця граматики; решта лишається в реченні.
                if self.math_display and ("\n" in text or "⟹" in text):
                    self._flush()
                    for row in text.split("\n"):
                        row = _tight(row)
                        if row and self.fh is not None and self.heading is None:
                            self.fh.write("    " + row + "\n")
                    if self.fh is not None and self.heading is None:
                        self.fh.write("\n")
                    else:
                        self._emit(_tight(text))
                else:
                    self._emit(" " + _tight(text) + " ")
                return
            # Закривається вкладений тег формули: знімаємо до нього.
            for i in range(len(self.math) - 1, 0, -1):
                if self.math[i].tag == tag:
                    del self.math[i:]
                    break
            return
        if tag in _VOID:
            return
        if tag not in self.stack:
            return
        while self.stack:
            depth = len(self.stack)
            top = self.stack.pop()
            if self.skip_at and self.skip_at[-1] == depth:
                self.skip_at.pop()
                self.skip = 0
            if self.display_depth == depth:
                self.math_display = False
                self.display_depth = -1
            if top == tag:
                break
        if self.skip:
            return
        if self.heading is not None and re.fullmatch(r"h[2-6]", tag):
            h = self.heading
            self.heading = None
            text = _tight("".join(h["parts"]))
            if h["level"] == 2:
                if h["num"]:
                    title = re.sub(r"^" + re.escape(h["num"]) + r"\.?\s*", "", text)
                    self._open_chapter(h["num"], title, h["id"])
                    return
                # Додаток Bikeshed не нумерує (`no-num`), але літера стоїть у самій
                # назві: «A Appendix», підрозділи — «A.1 Embedding». Це норма, як і
                # нумеровані розділи; решта ненумерованих — службові.
                m = _APPENDIX.match(text)
                if m:
                    self._open_chapter(m.group(1), m.group(2), h["id"])
                return
            if self.fh is not None and text:
                num = h["num"]
                title = re.sub(r"^" + re.escape(num) + r"\.?\s*", "", text) if num else text
                self.fh.write("#" * (h["level"] - 1) + " "
                              + (f"{num} {title}" if num else title) + "\n\n")
            return
        if tag == "pre":
            self._emit("\n```")
            self.pre -= 1
            if self.fh is not None and not self.pre:
                self.fh.write("".join(self.line).strip("\n") + "\n\n")
                self.line = []
            return
        if tag == "code" and not self.pre:
            self._emit("`")
            return
        if tag in ("ol", "ul"):
            self._flush()
            if self.lists:
                self.lists.pop()
            self.prefix = "   " * len(self.lists) if self.lists else ""
            return
        if tag in ("li", "dt", "dd", "tr") or tag in _BLOCK:
            self._flush()

    def handle_data(self, data):
        if self.skip or not self.body:
            return
        if self.math is not None:
            self.math[-1].children.append(data)
            return
        self._emit(data if self.pre else data.replace("\n", " "))

    def close(self):
        super().close()
        self._close_chapter()


def _pre_safe(text: str) -> str:
    """Рядки коду в огорожі не мають починатися з «#»: інакше поділ корпусу прийме
    їх за заголовок. Огорожу поділ бачить, тож досить прибрати зайві порожні рядки."""
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


@register("bikeshed")
def bikeshed(source: dict, ctx) -> list[Item]:
    url = source["url"]
    version = str(source.get("version") or "")
    label = source.get("label") or "Specification"
    cite = source.get("cite") or url
    page = ctx.text(url)
    store = tempfile.mkdtemp(prefix=f"bikeshed-{source['id']}-")
    parser = _Page(store)
    parser.feed(page)
    parser.close()
    del page
    if not parser.chapters:
        raise SystemExit(f"{url}: жодного нумерованого розділу (h2 з data-level) — "
                         f"розмітка не Bikeshed або змінилася.")
    items = []
    for ch in parser.chapters:
        name = _markup.slug(f"{source.get('prefix', '')} {ch['num']} {ch['title']}")
        base = urldefrag(cite)[0]

        def make(ch=ch, base=base):
            with open(ch["path"], encoding="utf-8") as fh:
                body = _pre_safe(fh.read())
            title = f"{label} {version}: {ch['num']} {ch['title']}".replace("  ", " ")
            where = f"{base}#{ch['id']}" if ch["id"] else base
            _markup.require(title, body, where, min_chars=1)
            return _markup.document(title, where, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
