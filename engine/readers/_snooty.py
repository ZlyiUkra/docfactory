"""Розмітка Snooty поверх reStructuredText: посібник MongoDB у markdown.

Навіщо. Документацію MongoDB (посібник сервера, mongosh, Database Tools, драйвер Node) пишуть
у rST з власним набором директив Snooty — спільний розбір rst (sitedocs.rst) бачить лише
заголовки, код і виноски, а без решти в корпус лягло б:

- `.. include:: /includes/x.rst` (дев'ять тисяч на посібник) — порожнє місце замість тексту, і
  половина сторінок складалася б із самих заголовків; `.. literalinclude:: /code-examples/…` —
  без прикладу коду, заради якого сторінка й написана;
- `.. tabs-drivers::` з `.. tab::` і `:tabid: nodejs` (у старих версіях — YAML `tabs: - id:`)
  — приклади всіх мов злипалися в один код без підпису, чия це мова;
- `.. procedure::` і `.. step:: Назва` — кроки без нумерації й назв; у версіях до 4.4 кроки
  взагалі лежать не в тексті, а в `includes/steps-*.yaml`, витяги — в `extracts-*.yaml` з
  успадкуванням (`inherit`) і підстановками `{{key}}`: сайт збирав їх у rST під час будування,
  у репозиторії зібраного немає;
- `.. method:: db.collection.find(query)`, `.. option:: --port`, `.. setting:: net.port`,
  `.. serverstatus::`, `.. data::` — сторінка довідника без імені того, що описує;
- константи `{+version+}`, `{+mongosh+}` із `snooty.toml` і підстановки `|ent-build|`,
  `|fcv|` (у старих версіях — `rst_epilog` у `conf.py`) — лишалися б фігурними дужками;
- `.. composable-tutorial::` з `.. selected-content:: :selections: driver, nodejs, atlas` —
  варіанти інструкції без підпису, для якого інтерфейсу й розгортання вони;
- ролі `:binary:`~bin.mongod``, `:method:`~db.collection.find()``, `:ref:`текст <мітка>``,
  `:issue:`SERVER-1`` — кодом із тильдою й міткою замість імені.

Що виходить. Сторінка — один markdown: вставки розгорнуто на місці, вкладки й кроки — підрозділи
з назвами («Node.js», «1. Create the list file»), директиви-об'єкти — підрозділи з ім'ям
об'єкта (`mongod --port <port>`), код — між огорожами з мовою, виноски — підпис і тіло,
таблиці `list-table` — таблицями markdown (складні клітинки — списком). Чого розбір не знає,
лишається текстом, а не зникає.

Модуль не знає ні GitHub, ні версій: він дістає тексти через `ctx` (вставки, буквальні файли,
спільні вставки, константи, підстановки, назви варіантів) — його дає читач `snooty-history`.
"""

import re

from engine.readers.sitedocs import (_RST_ADORN, _RST_DIRECTIVE, _RST_ENUM, _RST_OPTION,
                                     _RST_TABLE, _RST_TARGET, _indent, _rst_block,
                                     _rst_dedent)

_MAX_DEPTH = 14          # вкладені вставки: глибше — цикл, а не документація

# Директиви, що описують об'єкт довідника: аргумент стає назвою підрозділу.
OBJECTS = {"method", "dbcommand", "setting", "option", "parameter", "data", "readconcern",
           "writeconcern", "authrole", "authaction", "binary", "expression", "pipeline",
           "group", "query", "update", "projection", "operator", "limit", "error", "variable",
           "serverstatus", "bsontype", "collflag", "alert", "event", "macro", "envvar",
           "toolcommand", "dbstats", "replstate", "urioption", "readmode", "window",
           "autoencryptkeyword", "rsconf", "describe", "configuration", "httpaction",
           "cmdoption", "program", "class", "function", "attribute", "exception", "member",
           "glossaryterm", "mongodb"}
# Ролі, чий зміст — ім'я в коді.
CODE_ROLES = {"binary", "method", "dbcommand", "pipeline", "expression", "option", "setting",
              "query", "data", "parameter", "authaction", "serverstatus", "group", "update",
              "rsconf", "authrole", "readconcern", "writeconcern", "program", "bsontype",
              "replstate", "urioption", "readmode", "projection", "meth", "window", "variable",
              "file", "limit", "collflag", "error", "envvar", "toolcommand", "macro", "event",
              "alert", "dbstats", "operator", "configuration", "class", "func", "attr", "mod",
              "obj", "exception", "autoencryptkeyword", "samp", "command", "kbd", "regexp",
              "mailheader", "mimetype", "manpage", "httpaction", "cmdoption", "member",
              "issue", "ticket", "node-api", "java-api", "go-api", "ruby-api", "scala-api",
              "phpmethod", "phpclass", "csharp-api", "py-api", "cpp-api", "c-api", "func",
              "expr", "math"}
# Директиви без тексту для корпусу: картинки, зміст, службові поля сторінки, банери.
DROP = {"image", "figure", "contents", "sectnum", "raw", "meta", "facet", "default-domain", "instruqt", "dismissible-skills-card", "cta-banner", "cta", "banner",
        "landing", "openapi", "video", "youtube", "twitter", "class", "cssclass", "highlight",
        "role", "default-role", "index", "todo", "TODO", "atf-image", "tabs-selector",
        "tabs-pillstrip", "pubdate", "ia", "entry", "button", "wayfinding", "chapters",
        "chapter", "guide-index", "release-specification", "atf-figure", "kicker", "unicode",
        "replace", "replacement", "guide", "time", "level", "languages", "product", "author",
        "type", "topic-list", "only-in", "sharedinclude-root", "figma", "include-toc",
        "tabs-top", "tabs-cards", "hidden", "social"}
# Директиви, чиє тіло — звичайний текст, а сама вона нічого не додає.
TRANSPARENT = {"only", "cond", "container", "topic", "sidebar", "introduction", "card-group",
               "hlist", "glossary", "blockquote", "pull-quote", "epigraph", "compound",
               "method-selector", "method-description", "wayfinding-description", "composable-tutorial",
               "procedure", "io-code-block", "tabs-stitch-sdks", "parsed-literal", "line-block",
               "atlas-only", "self-managed-only", "div", "section", "body", "content",
               "mongodb-content", "list", "tab-content"}
