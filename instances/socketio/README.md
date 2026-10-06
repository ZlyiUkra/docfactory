# socketio — примірник фабрики docfactory

Тридцять третій примірник фабрики: захищений MCP-сервер, що відповідає на питання про Socket.IO — бібліотеку
двобічного обміну подіями в реальному часі між сервером Node.js і клієнтом: події й підтвердження, кімнати й простори
імен, middleware і автентифікація, відновлення з'єднання, кілька серверів через адаптери. Тут сайт socket.io для 4.x,
3.x і 2.x, посібники Get started і How-to, сторінки змін і блог, журнали змін і README пакетів монорепозиторію,
специфікації протоколів, README прикладів, адаптери Redis, Redis Streams, Postgres і MongoDB, Admin UI, README кожної
стабільної версії `socket.io` і `socket.io-client`, нотатки релізів і реєстр npm. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо

Socket.IO — живі дані планів NestJS (уся фаза 7: шлюзи `@nestjs/websockets`, кімнати, адаптер Redis) і Next.js (клієнт
у фазі 8). Між мажорами змінилося те, на чому тримається робочий код: у 3.0 — CORS став явним, `io.origins` і
`socket.rooms` як об'єкт прибрано, у 4.x додалися `emitWithAck`, таймаути, відновлення стану з'єднання і нові
адаптери. На день збирання на 4.x припадає 92% завантажень пакета `socket.io`, тому відповідь без названої версії — для
4, а 3 і 2 згадуються лише тоді, коли їх назвав користувач.

У яких фазах і днях планів навчання він потрібен — див. [../../docs/learning-map.md](../../docs/learning-map.md).

## Скільки цього

| Шар | Документів | Звідки |
|-----|-----------:|--------|
| Сайт для 4.x: документація, підручник, API й опції сервера й клієнта, шпаргалка `emit` | 67 | `docs/` socketio/socket.io-website |
| Сайт для 3.x | 31 | `versioned_docs/version-3.x` |
| Сайт для 2.x | 16 | `versioned_docs/version-2.x` |
| Get started, How-to (JWT, express-session, Passport, React, Next.js…), демо | 35 | `src/pages` |
| Сторінки змін релізів 4.5–4.8 і 2.5 | 21 | `docs/changelog` |
| Блог: релізи, міграції, нові адаптери | 42 | `blog/` |
| CHANGELOG пакетів монорепозиторію | 12 | `packages/*/CHANGELOG.md` socketio/socket.io |
| README внутрішніх пакетів: engine.io, парсери, адаптер у пам'яті, кластерні адаптер і рушій, емітери | 10 | `packages/*` |
| Специфікації протоколів Engine.IO (v3, v4) і Socket.IO (v3–v5) | 5 | `docs/*-protocol` |
| README прикладів: кластери за nginx, HAProxy, Traefik; NestJS, Next.js, Passport, JWT… | 32 | `examples/` |
| README `socket.io`: 151 стабільна версія, однакові тексти зведено | 46 | коміт публікації чи тег |
| README `socket.io-client`: 120 стабільних версій | 29 | монорепозиторій або socketio/socket.io-client |
| Адаптери Redis, Redis Streams, Postgres, MongoDB і Admin UI: README кожної версії й CHANGELOG | 31 | їхні репозиторії |
| Реєстр версій npm `socket.io` і `socket.io-client` | 12 | registry.npmjs.org |
| Нотатки релізів socketio/socket.io і socketio/socket.io-client | 164 | GitHub API |

Разом 553 документи; фрагментів в індексі — 3 753 (`expected_passages` у `checks.json`). Фрагменти — це шматки
документів між заголовками, по яких іде пошук; однаковий текст різних версій зливається в один з усіма версіями.

Замір `quality` на першому корпусі: перша десятка (питання своїми словами) — по словах 6 із 10, за змістом 9, разом
8; друга, «як модель» (назви API, з версією «4», як велить промпт), — 10 із 10.

**Версія у відповіді.** Без названої версії — Socket.IO 4. Фільтр `version` — мажор: «4», «3», «2». Сторінки змін і
журнали змін мають мітку «changelog», блог — «blog», протоколи — «protocol». README пакетів і нотатки релізів несуть
версію самого пакета: адаптери, Admin UI і engine.io мають власну нумерацію.

## Що в цій теці

- `corpus/` — лише паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа (тексти — в архіві,
  див. нижче).
- `index/passages.json.gz` — стиснений кеш фрагментів, з якого підіймається сервер.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — ключ Anthropic (лише для кроку `ask`) і токен GitHub (лише для завантаження); `.mcp.json` — запис
  HTTP-сервера для Claude Code.
