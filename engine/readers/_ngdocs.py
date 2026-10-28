"""Розмітка документації Angular у репозиторії: aio (`aio/content`, 4.x–17.x) і adev (`adev/src/content`, 17.x+).

Навіщо. Посібники Angular у репозиторії — markdown, але код прикладів у них не записаний:
сторінка лише посилається на файл прикладу й область у ньому, а текст підставляє генератор
сайту. В aio це `<code-example path="router/src/app/app.module.ts" region="imports">` (шлях
відносно `aio/content/examples/`) чи `<code-pane>` усередині `<code-tabs>`, у перших версіях —
`{@example 'architecture/ts/src/app/…' region='…'}`; в adev — `<docs-code path="adev/src/content/
examples/…" visibleRegion="…"/>` (шлях від кореня репозиторію) і `<docs-code-multifile>`.
Читач, що просто зняв би теги, дав би главу без жодного рядка коду — таку, що виглядає повною.
Тут файл прикладу береться з того самого тегу, а область вирізається за позначками
`#docregion`/`#enddocregion`, як це робить генератор: рядки з позначками випадають, кілька
шматків однієї області з'єднуються рядком «. . .».

Решта розмітки — текстом: `<code-example>` з кодом усередині (екранованим `&lt;`) — блок коду;
`<docs-step title>` — підзаголовок кроку, `<docs-callout title>`, `<docs-card title>`,
`<header>` виноски — підписом, `<docs-tab label>` — рядком-підписом, `<docs-pill title>` —
пунктом списку, `<docs-decorative-header title>` — назвою сторінки, коли `#` її немає;
`{@link Router}` — назва, `{@a якір}` і `@reviewed` — службове, випадає. Таблиці HTML (хуки
життєвого циклу, шпаргалка) стають рядками «| … | … »: зняті теги склеювали б клітинки в одне слово.

Файл прикладу, якого на тезі немає (у 4.0–4.1 приклади жили в іншому репозиторії), лишає
рядок «Example: `шлях`» — сказати, що код тут був, чесніше, ніж мовчки його загубити.

Редакція сторінки — її вміст разом із вмістом файлів прикладів, які вона бере: сторінка
між мінорними версіями часто та сама, а приклад змінився, і без цього версія 15.2 показувала б
код 16.2.
"""

import hashlib
import posixpath
import re
from html import unescape
from textwrap import dedent

from engine.readers import _markup

_CODE_EXT = r"(?:ts|js|mjs|cjs|html|css|scss|sass|less|json|jsonc|sh|txt|yaml|yml|svg|xml|toml|md|xlf|conf)"

_ATTR = re.compile(r"""([\w-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'))?""")
# Пара тегів із кодом усередині чи самозакритий тег.
_CODE_EL = re.compile(r"<(code-example|code-pane|docs-code)\b((?:[^>\"']|\"[^\"]*\"|'[^']*')*?)"
                      r"(?:/>|>(.*?)</\1\s*>)", re.S)
_OLD_EXAMPLE = re.compile(r"\{@example\s+'([^']+)'([^}]*)\}")
_OLD_ATTR = re.compile(r"(\w+)\s*=\s*'([^']*)'")
_WRAPPERS = re.compile(r"</?(?:code-tabs|docs-code-multifile|docs-workflow|docs-pill-row|"
                       r"docs-tab-group|docs-card-container)\b[^>]*>")
_STEP = re.compile(r"<docs-step\b([^>]*)>")
_CALLOUT = re.compile(r"<docs-callout\b([^>]*)>")
_CARD = re.compile(r"<docs-card\b([^>]*?)(/?)>")
_TAB = re.compile(r"<docs-tab\b([^>]*)>")
_PILL = re.compile(r"<docs-pill\b([^>]*?)/?>")
_DECOR = re.compile(r"<docs-decorative-header\b([^>]*)>(.*?)</docs-decorative-header>", re.S)
_DECOR_EMPTY = re.compile(r"<docs-decorative-header\b([^>]*)/>")
_CLOSERS = re.compile(r"</(?:docs-step|docs-callout|docs-card|docs-tab|docs-pill)\s*>")
_HEADER = re.compile(r"<header>(.*?)</header>", re.S)
_LINK = re.compile(r"\{@link\s+([^\s}]+)(?:\s+([^}]*))?\}")
_ANCHOR = re.compile(r"\{@a\s+[\w.-]+\s*\}")
_REVIEWED = re.compile(r"^[ \t]*@reviewed\b.*$\n?", re.M)
_TABLE = re.compile(r"<table\b.*?</table>", re.S | re.I)
_FENCE = re.compile(r"^\s*(```|~~~)")
_H1 = re.compile(r"^#\s+\S", re.M)
_MARK = re.compile(r"#(docregion|enddocregion|docplaster)\b(.*)")
_MARK_NAMES = re.compile(r"[\w.-]+")
# Хвіст рядка-позначки: кінець коментаря після назв областей.
_MARK_TAIL = re.compile(r"\s*(?:-->|\*/|\}\}|%\}).*$")
_BLOCK = re.compile(r"\x00(\d+)\x00")
_AIO_TITLE = re.compile(r"\A\s*@title[ \t]*\n[ \t]*(\S.*)\n")
_AIO_TAGS = re.compile(r"^@(?:intro|description)[ \t]*$\n?", re.M)

