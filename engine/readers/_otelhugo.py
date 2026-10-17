"""Шорткоди Hugo сайту opentelemetry.io → текст (поле `otel_hugo` читача `ghdocs-history`).

Сайт OpenTelemetry зібрано Hugo з темою Docsy, і сторінка в репозиторії — не те, що бачить людина:

- `{{% param vers %}}`, `{{% param versions.otelSdk %}}` — номери версій, які сторінка бере з власної
  шапки, з `cascade` шапки `_index.md` свого розділу чи вищих або з `params` у `config/_default/hugo.yaml`;
  без них «npm install @opentelemetry/sdk-node@» обривається на собачці;
- `{{% include "exporters/jaeger.md" %}}` — шматок з теки `_includes` сторінки чи її предків, з
  підстановкою `{{ $key }}` і блоками `{{ if $key }}…{{ end }}`;
- `{{% docs/languages/index-intro js /%}}` — вступ сторінки мови: шаблон шорткода лише називає
  шматок (`"_path" "index-intro.md"`), а ім'я мови й стан трас, метрик і логів бере з
  `data/instrumentation.yaml`;
- `{{< version-from-registry exporter-js-zipkin >}}` — версія пакета з запису реєстру `data/registry`;
- вкладки `{{< tabpane >}}{{% tab npm %}}…` — без підпису вкладки команди npm, yarn і pnpm злилися б
  в одну стрічку коду;
- `{{% config_option name="otel.traces.exporter" %}}` — опція з системною властивістю, змінною
  оточення й типовим значенням, які шаблон складає з аргументів;
- `{{% alert title="Note" %}}`, `figure`, `youtube`, `spec_status` — підпис і текст.

Решта шорткодів (головна сторінка, таблиці екосистеми з даних, лічильники) знімається, а текст між
ними лишається. Невдала вставка просто випадає: ціла сторінка через неї не губиться.

Файли, які вставки можуть узяти, перелічує `WANTED`: їх хеші читач тримає для кожного знімка, а вміст
тягне один раз на хеш.
"""

import re

WANTED = [re.compile(r"^content/en/.+\.md$"), re.compile(r"^layouts/_shortcodes/.+\.md$"),
          re.compile(r"^config/_default/hugo\.yaml$"),
          re.compile(r"^data/(?:registry/.+\.ya?ml|instrumentation\.ya?ml)$")]

_SC = r"\{\{([<%])\s*"
_END = r"\s*/?\s*[>%]\}\}"
_COMMENT_GO = re.compile(r"\{\{-?\s*/\*.*?\*/\s*-?\}\}", re.S)
_COMMENT_SC = re.compile(r"\{\{[<%]\s*comment\s*[>%]\}\}.*?\{\{[<%]\s*/comment\s*[>%]\}\}", re.S)
_PARAM = re.compile(_SC + r"_?param\s+\"?([\w.-]+)\"?" + _END)
_INCLUDE = re.compile(_SC + r"include\s+(.*?)\s*/?\s*[>%]\}\}", re.S)
_REGISTRY = re.compile(_SC + r"version-from-registry\s+\"?([\w.-]+)\"?(?:\s+(\S+))?" + _END)
_TAB_OPEN = re.compile(_SC + r"tab\b(.*?)[>%]\}\}")
_TAB_CLOSE = re.compile(_SC + r"/tab\s*[>%]\}\}")
_TABPANE = re.compile(_SC + r"/?tabpane\b.*?[>%]\}\}")
_CONFIG = re.compile(_SC + r"config_option\b(.*?)[>%]\}\}(.*?)\{\{[<%]\s*/config_option\s*[>%]\}\}", re.S)
_ALERT = re.compile(_SC + r"alert\b(.*?)[>%]\}\}(.*?)\{\{[<%]\s*/alert\s*[>%]\}\}", re.S)
_FIGURE = re.compile(_SC + r"figure\b(.*?)/?[>%]\}\}")
_YOUTUBE = re.compile(_SC + r"youtube\b(.*?)/?[>%]\}\}")
_STATUS = re.compile(_SC + r"spec_status\s+\"([^\"]*)\".*?[>%]\}\}")
_LANG_SC = re.compile(_SC + r"(docs/[\w/-]+)((?:\s+[^/>%\s]+)*)\s*/?\s*[>%]\}\}(?:(.*?)\{\{[<%]\s*/\2\s*[>%]\}\})?",
                      re.S)
