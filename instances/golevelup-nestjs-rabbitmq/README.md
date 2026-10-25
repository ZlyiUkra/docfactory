# golevelup-nestjs-rabbitmq — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про @golevelup/nestjs-rabbitmq — модуль NestJS для RabbitMQ від
Golevelup на amqplib і amqp-connection-manager (репозиторій golevelup/nestjs, пакет `@golevelup/nestjs-rabbitmq` на
npm) — за сторінкою модуля на сайті, README кожної стабільної версії, журналом змін та історією версій у реєстрі npm.
Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Примірник — четвертий і останній у родині RabbitMQ: сервер окремо (`rabbitmq`), кожен клієнт Node окремо, як у родинах
Redis, Mongo і Kafka (`amqplib`, `amqp-connection-manager`, цей). Менші клієнти — `rabbitmq-client` (близько 61 тисячі
завантажень за тиждень), `@cloudamqp/amqp-client` (48 тисяч), `rascal` (28 тисяч) — не беруться.

Модуль замінює транспорт RabbitMQ з `@nestjs/microservices` для тих, кому потрібні справжні обмінники й ключі
маршрутизації: обробники позначаються декораторами `@RabbitSubscribe` (публікація-підписка) і `@RabbitRPC` (запит-
відповідь), а `AmqpConnection` публікує й робить запити. Близько 135 тисяч завантажень за тиждень до 25.10.2026: лінія 9 —
близько 27 % (найновіша 9.1.1 від 24.10.2026, для NestJS 11 і 12), лінія 5 — близько 25 % (5.7.0), 6.1 — 10 %.

## Скільки цього

| Шар | Документів | Неповторних | Версій | Звідки |
|-----|-----------:|------------:|-------:|--------|
| Сторінка модуля на сайті | 1 | 1 | 9.1.1 | `docs/modules/rabbitmq.md` |
| README пакета, кожен неповторний текст один раз | 27 | 24 | стабільні версії npm 1.6–9.1 | tarball кожної версії |
| Журнал змін | 78 | 78 | 1.x–9.1.1 | `packages/rabbitmq/CHANGELOG.md` |
| Реєстр npm | 10 | 10 | усі | registry.npmjs.org |

Разом 116 документів; фрагментів в індексі — 311 (`expected_passages` у `checks.json`). Замір `quality`: по словах 8 із
10, за змістом 10, разом 10, «як модель» 10 із 10. Сторінка сайту й README 9.1.1 — той самий текст, тож у цілях обидва.

Чому сайт — одна сторінка. Сайт golevelup.github.io/nestjs (VitePress) з'явився недавно, версій не має і описує всі
пакети монорепозиторію; береться лише сторінка модуля RabbitMQ. Документацією давніших версій є їхній README.

Чого немає. Документації NestJS і його транспорту `Transport.RMQ`, amqplib (примірник `amqplib`),
amqp-connection-manager (примірник `amqp-connection-manager`), самого RabbitMQ (примірник `rabbitmq`), інших пакетів
golevelup/nestjs.

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа. Самих
  текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`, розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.mcp.json` — запис HTTP-сервера для Claude Code. `ANTHROPIC_API_KEY` (лише для кроку `ask`) і `GITHUB_TOKEN` (лише
  для завантаження корпусу) беруться з кореневого `.env`.

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df golevelup-nestjs-rabbitmq <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сторінка сайту | `docs/modules/rabbitmq.md` репозиторію golevelup/nestjs на коміті e1130cd0f | `ghdocs-history` |
| README | tarball `@golevelup/nestjs-rabbitmq` кожної стабільної версії | `npm-tarball-files` |
| журнал змін | `packages/rabbitmq/CHANGELOG.md` на master | `changelog-regex` |
| реєстр npm | registry.npmjs.org | `npm-versions` |

