"""Читачі документації Kubernetes: kubernetes.io з усіх гілок, журнали змін, розклад релізів.

`k8s-docs`      — сторінки документації на кожній оголошеній гілці, тезі чи коміті одного
                  репозиторію. `url` — префікс дерев (…/repos/ВЛАСНИК/РЕПО/git/trees/),
                  `refs` — об'єкт «гілка, тег чи коміт → версія», від найновішого.
                  Необов'язкові: `folders` — теки від кореня репозиторію (тоді беруться лише
                  вони, як готовий текст, без обробки шорткодів — так читаються згенеровані
                  довідники `static/docs/reference/generated`), `exclude` — вирази шляхів від
                  кореня репозиторію, що не беруться.
`k8s-changelog` — CHANGELOG/CHANGELOG-1.N.md з kubernetes/kubernetes. `url` — префікс теки,
                  `files` — імена файлів. Кожен заголовок «# v1.37.1» — документ із версією
                  «1.37.1», без розділів «Downloads for …» (таблиці архівів і хешів).
`k8s-releases`  — data/releases/schedule.yaml і eol.yaml сайту: коли вийшла кожна лінія,
                  патчі з датами, кінець підтримки. `url` — schedule.yaml, `eol` — eol.yaml.

Навіщо окремі читачі. Документація Kubernetes живе гілками: `release-1.4` … `release-1.36`
і `main` (поточна лінія), по одній гілці на мінорну версію. За ці десять років сайт тричі
міняв устрій, і жоден наявний читач не дає ради жодному з них:

1. kubernetes/kubernetes, теги v1.0–v1.1 — тека `docs/`, звичайний markdown GitHub. Тут
   нічого розгортати, лише прибрати пікселі аналітики. З v1.2 файли тут — заглушки «This file
   has moved», а сама документація вже на сайті.
2. Jekyll (сайт 2016–2017, гілки до release-1.9 і коміти 2016 року для 1.2 і 1.3) — тека
   `docs/`, Liquid: `{% capture overview %}` … і шаблон сторінки, що збирає ці блоки з
   заголовками («Before you begin», «What's next»), `{% include code.html file=… %}` (приклад
   із теки сторінки), `{% include tabs.md %}` з вкладками з `capture`, врізки `_includes/`.
3. Hugo (release-1.10 і новіші) — `content/en/docs`, шорткоди `{{< … >}}`: `note`, `caution`,
   `warning` (підпис і текст), `glossary_tooltip` (слово), `feature-state` (рядок «Feature
   state: Kubernetes v1.33 [stable]», для `feature_gate_name` — зі сторінки цього feature gate
   на тій самій гілці), `code_sample`/`codenew`/`code` (файл із `content/en/examples` чи теки
   сторінки стає блоком коду), `include` (`content/en/includes`), `heading` (англійський рядок
   i18n), `skew` і `param` (номер версії гілки), вкладки, таблиці, mermaid. До 1.17 сторінки
   ще й складалися з `{{% capture … %}}`, як у Jekyll.

Без розгортання шорткодів сторінка в корпусі — шматки розмітки, приклади без коду («Create a
Deployment based on the YAML file:» — і далі порожньо), «Feature state» без номера версії.

Одиниця — сторінка на гілці, а текст тягнеться раз на хеш. Те, що сторінка показує, залежить
не лише від її файла: номер у `skew` — від версії гілки, приклад — від файла прикладу тієї ж
гілки, стан feature gate — від його сторінки. Той самий файл на двох гілках дає різний текст:
«kubeadm upgrade apply v1.36.x» і «… v1.30.x». Тому для markdown Jekyll і Hugo документ — пара
«сторінка, гілка», з версією цієї гілки, а файл сторінки тягнеться один раз на хеш: документи
однієї пари «шлях, вміст» ідуть у переліку підряд, і текст береться з пам'яті попереднього.
Приклади, врізки, глосарій і сторінки feature gate тягнуться теж раз на хеш (хеші — з дерев
гілок). Однаковий текст сусідніх гілок зливається вже на рівні фрагментів (`revision_suffix`
у config.json): фрагмент лишається один, а в його версії дописується кожна гілка, де він такий.

Там, де від гілки нічого не залежить, — сторінки kubernetes/kubernetes, HTML, згенеровані
довідники, файли з версією в шляху (`api-reference/v1.8/`) — документ один на пару «шлях,
вміст», з усіма версіями, як у `ghdocs-history`. Версія з шляху (`v1.21/` у
`generated/kubernetes-api/v1.21/index.html`) важить більше за гілку: на гілці release-1.28
лежать довідники API і 1.23, і 1.28, і кожен — про свою версію.

`refs` — гілки (рухомі) і коміти. Сторінка, що змінилася на `main`, дає новий документ, а
попередній стає сиротою: `check` показує таких, прибирає їх людина — читач нічого не видаляє.
"""

import hashlib
import json
import posixpath
import re
from html import unescape
from urllib.parse import quote, urlsplit

from engine.readers import Item, _markup, register
from engine.readers.ghhistory import _atx, _split_title

_TREES = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/$")
# Версія в шляху: «kubernetes-api/v1.21/», «user-guide/kubectl/v1.5/».
_PATH_VERSION = re.compile(r"(?:^|/)v(1\.\d+)(?=/|$)")
# Службове дерево npm у теках старих довідників і переклади — не документація.
_ALWAYS_SKIP = re.compile(r"(^|/)node_modules/")
_EXTS = (".md", ".html")
# Обхід трьох з половиною десятків гілок триває хвилини, і рядок поступу показує, що він живий.
_PROGRESS = 5
# Скільки разів шорткод `include` може вкласти сам себе: врізки бувають вкладені на рівень-два,
# а більше — це вже петля.
_DEPTH = 3
# Скільки допоміжних файлів (приклади, врізки, глосарій) тримати в пам'яті. Різних на всі гілки
# — кілька тисяч по кілобайту; межа лише від того, щоб пам'ять не росла без краю.
_MEMO_MAX = 6000

# ── дерева й допоміжні файли ──────────────────────────────────────────────────


def _tree(ctx, url: str) -> list:
    try:
        data = json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(data, dict) or not isinstance(data.get("tree"), list):
        raise SystemExit(f"{url}: у відповіді немає дерева файлів.")
    if data.get("truncated"):
        raise SystemExit(f"{url}: GitHub обрізав дерево — перелік був би неповним.")
    return data["tree"]


