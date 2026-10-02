"""Читач документації інструментів навколо Kubernetes: сайт кожної версії з репозиторію.

`site-history` — markdown-сторінки сайту документації на кожній оголошеній гілці, тезі чи в кожній
                 теці версії. Поля:
                 `url`     — префікс дерев (…/repos/ВЛАСНИК/РЕПО/git/trees/);
                 `refs`    — об'єкт «гілка, тег чи коміт → версія», від найновішого; версія ""
                             — документація без версії (єдина «остання»);
                 `folders` — теки від кореня репозиторію зі сторінками; або об'єкт «тека →
                             версія», коли версії лежать теками на одній гілці (тоді в `refs`
                             одна гілка, а її мітка не важить);
                 `format`  — `hugo` (шорткоди Hugo/Docsy), `mkdocs` (mkdocs-material),
                             `docusaurus`, `markdown` (звичайний markdown GitHub) або `rst`
                             (reStructuredText; типове розширення тоді `.rst`);
                 `label`   — префікс назви документа («Traefik», «Helm»): версії різних
                             інструментів у корпусі — числа, і назва каже, чия це версія.
                 Необов'язкові: `files` — окремі файли від кореня (README.md), `extensions`
                 (типово `.md`; у docusaurus ще `.mdx`), `exclude` — вирази шляхів від кореня,
                 `assets` — теки, з яких сторінки вставляють файли (приклади YAML), `snippets`
                 — тека, від якої рахуються шляхи `--8<--` (mkdocs, типово `docs`),
                 `include_dir` — тека для `{% include 'x.yaml' %}` (mkdocs-macros), `skip_includes`
                 — вирази вставок, що не беруться (рекламний блок на кожній сторінці),
                 `variables` — файл змінних `[[VAR::ім'я]]` у теці версії (docusaurus).

Навіщо. Документацію Traefik, k3d, Gateway API, cert-manager, Helm, k3s, Kustomize, SOPS, age,
metrics-server і Let's Encrypt пишуть п'ятьма різними розмітками, і жодну з них спільний розбір
не розгортає. Без цього в корпус лягло б:

- mkdocs-material: виноска `!!! warning "Заголовок"` з тілом під відступом у чотири пробіли —
  для markdown це блок коду, і попередження ставало «кодом»; вкладки `=== "Docker"` і огорожі
  ```` ```yaml tab="File (YAML)" ```` губили підпис, до чого приклад; `--8<-- "шлях"` (вставка
  іншого файла — так складено половину довідника Traefik) лишалася рядком із шляхом, а
  `{% include 'standard/x.yaml' %}` у Gateway API спільний розбір мовчки викидав разом із
  прикладом;
- Docusaurus: виноска з назвою `:::info Version Gate` (у k3s таких 59) лишалася двокрапками в
  тексті, вкладки `<TabItem label="…">` губили підпис, `[[VAR::cert_manager_latest_version]]`
  лишався замість номера версії;
- Hugo/Docsy: шорткоди — так само, як на kubernetes.io (див. k8sdocs.py), плюс `readfile`
  (приклад YAML з теки examples/) і `def` (термін глосарію Let's Encrypt, назва якого — лише в
  атрибуті);
- ronn (сторінки man для age): `<INPUT>`, `<RECIPIENT>` спільний розбір приймав за теги HTML і
  стирав, і речення «encrypts or decrypts INPUT to OUTPUT» ставало «encrypts or decrypts  to»;
- reStructuredText (старий посібник SOPS, README.rst до 3.13.0): markdown-розбір не бачив у ньому
  ні заголовків (підкреслення «~~~~» лишалися рядками тексту, і посібник на 90 КБ ставав одним
  розділом), ні коду (`.. code:: yaml` і тіло під відступом розсипалися в абзаци), а посилання
  `` `текст <url>`_ `` лишалися з адресою й підкресленням.

Одиниця та сама, що в `k8s-docs`: сторінка у версії, текст файла — раз на хеш. Вставки й змінні
залежать від версії (приклад Gateway API v1beta1 став v1), тож той самий файл у двох версіях дає
два документи, кожен зі своєю версією, а однакові фрагменти зливаються вже в корпусі.
"""

import hashlib
import json
import posixpath
import re
from html import unescape
from urllib.parse import quote