_ANY = re.compile(r"\{\{[<%].*?[>%]\}\}", re.S)
_ANCHOR = re.compile(r"^(#{1,6} .*?)[ \t]*\{#[\w.-]+\}[ \t]*$", re.M)
_ARGS = re.compile(r"""(?:(\w+)=)?(?:"((?:[^"\\]|\\.)*)"|'([^']*)'|`([^`]*)`|([^\s"'`]+))""")
_PATH_ARG = re.compile(r'"_path"\s+"([^"]+)"')


def _args(raw: str) -> tuple[list, dict]:
    pos, named = [], {}
    for m in _ARGS.finditer(raw.strip()):
        value = next((g for g in m.groups()[1:] if g is not None), "")
        if m.group(1):
            named[m.group(1)] = value
        elif value not in ("/",):
            pos.append(value)
    return pos, named


# ------------------------------------------------------------------ мінімальний YAML
def _scalar(v: str):
    v = v.strip()
    if v[:1] in "\"'" and v[-1:] == v[:1] and len(v) > 1:
        return v[1:-1]
    if v.startswith("[") and v.endswith("]"):
        return [_scalar(x) for x in v[1:-1].split(",") if x.strip()]
    return v


def _strip_comment(line: str) -> str:
    if line.lstrip().startswith("#"):
        return ""
    m = re.search(r"\s#\s", line)
    if m and line.count('"', 0, m.start()) % 2 == 0 and line.count("'", 0, m.start()) % 2 == 0:
        return line[:m.start()]
    return line


def yaml_subset(text: str):
    """Підмножина YAML, якою написано шапки сторінок, hugo.yaml і записи реєстру: словники за
    відступом, списки «- …» (і словники в них), рядки в лапках і без, блоки «>-»/«|». Бібліотеки
    YAML примірник не тягне: більше цим файлам не треба."""
    lines = [ln.rstrip() for ln in text.replace("\t", "  ").split("\n")]

    def indent(s):
        return len(s) - len(s.lstrip(" "))

    def block(i, ind):
        # Значення, що починається з рядка i з відступом ind: словник або список.
        if i < len(lines) and lines[i].lstrip().startswith("- "):
            out = []
            while i < len(lines):
                ln = _strip_comment(lines[i])
                if not ln.strip():
                    i += 1
                    continue
                if indent(ln) < ind or not ln.lstrip().startswith("-"):
                    break
                item = ln.lstrip()[1:].strip()
                if re.match(r"^[\w.-]+:(\s|$)", item):
                    # словник у списку: перший ключ на рядку з дефісом
                    lines[i] = " " * (indent(ln) + 2) + item
                    val, i = mapping(i, indent(ln) + 2)
                    out.append(val)
                else:
                    out.append(_scalar(item))
                    i += 1
            return out, i
        return mapping(i, ind)

    def mapping(i, ind):
        out = {}
        while i < len(lines):
            ln = _strip_comment(lines[i])
            if not ln.strip():
                i += 1
                continue
            if indent(ln) < ind:
                break
            if indent(ln) > ind:
                i += 1
                continue
            m = re.match(r"^\s*([\w.@/-]+|\"[^\"]+\"|'[^']+')\s*:(?:\s+(.*))?$", ln)
            if not m:
                i += 1
                continue
            key, val = _scalar(m.group(1)), (m.group(2) or "").strip()
            i += 1
            if val in (">-", ">", "|", "|-", ">+", "|+"):
                body = []
                while i < len(lines) and (not lines[i].strip() or indent(lines[i]) > ind):
                    body.append(lines[i].strip())
                    i += 1
                joiner = "\n" if val.startswith("|") else " "
                out[key] = joiner.join(body).strip()
            elif val:
                out[key] = _scalar(val)
            else:
                j = i
                while j < len(lines) and not _strip_comment(lines[j]).strip():
                    j += 1
                if j < len(lines) and (indent(lines[j]) > ind or
                                       (indent(lines[j]) == ind and lines[j].lstrip().startswith("- "))):
                    out[key], i = block(j, indent(lines[j]))
                else:
                    out[key] = ""
        return out, i

    try:
        return block(0, 0)[0]
    except (IndexError, ValueError):
        return {}


def _front(text: str) -> dict:
    m = re.match(r"\A﻿?---\n(.*?)\n---\n", text.replace("\r\n", "\n"), re.S)
    return yaml_subset(m.group(1)) if m else {}