ADMONITIONS = {"note": "Note", "warning": "Warning", "important": "Important", "tip": "Tip",
               "caution": "Caution", "attention": "Attention", "danger": "Danger", "hint": "Hint",
               "error": "Error", "seealso": "See also", "see": "See", "example": "Example",
               "admonition": "", "optional": "Optional", "related": "Related",
               "versionadded": "New in version", "versionchanged": "Changed in version",
               "deprecated": "Deprecated since version", "mongodb-version-added": "New in version"}
CODE = {"code-block", "code", "sourcecode", "output-block"}

TAB_NAMES = {
    "shell": "mongosh", "mongosh": "mongosh", "mongo-shell": "mongo shell", "compass": "Compass",
    "python": "Python", "motor": "Motor (Python async)", "pymongo": "PyMongo", "java-sync": "Java (Sync)",
    "java-async": "Java (Async)", "java": "Java", "nodejs": "Node.js", "javascript": "JavaScript",
    "typescript": "TypeScript", "php": "PHP", "perl": "Perl", "ruby": "Ruby", "scala": "Scala",
    "csharp": "C#", "c": "C", "cpp": "C++", "go": "Go", "swift-async": "Swift (Async)",
    "swift-sync": "Swift (Sync)", "swift": "Swift", "kotlin-coroutine": "Kotlin (Coroutine)",
    "kotlin-sync": "Kotlin (Sync)", "kotlin": "Kotlin", "rust": "Rust", "dart": "Dart",
    "windows": "Windows", "macos": "macOS", "linux": "Linux", "debian": "Debian", "ubuntu": "Ubuntu",
    "rhel": "Red Hat / CentOS", "redhat": "Red Hat / CentOS", "amazon": "Amazon Linux",
    "amazon-linux": "Amazon Linux", "suse": "SUSE", "docker": "Docker", "atlas": "Atlas",
    "self-managed": "Self-Managed", "self": "Self-Managed", "cloud": "Cloud", "local": "Local",
    "aws": "AWS", "azure": "Azure", "gcp": "GCP", "kmip": "KMIP", "driver": "Driver",
    "focal": "Ubuntu 20.04 (Focal)", "jammy": "Ubuntu 22.04 (Jammy)", "noble": "Ubuntu 24.04 (Noble)",
    "bionic": "Ubuntu 18.04 (Bionic)", "xenial": "Ubuntu 16.04 (Xenial)", "trusty": "Ubuntu 14.04 (Trusty)",
    "precise": "Ubuntu 12.04 (Precise)", "pkg": "Package manager", "tar": "Tarball", "tgz": "Tarball",
    "msi": "MSI installer", "zip": "ZIP archive", "systemd": "systemd", "sysv": "SysV init",
    "standalone": "Standalone", "replica-set": "Replica set", "sharded": "Sharded cluster",
    "sharded-cluster": "Sharded cluster", "enterprise": "Enterprise", "community": "Community",
    "cli": "CLI", "ui": "UI", "api": "API",
}

_CONST = re.compile(r"\{\+([a-zA-Z0-9_.-]+)\+\}")
_SUBST = re.compile(r"\|([a-zA-Z0-9][a-zA-Z0-9_.+-]*)\|")
_SUBST_DEF = re.compile(r"^\s*\.\.\s+\|([^|]+)\|\s+(replace|unicode)::\s*(.*)$")
_PLACEHOLDER = re.compile(r"\{\{\s*([a-zA-Z0-9_-]+)\s*\}\}")
_SIMPLE_TABLE = re.compile(r"^\s*=+(?:\s+=+)+\s*$")
_FOOTNOTE_DEF = re.compile(r"^\s*\.\.\s+\[(#?[\w.-]+|\*)\]\s*(.*)$")
_FOOTNOTE_REF = re.compile(r"\s?\[(#?[\w.-]+|\*)\]_")
_FIELD = re.compile(r"^\s*:([\w-]+):(?:\s+[^`]*)?$")
_NAMED_FIELDS = {"returns": "Returns", "return": "Returns", "rtype": "Return type",
                 "raises": "Raises", "param": "Parameter", "parameter": "Parameter",
                 "type": "Type", "throws": "Throws", "example": "Example"}
_LIST_ROW = re.compile(r"^(\s*)\*\s+(?:-\s+(.*)|$)")
_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)]|#\.|\(\d+\)|[a-zA-Z][.)])\s+")
_LIST_CELL = re.compile(r"^(\s*)-\s+(.*)$")
_CODE_SPAN = re.compile(r"``(.+?)``")
_ROLE = re.compile(r":([a-zA-Z0-9_.+-]+(?::[a-zA-Z0-9_.+-]+)?):`([^`]*)`")
_WRAPPED_CODE = re.compile(r"(?<![`\w])``([^`\n]{1,80})\n[ \t]*([^`\n]{1,80})``(?![`\w])")
_WRAPPED_ROLE = re.compile(r":[a-zA-Z0-9_.+-]+(?::[a-zA-Z0-9_.+-]+)?:`[^`\n]*\n[^`]*?`")
_LINK = re.compile(r"`([^`<]*?)\s*<([^<>`]+)>`__?")
_WRAPPED_LINK = re.compile(r"(?<!`)`(?!`)[^`]*?\n[^`]*?<[^<>`\s]+>`__?")
_REF = re.compile(r"`([^`<]+)`__?(?!\w)")
_BARE_URL = re.compile(r"<(https?://[^<>\s`]+)>")
_STRONG = re.compile(r"(?<!\*)\*\*([^*]+)\*\*(?!\*)")
_EMPH = re.compile(r"(?<![*\w])\*([^*\s][^*]*?)\*(?![*\w])")
_HTML_TAG = re.compile(r"<(/?[a-zA-Z][\w-]*)(\s[^<>]*)?>")
_TITLE_UNDER = re.compile(r"^([=\-~^\"'`#*+_.:<>])\1{2,}\s*$")
_LANG_BY_EXT = {"js": "javascript", "mjs": "javascript", "cjs": "javascript", "ts": "typescript",
                "py": "python", "java": "java", "cs": "csharp", "go": "go", "php": "php", "rb": "ruby",
                "c": "c", "h": "c", "kt": "kotlin", "scala": "scala", "cpp": "cpp", "cc": "cpp",
                "rs": "rust", "sh": "sh", "bash": "bash", "json": "json", "yaml": "yaml",
                "yml": "yaml", "swift": "swift", "pl": "perl", "sql": "sql", "toml": "toml",
                "xml": "xml", "html": "html", "cfg": "ini", "conf": "ini", "ini": "ini",
                "ps1": "powershell", "bat": "bat", "txt": "", "csv": "", "log": "", "rst": ""}


