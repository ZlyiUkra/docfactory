"""Читач релізів GitHub для репозиторію, що пише версію в тегу без крапок.

`ghreleases-tag-version` — те саме, що `ghreleases` (поля `url`, `label`, `skip`, `stable`,
                           `name_prefix`, `version_prefix`), і ще одне:
                           `tag_version` — пара [вираз, заміна]: тег, що збігся з виразом,
                           дає версію документа заміною (`re.sub`); решта тегів лишає ту
                           версію, яку визначив `ghreleases`.

Навіщо. Fabric.js від 3.6.3 називає теги трьома цифрами поспіль: `v740` — це 7.4.0, `v552` —
5.5.2, `v542b` — 5.4.2. Спільний читач бачить у тезі `v740` одне число й пише версію «740», а
в `v542b` версії не бачить зовсім. Пошук з обмеженням версії шукає лінію за першим числом:
нотатки до 7.4.0 потрапили б у «лінію 740», якої ніхто не спитає, а запит з версією «7» їх би
не знайшов. З парою ["^v(\\d)(\\d)(\\d)[a-z]?$", "\\1.\\2.\\3"] ті самі нотатки несуть 7.4.0.

Ім'я файла, заголовок і рядок «Tag v740, published …» у тілі лишаються як є: тег справді
такий, і адреса релізу на GitHub містить саме його. Міняється лише рядок версії в шапці.

Чому окремий модуль, а не поле в `ghreleases`: примірники з тим читачем зібрані й звірені, а
правка спільного читача — ризик зсуву в готовій роботі. Перелік релізів і текст документа
складає він сам, тут лише обгортка над готовим документом.
"""

import re

from engine.readers import Item, register
from engine.readers.github import ghreleases

_TAG = re.compile(r"^Tag (\S+), published ", re.M)
_VERSION = re.compile(r"^# версія: .*\n", re.M)


def _relabel(text: str, pattern, repl: str, prefix: str) -> str:
    """Шапка документа з версією, виведеною з тегу; документ без збігу повертається як був."""
    head, sep, body = text.partition("\n\n")
    tag = _TAG.search(body)
    if not sep or not tag or not pattern.search(tag.group(1)):
        return text
    version = prefix + pattern.sub(repl, tag.group(1))
    head = _VERSION.sub("", head + "\n").rstrip("\n")
    return f"{head}\n# версія: {version}\n\n{body}"


@register("ghreleases-tag-version")
def ghreleases_tag_version(source: dict, ctx) -> list:
    pair = source.get("tag_version")
    if not (isinstance(pair, list) and len(pair) == 2):
        raise SystemExit(f"{source['id']}: читач ghreleases-tag-version вимагає поле `tag_version` — "
                         f"пару [вираз, заміна].")
    pattern, repl = re.compile(pair[0]), pair[1]
    prefix = str(source.get("version_prefix") or "")
    return [Item(id=item.id, file=item.file,
                 make=lambda make=item.make: _relabel(make(), pattern, repl, prefix))
            for item in ghreleases(source, ctx)]
