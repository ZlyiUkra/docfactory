# node-mongodb — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про офіційний драйвер MongoDB для Node.js (пакет `mongodb`) і
бібліотеку `bson`: підключення й пул, CRUD, агрегація, транзакції, change streams, GridFS, індекси, типізація у
TypeScript, шифрування полів, перехід між мажорними версіями. Документація — кожної мінорної лінії драйвера від 3.6 до
7.7 у тому вигляді, якою вона була для тієї лінії; код `src/` із TSDoc і `lib/` із JSDoc, тести integration і unit,
журнал `HISTORY.md` і нотатки релізів кожного стабільного випуску; реєстр npm і README семи пакетів. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

mongodb.com показує документацію драйвера лише для поточної й попередньої мажорної лінії, а в проєктах живуть 4.x,
5.x і 6.x разом; сторінка «Upgrade» каже, що зламано, але не те, як API виглядав до того. Тут кожна мінорна — окремою
редакцією, а код і тести кожного випуску дають відповідь на «коли з'явився `maxPoolSize` за замовчуванням 100» по
першоджерелу. Сервер, mongosh і Mongoose — окремі примірники родини (нижче).

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Документація 7.7 і 6.21 (монорепозиторій, `content/node/`) | 146 | 822 | `mongodb/docs`, гілка `main` |
| Документація 3.6–6.17 (гілка кожної мінорної) | 3 950 | 1 962 | `mongodb/docs-node`, 48 гілок |
| Код `src/` (TypeScript із TSDoc) | 2 026 | 8 153 | `mongodb/node-mongodb-native`, 84 теги v4.0.0–v7.7.0 |
| Код `lib/` (JavaScript із JSDoc) | 2 435 | 4 087 | ті самі, 338 тегів 0.6.8–3.7.4 |
| Тести `test/integration`, `test/unit` | 2 118 | 10 936 | ті самі, 84 теги v4.0.0–v7.7.0 |
| `HISTORY.md` (3.0.0–7.7.0) і нотатки релізів | 228 | 1 102 | ті самі + GitHub Releases |
| Код `src/` бібліотеки bson | 651 | 1 567 | `mongodb/js-bson`, 155 тегів 0.0.5–7.3.3 |
| `HISTORY.md` і релізи bson | 122 | 438 | ті самі + GitHub Releases |
| Типи `@types/mongodb` (`index.d.ts`) | 177 | 1 404 | npm, 191 версія, 177 неповторних |
| Реєстр npm і README семи пакетів (`mongodb`, `bson`, `mongodb-legacy`, …) | 177 | 815 | registry.npmjs.org |

Разом 12 030 документів; фрагментів — 31 286 (`expected_passages` у `checks.json`). Замір `quality` (10 запитів): по
словах 8, за змістом 10, разом 10.

Лінії документації: 3.6, 3.7, 4.0–4.17, 5.0–5.9, 6.0–6.17 (гілки), 6.21 і 7.7 (монорепозиторій). У гілках 3.6–6.17
сторінки, що не змінювалися між лініями, зливаються в одну редакцію з переліком версій.

## Що в цій теці

- `corpus/` — тексти документів (поки корпус не винесено в архів) і паспорт `index.json`: адреса, дата завантаження
  й сума тексту кожного документа.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `raw/` — сховище сирих відповідей (283 МБ): дерева й файли GitHub, tarball npm. Не в git; в архів разом із корпусом.
- `sources.json` — звідки корпус будується (23 джерела), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену й родина джерел `docs`.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — записи HTTP-серверів усієї родини.