class Ctx:
    """Що читач дає розбору. Усі методи повертають текст або None (файла немає)."""

    constants: dict = {}
    composables: dict = {}

    def include(self, target: str, page_dir: str) -> str | None:   # pragma: no cover
        return None

    def literal(self, target: str, page_dir: str) -> str | None:   # pragma: no cover
        return None

    def shared(self, target: str) -> str | None:                   # pragma: no cover
        return None

    def label_title(self, label: str) -> str:
        return ""

    def doc_title(self, path: str) -> str:
        return ""

    def substitutions(self) -> dict:
        return {}


class _State:
    def __init__(self, ctx: Ctx, page_dir: str):
        self.ctx = ctx
        self.styles: list = []        # порядок стилів підкреслення → рівень заголовка
        self.level = 1                # рівень останнього заголовка
        self.base = 0                 # зсув рівнів усередині підписаного блоку (вкладка, крок)
        self.targets: dict = {}       # `.. _назва: url`
        self.subs: list = [dict(ctx.substitutions())]   # шари підстановок, останній — верхній
        self.program = ""             # `.. program:: mongod` — префікс назв опцій
        self.depth = 0                # глибина вкладених вставок
        self.page_dir = page_dir
        self.step = [0]               # лічильники кроків procedure (стек)
        self.misses: list = []        # вставки, яких не знайдено

    def sub(self, name: str) -> str | None:
        for layer in reversed(self.subs):
            if name in layer:
                return layer[name]
        return None


# ── підготовка тексту ────────────────────────────────────────────────────────


def _constants(text: str, consts: dict) -> str:
    """`{+name+}` → значення; значення самі можуть містити константи — кілька проходів.
    `{{version}}` і `{{release}}` у YAML-записах без власного replacement збирання giza брало з
    конфігурації гілки — тут так само з констант."""
    if consts and "{{" in text:
        text = re.sub(r"\{\{\s*(version|release|branch)\s*\}\}",
                      lambda m: consts.get(m.group(1), m.group(0)), text)
    if not consts or "{+" not in text:
        return text
    for _ in range(4):
        new = _CONST.sub(lambda m: consts.get(m.group(1), m.group(0)), text)
        if new == text:
            break
        text = new
    return text


def _collect_subs(lines: list[str], st: _State) -> None:
    """`.. |x| replace:: y` і `.. |x| unicode:: U+000A9` — визначення підстановок тексту."""
    for ln in lines:
        m = _SUBST_DEF.match(ln)
        if not m:
            continue
        name, kind, value = m.group(1).strip(), m.group(2), m.group(3).strip()
        if kind == "unicode":
            value = " ".join(chr(int(p[2:], 16)) if p.upper().startswith("U+") else p
                             for p in value.split())
        st.subs[0][name] = value


def _substitute(text: str, st: _State) -> str:
    if "|" not in text:
        return text

    def one(m):
        if m.group(0).startswith("|") and m.start() > 0 and text[m.start() - 1] == "|":
            return m.group(0)
        val = st.sub(m.group(1))
        return m.group(0) if val is None else val
    # Значення підстановки саме буває з підстановок (`|downgradepath|` → «…|newversion|…»),
    # тому кілька проходів, поки текст міняється.
    for _ in range(4):
        out = []
        for ln in text.split("\n"):
            if _SUBST_DEF.match(ln):
                out.append(ln)      # визначення — не чіпаємо
            else:
                out.append(_SUBST.sub(one, ln))
        new = "\n".join(out)
        if new == text or "|" not in new:
            return new
        text = new
    return text


def _prepare(text: str, st: _State) -> list[str]:
    text = text.replace("\r\n", "\n").expandtabs(3)
    text = _constants(text, st.ctx.constants)
    text = _WRAPPED_LINK.sub(lambda m: m.group(0) if "\n\n" in m.group(0)
                             else re.sub(r"\s*\n\s*", " ", m.group(0)), text)
    text = _WRAPPED_ROLE.sub(lambda m: m.group(0) if "\n\n" in m.group(0)
                             else re.sub(r"\s*\n\s*", " ", m.group(0)), text)
    text = _WRAPPED_CODE.sub(lambda m: f"``{m.group(1).rstrip()} {m.group(2)}``", text)
    lines = text.split("\n")
    _collect_subs(lines, st)
    for ln in lines:
        t = _RST_TARGET.match(ln)
        if t and t.group(2):
            st.targets[t.group(1).strip("`").strip().lower()] = t.group(2)
    return _substitute("\n".join(lines), st).split("\n")


# ── вбудована розмітка ───────────────────────────────────────────────────────


def _humanize(label: str) -> str:
    label = label.strip().strip("/").rsplit("/", 1)[-1]
    return label.replace("-", " ").replace("_", " ").strip()


def _role(m, st: _State) -> str:
    role, body = m.group(1).lower(), m.group(2).strip()
    role = role.split(":")[-1]
    # Екрановані `\<` `\>` — частина тексту, не ціль: ховаються на час розбору.
    body = body.replace("\\<", "\x01").replace("\\>", "\x02")
    text, target = body, ""
    # Ціль — лише `<…>` наприкінці; `sh.status.<db>.chunks` посередині — частина тексту.
    t = re.match(r"^(.*?)\s*<(.+)>$", body)
    if t:
        text, target = t.group(1).strip(), t.group(2).strip()
    text, target, body = (x.replace("\x01", "<").replace("\x02", ">") for x in (text, target, body))
    if role == "ref":
        if text and target:
            return text
        label = (target or body).strip()
        title = _substitute(st.ctx.label_title(label.lower()), st) if label else ""
        if title:
            return _CODE_SPAN.sub(lambda c: f"`{c.group(1)}`", title)
        return _humanize(label)
    if role == "doc":
        return text if text and target else _humanize(body)
    if role == "guilabel":
        return f"**{text}**"
    if role in ("term", "abbr", "sub", "sup", "red", "gold", "blue", "green", "black",
                "strong", "emphasis", "title", "t", "dochub", "website", "manual", "atlas",
                "compass", "driver", "rfc", "wikipedia", "spec", "opsmgr", "cloudmgr", "mms-docs",
                "mms-home", "products", "wtdocs", "charts", "bic", "kafka", "datalake",
                "mongosh-docs", "ecosystem", "api", "gettingstarted", "hardlink", "pdf",
                "landing", "v2.2", "v2.4", "v2.6", "v3.0", "v3.2", "v3.4", "v3.6", "v4.0", "v4.2",
                "v4.4", "v5.0", "v6.0", "v7.0", "v8.0", "ref", "doc", "pep", "cve", "dbtools",
                "mongodb-shell", "realm", "stitch", "cloud", "sql", "cli", "atlascli",
                "mongocli", "k8s", "chart", "guides", "university", "support", "jira",
                "search", "vector", "wsc", "faq", "tutorial"):
        return text if text and target else (target or text)
    if role in CODE_ROLES:
        if text and target:
            name = text
        else:
            name = body
        if name.startswith("~"):
            # `~bin.mongod` → `mongod`: тильда ховає шлях, лишаючи останню ланку
            name = name[1:].rsplit(".", 1)[-1] if "(" not in name else _tail(name[1:])
        return f"`{name}`"
    return text if text and target else (f"`{body}`" if body else "")


