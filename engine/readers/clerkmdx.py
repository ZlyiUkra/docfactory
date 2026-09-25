"""Читач документації Clerk із репозиторію clerk/clerk-docs: гілки архівних ліній.

`clerk-mdx` — сторінки `.mdx` з теки `docs/` на гілці репозиторію (`core-2`,
              `core-1`), зі вставками, розгорнутими на місці. `url` — дерево гілки
              /repos/ВЛАСНИК/РЕПО/git/trees/ГІЛКА?recursive=1.

Навіщо. Сайт clerk.com віддає markdown-двійники лише поточної лінії (Core 3), а
архіви Core 2 і Core 1 його robots.txt закриває від автоматичного обходу. Та сама
документація лежить у публічному репозиторії, по гілці на лінію, тож архіви
беруться звідти, а не з сайту.

Чим відрізняється від `ghdocs-mdx`. Сторінка Core 2 не самодостатня: чимала частина
її тексту — вставки, яких у самому файлі немає.

1. `<Include src="_partials/…" />` — спільний фрагмент з `docs/_partials/`, а
   `<Include src="./_partials/…" />` — з теки поруч зі сторінкою. Без розгортання на
   місці кроків quickstart-а в корпус лягла б порожнеча.
2. `<Typedoc src="…" />` — таблиця параметрів, згенерована з коду SDK, лежить у
   `clerk-typedoc/`. Без неї довідник хуків лишався б без жодного параметра.
3. `<If sdk="nextjs">…</If>` — сайт показує вміст лише для обраного SDK. Корпус
   тримає одну сторінку на всі SDK, тож блок лишається, а замість тега стає рядок
   «SDK: nextjs», щоб уривок не видавав код Vue за спосіб для Next.js.

Вставка може вставляти вставку, тож розгортання йде до глибини _DEPTH, і кожен файл
завантажується раз на прогін. Вставку, якої в дереві гілки немає, не вигадуємо: на
її місці лишається порожньо, а в журнал іде попередження. Теки з підкресленням
(`_partials`, `_tooltips`) документами не стають: це шматки сторінок, а не сторінки.
"""

import hashlib
import json
import posixpath
import re
from urllib.parse import urlsplit

from engine.readers import Item, _markup, register

_TREE = re.compile(r"^/repos/([^/]+)/([^/]+)/git/trees/([^/]+)$")
_DEPTH = 5
_FENCE = re.compile(r"^\s*(```+|~~~+)")
_INCLUDE = re.compile(r"""^([ \t]*)<Include\s+src=["']([^"']+)["']\s*/>\s*$""")
_TYPEDOC = re.compile(r"""^([ \t]*)<Typedoc\s+src=["']([^"']+)["'][^<>]*/>\s*$""")
_IF = re.compile(r"^([ \t]*)<If\s+([^<>]*)>\s*$")
_IF_END = re.compile(r"^\s*</If>\s*$")
_INDENTED_HEADING = re.compile(r"^[ \t]+#{1,6}[ \t]+\S")
_SDK_ATTR = re.compile(r"""\b(sdk|notSdk)=(?:\{\[([^\]]*)\]\}|["']([^"']*)["'])""")


def _sdk_label(attrs: str) -> str:
    """Рядок-підпис замість відкривального `<If>`: для яких SDK цей блок."""
    m = _SDK_ATTR.search(attrs)
    if not m:
        return ""
    names = m.group(3) if m.group(3) is not None else m.group(2)
    names = ", ".join(n.strip().strip("\"'") for n in names.split(",") if n.strip())
    return f"SDK: {names}" if m.group(1) == "sdk" else f"SDK, except: {names}"


def _flush_headings(text: str) -> str:
    """Заголовки з відступом — до лівого краю, поза блоками коду.

    Усередині `<Steps>` і `<Tab>` заголовок пишеться з відступом, і для MDX це
    заголовок. Для markdown ні, тож без цього сторінка quickstart-а лягала б у корпус
    одним розділом без жодного підрозділу. Прохід один, по вже розгорнутому тексту:
    вставка всередині `<Steps>` отримує відступ уже після власного розгортання."""
    out, fence = [], ""
    for line in text.split("\n"):
        f = _FENCE.match(line)
        if fence:
            if _markup._closes(line, fence):
                fence = ""
        elif f:
            fence = f.group(1)
        elif _INDENTED_HEADING.match(line):
            line = line.lstrip()
        out.append(line)
    return "\n".join(out)