Кроки нижче запускаються з кореня фабрики через `./df node-mongodb <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| документація (Snooty rST, як і посібник сервера) | `snooty-history` (той самий, що у примірнику `mongodb`) |
| код `src/`, тести, bson, типи у TS | `ghcode-history-ts` (сигнатури з TSDoc) |
| код `lib/` 0.x–3.x | `ghcode-history` (з `outline`) |
| `HISTORY.md` обох репозиторіїв | `changelog-conventional` |
| нотатки релізів | `ghreleases-stable` (передрелізи відкинуто) |
| реєстр npm, README і `index.d.ts` з tarball | `npm-versions`, `npm-tarball-files` (`kind: markdown` / `types`) |

Нового коду для драйвера не знадобилось: читач Snooty написано для посібника сервера.

Особливості:

- **Мітки версій.** Документація — лінія «X.Y» (`version_line_depth: 2`); код, тести й журнали — повна версія тега
  (`6.17.0`); bson — із префіксом `bson-` (`bson-6.10.4`), пакети npm — із назвою пакета (`kerberos-2.2.2`,
  `types-5.11.97`), щоб нумерації не змішувались у фільтрі версії.
- **Імена документів.** Документація: `connect-mongoclient`, `crud-insert`, `crud-transactions`,
  `monitoring-and-logging-change-streams`, `typescript`, `reference-upgrade` (монорепозиторій) і
  `fundamentals-crud-write-operations-insert`, `usage-examples-changestream` (гілки). Код:
  `mongodb-src-collection-ts`, `mongodb-src-change-stream-ts`, `mongodb-lib-collection-js`; тести:
  `mongodb-test-test-integration-crud-…`;
  журнал: `mongodb-6.0.0`, `bson-6.0.0`; README: `mongodb-markdown-<хеш>`, типи: `types-mongodb-types-<хеш>`.
- **Два покоління документації.** До 6.17 сайт драйвера жив у `docs-node` (`fundamentals/…`, `usage-examples/…`),
  з 6.21 — у монорепозиторії `docs` з іншим деревом (`connect/…`, `crud/…`); одна й та сама тема має два імені, обидва
  видно поруч. Родина `docs` у `config.json` об'єднує їх у версіях.
- **Приклади CRUD**, яких немає в репозиторії документації сервера (`driver-examples/*.js`), тут є — у тестах
  драйвера (`test/integration/node-specific/examples/…`).

## Межі, про які треба пам'ятати

- Лише стабільні випуски: alpha, beta, rc не взято ні в код, ні в релізи, ні в npm.
- Сервер, mongosh, Database Tools — у примірнику `mongodb`; Mongoose — у `mongoose`.
- `@mongodb-js/zstd`, `@nestjs/*` і DefinitelyTyped не кладуть README у tarball: для zstd є лише реєстр версій, для
  `@types/mongodb` — самі типи.
- Версія за замовчуванням: за завантаженнями npm 6.x (44 %) і 7.x (34 %) — коли версію не названо, відповідь для обох.

## Родина Mongo: піднімати разом

Цей примірник — частина родини Mongo: сервер, офіційний драйвер Node.js і Mongoose з екосистемою. Питання про
`insertMany` у драйвері впирається в семантику `ordered` сервера, питання про Mongoose — у драйвер під ним. Тому
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

Коли родину зібрано, тексти виносять в архів: у `corpus/` лишається паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа. Поки архів не винесено, тексти лежать у `corpus/` (197 МБ).

**Як винести** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/node-mongodb-corpus-РРРР-ММ-ДД.tar.gz -C instances/node-mongodb corpus raw
find instances/node-mongodb/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/node-mongodb/raw
gzip -9 -c instances/node-mongodb/index/passages.json > instances/node-mongodb/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/node-mongodb-corpus-РРРР-ММ-ДД.tar.gz -C instances/node-mongodb
./df node-mongodb smoke
```

**Оновлення.** Новий випуск драйвера — новий тег у `tags` джерел `driver-src` і `driver-tests` (bson — `bson-src`);
нова мінорна лінія документації з'являється в монорепозиторії сама (`content/node/current`), а коли 7.x стане
попередньою — новий рядок у `folders` джерела `node-docs-monorepo`. Далі `./df node-mongodb refresh` (~2 год 20 хв
мережею), `manifest`, `vectors` (лише змінені фрагменти), `smoke`, `quality`.

## Установка venv

```
cd instances/node-mongodb
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df node-mongodb sources --why   # перелік джерел і білий список
./df node-mongodb refresh         # завантажити все задеклароване (близько 2 год 20 хв)
./df node-mongodb manifest        # оновити паспорт
./df node-mongodb setup           # Qdrant чи пошук лише по словах
./df node-mongodb vectors         # залити корпус у docs-node-mongodb (близько 2 годин: 31 тисяча фрагментів)
./df node-mongodb smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df node-mongodb serve     # порт 8851
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8851/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user node-mongodb-docs http://127.0.0.1:8851/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `node-mongodb-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера.
