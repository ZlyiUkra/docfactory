# Оновлення корпусу mysql

Нова версія посібника MySQL не приходить сама. Завантажувач не може звертатися до сайтів MySQL, тому людина завантажує файли
браузером.

Правило: **нічого не видаляється.** Лише `vectors` прибирає точки своєї колекції, чиїх фрагментів уже немає в корпусі.

1. Поверніть тексти за [README, розділ «Корпус лише локально»](README.md#корпус-лише-локально).
2. Завантажте браузером новий файл, наприклад `https://downloads.mysql.com/docs/mysql-8.4.info.zip`, і покладіть його в
   `instances/mysql/raw/local/`. Нову лінію довідника допишіть у `sources.json` і в поле `families` файлу `config.json`.
3. Оновіть примірник:

```
./df mysql refresh refman-8.4
./df mysql refresh npm-mysql2 readme-mysql2 mysql2-docs mysql2-releases docker-hub docker-docs
./df mysql manifest
./df mysql vectors
./df mysql smoke
./df mysql quality
```

4. Запишіть нове число фрагментів у `checks.json`, зробіть новий архів і звірте його з диском. Лише тоді видаляйте тексти з теки
   та попередній архів.

Джерела довідників позначено `frozen`, тому `refresh` без імен їх не чіпає.
