"""Читач CHANGELOG у форматі Keep a Changelog: «## [7.89.0] - 2026-09-26».

`changelog-keep` — те саме, що `changelog`: CHANGELOG.md, поділений на версії, одна
                   версія — один документ, версією документа стає номер у дужках.

Навіщо. React Hook Form пише журнал змін за https://keepachangelog.com: номер у квадратних
дужках, дата через тире. Чинні `changelog` і `changelog-v` такого заголовка не впізнають, і
журнал для них — жодної версії.

Чому окремий модуль, а не ще один варіант виразу в `changelog`: примірники, чиї журнали
вже поділено на документи, звірені, а правка спільного читача — ризик зсуву в готовій роботі.
"""

import re

from engine.readers import Item, _markup, register

_VERSION_HEAD = re.compile(
    r"^## +\[v?(\d+\.\d+[\w.-]*)\][ \t]*(?:-[ \t]*([\w-]+))?[ \t]*$", re.M)


@register("changelog-keep")
def changelog_keep(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    heads = list(_VERSION_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «## [X.Y.Z] - дата» — "
                         f"формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    # версія → [(дата, текст)]. Журнал RHF буває з двома записами однієї версії (6.12.0 від
    # 28.11 і від 12.12.2020): окремими документами з одним ім'ям файла другий затер би
    # перший, тож записи версії зливаються в один документ у порядку журналу.
    entries: dict = {}
    for i, head in enumerate(heads):
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        entries.setdefault(head.group(1), []).append((head.group(2) or "", chunk))
    items = []
    for version, parts in entries.items():
        name = re.sub(r"[^\w.-]+", "-", version)

        def make(parts=parts, version=version):
            bodies = []
            for day, chunk in parts:
                body = _markup.markdown_body(chunk)
                bodies.append(f"Released {day}.\n\n{body}" if day else body)
            return _markup.document(f"{label}: {version}", cite, ctx.stamp,
                                    "\n\n".join(bodies), version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
