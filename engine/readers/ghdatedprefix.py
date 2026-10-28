"""Читачі з префіксом версії: для пакетів із власною нумерацією в одному примірнику.

`ghsite-dated-prefixed` — те саме, що `ghsite-dated` (знімок репозиторію сайту на кожну версію
                          пакета npm), плюс обов'язкове поле `version_prefix` — рядок перед кожною
                          версією, яку несе документ («router-»), як у `npm-readme` і `npm-versions`.

Навіщо. Сайт docs.solidjs.com тримає в одному репозиторії розділи кількох пакетів, і кожен
розділ знімається на релізи свого пакета: @solidjs/router 0.15 і 1.0, @solidjs/start 1.4 і 2.1.
Без префікса фільтр «1» збирав би разом solid-js 1.x, Router 1.0 і Start 1.x, а фільтр «2» —
SolidStart 2 разом із реліз-кандидатом Solid 2.0. README, реєстр і журнали тих самих пакетів уже
несуть префікс, і розділ сайту мусить нести такий самий, щоб фільтр «router-0.15» бачив усе про
цю версію Router.

`changelog-named-prefixed` — те саме, що `changelog-named` (журнал Changesets, поділений на
                             версії), з тим самим полем `version_prefix`. `changelog-named` поле
                             приймає, але ставить префікс лише на сторінку README з реєстру, а не на
                             версії журналу: журнал @solid-primitives/utils 6.x стояв би в лінії «6»
                             поряд із чужими пакетами, а журнал Router 1.0 — у лінії solid-js 1.
                             Необов'язкове `skip_versions` — вираз версій, записи яких не беруться
                             (`-` — передрелізи): Changesets пише в журнал і alpha, і rc, а
                             `changelog-named` їх не відсіює. З цим полем `version_prefix` може бути
                             порожнім — для пакета, чия нумерація в примірнику головна.

Чому окремий модуль, а не поле в `ghsite-dated`: той читач звірено в готових примірниках, і правка
спільного коду — ризик зсуву в них. Тут лише обгортки: перелік і тексти дає наявний читач, а
обгортка дописує префікс у рядок «# версія:» шапки готового документа.
"""

import re

from engine.readers import Item, register
from engine.readers.ghdated import ghsite_dated
from engine.readers.sentry import sentry_changelog

_VERSION_LINE = re.compile(r"^(# версія: )(.+)$", re.M)


def _prefixed(reader: str, items: list[Item], source: dict) -> list[Item]:
    prefix = str(source.get("version_prefix") or "")
    skip = source.get("skip_versions")
    if not prefix and not skip:
        raise SystemExit(f"{source['id']}: читач {reader} потребує поля version_prefix.")
    if skip:
        # Версія запису — хвіст імені файла після останнього «-»-префікса імені: «…-changelog-2.0.0-rc.5».
        tail = re.compile(r"-(\d+\.\d+\.\d+\S*)\.txt$")
        items = [i for i in items
                 if not ((m := tail.search(i.file)) and re.search(skip, m.group(1)))]

    def wrap(make):
        def prefixed():
            text = make()
            return _VERSION_LINE.sub(
                lambda m: m.group(1) + ", ".join(prefix + v.strip() for v in m.group(2).split(",")),
                text, count=1)
        return prefixed

    return [Item(id=i.id, file=i.file, make=wrap(i.make)) for i in items]


@register("ghsite-dated-prefixed")
def ghsite_dated_prefixed(source: dict, ctx) -> list[Item]:
    return _prefixed("ghsite-dated-prefixed", ghsite_dated(source, ctx), source)


@register("changelog-named-prefixed")
def changelog_named_prefixed(source: dict, ctx) -> list[Item]:
    return _prefixed("changelog-named-prefixed", sentry_changelog(source, ctx), source)
