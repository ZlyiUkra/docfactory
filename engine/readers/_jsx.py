"""Текст сторінки, що живе в коді React: JSX, дані сторінок в об'єктах TSX, приклади в шаблонних рядках.

Сайти 2019–2023 років (react-hook-form.com на Create React App, потім на Gatsby) не мали
markdown: текст документації лежав прямо в компонентах (`<p>…</p>` усередині `Api.tsx`)
або в об'єктах даних (`useForm: { title: "useForm", description: (<p>…</p>) }`), а приклади
коду — у модулях `export default \\`…\\``. Щоб такий текст ліг у корпус, файл читається
тут простим сканером мови, без Node і без бібліотек: повного розбору TypeScript пошуку
не треба, треба відрізнити текст від коду.

Що береться:
- текст між тегами JSX; `h1`–`h6` і styled-компоненти з «Title»/«Heading» у назві стають
  заголовками, `li` — пунктом списку, `code` — `кодом`, `pre` — огородженим кодом, рядок
  таблиці — клітинками через « | »;
- рядок у лапках поза JSX — лише коли схожий на прозу (кілька слів) або стоїть під ключем
  `title`/`label`/`description`: інакше в текст лізли б класи, адреси й значення CSS;
- ключ об'єкта, під яким лежить інший об'єкт (`useForm: {…}`), — заголовок розділу: саме так
  дані сторінки діляться на API-методи;
- нетегований багаторядковий шаблонний рядок — приклад коду між огорожами.

Що відкидається: імпорти, коментарі, стилі (`styled.div\\`…\\``, `css\\`…\\``), атрибути
тегів, вирази в `{…}` без JSX і без рядків. Сканер не падає на тому, чого не впізнав: у
гіршому разі частина тексту губиться, а не весь файл.
"""

import re

_WORD = re.compile(r"[A-Za-z][A-Za-z'’-]+")
_IDENT = re.compile(r"[A-Za-z_$][\w$]*")
# Після цих слів «<» відкриває JSX, а «/» — регулярний вираз, а не порівняння чи ділення.
_KEYWORDS = {"return", "yield", "default", "case", "else", "await", "typeof", "in", "of",
             "do", "void", "new", "delete", "throw"}
_PROSE_KEYS = {"title", "label", "description", "intro", "subTitle", "subtitle", "header",
               "note", "text", "message", "content", "tip", "warning"}
_BLOCK = {"p", "div", "section", "article", "main", "header", "footer", "aside", "ul", "ol",
          "table", "thead", "tbody", "blockquote", "br", "hr", "nav", "figure", "details",
          "summary", "form", "fieldset", "dl", "dd", "dt"}
_HEADING_TAG = re.compile(r"^h([1-6])$")
_HEADING_NAME = re.compile(r"(Title|Heading)")
_STYLE_TAGS = re.compile(r"(^|\.)(styled|css|keyframes|createGlobalStyle|injectGlobal|"
                         r"styled\.[\w$]+|styled\([^)]*\)|gql|graphql)$")
_SKIP_TAGS = {"style", "script", "svg", "path", "Helmet", "SEO", "Seo", "Head", "Link_"}


def _prose(s: str, key: str = "") -> bool:
    s = s.strip()
    if not s or "\n" in s and len(s) > 400:
        return False
    if key in _PROSE_KEYS:
        return bool(_WORD.search(s))
    if re.match(r"^(https?:|/|\.|#|[\w-]+\.(tsx?|jsx?|css|png|svg))", s):
        return False
    words = _WORD.findall(s)
    return len(words) >= 3 and sum(map(len, words)) >= len(s) * 0.55


