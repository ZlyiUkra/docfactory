"""Читач README пакета npm: один документ на кожен неповторний текст README серед усіх версій.

`npm-readme` — `url` — опис пакета в реєстрі (https://registry.npmjs.org/ПАКЕТ), `files` —
               шаблон адреси README однієї версії з `{version}` або `{gitHead}` (напр.
               https://raw.githubusercontent.com/ВЛАСНИК/РЕПО/{gitHead}/README.md).

Навіщо. README, що публікується в npm разом із пакетом, — найстаріша документація
бібліотеки: у перших версіях іншої не було, а сайт з'явився пізніше. Реєстр віддає текст
README лише найновішої версії, тож кожна версія читається окремо. `{gitHead}` — коміт, з
якого версію опубліковано (реєстр пише його в опис кожної версії): README пакета —
це README кореня репозиторію на тому коміті. CDN з вмістом пакетів (jsDelivr, unpkg)
тут не годиться: білий список не вміє дозволити «лише цей пакет» на спільному хості.

Між сусідніми версіями README зазвичай не змінюється: сотні версій дають кілька десятків
різних текстів. Тому одиниця — неповторний текст (упізнається хешем), а його версії — усі,
у пакеті яких README був саме таким. Перелік складається одразу: щоб звести однакові тексти,
їх треба прочитати, тож тексти й тримаються в пам'яті до запису.
"""

import hashlib
import json
import re

from engine.readers import Item, _markup, register
from engine.readers.ghhistory import _atx, _split_title


@register("npm-readme")
def npm_readme(source: dict, ctx) -> list[Item]:
    pattern = source.get("files", "")
    if "{version}" not in pattern and "{gitHead}" not in pattern:
        raise SystemExit(f"{source['id']}: читач npm-readme потребує поля files з "
                         f"{{version}} або {{gitHead}}.")
    try:
        packument = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}).")
    times = packument.get("time") or {}
    versions = sorted((v for v in packument.get("versions") or {} if v in times),
                      key=lambda v: times[v], reverse=True)
    if not versions:
        raise SystemExit(f"{source['url']}: жодної версії.")
    # хеш тексту → [текст, адреса найновішої версії з ним, [версії]]
    seen: dict = {}
    missing = []
    for v in versions:
        head = str((packument["versions"][v] or {}).get("gitHead") or "")
        if "{gitHead}" in pattern and not head:
            missing.append(v)
            continue
        url = pattern.replace("{version}", v).replace("{gitHead}", head)
        if not ctx.allowed(url):
            continue
        try:
            text = ctx.text(url)
        except SystemExit as exc:
            # Пакет без README (так буває в найперших збірках) — не збій переліку.
            if "404" not in str(exc):
                raise
            missing.append(v)
            continue
        text = text.replace("\r\n", "\n")
        key = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
        seen.setdefault(key, [text, url, []])[2].append(v)
    if missing:
        print(f"  {source['id']}: без README {len(missing)} версій: {', '.join(missing[:12])}"
              f"{' …' if len(missing) > 12 else ''}")

    items = []
    label = source.get("label", "README")
    for key, (text, url, found) in seen.items():
        newest = found[0]
        name = f"{re.sub(r'[^\w.-]+', '-', newest)}-{key[:8]}"

        def make(text=text, url=url, found=found, newest=newest):
            _markup.refuse_html(text, url)
            meta, rest = _markup.front_matter(text)
            title, rest = _split_title(_atx(rest))
            body = _markup.markdown_body(rest)
            span = found[-1] if len(found) == 1 else f"{found[-1]} … {found[0]}"
            full = f"{label} {span}" + (f": {title}" if title else "")
            return _markup.document(full, url, ctx.stamp, body, ", ".join(found))

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{source['id']}: жодного README.")
    return items