class _Ref:
    """Одна гілка (тег, коміт): доба сайту, файли документації, приклади й врізки з хешами."""

    def __init__(self, ref: str, label: str):
        self.ref = ref
        self.label = label
        self.era = ""            # hugo | jekyll | plain | static
        self.docs_root = ""      # шлях теки документації від кореня репозиторію
        self.docs: dict = {}     # шлях від docs_root → (хеш, розмір)
        self.examples: dict = {}  # шлях від content/en/examples → хеш
        self.includes: dict = {}  # ім'я врізки → хеш
        self.root_blobs: set = set()
        self.params: dict | None = None
        self.patches: dict | None = None


class _Site:
    """Звернення одного джерела: дерева через API (піддерево — раз на хеш) і сирі файли (раз
    на хеш, з пам'яттю)."""

    def __init__(self, source: dict, ctx):
        m = _TREES.match(urlsplit(source["url"]).path)
        if not m:
            raise SystemExit(f"{source['url']}: очікував префікс дерев "
                             f"/repos/ВЛАСНИК/РЕПО/git/trees/.")
        self.owner, self.repo = m.groups()
        self.ctx = ctx
        self.trees_url = source["url"]
        self.raw_base = f"https://raw.githubusercontent.com/{self.owner}/{self.repo}"
        self.flat: dict = {}       # хеш дерева → його записи (без рекурсії)
        self.deep: dict = {}       # хеш дерева → його записи (з рекурсією)
        self.memo: dict = {}       # хеш файла → текст
        self.last = ("", "")       # (хеш, текст) останнього тіла сторінки

    def entries(self, sha: str, recursive: bool = False) -> list:
        store = self.deep if recursive else self.flat
        if sha not in store:
            suffix = "?recursive=1" if recursive else ""
            store[sha] = _tree(self.ctx, f"{self.trees_url}{quote(sha, safe='@')}{suffix}")
        return store[sha]

    def subtree(self, root: list, path: str) -> str:
        """Хеш теки `path` (через «/») від записів кореня; "" — такої теки немає."""
        entries, sha = root, ""
        parts = path.split("/")
        for i, part in enumerate(parts):
            sha = next((e["sha"] for e in entries
                        if e.get("path") == part and e.get("type") == "tree"), "")
            if not sha:
                return ""
            if i < len(parts) - 1:
                entries = self.entries(sha)
        return sha

    def raw(self, ref: str, path: str) -> str:
        return f"{self.raw_base}/{quote(ref, safe='@')}/{quote(path)}"

    def text(self, ref: str, path: str, sha: str = "") -> str | None:
        """Сирий файл; None — адреса поза білим списком. З хешем — раз на хеш."""
        if sha and sha in self.memo:
            return self.memo[sha]
        url = self.raw(ref, path)
        if not self.ctx.allowed(url):
            return None
        text = self.ctx.text(url).replace("\r\n", "\n")
        if sha:
            if len(self.memo) >= _MEMO_MAX:
                self.memo.clear()
            self.memo[sha] = text
        return text

    def page(self, ref: str, path: str, sha: str) -> str:
        """Тіло сторінки: документи однієї пари «шлях, вміст» ідуть підряд, тож друге й далі
        звернення бере текст із пам'яті попереднього."""
        if self.last[0] != sha:
            url = self.raw(ref, path)
            text = self.ctx.text(url)
            if path.endswith(".md"):
                _markup.refuse_html(text, url)
            self.last = (sha, text.replace("\r\n", "\n"))
        return self.last[1]


def _blobs(entries: list, prefix: str = "") -> dict:
    return {prefix + e["path"]: (e["sha"], e.get("size", 0)) for e in entries
            if e.get("type") == "blob"}


def _walk_ref(site: _Site, ref: _Ref, folders: list) -> None:
    """Доба гілки за її коренем і файли документації, прикладів та врізок з хешами."""
    root = site.entries(ref.ref)
    names = {e["path"]: e for e in root}
    ref.root_blobs = {p for p, e in names.items() if e.get("type") == "blob"}

    def deep(path: str) -> dict:
        sha = site.subtree(root, path)
        return _blobs(site.entries(sha, recursive=True)) if sha else {}

    if folders:
        ref.era = "static"
        for folder in folders:
            sha = site.subtree(root, folder.strip("/"))
            if sha:
                ref.docs.update(_blobs(site.entries(sha, recursive=True),
                                       folder.strip("/") + "/"))
        return
    if names.get("content", {}).get("type") == "tree":
        ref.era, ref.docs_root = "hugo", "content/en/docs"
        ref.docs = deep(ref.docs_root)
        ref.examples = {p: s for p, (s, _) in deep("content/en/examples").items()}
        ref.includes = {p: s for p, (s, _) in deep("content/en/includes").items()}
    elif "_includes" in names or "_config.yml" in names:
        ref.era, ref.docs_root = "jekyll", "docs"
        ref.docs = deep("docs")
        ref.includes = {p: s for p, (s, _) in deep("_includes").items()}
    elif names.get("docs", {}).get("type") == "tree":
        ref.era, ref.docs_root = "plain", "docs"
        ref.docs = deep("docs")


def _stem(rel: str) -> str:
    """Ім'я сторінки зі шляху: без розширення, без «_index»/«index», без версії в шляху —
    щоб той самий довідник різних версій мав одне ім'я і його незмінні розділи зливалися."""
    stem = re.sub(r"\.(md|html)$", "", rel)
    stem = re.sub(r"(^|/)_?index$", "", stem) or "index"
    return _PATH_VERSION.sub("", stem) or stem


# ── шапка сторінки ────────────────────────────────────────────────────────────

_FRONT_YAML = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)
_FRONT_TOML = re.compile(r"\A\+\+\+[ \t]*\n(.*?)\n\+\+\+[ \t]*(?:\n|\Z)", re.S)
_FOLDED = (">", ">-", "|", "|-", ">+", "|+")


def front(text: str) -> tuple[dict, str, str]:
    """(поля шапки, текст без шапки, сира шапка). Окрім «ключ: значення» в рядок, як
    `_markup.front_matter`, розуміє складене значення (`description: >` і рядки з відступом
    під ним) і шапку TOML (`+++`, `title = "…"`), яку мають кілька старих сторінок."""
    text = text.replace("\r\n", "\n").lstrip("﻿")
    m = _FRONT_YAML.match(text)
    if not m:
        t = _FRONT_TOML.match(text)
        if not t:
            return {}, text, ""
        meta = {}
        for ln in t.group(1).splitlines():
            key, sep, value = ln.partition("=")
            if sep and key.strip() and not key[:1].isspace():
                meta[key.strip()] = value.strip().strip('"').strip("'")
        return meta, text[t.end():], t.group(1)
    meta: dict = {}
    lines = m.group(1).splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        key, sep, value = ln.partition(":")
        i += 1
        if not sep or not key.strip() or key[:1].isspace():
            continue
        value = value.strip()
        if value in _FOLDED:
            block = []
            while i < len(lines) and (not lines[i].strip() or lines[i][:1].isspace()):
                block.append(lines[i].strip())
                i += 1
            joiner = "\n" if value.startswith("|") else " "
            value = joiner.join(block).strip()
        meta[key.strip()] = value.strip('"').strip("'")
    return meta, text[m.end():], m.group(1)


