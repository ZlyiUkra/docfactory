"""Читач журналів змін OpenTelemetry: усі види заголовка версії, якими пишуть репозиторії проєкту.

`changelog-otel` — CHANGELOG.md, поділений на версії, одна версія — один документ, як у
                   `changelog-conventional`: `name_prefix` — рядок перед іменем документа, `label` —
                   підпис у назві, `cite` — адреса для людей, `version_prefix` — рядок перед версією в
                   документі («spec-», «collector-», «instrumentation-express-»). Заголовок версії —
                   «#», «##» чи «###» з номером у будь-якому з видів:
                   «## 2.12.0» (opentelemetry-js), «## v1.61.0 (2026-09-12)» (специфікація),
                   «## [0.71.1](…/compare/…) (2026-10-15)» і старе «### [0.23.1](…)» (release-please у
                   js-contrib), «## v1.2.0 - 2026-09-11» (декларативна конфігурація), «## v0.50.0 Beta»
                   і «## v1.69.0/v0.163.0» (Collector: стабільні модулі й решта однією лінією).
                   Необов'язкове `pick: "last"` — з подвійного номера береться другий: лінія 0.x, якою
                   нумеруються випуски Collector, а не 1.x його стабільних модулів. «Unreleased» номера
                   не має й документом не стає.

Навіщо свій читач. Проєкт пише журнали п'ятьма способами, і кожен спільний читач бачить лише свій:
`changelog-named` — голий номер, `changelog-conventional` — дату лише в дужках, `changelog-dated` —
лише через тире, і жоден не знає подвійного номера Collector. Узяті різними читачами, журнали одного
примірника ще й по-різному називали б документи; тут ім'я — `name_prefix` і номер, версія — з
`version_prefix`, щоб фільтр «collector-0.163» не змішувався зі «spec-1.61» чи SDK 2.x.
"""

import re

from engine.readers import Item, _markup, register

_HEAD = re.compile(
    r"^#{1,3} +\[?v?(?P<first>\d+\.\d+\.\d+(?:-[\w.]+)?)\]?(?:\([^)\n]*\))?"
    r"(?:/v?(?P<second>\d+\.\d+\.\d+(?:-[\w.]+)?))?(?P<rest>[^\n]*)$", re.M)


@register("changelog-otel")
def changelog_otel(source: dict, ctx) -> list[Item]:
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    _markup.refuse_html(text, source["url"])
    heads = list(_HEAD.finditer(text))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії — формат змінився, читача треба "
                         f"поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    lead = (re.sub(r"[^\w.-]+", "-", source["name_prefix"]).strip("-") + "-"
            if source.get("name_prefix") else "")
    prefix = str(source.get("version_prefix") or "")
    last = source.get("pick") == "last"
    items, seen = [], set()
    for i, head in enumerate(heads):
        version = (head.group("second") if last and head.group("second") else head.group("first"))
        rest = head.group("rest").strip()
        heading = f"{version} {rest}".strip()
        name = lead + re.sub(r"[^\w.-]+", "-", version)
        # Той самий номер двічі (запис повторено після виправлення журналу) — одне ім'я файла;
        # другий запис дістає мітку, щоб не затерти першого.
        while name in seen:
            name += "-x"
        seen.add(name)
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        anchor = _markup.github_anchor(head.group(0).lstrip("#").strip())

        def make(chunk=chunk, heading=heading, version=version, anchor=anchor):
            body = _markup.markdown_body(chunk)
            _markup.require(heading, body, f"{source['url']} {heading}", min_chars=1)
            return _markup.document(f"{label}: {heading}", f"{cite}#{anchor}", ctx.stamp,
                                    body, prefix + version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