from engine.readers import Item, _markup, register
from engine.readers.ghhistory import _atx, _split_title
from engine.readers.k8sdocs import Page, _Site, _blobs, front, hugo

_FORMATS = ("hugo", "mkdocs", "docusaurus", "markdown", "rst")
_DEPTH = 3

# ── mkdocs-material ───────────────────────────────────────────────────────────

_ADMONITION = re.compile(r"^(\s*)(!!!|\?\?\?\+?)\s*([\w-]+)?(?:\s+(?:\"([^\"]*)\"|(.+?)))?\s*$")
_CONTENT_TAB = re.compile(r"^(\s*)===\+?\s*\"([^\"]*)\"\s*$")
_FENCE = re.compile(r"^(\s*)(```+|~~~+)\s*([\w+#.-]*)(.*)$")
_TAB_ATTR = re.compile(r"\btab=\"([^\"]*)\"")
_SNIPPET = re.compile(r"^(\s*)--8<--\s+[\"']([^\"']+)[\"']\s*$")
_INCLUDE_MD = re.compile(r"\{%\s*include-markdown\s+[\"']([^\"']+)[\"'][^%]*%\}", re.S)
_INCLUDE_MACRO = re.compile(r"\{%-?\s*include\s+[\"']([^\"']+)[\"']\s*-?%\}")
_ATTR_LIST = re.compile(r"\{:[^}\n]*\}|\{\s*\.[\w-]+(?:\s+[.#][\w-]+)*\s*\}")
_ICON = re.compile(r":(?:material|fontawesome|octicons|simple)-[\w-]+:(?:\{[^}]*\})?")


def _dedent(lines: list[str], indent: int) -> list[str]:
    return [ln[indent:] if ln[:indent].strip() == "" else ln.lstrip() for ln in lines]


def mkdocs(text: str, page: Page, opts: dict, depth: int = 0) -> str:
    """Markdown mkdocs-material у звичайний: виноски й вкладки — підпис і тіло без відступу,
    підпис вкладки з огорожі коду — рядком перед кодом, вставки — текстом вставленого файла."""
    skip = [re.compile(r) for r in opts.get("skip_includes") or ()]
    base = (opts.get("snippets") or "docs").strip("/")

    def include_md(m):
        name = m.group(1)
        if any(r.search(name) for r in skip) or depth >= _DEPTH:
            return ""
        inc = page.load("page_file", name)
        if inc is None:
            return ""
        if not name.endswith(".md"):
            return page.code(name, "", "page_file")
        return "\n\n" + mkdocs(front(inc)[1], page, opts, depth + 1) + "\n\n"

    def include_macro(m):
        name = m.group(1)
        inc = page.load("repo", f"{opts.get('include_dir', '').strip('/')}/{name}".lstrip("/"))
        return inc.rstrip("\n") if inc is not None else ""

    text = _INCLUDE_MD.sub(include_md, text)
    lines = text.split("\n")
    out: list[str] = []
    fence = ""
    i = 0
    while i < len(lines):
        ln = lines[i]
        snip = _SNIPPET.match(ln)
        if snip:
            # Шлях вставки — від теки docs/ (base_path mkdocs), не від сторінки.
            name = snip.group(2)
            inc = page.load("repo", f"{base}/{name}") if depth < _DEPTH else None
            if inc is not None:
                body = inc if fence or not name.endswith(".md") else mkdocs(
                    front(inc)[1], page, opts, depth + 1)
                out.extend(snip.group(1) + x if x else x for x in body.rstrip("\n").split("\n"))
            i += 1
            continue
        if _INCLUDE_MACRO.search(ln):
            ln = _INCLUDE_MACRO.sub(include_macro, ln)
        f = _FENCE.match(ln)
        if fence:
            if f and f.group(2)[0] == fence[0] and len(f.group(2)) >= len(fence) \
                    and not (f.group(3) + f.group(4)).strip():
                fence = ""
            out.append(ln)
            i += 1
            continue
        if f:
            fence = f.group(2)
            tab = _TAB_ATTR.search(f.group(4))
            if tab:
                out.extend(["", f"{f.group(1)}{tab.group(1)}:", ""])
            out.append(f"{f.group(1)}{f.group(2)}{f.group(3)}")
            i += 1
            continue
        head = _ADMONITION.match(ln) or _CONTENT_TAB.match(ln)
        if head:
            indent = len(head.group(1))
            if head.re is _CONTENT_TAB:
                label = head.group(2)
            else:
                # Назва в лапках, назва без лапок («!!! note Referencing a resolver») або
                # сам тип виноски з великої літери.
                title = head.group(4) if head.group(4) is not None else head.group(5)
                label = title if title is not None else (head.group(3) or "note").capitalize()
            j = i + 1
            block: list[str] = []
            while j < len(lines) and (not lines[j].strip()
                                      or len(lines[j]) - len(lines[j].lstrip()) >= indent + 4):
                block.append(lines[j])
                j += 1
            while block and not block[-1].strip():
                block.pop()
                j -= 1
            inner = mkdocs("\n".join(_dedent(block, indent + 4)), page, opts, depth)
            out.append("")
            if label.strip():
                out.extend([f"{label.rstrip(':')}:", ""])
            out.extend(inner.split("\n"))
            out.append("")
            i = j
            continue
        out.append(_ICON.sub("", _ATTR_LIST.sub("", ln)))
        i += 1
    return "\n".join(out)


