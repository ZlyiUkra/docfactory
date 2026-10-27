"""Читач сайту go.dev з репозиторіїв golang/website і golang/go: markdown і HTML з діями шаблону сайту,
статті й доповіді у форматі present.

`ghdocs-history-godev` — поля ті самі, що в `ghdocs-history` (`url`, `tags`, `folders`, `recursive`, `files`,
                         `extensions`, `exclude`, `site`, `path_version`, `name_prefix` …). Текст кожного файла
                         перед розбором стає markdown:
                         - `.md` — дії шаблону сайту: `{{code "файл" `/від/` `/до/`}}` і `{{play …}}` стають
                           блоком коду з файла поруч (шлях відносно теки сторінки, «/…» — від теки `content`),
                           `{{raw `…`}}` — своїм вмістом, `{{image …}}` випадає, `{{video "адреса"}}` стає
                           рядком «Video: адреса». Інших `{{…}}` читач не чіпає: у примітках до випусків це
                           приклади text/template. Шапка блогу (`date`, `by`) стає першим рядком тексту;
                           сторінка без YAML-шапки, але з JSON-шапкою `<!--{ "Title": … }-->` (посібники
                           database/sql, модулі), бере назву з неї, як `.html`;
                         - `.html` — шапка `<!--{ "Title": …, "Subtitle": … }-->` дає назву й рядок під нею,
                           ті самі дії шаблону, далі HTML → markdown;
                         - `.article`, `.slide` — формат present (Tour of Go, доповіді): назва й підзаголовок
                           з шапки, `* `/`** `/`*** ` → `##`/`###`/`####`, рядки з відступом → блок коду,
                           `.code`/`.play файл [адреса]` → блок коду з файла, `.link адреса текст` і `[[адреса][текст]]` → посилання
                           markdown; `.image`, `.background`, `.iframe`, `.html`, `.caption` випадають, рядок
                           з `//` на початку — коментар автора.
                         Необов'язкове `content` — тека, від якої рахуються шляхи «/…» (типово `_content`).
                         Сторінка-переадресація (`"Redirect"` у шапці JSON, `redirect:` у YAML) стає порожньою:
                         на сайті її тексту немає, лише перехід на іншу адресу.
                         `literate` — шлях файла з назвами прикладів (`examples.txt` Go by Example): тоді
                         файл `.go` — приклад, де коментарі `//` — текст, а решта — код, і поруч лежить
                         `.sh` з командою й виводом; назва прикладу — рядок файла назв, чий slug збігся з
                         текою прикладу.

Навіщо. go.dev збирає сервер golang.org/x/website з теки `_content`: сторінки — markdown з шапкою YAML або
HTML з шапкою JSON у коментарі, а код у блозі, примітках до Go 1 і Effective Go вставляється з файлів `.go`
поруч дією `{{code}}`. Спільний `ghdocs-history` лишив би на місці коду рядок `{{code "pipelines/sqfan.go"
…}}`, а HTML відкинув би як сторінку помилки. Tour of Go і доповіді (`talks/`) написано у форматі present —
своєму синтаксисі заголовків і вставок коду.

Вибір рядків коду — як у present: адреса `/вираз/` — перший рядок, що збігся; `/від/,/до/` — від рядка
першого збігу до рядка другого включно; число — номер рядка, `$` — останній. Рядки, що закінчуються на
`OMIT`, випадають, мітки підсвітки `// HL…` знімаються. Адреса, якої у файлі немає, дає файл цілком: краще
зайвий код, ніж розділ без коду. Вставлений файл не робить сторінку новою редакцією — редакцію рахує
`ghdocs-history` за вмістом самої сторінки, а сайт береться з однієї гілки.
"""

import html as html_lib
import json
import re

from engine.readers import _markup, register
from engine.readers.ghhistory import ghdocs_history