def _tail(name: str) -> str:
    """`db.collection.find()` без тильди лишається цілим; `~db.collection.find()` → `find()`."""
    head, _, rest = name.partition("(")
    return head.rsplit(".", 1)[-1] + ("(" + rest if rest or name.endswith("(") else "")


def inline(line: str, st: _State) -> str:
    """Вбудована розмітка rst → markdown. Код не чіпається."""
    def text(part: str) -> str:
        # Результат ролі (часто код із `<db>` усередині) ховається за заповнювачем, щоб решта
        # замін — теги, посилання — його не чіпала.
        saved: list[str] = []

        def keep(m) -> str:
            saved.append(_role(m, st))
            return f"\x00{len(saved) - 1}\x00"
        part = _ROLE.sub(keep, part)
        part = _LINK.sub(lambda m: (f"[{m.group(1)}]({m.group(2)})" if m.group(1)
                                    and not m.group(2).startswith("#")
                                    else m.group(1) or m.group(2)), part)
        part = _BARE_URL.sub(r"\1", part)

        def ref(m):
            url = st.targets.get(m.group(1).strip().lower())
            return f"[{m.group(1)}]({url})" if url else m.group(1)
        part = _REF.sub(ref, part)
        part = _HTML_TAG.sub(lambda m: f"`<{m.group(1)}{m.group(2) or ''}>`", part)
        part = _FOOTNOTE_REF.sub("", part)
        return re.sub(r"\x00(\d+)\x00", lambda m: saved[int(m.group(1))], part)

    parts, pos = [], 0
    for m in _CODE_SPAN.finditer(line):
        parts.append(text(line[pos:m.start()]))
        code = m.group(1)
        parts.append(f"`` {code} ``" if "`" in code else f"`{code}`")
        pos = m.end()
    parts.append(text(line[pos:]))
    return "".join(parts)


# ── розбір блоків ────────────────────────────────────────────────────────────


def _options(block: list[str]) -> tuple[dict, list[str]]:
    """Параметри директиви (`:language: js`) на початку тіла → словник і решта тіла."""
    opts: dict = {}
    i = 0
    while i < len(block):
        ln = block[i]
        if not ln.strip():
            if opts:
                i += 1
                break
            i += 1
            continue
        m = re.match(r"^\s*:([\w-]+):\s*(.*)$", ln)
        if not m or "`" in ln:
            break
        opts[m.group(1).lower()] = m.group(2).strip()
        i += 1
    rest = block[i:]
    while rest and not rest[0].strip():
        rest.pop(0)
    return opts, rest


def _fence(code: list[str], lang: str, pad: str = "") -> list[str]:
    code = _trim_blank(code)
    width = min((_indent(ln) for ln in code if ln.strip()), default=0)
    code = [ln[width:] for ln in code]
    return [f"{pad}```{lang}", *[pad + ln if ln else ln for ln in code], f"{pad}```", ""]


def _trim_blank(lines: list[str]) -> list[str]:
    lines = list(lines)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def _cut(lines: list[str], opts: dict) -> list[str]:
    """`:start-after:` / `:end-before:` / `:lines:` — вирізка з файла, як у Sphinx."""
    start, end = opts.get("start-after"), opts.get("end-before")
    if start:
        for i, ln in enumerate(lines):
            if start in ln:
                lines = lines[i + 1:]
                break
        else:
            lines = []
    if end:
        for i, ln in enumerate(lines):
            if end in ln:
                lines = lines[:i]
                break
    if opts.get("lines"):
        picked = []
        for part in opts["lines"].split(","):
            part = part.strip()
            if "-" in part:
                a, _, b = part.partition("-")
                a = int(a) if a.strip() else 1
                b = int(b) if b.strip() else len(lines)
                picked.extend(lines[a - 1:b])
            elif part.isdigit():
                idx = int(part) - 1
                if 0 <= idx < len(lines):
                    picked.append(lines[idx])
        lines = picked
    return lines


def _lang(opts: dict, path: str = "") -> str:
    lang = opts.get("language", "").strip().lower()
    if lang in ("none", "text", "plain", "plaintext"):
        return ""
    if lang:
        return {"js": "javascript", "py": "python", "shell": "sh", "console": "sh",
                "cs": "csharp", "c#": "csharp", "c++": "cpp", "yml": "yaml", "rb": "ruby",
                "kt": "kotlin", "rs": "rust", "ts": "typescript", "jsx": "javascript",
                "golang": "go"}.get(lang, lang)
    ext = path.rsplit(".", 1)[-1].lower() if "." in path.rsplit("/", 1)[-1] else ""
    return _LANG_BY_EXT.get(ext, "")


def _name_of(tab_id: str, st: _State) -> str:
    tab_id = tab_id.strip()
    if tab_id in st.ctx.composables:
        return st.ctx.composables[tab_id]
    if tab_id in TAB_NAMES:
        return TAB_NAMES[tab_id]
    return _humanize(tab_id).capitalize() if tab_id else ""


class _Out:
    def __init__(self):
        self.lines: list[str] = []

    def blank(self) -> None:
        if self.lines and self.lines[-1].strip():
            self.lines.append("")

    def add(self, *lines: str) -> None:
        self.lines.extend(lines)


def _heading(out: _Out, st: _State, title: str, level: int) -> None:
    level = max(1, min(level, 6))
    out.blank()
    out.add("#" * level + " " + " ".join(inline(title, st).split()), "")
    st.level = level


_INCLUDE_LINE = re.compile(r"^\s*\.\.\s+(include|sharedinclude)::\s*(\S+)", re.M)