# ── Docusaurus ────────────────────────────────────────────────────────────────

_ASIDE = re.compile(r"^(\s*):{3,}\s*(\w+)"
                    r"(?:\[([^\]]*)\]|\{\s*title=\"([^\"]*)\"\s*\}|\s+(.+?))?\s*$")
_ASIDE_END = re.compile(r"^\s*:{3,}\s*$")
_TABITEM = re.compile(r"<TabItem\b([^>]*)>")
_TABS = re.compile(r"</?Tabs\b[^>]*>|</TabItem>")
_ATTR = re.compile(r"\b(label|value)=[\"']([^\"']*)[\"']")
_VAR = re.compile(r"\[\[VAR::([\w.-]+)\]\]")


def docusaurus(text: str, page: Page, variables: dict) -> str:
    """MDX Docusaurus у звичайний markdown: виноски з назвою чи без — підпис, вкладки —
    підпис вкладки, змінні теки версії — їхні значення. Код між огорожами не чіпається."""
    text = _markup.mdx_statements_out(text)
    out: list[str] = []
    fence = ""
    for ln in text.split("\n"):
        f = _FENCE.match(ln)
        if fence:
            if f and f.group(2)[0] == fence[0] and not (f.group(3) + f.group(4)).strip():
                fence = ""
            out.append(_VAR.sub(lambda m: str(variables.get(m.group(1), m.group(0))), ln))
            continue
        if f:
            fence = f.group(2)
            out.append(ln)
            continue
        ln = _VAR.sub(lambda m: str(variables.get(m.group(1), m.group(0))), ln)
        a = _ASIDE.match(ln)
        if a:
            label = a.group(3) or a.group(4) or a.group(5) or a.group(2).capitalize()
            out.extend(["", f"{label.rstrip(':')}:", ""])
            continue
        if _ASIDE_END.match(ln):
            out.append("")
            continue
        if "<TabItem" in ln or "Tabs" in ln:
            def tab(m):
                attrs = dict(_ATTR.findall(m.group(1)))
                name = attrs.get("label") or attrs.get("value") or ""
                return f"\n\n{name}:\n\n" if name else "\n\n"
            ln = _TABS.sub("\n\n", _TABITEM.sub(tab, ln))
        out.append(ln)
    return "\n".join(out)


# ── звичайний markdown ────────────────────────────────────────────────────────

_PLACEHOLDER = re.compile(r"(?<![`\w])<([A-Z][A-Z0-9_]*(?:[ .-][A-Z0-9_]+)*)>(?![`\w])")
_CODE_SPAN = re.compile(r"(`+).+?\1")


def plain(text: str) -> str:
    """Markdown GitHub і ronn: заповнювач `<INPUT>` поза кодом стає кодом — спільний розбір
    інакше прийняв би його за тег HTML і стер."""
    out, fence = [], False
    for ln in text.split("\n"):
        if re.match(r"^\s*(```|~~~)", ln):
            fence = not fence
        if not fence:
            parts, pos = [], 0
            for m in _CODE_SPAN.finditer(ln):
                parts.append(_PLACEHOLDER.sub(r"`<\1>`", ln[pos:m.start()]))
                parts.append(m.group(0))
                pos = m.end()
            parts.append(_PLACEHOLDER.sub(r"`<\1>`", ln[pos:]))
            ln = "".join(parts)
        out.append(ln)
    return "\n".join(out)