def gate_stages(raw_front: str) -> list[dict]:
    """Стадії feature gate з шапки його сторінки: список `stages:` з полями `stage`,
    `defaultValue`, `fromVersion`, `toVersion`, `locked`."""
    stages: list[dict] = []
    inside = False
    for ln in raw_front.splitlines():
        if re.match(r"^stages:\s*$", ln):
            inside = True
            continue
        if inside and ln.strip() and not ln[:1].isspace() and not ln.startswith("-"):
            break
        if not inside:
            continue
        m = re.match(r"^\s*(-\s+)?(\w+):\s*(.*?)\s*$", ln)
        if not m:
            continue
        if m.group(1) or not stages:
            stages.append({})
        stages[-1][m.group(2)] = m.group(3).strip('"').strip("'")
    return stages


def gate_lines(raw_front: str, meta: dict) -> str:
    """Стадії feature gate людськими рядками: на самій сторінці gate вони лише в шапці, а
    відповідь «з якої версії це beta і чи ввімкнено типово» — саме звідти."""
    out = []
    for st in gate_stages(raw_front):
        span = st.get("fromVersion", "?")
        if st.get("toVersion"):
            span += f"–{st['toVersion']}"
        default = {"true": "enabled by default", "false": "disabled by default"}.get(
            st.get("defaultValue", "").lower(), "")
        extra = ", ".join(x for x in (default, "locked" if st.get("locked") == "true" else "")
                          if x)
        out.append(f"- {st.get('stage', '?')}: Kubernetes {span}" + (f" ({extra})" if extra
                                                                      else ""))
    if not out:
        return ""
    head = "Feature gate stages:"
    if meta.get("removed") in ("true", "True"):
        head = "Feature gate stages (the gate has been removed):"
    return head + "\n\n" + "\n".join(out)


# ── шорткоди Hugo ─────────────────────────────────────────────────────────────

# Рядки i18n/en/en.toml, які сторінка показує замість `{{< heading "…" >}}` і блоків capture.
HEADINGS = {
    "prerequisites": "Before you begin", "whatsnext": "What's next",
    "objectives": "Objectives", "cleanup": "Cleaning up", "synopsis": "Synopsis",
    "options": "Options", "seealso": "See Also", "parentoptions": "Parent Options Inherited",
    "examples": "Examples", "envvars": "Environment variables", "feedback": "Feedback",
}
LABELS = {"note": "Note:", "caution": "Caution:", "warning": "Warning:"}
# Порядок блоків capture у шаблонах сторінки (concept, task, tutorial): сторінка показує їх
# у цьому порядку, хоч би як їх розставили у файлі; заголовок мають лише деякі.
CAPTURE_ORDER = ("overview", "objectives", "prerequisites", "steps", "lessoncontent",
                 "discussion", "body", "", "cleanup", "whatsnext")
CAPTURE_HEADINGS = {"prerequisites": "Before you begin", "objectives": "Objectives",
                    "cleanup": "Cleaning up", "whatsnext": "What's next"}

_SC = re.compile(r"\{\{([<%])\s*(/?)\s*([\w-]+)(.*?)\s*/?\s*[>%]\}\}", re.S)
_SC_ESCAPED = re.compile(r"\{\{([<%])/\*\s*(.*?)\s*\*/([>%])\}\}", re.S)
_ARG = re.compile(r'(?:([\w-]+)\s*=\s*)?(?:"((?:[^"\\]|\\.)*)"|“([^”]*)”|`([^`]*)`|'
                  r"'([^']*)'|([^\s\"'`=]+))")


def _pair(name: str) -> re.Pattern:
    return re.compile(r"\{\{[<%]\s*" + name + r"\b(.*?)[>%]\}\}(.*?)\{\{[<%]\s*/\s*" + name
                      + r"\s*[>%]\}\}", re.S)


_COMMENT_PAIR = _pair("comment")
_HIGHLIGHT_PAIR = _pair("highlight")
_MERMAID_PAIR = _pair("mermaid")
_CAPTURE_PAIR = _pair("capture")


def args_of(raw: str) -> tuple[list, dict]:
    """(позиційні, іменовані) аргументи шорткоду."""
    pos, named = [], {}
    for m in _ARG.finditer(raw or ""):
        value = next((g for g in m.groups()[1:] if g is not None), "")
        value = value.replace('\\"', '"')
        if m.group(1):
            named[m.group(1)] = value
        else:
            pos.append(value)
    return pos, named


def _minor(version: str) -> tuple[str, int]:
    """«v1.36» → ("1", 36)."""
    nums = re.findall(r"\d+", version)
    return (nums[0], int(nums[1])) if len(nums) >= 2 else ("1", 0)


def skew(pos: list, version: str, patch: str) -> str:
    """Номер, який показує `{{< skew … >}}`. Відлік — від версії самої гілки: у старих гілках
    поле `latest` конфігурації пізніше переписали на тодішню найновішу лінію (у release-1.25
    стоїть v1.29), а автор сторінки 1.25 мав на увазі саме 1.25."""
    major, minor = _minor(version)
    kind = pos[0] if pos else ""
    step = int(pos[1]) if len(pos) > 1 and re.fullmatch(r"-?\d+", pos[1]) else 0
    sep = pos[2] if len(pos) > 2 and pos[2] else "."
    if kind in ("currentVersion", "latestVersion"):
        return f"{major}.{minor}"
    if kind == "nextMinorVersion":
        return f"{major}.{minor + 1}"
    if kind == "prevMinorVersion":
        return f"{major}.{minor - 1}"
    if kind == "oldestMinorVersion":
        return f"{major}.{minor - 2}"
    if kind in ("currentVersionAddMinor", "latestVersionAddMinor"):
        return f"{major}{sep}{minor + step}"
    if kind == "currentPatchVersion":
        return patch or f"{major}.{minor}.0"
    return f"{major}.{minor}"


