# bullmq — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про BullMQ — черги задач поверх Redis для Node.js: `Queue.add` і
опції задачі (`delay`, `attempts`, `backoff`, `priority`, `jobId`, `removeOnComplete`), `Worker` і його обробник
(`concurrency`, `lockDuration`, застряглі задачі, `limiter`, sandboxed-процесори), повторювані задачі та планувальники
(`JobScheduler`), потоки батьківських і дочірніх задач (`FlowProducer`), події (`QueueEvents`), дедуплікація,
телеметрія, Lua-скрипти, що рухають задачу між станами, бекенд Postgres у 6.x, BullMQ Pro (групи, пакети,
observables). Поруч — попередник Bull з довідником і типами, панелі Bull Board (з кодом React-інтерфейсу) та Arena,
модулі `@nestjs/bull` і `@nestjs/bullmq`, порти BullMQ на Python, Elixir, Rust, PHP і .NET. Документація — кожного
стабільного випуску: сайт docs.bullmq.io, README, журнали змін, код, тести останнього випуску кожної мінорної лінії,
нотатки релізів GitHub. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

BullMQ міняється щотижня: у 5.x з'явились планувальники задач замість повторюваних, дедуплікація замість debounce,
телеметрія, у 6.x — бекенд Postgres і нові правила для потоків; на проді живуть і Bull 3.x–4.x, і BullMQ 1.x–6.x.
Сайт показує лише поточну редакцію, а довідник API BullMQ — це код з типами. Тут кожен випуск — окремою редакцією:
«які опції `backoff` були в 4.12» чи «що змінилось у `upsertJobScheduler` між 5.20 і 6.0» береться з документів тієї
версії. Сервер Redis (команди, `redis.conf`) — примірник `redis`; клієнти ioredis і node-redis — свої примірники;
глава Queues самого NestJS — примірник `nestjs`.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| BullMQ: сайт docs.bullmq.io (посібник, шаблони, Pro, розділ Bull, порти, журнали змін мажорів), README, CHANGELOG, README портів | 3 564 | 9 143 | `taskforcesh/bullmq`, 788 тегів 1.0.0–6.3.15 |
| BullMQ: код `src/` з Lua-скриптами `commands/` і SQL Postgres | 3 611 | 7 264 | ті самі теги |
| BullMQ: тести `tests/` | 726 | 4 313 | останній випуск кожної з 219 мінорних ліній |
| BullMQ: нотатки релізів | 787 | 1 637 | GitHub Releases 1.0.0–6.3.15 |
| Порти: Python 0.4.3–3.4.0, Elixir 1.0–2.3.1, Rust 1.0–1.3.6, PHP 1.0–2.0.3, .NET 1.0–1.2.2 | 683 | 676 | теги `vpy…`, `vex…`, `vrs…`, `vphp…`, `vnet…` |
| Bull: README, REFERENCE, PATTERNS, MIGRATION, CHANGELOG, `docs/` | 301 | 900 | `OptimalBits/bull`, 168 тегів 0.1.6–4.16.5 |
| Bull: код `lib/`, `index.js`, `index.d.ts` | 511 | 733 | ті самі теги |
| Bull: тести | 206 | 1 626 | останній випуск кожної з 58 мінорних ліній |
| Bull: нотатки релізів | 87 | 177 | GitHub Releases 3.22.2–4.16.5 |
| `@types/bull` (`index.d.ts`) | 77 | 159 | npm 0.7.29–3.15.9 |
| Bull Board: сайт `website/docs`, README, README пакетів і прикладів, CHANGELOG | 599 | 3 866 | `felixmosh/bull-board`, 316 тегів 0.0.6–9.10.4 |
| Bull Board: код пакетів (api, express, fastify, koa, hapi, nestjs, hono, h3, elysia, bun, ui на React) | 1 596 | 3 332 | ті самі теги (код є з 3.0.0) |
| Bull Board: приклади | 129 | 259 | ті самі теги |
| Bull Board: нотатки релізів | 302 | 382 | GitHub Releases 0.0.6–9.10.4 |
| `@nestjs/bull`, `@nestjs/bullmq`: README і код | 316 | 852 | `nestjs/bull`, 67 тегів 0.0.1–12.0.0 |
| Arena: README, CHANGELOG, приклад і код | 387 | 603 | `bee-queue/arena`, 118 тегів 1.0.0–4.10.0 |

