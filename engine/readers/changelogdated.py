"""Читач CHANGELOG, де заголовок версії — «## 8.3.0 - 2026-07-11» (номер без дужок, дата через тире).

`changelog-dated` — те саме, що `changelog`: CHANGELOG.md, поділений на версії, одна
                    версія — один документ, версією документа стає номер із заголовка.

Навіщо. Helmet пише журнал як «## 8.3.0 - 2026-07-11»: дата через тире, без круглих дужок
(яких чекає `changelog`) і без квадратних (яких чекає `changelog-keep`). Обидва читачі такого
заголовка не впізнають, і журнал для них — жодної версії.

Тире буває й довгим: Expo пише «## 57.0.0 — 2026-07-08».

Місяць і день бувають однією цифрою: у журналі Certbot стоїть «## 0.28.0 - 2018-11-7», і без цього
запис 0.28.0 приліпав би до сусідньої версії.

Чому окремий модуль: спільні читачі вже звірено в готових примірниках, правка виразу в них —
ризик зсуву; новий домен додає свого читача.
"""

import re

from engine.readers import Item, _markup, register

_VERSION_HEAD = re.compile(
    r"^## +v?(\d+\.\d+\.\d+[\w.-]*)[ \t]+[-—][ \t]+(\d{4}-\d{1,2}-\d{1,2})[ \t]*$", re.M)


@register("changelog-dated")
def changelog_dated(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    heads = list(_VERSION_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «## X.Y.Z - дата» — "
                         f"формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    # Запис версії може повторитися (виправлений випуск під тим самим номером): окремими
    # документами з одним ім'ям файла другий затер би перший, тож записи зливаються в один.
    entries: dict = {}
    for i, head in enumerate(heads):
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        entries.setdefault(head.group(1), []).append((head.group(2), chunk))
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
