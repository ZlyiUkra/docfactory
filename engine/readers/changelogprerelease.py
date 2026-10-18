"""Читач CHANGELOG, де зміни сталого випуску записано під його передрелізами.

`changelog-prerelease` — CHANGELOG.md, поділений на версії: один сталий випуск — один документ.
                         Заголовок версії — «## v1.19.0» чи «## 1.14.0»; заголовок передрелізу —
                         той самий номер із хвостом «-rc.7», «-beta.1», «~rc.2». Записи
                         передрелізів стають розділами документа свого сталого випуску
                         («## v1.19.0-rc.7»), а їхні підзаголовки — під ними; передреліз,
                         чийого сталого запису у файлі немає, не береться. `label` — підпис у
                         назві, `cite` — адреса для людей, `name_prefix` — рядок перед номером в
                         імені документа, `version_prefix` — рядок перед номером у мітці версії.

Навіщо. NVIDIA Container Toolkit пише журнал так: «## v1.19.0» — один рядок «Promote v1.19.0-rc.7 to
v1.19.0», а все, що в 1.19.0 справді змінилося, — під «## v1.19.0-rc.1» … «## v1.19.0-rc.7». Примірник
бере лише сталі версії: `changelog-v` з `skip` лишив би від 1.19.0 той один рядок, а без `skip` дав би
документи «1.19.0-rc.3», яких фільтр версії «1.19.0» не знаходить, — на питання «що змінилося в
1.19.0» відповіді не було б ні так, ні так. Тут зміни передрелізів лежать у документі 1.19.0, з
назвою передрелізу, де їх уперше випущено.

Рядок рівня версії без номера («## Changes in libnvidia-container» посеред запису) — підрозділ
свого запису, не новий запис.

Чому окремий модуль: `changelog-v` звірено в готових примірниках, а правка спільного читача —
ризик зсуву в готовій роботі.
"""

import re

from engine.readers import Item, _markup, register

_HEAD = re.compile(r"^## +v?(\d+(?:\.\d+)+)([-~][0-9A-Za-z.-]+)?[ \t]*$", re.M)
# Рядок рівня запису без номера всередині передрелізу — його підрозділ, а не сусідній розділ.
_LEVEL2 = re.compile(r"^## (?=\S)", re.M)


@register("changelog-prerelease")
def changelog_prerelease(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    _markup.refuse_html(text, source["url"])
    heads = list(_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «## vX.Y.Z» — формат "
                         f"змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    lead = (re.sub(r"[^\w.-]+", "-", source["name_prefix"]).strip("-") + "-"
            if source.get("name_prefix") else "")
    vprefix = source.get("version_prefix", "")

    # Сталий номер → [заголовок, власний текст, [(заголовок передрелізу, текст)…]], у порядку файла.
    releases: dict[str, list] = {}
    pre: list[tuple[str, str, str]] = []
    for i, head in enumerate(heads):
        number, tail = head.group(1), head.group(2) or ""
        heading = head.group(0)[2:].strip()
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        if tail:
            pre.append((number, heading, chunk))
        elif number not in releases:
            releases[number] = [heading, chunk, []]
    for number, heading, chunk in pre:
        if number in releases:
            releases[number][2].append((heading, chunk))

    items = []
    for number, (heading, chunk, pres) in releases.items():
        name = lead + re.sub(r"[^\w.-]+", "-", number)

        def make(heading=heading, chunk=chunk, pres=pres, number=number):
            parts = [chunk.strip("\n")]
            for pre_heading, pre_chunk in pres:
                parts.append(f"## {pre_heading}\n\n{_LEVEL2.sub('### ', pre_chunk).strip()}")
            body = _markup.markdown_body("\n\n".join(p for p in parts if p))
            _markup.require(heading, body, f"{source['url']} {heading}", min_chars=1)
            url = f"{cite}#{_markup.github_anchor(heading)}"
            return _markup.document(f"{label}: {heading}", url, ctx.stamp, body,
                                    vprefix + number)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
