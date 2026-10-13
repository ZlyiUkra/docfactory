# Оновлення корпусу prisma

Дві різні роботи: звичайне оновлення, коли вийшли нові стабільні версії Prisma, і збирання з нуля. Порядок усередині
кожної важливіший за самі команди.

Головне правило: **оновлювач тягне лише оголошене.** Дерева й файли репозиторіїв — лише тих комітів і тегів, що
перелічені в полі `tags` джерел, і лише в межах `within`; релізи — лише з адрес джерел `releases` і
`releases-prisma1`; версії — з реєстру npm. Нова версія сама в документацію не потрапить, доки її тег (чи коміт сайту)
не дописано в `tags`.

Друге правило: **лише стабільні версії.** У `tags` — тільки стабільні випуски, без `-dev`, `-integration`, `-preview`
і кандидатів `8.0.0-rc`; поле `skip_versions` джерел `npm-*` і поле `skip` джерел релізів відкидають усе з дефісом.

Третє правило: **версія сайту — стан гілки перед наступною версією.** Сайт (репозиторій prisma/web, гілка `main`)
тегів версій не має. Для кожної стабільної версії в `tags` джерела `site` стоїть повний SHA вершини гілки (за
ланцюжком перших батьків, `git rev-list -1 --first-parent --before=<час> main`) перед публікацією наступної стабільної
версії `@prisma/client` (реєстр npm, поле `time`). Але з 25.08.2026 (коміт `0053ff85`, «promote Prisma ORM 8 and
version Prisma 7 content») сайт описує передреліз Prisma 8, тож межа знімків — останній коміт перед ним, `6083b7a8`:
кожна нова версія 7.x дописується до його ключа. Латка старшої лінії, що вийшла після нового мажора (6.19.1–6.19.3),
дописується до ключа останнього знімка своєї лінії.

Четверте правило: **нова версія змінює й старі документи.** Документ сторінки — неповторна редакція, а в рядку
`# версія:` стоять усі версії, де вона була саме такою. Тож після нових комітів джерела перезаписуються цілком
(`refresh site repo`), а не докачуються (`--missing`).

П'яте правило: **нічого не видаляється.** Ані `refresh`, ані `build`, ані `manifest` нічого не стирають самі;
`vectors` прибирає лише точки власної колекції, чиїх фрагментів у корпусі вже немає. Редакції сторінок, що після
правки читача дістали нове ім'я, і файли, що випали з білого списку (як `docs/plans/` монорепозиторію), лишаються в
`corpus/` — їх переносять убік вручну.