Усі читачі вже були у фабриці; нових не додавалося. Журнал змін пише заголовки двома способами — давні записи lerna
(заголовок першого рівня, де номер версії — посилання на порівняння тегів, а за ним дата) і нові changesets
(«## 9.1.1»), тож вираз заголовка в `sources.json` бере обидва.

## Версії

Версія — номер випуску; сторінка сайту — 9.1.1. Фільтр `version` бере мажор (`"5"`), мінор (`"9.1"`) або точну версію
(`"5.7.0"`). Лінії 9 і 5 мають майже порівну завантажень, тож на питання «як це зробити зараз» промпт велить шукати для
обох і казати, де вони різняться. README, що не змінився між версіями, — один документ з усіма ними, тож перелік версій
уривка сам показує, відколи й доки документація казала саме це.

## Родина RabbitMQ: піднімати разом

Цей примірник — частина родини RabbitMQ: сам брокер і три бібліотеки для Node.js. Питання про клієнта впирається в
поведінку брокера (підтвердження, prefetch, dead lettering, типи черг), а питання про модуль NestJS — у те, що роблять
під ним amqplib і amqp-connection-manager. Тому примірники родини піднімають у Claude Code разом, а `.mcp.json` цієї
теки перелічує всі чотири сервери: підключивши будь-який із них, Claude Code бачить решту.

| Примірник | Сервер | Порт | Що |
|-----------|--------|-----:|----|
| `rabbitmq` | `rabbitmq-docs` | 8890 | сам RabbitMQ 3.11–4.4: типи черг, обмінники, підтвердження, кластер, `rabbitmq.conf`, нотатки релізів |
| `amqplib` | `amqplib-docs` | 8891 | клієнт amqplib для Node.js (на ньому транспорт RMQ NestJS) |
| `amqp-connection-manager` | `amqp-connection-manager-docs` | 8892 | перепідключення поверх amqplib, друга половина транспорту RMQ NestJS |
| `golevelup-nestjs-rabbitmq` | `golevelup-nestjs-rabbitmq-docs` | 8893 | модуль NestJS `@golevelup/nestjs-rabbitmq` з `@RabbitSubscribe` і `@RabbitRPC` |

`prompts/loaded.txt` каже моделі, що цей набір — частина родини, і які сервери її доповнюють. Повний перелік родин — у
розділі «Родини примірників» кореневого [README](../../README.md).

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/golevelup-nestjs-rabbitmq-corpus-2026-10-25.tar.gz` (116 текстів, паспорт і сховище
сирого `raw/`; перед видаленням текстів розпакований окремо й звірений із диском) і в копії на Windows-диску
`C:\Distr\golevelup-nestjs-rabbitmq-corpus-2026-10-25.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/golevelup-nestjs-rabbitmq/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/golevelup-nestjs-rabbitmq-corpus-РРРР-ММ-ДД.tar.gz -C instances/golevelup-nestjs-rabbitmq corpus raw
find instances/golevelup-nestjs-rabbitmq/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/golevelup-nestjs-rabbitmq/raw
gzip -9 -c instances/golevelup-nestjs-rabbitmq/index/passages.json > instances/golevelup-nestjs-rabbitmq/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти й сховище — лише після того, як
архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із ними повертається й сховище `raw/`:

```
tar -xzf ~/archives/docfactory/golevelup-nestjs-rabbitmq-corpus-2026-10-25.tar.gz -C instances/golevelup-nestjs-rabbitmq
./df golevelup-nestjs-rabbitmq smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/golevelup-nestjs-rabbitmq/index/passages.json.gz`,
далі `./df golevelup-nestjs-rabbitmq vectors` заллє колекцію Qdrant (секунди на відеокарті, кілька хвилин на процесорі).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df golevelup-nestjs-rabbitmq …` бере спільне середовище з кореня репозиторію (`.venvs/cpu`
або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md, розділ «Спільне
середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df golevelup-nestjs-rabbitmq sources --why   # перелік джерел і білий список
./df golevelup-nestjs-rabbitmq refresh         # завантажити все задеклароване (близько хвилини)
./df golevelup-nestjs-rabbitmq manifest        # оновити паспорт
./df golevelup-nestjs-rabbitmq setup           # Qdrant чи пошук лише по словах
./df golevelup-nestjs-rabbitmq vectors         # залити корпус у docs-golevelup-nestjs-rabbitmq
./df golevelup-nestjs-rabbitmq smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df golevelup-nestjs-rabbitmq serve          # порт 8893
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8893/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user golevelup-nestjs-rabbitmq-docs http://127.0.0.1:8893/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `golevelup-nestjs-rabbitmq-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