_PAGE = re.compile(r"\.(md|html?|article|slide)$", re.I)
_JSON_HEAD = re.compile(r"\A\s*<!--(\{.*?\})-->", re.S)
_ACTION = re.compile(r"\{\{-?\s*(code|play|raw|image|video)\b(.*?)-?\}\}", re.S)
_ARG = re.compile(r'"((?:[^"\\]|\\.)*)"|`([^`]*)`|(\S+)')
_STYLE = re.compile(r"<(style|script)\b.*?</\1>\s*", re.S | re.I)
_HL = re.compile(r"\s*//\s*HL\w*\s*$")
_BY = re.compile(r"^by:[ \t]*\n((?:[ \t]*-[ \t]+.*\n?)+)", re.M)
_LANG = {".go": "go", ".sh": "sh", ".mod": "", ".txt": "", ".html": "html", ".js": "js", ".c": "c",
         ".s": "asm", ".proto": "protobuf", ".json": "json", ".yaml": "yaml", ".sql": "sql"}
_PRESENT_HEAD = re.compile(r"^(\*{1,3})\s+(.*)$")
_PRESENT_SKIP = re.compile(r"^\.(image|background|iframe|html|caption|figure)\b")
_PRESENT_META = re.compile(r"^(Tags|Summary|OldURL):", re.I)
_PRESENT_LINK = re.compile(r"\[\[([^\]\s]+)\]\[([^\]]+)\]\]")
_PRESENT_BARE = re.compile(r"\[\[([^\]\s]+)\]\]")


def _addr(lines: list[str], spec: str, start: int) -> int:
    """Номер рядка (від 0) за однією адресою present, шукаючи з рядка `start`; -1 — немає."""
    spec = spec.strip()
    if spec == "$":
        return len(lines) - 1
    if spec.isdigit():
        n = int(spec) - 1
        return n if 0 <= n < len(lines) else -1
    if len(spec) >= 2 and spec[0] == "/" and spec[-1] == "/":
        try:
            rx = re.compile(spec[1:-1])
        except re.error:
            return -1
        for i in range(start, len(lines)):
            if rx.search(lines[i]):
                return i
    return -1


def _split_range(spec: str) -> list[str]:
    """`/від/,/до/` → дві адреси; кома всередині виразу між «/» адреси не ділить."""
    parts, cur, inside = [], "", False
    for ch in spec:
        if ch == "/":
            inside = not inside
        if ch == "," and not inside:
            parts.append(cur)
            cur = ""
            continue
        cur += ch
    parts.append(cur)
    return [p for p in parts if p.strip()]


def _select(code: str, addrs: list[str]) -> str:
    lines = code.split("\n")
    if addrs:
        first = _addr(lines, addrs[0], 0)
        last = _addr(lines, addrs[1], max(first, 0)) if len(addrs) > 1 else first
        if first >= 0 and last >= first:
            lines = lines[first:last + 1]
    kept = [_HL.sub("", ln) for ln in lines if not ln.rstrip().endswith("OMIT")]
    return "\n".join(kept).strip("\n")