# ── reStructuredText ──────────────────────────────────────────────────────────

# Рядок підкреслення чи надкреслення заголовка: один і той самий знак пунктуації не менше
# трьох разів. Рівень заголовка в rst задає не знак, а порядок, у якому стилі вперше
# трапилися в документі, — тому рівні рахуються на кожен документ окремо.
_RST_ADORN = re.compile(r"^([=\-~^\"'`#*+_.:<>])\1{2,}\s*$")
_RST_DIRECTIVE = re.compile(r"^(\s*)\.\.\s+(?:\|[^|]+\|\s+)?([\w-]+)::(?:\s+(.*))?$")
_RST_TARGET = re.compile(r"^\s*\.\.\s+_(`[^`]+`|[^:]+):\s*(\S*)\s*$")
_RST_COMMENT = re.compile(r"^\s*\.\.(?:\s|$)")
_RST_OPTION = re.compile(r"^\s*:[\w-]+:")
_RST_ENUM = re.compile(r"^(\s*)(?:#\.|\(?\d+\))(\s+)")
_RST_TABLE = re.compile(r"^\s*\+[-=]+(?:\+[-=]+)*\+\s*$")
_RST_CODE_SPAN = re.compile(r"``(.+?)``")
_RST_LINK = re.compile(r"`([^`<]*?)\s*<([^<>`]+)>`__?")
_RST_LINK_WRAPPED = re.compile(r"(?<!`)`(?!`)[^`]*?\n[^`]*?<[^<>`\s]+>`__?")
# Адреса в кутових дужках поза посиланням — у rst просто адреса; дужки лише відділяють її
# від тексту.
_RST_BARE_URL = re.compile(r"<(https?://[^<>\s`]+)>")
_RST_ROLE = re.compile(r":[\w.+-]+(?::[\w.+-]+)?:`([^`]+)`")
_RST_REF = re.compile(r"`([^`<]+)`__?(?!\w)")
_RST_CODE = ("code", "code-block", "sourcecode")
_RST_ADMONITIONS = ("note", "warning", "tip", "important", "caution", "attention", "danger",
                    "hint", "error", "seealso", "admonition")
# Картинки, зміст, нумерація розділів, сирий HTML: тексту в них немає, а лишені як є вони
# давали б у корпусі «.. image:: https://…» рядком посеред розділу.
_RST_DROP = ("image", "figure", "contents", "sectnum", "raw", "include", "meta", "class",
             "highlight", "role", "default-role", "only", "replace", "unicode")


def _indent(ln: str) -> int:
    return len(ln) - len(ln.lstrip())


def _rst_block(lines: list[str], i: int, indent: int) -> tuple[list[str], int]:
    """Тіло блоку з рядка `i`: порожні рядки й рядки з відступом, більшим за `indent`.
    Порожні рядки в кінці — не тіло, а відступ до наступного абзацу."""
    j = i
    while j < len(lines) and (not lines[j].strip() or _indent(lines[j]) > indent):
        j += 1
    while j > i and not lines[j - 1].strip():
        j -= 1
    return lines[i:j], j


def _rst_dedent(block: list[str]) -> list[str]:
    width = min((_indent(ln) for ln in block if ln.strip()), default=0)
    lines = [ln[width:] for ln in block]
    while lines and not lines[0].strip():
        lines.pop(0)
    return lines


def _rst_inline(line: str, targets: dict) -> str:
    """Вбудована розмітка rst → markdown: ``код`` → `код`, `текст <url>`_ → [текст](url),
    :роль:`x` → `x`, `назва`_ — посилання за ціллю `.. _назва: url` або просто назва
    (посилання на розділ того самого файла). Код не чіпається."""
    def text(part: str) -> str:
        part = _RST_LINK.sub(lambda m: (f"[{m.group(1)}]({m.group(2)})" if m.group(1)
                                        and not m.group(2).startswith("#")
                                        else m.group(1) or m.group(2)), part)
        part = _RST_ROLE.sub(r"`\1`", part)
        part = _RST_BARE_URL.sub(r"\1", part)

        def ref(m):
            url = targets.get(m.group(1).strip().lower())
            return f"[{m.group(1)}]({url})" if url else m.group(1)
        return _RST_REF.sub(ref, part)

    parts, pos = [], 0
    for m in _RST_CODE_SPAN.finditer(line):
        parts.append(text(line[pos:m.start()]))
        code = m.group(1)
        parts.append(f"`` {code} ``" if "`" in code else f"`{code}`")
        pos = m.end()
    parts.append(text(line[pos:]))
    return "".join(parts)


