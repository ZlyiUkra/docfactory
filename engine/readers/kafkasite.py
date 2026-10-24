"""Читач сайту kafka.apache.org: markdown Hugo з репозиторію apache/kafka-site.

`kafka-hugo` — сторінки однієї теки сайту на закріпленому коміті. `url` — дерево теки через API
              (…/repos/apache/kafka-site/git/trees/SHA:content/en/41?recursive=1): сайт тримає
              документацію кожної мінорної версії окремою текою (`07`, `0100`, `41`), тож одна
              тека — одне джерело з полем `version`, а редакції однієї сторінки зводить `families`.
              `site` — адреса сторінки на сайті, до якої дописується шлях файла без `.md`
              («https://kafka.apache.org/41/» + «design/design/»); `dated: true` — адреса блогу
              Hugo (`/:section/:year/:month/:day/:slug/`): дата й назва з шапки сторінки. `files` —
              вираз імен файлів, що беруться (типово всі `.md`).

Сторінка в репозиторії — не те, що бачить людина: таблиці конфігурації брокера, продюсера й
консумера та схеми протоколу на ній лише названо шорткодом
`{{< include-html file="/static/41/generated/consumer_config.html" >}}`, а сам HTML генерує збірка
Kafka. Без вставки сторінка «Consumer Configs» — один рядок «Below is the consumer configuration:».
Шорткод розгортається так, як його розгортає шаблон сайту (`layouts/shortcodes/include-html.html`):
`{version}` — тека сторінки; з 4.2 файли лежать у `content/en/<тека>/generated/`, раніше — у
`static/<тека>/generated/`. Вставлений HTML стає текстом тими самими правилами, що й сторінки HTML:
кожен параметр — свій заголовок «#### bootstrap.servers» з рядками Type, Default, Importance.
Невдала вставка випадає з поміткою, ціла сторінка через неї не губиться. У схемах протоколу 2.5
заголовок запиту зіпсовано ще на сайті — `<code><code></code>Request Header v0 …</code></pre>` без
`<pre>`: без лагодження цей блок коду не закривався, і вся сторінка протоколу ставала одним уривком
на 300 тисяч символів.

Не беруться заглушки старих адрес (`documentation/…` — лише `{{< doc-redirect >}}`) і порожні
сторінки розділів: `_index.md` до 1 500 байтів — це шапка й ліцензія без тексту (розділ `apis` 0.7
теж такий), а в `apis` пізніших версій `_index.md` — сама сторінка на кілька кілобайтів.
Решта шорткодів (вкладки, відео, каруселі) знімається; підпис вкладки лишається рядком.
"""

import re
from urllib.parse import unquote, urlsplit

from engine.readers import Item, _markup, github, register

_INCLUDE = re.compile(r"\{\{<\s*include-html\s+file=\"([^\"]+)\"\s*/?\s*>\}\}")
_TAB = re.compile(r"\{\{[<%]\s*tab\s+(?:header=)?\"([^\"]*)\"[^}]*[>%]\}\}")
_SHORTCODE = re.compile(r"\{\{[<%].*?[>%]\}\}", re.S)
_SKIP = re.compile(r"^documentation/")
_EMPTY_INDEX = 1500
_BULLET = re.compile(r"^-[ \t]*\n", re.M)
_BROKEN_PRE = "<code><code></code>"


def _urlize(title: str) -> str:
    """Hugo urlize: малі літери, пробіли — дефіси, без розділових знаків, крім «.», «_», «-»."""
    return re.sub(r"[^\w.\-]", "", "-".join(title.lower().split()))


def _shortcodes_out(text: str) -> str:
    text = _TAB.sub(lambda m: f"\n{m.group(1)}:\n", text)
    return _SHORTCODE.sub("", text)


@register("kafka-hugo")
def kafka_hugo(source: dict, ctx) -> list[Item]:
    m = github._TREE.match(urlsplit(source["url"]).path)
    if not m:
        raise SystemExit(f"{source['url']}: очікував адресу дерева теки "
                         f"/repos/ВЛАСНИК/РЕПО/git/trees/SHA:ТЕКА.")
    owner, repo, ref = m.groups()
    ref, _, sub = unquote(ref).partition(":")
    sub = sub.strip("/")
    if not sub:
        raise SystemExit(f"{source['url']}: потрібне дерево однієї теки — «SHA:content/en/41».")
    tree = github._json(ctx, source["url"])
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        raise SystemExit(f"{source['url']}: у відповіді немає дерева файлів.")
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")
    sizes = {e.get("path", ""): e.get("size", 0) for e in tree["tree"] if e.get("type") == "blob"}
    have = set(sizes)
    section = sub.rsplit("/", 1)[-1]
    only = re.compile(source["files"]) if source.get("files") else None
    raw_base = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/"

    def include(path: str) -> str:
        path = path.replace("{version}", section).lstrip("/")
        moved = path.replace(f"static/{section}/", f"content/en/{section}/", 1)
        if moved.startswith(sub + "/") and moved[len(sub) + 1:] in have:
            path = moved
        code, data = ctx.fetch(raw_base + path)
        if code != "200":
            return f"\n\n(Таблиця {path.rsplit('/', 1)[-1]} не вставилася: {code}.)\n\n"
        # Кожен параметр у згенерованому HTML — пункт списку з заголовком усередині: голий
        # маркер «-» перед «#### bootstrap.servers» нічого не каже.
        html = data.decode("utf-8", errors="replace").replace(_BROKEN_PRE, "<pre><code>")
        text = _BULLET.sub("", _markup.html_body(html))
        return "\n\n" + text + "\n\n"

    items = []
    for rel in sorted(have):
        leaf = rel.rsplit("/", 1)[-1]
        if (not rel.endswith(".md") or _SKIP.search(rel) or (only and not only.search(leaf))
                or (leaf == "_index.md" and sizes[rel] < _EMPTY_INDEX)):
            continue
        raw = raw_base + f"{sub}/{rel}"
        if not ctx.allowed(raw):
            continue
        stem = re.sub(r"(^|/)_index$", "", rel.removesuffix(".md"))
        name = _markup.slug(stem)

        def make(raw=raw, stem=stem):
            text = ctx.text(raw)
            _markup.refuse_html(text, raw)
            meta, rest = _markup.front_matter(text)
            title = _markup.title_of(meta, raw)
            parts, pos = [], 0
            for inc in _INCLUDE.finditer(rest):
                parts.append(_markup.markdown_body(_shortcodes_out(rest[pos:inc.start()])))
                parts.append(include(inc.group(1)))
                pos = inc.end()
            parts.append(_markup.markdown_body(_shortcodes_out(rest[pos:])))
            body = _markup.tidy("\n\n".join(parts), strip=False).strip()
            if not source.get("site"):
                url = f"https://github.com/{owner}/{repo}/blob/{ref}/{sub}/{stem}.md"
            elif source.get("dated") and meta.get("date"):
                y, mo, d = meta["date"][:10].split("-")
                url = f"{source['site']}{y}/{mo}/{d}/{_urlize(title)}/"
            else:
                url = f"{source['site']}{stem + '/' if stem else ''}"
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, url, ctx.stamp, body, source.get("version", ""))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['url']}: у теці {sub} немає жодного дозволеного .md.")
    return items
