# Оновлення корпусу wordpress

Сайти wordpress.org, реєстри npm і Packagist, Docker Hub живуть нагорі, і `refresh` сам бачить нові сторінки. Перелік тегів
Gutenberg, WP-CLI і ядра, навпаки, записано в `sources.json` на день збирання: нову мінорну версію туди треба дописати.

Правило: **нічого не видаляється.** Ані `refresh`, ані `manifest` нічого не видаляють. `vectors` прибирає лише точки своєї
колекції, чиїх фрагментів у корпусі вже немає.

**Спершу — повернути тексти.** Корпус примірника в архіві, а `check`, `refresh` і `manifest` працюють із файлами. Перед
роботою нижче тексти розпаковують, а після неї виносять знову: обидві дії описані в
[README, розділ «Архівний режим»](README.md#архівний-режим-сервер-без-корпусу).

Довідник коду завантажується близько п'яти годин, тому джерела варто оновлювати блоками:

```
./df wordpress refresh doc-versions dev-notes doc-articles   # нова версія WordPress і її нотатки
./df wordpress refresh h-plugins h-themes h-blocks h-restapi h-apis
./df wordpress refresh ref-classes ref-hooks ref-functions ref-methods   # окремим довгим кроком
./df wordpress manifest
./df wordpress vectors
./df wordpress smoke
# Ctrl+C у терміналі з serve, і знову: ./df wordpress serve
```

Довгі кроки треба запускати через `setsid nohup`, бо фонове завдання обривається приблизно за 30 хвилин.

На що дивитися після оновлення:

- **Нова версія WordPress.** Додати джерела `core-X-Y` і `readme-X-Y` з її тегом, а в `prompts/search.txt` і `prompts/agent.txt`
  замінити чинну лінію.
- **Нова мінорна Gutenberg або тег WP-CLI.** Дописати тег у поле `tags` джерела `gutenberg-docs` або `cli-handbook`.
- **Новий пакет `@wordpress/*`.** Додати джерело `npm-<пакет>` з `version_prefix`, інакше його номери змішаються з номерами WordPress.
- **Codex.** Якщо `codex.wordpress.org` перестане вимагати перевірку браузера, його варто додати читачем `mediawiki`.

Якщо `smoke` скаржиться на число фрагментів, корпус підріс: нове число пишуть у `checks.json`, поле `expected_passages`, а в
`expected_note` — коли й чому його знято.

## Уточнення відповідей після оновлення

Після кожного оновлення корпусу треба виконати `./df wordpress quality --show`, порівняти обидві десятки з попереднім
результатом і записати новий замір у README, розділ «Скільки цього».