def _dig(data, dotted: str):
    cur = data
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur if isinstance(cur, (str, int, float)) else None


# ------------------------------------------------------------------ розгортання
class _Site:
    """Файли знімка, які потрібні вставкам, з кешем розібраного вмісту на весь прогін."""

    def __init__(self, files: dict, fetch):
        self.files, self.fetch = files, fetch

    def text(self, path: str) -> str:
        sha = self.files.get(path)
        return self.fetch(path, sha) if sha else ""

    def front(self, path: str) -> dict:
        key = ("front", path)
        if key not in _CACHE:
            _CACHE[key] = _front(self.text(path))
        return _CACHE[key]

    def yaml(self, path: str):
        key = ("yaml", path)
        if key not in _CACHE:
            _CACHE[key] = yaml_subset(self.text(path))
        return _CACHE[key]


_CACHE: dict = {}


def _ancestors(path: str) -> list[str]:
    """Теки від теки сторінки до content/en включно, найближча першою."""
    parts = path.split("/")[:-1]
    out = []
    while len(parts) >= 2:
        out.append("/".join(parts))
        if parts[-1] == "en" and parts[-2] == "content":
            break
        parts = parts[:-1]
    return out


def _param(name: str, path: str, page_front: dict, site: _Site) -> str:
    value = _dig(page_front, name)
    if value is None:
        for d in _ancestors(path):
            front = site.front(f"{d}/_index.md")
            value = _dig(front.get("cascade") if isinstance(front.get("cascade"), dict) else {}, name)
            if value is not None:
                break
    if value is None:
        conf = site.yaml("config/_default/hugo.yaml")
        value = _dig(conf.get("params") if isinstance(conf, dict) else {}, name)
    return "" if value is None else str(value)


def _find_include(name: str, path: str, site: _Site) -> str:
    name = name if name.endswith(".md") else name + ".md"
    if name.startswith("/"):
        cands = [f"content/en{name}"]
    elif name.startswith("."):
        cands = [f"{path.rsplit('/', 1)[0]}/{name.lstrip('./')}"]
    else:
        cands = [f"{d}/_includes/{name}" for d in _ancestors(path)]
    return next((c for c in cands if c in site.files), "")


def _substitute(piece: str, args: dict) -> str:
    for k, v in args.items():
        piece = re.sub(r"\{\{\s*\$" + re.escape(k) + r"\s*\}\}", lambda _m, v=v: v, piece)
        flag = bool(v)
        piece = re.sub(r"(?ms)^\{\{\s*if\s+\$" + re.escape(k) + r"\s*\}\}(.+?)^\{\{\s*end\s*\}\}\n?",
                       (lambda m: m.group(1)) if flag else "", piece)
        piece = re.sub(r"(?ms)^\{\{\s*if\s+not\s+\$" + re.escape(k) + r"\s*\}\}(.+?)^\{\{\s*end\s*\}\}\n?",
                       "" if flag else (lambda m: m.group(1)), piece)
    # Аргумент, якого не передали, — порожній, як у Hugo.
    piece = re.sub(r"(?ms)^\{\{\s*if\s+\$[\w.]+\s*\}\}.+?^\{\{\s*end\s*\}\}\n?", "", piece)
    piece = re.sub(r"(?ms)^\{\{\s*if\s+not\s+\$[\w.]+\s*\}\}(.+?)^\{\{\s*end\s*\}\}\n?", r"\1", piece)
    return re.sub(r"\{\{\s*\$[\w.]+\s*\}\}", "", piece)


def _include(target: str, args: dict, path: str, site: _Site, page_front: dict, depth: int) -> str:
    found = _find_include(target, path, site)
    if not found or depth >= 4:
        return ""
    body = re.sub(r"\A﻿?---\n(?:.*?\n)?---\n", "", site.text(found).replace("\r\n", "\n"), flags=re.S)
    body = _substitute(body, args)
    return "\n" + _expand(body, path, page_front, site, depth + 1).strip("\n") + "\n"


def _status(lang: str, signal: str, site: _Site) -> str:
    data = site.yaml("data/instrumentation.yaml")
    value = _dig(data, f"{lang}.status.{signal}") if isinstance(data, dict) else None
    if value is None:
        return "-"
    value = "development" if value in ("experimental", "in development") else str(value)
    return value.capitalize()