def feature_state(named: dict, version: str, gate: tuple | None) -> str:
    """Рядок «Feature state: Kubernetes v1.33 [stable]». `gate` — (поля, сира шапка)
    сторінки feature gate для `feature_gate_name`, None — gate не знайдено."""
    name = named.get("feature_gate_name", "")
    if name:
        if not gate:
            return f"Feature state: feature gate {name}"
        meta, raw_front = gate
        stages = gate_stages(raw_front)
        if not stages:
            return f"Feature state: feature gate {name}"
        cur = stages[-1]
        if meta.get("removed") in ("true", "True"):
            last = cur.get("toVersion") or cur.get("fromVersion", "?")
            return (f"Feature state: feature gate {name} has been removed "
                    f"(last stage: {cur.get('stage', '?')}, Kubernetes {last})")
        default = {"true": "enabled by default", "false": "disabled by default"}.get(
            cur.get("defaultValue", "").lower(), "")
        line = (f"Feature state: Kubernetes v{cur.get('fromVersion', '?').lstrip('v')} "
                f"[{cur.get('stage', '?')}]")
        return line + (f" (feature gate {name}, {default})" if default
                       else f" (feature gate {name})")
    state = named.get("state", "")
    ver = named.get("for_k8s_version") or version
    return f"Feature state: Kubernetes v{ver.lstrip('v')} [{state}]"


class Page:
    """Що сторінка бачить навколо себе під час розгортання шорткодів: версію своєї гілки,
    поля шапки і доступ до прикладів, врізок, глосарію та сторінок feature gate тієї ж гілки.
    `load(kind, name)` повертає текст або None; kind — example, include, doc, page_file,
    jekyll_include, jekyll_data."""

    def __init__(self, meta: dict, rel: str, version: str, load, params: dict | None = None,
                 patch: str = ""):
        self.meta = meta
        self.dir = posixpath.dirname(rel)
        self.version = version if version.startswith("v") else f"v{version}"
        self.load = load
        self.params = params or {}
        self.patch = patch

    def param(self, name: str) -> str:
        if name in self.meta and self.meta[name]:
            return self.meta[name]
        if name == "version":
            return self.version
        return self.params.get(name, name)

    def term(self, term_id: str) -> tuple[dict, str]:
        """(поля, тіло) сторінки глосарію."""
        text = self.load("doc", f"reference/glossary/{term_id}.md")
        if text is None:
            return {}, ""
        meta, body, _ = front(text)
        return meta, body

    def code(self, file: str, lang: str, where: str) -> str:
        """Файл прикладу блоком коду з ім'ям файла рядком перед ним — як на сторінці."""
        text = self.load(where, file)
        if text is None:
            return f"\n\n`{file}`\n\n"
        lang = lang or posixpath.splitext(file)[1].lstrip(".")
        fence = "````" if "```" in text else "```"
        return f"\n\n`{file}`\n\n{fence}{lang}\n{text.rstrip()}\n{fence}\n\n"


def _protect(store: list, text: str) -> str:
    store.append(text)
    return f"\x00{len(store) - 1}\x00"


def _restore(store: list, text: str) -> str:
    for _ in range(3):
        if "\x00" not in text:
            break
        text = re.sub(r"\x00(\d+)\x00", lambda m: store[int(m.group(1))], text)
    return text


def _captures(text: str, pair: re.Pattern, headings: dict = CAPTURE_HEADINGS) -> str:
    """Сторінка з блоків capture — у порядку шаблону, з заголовками шаблону."""
    blocks: dict = {}
    order: list = []

    def take(m):
        name = args_of(m.group(1))[0][:1] or [""]
        blocks[name[0]] = blocks.get(name[0], "") + m.group(2)
        order.append(name[0])
        return ""

    rest = pair.sub(take, text)
    if not blocks:
        return text
    blocks[""] = rest
    out = []
    for name in list(CAPTURE_ORDER) + [n for n in order if n not in CAPTURE_ORDER]:
        body = blocks.pop(name, "")
        if not body.strip():
            continue
        if name in headings:
            out.append(f"\n\n## {headings[name]}\n\n")
        out.append(body)
    return "".join(out)


