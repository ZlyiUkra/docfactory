# Оновлення корпусу php

Посібник PHP оновлюється на php.net часто, тому `refresh manual` щоразу бере новий архів. Новий випуск PHP чи Composer оновлюється
вручну: у `sources.json` треба додати його останній патч до поля `tags`, бо перелік тегів там записаний явно. Нові RFC читач бере зі
сторінки-змісту сам.

Правило: **нічого не видаляється.** Лише `vectors` прибирає точки своєї колекції, чиїх фрагментів у корпусі вже немає.

**Спершу — повернути тексти** за [README, розділ «Архівний режим»](README.md#архівний-режим-сервер-без-корпусу).

```
./df php refresh manual                # архів посібника, близько хвилини
./df php refresh php-src
./df php refresh composer
./df php refresh composer-news
./df php refresh rfc                   # близько 960 сторінок, близько 6 хвилин
./df php refresh site
./df php refresh packagist
./df php refresh packagist-composer
./df php manifest
./df php vectors
./df php smoke
./df php quality
```

Коли `refresh` повідомляє про порожню сторінку посібника, її назву треба додати до поля `exclude` джерела `manual`.
