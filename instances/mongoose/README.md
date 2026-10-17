# mongoose — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Mongoose — ODM для MongoDB у Node.js: схеми й типи, моделі й
документи, запити, валідація, middleware, populate, дискримінатори, транзакції, change streams, TypeScript, переходи
між мажорними версіями; а також про його екосистему: `@nestjs/mongoose`, Typegoose, mongodb-memory-server,
connect-mongo і плагіни mongoose-autopopulate, mongoose-lean-virtuals, mongoose-unique-validator,
mongoose-paginate-v2. Документація — `docs/*.md` кожного стабільного випуску від 5.13.0 до найновішого 9.x, знімки
сайту 3.8.x і 4.x, код `lib/` із JSDoc, типи `types/` і тести кожного випуску, `CHANGELOG.md` від 1.0.1, нотатки
релізів, реєстр npm і README; у додатків — документація, код, релізи й npm кожного випуску. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

mongoosejs.com показує документацію лише поточної мажорної лінії, а проєкти живуть на 6, 7, 8 і 9 водночас; сторінки
«Migrating to X» кажуть, що зламано, але не те, як API виглядав до того, а відповідь на «коли `strictQuery` став
`false` за замовчуванням» — у журналі змін і коді конкретного випуску. Тут кожен випуск — окремою редакцією.
Сервер MongoDB і драйвер під Mongoose — окремі примірники родини (нижче).

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Документація `docs/*.md` 5.13.0–9.x | 875 | 2 153 | `Automattic/mongoose`, 354 теги |
| Сайт 3.8.x і 4.x (знімки) | 42 | 3 406 | mongoosejs.com/docs/3.8.x, /docs/4.x |
| Код `lib/` із JSDoc | 7 509 | 11 846 | `Automattic/mongoose`, 999 тегів 0.0.1–9.x |
| Типи `types/*.d.ts` (від 5.11.0) | 688 | 749 | ті самі, 391 тег |
| Тести `test/` | 4 452 | 19 636 | ті самі, 999 тегів |
| `CHANGELOG.md` (від 1.0.1) і нотатки релізів | 1 269 | 1 308 | ті самі + GitHub Releases |
| `@nestjs/mongoose`: README, код `lib/`, релізи, npm | 210 | 373 | `nestjs/mongoose`, 45 тегів |
| Typegoose: документація (від 8.0.0), код `src/`, релізи, npm | 1 265 | 2 984 | `typegoose/typegoose`, 187 тегів |
| mongodb-memory-server: документація від 7.0.0, код, релізи, npm | 982 | 3 503 | `typegoose/mongodb-memory-server` |
| connect-mongo: README і CHANGELOG, код, релізи, npm | 142 | 517 | `jdesboeufs/connect-mongo`, 40 тегів |
| Плагіни autopopulate, lean-virtuals, unique-validator, paginate-v2 | 272 | 681 | `mongoosejs/*` та інші, 89 тегів |
| Реєстр npm і README `mongoose`, типи `@types/mongoose` (`index.d.ts`) | 352 | 1 002 | registry.npmjs.org |

Разом 18 058 документів; фрагментів — 48 158 (`expected_passages` у `checks.json`). Замір `quality` (10 запитів): по
словах 9, за змістом 9, разом 10.

Лінії документації: 5.13, 6.0–6.13, 7.0–7.8, 8.0–8.23 і далі, 9.x (кожен тег — окрема редакція; сторінки, що не
змінювалися між випусками, зливаються в одну з переліком версій). Сайт 3.8 і 4.13 — одним знімком кожен.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут
  немає: корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `raw/` — сховище сирих відповідей (612 МБ): дерева й файли GitHub, сторінки сайту, tarball npm. Не в git; в архіві
  разом із корпусом.