def hugo(text: str, page: Page, depth: int = 0) -> str:
    """Markdown сторінки Hugo з розгорнутими шорткодами."""
    store: list = []
    text = _SC_ESCAPED.sub(lambda m: _protect(store, "{{" + m.group(1) + " " + m.group(2)
                                              + " " + m.group(3) + "}}"), text)
    text = _COMMENT_PAIR.sub("", text)
    text = _HIGHLIGHT_PAIR.sub(lambda m: _protect(
        store, f"\n\n```{(args_of(m.group(1))[0] or [''])[0]}\n{m.group(2).strip(chr(10))}"
               f"\n```\n\n"), text)
    text = _MERMAID_PAIR.sub(lambda m: _protect(
        store, f"\n\n```mermaid\n{m.group(2).strip(chr(10))}\n```\n\n"), text)
    text = _captures(text, _CAPTURE_PAIR)

    # Вкладка з `codelang` і без `include` — це блок коду: огорожа відкривається з тегом
    # вкладки й закривається з його парою, тож відкриті вкладки тримаються стосом.
    tabs: list = []

    def one(m) -> str:
        closing, name, raw = m.group(2), m.group(3), m.group(4)
        if closing:
            if name == "tab" and tabs and tabs.pop():
                return "\n```\n\n"
            return "\n\n" if name not in ("example", "link") else ""
        pos, named = args_of(raw)
        if name in LABELS:
            return f"\n\n{LABELS[name]}\n\n"
        if name == "alert":
            title = named.get("title") or "Note"
            return f"\n\n{title.rstrip(':')}:\n\n"
        if name == "glossary_tooltip":
            if named.get("text"):
                return named["text"]
            term = named.get("term_id", "")
            return page.term(term)[0].get("title") or term.replace("-", " ")
        if name == "glossary_definition":
            meta, body = page.term(named.get("term_id", ""))
            body = body.split("<!--more-->", 1)
            short = body[0].strip()
            text_ = short if named.get("length", "short") == "short" else "\n\n".join(
                b.strip() for b in body)
            if named.get("prepend") and text_:
                text_ = f"{named['prepend']} {text_[:1].lower()}{text_[1:]}"
            return hugo(text_, page, depth + 1) if depth < _DEPTH else text_
        if name == "heading":
            key = pos[0] if pos else ""
            return HEADINGS.get(key, key.replace("_", " ").capitalize())
        if name == "feature-state":
            gate = None
            if named.get("feature_gate_name"):
                path = ("reference/command-line-tools-reference/feature-gates/"
                        f"{named['feature_gate_name']}.md")
                gtext = page.load("doc", path)
                if gtext is None:
                    gtext = page.load("doc", path.replace("feature-gates/",
                                                          "feature-gates-removed/"))
                if gtext is not None:
                    gmeta, _, graw = front(gtext)
                    gate = (gmeta, graw)
            return f"\n\n{feature_state(named, page.param('version'), gate)}\n\n"
        if name in ("code_sample", "codenew"):
            return page.code(named.get("file", ""), named.get("language", ""), "example")
        if name == "code":
            return page.code(named.get("file", ""), named.get("language", ""), "page_file")
        if name == "readfile":
            # Сайти Docsy (Gateway API) вставляють файл репозиторію: «/examples/…» — від кореня,
            # інакше — від теки сторінки; `code="true"` — блоком коду, без нього — текстом.
            file = named.get("file", pos[0] if pos else "")
            where = "repo" if file.startswith("/") else "page_file"
            if named.get("code", "").lower() == "true":
                return page.code(file.lstrip("/") if where == "repo" else file,
                                 named.get("lang", ""), where)
            inc = page.load(where, file.lstrip("/") if where == "repo" else file)
            if inc is None or depth >= _DEPTH:
                return ""
            return f"\n\n{hugo(front(inc)[1], page, depth + 1)}\n\n"
        if name == "def":
            # Глосарій Let's Encrypt: назва терміна лише в атрибутах.
            term = named.get("name", "")
            if named.get("abbr") and named["abbr"] != term:
                term = f"{term} ({named['abbr']})"
            return f"\n\n{term}:\n\n" if term else "\n\n"
        if name == "include":
            inc = page.load("include", pos[0]) if pos else None
            if inc is None and pos:
                inc = page.load("page_file", pos[0] if pos[0].endswith(".md")
                                else pos[0] + ".md")
            if inc is None:
                return ""
            inc = front(inc)[1]
            return f"\n\n{hugo(inc, page, depth + 1) if depth < _DEPTH else inc}\n\n"
        if name == "skew":
            return skew(pos, page.param("version"), page.patch)
        if name == "param":
            value = page.param(pos[0]) if pos else ""
            return value
        if name in ("latest-version",):
            return page.param("version")
        if name == "latest-semver":
            return page.param("version").lstrip("v")
        if name == "release-branch":
            return f"release-{page.param('version').lstrip('v')}"
        if name == "version-check":
            least = page.meta.get("min-kubernetes-server-version", "")
            check = "To check the version, enter `kubectl version`."
            if least and least.lstrip("v") == page.param("version").lstrip("v"):
                return f"Your Kubernetes server must be version {least}. {check}"
            if least:
                return f"Your Kubernetes server must be at or later than version {least}. {check}"
            return check
        if name == "tab":
            label = named.get("name") or named.get("header", "")
            out = f"\n\n{label}:\n\n" if label else "\n\n"
            inc = named.get("include", "")
            if inc.endswith(".md"):
                # Вкладка, що вставляє сторінку з теки поруч (included/…md), — це текст.
                text_ = page.load("page_file", inc)
                if text_ is not None and depth < _DEPTH:
                    out += hugo(front(text_)[1], page, depth + 1)
            elif inc:
                out += page.code(inc, named.get("codelang", ""), "page_file")
            elif named.get("codelang") and not m.group(0).rstrip("}%> ").endswith("/"):
                tabs.append(True)
                return out + f"```{named['codelang']}\n"
            else:
                tabs.append(False)
            return out
        if name in ("table", "figure"):
            caption = named.get("caption") or named.get("alt") or named.get("title") or ""
            return f"\n\n{caption}\n\n" if caption else "\n\n"
        if name == "details":
            summary = named.get("summary") or named.get("title", "")
            return f"\n\n{summary}\n\n" if summary else "\n\n"
        if name == "api-reference":
            return (named.get("text") or named.get("anchor")
                    or named.get("page", "").rsplit("/", 1)[-1].split("-v")[0].capitalize())
        if name == "link":
            return named.get("text", "")
        if name in ("ref", "relref"):
            return pos[0] if pos else ""
        if name == "deprecationfilewarning":
            return "\n\nDeprecated:\n\n"
        if name == "tabs":
            return "\n\n"
        # Решта — оздоба сторінки без змісту (thirdparty-content, toc, кнопки, віджети
        # подій і стрічок): тег зникає, вкладений текст (якщо є) лишається.
        return ""

    # Один прохід: розгорнуте (приклад, врізка) далі не розбирається — у прикладах YAML
    # трапляються шаблони Go і Helm, і чіпати їх не можна.
    return _restore(store, _SC.sub(one, text))


# ── Liquid (Jekyll) ───────────────────────────────────────────────────────────

_LQ_TAG = re.compile(r"\{%-?\s*(\w+)(.*?)-?%\}", re.S)
_LQ_RAW = re.compile(r"\{%-?\s*raw\s*-?%\}(.*?)\{%-?\s*endraw\s*-?%\}", re.S)
_LQ_COMMENT = re.compile(r"\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}", re.S)
_LQ_HIGHLIGHT = re.compile(r"\{%-?\s*highlight\b.*?\{%-?\s*endhighlight\s*-?%\}", re.S)
_LQ_VAR = re.compile(r"\{\{-?\s*(page|site)\.([\w-]+)[^}]*\}\}")
_LQ_LIST = re.compile(r"['\"]([^'\"]*)['\"]\s*\|\s*split:\s*['\"]([^'\"]*)['\"]")
_IAL = re.compile(r"^\s*\{:[^}]*\}\s*$", re.M)
# Атрибути kramdown посеред рядка: «![pod](x.svg){: style="…"}», «{::nomarkdown}…{:/}».
_IAL_INLINE = re.compile(r"\{::?\s*[a-z/.#][^}]*\}|\{:/\}")
_TOC = re.compile(r"^\s*\*\s+TOC\s*$", re.M)
_TEMPLATES = ("templates/task.md", "templates/concept.md", "templates/tutorial.md",
              "templates/user-journey-content.md", "templates/kubectl.md",
              "templates/concept-overview.md")


