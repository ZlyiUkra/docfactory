"""Читач CHANGELOG, де номер версії в заголовку — посилання без дати: «## [8.7.1](https://…/v8.7.1)».

`changelog-linked` — те саме, що `changelog-keep`: CHANGELOG.md, поділений на версії, одна
                     версія — один документ, версією документа стає номер у дужках (з «v» чи
                     без). Голий номер «## v3.1.1» — теж заголовок версії. Підсумок цілої
                     лінії («## [4.x](…)») — теж документ, з версією «4.x»: фільтр «4» його
                     знаходить. Необов'язкові поля: `name_prefix` — рядок перед номером в імені
                     документа, `label` — підпис у назві, `cite` — адреса для людей.

Навіщо. express-rate-limit і сховища його організації пишуть журнал за Keep a Changelog, але
номер у квадратних дужках — посилання на реліз GitHub, а дати немає зовсім. `changelog-keep`
чекає після дужок кінця рядка чи « - дата», `changelog-mixed` — дати в круглих дужках, тож
для обох такий журнал — жодної версії. express-slow-down до того ж змішує в одному файлі обидва
види: «## v3.1.1» нагорі й «## [v1.5.0](…)» нижче, а `changelog-heading` бере лише перший.

Чому окремий модуль: спільні читачі вже звірено в готових примірниках, правка виразу в них —
ризик зсуву; новий домен додає свого читача.
"""

import re

from engine.readers import Item, _markup, register

_VERSION = r"v?(\d+\.(?:\d+\.\d+[\w.-]*|x))"
_VERSION_HEAD = re.compile(rf"^## +(?:\[{_VERSION}\]\([^)\n]*\)|{_VERSION})[ \t]*$", re.M)


@register("changelog-linked")
def changelog_linked(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    heads = list(_VERSION_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «## [X.Y.Z](посилання)» "
                         f"чи «## vX.Y.Z» — формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    lead = (re.sub(r"[^\w.-]+", "-", source["name_prefix"]).strip("-") + "-"
            if source.get("name_prefix") else "")
    # версія → [текст]. Якщо номер у журналі трапився двічі, окремі документи з одним ім'ям
    # файла затерли б один одного, тож записи версії зливаються в порядку журналу.
    entries: dict = {}
    for i, head in enumerate(heads):
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        entries.setdefault(head.group(1) or head.group(2), []).append(chunk)
    items = []
    for version, chunks in entries.items():
        name = lead + re.sub(r"[^\w.-]+", "-", version)

        def make(chunks=chunks, version=version):
            body = "\n\n".join(_markup.markdown_body(c) for c in chunks)
            _markup.require(version, body, f"{source['url']} {version}", min_chars=1)
            return _markup.document(f"{label}: {version}", cite, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