def _collect_defs(text: str, st: _State, page_dir: str, seen: set) -> None:
    """Підстановки, визначені у вставках сторінки (`includes/links-urls/*.rst`), діють на всю
    сторінку, хоч би де стояла вставка, — тому визначення збираються наперед."""
    _collect_subs(_constants(text, st.ctx.constants).split("\n"), st)
    if len(seen) > 400:
        return
    for m in _INCLUDE_LINE.finditer(text):
        kind, target = m.group(1), m.group(2)
        key = f"{kind}:{page_dir}:{target}"
        if key in seen:
            continue
        seen.add(key)
        inner = st.ctx.shared(target) if kind == "sharedinclude" else st.ctx.include(target, page_dir)
        if inner:
            _collect_defs(inner, st, _dir_of(target, page_dir), seen)


def render(text: str, ctx: Ctx, page_dir: str = "") -> tuple[str, list[str]]:
    """Сторінка rST Snooty → markdown. Повертає текст і перелік вставок, яких не знайшлося."""
    st = _State(ctx, page_dir)
    out = _Out()
    _collect_defs(text, st, page_dir, set())
    _render(_prepare(text, st), st, out)
    body = "\n".join(out.lines)
    body = re.sub(r"\n{3,}", "\n\n", body).strip("\n") + "\n"
    return body, st.misses


def _render(lines: list[str], st: _State, out: _Out) -> None:
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        nxt = lines[i + 1] if i + 1 < n else ""
        after = lines[i + 2] if i + 2 < n else ""
        if not ln.strip():
            out.blank()
            i += 1
            continue
        a = _RST_ADORN.match(ln)
        blank_before = not out.lines or not out.lines[-1].strip()
        if a and blank_before:
            if nxt.strip() and _RST_ADORN.match(after) and after.strip()[0] == a.group(1):
                _adorned(out, st, nxt, (a.group(1), True))
                i += 3
                continue
            if not nxt.strip():
                i += 1
                continue
        if (_RST_TABLE.match(ln) or _SIMPLE_TABLE.match(ln)) and blank_before:
            j = i
            while j < n and lines[j].strip():
                j += 1
            out.blank()
            out.add("```", *_rst_dedent(lines[i:j]), "```", "")
            i = j
            continue
        u = _RST_ADORN.match(nxt)
        if (u and not a and blank_before and ln.strip() and not ln.startswith(" ")
                and len(nxt.strip()) >= min(len(ln.strip()), 3)
                and not _RST_DIRECTIVE.match(ln) and not ln.lstrip().startswith("..")):
            _adorned(out, st, ln, (u.group(1), False))
            i += 2
            continue
        d = _RST_DIRECTIVE.match(ln)
        if d and not ln.lstrip().startswith(".. |"):
            indent, name, arg = len(d.group(1)), d.group(2), (d.group(3) or "").strip()
            block, j = _rst_block(lines, i + 1, indent)
            _directive(name, arg, block, st, out)
            i = j
            continue
        fn = _FOOTNOTE_DEF.match(ln)
        if fn:
            block, j = _rst_block(lines, i + 1, _indent(ln))
            out.blank()
            out.add(f"Note: {inline(fn.group(2), st)}".rstrip())
            _sub_render(_rst_dedent(block), st, out)
            out.blank()
            i = j
            continue
        if _RST_TARGET.match(ln) or ln.lstrip().startswith(".."):
            # Ціль посилання вже зібрано; решта «..» — коментар із тілом під відступом.
            _, i = _rst_block(lines, i + 1, _indent(ln))
            continue
        if ln.rstrip().endswith("::"):
            line = ln.rstrip()[:-2]
            line = line.rstrip() if not line.strip() or line.endswith(" ") else line + ":"
            if line.strip():
                out.add(inline(line, st))
            k = i + 1
            while k < n and not lines[k].strip():
                k += 1
            if k < n and _indent(lines[k]) > _indent(ln):
                block, j = _rst_block(lines, k, _indent(ln))
                out.blank()
                out.add(*_fence(block, ""))
                i = j
            else:
                i += 1
            continue
        f = _FIELD.match(ln)
        if f and blank_before:
            # Поле сторінки (`:orphan:`, `:copyable:` поза директивою) — не текст; поле опису
            # (`:returns:`) — підпис перед своїм тілом.
            name = f.group(1).lower()
            if name in _NAMED_FIELDS:
                out.add(f"**{_NAMED_FIELDS[name]}:** {inline(ln.split(':', 2)[2].strip(), st)}"
                        .rstrip(), "")
            i += 1
            continue
        e = _RST_ENUM.match(ln)
        if e:
            ln = f"{e.group(1)}1.{e.group(2)}{ln[e.end():]}"
        if (blank_before and nxt.strip() and _indent(nxt) > _indent(ln) and not e
                and not _LIST_ITEM.match(ln) and not ln.rstrip().endswith("::")
                and not ln.lstrip().startswith(("|", ".."))):
            # Список визначень: термін і тіло під відступом — термін жирним, тіло абзацом,
            # інакше markdown зліпив би їх в одне речення («$cmd A virtual collection…»).
            block, j = _rst_block(lines, i + 1, _indent(ln))
            out.add(f"**{inline(ln.strip(), st)}**", "")
            _sub_render(_rst_dedent(block), st, out)
            out.blank()
            i = j
            continue
        out.add(inline(ln, st))
        i += 1


def _adorned(out: _Out, st: _State, title: str, style: tuple) -> None:
    if style not in st.styles:
        st.styles.append(style)
    _heading(out, st, title.strip(), st.styles.index(style) + 1 + st.base)


def _sub_render(text_lines: list[str], st: _State, out: _Out, level: int | None = None) -> None:
    """Тіло директиви під власним рівнем заголовків; після нього рівень повертається."""
    saved = st.level
    if level is not None:
        st.level = level
    _render(text_lines, st, out)
    st.level = saved