def jekyll(text: str, page: Page, depth: int = 0) -> str:
    """Markdown сторінки Jekyll з розгорнутим Liquid: блоки capture — у порядку шаблону,
    приклади й врізки — текстом, вкладки — підписаними розділами."""
    store: list = []
    text = _LQ_RAW.sub(lambda m: _protect(store, m.group(1)), text)
    text = _LQ_COMMENT.sub("", text)
    text = _LQ_HIGHLIGHT.sub(lambda m: _protect(store, m.group(0)), text)
    variables: dict = {}
    captures: dict = {}
    used: set = set()
    stack: list = [("", [])]
    template = False
    pos = 0

    def emit(s: str) -> None:
        stack[-1][1].append(s)

    for m in _LQ_TAG.finditer(text):
        emit(text[pos:m.start()])
        pos = m.end()
        tag, raw = m.group(1), m.group(2).strip()
        if tag == "capture":
            stack.append((raw.split()[0] if raw else "", []))
        elif tag == "endcapture" and len(stack) > 1:
            name, parts = stack.pop()
            captures[name] = "".join(parts)
        elif tag == "assign":
            key, _, value = raw.partition("=")
            key, value = key.strip(), value.strip()
            listed = _LQ_LIST.search(value)
            if listed:
                variables[key] = [x.strip() for x in listed.group(1).split(listed.group(2))]
            elif "push:" in value:
                variables[key] = [x.strip() for x in re.findall(r"push:\s*([\w-]+)", value)]
            else:
                variables[key] = value.strip('"').strip("'")
        elif tag == "include":
            name = raw.split()[0] if raw else ""
            _, named = args_of(raw[len(name):])
            if name in _TEMPLATES:
                template = True
                emit("\x01TEMPLATE\x01")
            elif name == "code.html":
                emit(page.code(named.get("file", ""), named.get("language", ""), "page_file"))
            elif name in ("tabs.md", "tabs.html"):
                names = variables.get("tab_names") or []
                parts = variables.get("tab_contents") or []
                for label, key in zip(names, parts):
                    used.add(key)
                    emit(f"\n\n{label}:\n\n{captures.get(key, '')}\n\n")
            elif name.startswith("feature-state-"):
                state = name[len("feature-state-"):].rsplit(".", 1)[0]
                ver = variables.get("for_k8s_version") or page.version
                emit(f"\n\nFeature state: Kubernetes v{str(ver).lstrip('v')} [{state}]\n\n")
            elif name.endswith(".md") and depth < _DEPTH:
                inc = page.load("jekyll_include", name)
                if inc is not None:
                    emit(f"\n\n{jekyll(front(inc)[1], page, depth + 1)}\n\n")
        elif tag == "include_relative":
            name = raw.split()[0] if raw else ""
            inc = page.load("page_file", name) if name else None
            if inc is not None and depth < _DEPTH:
                emit(f"\n\n{jekyll(front(inc)[1], page, depth + 1)}\n\n")
        elif tag == "glossary_tooltip":
            _, named = args_of(raw)
            emit(named.get("text") or named.get("term_id", "").replace("-", " "))
        elif tag == "glossary_definition":
            _, named = args_of(raw)
            data = page.load("jekyll_data", f"glossary/{named.get('term_id', '')}.yaml")
            if data is None:
                data = page.load("jekyll_data", f"glossary/{named.get('term_id', '')}.yml")
            if data:
                meta = front(f"---\n{data.strip()}\n---\n")[0]
                text_ = meta.get("short-description", "")
                if named.get("length") == "all" and meta.get("long-description"):
                    text_ += "\n\n" + meta["long-description"]
                # Визначення в глосарії саме пишеться з Liquid (підказки до інших термінів).
                emit(jekyll(text_, page, depth + 1) if depth < _DEPTH else text_)
        # if/for/unless і решта — керування шаблоном: тег зникає, вміст лишається.
    emit(text[pos:])
    while len(stack) > 1:
        name, parts = stack.pop()
        captures[name] = "".join(parts)
    body = "".join(stack[0][1])

    def var(m) -> str:
        if m.group(1) == "page":
            key = m.group(2)
            if key in page.meta:
                return page.meta[key]
            if key in ("version", "fullversion", "githubbranch", "docsbranch"):
                return page.param(key)
        return ""

    if template:
        blocks = {k: v for k, v in captures.items() if k not in used}
        rest = body.replace("\x01TEMPLATE\x01", "")
        out = []
        for name in CAPTURE_ORDER:
            chunk = rest if name == "" else blocks.pop(name, "")
            if not chunk.strip():
                continue
            if name in CAPTURE_HEADINGS:
                out.append(f"\n\n## {CAPTURE_HEADINGS[name]}\n\n")
            out.append(chunk)
        # Блок, який шаблон не знає (вкладка без tabs.md, діалог feature state), — лишається
        # у кінці, щоб його текст не пропав.
        for name, chunk in blocks.items():
            if chunk.strip() and not name.startswith("dialog"):
                out.append(f"\n\n{chunk}")
        body = "".join(out)
    body = _LQ_VAR.sub(var, body)
    body = _IAL_INLINE.sub("", _IAL.sub("", _TOC.sub("", body)))
    return _restore(store, body)


# ── читач k8s-docs ────────────────────────────────────────────────────────────

_ANALYTICS = re.compile(r"^\[!\[Analytics\]\([^)]*\)\]\([^)]*\)\s*$", re.M)
_CONTENT_START = re.compile(r"<div[^>]+id=[\"']page-content-wrapper[\"']", re.I)


def _params(site: _Site, ref: _Ref) -> dict:
    """Поля конфігурації гілки, які показують шорткоди `param`: перше входження кожного
    (далі в файлі — перелік інших версій для меню, вони не про цю гілку)."""
    if ref.params is not None:
        return ref.params
    ref.params = {}
    for name in ("hugo.toml", "config.toml", "_config.yml"):
        if name not in ref.root_blobs:
            continue
        text = site.text(ref.ref, name) or ""
        for m in re.finditer(r"^\s*(version|fullversion|latest|githubbranch|docsbranch)"
                             r"\s*[:=]\s*[\"']?([^\"'\n]+)[\"']?\s*$", text, re.M):
            ref.params.setdefault(m.group(1), m.group(2).strip())
        break
    return ref.params


def _patch(site: _Site, ref: _Ref) -> str:
    """Останній патч лінії гілки — `{{< skew currentPatchVersion >}}`: з `fullversion`
    конфігурації, а де його немає (main) — з data/releases/schedule.yaml тієї ж гілки."""
    params = _params(site, ref)
    if params.get("fullversion"):
        return params["fullversion"].lstrip("v")
    if ref.patches is None:
        ref.patches = {}
        text = site.text(ref.ref, "data/releases/schedule.yaml")
        if text:
            for line, patch in _schedule_patches(text).items():
                ref.patches[line] = patch
    return ref.patches.get(ref.label, "")