def _padded(pad: str, lines: list[str]) -> list[str]:
    return [pad + x if x else x for x in lines]


def rst(text: str, targets: dict | None = None, styles: list | None = None) -> str:
    """reStructuredText у markdown: заголовки з підкресленням (і надкресленням) — «#» за
    порядком появи стилю, `.. code:: мова` і абзац на «::» — код між огорожами, виноски
    `.. note::` — підпис і тіло без відступу, картинки й зміст — геть, вбудована розмітка —
    як у markdown, таблиця-сітка — текстом між огорожами, щоб рядки не злиплися в абзац.

    Розбір свідомо неповний: лише те, що трапляється в посібниках інструментів (README.rst
    SOPS). Чого розбір не знає, лишається текстом, а не зникає."""
    text = text.replace("\r\n", "\n").expandtabs(8)
    # Посилання `текст <url>`_ часто перенесене на інший рядок, а розбір іде рядками —
    # розірване, воно лишалося б у тексті з `_ і голою адресою. Порожній рядок посередині —
    # уже не посилання, а два абзаци.
    text = _RST_LINK_WRAPPED.sub(lambda m: m.group(0) if "\n\n" in m.group(0)
                                 else re.sub(r"\s*\n\s*", " ", m.group(0)), text)
    lines = text.split("\n")
    if targets is None:
        # Ціль посилання `.. _назва: url` може стояти після першого вжитку — збирається
        # наперед.
        targets = {}
        for ln in lines:
            t = _RST_TARGET.match(ln)
            if t and t.group(2):
                targets[t.group(1).strip("`").strip().lower()] = t.group(2)
    styles = [] if styles is None else styles
    out: list[str] = []

    def heading(title: str, style: tuple) -> None:
        if style not in styles:
            styles.append(style)
        level = min(styles.index(style) + 1, 6)
        out.extend(["", "#" * level + " " + _rst_inline(title.strip(), targets), ""])

    def blank_before() -> bool:
        return not out or not out[-1].strip()

    i = 0
    while i < len(lines):
        ln = lines[i]
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        after = lines[i + 2] if i + 2 < len(lines) else ""
        if not ln.strip():
            out.append("")
            i += 1
            continue
        a = _RST_ADORN.match(ln)
        if a and blank_before():
            # Надкреслення, назва, підкреслення тим самим знаком.
            if nxt.strip() and _RST_ADORN.match(after) and after.strip()[0] == a.group(1):
                heading(nxt, (a.group(1), True))
                i += 3
                continue
            if not nxt.strip():
                i += 1  # перехід (риска між абзацами) — тексту не несе
                continue
        if _RST_TABLE.match(ln) and blank_before():
            j = i
            while j < len(lines) and lines[j].strip():
                j += 1
            out.extend(["```", *lines[i:j], "```"])
            i = j
            continue
        u = _RST_ADORN.match(nxt)
        if u and not a and _indent(ln) == 0 and blank_before() \
                and len(nxt.strip()) >= min(len(ln.strip()), 3):
            heading(ln, (u.group(1), False))
            i += 2
            continue
        d = _RST_DIRECTIVE.match(ln)
        if d:
            indent, name, arg = len(d.group(1)), d.group(2).lower(), (d.group(3) or "").strip()
            block, j = _rst_block(lines, i + 1, indent)
            # Параметри директиви (`:target:`, `:width:`) — одразу під нею, до тіла.
            while block and _RST_OPTION.match(block[0]):
                block = block[1:]
            body = _rst_dedent(block)
            pad = " " * indent
            if name in _RST_CODE:
                lang = arg.split()[0] if arg else ""
                out.extend([f"{pad}```{lang}", *_padded(pad, body), f"{pad}```"])
            elif name in _RST_ADMONITIONS:
                label = arg if name == "admonition" else name.capitalize()
                if name != "admonition" and arg:
                    body = [arg, ""] + body
                inner = rst("\n".join(body), targets, styles).strip("\n")
                out.extend(["", f"{pad}{label.rstrip(':')}:", ""])
                out.extend(_padded(pad, inner.split("\n")))
                out.append("")
            elif name not in _RST_DROP:
                inner = rst("\n".join(([arg, ""] if arg else []) + body), targets, styles)
                out.extend(_padded(pad, inner.split("\n")))
            i = j
            continue
        if _RST_TARGET.match(ln) or _RST_COMMENT.match(ln):
            # Ціль посилання вже зібрано; решта «..» — коментар із тілом під відступом.
            _, i = _rst_block(lines, i + 1, _indent(ln))
            continue
        if ln.rstrip().endswith("::"):
            # Абзац на «::» — далі буквальний блок. «Текст::» лишає одну двокрапку,
            # «Текст ::» і самотнє «::» — жодної.
            line = ln.rstrip()[:-2]
            line = line.rstrip() if not line.strip() or line.endswith(" ") else line + ":"
            if line.strip():
                out.append(_rst_inline(line, targets))
            k = i + 1
            while k < len(lines) and not lines[k].strip():
                k += 1
            if k < len(lines) and _indent(lines[k]) > _indent(ln):
                block, j = _rst_block(lines, k, _indent(ln))
                pad = " " * _indent(ln)
                out.extend(["", f"{pad}```", *_padded(pad, _rst_dedent(block)), f"{pad}```"])
                i = j
            else:
                i += 1
            continue
        e = _RST_ENUM.match(ln)
        if e:
            ln = f"{e.group(1)}1.{e.group(2)}{ln[e.end():]}"
        out.append(_rst_inline(ln, targets))
        i += 1
    return "\n".join(out)