def _directive(name: str, arg: str, block: list[str], st: _State, out: _Out) -> None:
    lname = name.lower()
    opts, body = _options(block)
    body = _rst_dedent(body)

    if lname in CODE or lname == "input" or lname == "output":
        out.blank()
        if lname in ("input", "output"):
            out.add(f"{lname.capitalize()}:")
            if arg:
                text = st.ctx.literal(arg, st.page_dir)
                if text is None:
                    st.misses.append(arg)
                    body = []
                else:
                    body = _cut(text.split("\n"), opts)
        lang = _lang(opts, arg if lname in ("input", "output") else "")
        if lname in CODE and arg and not opts.get("language"):
            lang = _lang({"language": arg.split()[0]})
        if opts.get("caption"):
            out.add(inline(opts["caption"], st), "")
        out.add(*_fence(body, lang))
        return
    if lname == "literalinclude":
        text = st.ctx.literal(arg, st.page_dir)
        out.blank()
        if opts.get("caption"):
            out.add(inline(opts["caption"], st), "")
        if text is None:
            st.misses.append(arg)
            out.add(f"(code example `{arg.rsplit('/', 1)[-1]}` — kept outside the "
                    f"documentation repository)", "")
            return
        out.add(*_fence(_cut(text.split("\n"), opts), _lang(opts, arg)))
        return
    if lname == "include":
        _include(arg, block, opts, st, out)
        return
    if lname == "sharedinclude":
        _include(arg, block, _options(block)[0], st, out, shared=True)
        return
    if lname.startswith("tabs") or lname == "tab-set" or lname == "tabset":
        _tabs(lname, body, st, out)
        return
    if lname in ("tab", "tab-item"):
        _tab(arg, opts, body, st, out)
        return
    if lname == "step":
        st.step[-1] += 1
        _labelled(f"{st.step[-1]}. {arg}" if arg else f"Step {st.step[-1]}", body, st, out)
        return
    if lname == "procedure":
        st.step.append(0)
        _sub_render(body, st, out)
        st.step.pop()
        return
    if lname == "selected-content":
        sel = [s.strip() for s in opts.get("selections", "").split(",")
               if s.strip() and s.strip().lower() != "none"]
        label = " · ".join(_name_of(s, st) for s in sel) or "Variant"
        _labelled(label, body, st, out)
        return
    if lname in ("method-option", "wayfinding-option"):
        if lname == "wayfinding-option":
            return
        _labelled(_name_of(opts.get("id", arg), st) or "Option", body, st, out)
        return
    if lname == "collapsible":
        title = opts.get("heading") or arg or "Details"
        sub = opts.get("sub_heading", "")
        _labelled(title, ([f"*{sub}*", ""] if sub else []) + body, st, out)
        return
    if lname == "card":
        title = opts.get("headline") or arg
        out.blank()
        if title:
            out.add(f"**{inline(title, st)}**", "")
        _sub_render(body, st, out)
        return
    if lname == "rubric":
        out.blank()
        out.add(f"**{inline(arg, st)}**", "")
        return
    if lname == "toctree":
        # Зміст розділу: сторінка-перелік без нього лишалася б порожньою. Запис — `Назва </шлях>`
        # або сам `/шлях`; назва без запису — зі шляху.
        entries = []
        for ln in body:
            t = ln.strip()
            if not t or t.startswith(":"):
                continue
            m = re.match(r"^(.*?)\s*<([^<>]+)>$", t)
            name = (m.group(1).strip() if m and m.group(1).strip() else "")
            path = m.group(2).strip() if m else t
            if not name:
                # Назва чужої сторінки буває з `|newversion|`: підстановки — цієї сторінки,
                # бо сторінки-переліки випусків вставляють той самий файл визначень.
                name = _substitute(st.ctx.doc_title(path), st) or _humanize(path).capitalize()
            entries.append(f"- {inline(name, st)}")
        if entries:
            out.blank()
            out.add(*entries, "")
        return
    if lname == "program":
        st.program = arg.strip()
        _sub_render(body, st, out)
        return
    if lname in ADMONITIONS:
        _admonition(lname, arg, body, st, out)
        return
    if lname in OBJECTS or lname.startswith("mongodb:"):
        title = arg
        if lname in ("option", "cmdoption") and st.program and not title.startswith(st.program):
            title = f"{st.program} {title}"
        _labelled(title or lname, body, st, out)
        return
    if lname == "list-table":
        _list_table(opts, body, st, out)
        return
    if lname == "csv-table":
        out.blank()
        out.add(*_fence(body, ""))
        return
    if lname in ("math", "parsed-literal"):
        out.blank()
        out.add(*_fence(body, ""))
        return
    if lname in DROP:
        return
    if lname in TRANSPARENT or lname == "composable-tutorial":
        _sub_render(body, st, out)
        return
    # Незнайома директива: назва з аргументом рядком, тіло — текстом, щоб нічого не зникло.
    out.blank()
    if arg:
        out.add(inline(arg, st), "")
    _sub_render(body, st, out)


def _labelled(label: str, body: list[str], st: _State, out: _Out) -> None:
    """Підрозділ з назвою (вкладка, варіант, крок, об'єкт довідника): заголовки його тіла —
    під ним, а після нього рівень повертається до рівня перед блоком."""
    level, base = st.level, st.base
    _heading(out, st, label, level + 1)
    st.base = level + 1
    _sub_render(body, st, out, level + 1)
    st.level, st.base = level, base


def _admonition(lname: str, arg: str, body: list[str], st: _State, out: _Out) -> None:
    label = ADMONITIONS[lname]
    out.blank()
    if lname in ("versionadded", "versionchanged", "deprecated", "mongodb-version-added"):
        ver, _, rest = arg.partition(" ")
        head = f"*{label} {ver}.*"
        if rest.strip():
            out.add(f"{head} {inline(rest.strip(), st)}")
        else:
            out.add(head)
        out.add("")
        _sub_render(body, st, out)
        return
    if lname == "admonition":
        label = inline(arg, st)
        arg = ""
    if arg:
        body = [arg, ""] + body
    out.add(f"**{label}:**" if label else "", "")
    _sub_render(body, st, out)
    out.blank()


def _include(arg: str, block: list[str], opts: dict, st: _State, out: _Out,
             shared: bool = False) -> None:
    # Дочірні `.. replacement:: name` дають значення `|name|` всередині вставки — і в
    # `include`, і в `sharedinclude` (шаблони драйверів у docs-shared живуть саме так).
    layer: dict = {}
    lines = _rst_dedent(block)
    k = 0
    while k < len(lines):
        m = _RST_DIRECTIVE.match(lines[k])
        if m and m.group(2) == "replacement":
            body, k = _rst_block(lines, k + 1, len(m.group(1)))
            layer[(m.group(3) or "").strip()] = " ".join(
                inline(x.strip(), st) for x in _rst_dedent(body) if x.strip())
        else:
            k += 1
    text = st.ctx.shared(arg) if shared else st.ctx.include(arg, st.page_dir)
    if text is None:
        st.misses.append(("shared:" if shared else "") + arg)
        return
    _nested(text, st, out, st.page_dir if shared else _dir_of(arg, st.page_dir), opts, layer)


def _dir_of(target: str, page_dir: str) -> str:
    target = target.strip()
    if target.startswith("/"):
        return target.rsplit("/", 1)[0].lstrip("/")
    joined = f"{page_dir}/{target}" if page_dir else target
    return joined.rsplit("/", 1)[0] if "/" in joined else ""


