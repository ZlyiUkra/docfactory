"""Маскування рядків, схожих на секрети, у тексті документа.

Документація любить показувати ключі й токени «як є» — заглушками на кшталт
`xoxb-0000000000-…nacho…`. Для сканера секретів GitHub така заглушка невідрізненна
від справжнього токена Slack, і push корпусу блокується. Тут кожен документ перед
записом проходить через правила примірника: поле `redact` у config.json — перелік
`{"pattern": регулярний вираз, "with": заміна}`. Заміна — та сама заглушка скрізь,
щоб текст і далі казав, що тут стоїть токен такого-то продукту, а рядка у форматі
справжнього токена в корпусі не було.

Застосовується до готового тексту документа — після читача, перед записом — і так
само в `check`, щоб сума тексту збігалася з паспортом. Без поля правил немає, і
текст лишається тим, що віддав читач: примірник без `redact` не змінюється.
"""

import json
import re


def rules(instance_dir) -> list:
    """Правила з поля `redact` у config.json примірника: список пар (вираз, заміна).
    Без поля — порожній список. Хибне правило зупиняє прогін одразу, а не мовчки
    пропускає маскування."""
    path = instance_dir / "config.json"
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8")).get("redact")
    except (OSError, ValueError) as exc:
        raise SystemExit(f"{path}: не читається ({exc})")
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise SystemExit(f"{path}: поле redact мусить бути списком правил.")
    out = []
    for rule in raw:
        if (not isinstance(rule, dict) or not isinstance(rule.get("pattern"), str)
                or not isinstance(rule.get("with"), str)):
            raise SystemExit(f"{path}: правило redact мусить мати рядки `pattern` і "
                             f"`with`: {rule!r}")
        try:
            out.append((re.compile(rule["pattern"]), rule["with"]))
        except re.error as exc:
            raise SystemExit(f"{path}: redact — вираз {rule['pattern']!r} не "
                             f"розбирається: {exc}")
    return out


def apply(text: str, rules: list) -> str:
    """Текст із заміненими збігами. Заміна підставляється як є, без розбору
    зворотних рис — заглушка в конфігу пишеться буквально."""
    for pattern, replacement in rules:
        text = pattern.sub(lambda m: replacement, text)
    return text
