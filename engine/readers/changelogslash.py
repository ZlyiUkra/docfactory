"""Читач CHANGELOG, де заголовок версії — «9.11.2 / 2026-10-12» з підкресленням «====».

`changelog-slash-dated` — те саме, що `changelog-dated`: CHANGELOG.md, поділений на версії, одна
                          версія — один документ, версією документа стає номер із заголовка.
                          Поля: `label` — підпис у назві, `cite` — адреса для людей,
                          `name_prefix` — рядок перед іменем документа, `version_prefix` —
                          рядок перед версією, `skip` — вираз версій, що не беруться.

Навіщо. Mongoose пише журнал як «9.11.2 / 2026-10-12» і рядок знаків «=» під ним: ні
дужок, ні тире, ні «##» — жоден із читачів журналів такого заголовка не впізнає, і тисяча
записів від 2010 року для них — жодної версії. Підкреслення буває коротшим чи довшим за
заголовок, а в найстаріших записах дата стоїть і без нуля в місяці.

Чому окремий модуль: спільні читачі вже звірено в готових примірниках, правка виразу — ризик
зсуву; новий домен додає свого читача.
"""

import re

from engine.readers import Item, _markup, register

_VERSION_HEAD = re.compile(
    r"^v?(\d+\.\d+\.\d+[\w.-]*)[ \t]*/[ \t]*(\d{4}-\d{1,2}-\d{1,2})[ \t]*\n=+[ \t]*$", re.M)


@register("changelog-slash-dated")
def changelog_slash_dated(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    heads = list(_VERSION_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «X.Y.Z / дата» з "
                         f"підкресленням — формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    prefix = str(source.get("name_prefix") or "")
    vprefix = str(source.get("version_prefix") or "")
    skip = re.compile(source["skip"]) if source.get("skip") else None
    entries: dict = {}
    for i, head in enumerate(heads):
        version = head.group(1)
        if skip and skip.search(version):
            continue
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        entries.setdefault(version, []).append((head.group(2), chunk))
    items = []
    for version, parts in entries.items():
        name = re.sub(r"[^\w.-]+", "-", version)
        if prefix:
            name = f"{prefix}-{name}"

        def make(parts=parts, version=version):
            bodies = [f"Released {day}.\n\n{_markup.markdown_body(chunk)}" for day, chunk in parts]
            return _markup.document(f"{label}: {version}", cite, ctx.stamp,
                                    "\n\n".join(bodies), vprefix + version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
