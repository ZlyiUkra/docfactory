"""Читач CHANGELOG, де номер версії то голий, то в дужках із посиланням і датою.

`changelog-bracket` — CHANGELOG.md, поділений на версії, одна версія — один документ, як у
                      `changelog-heading`: `name_prefix` — рядок перед іменем документа, `label` —
                      підпис у назві, `cite` — адреса для людей. Заголовок версії — «##» з номером
                      у будь-якому з видів: «## 1.75.2», «## [1.56.11](адреса) - 2026-05-07»,
                      «## [0.9.0] - 2025-09-25», «## [0.9.10] - 2025-09-25(адреса)». Дата, якщо є,
                      лишається в назві документа.

Навіщо. Журнал i18next-cli до 1.56.11 писався інструментом релізів — номер у квадратних дужках,
посилання на порівняння тегів і дата через дефіс (а в перших записах посилання прилипло вже
після дати), — а з 1.56.12 руками: голий номер. `changelog-heading` бачить лише голий номер,
`changelog-linked` — лише посилання без дати, `changelog-keep` — лише дужки без посилання, тож
кожен із них губив би більшу частину журналу, а записи, яких він не бачить, лягали б у тіло
сусідньої версії.

Чому не поле в наявному читачі: спільні читачі звірено в примірниках, що ними зібрані, а новий
домен додає свого читача, не змінюючи спільного.
"""

import re

from engine.readers import Item, _markup, register

_VERSION = r"v?(\d+\.\d+\.\d+[\w.-]*)"
_HEAD = re.compile(rf"^## +(?:\[{_VERSION}\](?:\([^)\n]*\))?|{_VERSION})([^\n]*)$", re.M)
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
# Якір GitHub будується з показаного тексту заголовка, а посилання показує лише свій текст:
# «[1.56.11](адреса) - 2026-05-07» має якір «15611---2026-05-07», без адреси.
_LINK = re.compile(r"\[([^\]\n]*)\]\([^)\n]*\)")


@register("changelog-bracket")
def changelog_bracket(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    _markup.refuse_html(text, source["url"])
    heads = list(_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «## X.Y.Z» чи "
                         f"«## [X.Y.Z]» — формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    lead = (re.sub(r"[^\w.-]+", "-", source["name_prefix"]).strip("-") + "-"
            if source.get("name_prefix") else "")
    items = []
    for i, head in enumerate(heads):
        version = head.group(1) or head.group(2)
        date = _DATE.search(head.group(3))
        heading = f"{version} ({date.group(0)})" if date else version
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        name = lead + re.sub(r"[^\w.-]+", "-", version)
        anchor = _markup.github_anchor(_LINK.sub(r"\1", head.group(0).lstrip("#")))

        def make(chunk=chunk, heading=heading, version=version, anchor=anchor):
            body = _markup.markdown_body(chunk)
            _markup.require(heading, body, f"{source['url']} {heading}", min_chars=1)
            return _markup.document(f"{label}: {heading}", f"{cite}#{anchor}", ctx.stamp,
                                    body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
