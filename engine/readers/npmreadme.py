"""Читач README пакета npm: один документ на кожен неповторний текст README серед усіх версій.

`npm-readme` — `url` — опис пакета в реєстрі (https://registry.npmjs.org/ПАКЕТ), `files` —
               шаблон адреси README однієї версії з `{version}`, `{gitHead}` або `{ref}` (напр.
               https://raw.githubusercontent.com/ВЛАСНИК/РЕПО/{gitHead}/README.md), або
               список таких шаблонів, які пробуються по черзі.
               Необов'язкові поля: `tag` — шаблон тегу з `{version}` (напр. `v{version}`): `{ref}`
               стає `gitHead`, а коли реєстр коміту не записав, — цим тегом; `skip_versions` —
               вираз версій, які не беруться (напр. `-canary`); `min_chars` — найкоротший текст,
               що вважається README: коротший (заглушка «дивись сайт») — привід узяти наступний
               шаблон.

Навіщо. README, що публікується в npm разом із пакетом, — найстаріша документація
бібліотеки: у перших версіях іншої не було, а сайт з'явився пізніше. Реєстр віддає текст
README лише найновішої версії, тож кожна версія читається окремо. `{gitHead}` — коміт, з
якого версію опубліковано (реєстр пише його в опис кожної версії): README пакета —
це README кореня репозиторію на тому коміті. CDN з вмістом пакетів (jsDelivr, unpkg)
тут не годиться: білий список не вміє дозволити «лише цей пакет» на спільному хості.

Кілька шаблонів — для монорепозиторію, де README пакета з часом переїхав: у Zod до v4 це
кореневий README.md, а з v4 — packages/zod/README.md, тоді як у корені лишилася заглушка на
22 байти. Реєстр пише `gitHead` не для кожної версії (у Zod 4.6.5 його немає), і тоді коміт
заміняє тег релізу.

Між сусідніми версіями README зазвичай не змінюється: сотні версій дають кілька десятків
різних текстів. Тому одиниця — неповторний текст (упізнається хешем), а його версії — усі,
у пакеті яких README був саме таким. Перелік складається одразу: щоб звести однакові тексти,
їх треба прочитати. Але в пам'яті лишаються тільки хеш, адреса й версії: сам текст
читається вдруге під час запису (адреса вказує на незмінний коміт чи тег), бо сотні
великих README разом тиснуть на пам'ять машини, де поруч працюють Qdrant і сервери.
"""

import hashlib
import json
import re

from engine.readers import Item, _markup, register
from engine.readers.ghhistory import _atx, _split_title


@register("npm-readme")
def npm_readme(source: dict, ctx) -> list[Item]:
    patterns = source.get("files", "")
    patterns = [patterns] if isinstance(patterns, str) else list(patterns or [])
    if not patterns or not all(any(k in p for k in ("{version}", "{gitHead}", "{ref}"))
                               for p in patterns):
        raise SystemExit(f"{source['id']}: читач npm-readme потребує поля files з "
                         f"{{version}}, {{gitHead}} або {{ref}}.")
    tag = str(source.get("tag") or "")
    skip = re.compile(source["skip_versions"]) if source.get("skip_versions") else None
    min_chars = int(source.get("min_chars") or 0)
    try:
        packument = json.loads(ctx.text(source["url"]))
    except ValueError as exc:
        raise SystemExit(f"{source['url']}: відповідь не JSON ({exc}).")
    times = packument.get("time") or {}
    versions = sorted((v for v in packument.get("versions") or {}
                       if v in times and not (skip and skip.search(v))),
                      key=lambda v: times[v], reverse=True)
    if not versions:
        raise SystemExit(f"{source['url']}: жодної версії.")
    # хеш тексту → [адреса найновішої версії з ним, [версії]]
    seen: dict = {}
    missing = []
    for v in versions:
        head = str((packument["versions"][v] or {}).get("gitHead") or "")
        ref = head or (tag.replace("{version}", v) if tag else "")
        text = url = ""
        for pattern in patterns:
            if ("{gitHead}" in pattern and not head) or ("{ref}" in pattern and not ref):
                continue
            candidate = (pattern.replace("{version}", v).replace("{gitHead}", head)
                         .replace("{ref}", ref))
            if not ctx.allowed(candidate):
                continue
            try:
                got = ctx.text(candidate)
            except SystemExit as exc:
                # Пакет без README (так буває в найперших збірках) — не збій переліку.
                if "404" not in str(exc):
                    raise
                continue
            if len(got.strip()) >= min_chars:
                text, url = got, candidate
                break
        if not text:
            missing.append(v)
            continue
        text = text.replace("\r\n", "\n")
        key = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
        seen.setdefault(key, [url, []])[1].append(v)
        del text
    if missing:
        print(f"  {source['id']}: без README {len(missing)} версій: {', '.join(missing[:12])}"
              f"{' …' if len(missing) > 12 else ''}")

    items = []
    label = source.get("label", "README")
    for key, (url, found) in seen.items():
        newest = found[0]
        name = f"{re.sub(r'[^\w.-]+', '-', newest)}-{key[:8]}"

        def make(url=url, found=found, newest=newest):
            text = ctx.text(url).replace("\r\n", "\n")
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