@register("clerk-mdx")
def clerk_mdx(source: dict, ctx) -> list[Item]:
    m = _TREE.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував адресу дерева гілки "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/ГІЛКА.")
    owner, repo, branch = m.groups()
    try:
        tree = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}) — перелік не складено.")
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        raise SystemExit(f"{source['url']}: у відповіді немає дерева файлів.")
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")
    blobs = {e.get("path", "") for e in tree["tree"] if e.get("type") == "blob"}
    raw_base = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/"
    cache: dict[str, str] = {}

    def fragment(path: str, where: str) -> str | None:
        """Текст вставки без шапки YAML, або None, якщо файла в гілці немає."""
        if path not in blobs:
            print(f"  {where}: вставки {path} у гілці {branch} немає — лишаю порожньо",
                  flush=True)
            return None
        if path not in cache:
            text = ctx.text(raw_base + path)
            _markup.refuse_html(text, raw_base + path)
            cache[path] = _markup.front_matter(text)[1]
        return cache[path]

    def expand(text: str, where: str, here: str, depth: int = 0) -> str:
        """`here` — файл, чий це текст: `./_partials/…` рахується від його теки."""
        out: list[str] = []
        fence = ""
        for line in text.replace("\r\n", "\n").split("\n"):
            f = _FENCE.match(line)
            if fence:
                out.append(line)
                if _markup._closes(line, fence):
                    fence = ""
                continue
            if f:
                fence = f.group(1)
                out.append(line)
                continue
            inc, doc = _INCLUDE.match(line), _TYPEDOC.match(line)
            if (inc or doc) and depth < _DEPTH:
                indent, src = (inc or doc).groups()
                src = src.removesuffix(".mdx")
                if src.startswith(("./", "../")):
                    path = posixpath.normpath(posixpath.join(posixpath.dirname(here), src))
                else:
                    path = ("docs/" if inc else "clerk-typedoc/") + src.strip("/")
                path += ".mdx"
                body = fragment(path, where)
                if body is not None:
                    body = expand(body, where, path, depth + 1)
                    out += ["", *[(indent + ln) if ln.strip() else "" for ln in
                                  body.split("\n")], ""]
                continue
            cond = _IF.match(line)
            if cond:
                label = _sdk_label(cond.group(2))
                out += ["", cond.group(1) + label, ""] if label else [""]
                continue
            if _IF_END.match(line):
                out.append("")
                continue
            out.append(line)
        return "\n".join(out)

    pages = sorted(p for p in blobs
                   if p.startswith("docs/") and p.endswith(".mdx")
                   and not any(part.startswith("_") for part in p.split("/")))
    items = []
    names: set[str] = set()
    for path in pages:
        raw = raw_base + path
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{branch}/{path}"
        stem = path[len("docs/"):].removesuffix(".mdx")
        stem = re.sub(r"(^|/)index$", "", stem) or "index"
        name = _markup.slug(stem)
        # «organization-membership-request.mdx» і «organization/membership-request.mdx»
        # лежать у core-1 поруч і дають те саме ім'я: без суфікса друга сторінка тихо
        # перезаписала б першу. Суфікс — від шляху, тож не зсувається з новими файлами.
        if name in names:
            name += "-" + hashlib.sha1(path.encode()).hexdigest()[:8]
        names.add(name)

        def make(raw=raw, blob=blob, path=path):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            meta, rest = _markup.front_matter(text)
            body = _markup.markdown_body(_flush_headings(expand(rest, path, path)))
            # Сторінка для окремих SDK каже про це лише в шапці YAML, яку корпус не
            # зберігає; без цього рядка довідник хука Expo не відрізнити від вебового.
            if meta.get("sdk"):
                body = f"SDK: {meta['sdk']}\n\n{body}"
            title = _markup.title_of(meta, blob) if meta else ""
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['url']}: у теці docs/ немає жодної дозволеної сторінки .mdx.")
    return items
