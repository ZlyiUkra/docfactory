"""Реєстр читачів: ім'я формату → функція, що дає перелік документів джерела.

Читач приймає джерело (запис `sources.json`) і контекст (звернення крізь білий
список, дата) і повертає список `Item(id, file, make)`. `make()` — відкладене:
воно завантажує й розбирає документ лише тоді, коли оновлювач вирішив його
записати, тож пропущені документи не смикають чужий сервер. Читачі
багатосторінкового джерела (`toc`) і сторінки з розділами (`page`) складають
перелік одразу, бо для цього треба прочитати зміст; тіло глав тягнеться в `make`.

Новий домен додає своїх читачів окремим модулем у цій теці з `@register("ім'я")`;
ядро при цьому не змінюється — модулі теки імпортуються самі, поіменно їх ніде не
вписують. Модуль з іменем на «_» — спільні помічники читачів, не читач.
"""

import collections
import importlib
import pkgutil

Item = collections.namedtuple("Item", "id file make")

REGISTRY: dict = {}


def register(name: str):
    """Декоратор: додає читача в реєстр під іменем формату."""
    def deco(fn):
        REGISTRY[name] = fn
        return fn
    return deco


def get(name: str):
    if name not in REGISTRY:
        raise SystemExit(f"Немає читача «{name}». Є: {', '.join(sorted(REGISTRY))}")
    return REGISTRY[name]


# Імпорт наповнює REGISTRY — кожен модуль реєструє свої читачі. Перелік модулів
# береться з самої теки: раніше його вписували сюди руками, і новий читач
# вимагав правки ядра.
for _module in pkgutil.iter_modules(__path__):
    if not _module.name.startswith("_"):
        importlib.import_module(f"{__name__}.{_module.name}")