# ── читач ─────────────────────────────────────────────────────────────────────


class _Unit:
    """Одна версія: гілка (тег) і теки з мітками; файли — шлях від кореня → (хеш, розмір)."""

    def __init__(self, ref: str, label: str, folder: str):
        self.ref, self.label, self.folder = ref, label, folder
        self.files: dict = {}


def _loader(site: _Site, unit: _Unit, path: str):
    page_dir = posixpath.dirname(path)

    def load(kind: str, name: str):
        if kind == "page_file":
            target = posixpath.normpath(posixpath.join(page_dir, name.strip()))
        else:
            target = posixpath.normpath(name.strip().lstrip("/"))
        if target.startswith("../"):
            return None
        hit = unit.files.get(target)
        if hit:
            return site.text(unit.ref, target, hit[0])
        # Файла немає в оголошених теках — ще одна спроба напряму (той самий репозиторій і
        # гілка, крізь білий список); 404 — «немає», а не збій сторінки.
        try:
            return site.text(unit.ref, target)
        except SystemExit:
            return None

    return load


@register("site-history")
def site_history(source: dict, ctx) -> list[Item]:
    refs = source.get("refs")
    if not isinstance(refs, dict) or not refs:
        raise SystemExit(f"{source['id']}: читач site-history потребує поля refs — об'єкта "
                         f"«гілка, тег чи коміт → версія».")
    fmt = source.get("format", "")
    if fmt not in _FORMATS:
        raise SystemExit(f"{source['id']}: поле format — одне з {', '.join(_FORMATS)}.")
    folders = source.get("folders") or []
    by_folder = isinstance(folders, dict)
    if by_folder and len(refs) != 1:
        raise SystemExit(f"{source['id']}: теки з версіями (folders-об'єкт) — лише на одній "
                         f"гілці.")
    files = [f.strip("/") for f in source.get("files") or ()]
    assets = [a.strip("/") for a in source.get("assets") or ()]
    exts = tuple(source.get("extensions") or {"docusaurus": (".md", ".mdx"),
                                              "rst": (".rst",)}.get(fmt, (".md",)))
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    label = source.get("label", "")
    site = _Site(source, ctx)

    units: list[_Unit] = []
    for ref, ref_label in refs.items():
        root = site.entries(ref)
        shared: dict = {}
        for folder in assets:
            sha = site.subtree(root, folder)
            if sha:
                shared.update(_blobs(site.entries(sha, recursive=True), folder + "/"))
        for f in files:
            parent = posixpath.dirname(f)
            entries = root if not parent else (
                site.entries(site.subtree(root, parent)) if site.subtree(root, parent) else [])
            leaf = posixpath.basename(f)
            hit = next((e for e in entries if e.get("path") == leaf
                        and e.get("type") == "blob"), None)
            if hit:
                shared[f] = (hit["sha"], hit.get("size", 0))
        pairs = folders.items() if by_folder else [(f, str(ref_label)) for f in folders]
        if not pairs:
            pairs = [("", str(ref_label))]
        for folder, folder_label in pairs:
            unit = _Unit(ref, str(folder_label), folder.strip("/"))
            unit.files.update(shared)
            sha = site.subtree(root, unit.folder) if unit.folder else ""
            if sha:
                unit.files.update(_blobs(site.entries(sha, recursive=True), unit.folder + "/"))
            if sha or files:
                units.append(unit)

    # Документи однієї пари «шлях, вміст» — підряд: текст сторінки береться з пам'яті.
    groups: dict = {}
    seen_paths: set = set()
    for unit in units:
        for path, (sha, size) in unit.files.items():
            inside = (unit.folder and path.startswith(unit.folder + "/")) or path in files
            if (not inside or not path.endswith(exts) or size == 0
                    or any(r.search(path) for r in exclude)):
                continue
            # Файл із `files` у кількох теках однієї гілки — один документ на гілку.
            if path in files and (unit.ref, path) in seen_paths:
                continue
            seen_paths.add((unit.ref, path))
            groups.setdefault((path, sha), []).append(unit)

    items = []
    names: set = set()
    for (path, sha), found in groups.items():
        for unit in found:
            rel = path[len(unit.folder) + 1:] if unit.folder and path.startswith(
                unit.folder + "/") else path
            raw = site.raw(unit.ref, path)
            if not ctx.allowed(raw):
                continue
            stem = re.sub(r"\.(mdx?|ronn|rst)$", "", rel)
            stem = re.sub(r"(^|/)_?index$", "", stem) or "index"
            key = f"{path}\0{sha}\0{unit.ref}\0{unit.folder}"
            name = f"{_markup.slug(stem)}-{hashlib.sha1(key.encode()).hexdigest()[:8]}"
            if name in names:
                continue
            names.add(name)
            blob = (f"https://github.com/{site.owner}/{site.repo}/blob/"
                    f"{quote(unit.ref, safe='@')}/{quote(path)}")

            def make(unit=unit, path=path, sha=sha, blob=blob, raw=raw, rel=rel):
                text = site.page(unit.ref, path, sha)
                meta, rest, _ = front(text)
                page = Page(meta, path, unit.label or "0.0", _loader(site, unit, path))
                if fmt == "hugo":
                    rest = hugo(rest, page)
                elif fmt == "mkdocs":
                    rest = mkdocs(rest, page, source)
                elif fmt == "docusaurus":
                    variables = {}
                    if source.get("variables") and unit.folder:
                        vtext = page.load("repo", f"{unit.folder}/{source['variables']}")
                        try:
                            variables = json.loads(vtext) if vtext else {}
                        except ValueError:
                            variables = {}
                    rest = docusaurus(rest, page, variables)
                elif fmt == "rst":
                    rest = plain(rst(rest))
                else:
                    rest = plain(rest)
                rest = _atx(rest)
                title = meta.get("title") or meta.get("linkTitle") or ""
                if not title:
                    title, rest = _split_title(rest)
                if not title:
                    title = posixpath.splitext(posixpath.basename(rel))[0]
                    if title in ("_index", "index", "README"):
                        title = posixpath.dirname(rel).rsplit("/", 1)[-1] or title
                lead = meta.get("description", "")
                if lead:
                    rest = f"{lead}\n\n{rest}"
                body = _markup.markdown_body(rest)
                title = unescape(title)
                if label:
                    title = f"{label}: {title}"
                if body.strip():
                    _markup.require(title, body, raw, min_chars=1)
                return _markup.document(title, blob, ctx.stamp, body, unit.label)

            items.append(Item(id=f"{source['id']}/{name}",
                              file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: на жодній із {len(refs)} гілок не знайдено "
                         f"дозволених сторінок.")
    return items