_LANG = {"ts": "typescript", "js": "javascript", "mjs": "javascript", "html": "html",
         "css": "css", "scss": "scss", "json": "json", "sh": "shell", "yaml": "yaml",
         "yml": "yaml", "svg": "xml", "xml": "xml"}


def wanted(kind: str) -> list:
    """Файли тегу, які сторінки можуть узяти прикладом."""
    if kind == "aio":
        return [re.compile(rf"^aio/content/examples/.+\.{_CODE_EXT}$")]
    return [re.compile(rf"^(?:adev|packages/[\w-]+/resources)/.+\.{_CODE_EXT}$")]


def _attrs(raw: str) -> dict:
    return {m.group(1): (m.group(2) if m.group(2) is not None else m.group(3) or "")
            for m in _ATTR.finditer(raw or "")}


def _target(attrs: dict, kind: str) -> str:
    path = attrs.get("path", "").strip()
    if not path:
        return ""
    if kind == "aio":
        return posixpath.normpath(f"aio/content/examples/{path}")
    return posixpath.normpath(path.lstrip("/"))


def _refs(text: str, kind: str) -> list[str]:
    out = [_target(_attrs(m.group(2)), kind) for m in _CODE_EL.finditer(text)]
    if kind == "aio":
        out += [posixpath.normpath(f"aio/content/examples/{m.group(1)}")
                for m in _OLD_EXAMPLE.finditer(text)]
    return sorted({p for p in out if p})


def revision(path: str, sha: str, files: dict, fetch, kind: str) -> str:
    """Відбиток редакції сторінки разом із файлами прикладів, які вона бере."""
    text = fetch(path, files[path])
    near = [f"{p}:{files[p]}" for p in _refs(text, kind) if p in files]
    if not near:
        return sha
    return hashlib.sha1("\n".join([sha] + near).encode()).hexdigest()


def region(code: str, name: str) -> str:
    """Область файла прикладу за позначками `#docregion` — так, як її вирізає генератор сайту.
    Без назви — увесь файл без рядків-позначок; область, якої у файлі немає, — теж увесь файл:
    краще зайвий код, ніж жодного."""
    names = [n.strip() for n in name.split(",") if n.strip()] if name else []
    keep_all, parts, current, opened = not names, [], [], []
    for line in code.replace("\r\n", "\n").split("\n"):
        m = _MARK.search(line)
        if m:
            kind = m.group(1)
            tags = _MARK_NAMES.findall(_MARK_TAIL.sub("", m.group(2)))
            if kind == "docregion":
                opened.extend(tags or [""])
            elif kind == "enddocregion":
                if tags:
                    opened = [t for t in opened if t not in tags]
                elif opened:
                    opened.pop()
                if not keep_all and not any(t in names for t in opened) and current:
                    parts.append(current)
                    current = []
            continue
        if keep_all or any(t in names for t in opened):
            current.append(line)
    if current:
        parts.append(current)
    if keep_all:
        lines = parts[0] if parts else []
    elif not parts:
        return region(code, "")
    else:
        lines = []
        for i, chunk in enumerate(parts):
            if i:
                lines.append(". . .")
            lines.extend(chunk)
    return dedent("\n".join(lines)).strip("\n")


def _fence(code: str, lang: str, header: str) -> str:
    longest = max((len(m) for m in re.findall(r"`{3,}", code)), default=2)
    tick = "`" * max(3, longest + 1)
    head = f"{header}:\n\n" if header else ""
    return f"\n\n{head}{tick}{lang}\n{code}\n{tick}\n\n"


