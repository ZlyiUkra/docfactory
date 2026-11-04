# Оновлення корпусу mariadb

Репозиторій `mariadb-docs` змінюється майже щодня, а завантажувач тягне з нього лише те, що оголошено в `sources.json`.

Правило: **нічого не видаляється.** Лише `vectors` прибирає точки своєї колекції, чиїх фрагментів уже немає в корпусі.

Спершу поверніть тексти за [README, розділ «Архівний режим»](README.md#архівний-режим). Великі джерела завантажуйте окремими
процесами, бо так удвічі швидше:

```
./df mariadb refresh server
./df mariadb refresh release-notes
./df mariadb refresh connectors galera maxscale tools columnstore get-started general
./df mariadb refresh server-releases docker-hub docker-docs npm-mariadb readme-mariadb
./df mariadb manifest
./df mariadb vectors
./df mariadb smoke
./df mariadb quality
```

Запишіть нове число фрагментів у `checks.json`, зробіть новий архів, звірте його з диском і оновіть імена в README. Лише тоді
видаляйте тексти з теки та попередній архів.