Разом 13 882 документи; фрагментів — 35 922 (`expected_passages` у `checks.json`). Замір `quality` (10 запитів):
по словах 10, за змістом 10, разом 10. `max_per_doc` 0 (1–3 дають те саме).

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут
  немає: корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (22 джерела), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями, правила перейменування ключів
  і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — записи HTTP-серверів родини Redis
  для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df bullmq <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| сайт docs.bullmq.io (`docs/gitbook`), README, журнали, сайт Bull Board, README пакетів | `ghdocs-history` |
| код і тести BullMQ, Bull, Bull Board, NestJS-модулів, Arena; приклади Bull Board | `ghcode-history-ts` (розділи — за класами, функціями, типами, `describe`/`it`) |
| код портів Python, Elixir, Rust, PHP, .NET | `ghcode-history` |
| нотатки релізів | `ghreleases` (пре-релізи й теги портів відкинуто за `skip`) |
| `@types/bull` | `npm-tarball-files` |

Нового читача не знадобилось.

Особливості:

- **Імена документів.** Сайт BullMQ — `bullmq-docs-guide-workers-concurrency`, `bullmq-docs-guide-flows-readme`,
  `bullmq-docs-patterns-flows`, `bullmq-docs-bullmq-pro-groups-readme`, `bullmq-docs-changelogs-changelog-v5`; README
  і журнал — `bullmq-readme`, `bullmq-changelog`; код — `src-classes-worker-ts`, `src-commands-movetoactive-11-lua`,
  `src-interfaces-worker-options-ts`; тести — `tests-test-worker-ts`; порти — `python-bullmq-queue-py`,
  `elixir-lib-bullmq-queue-ex`; релізи — `bullmq-v5.34.0`, `bull-v4.16.5`, `bull-board-v9.10.4`. Bull —
  `bull-reference`, `bull-patterns`, `bull-migration`, `bull-src-lib-queue-js`, `bull-tests-test-job-js`,
  `types-bull-types`. Bull Board — `bull-board-docs-server-adapters-express`, `bull-board-docs-queue-adapters-bullmq`,
  `bull-board-packages-express-readme`, `bull-board-src-packages-api-src-queueadapters-bullmq-ts`,
  `bull-board-examples-with-express-index-js`. NestJS — `nestjs-bull-packages-bullmq-readme`,
  `nestjs-bull-src-packages-bullmq-lib-bull-module-ts`; Arena — `arena-readme`, `arena-src-server-app-js`. Подвоєні
  префікси на кшталт `src-src-…` прибирає `slug_rewrite` у `config.json`.
- **Мітки версій — у кожного продукту свої.** Документ BullMQ несе випуски BullMQ, документ Bull — Bull, Bull Board —
  Bull Board, порт — порту, модуль NestJS — `@nestjs/bull*`. Фільтр `version: "5"` лишає все, що позначено 5.x, у
  будь-якому продукті, тож у питанні з версією варто назвати продукт («Bull Board 6 fastify»). Перелік ліній у
  відповіді сервера — мажорний.
- **Де довідник API.** У BullMQ його немає як окремого тексту: розділ `api` сайту — згенерований typedoc, а повна
  правда — код з типами (`src-classes-queue-ts`, `src-classes-worker-ts`, `src-classes-job-ts`,
  `src-interfaces-*-options-ts`) і Lua-скрипти станів. У Bull довідник — `bull-reference` (REFERENCE.md).
- **BullMQ Pro** — лише сторінки сайту (`bullmq-docs-bullmq-pro-*`, журнали змін Pro); коду немає, пакет комерційний.
- **Тести** взято з останнього випуску кожної мінорної лінії, а не з усіх тегів; код і сайт — з усіх.
- **Теги портів** (`vpy3.4.0`, `vex2.3.1`, `vrs1.3.6`, `vphp2.0.3`, `vnet1.2.2`) зведено до версії порту; теги
  NestJS-модулів (`@nestjs/bullmq@12.0.0`) — до версії пакета.

