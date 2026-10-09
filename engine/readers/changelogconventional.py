"""Читач CHANGELOG від conventional-changelog: «# [2.2.0](https://…/compare/…) (2026-08-29)».

`changelog-conventional` — CHANGELOG.md, поділений на версії, одна версія — один документ, як у
                           `changelog-heading`: `name_prefix` — рядок перед іменем документа,
                           `label` — підпис у назві, `cite` — адреса для людей. Заголовок версії —
                           «#», «##» чи «###», номер у ньому — посилання на порівняння версій
                           («[2.0.2](…)») або голий номер («# 1.0.0 (2021-12-29)»), дата — у
                           круглих дужках після нього.

Навіщо. Lerna з conventional-changelog пише журнал пакета монорепозиторію (так веде його
napi-rs/node-rs, звідки `@node-rs/argon2`): мінорні й мажорні версії — «#», латки — «##», номер —
посилання, а найперша версія — без посилання. `changelog-heading` посилання не бачить: журнал для
нього — одна версія 1.0.0, а записи 1.0.1–2.2.0 зникли б. `changelog-mixed` бачить посилання лише
за «##»: записи 2.2.0, 2.1.0, 1.8.0 тощо приліпли б до сусідніх латок.

Якір посилання рахується з того, що GitHub показує в заголовку («2.2.0 (2026-08-29)»), а не з
розмітки: адреса порівняння в якір не входить.

Чому окремий модуль: спільні читачі вже звірено в готових примірниках, а новий домен додає свого
читача, не змінюючи спільного.
"""

import re

from engine.readers import Item, _markup, register

_HEAD = re.compile(
    r"^#{1,3} +(?:\[v?(?P<linked>\d+\.\d+\.\d+[\w.-]*)\]\([^)\n]*\)|v?(?P<bare>\d+\.\d+\.\d+[\w.-]*))"
    r"[ \t]*(?P<date>\([^)\n]*\))?[ \t]*$", re.M)


@register("changelog-conventional")
def changelog_conventional(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    _markup.refuse_html(text, source["url"])
    heads = list(_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «# [X.Y.Z](…) (дата)» — "
                         f"формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    lead = (re.sub(r"[^\w.-]+", "-", source["name_prefix"]).strip("-") + "-"
            if source.get("name_prefix") else "")
    items = []
    for i, head in enumerate(heads):
        version = head.group("linked") or head.group("bare")
        heading = f"{version} {head.group('date') or ''}".strip()
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        name = lead + re.sub(r"[^\w.-]+", "-", version)
        anchor = _markup.github_anchor(heading)

        def make(chunk=chunk, heading=heading, version=version, anchor=anchor):
            body = _markup.markdown_body(chunk)
            _markup.require(heading, body, f"{source['url']} {heading}", min_chars=1)
            return _markup.document(f"{label}: {heading}", f"{cite}#{anchor}", ctx.stamp,
                                    body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