class _Scan:
    def __init__(self, src: str):
        self.s = src.replace("\r\n", "\n")
        self.n = len(self.s)
        self.out: list[str] = []

    # ── низ: пропуск рядків, коментарів, регулярних виразів ──

    def skip_string(self, i: int) -> tuple[str, int]:
        q = self.s[i]
        j = i + 1
        buf = []
        while j < self.n and self.s[j] != q:
            if self.s[j] == "\\" and j + 1 < self.n:
                nxt = self.s[j + 1]
                buf.append({"n": "\n", "t": "\t"}.get(nxt, nxt))
                j += 2
                continue
            if self.s[j] == "\n":
                break
            buf.append(self.s[j])
            j += 1
        return "".join(buf), j + 1

    def skip_template(self, i: int) -> tuple[str, int]:
        """Шаблонний рядок від «`»: (текст з `${…}` як є, позиція за ним)."""
        j = i + 1
        buf = []
        while j < self.n and self.s[j] != "`":
            c = self.s[j]
            if c == "\\" and j + 1 < self.n:
                buf.append(self.s[j + 1] if self.s[j + 1] in "`$\\" else self.s[j:j + 2])
                j += 2
                continue
            if c == "$" and j + 1 < self.n and self.s[j + 1] == "{":
                k = self.skip_braces(j + 1)
                buf.append(self.s[j:k])
                j = k
                continue
            buf.append(c)
            j += 1
        return "".join(buf), j + 1

    def skip_braces(self, i: int) -> int:
        """Від «{» до позиції за парною «}», з урахуванням рядків і коментарів."""
        depth = 0
        j = i
        while j < self.n:
            c = self.s[j]
            if c in "\"'":
                j = self.skip_string(j)[1]
                continue
            if c == "`":
                j = self.skip_template(j)[1]
                continue
            if self.s.startswith("//", j):
                j = self.s.find("\n", j)
                j = self.n if j < 0 else j
                continue
            if self.s.startswith("/*", j):
                j = self.s.find("*/", j + 2)
                j = self.n if j < 0 else j + 2
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return j + 1
            j += 1
        return self.n

    def skip_regex(self, i: int) -> int:
        j = i + 1
        klass = False
        while j < self.n and self.s[j] != "\n":
            c = self.s[j]
            if c == "\\":
                j += 2
                continue
            if c == "[":
                klass = True
            elif c == "]":
                klass = False
            elif c == "/" and not klass:
                j += 1
                while j < self.n and self.s[j].isalpha():
                    j += 1
                return j
            j += 1
        return i + 1

    def prev_token(self, i: int) -> str:
        """Попередній значущий знак або слово перед позицією i."""
        j = i - 1
        while j >= 0 and self.s[j] in " \t\n":
            j -= 1
        if j < 0:
            return ""
        if self.s[j].isalnum() or self.s[j] in "_$":
            k = j
            while k >= 0 and (self.s[k].isalnum() or self.s[k] in "_$"):
                k -= 1
            return self.s[k + 1:j + 1]
        if self.s[j] == ">" and j > 0 and self.s[j - 1] == "=":
            return "=>"
        return self.s[j]

    def expr_start(self, i: int) -> bool:
        """Чи стоїть позиція там, де починається вираз (а не де триває операнд)."""
        p = self.prev_token(i)
        if not p:
            return True
        if p[0].isalnum() or p[0] in "_$":
            return p in _KEYWORDS
        return p in ("(", "[", ",", "=", ":", "?", "&", "|", "!", "{", "}", ";", "=>", "+",
                     "-", "*", "%", "~", "^", "<", ">")

    # ── рівень JS ──

    def js(self, i: int, end: int, depth: int = 0) -> None:
        """Прохід коду між i та end: рядки-проза, ключі-розділи, шаблони-приклади, JSX."""
        key = ""
        while i < end:
            c = self.s[i]
            if self.s.startswith("//", i):
                i = self.s.find("\n", i)
                i = end if i < 0 else i
                continue
            if self.s.startswith("/*", i):
                i = self.s.find("*/", i + 2)
                i = end if i < 0 else i + 2
                continue
            if c in "\"'":
                text, i = self.skip_string(i)
                if _prose(text, key):
                    self.out.append(f"\n{text.strip()}\n")
                key = ""
                continue
            if c == "`":
                tag = self.tag_before(i)
                text, i = self.skip_template(i)
                if not _STYLE_TAGS.search(tag) and "\n" in text.strip("\n"):
                    self.out.append("\n```\n" + text.strip("\n") + "\n```\n")
                continue
            if c == "/" and self.expr_start(i):
                i = self.skip_regex(i)
                continue
            if c == "<" and self.expr_start(i) and i + 1 < end and (
                    self.s[i + 1].isalpha() or self.s[i + 1] == ">"):
                i = self.element(i, end)
                key = ""
                continue
            if c == "{":
                close = self.skip_braces(i) - 1
                if key and self.prev_token(i) == ":":
                    level = min(2 + depth, 6)
                    self.out.append(f"\n{'#' * level} {key}\n")
                    self.js(i + 1, close, depth + 1)
                else:
                    self.js(i + 1, close, depth)
                i = close + 1
                key = ""
                continue
            m = _IDENT.match(self.s, i)
            if m and (i == 0 or not (self.s[i - 1].isalnum() or self.s[i - 1] in "_$.")):
                word = m.group(0)
                j = m.end()
                while j < end and self.s[j] in " \t":
                    j += 1
                key = word if j < end and self.s[j] == ":" and word not in _KEYWORDS else ""
                if word in ("import", "export") and self.at_line_start(i):
                    stop = self.import_end(j)
                    if stop:
                        i = stop
                        continue
                i = m.end()
                continue
            if c not in " \t\n:":
                key = ""
            i += 1

    def at_line_start(self, i: int) -> bool:
        k = self.s.rfind("\n", 0, i)
        return not self.s[k + 1:i].strip()

    def import_end(self, j: int) -> int:
        """Кінець оператора import/export … from '…' (0, якщо це не він)."""
        m = re.compile(r"[^;`]*?\bfrom\s*(['\"])[^'\"\n]*\1;?|\s*(['\"])[^'\"\n]*\2;?"
                       ).match(self.s, j)
        return m.end() if m else 0

    def tag_before(self, i: int) -> str:
        j = i - 1
        while j >= 0 and self.s[j] in " \t\n":
            j -= 1
        if j >= 0 and self.s[j] == ")":
            depth, k = 0, j
            while k >= 0:
                if self.s[k] == ")":
                    depth += 1
                elif self.s[k] == "(":
                    depth -= 1
                    if depth == 0:
                        break
                k -= 1
            j = k - 1
            end = k
        else:
            end = j + 1
        k = j
        while k >= 0 and (self.s[k].isalnum() or self.s[k] in "_$."):
            k -= 1
        return self.s[k + 1:end] if end > k + 1 else ""

    # ── рівень JSX ──

    def open_tag(self, i: int) -> tuple[str, bool, int, dict]:
        """(ім'я, самозакритий, позиція за «>», атрибути-рядки) тегу від «<»."""
        m = re.compile(r"<\s*([\w$.:-]*)").match(self.s, i)
        name = m.group(1)
        j = m.end()
        attrs = {}
        while j < self.n:
            c = self.s[j]
            if c == "{":
                k = self.skip_braces(j)
                # Render-проп (`render={({ style }) => <Root>…</Root>}`) несе всю сторінку.
                if re.search(r"<[A-Za-z>]", self.s[j:k]):
                    self.js(j + 1, k - 1)
                j = k
                continue
            if c in "\"'":
                val, j2 = self.skip_string(j)
                a = re.search(r"([\w-]+)\s*=\s*$", self.s[max(i, j - 40):j])
                if a:
                    attrs[a.group(1)] = val
                j = j2
                continue
            if c == "/" and self.s.startswith("/>", j):
                return name, True, j + 2, attrs
            if c == ">":
                return name, False, j + 1, attrs
            j += 1
        return name, True, self.n, attrs

    def element(self, i: int, end: int) -> int:
        start = len(self.out)
        name, selfclosing, j, attrs = self.open_tag(i)
        if name.startswith("h") and _HEADING_TAG.match(name):
            level = int(name[1])
        elif name[:1].isupper() and _HEADING_NAME.search(name):
            level = 2
        else:
            level = 0
        if selfclosing:
            if name in _BLOCK:
                self.out.append("\n")
            for a in ("title", "alt", "label"):
                if attrs.get(a) and _prose(attrs[a], "title"):
                    self.out.append(f"\n{attrs[a]}\n")
            return j
        j = self.children(j, end, name)
        if name.split(".")[0] in _SKIP_TAGS:
            del self.out[start:]
            return j
        inner = self.out[start:]
        del self.out[start:]
        text = "".join(inner)
        if level:
            flat = " ".join(text.replace("```", "").split()).strip()
            if flat:
                self.out.append(f"\n\n{'#' * max(2, level)} {flat}\n\n")
        elif name == "code":
            flat = text.strip()
            # Заголовок чи блок коду всередині <code> (так писав перший сайт) — уже розмітка.
            if "\n#" in text or "```" in flat:
                self.out.append(text)
            elif "\n" in flat:
                self.out.append("\n```\n" + flat + "\n```\n")
            else:
                self.out.append(f"`{' '.join(flat.split())}`" if flat else "")
        elif name == "pre":
            body = text.strip("\n").replace("```\n", "").replace("\n```", "").strip("`")
            self.out.append("\n```\n" + body + "\n```\n")
        elif name == "li":
            # Пункт з блоком коду зберігає рядки: стиснутий в один рядок, код ламається.
            item = text.strip() if "```" in text else " ".join(text.split())
            self.out.append("\n- " + item + "\n")
        elif name == "tr":
            cells = [c.strip() for c in text.split("\x00") if c.strip()]
            self.out.append("\n" + " | ".join(" ".join(c.split()) for c in cells) + "\n")
        elif name in ("td", "th"):
            self.out.append("\x00" + text + "\x00")
        elif name in _BLOCK:
            self.out.append("\n" + text + "\n")
        else:
            self.out.append(text)
        return j

    def children(self, j: int, end: int, name: str) -> int:
        """Діти тегу name від позиції j до його закриття; позиція за «</name>»."""
        buf: list[str] = []

        def flush():
            if buf:
                raw = "".join(buf)
                # Пробіли JSX: рядок, що переходить на новий, стискається в один пробіл.
                text = re.sub(r"\s*\n\s*", " ", raw)
                if name == "pre" or name == "code":
                    text = raw
                self.out.append(text)
                buf.clear()

        while j < end:
            c = self.s[j]
            if c == "<":
                if self.s.startswith("</", j):
                    k = self.s.find(">", j)
                    flush()
                    return end if k < 0 else k + 1
                if j + 1 < end and (self.s[j + 1].isalpha() or self.s[j + 1] == ">"):
                    flush()
                    j = self.element(j, end)
                    continue
            if c == "{":
                flush()
                close = self.skip_braces(j) - 1
                self.container(j + 1, close, name)
                j = close + 1
                continue
            buf.append(c)
            j += 1
        flush()
        return end

    def container(self, i: int, close: int, name: str) -> None:
        """Вираз `{…}` усередині JSX: рядок чи шаблон — текст, решта — прохід JS."""
        inner = self.s[i:close].strip()
        if not inner or inner.startswith("/*"):
            return
        if inner[0] in "\"'" and self.skip_string(self.s.index(inner[0], i))[1] > close - 1:
            self.out.append(self.skip_string(self.s.index(inner[0], i))[0])
            return
        if inner[0] == "`" and inner.endswith("`"):
            text = self.skip_template(self.s.index("`", i))[0]
            if "\n" in text.strip("\n") and name not in ("code", "pre"):
                self.out.append("\n```\n" + text.strip("\n") + "\n```\n")
            else:
                self.out.append(text)
            return
        start = len(self.out)
        self.js(i, close)
        # Рядок-проза у виразі JSX ({cond ? "так" : "ні"}) — текст абзацу, а не окремий абзац.
        for k in range(start, len(self.out)):
            piece = self.out[k]
            if piece.startswith("\n") and piece.endswith("\n") and not piece.startswith(
                    ("\n#", "\n```", "\n- ", "\n\n")):
                self.out[k] = " " + piece.strip() + " "


def text_of(src: str) -> str:
    """Markdown-подібний текст файла коду. Порожній — якщо тексту для людей у ньому немає."""
    scan = _Scan(src)
    try:
        scan.js(0, scan.n)
    except (IndexError, RecursionError, AttributeError):
        pass
    text = "".join(scan.out).replace("\x00", " ")
    lines = [ln.rstrip() for ln in text.split("\n")]
    out: list[str] = []
    fence = False
    for ln in lines:
        if ln.startswith("```"):
            fence = not fence
            out.append(ln)
            continue
        out.append(ln if fence else " ".join(ln.split()) if not ln.lstrip().startswith("#")
                   else ln.strip())
    return "\n".join(out)


def title_of(src: str) -> str:
    """`title: "…"` першим полем `export default {…}` — назва сторінки даних. Будь-яке
    інше `title` (підпис відео, атрибут тегу) назвою файла не є."""
    m = re.search(r"export\s+default\s*\{\s*title\s*:\s*([\"'])(.+?)\1", src)
    return m.group(2).strip() if m else ""