def _nested(text: str, st: _State, out: _Out, page_dir: str, opts: dict,
            layer: dict | None = None) -> None:
    if st.depth >= _MAX_DEPTH:
        st.misses.append("depth")
        return
    st.depth += 1
    st.subs.append(layer or {})
    saved_dir, st.page_dir = st.page_dir, page_dir
    try:
        lines = _prepare(text, st)
        if opts.get("start-after") or opts.get("end-before"):
            lines = _cut(lines, {k: v for k, v in opts.items() if k in ("start-after", "end-before")})
        _render(lines, st, out)
    finally:
        st.page_dir = saved_dir
        st.subs.pop()
        st.depth -= 1


# ── вкладки ──────────────────────────────────────────────────────────────────


def _tabs(lname: str, body: list[str], st: _State, out: _Out) -> None:
    if any(_RST_DIRECTIVE.match(x) and _RST_DIRECTIVE.match(x).group(2) in ("tab", "tab-item")
           for x in body):
        _sub_render(body, st, out)
        return
    # Старий запис: YAML `tabs: - id: … name: … content: |`.
    tabs = _yaml_tabs(body)
    if tabs is None:
        _sub_render(body, st, out)
        return
    for tab in tabs:
        tab_id = str(tab.get("id", "")).strip()
        name = str(tab.get("name") or "").strip() or _name_of(tab_id, st)
        content = tab.get("content") or ""
        _labelled(name or "Tab", str(content).split("\n"), st, out)


def _yaml_tabs(body: list[str]):
    try:
        import yaml
        data = yaml.safe_load("\n".join(body))
    except Exception:
        return None
    if isinstance(data, dict) and isinstance(data.get("tabs"), list):
        return [t for t in data["tabs"] if isinstance(t, dict)]
    return None


def _tab(arg: str, opts: dict, body: list[str], st: _State, out: _Out) -> None:
    name = arg.strip() or _name_of(opts.get("tabid", ""), st) or "Tab"
    _labelled(name, body, st, out)


# ── таблиці ──────────────────────────────────────────────────────────────────


def _list_table(opts: dict, body: list[str], st: _State, out: _Out) -> None:
    rows: list[list[list[str]]] = []
    i = 0
    while i < len(body):
        m = _LIST_ROW.match(body[i])
        if not m:
            i += 1
            continue
        row_indent = len(m.group(1))
        row_lines, j = _rst_block(body, i + 1, row_indent)
        first = body[i][m.end(1) + 1:].lstrip()   # після «* »
        cells: list[list[str]] = []
        all_lines = ([first] if first.strip() else []) + _rst_dedent(row_lines)
        k = 0
        while k < len(all_lines):
            c = _LIST_CELL.match(all_lines[k])
            if c and _indent(all_lines[k]) == (0 if k else 0):
                cell_lines, k2 = _rst_block(all_lines, k + 1, len(c.group(1)))
                cells.append([c.group(2)] + _rst_dedent(cell_lines))
                k = k2
            else:
                if cells:
                    cells[-1].append(all_lines[k])
                k += 1
        rows.append(cells)
        i = j
    if not rows:
        _sub_render(body, st, out)
        return
    header = int(opts.get("header-rows", "0") or 0)
    simple = all(not _RST_DIRECTIVE.match(x) and not x.rstrip().endswith("::")
                 for row in rows for cell in row for x in cell)
    out.blank()
    if simple:
        width = max(len(r) for r in rows)
        def flat(cell: list[str]) -> str:
            text = " ".join(x.strip() for x in cell
                            if x.strip() and not x.lstrip().startswith(".."))
            return inline(text, st).replace("|", "\\|")
        table = [[flat(c) for c in r] + [""] * (width - len(r)) for r in rows]
        if header >= 1:
            head, data = table[0], table[1:]
        else:
            head, data = [""] * width, table
        out.add("| " + " | ".join(head) + " |", "|" + "---|" * width)
        for r in data:
            out.add("| " + " | ".join(r) + " |")
        out.add("")
        return
    head = rows[0] if header >= 1 else None
    data = rows[1:] if header >= 1 else rows
    for r in data:
        first = " ".join(x.strip() for x in r[0] if x.strip()) if r else ""
        out.add(f"- **{inline(first, st)}**")
        for idx, cell in enumerate(r[1:], 1):
            label = ""
            if head and idx < len(head):
                label = " ".join(x.strip() for x in head[idx] if x.strip())
            sub = _Out()
            _sub_render(cell, st, sub, st.level)
            text = "\n".join(sub.lines).strip("\n")
            if label:
                out.add(f"  {inline(label, st)}:")
            out.add(*["  " + x if x else "" for x in text.split("\n")])
        out.add("")


# ── YAML-кроки, витяги, релізи (giza) ────────────────────────────────────────


def _text_of(value) -> str:
    if isinstance(value, dict):
        return str(value.get("text") or value.get("content") or "")
    return "" if value is None else str(value)


def _inherit(entry: dict, loader) -> dict:
    """`inherit`/`source`: {file, ref} — батьківський запис з іншого файла; поля дитини
    зверху, `replacement` обох шарів — підстановки `{{key}}`."""
    seen = 0
    merged = dict(entry)
    while seen < 8 and (merged.get("inherit") or merged.get("source")):
        link = merged.pop("inherit", None) or merged.pop("source", None)
        if not isinstance(link, dict):
            break
        parent = loader(str(link.get("file", "")), str(link.get("ref", "")))
        if not parent:
            break
        rep = dict(parent.get("replacement") or {})
        rep.update(merged.get("replacement") or {})
        merged = {**parent, **{k: v for k, v in merged.items() if k != "replacement"}}
        merged["replacement"] = rep
        seen += 1
    return merged


def _fill(text: str, rep: dict) -> str:
    if not rep or "{{" not in text:
        return text
    return _PLACEHOLDER.sub(lambda m: str(rep.get(m.group(1), m.group(0))), text)


