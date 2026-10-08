"""Читач CHANGELOG, де номер версії в заголовку стоїть із «v».

`changelog-v` — те саме, що `changelog`: CHANGELOG.md, поділений на версії, одна
                версія — один документ. Різниця одна: заголовок «## v8.4.0» теж
                заголовок версії, а версією документа стає номер без «v».
                Необов'язкове поле `heading` — рівень заголовка версії: web-vitals
                пише «### v6.2.0 (2026-08-24)». Без поля — «##», як і досі.

Навіщо. React Router пише журнал змін так: «## v8.4.0» у кореневому журналі й
журналі гілки v6, а в журналі пакета react-router — упереміш «## v8.4.0» і
«## 6.4.0». Чинний `changelog` заголовка з «v» не впізнає: кореневий журнал для
нього — жодної версії, а журнал пакета втратив би всі записи лінії 8.

Чому копія, а не «v?» у виразі `changelog`: примірники, чиї журнали вже поділено
на документи, звірені, а правка спільного читача — ризик зсуву в готовій роботі.
"""

import re

from engine.readers import Item, _markup, register

_VERSION_HEAD = r"^{level} +v?(\d+\.\d+[\w.-]*)[ \t]*(\([^)\n]*\))?[ \t]*$"


@register("changelog-v")
def changelog_v(source: dict, ctx) -> list[Item]:
    level = source.get("heading", "##")
    if not re.fullmatch(r"#{1,6}", level):
        raise SystemExit(f"{source['id']}: поле heading — від «#» до «######», а не {level!r}.")
    text = ctx.text(source["url"]).replace("\r\n", "\n")
    heads = list(re.finditer(_VERSION_HEAD.format(level=level), text, re.M))
    if not heads:
        raise SystemExit(f"{source['url']}: жодного заголовка версії «{level} vX.Y.Z» — "
                         f"формат змінився, читача треба поправити.")
    cite = source.get("cite", source["url"])
    label = source.get("label", "Changelog")
    items = []
    for i, head in enumerate(heads):
        version = head.group(1)
        heading = head.group(0)[len(level):].strip()
        chunk = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        name = re.sub(r"[^\w.-]+", "-", version)

        def make(chunk=chunk, heading=heading, version=version):
            body = _markup.markdown_body(chunk)
            _markup.require(heading, body, f"{source['url']} {heading}", min_chars=1)
            url = f"{cite}#{_markup.github_anchor(heading)}"
            return _markup.document(f"{label}: {heading}", url, ctx.stamp, body, version)

        items.append(Item(id=f"{source['id']}/{name}",
                          file=f"{source['id']}--{name}.txt", make=make))
    return items