- `.venv/` — власний venv примірника; `requirements.txt` — його склад.

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df socketio <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт для 4.x, 3.x, 2.x, посібники, сторінки змін, блог | socketio/socket.io-website, гілка main | `ghdocs-history` |
| журнали змін, README пакетів, протоколи, приклади | socketio/socket.io, гілка main | `ghdocs-history` |
| журнали змін адаптерів і Admin UI | їхні репозиторії, гілка main (Admin UI — develop) | `ghdocs-history` |
| README кожної версії | коміт публікації з реєстру npm, інакше тег | `npm-readme` |
| нотатки релізів | GitHub API | `ghreleases` |
| версії пакетів | реєстр npm | `npm-versions` |

Білий список — три хости: `api.github.com`, `raw.githubusercontent.com`, `registry.npmjs.org`. Сам socket.io не
читається: сайт збирається з репозиторію socketio/socket.io-website. Посилання у відповідях можуть вести на сайт.

Особливості, які варто знати:

- **Сайт на Docusaurus** збирає і `.md` як MDX: сторінки з вкладками починаються з `import Tabs from '@theme/Tabs'`.
  Для джерел сайту ввімкнено поле `mdx` читача `ghdocs-history` — імпорти й експорти верхнього рівня викидаються, а в
  прикладах коду лишаються. Вкладки «CommonJS / ES modules / TypeScript» стають кількома блоками коду поспіль.
- **Монорепозиторій.** З 2024 року сервер, клієнт, engine.io й парсери живуть у socketio/socket.io, а теги релізів
  мають вигляд `socket.io@4.8.1`, `@socket.io/cluster-adapter@0.3.0`; читач `ghreleases` бере версію і з таких тегів.
  Клієнт до переїзду жив у socketio/socket.io-client — його README й релізи читаються звідти.
- **Чотири найстаріші версії** `socket.io` (0.4.0, 0.6.18, 0.9.6, 0.9.16) без README: ні за комітом публікації, ні за
  тегом файла немає.
- **Переклади сайту** (іспанський, французький, португальський, китайський) не взято: лише англійська.

## Межі, про які треба пам'ятати

Тут немає документації самого Node.js, браузерного WebSocket API і пакета `ws` (вебплатформа — примірники `mdn` і
`webstandards`), Redis, PostgreSQL і MongoDB як таких (PostgreSQL — окремий примірник `postgresql`), NestJS (примірник
`nestjs`, глави `@nestjs/websockets`), клієнтів іншими мовами (Java, Swift, C++, Python) і адаптерів хмар поза сайтом
(AWS SQS, Azure Service Bus, Google Pub/Sub описані лише сторінками сайту). Issues і GitHub Discussions свідомо не взято.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку, як у express: у `corpus/` лежить лише паспорт `index.json`, а сервер
підіймається з кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає
повний текст кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/socketio-corpus-2026-10-06.tar.gz` (0,5 МБ, 553 тексти й паспорт; перед
видаленням розпакований окремо й звірений із диском — нуль розбіжностей). В історії git текстів немає ніде. Архів
лежить лише на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/socketio/index/passages.json        # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/socketio-corpus-РРРР-ММ-ДД.tar.gz -C instances/socketio corpus
find instances/socketio/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/socketio/index/passages.json > instances/socketio/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/socketio-corpus-РРРР-ММ-ДД.tar.gz -C instances/socketio
./df socketio smoke
```

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/socketio/index/passages.json.gz`, далі
`./df socketio vectors` заллє колекцію Qdrant (кілька хвилин).

## Установка venv

```
cd instances/socketio
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df socketio sources --why   # перелік джерел і білий список
./df socketio refresh         # завантажити все задеклароване (~40 хвилин)
./df socketio manifest        # оновити паспорт
./df socketio setup           # Qdrant чи пошук лише по словах
./df socketio vectors         # залити корпус у docs-socketio (кілька хвилин)
./df socketio smoke           # перевірки
```

Найдовша частина `refresh` — README: реєстр npm віддає текст лише найновішої версії, тож кожна з 151 версії
`socket.io` і 120 версій `socket.io-client` читається окремо. Без `GITHUB_TOKEN` у `.env` анонімного ліміту GitHub API
(60 звернень на годину) не вистачить на релізи. Обірваний `refresh` продовжується з `--missing`.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd /mnt/c/Projects/fwdays/docfactory
./df socketio serve           # порт 8793
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8793/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user socketio-docs http://127.0.0.1:8793/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `socketio-docs` і два інструменти `search_docs`, `read_section`. Якщо сесію Claude
Code відкрито раніше, ніж піднято сервер, вона покаже його як недоступний: у `/mcp` виберіть сервер і «Reconnect».

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