def _schedule_patches(text: str) -> dict:
    """«1.37» → найсвіжіший патч зі schedule.yaml (перший у previousPatches)."""
    out: dict = {}
    for block in re.split(r"^- ", text, flags=re.M)[1:]:
        line = re.search(r"^\s*release:\s*[\"']?(\d+\.\d+)[\"']?\s*$", block, re.M)
        # Перший патч саме в previousPatches: поле `next` — ще не випущений.
        prev = block.split("previousPatches:", 1)[-1] if "previousPatches:" in block else ""
        patches = re.findall(r"^\s*-?\s*release:\s*[\"']?(\d+\.\d+\.\d+)[\"']?\s*$", prev,
                             re.M)
        if line and patches:
            out[line.group(1)] = patches[0]
    return out


def _loader(site: _Site, ref: _Ref, rel: str):
    """Доступ сторінки до файлів своєї гілки: раз на хеш, і лише крізь білий список."""
    page_dir = posixpath.dirname(rel)

    def load(kind: str, name: str):
        name = name.strip().lstrip("./") if kind != "page_file" else name.strip()
        if kind == "example":
            sha = ref.examples.get(name)
            return site.text(ref.ref, f"content/en/examples/{name}", sha) if sha else None
        if kind == "include":
            hit = next((n for n in sorted(ref.includes) if n == name or n.startswith(name)),
                       "")
            if not hit:
                return None
            return site.text(ref.ref, f"content/en/includes/{hit}", ref.includes[hit])
        if kind == "jekyll_include":
            sha = ref.includes.get(name)
            return site.text(ref.ref, f"_includes/{name}", sha) if sha else None
        if kind == "repo":
            # Файл від кореня репозиторію (readfile із «/»): його дерева в переліку немає.
            try:
                return site.text(ref.ref, name)
            except SystemExit:
                return None
        if kind == "jekyll_data":
            # Дерева _data у переліку немає (глосарій Jekyll — три десятки згадок на всі
            # гілки), тож файла може й не бути: 404 тут — «немає», а не збій сторінки.
            try:
                return site.text(ref.ref, f"_data/{name}") if name else None
            except SystemExit:
                return None
        path = posixpath.normpath(posixpath.join(page_dir, name)) if kind == "page_file" \
            else name
        hit = ref.docs.get(path)
        if not hit:
            return None
        return site.text(ref.ref, f"{ref.docs_root}/{path}", hit[0])

    return load


def _render(site: _Site, ref: _Ref, rel: str, sha: str, root_path: str) -> tuple[str, str]:
    text = site.page(ref.ref, root_path, sha)
    meta, rest, raw_front = front(text)
    era = ref.era
    page = None
    if era in ("hugo", "jekyll"):
        page = Page(meta, rel, ref.label, _loader(site, ref, rel), {}, "")
        # Конфігурація гілки — лише коли сторінка її справді показує: інакше на кожну гілку
        # був би зайвий файл.
        if re.search(r"\{\{[<%]\s*(param|skew)\b|\{\{-?\s*page\.(fullversion|githubbranch|"
                     r"docsbranch)", rest):
            page.params = _params(site, ref)
            if "currentPatchVersion" in rest:
                page.patch = _patch(site, ref)
        rest = hugo(rest, page) if era == "hugo" else jekyll(rest, page)
    elif era in ("plain", "static"):
        rest = _ANALYTICS.sub("", rest)
    if rel.endswith(".html"):
        start = _CONTENT_START.search(rest)
        body = _markup.html_body(rest[start.start():] if start else rest)
        title = meta.get("title", "")
        if not title:
            t = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
            title = unescape(t.group(1).strip()) if t else ""
    else:
        rest = _atx(rest)
        title = meta.get("title", "")
        if not title:
            title, rest = _split_title(rest)
        if "stages:" in raw_front:
            lines = gate_lines(raw_front, meta)
            rest = f"{lines}\n\n{rest}" if lines else rest
        lead = meta.get("description", "")
        if lead:
            rest = f"{lead}\n\n{rest}"
        body = _markup.markdown_body(rest)
    if not title:
        title = posixpath.splitext(rel.rsplit("/", 1)[-1])[0]
        if title in ("_index", "index"):
            title = posixpath.dirname(rel).rsplit("/", 1)[-1] or "Kubernetes Documentation"
    return unescape(title), body


