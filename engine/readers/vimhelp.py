"""Читач довідки vim: `runtime/doc/*.txt` репозиторію vim/vim на кожній лінії.

`vim-help` — `url`    — префікс дерев GitHub (…/repos/vim/vim/git/trees/);
             `refs`   — «тег чи гілка → версія», від найновішого;
             `folder` — тека довідки («runtime/doc»); `exclude` — вирази шляхів;
             `label`  — префікс назви документа.

Навіщо. На іспиті LFCS редактор — vim або nano, і довідка vim (`:help`) — єдиний повний
опис команд, режимів і налаштувань. Розмітка своя: рядок `===` чи `---` відділяє розділ,
назва розділу стоїть поруч із тегами `*tag*`, рядок на `~` — підзаголовок, приклад
починається рядком на `>` і закінчується рядком на `<`. Без розбору приклади ставали б
текстом, а теги з зірочками заважали б пошукові по словах (`*:substitute*`).

Одиниця — неповторний файл: той самий файл кількох ліній — один документ з усіма цими
версіями.
"""

import re

from engine.readers import Item, _markup, register
from engine.readers.k8sdocs import _Site

_TAG = re.compile(r"\*([^*\s|]+)\*")
_LINK = re.compile(r"\|([^|\s]+)\|")
_OPT = re.compile(r"'([a-z]{2,})'")


def _strip_marks(line: str) -> str:
    return _LINK.sub(r"\1", _TAG.sub(r"\1", line))


def to_markdown(text: str) -> tuple[str, str]:
    """Файл довідки → (назва з першого рядка, markdown)."""
    lines = text.replace("\r\n", "\n").split("\n")
    first = lines[0] if lines else ""
    # «*usr_01.txt*	For Vim version 9.1.  Last change: …» або «*change.txt*  Vim version …»
    title = _TAG.sub("", first).strip()
    title = re.sub(r"\s*(For\s+)?Vim version.*$", "", title).strip()
    if not title:
        # Звичайно перший рядок — лише тег файла: «*change.txt*  For Vim version 9.1».
        tag = _TAG.search(first)
        title = tag.group(1) if tag else ""
    out: list[str] = []
    code: list[str] | None = None
    i = 1
    while i < len(lines):
        ln = lines[i]
        i += 1
        if code is not None:
            if ln.startswith("<") or (ln.strip() and not ln.startswith((" ", "\t"))):
                out.extend(["```", *[c.rstrip() for c in code], "```", ""])
                code = None
                if ln.startswith("<"):
                    ln = ln[1:]
                    if not ln.strip():
                        continue
            else:
                code.append(ln.replace("\t", "        "))
                continue
        if re.fullmatch(r"[=-]{20,}", ln.strip()):
            # Наступний непорожній рядок — назва розділу з тегами праворуч.
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines):
                head = lines[i]
                name = _TAG.sub("", head).strip()
                name = re.sub(r"\s{2,}.*$", "", name) if "\t" not in name else name.split("\t")[0]
                tags = " ".join(_TAG.findall(head))
                if name:
                    out.extend(["", f"## {name.strip()}", ""])
                    if tags:
                        out.extend([f"Tags: {tags}", ""])
                    i += 1
            continue
        if ln.rstrip().endswith(" ~") and ln.strip() != "~":
            out.extend(["", f"### {_strip_marks(ln.rstrip()[:-1]).strip()}", ""])
            continue
        if ln.rstrip().endswith(">") and (ln.rstrip() == ">" or ln.rstrip()[-2] in " \t"):
            body = ln.rstrip()[:-1].rstrip()
            if body:
                out.append(_strip_marks(body))
            code = []
            continue
        out.append(_strip_marks(ln.rstrip()))
    if code:
        out.extend(["```", *code, "```"])
    body = "\n".join(out)
    body = re.sub(r"\n[ \t]*vim:[^\n]*$", "", body.rstrip())   # модельний рядок у кінці
    return title, re.sub(r"\n{3,}", "\n\n", body).strip()


def _vkey(v: str) -> tuple:
    return tuple(int(n) for n in re.findall(r"\d+", v))


@register("vim-help")
def vim_help(source: dict, ctx) -> list[Item]:
    refs = source.get("refs") or {}
    folder = (source.get("folder") or "").strip("/")
    if not refs or not folder:
        raise SystemExit(f"{source['id']}: читач vim-help потребує полів refs і folder.")
    exclude = [re.compile(r) for r in source.get("exclude") or ()]
    label = source.get("label", "")
    site = _Site(source, ctx)
    groups: dict = {}
    for ref, version in refs.items():
        sha = site.subtree(site.entries(ref), folder)
        if not sha:
            continue
        for e in site.entries(sha):
            path = f"{folder}/{e.get('path')}"
            if (e.get("type") == "blob" and path.endswith(".txt")
                    and not any(r.search(path) for r in exclude)):
                groups.setdefault((path, e["sha"]), []).append((ref, str(version)))
    items = []
    for (path, sha), found in sorted(groups.items()):
        found = sorted(found, key=lambda rv: _vkey(rv[1]), reverse=True)
        ref = found[0][0]
        versions = ", ".join(dict.fromkeys(v for _, v in found))
        stem = path.rsplit("/", 1)[-1][:-4]
        doc = f"{_markup.slug(stem)}-{sha[:8]}"
        url = site.raw(ref, path)
        if not ctx.allowed(url):
            continue

        def make(ref=ref, path=path, sha=sha, url=url, versions=versions, stem=stem):
            title, body = to_markdown(site.text(ref, path, sha) or "")
            title = title or stem
            if label:
                title = f"{label}: {title}"
            _markup.require(title, body, url)
            return _markup.document(title, url, ctx.stamp, body, versions)

        items.append(Item(id=f"{source['id']}/{doc}", file=f"{source['id']}--{doc}.txt",
                          make=make))
    return items
