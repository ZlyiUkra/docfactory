# Оновлення корпусу confluent-kafka-javascript

Перелік версій README, властивостей librdkafka і реєстру тут не оголошується руками: читачі беруть його з опису пакета
в реєстрі npm (`https://registry.npmjs.org/@confluentinc%2Fkafka-javascript`), журнал змін — з `CHANGELOG.md` на master,
тож нова версія потрапляє туди сама. Теги репозиторію (об'єкт `tags` джерела `cfk-repo-docs`, ключ — коміт тегу) і
сторінки docs.confluent.io (джерела `cfk-overview-*` і `cfk-migration`) записано в `sources.json` руками.

Правило: **нічого не видаляється.** Ані `refresh`, ані `vectors`, ані `manifest` нічого не стирають самі.

**Спершу — повернути тексти.** Корпус примірника в архіві: у `corpus/` лежить лише паспорт, а `check`, `refresh` і
`manifest` працюють із файлами. Перед роботою нижче тексти розпаковують, а після неї — пакують і виносять знову;
обидві дії описані в [README, розділ «Архівний режим»](README.md#архівний-режим-сервер-без-корпусу).

## Вийшла нова версія

```
./df confluent-kafka-javascript check                 # чи змінилося щось нагорі за джерелом
./df confluent-kafka-javascript refresh               # повне перезавантаження, близько двох хвилин
./df confluent-kafka-javascript manifest
./df confluent-kafka-javascript vectors
./df confluent-kafka-javascript smoke
# Ctrl+C у терміналі з serve, і знову: ./df confluent-kafka-javascript serve
```

`refresh` повний, не `--missing`: у документі стоять усі версії, де текст був таким, тож нова версія змінює й старі
документи.

Нова мінорна версія (1.12):

- тег репозиторію: в об'єкт `tags` джерела `cfk-repo-docs` дописують коміт тегу `v1.12.Z` з версією `1.12.Z`, а для нової
  латки тієї самої мінорної — замінюють коміт старої латки новим. Коміт тегу дає
  `https://api.github.com/repos/confluentinc/confluent-kafka-javascript/git/refs/tags/v1.12.0`. Передрелізи (`-rc`,
  `-alpha`, `-dev`) і тег `v2.16.0` (спадок node-rdkafka) не беруться;
- сайт: сторінки `https://docs.confluent.io/kafka-clients/javascript/1.12/overview.md` і `migration.md` звіряють із
  попередньою версією. Текст той самий — нову версію дописують у поле `version` відповідного джерела; новий текст —
  нове джерело `cfk-overview-1.12` за зразком `cfk-overview-1.11`, його id — у родину `cfk-site-overview` поля
  `families` у `config.json`.

Якщо зміниться версія, яку завантажують найбільше, — у `prompts/search.txt` (абзац «Which version to search first») і
`prompts/agent.txt` замінити її, звіривши з `https://api.npmjs.org/versions/@confluentinc%2Fkafka-javascript/last-week`;
на 25.10.2026 найбільше мала 1.10.0 (близько 22 %, лінія 1.10 — 31 %).

Якщо `smoke` скаржиться на число фрагментів — корпус підріс; нове число записують у `checks.json` полем
`expected_passages`, а в `expected_note` — коли й чому його знято.

Токен GitHub (`GITHUB_TOKEN` у кореневому `.env`) потрібен: дерев тегів 15, а без токена GitHub дає 60 звернень на
годину.

## Уточнення відповідей після оновлення

Після кожного оновлення корпусу — цикл із [кроку 7 загального довідника](../../UPDATE.md#крок-7--відновити-уточнення-відповідей):
`./df confluent-kafka-javascript quality --show`, порівняння обох десяток з попереднім результатом, розбір промахів,
правка промпту, знову замір. Останній результат — у README, розділ «Скільки цього».