@register("k8s-docs")
def k8s_docs(source: dict, ctx) -> list[Item]:
    refs = source.get("refs")
    if not isinstance(refs, dict) or not refs:
        raise SystemExit(f"{source['id']}: читач k8s-docs потребує поля refs — об'єкта "
                         f"«гілка, тег чи коміт → версія».")
    folders = [f.strip("/") for f in source.get("folders") or ()]
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    site = _Site(source, ctx)

    walked: list[_Ref] = []
    for n, (name, label) in enumerate(refs.items(), 1):
        ref = _Ref(name, str(label))
        _walk_ref(site, ref, folders)
        if ref.era:
            walked.append(ref)
        if n % _PROGRESS == 0:
            print(f"  {source['id']}: пройдено {n} із {len(refs)} гілок, різних тек "
                  f"{len(site.deep)}", flush=True)

    # (шлях від кореня, хеш) → [(гілка, шлях від теки документації)], у порядку гілок.
    groups: dict = {}
    for ref in walked:
        for rel, (sha, size) in ref.docs.items():
            path = f"{ref.docs_root}/{rel}" if ref.docs_root else rel
            if (not rel.endswith(_EXTS) or size == 0 or _ALWAYS_SKIP.search(path)
                    or any(r.search(path) for r in exclude)):
                continue
            groups.setdefault((path, sha), []).append((ref, rel))

    items = []
    names: set = set()
    for (path, sha), found in groups.items():
        rel = found[0][1]
        in_path = _PATH_VERSION.search(rel)
        # Один документ на вміст, коли від гілки нічого не залежить; інакше — по документу на
        # кожну гілку, з тим самим тілом сторінки з пам'яті.
        shared = (found[0][0].era in ("plain", "static") or rel.endswith(".html")
                  or bool(in_path))
        batches = [found] if shared else [[f] for f in found]
        for batch in batches:
            ref = batch[0][0]
            raw = site.raw(ref.ref, path)
            if not ctx.allowed(raw):
                continue
            if in_path:
                version = in_path.group(1)
            else:
                version = ", ".join(dict.fromkeys(r.label for r, _ in batch))
            key = f"{path}\0{sha}" + ("" if shared else f"\0{ref.ref}")
            name = f"{_markup.slug(_stem(rel))}-{hashlib.sha1(key.encode()).hexdigest()[:8]}"
            if name in names:
                continue
            names.add(name)
            blob = f"https://github.com/{site.owner}/{site.repo}/blob/{quote(ref.ref, safe='@')}/" \
                   f"{quote(path)}"

            def make(ref=ref, rel=rel, sha=sha, version=version, path=path, blob=blob,
                     raw=raw):
                title, body = _render(site, ref, rel, sha, path)
                # Файл на закріпленій гілці — не сторінка помилки, тож і коротке тіло
                # («сторінку перенесено»), і порожнє (рубрика меню) — теж історія.
                if body.strip():
                    _markup.require(title, body, raw, min_chars=1)
                return _markup.document(title, blob, ctx.stamp, body, version)

            items.append(Item(id=f"{source['id']}/{name}",
                              file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: на жодній із {len(refs)} гілок не знайдено "
                         f"дозволених сторінок.")
    return items


# ── журнали змін ──────────────────────────────────────────────────────────────

_CL_HEAD = re.compile(r"^# +v(\d+\.\d+\.\d+(?:-[\w.]+)?)[ \t]*$", re.M)
_CL_DOWNLOADS = re.compile(r"^## +Downloads for .*?(?=^## |\Z)", re.M | re.S)


@register("k8s-changelog")
def k8s_changelog(source: dict, ctx) -> list[Item]:
    files = source.get("files")
    if not isinstance(files, list) or not files:
        raise SystemExit(f"{source['id']}: читач k8s-changelog потребує поля files — "
                         f"імен файлів журналу (CHANGELOG-1.37.md).")
    base = source["url"].rstrip("/") + "/"
    cite_base = source.get("cite", base)
    items = []
    for fname in files:
        url = base + fname
        if not ctx.allowed(url):
            continue
        text = ctx.text(url).replace("\r\n", "\n")
        heads = list(_CL_HEAD.finditer(text))
        if not heads:
            raise SystemExit(f"{url}: жодного заголовка версії «# v1.N.N» — формат змінився, "
                             f"читача треба поправити.")
        cite = cite_base.rstrip("/") + "/" + fname
        for i, head in enumerate(heads):
            version = head.group(1)
            chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]

            def make(chunk=chunk, version=version, cite=cite, url=url):
                # Таблиці архівів з хешами SHA-512 — сотні рядків без жодного слова змісту.
                body = _markup.markdown_body(_CL_DOWNLOADS.sub("", chunk))
                heading = f"v{version}"
                _markup.require(heading, body, f"{url} {heading}", min_chars=1)
                anchor = re.sub(r"[^\w-]", "", heading.lower())
                return _markup.document(f"Kubernetes changelog: {heading}",
                                        f"{cite}#{anchor}", ctx.stamp, body, version)

            name = re.sub(r"[^\w.-]+", "-", version)
            items.append(Item(id=f"{source['id']}/{name}",
                              file=f"{source['id']}--{name}.txt", make=make))
    return items


# ── розклад релізів ───────────────────────────────────────────────────────────


def schedule_lines(schedule: str, eol: str) -> dict:
    """«1.36» → рядки документа: дата виходу, режим супроводу, кінець підтримки, патчі."""
    out: dict = {}
    for block in re.split(r"^- ", schedule.split("schedules:", 1)[-1], flags=re.M)[1:]:
        line = re.search(r"^\s*release:\s*[\"']?(\d+\.\d+)[\"']?\s*$", block, re.M)
        if not line:
            continue

        def field(name, text=block):
            m = re.search(rf"^\s*{name}:\s*[\"']?([^\"'\n]+)[\"']?\s*$", text, re.M)
            return m.group(1).strip() if m else ""

        rows = [f"Kubernetes {line.group(1)}"]
        for key, label in (("releaseDate", "Released"),
                           ("maintenanceModeStartDate", "Maintenance mode starts"),
                           ("endOfLifeDate", "End of life")):
            if field(key):
                rows.append(f"- {label}: {field(key)}")
        nxt = re.search(r"^\s*next:\s*\n((?:\s{4,}.*\n?)+)", block, re.M)
        if nxt:
            rows.append(f"- Next patch: {field('release', nxt.group(1))}, target date "
                        f"{field('targetDate', nxt.group(1))}, cherry-pick deadline "
                        f"{field('cherryPickDeadline', nxt.group(1))}")
        prev = block.split("previousPatches:", 1)
        if len(prev) == 2:
            rows.append("")
            rows.append("Patch releases:")
            rows.append("")
            for p in re.split(r"^\s*- ", prev[1], flags=re.M)[1:]:
                rel = field("release", p)
                if not re.fullmatch(r"\d+\.\d+\.\d+.*", rel):
                    continue
                note = field("note", p)
                rows.append(f"- {rel}: {field('targetDate', p)}"
                            + (f" ({note})" if note else ""))
        out[line.group(1)] = rows
    for block in re.split(r"^- ", eol.split("branches:", 1)[-1], flags=re.M)[1:]:
        line = re.search(r"^\s*release:\s*[\"']?(\d+\.\d+)[\"']?\s*$", block, re.M)
        if not line or line.group(1) in out:
            continue
        rows = [f"Kubernetes {line.group(1)} (end of life)"]
        for key, label in (("endOfLifeDate", "End of life"),
                           ("finalPatchRelease", "Final patch release"), ("note", "Note")):
            m = re.search(rf"^\s*{key}:\s*[\"']?([^\"'\n]+)[\"']?\s*$", block, re.M)
            if m:
                rows.append(f"- {label}: {m.group(1).strip()}")
        out[line.group(1)] = rows
    return out


@register("k8s-releases")
def k8s_releases(source: dict, ctx) -> list[Item]:
    eol_url = source.get("eol", "")
    cite = source.get("cite", "https://kubernetes.io/releases/")
    schedule = ctx.text(source["url"])
    eol = ctx.text(eol_url) if eol_url and ctx.allowed(eol_url) else ""
    lines = schedule_lines(schedule, eol)
    if not lines:
        raise SystemExit(f"{source['url']}: жодної лінії релізу — формат змінився, читача "
                         f"треба поправити.")
    items = []
    for minor, rows in lines.items():
        def make(minor=minor, rows=rows):
            body = "\n".join(rows[1:]).strip()
            return _markup.document(f"Kubernetes {minor} release dates and support", cite,
                                    ctx.stamp, body, minor)

        items.append(Item(id=f"{source['id']}/{minor}",
                          file=f"{source['id']}--release-{minor}.txt", make=make))
    return items
