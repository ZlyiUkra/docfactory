"""Читач ChangeLog libuv: «2026.09.24, Version 1.53.0 (Stable), 840404ce…» і список змін до наступного заголовка.

`changelog-libuv` — один документ на версію. `url` — файл ChangeLog, `cite` — адреса для людей, `label` — підпис
                    у назві, `name_prefix` — рядок перед версією в імені документа. Заголовок — дата з крапками,
                    слово Version, номер, у дужках стан лінії (Stable, Maintenance) і хеш коміту випуску; хеш у
                    назву не потрапляє, а стан лінії лишається — з нього видно, чи була лінія ще підтримуваною.

Навіщо. Журнал libuv не markdown: заголовка немає, дата йде першою, і жоден із готових читачів журналів його не
впізнає. Це єдине місце, де записано, що змінювалося між версіями й що виправлено (з номерами помилок).
"""

import re

from engine.readers import Item, _markup, register

_HEAD = re.compile(
    r"^(?P<date>\d{4}\.\d{2}\.\d{2}), Version (?P<v>\d+\.\d+\.\d+)(?P<rest>[^\n]*)$", re.M)


@register("changelog-libuv")
def changelog_libuv(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    _markup.refuse_html(text, source["url"])
    heads = list(_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка «дата, Version X.Y.Z» — формат змінився, "
                         f"читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "ChangeLog")
    lead = (re.sub(r"[^\w.-]+", "-", source["name_prefix"]).strip("-") + "-"
            if source.get("name_prefix") else "")
    items, seen = [], set()
    for i, head in enumerate(heads):
        version = head.group("v")
        if version in seen:
            continue
        seen.add(version)
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        chunk = text[head.end():end]
        state = re.search(r"\(([^)]+)\)", head.group("rest"))
        title = f"{label}: {version} ({state.group(1)}) — {head.group('date').replace('.', '-')}" \
            if state else f"{label}: {version} — {head.group('date').replace('.', '-')}"
        name = lead + version

        def make(chunk=chunk, title=title, version=version):
            body = _markup.markdown_body(chunk)
            _markup.require(title, body, f"{cite} {version}", min_chars=1)
            return _markup.document(title, f"{cite}", ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    return items
