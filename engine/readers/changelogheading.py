"""Читач CHANGELOG, де заголовок версії буває будь-якого рівня: «# 2.0.0», «## 1.0.26», «### 2.0.1».

`changelog-heading` — CHANGELOG.md, поділений на версії, одна версія — один документ, як у
                      `changelog-named`: `name_prefix` — рядок перед іменем документа, `label` —
                      підпис у назві, `cite` — адреса для людей. Різниця одна: заголовком версії
                      вважається «#», «##» і «###» з номером, а не лише «##».

Навіщо. Журнали супутніх пакетів react-window пишуть версії по-різному:
react-window-infinite-loader — «### 2.0.1», react-virtualized-auto-sizer — «## 2.0.1», але
«# 2.0.0» між ними. `changelog-named` бачить лише «##»: журнал infinite-loader для нього —
жодної версії, а запис 2.0.0 auto-sizer разом з інструкцією переходу ліг би в документ 2.0.1.
Підрозділи всередині запису («## Migrating from 1.x to 2.x» під «# 2.0.0») номера не мають і
лишаються в тілі свого запису.

Чому не поле в `changelog-named`: спільний читач уже звірено в примірниках, що ним зібрані, а
новий домен додає свого читача, не змінюючи спільного.
"""

import re

from engine.readers import Item, _markup, register

_HEAD = re.compile(r"^#{1,3} +v?(\d+\.\d+\.\d+[\w.-]*)[ \t]*(\([^)\n]*\))?[ \t]*$", re.M)


@register("changelog-heading")
def changelog_heading(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    _markup.refuse_html(text, source["url"])
    heads = list(_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «# X.Y.Z» — "
                         f"формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    lead = (re.sub(r"[^\w.-]+", "-", source["name_prefix"]).strip("-") + "-"
            if source.get("name_prefix") else "")
    items = []
    for i, head in enumerate(heads):
        version = head.group(1)
        heading = f"{version} {head.group(2) or ''}".strip()
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        name = lead + re.sub(r"[^\w.-]+", "-", version)
        anchor = _markup.github_anchor(head.group(0).lstrip("#"))

        def make(chunk=chunk, heading=heading, version=version, anchor=anchor):
            body = _markup.markdown_body(chunk)
            _markup.require(heading, body, f"{source['url']} {heading}", min_chars=1)
            return _markup.document(f"{label}: {heading}", f"{cite}#{anchor}", ctx.stamp,
                                    body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
