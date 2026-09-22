"""Читач нотаток релізів монорепозиторію: лише теги одного пакета.

`ghreleases-tagged` — те саме, що `ghreleases`, плюс обов'язкове поле
                      `tag_prefix`: беруться лише релізи, чий тег починається цим
                      рядком, а версією документа стає решта тега.

Навіщо. `ghreleases` бере всі релізи репозиторію підряд, і для одного пакета це
правильно. Але Astro живе монорепозиторієм: в одному потоці релізів стоять
`astro@7.3.3`, `@astrojs/vue@7.0.3`, `astro-vscode@2.17.0` і ще два десятки
пакетів. Без відбору корпус документації Astro на дві третини складався б із
нотаток чужих інтеграцій, а фільтр версії показував би лінії, яких у самого
фреймворка немає.

`tag_prefix: "astro@"` лишає рівно теги фреймворка, і версією стає «7.3.3» —
той самий вигляд, що й у решті корпусу, тож фільтр `version: "7"` бере і
документацію сьомої лінії, і її релізи.

Чому копія, а не поле в `ghreleases`: примірники `ecmascript`, `react` і `nestjs`
зібрані й звірені, а правка спільного читача — ризик зсуву в готовій роботі.
"""

import json
import re
from urllib.parse import parse_qs, urlsplit

from engine.readers import Item, _markup, register


@register("ghreleases-tagged")
def ghreleases_tagged(source: dict, ctx) -> list[Item]:
    prefix = str(source.get("tag_prefix") or "").strip()
    if not prefix:
        raise SystemExit(f"{source['id']}: читач ghreleases-tagged потребує поля "
                         f"tag_prefix (напр. «astro@»).")
    base = source["url"]
    per_page = int((parse_qs(urlsplit(base).query).get("per_page") or ["30"])[0])
    releases: list = []
    for page in range(1, 101):
        url = base if page == 1 else f"{base}{'&' if '?' in base else '?'}page={page}"
        try:
            batch = json.loads(ctx.text(url))
        except ValueError as exc:
            raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")
        if not isinstance(batch, list):
            raise SystemExit(f"{url}: очікував список релізів.")
        releases.extend(batch)
        if len(batch) < per_page:
            break
    if not releases:
        raise SystemExit(f"{base}: жодного релізу.")
    label = source.get("label", "Release")
    items = []
    for rel in releases:
        if not isinstance(rel, dict) or rel.get("draft") or not rel.get("tag_name"):
            continue
        tag = str(rel["tag_name"])
        if not tag.startswith(prefix):
            continue
        version = tag[len(prefix):].lstrip("v")
        name = re.sub(r"[^\w.-]+", "-", tag).strip("-")

        def make(rel=rel, tag=tag, version=version):
            day = str(rel.get("published_at") or rel.get("created_at") or "")[:10]
            pre = ", pre-release" if rel.get("prerelease") else ""
            notes = _markup.markdown_body(str(rel.get("body") or "")) or "No release notes."
            body = f"Tag {tag}, published {day}{pre}.\n\n{notes}"
            title = f"{label}: {rel.get('name') or tag}"
            return _markup.document(title, str(rel.get("html_url") or base), ctx.stamp,
                                    body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{base}: жодного релізу з тегом «{prefix}…» — "
                         f"перевірте tag_prefix.")
    return items
