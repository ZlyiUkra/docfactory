"""Читач довідника API, що лежить у пакеті npm сторінками HTML: один документ на неповторний текст сторінки класу.

`npm-tarball-classdocs` — `url` — опис пакета в реєстрі (https://registry.npmjs.org/ПАКЕТ), `versions` —
                          перелік версій, tarball яких читається, від найновішої; `match` — вираз шляху
                          сторінки в пакеті без кореневої теки («package/») з групою `name` — іменем класу
                          (`^dist/docs/classes/(?P<name>(?!index)[^/]+)\\.html$`); `cite` — шаблон адреси
                          сторінки для людей з `{version}`, `{name}` і `{lower}` (ім'я малими літерами).
                          Необов'язкові: `cite_latest` — шаблон адреси для сторінок, чий текст є в
                          найновішій версії переліку (сайт проєкту показує довідник лише її), `label` —
                          початок назви документа («Paper.js API»), `name_prefix` — рядок перед іменем
                          документа, `skip_inherited: true` — розділи успадкованих членів знімаються, а
                          наприкінці лишається розділ «Inherited members» з іменами предків.

Навіщо. Paper.js збирає довідник власним шаблоном JSDoc і кладе його в пакет: `dist/docs/classes/Path.html`.
Сайт paperjs.org показує довідник лише найновішої версії, а 69 % завантажень припадає на 0.12.18: її
довідник є тільки в її tarball. `npm-tarball-files` бере з пакета один файл, а сторінок тут півсотні на
версію; джерело на кожну сторінку тягнуло б той самий tarball півсотні разів.

Одиниця — пара «клас, текст сторінки» (хеш перетвореного тексту). Версії документа — усі з переліку, де
текст сторінки був саме таким, тож незмінна між 0.13 і 0.17 сторінка — один документ з п'ятьма версіями.

Що робиться зі сторінкою. Член класу (`<div class="member">`) стає заголовком четвертого рівня з
підписом, як на сторінці («Path.Circle(center, radius)»), під заголовками розділів («Properties»,
«Methods») і груп («Shaped Paths»). Підписи всередині члена («Type:», «Parameters:», «Returns:»,
«Example:») — рядки жирним, а не заголовки: фрагмент пошуку — цілий член. Приклад PaperScript
(`<script type="text/paperscript">`) стає блоком коду. Успадковані члени сторінка повторює дослівно: на
сторінці `Path` понад половину тексту — члени `Item` і `PathItem`, і без `skip_inherited` та сама
властивість займала б видачу під іменами двадцяти класів. Предок завжди має власну сторінку в тому ж
пакеті: розділ називає його посиланням на `../classes/Item.html`.
"""

import gzip
import hashlib
import html as html_lib
import io
import json
import re
import tarfile

from engine.readers import Item, _markup, register

_ARTICLE = re.compile(r"<article\b[^>]*>(.*)", re.S)
_COPYRIGHT = re.compile(r"<!-- =+ copyright notice =+ -->.*", re.S)
_INHERITED = re.compile(r"<!-- =+ inherited (?:properties|methods) =+ -->(.*?)(?=<!-- =+ |\Z)", re.S)
_PARENT = re.compile(r"inherited from\s*<a\b[^>]*>(.*?)</a>", re.S)
_H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S)
_SCRIPT = re.compile(r"<script type=\"text/paperscript\"[^>]*>\n?(.*?)</script>", re.S)
_RUN = re.compile(r"<div class=\"button run\">.*?</div>", re.S)
_EXAMPLE = re.compile(r"<h4>\s*(Example:?)\s*<span class=\"description\">(.*?)</span>\s*</h4>", re.S)
_H4 = re.compile(r"<h4\b[^>]*>(.*?)</h4>", re.S)
_MEMBER = re.compile(r"<div id=\"[^\"]*\" class=\"member\">\s*<div class=\"member-link\">\s*"
                     r"<a\b[^>]*>(.*?)</a>\s*</div>", re.S)
_TT = re.compile(r"<(/?)tt>")
_TAG = re.compile(r"<[^>]+>")


def _plain(fragment: str) -> str:
    return " ".join(html_lib.unescape(_TAG.sub("", fragment)).split())


def _tt_to_code(fragment: str) -> str:
    """`<tt>` → `<code>`, але лише зовнішній: шаблон вкладає їх («<tt>Array of <tt>Numbers</tt></tt>»),
    і два рівні дали б подвійні лапки коду посеред слова."""
    depth = 0

    def swap(m):
        nonlocal depth
        if m.group(1):
            depth = max(0, depth - 1)
            return "</code>" if depth == 0 else ""
        depth += 1
        return "<code>" if depth == 1 else ""

    return _TT.sub(swap, fragment)


