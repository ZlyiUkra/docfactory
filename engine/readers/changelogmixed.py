"""Читач CHANGELOG із трьома видами заголовка версії в одному файлі.

`changelog-mixed` — те саме, що `changelog-dated`: CHANGELOG.md, поділений на версії, одна
                    версія — один документ, версією документа стає номер із заголовка.

Навіщо. Nodemailer міняв формат журналу тричі, і всі три живуть в одному файлі:
«## [10.0.16](https://…/compare/v10.0.15...v10.0.16) (2026-10-07)» (release-please, від 6.9.5),
«## 6.9.4 2023-07-19» (номер і дата через пробіл) та «## v0.6.1 2014-01-26» (з «v»). Жоден зі
спільних читачів не бере всіх трьох разом, і журнал для них — або частина версій, або жодної.

Чому окремий модуль: спільні читачі вже звірено в готових примірниках, правка виразу в них —
ризик зсуву; новий домен додає свого читача.
"""

import re

from engine.readers import Item, _markup, register

_VERSION_HEAD = re.compile(
    r"^## +(?:\[v?(?P<a>\d+\.\d+\.\d+[\w.-]*)\]\([^)\n]*\)[ \t]+\((?P<da>\d{4}-\d{2}-\d{2})\)"
    r"|v?(?P<b>\d+\.\d+\.\d+[\w.-]*)[ \t]+(?P<db>\d{4}-\d{2}-\d{2}))[ \t]*$", re.M)


@register("changelog-mixed")
def changelog_mixed(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    heads = list(_VERSION_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії — формат змінився, "
                         f"читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    # Запис версії може повторитися (виправлений випуск під тим самим номером): окремими
    # документами з одним ім'ям файла другий затер би перший, тож записи зливаються в один.
    entries: dict = {}
    for i, head in enumerate(heads):
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        version = head.group("a") or head.group("b")
        day = head.group("da") or head.group("db")
        if "-" in version:                       # передрелізи (2.1.0-beta.0): лише стабільні версії
            continue
        entries.setdefault(version, []).append((day, chunk))
    items = []
    for version, parts in entries.items():
        name = re.sub(r"[^\w.-]+", "-", version)

        def make(parts=parts, version=version):
            bodies = [f"Released {day}.\n\n{_markup.markdown_body(chunk)}" for day, chunk in parts]
            return _markup.document(f"{label}: {version}", cite, ctx.stamp,
                                    "\n\n".join(bodies), version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
