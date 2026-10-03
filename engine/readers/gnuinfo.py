"""Читач посібників GNU (bash, coreutils, grep, sed, findutils, tar): файл info з архіву випуску.

`gnu-info` — `url`      — тека випусків пакета на ftp.gnu.org (…/gnu/coreutils/);
             `package`  — ім'я архіву («coreutils» → coreutils-9.12.tar.xz);
             `info`     — ім'я посібника в теці doc/ архіву («coreutils», «bashref», «find»);
             `versions` — перелік випусків, від найновішого;
             `label`    — префікс назви документа («GNU coreutils»).

Навіщо. Повний посібник GNU — не man-сторінка: man coreutils лише відсилає до info, і
пояснення режимів chmod, опцій find чи розгортань bash є тільки там. На gnu.org лежить
лише поточна редакція, а випуски на ftp.gnu.org несуть готовий файл info кожної версії —
звичайний текст, поділений на вузли, без розбору texinfo.

Одиниця — посібник у випуску: перелік складається з однієї сторінки-каталогу, архів
тягнеться лише тоді, коли документ пишеться. Вузли стають розділами (`*` — `##`, `=` —
`###`, `-` — `####`, `.` — `#####` за підкресленням заголовка), меню вузлів і покажчики
відкидаються, перехресні посилання `*Note X::` стають «see X». Однакові вузли сусідніх
випусків зливаються в корпусі у фрагмент з усіма версіями.
"""

import gzip
import hashlib
import io
import lzma
import re
import tarfile

from engine.readers import Item, _markup, register

_UNDER = {"*": "##", "=": "###", "-": "####", ".": "#####"}
_NOTE = re.compile(r"\*[Nn]ote\s+([^:]+?)::|\*[Nn]ote\s+[^:]+?:\s*([^,.;)]+?)[.,;)]", re.S)


def info_to_markdown(info: str) -> str:
    """Текст info → markdown: вузол — розділ, меню й покажчики — геть."""
    nodes = info.split("\x1f")
    out = []
    for node in nodes:
        node = node.lstrip("\n")
        if not node.startswith("File:") or "Tag Table:" in node[:40]:
            continue
        head, _, body = node.partition("\n")
        name = re.search(r"Node:\s*([^,\n]+)", head)
        if name and re.search(r"\bIndex\b", name.group(1)):
            continue
        lines = body.split("\n")
        # Меню вузлів — від «* Menu:» до кінця вузла або порожнього рядка після пунктів.
        kept, in_menu = [], False
        for ln in lines:
            if ln.startswith("* Menu:"):
                in_menu = True
                continue
            if in_menu:
                if ln.startswith("* ") or not ln.strip() or ln.startswith((" ", "\t")):
                    continue
                in_menu = False
            kept.append(ln)
        text = []
        i = 0
        while i < len(kept):
            ln = kept[i]
            nxt = kept[i + 1] if i + 1 < len(kept) else ""
            if (ln.strip() and nxt and len(set(nxt.strip())) == 1 and nxt.strip()[0] in _UNDER
                    and len(nxt.strip()) >= max(3, len(ln.strip()) - 2)):
                text.extend(["", f"{_UNDER[nxt.strip()[0]]} {ln.strip()}", ""])
                i += 2
                continue
            text.append(ln)
            i += 1
        chunk = "\n".join(text)
        chunk = _NOTE.sub(lambda m: f"see {(m.group(1) or m.group(2) or '').strip()}", chunk)
        out.append(chunk.strip("\n"))
    body = "\n\n".join(_unwrap(c) for c in out if c.strip())
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def _unwrap(text: str) -> str:
    """Абзаци info розбиті на рядки по 72 знаки — склеюються в один рядок; блок, де
    кожен рядок відступлений щонайменше на п'ять пробілів (приклад команди, вивід),
    береться в огорожу коду, як є. Пункт списку («•», «*», «-») починає новий рядок."""
    out = []
    for block in re.split(r"\n\s*\n", text):
        lines = [ln for ln in block.split("\n") if ln.strip()]
        if not lines:
            continue
        if lines[0].startswith("#"):
            out.append("\n".join(lines))
            continue
        if all(len(ln) - len(ln.lstrip(" ")) >= 5 for ln in lines):
            pad = min(len(ln) - len(ln.lstrip(" ")) for ln in lines)
            out.append("```\n" + "\n".join(ln[pad:] for ln in lines) + "\n```")
            continue
        merged: list[str] = []
        for ln in lines:
            stripped = ln.strip()
            if not merged or re.match(r"(•|\*|-|\d+\.)\s", stripped):
                merged.append(stripped)
            else:
                merged[-1] += " " + stripped
        out.append("\n".join(" ".join(m.split()) for m in merged))
    return "\n\n".join(out)


def _unpack(data: bytes, url: str) -> tarfile.TarFile:
    raw = lzma.decompress(data) if url.endswith(".xz") else gzip.decompress(data)
    return tarfile.open(fileobj=io.BytesIO(raw))


def _info_text(tar: tarfile.TarFile, info: str) -> str:
    """Файл info посібника: цілий або частинами (x.info-1, x.info-2 …) за порядком."""
    parts = []
    for m in tar.getmembers():
        hit = re.search(rf"/{re.escape(info)}\.info(?:-(\d+))?$", m.name)
        if m.isfile() and hit:
            parts.append((int(hit.group(1) or 0), m))
    if not parts:
        return ""
    parts.sort(key=lambda p: p[0])
    if len(parts) > 1:
        parts = [p for p in parts if p[0] > 0]   # головний файл — лише перелік частин
    return "".join(tar.extractfile(m).read().decode("utf-8", errors="replace")
                   for _, m in parts)


@register("gnu-info")
def gnu_info(source: dict, ctx) -> list[Item]:
    package, info = source.get("package"), source.get("info")
    versions = source.get("versions")
    if not package or not info or not versions:
        raise SystemExit(f"{source['id']}: читач gnu-info потребує полів package, info і "
                         f"versions.")
    base = source["url"].rstrip("/") + "/"
    listing = ctx.text(base)
    have = set(re.findall(rf'href="({re.escape(package)}-[0-9][0-9.]*\.tar\.(?:xz|gz))"',
                          listing))
    label = source.get("label", "")
    items = []
    for v in versions:
        name = next((f"{package}-{v}.tar.{e}" for e in ("xz", "gz")
                     if f"{package}-{v}.tar.{e}" in have), None)
        if not name:
            raise SystemExit(f"{source['id']}: випуску {v} немає в {base}.")
        url = base + name
        if not ctx.allowed(url):
            continue
        # Хеш версії в кінці імені: revision_suffix зрізає його, і однакові вузли різних
        # випусків зливаються в один фрагмент з усіма версіями.
        doc = f"{_markup.slug(info)}-{hashlib.sha1(v.encode()).hexdigest()[:8]}"

        def make(url=url, v=v):
            with _unpack(ctx.bytes(url), url) as tar:
                text = _info_text(tar, info)
            if not text:
                raise SystemExit(f"{url}: в архіві немає doc/{info}.info — документ не "
                                 f"записую.")
            body = info_to_markdown(text)
            title = f"{label} {v} manual" if label else f"{info} {v}"
            _markup.require(title, body, url)
            return _markup.document(title, url, ctx.stamp, body, v)

        items.append(Item(id=f"{source['id']}/{doc}", file=f"{source['id']}--{doc}.txt",
                          make=make))
    return items
