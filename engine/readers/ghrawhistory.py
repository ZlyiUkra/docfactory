"""Читач файлів репозиторію на тегах без дерев API: один документ на кожен неповторний вміст файла.

`ghraw-history` — `url` — префікс сирих файлів репозиторію (`https://raw.githubusercontent.com/ВЛАСНИК/РЕПО/`),
                  `tags` — об'єкт «тег → версія» від найновішого, `files` — шляхи файлів markdown.
                  Кожен файл кожного тегу читається напряму (`<url><тег>/<шлях>`); відсутній на тезі
                  файл (404) пропускається. Однаковий вміст на кількох тегах — один документ з усіма
                  їхніми версіями, у шапці — адреса blob на GitHub найновішого з них. `name_prefix` —
                  початок імені документа (назва репозиторію), `title_prefix` — початок назви.

Навіщо. `ghdocs-history` бере дерево тегу через API, щоб знайти файли: у SDK Stripe понад шість
тисяч стабільних тегів, а година API з токеном — п'ять тисяч звернень; дерева stripe-ios і
stripe-java (понад гігабайт) GitHub ще й обрізає. Тут потрібні лише кілька відомих файлів кореня
(README, MIGRATING, CONTRIBUTING), і сирі файли не витрачають ліміт API зовсім.
"""

import hashlib
import re
from urllib.parse import quote

from engine.readers import Item, _markup, register

_TITLE = re.compile(r"\A\s*#\s+(.+)\n")


@register("ghraw-history")
def ghraw_history(source: dict, ctx) -> list[Item]:
    base = source["url"].rstrip("/") + "/"
    m = re.match(r"https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/$", base)
    if not m:
        raise SystemExit(f"{source['id']}: url — префікс https://raw.githubusercontent.com/ВЛАСНИК/РЕПО/.")
    owner, repo = m.groups()
    tags = source.get("tags")
    if not isinstance(tags, dict) or not tags:
        raise SystemExit(f"{source['id']}: потрібне поле tags — «тег → версія».")
    lead = _markup.slug(source.get("name_prefix") or repo)
    prefix = source.get("title_prefix", "")
    # (шлях, хеш вмісту) → [найновіший тег, [версії]]; вміст не тримається в пам'яті —
    # make прочитає його ще раз з тієї самої адреси (у межах прогону — зі сховища сирого).
    seen: dict = {}
    for tag, version in tags.items():
        for path in source.get("files") or ():
            url = f"{base}{quote(tag, safe='@')}/{quote(path)}"
            if not ctx.allowed(url):
                continue
            code, data = ctx.fetch(url)
            if code != "200" or not data.strip():
                continue
            key = (path, hashlib.sha1(data).hexdigest()[:8])
            if key not in seen:
                seen[key] = [tag, url, []]
            seen[key][2].append(version)
    if not seen:
        raise SystemExit(f"{source['id']}: жодного з файлів {source.get('files')} на жодному тезі.")
    items = []
    for (path, digest), (tag, url, versions) in seen.items():
        stem = re.sub(r"\.md$", "", path, flags=re.I)
        name = f"{lead}-{_markup.slug(stem)}-{digest}"

        def make(path=path, tag=tag, url=url, versions=versions):
            text = ctx.text(url)
            meta, rest = _markup.front_matter(text)
            head = _TITLE.match(rest)
            title = meta.get("title") or (head.group(1).strip() if head else path)
            if head:
                rest = rest[head.end():]
            if prefix and prefix.lower() not in title.lower():
                title = f"{prefix}: {title}"
            body = _markup.markdown_body(rest)
            _markup.require(title, body, url, min_chars=1)
            page = f"https://github.com/{owner}/{repo}/blob/{quote(tag, safe='@')}/{quote(path)}"
            return _markup.document(title, page, ctx.stamp, body, ", ".join(versions))

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    return items