def class_page(page: str, skip_inherited: bool) -> tuple[str, str]:
    """(назва класу зі сторінки, тіло markdown)."""
    m = _ARTICLE.search(page)
    body = _COPYRIGHT.sub("", m.group(1) if m else page)
    parents: list[str] = []
    if skip_inherited:
        for block in _INHERITED.findall(body):
            parent = _PARENT.search(block)
            if parent and _plain(parent.group(1)) not in parents:
                parents.append(_plain(parent.group(1)))
        body = _INHERITED.sub("", body)
    title = ""
    head = _H1.search(body)
    if head:
        title = _plain(head.group(1))
        body = body[:head.start()] + body[head.end():]
    body = _RUN.sub("", body)
    body = _SCRIPT.sub(lambda s: f"<pre class=\"language-js\">{html_lib.escape(s.group(1), quote=False)}</pre>",
                       body)
    body = _EXAMPLE.sub(lambda e: f"<p>**{_plain(e.group(1))}** {e.group(2)}</p>", body)
    body = _H4.sub(lambda h: f"<p>**{_plain(h.group(1))}**</p>", body)
    body = _MEMBER.sub(lambda mm: f"<h4>{html_lib.escape(_plain(mm.group(1)), quote=False)}</h4>", body)
    body = _tt_to_code(body)
    text = _markup.html_body(body)
    if parents:
        names = " and ".join(f"`{p}`" for p in parents)
        text = (f"{text}\n\n## Inherited members\n\nThe properties and methods this class inherits from "
                f"{names} are not repeated here: they are described on the page of {names}.")
    return title, text


def _pages(url: str, match, ctx) -> dict:
    """ім'я класу → HTML сторінки для всіх файлів tarball, що збіглися з виразом."""
    data = ctx.bytes(url)
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    found = {}
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        for member in tar:
            if not member.isfile():
                continue
            m = match.search(member.name.split("/", 1)[-1])
            if m:
                found[m.group("name")] = (tar.extractfile(member).read()
                                          .decode("utf-8", errors="replace").replace("\r\n", "\n"))
    return found


@register("npm-tarball-classdocs")
def npm_tarball_classdocs(source: dict, ctx) -> list[Item]:
    versions = [str(v) for v in source.get("versions") or ()]
    if not versions or not source.get("match") or not source.get("cite"):
        raise SystemExit(f"{source['id']}: читач npm-tarball-classdocs потребує полів versions, match "
                         f"(з групою name) і cite.")
    match = re.compile(source["match"])
    if "name" not in match.groupindex:
        raise SystemExit(f"{source['id']}: у виразі match немає групи name — імені класу.")
    try:
        packument = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}).")
    skip_inherited = source.get("skip_inherited") is True
    label = str(source.get("label") or "API")
    lead = f"{_markup.slug(source['name_prefix'])}-" if source.get("name_prefix") else ""

    # Остання прочитана пара (адреса, сторінки): документи однієї версії записуються підряд, тож
    # tarball розпаковується раз на версію, а в пам'яті лежить один.
    last: list = ["", {}]

    def pages(url: str) -> dict:
        if last[0] != url:
            last[0], last[1] = url, _pages(url, match, ctx)
        return last[1]

    seen: dict = {}      # (клас, хеш) → [адреса tarball найновішої версії, [версії]]
    for v in versions:
        url = ((packument.get("versions") or {}).get(v) or {}).get("dist", {}).get("tarball", "")
        if not url:
            raise SystemExit(f"{source['id']}: версії {v} у реєстрі немає.")
        if not ctx.allowed(url):
            raise SystemExit(f"{source['id']}: адреса {url} поза білим списком.")
        found = pages(url)
        if not found:
            raise SystemExit(f"{source['id']}: у пакеті версії {v} жодної сторінки за виразом "
                             f"{source['match']!r}.")
        for name, page in found.items():
            # Хеш — від перетвореного тексту, а не від HTML: сторінки сусідніх версій різняться
            # розміткою довкола (номери полотен прикладів, службові атрибути), а текст той самий.
            text = class_page(page, skip_inherited)[1]
            key = (name, hashlib.sha1(text.encode("utf-8")).hexdigest()[:8])
            seen.setdefault(key, [url, []])[1].append(v)
    last[0], last[1] = "", {}

    items = []
    for (name, digest), (url, found) in seen.items():
        doc = f"{lead}{_markup.slug(name)}-{digest}"

        def make(url=url, found=found, name=name):
            title, body = class_page(pages(url)[name], skip_inherited)
            template = (source.get("cite_latest") if found[0] == versions[0] else "") or source["cite"]
            cite = template.format(version=found[0], name=name, lower=name.lower())
            full = f"{label}: {title or name}"
            _markup.require(full, body, cite, min_chars=1)
            return _markup.document(full, cite, ctx.stamp, body, ", ".join(found))

        items.append(Item(id=f"{source['id']}/{doc}", file=f"{source['id']}--{doc}.txt", make=make))
    return items