def steps_rst(docs: list, loader) -> str:
    """Кроки з `steps-*.yaml` → rST: кожен крок — `.. step:: Назва` з тілом."""
    out: list[str] = []
    for idx, raw in enumerate(d for d in docs if isinstance(d, dict)):
        d = _inherit(raw, loader)
        rep = d.get("replacement") or {}
        title = _fill(_text_of(d.get("title")), rep).strip() or f"Step {idx + 1}"
        out.append(f".. step:: {title}")
        out.append("")
        parts: list[str] = []
        if d.get("pre"):
            parts.append(_fill(_text_of(d["pre"]), rep))
        actions = d.get("action")
        for act in (actions if isinstance(actions, list) else [actions] if actions else []):
            if not isinstance(act, dict):
                continue
            if act.get("heading"):
                parts.append(f"**{_fill(_text_of(act['heading']), rep).strip()}**")
            if act.get("pre"):
                parts.append(_fill(_text_of(act["pre"]), rep))
            if act.get("code") is not None:
                lang = str(act.get("language") or "")
                code = _fill(str(act["code"]), rep).rstrip("\n")
                parts.append(f".. code-block:: {lang}\n\n" + "\n".join("   " + x for x in code.split("\n")))
            if act.get("content"):
                parts.append(_fill(_text_of(act["content"]), rep))
            if act.get("post"):
                parts.append(_fill(_text_of(act["post"]), rep))
        if d.get("content"):
            parts.append(_fill(_text_of(d["content"]), rep))
        if d.get("post"):
            parts.append(_fill(_text_of(d["post"]), rep))
        for p in parts:
            out.extend("   " + x if x.strip() else "" for x in p.rstrip("\n").split("\n"))
            out.append("")
    return "\n".join(out)


def extract_rst(entry: dict, loader) -> str:
    d = _inherit(entry, loader)
    rep = d.get("replacement") or {}
    parts: list[str] = []
    if d.get("title"):
        parts.append(f"**{_fill(_text_of(d['title']), rep).strip()}**")
    for key in ("pre", "content", "post", "append"):
        if d.get(key):
            parts.append(_fill(_text_of(d[key]), rep))
    return "\n\n".join(parts)


def release_rst(entry: dict, loader) -> str:
    d = _inherit(entry, loader)
    rep = d.get("replacement") or {}
    parts: list[str] = []
    if d.get("pre"):
        parts.append(_fill(_text_of(d["pre"]), rep))
    if d.get("code") is not None:
        lang = str(d.get("language") or "")
        code = _fill(str(d["code"]), rep).rstrip("\n")
        parts.append(f".. code-block:: {lang}\n\n" + "\n".join("   " + x for x in code.split("\n")))
    for key in ("content", "post"):
        if d.get(key):
            parts.append(_fill(_text_of(d[key]), rep))
    return "\n\n".join(parts)


def toc_rst(docs: list, title_of) -> str:
    """Зміст розділу з `toc-*.yaml` (giza, версії 2.x–3.x): запис — сторінка `file`, її назва
    (`name`/`title` або назва самої сторінки) і `description`."""
    out: list[str] = []
    for d in docs:
        if not isinstance(d, dict):
            continue
        path = str(d.get("file") or "").strip()
        name = _text_of(d.get("name") or d.get("title")).strip()
        if not name:
            name = title_of(path) if path else ""
        if not name:
            name = _humanize(path).capitalize() if path else ""
        desc = " ".join(_text_of(d.get("description")).split())
        if not name and not desc:
            continue
        out.append(f"- **{name}** — {desc}" if name and desc else f"- {name or desc}")
    return "\n".join(out) + "\n"


# ── snooty.toml і conf.py ────────────────────────────────────────────────────

_TOML_PAIR = re.compile(r"""^\s*([A-Za-z0-9_.-]+)\s*=\s*(?:"((?:[^"\\]|\\.)*)"|'([^']*)')\s*(?:#.*)?$""")


def toml_section(text: str, section: str) -> dict:
    """Пари `key = "value"` розділу `[section]` файла snooty.toml — без повного TOML."""
    out: dict = {}
    inside = False
    for ln in text.split("\n"):
        s = ln.strip()
        if s.startswith("["):
            inside = s == f"[{section}]"
            continue
        if not inside:
            continue
        m = _TOML_PAIR.match(ln)
        if m:
            val = m.group(2) if m.group(2) is not None else m.group(3)
            out[m.group(1)] = val.replace('\\"', '"').replace("\\\\", "\\")
    return out


def toml_composables(text: str) -> dict:
    """`[[composables]]`: id варіанта → його назва (`nodejs` → «Node.js»)."""
    names: dict = {}
    for m in re.finditer(r'\{\s*id\s*=\s*"([^"]+)"\s*,\s*title\s*=\s*"([^"]+)"', text):
        names.setdefault(m.group(1), m.group(2))
    for m in re.finditer(r'^id\s*=\s*"([^"]+)"\s*\n(?:.*\n)*?title\s*=\s*"([^"]+)"', text, re.M):
        names.setdefault(m.group(1), m.group(2))
    return names


def conf_py(text: str, version: str, branch: str) -> tuple[dict, dict]:
    """Старі гілки без snooty.toml: константи `source_constants` і підстановки `rst_epilog`
    з conf.py. Вирази Python (`version`, `datetime…year`) — значеннями гілки."""
    consts: dict = {}
    block = re.search(r"source_constants\s*=\s*\{(.*?)\n\}", text, re.S)
    if block:
        for m in re.finditer(r"""['"]([\w-]+)['"]\s*:\s*(?:['"]((?:[^'"\\]|\\.)*)['"]|([\w.]+))""",
                             block.group(1)):
            val = m.group(2) if m.group(2) is not None else m.group(3)
            if m.group(2) is None:
                val = version if "version" in val or "release" in val else val
            consts[m.group(1)] = val
    subs: dict = {}
    epilog = re.search(r"rst_epilog\s*=\s*'\\n'\.join\(\[(.*?)\]\)", text, re.S)
    if epilog:
        for m in re.finditer(r"'\.\. \|([^|]+)\| (replace|unicode):: ([^']*)'(\.format\(([^)]*)\))?",
                             epilog.group(1)):
            name, kind, val, fmt = m.group(1), m.group(2), m.group(3), m.group(5)
            if kind == "unicode":
                val = " ".join(chr(int(p[2:], 16)) for p in val.split() if p.upper().startswith("U+"))
            elif fmt:
                args = [a.strip() for a in fmt.split(",")]
                values = []
                for a in args:
                    if "year" in a:
                        import datetime
                        values.append(str(datetime.date.today().year))
                    elif "branch" in a:
                        values.append(branch)
                    elif "version" in a or "release" in a:
                        values.append(version)
                    elif "url" in a:
                        values.append("https://www.mongodb.com/docs")
                    else:
                        values.append(a.strip("'\""))
                try:
                    val = val.format(*values)
                except (IndexError, KeyError, ValueError):
                    pass
            subs[name] = val
    return consts, subs