class _Ctx:
    def __init__(self, ctx, source: dict):
        self._ctx = ctx
        self._content = str(source.get("content") or "_content").strip("/")
        self._literate = str(source.get("literate") or "").strip("/")
        self._titles: dict | None = None

    def _title(self, page_url: str, slug: str) -> str:
        """Назва прикладу Go by Example з файла назв у корені того самого тегу."""
        if self._titles is None:
            self._titles = {}
            root = page_url.split("/examples/", 1)[0]
            url = f"{root}/{self._literate}"
            if self._ctx.allowed(url):
                code, data = self._ctx.fetch(url)
                if code == "200":
                    for line in data.decode("utf-8", errors="replace").splitlines():
                        if line.strip():
                            key = re.sub(r"[^a-z0-9]+", "-", line.strip().lower()).strip("-")
                            self._titles[key] = line.strip()
        return self._titles.get(slug) or slug.replace("-", " ").title()

    def _example(self, text: str, page_url: str) -> str:
        slug = page_url.rsplit("/", 2)[-2]
        out = [f"# Go by Example: {self._title(page_url, slug)}", ""]
        doc: list[str] = []
        code: list[str] = []

        def flush_doc():
            if doc:
                out.extend([" ".join(doc), ""])
                doc.clear()

        def flush_code():
            while code and not code[-1].strip():
                code.pop()
            while code and not code[0].strip():
                code.pop(0)
            if code:
                out.extend(["```go", *code, "```", ""])
            code.clear()

        for line in text.replace("\r\n", "\n").split("\n"):
            s = line.strip()
            if s.startswith("//") and not s.startswith("//go:"):
                flush_code()
                doc.append(s[2:].strip())
            else:
                flush_doc()
                code.append(line)
        flush_doc()
        flush_code()
        shell, _ = self._code(page_url, page_url.rsplit("/", 1)[1][:-3] + ".sh")
        if shell:
            run: list[str] = []
            for line in shell.strip("\n").split("\n"):
                if line.startswith("# "):
                    if run:
                        out.extend(["```sh", *run, "```", ""])
                        run = []
                    doc.append(line[2:].strip())
                else:
                    flush_doc()
                    run.append(line)
            flush_doc()
            if run:
                out.extend(["```sh", *run, "```", ""])
        return "\n".join(out)

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def _code(self, page_url: str, path: str) -> tuple[str, str]:
        """(текст файла, мова) для вставки зі сторінки `page_url`; ("", "") — файла немає."""
        if path.startswith("/"):
            marker = f"/{self._content}/"
            base = page_url.split(marker, 1)[0] + marker if marker in page_url else page_url
            url = base + path.lstrip("/")
        else:
            url = page_url.rsplit("/", 1)[0] + "/" + path
        if not self._ctx.allowed(url):
            return "", ""
        code, data = self._ctx.fetch(url)
        if code != "200":
            return "", ""
        ext = re.search(r"\.[A-Za-z0-9]+$", path)
        return (data.decode("utf-8", errors="replace"),
                _LANG.get(ext.group(0).lower(), "") if ext else "")

    def _block(self, page_url: str, path: str, addrs: list[str], html: bool) -> str:
        code, lang = self._code(page_url, path)
        if not code:
            return f"\n\n(Code: {path})\n\n"
        body = _select(code, addrs)
        if html:
            cls = f' class="language-{lang}"' if lang else ""
            return f"\n<pre{cls}>{html_lib.escape(body)}</pre>\n"
        return f"\n\n```{lang}\n{body}\n```\n\n"

    def _actions(self, text: str, page_url: str, html: bool) -> str:
        def put(m):
            kind = m.group(1)
            args = [a if a is not None else b if b is not None else c
                    for a, b, c in _ARG.findall(m.group(2))]
            if kind == "raw":
                return args[0] if args else ""
            if kind == "image":
                return ""
            if kind == "video":
                return f"\n\nVideo: {args[0]}\n\n" if args else ""
            if not args:
                return m.group(0)
            return self._block(page_url, args[0], args[1:3], html)

        return _ACTION.sub(put, text)

    def _present(self, text: str, page_url: str) -> str:
        lines = text.replace("\r\n", "\n").split("\n")
        # Шапка: назва, підзаголовок, службові рядки — до першого порожнього рядка; далі блок
        # авторів до першого розділу. Автори лишаються одним рядком: «хто це сказав» — частина
        # доповіді.
        i = 0
        head = []
        while i < len(lines) and lines[i].strip():
            if not _PRESENT_META.match(lines[i]) and not lines[i].startswith("//"):
                head.append(lines[i].strip())
            i += 1
        authors = []
        while i < len(lines) and not _PRESENT_HEAD.match(lines[i]) \
                and not lines[i].startswith("## "):
            line = lines[i].strip()
            if line and not re.match(r"^(https?://|@|\S+@\S+$)", line):
                authors.append(line)
            i += 1
        title = head[0].lstrip("# ").strip() if head else ""
        out = [f"# {title}", ""] if title else []
        if len(head) > 1:
            out += [" ".join(head[1:]), ""]
        if authors:
            out += ["By " + ", ".join(authors) + ".", ""]
        code: list[str] = []

        def flush():
            if code:
                while code and not code[-1].strip():
                    code.pop()
                out.extend(["```", *code, "```", ""])
                code.clear()

        for line in lines[i:]:
            if code and (line.startswith(("\t", " ")) or not line.strip()):
                code.append(line[1:] if line.startswith("\t") else line)
                continue
            if line.startswith(("\t", "  ")) and line.strip():
                flush()
                code.append(line[1:] if line.startswith("\t") else line)
                continue
            flush()
            if line.startswith("//"):
                continue
            m = _PRESENT_HEAD.match(line)
            if m:
                out += ["", "#" * (len(m.group(1)) + 1) + " " + m.group(2).strip(), ""]
                continue
            if line.startswith((".code", ".play")):
                tokens = line.split()[1:]
                tokens = [t for t in tokens if not t.startswith("-")]
                if not tokens:
                    continue
                addrs = []
                rest = " ".join(tokens[1:])
                rest = re.sub(r"\s+HL\w*\s*$", "", rest)
                if rest.strip():
                    addrs = _split_range(rest.strip())
                out.append(self._block(page_url, tokens[0], addrs, False))
                continue
            if line.startswith(".link"):
                tokens = line.split(None, 2)
                if len(tokens) >= 2:
                    label = tokens[2] if len(tokens) > 2 else tokens[1]
                    out.append(f"[{label}]({tokens[1]})")
                continue
            if _PRESENT_SKIP.match(line):
                continue
            # Посилання present: `[[адреса][текст]]` і голе `[[адреса]]`.
            line = _PRESENT_LINK.sub(r"[\2](\1)", line)
            out.append(_PRESENT_BARE.sub(r"<\1>", line))
        flush()
        return "\n".join(out)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        if self._literate and "/examples/" in url and url.endswith(".go"):
            return self._example(text, url)
        m = _PAGE.search(url.split("?", 1)[0])
        if not m:
            return text
        ext = m.group(1).lower()
        if ext in ("article", "slide"):
            return self._present(text, url)
        if ext == "md":
            meta, rest = _markup.front_matter(text)
            if meta and meta.get("redirect"):
                return ""
            head = _JSON_HEAD.match(rest)
            if head and '"Redirect"' in head.group(1):
                return ""
            top = ""
            if head and not meta:
                try:
                    info = json.loads(head.group(1))
                except ValueError:
                    info = {}
                rest = rest[head.end():].lstrip("\n")
                title, sub = str(info.get("Title") or ""), str(info.get("Subtitle") or "")
                if title and not rest.startswith("# "):
                    top = f"# {title}\n\n" + (f"{sub}\n\n" if sub else "")
            rest = _STYLE.sub("", self._actions(rest, url, html=False))
            if not meta:
                return top + rest
            close = text.find("\n---", 3)
            lead = []
            if meta.get("date"):
                lead.append(f"Published {str(meta['date'])[:10]}")
            # Автори в шапці блогу — список YAML («by:» і рядки «- Ім'я»), якого спільний розбір
            # шапки не читає: там «by» порожнє.
            by = [str(meta["by"])] if meta.get("by") else re.findall(
                r"^[ \t]*-[ \t]+(.+?)\s*$", _BY.search(text[:close]).group(1), re.M
            ) if _BY.search(text[:close]) else []
            if by:
                lead.append("by " + "; ".join(by))
            line = (" ".join(lead) + ".\n\n") if lead else ""
            return text[:close + 4] + "\n\n" + line + rest.lstrip("\n")
        title, sub = "", ""
        head = _JSON_HEAD.match(text)
        if head:
            try:
                meta = json.loads(head.group(1))
            except ValueError:
                meta = {}
            if meta.get("Redirect"):
                return ""
            title, sub = str(meta.get("Title") or ""), str(meta.get("Subtitle") or "")
            text = text[head.end():]
        body = _markup.html_body(_STYLE.sub("", self._actions(text, url, html=True)))
        top = (f"# {title}\n\n" if title else "") + (f"{sub}\n\n" if sub else "")
        return top + body


@register("ghdocs-history-godev")
def ghdocs_history_godev(source: dict, ctx):
    return ghdocs_history(source, _Ctx(ctx, source))
