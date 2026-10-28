"""Читач `ghsite-dated` з префіксом версії: для пакетів із власною нумерацією в одному примірнику.

`ghsite-dated-prefixed` — те саме, що `ghsite-dated` (знімок репозиторію сайту на кожну версію
                          пакета npm), плюс обов'язкове поле `version_prefix` — рядок перед кожною
                          версією, яку несе документ («router-»), як у `npm-readme` і `npm-versions`.

Навіщо. Сайт docs.solidjs.com тримає в одному репозиторії розділи кількох пакетів, і кожен
розділ знімається на релізи свого пакета: @solidjs/router 0.15 і 1.0, @solidjs/start 1.4 і 2.1.
Без префікса фільтр «1» збирав би разом solid-js 1.x, Router 1.0 і Start 1.x, а фільтр «2» —
SolidStart 2 разом із реліз-кандидатом Solid 2.0. README, реєстр і журнали тих самих пакетів уже
несуть префікс, і розділ сайту мусить нести такий самий, щоб фільтр «router-0.15» бачив усе про
цю версію Router.

Чому окремий модуль, а не поле в `ghsite-dated`: той читач звірено в готових примірниках, і правка
спільного коду — ризик зсуву в них. Тут лише обгортка: перелік і тексти дає `ghsite-dated`, а
обгортка дописує префікс у рядок «# версія:» шапки готового документа.
"""

import re

from engine.readers import Item, register
from engine.readers.ghdated import ghsite_dated

_VERSION_LINE = re.compile(r"^(# версія: )(.+)$", re.M)


@register("ghsite-dated-prefixed")
def ghsite_dated_prefixed(source: dict, ctx) -> list[Item]:
    prefix = str(source.get("version_prefix") or "")
    if not prefix:
        raise SystemExit(f"{source['id']}: читач ghsite-dated-prefixed потребує поля version_prefix.")

    def wrap(make):
        def prefixed():
            text = make()
            return _VERSION_LINE.sub(
                lambda m: m.group(1) + ", ".join(prefix + v.strip() for v in m.group(2).split(",")),
                text, count=1)
        return prefixed

    return [Item(id=i.id, file=i.file, make=wrap(i.make)) for i in ghsite_dated(source, ctx)]