def _code(attrs: dict, inner: str | None, kind: str, files: dict, fetch) -> str:
    header = unescape(attrs.get("header") or attrs.get("title") or "").strip()
    lang = (attrs.get("language") or "").strip()
    target = _target(attrs, kind)
    if target:
        ext = target.rsplit(".", 1)[-1]
        lang = lang or _LANG.get(ext, ext)
        if target not in files:
            return f"\n\nExample: `{target}`" + (f" ({header})" if header else "") + "\n\n"
        name = attrs.get("visibleRegion") or attrs.get("region") or ""
        return _fence(region(fetch(target, files[target]), name), lang, header)
    code = dedent(unescape(inner or "").replace("\r\n", "\n")).strip("\n")
    if not code.strip():
        return ""
    return _fence(code, lang, header)


def _title(attrs: dict) -> str:
    return unescape(attrs.get("title", "")).strip()


def expand(text: str, path: str, files: dict, fetch, kind: str) -> str:
    """Сторінка з розміткою Angular → markdown для `_markup.markdown_body`."""
    if kind == "aio":
        # Перші версії aio (4.x) пишуть шапку тегами генератора: «@title» з назвою наступним
        # рядком, «@intro» з підзаголовком, «@description» перед текстом.
        text = _AIO_TITLE.sub(lambda m: f"# {m.group(1).strip()}\n", text, count=1)
        text = _AIO_TAGS.sub("", text)
    # Блоки markdown не чіпаємо: сторінки про саму розмітку («special elements») показують її
    # кодом, і вона мусить лишитися такою, як написана.
    out, chunk, fenced = [], [], False
    for line in text.replace("\r\n", "\n").split("\n"):
        if _FENCE.match(line):
            if not fenced:
                out.append(_expand_prose("\n".join(chunk), files, fetch, kind))
                chunk = []
            fenced = not fenced
            out.append(line)
            continue
        (out if fenced else chunk).append(line)
    out.append(_expand_prose("\n".join(chunk), files, fetch, kind))
    return "\n".join(out)


def _expand_prose(text: str, files: dict, fetch, kind: str) -> str:
    if not text:
        return text
    # Код ставиться на місце заглушок наприкінці: приклад HTML сам буває з `<table>` чи
    # `<header>`, і правила тексту нижче не повинні його торкатися.
    blocks: list[str] = []

    def keep(code: str) -> str:
        blocks.append(code)
        return f"\x00{len(blocks) - 1}\x00"

    text = _CODE_EL.sub(lambda m: keep(_code(_attrs(m.group(2)), m.group(3), kind, files, fetch)),
                        text)
    if kind == "aio":
        def old(m):
            attrs = dict(_OLD_ATTR.findall(m.group(2)))
            attrs["path"] = m.group(1)
            return keep(_code(attrs, None, kind, files, fetch))
        text = _OLD_EXAMPLE.sub(old, text)
    text = _WRAPPERS.sub("\n", text)
    text = _STEP.sub(lambda m: f"\n\n### {_title(_attrs(m.group(1)))}\n\n", text)
    text = _CALLOUT.sub(lambda m: (f"\n\n**{t}**\n\n" if (t := _title(_attrs(m.group(1))))
                                   else "\n\n"), text)
    text = _CARD.sub(lambda m: (f"\n\n**{t}**\n\n" if (t := _title(_attrs(m.group(1))))
                                else "\n\n"), text)
    text = _TAB.sub(lambda m: (f"\n\n{t}:\n\n" if (t := unescape(_attrs(m.group(1)).get(
        "label", "")).strip()) else "\n\n"), text)
    text = _PILL.sub(lambda m: (f"\n- {t}\n" if (t := _title(_attrs(m.group(1)))) else ""), text)

    def decor(m):
        t = _title(_attrs(m.group(1)))
        rest = m.group(2) if m.lastindex and m.lastindex >= 2 else ""
        head = f"# {t}\n\n" if t and not _H1.search(text) else ""
        return f"\n{head}{rest}\n"
    text = _DECOR.sub(decor, text)
    text = _DECOR_EMPTY.sub(decor, text)
    text = _CLOSERS.sub("\n", text)
    text = _HEADER.sub(lambda m: f"\n**{m.group(1).strip()}**\n", text)
    text = _LINK.sub(lambda m: (m.group(2) or m.group(1)).strip(), text)
    text = _ANCHOR.sub("", text)
    text = _REVIEWED.sub("", text)
    text = _TABLE.sub(lambda m: "\n\n" + _markup.html_body(m.group(0)).strip() + "\n\n", text)
    return _BLOCK.sub(lambda m: blocks[int(m.group(1))], text)
