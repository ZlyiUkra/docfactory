"""Читач теки файлів, де кожен файл — окрема версія: версія береться з імені файла.

`ghdocs-filever` — файли однієї теки репозиторію на закріпленому коміті. `url` — дерево теки через API
                   (…/repos/ВЛАСНИК/РЕПО/git/trees/SHA:ТЕКА, риски теки закодовано `%2F`), `version_from` —
                   вираз над іменем файла з однією групою — версією («^(\\d+\\.\\d+\\.\\d+)\\.md$»): файл,
                   ім'я якого не збіглося, не береться. Необов'язкові: `skip` — вираз версій, що не беруться
                   (ще не випущені), `name_prefix` — рядок перед іменем документа, `title_prefix` — назва
                   документа без заголовка у файлі («RabbitMQ release notes » + версія). Файл `.md`
                   розбирається як markdown, будь-який інший — як простий текст.

Навіщо. Нотатки релізів RabbitMQ лежать у `release-notes/` репозиторію rabbitmq-server по файлу на версію
(`4.3.7.md`, а давні — `README-3.4.0.txt`), і версія є лише в імені файла. `ghdocs` дає один `version` на все
джерело, а по джерелу на кожну з двохсот версій — двісті звернень по те саме дерево.
"""

import re
from urllib.parse import unquote, urlsplit

from engine.readers import Item, _markup, github, register

_H1 = re.compile(r"^#\s+(.+?)\s*#*\s*$", re.M)


@register("ghdocs-filever")
def ghdocs_filever(source: dict, ctx) -> list[Item]:
    m = github._TREE.match(urlsplit(source["url"]).path)
    if not m or not source.get("version_from"):
        raise SystemExit(f"{source['url']}: потрібні адреса дерева теки …/git/trees/SHA:ТЕКА і поле "
                         f"version_from.")
    owner, repo, ref = m.groups()
    ref, _, sub = unquote(ref).partition(":")
    sub = sub.strip("/")
    tree = github._json(ctx, source["url"])
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        raise SystemExit(f"{source['url']}: у відповіді немає дерева файлів.")
    if tree.get("truncated"):
        raise SystemExit(f"{source['url']}: GitHub обрізав дерево — перелік був би неповним.")
    version_rx = re.compile(source["version_from"])
    skip = re.compile(source["skip"]) if source.get("skip") else None
    prefix = source.get("name_prefix", "")
    items = []
    for entry in tree["tree"]:
        path = entry.get("path", "")
        hit = version_rx.search(path) if entry.get("type") == "blob" and "/" not in path else None
        if not hit or (skip and skip.search(hit.group(1))):
            continue
        version = hit.group(1)
        full = f"{sub}/{path}" if sub else path
        raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{full}"
        if not ctx.allowed(raw):
            continue
        blob = f"https://github.com/{owner}/{repo}/blob/{ref}/{full}"
        name = _markup.slug(f"{prefix}-{version}" if prefix else version)

        def make(raw=raw, blob=blob, version=version, markdown=path.endswith(".md")):
            text = ctx.text(raw).replace("\r\n", "\n")
            _markup.refuse_html(text, raw)
            head = _H1.search(text) if markdown else None
            title = (_markup._inline(head.group(1)).strip() if head else
                     f"{source.get('title_prefix', '')}{version}".strip())
            if markdown:
                body = _markup.markdown_body(text[head.end():] if head else text)
            else:
                body = _markup.tidy(text, strip=False).strip()
            _markup.require(title, body, raw, min_chars=1)
            return _markup.document(title, blob, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['url']}: жоден файл не збігся з version_from.")
    return items