- `sources.json` — звідки корпус будується (48 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — записи HTTP-серверів усієї родини.

Кроки нижче запускаються з кореня фабрики через `./df mongoose <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| `docs/*.md` Mongoose, README і документація додатків | `ghdocs-history` (кожен тег, однакові редакції зливаються) |
| сайт 3.8.x і 4.x | `html-pages` (знімок; картинки й ресурси відкинуто за `exclude`) |
| код `lib/` Mongoose | `ghcode-history` (з `outline`) |
| типи, тести, код додатків у TS | `ghcode-history-ts` (сигнатури з TSDoc) |
| `CHANGELOG.md` Mongoose | `changelog-slash-dated` — новий: заголовок «9.11.2 / 2026-10-12» з підкресленням «====» |
| нотатки релізів | `ghreleases` (передрелізи відкинуто за `skip`) |
| реєстр npm, README і `index.d.ts` з tarball | `npm-versions`, `npm-tarball-files` (`kind: markdown` / `types`) |

Новий код — лише читач журналу змін (`engine/readers/changelogslash.py`): жоден із наявних читачів журналів не впізнає
заголовка без дужок, тире чи «##».

Особливості:

- **Мітки версій.** Mongoose — повна версія тега (`8.19.3`), лінія в переліку — «X.Y» (`version_line_depth: 2`).
  Додатки — з назвою пакета, щоб нумерації не змішувались: `nestjs-11.0.4`, `typegoose-12.21.1`,
  `memory-server-10.2.3`, `connect-mongo-5.1.0`, `autopopulate-1.2.1`, `lean-virtuals-2.1.0`,
  `unique-validator-6.1.1`, `paginate-1.9.5`, `types-5.11.97`. Сайти — `3.8` і `4.13`.
- **Імена документів.** Документація: `mongoose-docs-guide`, `mongoose-docs-populate`, `mongoose-docs-middleware`,
  `mongoose-docs-typescript-statics`, `mongoose-docs-migrating-to-8`; код: `mongoose-lib-model-js`,
  `mongoose-lib-schema-js`; типи: `mongoose-types-models-d-ts`; тести: `mongoose-test-model-populate-test-js`;
  журнал і релізи: `mongoose-8.0.0`; NestJS: `nestjs-mongoose-readme`,
  `nestjs-mongoose-lib-decorators-prop-decorator-ts`;
  Typegoose: `typegoose-docs-api-decorators-prop`; memory-server: `memory-server-docs-guides-quick-start-guide`.
- **До 5.13 документація була шаблонами jade/pug** і з тегів не читається: за 3.8 і 4.x взято знімки сайту, за
  5.0–5.12 документації немає (код, типи, тести й журнал — є).
- **Версія за замовчуванням** за завантаженнями npm: 8.x (44 %) і 9.x (34 %) — коли версію не названо, відповідь для
  обох.

## Межі, про які треба пам'ятати

- Лише стабільні випуски: rc, alpha, beta не взято ні в код, ні в релізи, ні в npm.
- Сервер MongoDB, mongosh, Database Tools — у примірнику `mongodb`; драйвер — у `node-mongodb`.
- Без README у tarball — `@nestjs/mongoose`, `@typegoose/typegoose` і DefinitelyTyped: для них є документація й код з
  репозиторіїв, для `@types/mongoose` — самі типи. GitHub Releases немає в mongoose-autopopulate і
  mongoose-lean-virtuals — у них журнал змін у `History.md`.
- `mongoose-autopopulate` має лише два теги (1.2.0, 1.2.1): старіші випуски без тегів — у npm (реєстр версій і
  README).

## Родина Mongo: піднімати разом

Цей примірник — частина родини Mongo: сервер, офіційний драйвер Node.js і Mongoose з екосистемою. Питання про
`populate` впирається в `$lookup` сервера, питання про `bufferCommands` — у пул з'єднань драйвера під Mongoose. Тому
примірники родини піднімають у Claude Code разом, а `.mcp.json` цієї теки перелічує всі три сервери: підключивши
будь-який із них, Claude Code бачить решту.

| Примірник | Сервер | Порт | Що |
|-----------|--------|-----:|----|
| `mongodb` | `mongodb-docs` | 8850 | сервер MongoDB 2.2–9.0, mongosh, Database Tools |
| `node-mongodb` | `node-mongodb-docs` | 8851 | офіційний драйвер Node.js (пакет `mongodb`) і `bson` |
| `mongoose` | `mongoose-docs` | 8852 | Mongoose і додатки: `@nestjs/mongoose`, Typegoose, memory-server, плагіни |

`prompts/loaded.txt` каже моделі, що цей набір — частина родини, і які сервери її доповнюють. Повний перелік родин — у
розділі «Родини примірників» кореневого [README](../../README.md).

## Архівний режим: сервер без корпусу

Корпус в архіві від дня збирання: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/mongoose-corpus-2026-10-17.tar.gz` (668 МБ:
18 058 текстів, паспорт і сховище сирого `raw/` — 37 320 файлів; перед
видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на цій машині.

**Як винести** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/mongoose-corpus-РРРР-ММ-ДД.tar.gz -C instances/mongoose corpus raw
find instances/mongoose/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/mongoose/raw
gzip -9 -c instances/mongoose/index/passages.json > instances/mongoose/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/mongoose-corpus-2026-10-17.tar.gz -C instances/mongoose
./df mongoose smoke
```

**Оновлення.** Новий випуск Mongoose чи додатка — новий тег у `tags` відповідних джерел (`mongoose-docs`,
`mongoose-lib`, `mongoose-types`, `mongoose-test`, `typegoose-*`, `memory-server-*`…); npm і релізи підтягуються самі.
Далі `./df mongoose refresh` (~2 год мережею), `manifest`, `vectors` (лише змінені фрагменти), `smoke`, `quality`.

## Установка venv

```
cd instances/mongoose
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df mongoose sources --why   # перелік джерел і білий список
./df mongoose refresh         # завантажити все задеклароване (близько 2 годин)
./df mongoose manifest        # оновити паспорт
./df mongoose setup           # Qdrant чи пошук лише по словах
./df mongoose vectors         # залити корпус у docs-mongoose (близько 2 год 20 хв: 48 тисяч фрагментів)
./df mongoose smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df mongoose serve         # порт 8852
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8852/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user mongoose-docs http://127.0.0.1:8852/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `mongoose-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера.
