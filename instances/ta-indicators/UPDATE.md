# Оновлення корпусу ta-indicators

Корпус живе нагорі: репозиторії `TA-Lib/ta-lib`, `TA-Lib/ta-lib-python`, `xgboosted/pandas-ta-classic`, `bukosabino/ta` і реєстр
PyPI. Теги вже вийшлих версій не змінюються, а нова мінорна лінія потребує правки `sources.json`.

Правило: **нічого не видаляється.** Ані `refresh`, ані `manifest` нічого не видаляють. Лише `vectors` прибирає точки своєї колекції,
чиїх фрагментів у корпусі вже немає.

**Спершу — повернути тексти.** Корпус примірника в архіві, а `check`, `refresh` і `manifest` читають файли. Тому перед роботою нижче
тексти розпаковують, а після неї виносять знову: обидві дії описано в
[README, розділ «Архівний режим»](README.md#архівний-режим-сервер-без-корпусу).

```
./df ta-indicators refresh <id джерела>   # лише те, що змінилося
./df ta-indicators manifest
./df ta-indicators vectors
./df ta-indicators smoke
# Ctrl+C у терміналі з serve, і знову: ./df ta-indicators serve
```

## Дозбирати записи PyPI

13.11.2026 записи PyPI не склалися: pypi.org з WSL відповідав лише на половину з'єднань, а читач `pypi-versions` звертається до
реєстру по разу на кожну версію, тож один збій зупиняв увесь перелік. Коли мережа відновиться (перевірка: кілька разів поспіль
`curl -s -o /dev/null -w "%{http_code}\n" https://pypi.org/pypi/ta/json` дають `200` без затримки), поверніть тексти й виконайте:

```
./df ta-indicators refresh talib-python-pypi pandas-ta-classic-pypi pandas-ta-pypi ta-pypi
./df ta-indicators manifest
./df ta-indicators vectors
./df ta-indicators smoke    # нове число фрагментів записати в checks.json
./df ta-indicators quality
```

Після цього зробіть новий архів за README і приберіть рядок «Чого ще немає» з README.

## Що міняти, коли вийшла нова лінія

- **Сайт ta-lib.org:** замінити тег у полі `tags` джерела `talib-site` на новий. Сайт не тримає старих ліній, тому лишається один тег.
  Тег у адресах `talib-changelog` теж міняється на новий.
- **Обгортка для Python і pandas-ta-classic:** дописати новий тег у поле `tags` джерел `talib-python-docs`, `pandas-ta-classic-docs` і
  `pandas-ta-classic-code`, найновіший першим; у журналах змін замінити тег в адресі.
- **ta:** дописати тег у `ta-code` і `ta-docs`, а в `ta-release` замінити тег на новий.
- Релізи GitHub і PyPI підтягуються самі.

Якщо `smoke` скаржиться на число фрагментів, корпус підріс: нове число записують в `expected_passages`, а в `expected_note` — коли й
чому його знято.

## Уточнення відповідей після оновлення

Після кожного оновлення корпусу треба виконати `./df ta-indicators quality --show`, переглянути запити зі знаком «-» і перевірити,
чи справді відповідь змінилася. Ціль розширюють лише тоді, коли знайдена сторінка справді відповідає на запит.