**Спершу — повернути тексти.** Корпус примірника в архіві: у `corpus/` лежить лише паспорт, а `check`, `refresh` і
`manifest` працюють із файлами. Перед будь-якою роботою нижче тексти й сховище сирого розпаковують, а після неї —
пакують і виносять знову; обидві дії описані в [README, розділ «Архівний режим»](README.md#архівний-режим-сервер-без-корпусу).

## 1. Вийшла нова стабільна версія 7.x

**Крок 1. Знайти версію.** Стабільні версії й час публікації — у реєстрі npm
(`https://registry.npmjs.org/@prisma%2Fclient`, поле `time`), теги — на `https://github.com/prisma/orm/tags` (голий
номер: `7.11.0`).

**Крок 2. Сайт.** Поки `main` описує Prisma 8, нова версія 7.x дописується до ключа `6083b7a8…` джерела `site`:
`"6083b7a8f7046c8128ee0f8c4fd6cab0947b6444": "7.11.0, 7.10.0, 7.9.1"`. Сторінки Prisma 7 після переведення живуть у
теках `v7` (`orm/v7`, `cli/v7`, `guides/v7`, `(index)/v7`) і там ще правляться; щоб узяти ці правки, потрібне нове
джерело-знімок цих тек із правилами `slug_rewrite`, що прибирають сегмент `v7`, — окрема робота, не крок оновлення.

**Крок 3. Тег монорепозиторію.** `"7.11.0": "7.11.0"` — на початок поля `tags` джерела `repo`.

**Крок 4. Завантажити.**

```
./df prisma sources --why
./df prisma refresh site repo releases npm-prisma npm-prisma-client npm-prisma-config npm-prisma-adapter-pg npm-prisma-adapter-neon npm-prisma-adapter-planetscale npm-prisma-adapter-libsql npm-prisma-adapter-d1 npm-prisma-adapter-better-sqlite3 npm-prisma-adapter-mariadb npm-prisma-adapter-mssql npm-prisma-adapter-ppg npm-prisma-instrumentation npm-prisma-nextjs-monorepo-workaround-plugin npm-prisma-sqlcommenter-query-tags npm-prisma-sqlcommenter-trace-context npm-prisma-sqlcommenter-query-insights npm-prisma-extension-accelerate npm-prisma-extension-read-replicas npm-prisma-extension-optimize npm-prisma-ppg npm-prisma-studio-core readme-prisma-extension-read-replicas readme-prisma-ppg readme-prisma-studio-core
./df prisma manifest
./df prisma vectors
./df prisma smoke
# Ctrl+C у терміналі з serve, і знову: ./df prisma serve
```

Названий `refresh` інших джерел не чіпає зовсім. Джерела `prisma1`, `releases-prisma1`, `npm-prisma-cli` і
`npm-prisma-adapter-pg-worker` застиглі: репозиторій prisma/prisma1 архівний, `@prisma/cli` з 2.16 не виходить (його
замінив пакет `prisma`), а `@prisma/adapter-pg-worker` — з 6.9.

**Крок 5. Промпти.** Версії за замовчуванням (найпопулярніші за завантаженнями npm:
`https://api.npmjs.org/versions/prisma/last-week`) записано в `prompts/search.txt` (абзац «Every answer says which
version…») і `prompts/agent.txt`; межі версій — ще й у `prompts/loaded.txt` і `prompts/search.txt` («from 2.0.0 to
7.10.0»).

## 2. Вийшов стабільний Prisma 8

Тоді `main` сайту знову описує стабільну версію. Нове джерело `site-8` робиться за зразком `site` з ключами-комітами
`main` для версій 8.x (від виходу 8.0.0), id обох джерел іде в одну родину поля `families` у `config.json`, а з
`exclude` нового джерела прибирається `v8/`, зате додаються теки старих версій (`v7/`, `v6/`). У `slug_rewrite` —
правила, що зводять нові шляхи сторінок до спільного ключа `content-…`; правильність ключів перевіряють в
`index/passages.json`: ключ розділу (`slug` і `section`) мусить бути спільним лише для джерел однієї родини. Нові
компоненти сайту (рядки `<…>` у текстах, `{props.…}`) — правка модуля `engine/readers/_prismamdx.py`; межі версій у
промптах і README — «8».

## 3. Сайт змінив розмітку

Якщо в тексті з'явилися службові рядки MDX (теги компонентів `<…>`, `{props.…}`, рядки `import`), правиться модуль
`engine/readers/_prismamdx.py`. Правка читача не вимагає нового завантаження: `./df prisma build site` збирає тексти
зі сховища сирого. Виняток — вставка файла, якого читач досі не брав: його в сховищі ще немає, тож потрібен `refresh`
джерела.

Якщо сайт знову переніс сторінки, нові пари для `slug_rewrite` виводять так само, як перші: з перенаправлень сайту
(`apps/docs/vercel.json`) і з однакової назви та кінця адреси, а пару лишають лише тоді, коли стара й нова сторінка не
співіснують в одній версії.

Корпус не комітиться: після оновлення пишуть новий архів і знову виносять тексти й сховище (README, розділ «Архівний
режим»), а в git ідуть лише паспорт і кеш. Старий архів видаляють, коли новий звірено з диском.

Якщо `smoke` скаржиться на число фрагментів — це наслідок того, що документація підросла. Нове число записують у
`checks.json` полем `expected_passages`, а в `expected_note` — коли й чому його знято.

## 4. Збирання з нуля

**Крок 1. Токен.** Покладіть `GITHUB_TOKEN=…` у `.env` цієї теки: без нього ~390 дерев ішли б годинними вікнами по 60
звернень.

**Крок 2. Завантаження** окремими процесами — найдовші джерела паралельно, щоб не чекати одне одного:

```
PYTHONUNBUFFERED=1 setsid nohup ./df prisma refresh site > refresh-site.log 2>&1 < /dev/null &
PYTHONUNBUFFERED=1 setsid nohup ./df prisma refresh prisma1 > refresh-prisma1.log 2>&1 < /dev/null &
PYTHONUNBUFFERED=1 setsid nohup ./df prisma refresh <усі інші id з sources.json> > refresh-rest.log 2>&1 < /dev/null &
```

Сайт — близько 1 години 45 хвилин: 192 дерева через API GitHub і кожна неповторна сторінка (9 254) один раз із
raw.githubusercontent.com, з паузою 0,3 с; Prisma 1 — близько 40 хвилин; решта — кілька хвилин. Обірваний прогін
продовжують `./df prisma refresh <джерело, де зупинився>`, далі `refresh --missing`.

**Крок 3.** `manifest`, `vectors` (~2 години на 8 ядрах), `smoke`, `quality`; далі — архів і винесення текстів.

Очікуваних збоїв `refresh` немає.