## Межі, про які треба пам'ятати

- Лише стабільні випуски: alpha, beta, rc і next не взято.
- Сервер Redis (команди, `redis.conf`, Sentinel і Cluster зсередини) — примірник `redis`; клієнти — `ioredis` і
  `node-redis`; глава Queues документації NestJS — примірник `nestjs`.
- Інші черги (Bee-Queue, Agenda, RabbitMQ, Kafka, SQS) і панель Taskforce.sh — поза межами.
- `@types/bull` 4.10.x — заглушки без типів, у корпус не потрапили; для Bull 4.x типи вбудовані.

## Родина Redis: піднімати разом

Цей примірник — частина родини Redis: сервер, два клієнти для Node.js і черги поверх них. Питання про чергу
впирається в клієнт (BullMQ працює через ioredis), питання про клієнт — у команду сервера. Тому примірники родини
підіймають у Claude Code разом, а `.mcp.json` цієї теки перелічує всі п'ять серверів: підключивши будь-який із них,
Claude Code бачить решту.

| Примірник | Сервер | Порт | Що |
|-----------|--------|-----:|----|
| `redis` | `redis-docs` | 8845 | сервер Redis: команди, `redis.conf`, збереження, реплікація, Sentinel, Cluster |
| `ioredis` | `ioredis-docs` | 8846 | клієнт ioredis для Node.js |
| `node-redis` | `node-redis-docs` | 8847 | офіційний клієнт node-redis (пакет `redis`) з модулями |
| `bullmq` | `bullmq-docs` | 8848 | черги BullMQ, Bull, панелі Bull Board і Arena, `@nestjs/bull*` |
| `upstash` | `upstash-docs` | 8849 | платформа Upstash: Redis по HTTP, ratelimit, QStash, Workflow, Vector, Search, Box… |

`prompts/loaded.txt` каже моделі, що цей набір — частина родини, і які сервери її доповнюють. Повний перелік родин — у
розділі «Родини примірників» кореневого [README](../../README.md).

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/bullmq-corpus-2026-10-16.tar.gz` (120 МБ: 13 882 тексти, паспорт і
сховище сирого `raw/`; перед видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на цій
машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/bullmq-corpus-РРРР-ММ-ДД.tar.gz -C instances/bullmq corpus raw
find instances/bullmq/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/bullmq/raw
gzip -9 -c instances/bullmq/index/passages.json > instances/bullmq/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/bullmq-corpus-2026-10-16.tar.gz -C instances/bullmq
./df bullmq smoke
```

**Оновлення.** Новий випуск BullMQ дописують першим рядком у `tags` джерел `bullmq-docs` і `bullmq-src`
(«"v6.3.16": "6.3.16"»), а в `bullmq-tests` — заміняють тег своєї мінорної лінії на новіший; так само Bull
(`bull-docs`, `bull-src`, `bull-tests`), Bull Board (`bull-board-docs`, `bull-board-src`, `bull-board-examples`),
NestJS-модулі («"@nestjs/bullmq@12.1.0": "12.1.0"» в обох джерелах `nestjs-bull-*`), Arena (`bull-arena-*`) і порти
(`bullmq-python` тощо, тег порту). Нотатки релізів і нові версії `@types/bull` підхоплюються самі. Далі
`./df bullmq refresh`, `manifest`, `vectors`, `smoke`, `quality`.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df bullmq …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md,
розділ «Спільне середовище». Свій `.env` примірник тримає в `instances/bullmq/.env` (`cp .env.example .env`;
для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`, береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df bullmq sources --why   # перелік джерел і білий список
./df bullmq refresh         # завантажити все задеклароване (близько 1,5 години)
./df bullmq manifest        # оновити паспорт
./df bullmq setup           # Qdrant чи пошук лише по словах
./df bullmq vectors         # залити корпус у docs-bullmq (близько 1 години)
./df bullmq smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df bullmq serve       # порт 8848
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8848/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user bullmq-docs http://127.0.0.1:8848/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `bullmq-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера.