def _lang_shortcode(m, path: str, page_front: dict, site: _Site, depth: int) -> str:
    name, raw_args, inner = m.group(2), m.group(3) or "", m.group(4) or ""
    template = site.text(f"layouts/_shortcodes/{name}.md")
    target = _PATH_ARG.search(template)
    if not target:
        return inner
    pos, named = _args(raw_args)
    lang = pos[0] if pos else ""
    if not lang:
        hit = re.match(r"^content/en/docs/languages/([^/]+)/", path)
        lang = ("dotnet" if hit and hit.group(1) == "net" else hit.group(1)) if hit else ""
    data = site.yaml("data/instrumentation.yaml")
    lname = _dig(data, f"{lang}.name") if isinstance(data, dict) and lang else ""
    args = {"lang": lang, "name": lname or "", ".Inner": inner.strip(), "Inner": inner.strip()}
    for sig in ("traces", "metrics", "logs", "profiles"):
        args[f"{sig}Status"] = _status(lang, sig, site) if lang else "-"
    args.update(named)
    out = _include(target.group(1), args, path, site, page_front, depth)
    return out.replace("{{ $.Inner }}", inner.strip())


def _expand(text: str, path: str, page_front: dict, site: _Site, depth: int = 0) -> str:
    text = _COMMENT_GO.sub("", text)
    text = _COMMENT_SC.sub("", text)
    text = _PARAM.sub(lambda m: _param(m.group(2), path, page_front, site), text)

    def include(m):
        pos, named = _args(m.group(2))
        target = named.pop("file", "") or (pos.pop(0) if pos else "")
        args = {str(i): v for i, v in enumerate(pos)} | named
        return _include(target, args, path, site, page_front, depth) if target else ""

    text = _INCLUDE.sub(include, text)
    text = _LANG_SC.sub(lambda m: _lang_shortcode(m, path, page_front, site, depth), text)

    def registry(m):
        data = site.yaml(f"data/registry/{m.group(2)}.yml") or site.yaml(f"data/registry/{m.group(2)}.yaml")
        version = _dig(data, "package.version") if isinstance(data, dict) else None
        if not version:
            return ""
        return str(version).lstrip("v") if m.group(3) and m.group(3).strip('"') not in ("false", "") else str(version)

    text = _REGISTRY.sub(registry, text)

    def config(m):
        _, named = _args(m.group(2))
        name = named.get("name", "")
        env = named.get("envVar") or re.sub(r"[.-]", "_", name.upper())
        default = f"; default: {named['default']}" if "default" in named else ""
        return (f"\n\n**`{name}`** — system property `{name}`, environment variable `{env}`{default}.\n\n"
                f"{m.group(3).strip()}\n\n")

    text = _CONFIG.sub(config, text)

    def alert(m):
        _, named = _args(m.group(2))
        label = named.get("title") or (named.get("color") or "note").capitalize()
        return f"\n\n{label}: {m.group(3).strip()}\n\n"

    text = _ALERT.sub(alert, text)

    def tab(m):
        pos, named = _args(m.group(2))
        label = named.get("header") or (pos[0] if pos else "") or named.get("lang", "")
        return f"\n\n{label}:\n\n" if label else "\n\n"

    text = _TAB_OPEN.sub(tab, text)
    text = _TAB_CLOSE.sub("\n", text)
    text = _TABPANE.sub("\n", text)

    def figure(m):
        _, named = _args(m.group(2))
        caption = named.get("caption") or named.get("title") or named.get("alt") or ""
        return f"\n\n{caption}\n\n" if caption else ""

    text = _FIGURE.sub(figure, text)

    def youtube(m):
        _, named = _args(m.group(2))
        return f"\n\nVideo: {named['title']}\n\n" if named.get("title") else ""

    text = _YOUTUBE.sub(youtube, text)
    text = _STATUS.sub(lambda m: f"**{m.group(2)}**", text)
    # Якір заголовка Hugo («## Dependencies {#otlp-dependencies}») — розмітка, а не назва.
    text = _ANCHOR.sub(r"\1", text)
    return _ANY.sub("", text)


def expand(text: str, path: str, page: str, files: dict, fetch) -> str:
    """`text` — тіло сторінки без шапки, `page` — повний текст файла (з шапкою: звідти `param`),
    `files` — {шлях: sha} файлів знімка з `WANTED`, `fetch(шлях, sha)` — вміст файла."""
    site = _Site(files, fetch)
    return _expand(text, path, _front(page), site)
