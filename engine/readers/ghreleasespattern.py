"""Читач нотаток релізів GitHub, де тег сталого релізу впізнається виразом, а не префіксом.

`ghreleases-pattern` — `url` — адреса API релізів (`…/releases?per_page=100`), `tag_pattern` — вираз над усім
                       тегом з групою `v`, що дає номер версії: `^v(?P<v>\\d+\\.\\d+\\.\\d+)(?:-ember-source)?$`.
                       Тег, що не збігся, не береться — так випадають і передрелізи (`v7.5.0-beta.1-ember-source`),
                       і релізи сусідніх пакетів монорепозиторію (`v2.2.1-@glimmer/component`). Необов'язкові
                       `label`, `name_prefix`, `version_prefix` — як у `ghreleases-tagged`.

Навіщо. Ember з 6.0 і Ember CLI з 6.5 ставлять ім'я пакета в кінець тегу: `v7.4.0-ember-source`,
`v7.3.0-ember-cli`, а старші релізи мають простий `v5.12.0`. `ghreleases-stable` бере версією решту тегу після
префікса і вважає все з дефісом за номером передрелізом, тож релізи 6.x–7.x випадали цілком. Тут версія — лише
група `v` («7.4.0»), той самий вигляд, що в журналі змін і реєстрі npm. Розбір нотатки той самий, що в
`ghreleases-tagged`; окремий модуль — щоб не зсунути примірники, звірені з тим читачем.
"""

import json
import re
from urllib.parse import parse_qs, urlsplit

from engine.readers import Item, _markup, register


@register("ghreleases-pattern")
def ghreleases_pattern(source: dict, ctx) -> list[Item]:
    if not source.get("tag_pattern"):
        raise SystemExit(f"{source['id']}: читач ghreleases-pattern потребує поля tag_pattern.")
    rx = re.compile(source["tag_pattern"])
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
    label = source.get("label", "Release")
    lead = (re.sub(r"[^\w.-]+", "-", source["name_prefix"]).strip("-") + "-"
            if source.get("name_prefix") else "")
    items = []
    for rel in releases:
        if not isinstance(rel, dict) or rel.get("draft") or rel.get("prerelease"):
            continue
        tag = str(rel.get("tag_name") or "")
        m = rx.match(tag)
        if not m:
            continue
        version = str(source.get("version_prefix") or "") + m.group("v")
        name = lead + re.sub(r"[^\w.-]+", "-", tag).strip("-")

        def make(rel=rel, tag=tag, version=version):
            day = str(rel.get("published_at") or rel.get("created_at") or "")[:10]
            notes = _markup.markdown_body(str(rel.get("body") or "")) or "No release notes."
            body = f"Tag {tag}, published {day}.\n\n{notes}"
            title = f"{label}: {rel.get('name') or tag}"
            return _markup.document(title, str(rel.get("html_url") or base), ctx.stamp,
                                    body, version)

        items.append(Item(id=f"{source['id']}/{name}", file=f"{source['id']}--{name}.txt", make=make))
    if not items:
        raise SystemExit(f"{base}: жодного релізу з тегом за `tag_pattern` — перевірте вираз.")
    return items
