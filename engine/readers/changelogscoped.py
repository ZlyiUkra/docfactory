"""Читач спільного журналу змін монорепозиторію, де заголовок версії несе ім'я пакета: «## pg@8.23.0».

`changelog-scoped` — CHANGELOG.md, поділений на версії, одна версія — один документ, як у
                     `changelog-heading` (заголовок будь-якого рівня «#»–«###»). Заголовок буває
                     з пакетом (`pg@8.23.0`, `pg-pool@3.0.0`) і без нього (`v6.2.0`, `7.11.0`):
                     перший дає документ цього пакета, другий — пакета з поля `package`, головного
                     в журналі. Ім'я документа — «пакет-версія», назва — «підпис: пакет@версія».
                     `label` — підпис у назві, `cite` — адреса для людей.

Навіщо. node-postgres веде один журнал на весь монорепозиторій: «## pg@8.23.0», «### pg-pool@3.0.0» і
«### pg-cursor@2.0.0» стоять у ньому поруч, а записи до переходу на монорепозиторій — «### v6.2.0» і
«### 7.11.0», без пакета, бо тоді пакет був один. `changelog-heading` номера з «pg@» не впізнає, а
`changelog-named` чекає назви через пробіл. Пакет у імені документа ще й розводить однакові номери
різних пакетів: «pg-pool@3.0.0» і «pg@3.0.0» — різні записи.

Чому не поле в `changelog-heading`: той читач звірено на примірнику react-window, а новий домен додає
свого читача, не змінюючи спільного.
"""

import re

from engine.readers import Item, _markup, register

_HEAD = re.compile(r"^#{1,3} +(?:([a-z][\w.-]*)@)?v?(\d+\.\d+\.\d+[\w.-]*)[ \t]*(\([^)\n]*\))?[ \t]*$",
                   re.M)


@register("changelog-scoped")
def changelog_scoped(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    _markup.refuse_html(text, source["url"])
    heads = list(_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «## пакет@X.Y.Z» — "
                         f"формат змінився, читача треба поправити.")
    default = source.get("package")
    if not default:
        raise SystemExit(f"{source['id']}: читач changelog-scoped потребує поля package — пакета "
                         f"для заголовків без імені.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    items, seen = [], set()
    for i, head in enumerate(heads):
        package, version = head.group(1) or default, head.group(2)
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        name = re.sub(r"[^\w.-]+", "-", f"{package}-{version}").strip("-")
        # Той самий запис двічі (заголовок повторено рівнем нижче) — один документ: перший.
        if name in seen:
            continue
        seen.add(name)
        anchor = _markup.github_anchor(head.group(0).lstrip("#"))
        heading = f"{package}@{version} {head.group(3) or ''}".strip()

        def make(chunk=chunk, heading=heading, version=version, anchor=anchor):
            body = _markup.markdown_body(chunk)
            _markup.require(heading, body, f"{source['url']} {heading}", min_chars=1)
            return _markup.document(f"{label}: {heading}", f"{cite}#{anchor}", ctx.stamp,
                                    body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
