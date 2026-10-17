# mongodb — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про сервер MongoDB: CRUD і агрегація, індекси, транзакції, реплікація,
шардинг, безпека, конфігурація `mongod`/`mongos`, журнал змін кожної версії, mongosh і Database Tools (mongodump,
mongorestore, mongoimport…). Документація — офіційний Database Manual кожної лінії від 2.2 до 9.0 у тому вигляді,
яким він був для тієї лінії: усі мажорні й мінорні, разом із rapid-випусками 5.1–5.3, 6.1–6.3, 7.1–7.3 і 8.3; вкладки
прикладів усіх мов (mongosh, Compass, Python, Java, Node.js, C#, Go, Rust, PHP, Ruby, Scala, Kotlin, Swift, C, C++)
збережено. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

mongodb.com показує одну версію за раз і лише підтримувані лінії, а на проді живуть 4.4, 5.0, 6.0, 7.0 і 8.0 водночас;
питання «з якої версії є `$lookup` з pipeline» чи «що змінилося в транзакціях між 4.2 і 4.4» вимагають документа тієї
версії, а не сьогоднішнього. Тут кожна лінія — окремою редакцією: фільтр `version: "4.4"` дає посібник 4.4, і сторінка
`reference-command-find` існує 25 разів. Драйвери і Mongoose — окремі примірники родини (нижче).

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Посібник 7.0, 8.0, 8.3, 9.0 (монорепозиторій, `content/manual/`) | 6 477 | 29 603 | `mongodb/docs`, гілка `main` |
| Посібник 2.2–6.3 і 7.1–7.3 (заморожені гілки `vX.Y`) | 26 007 | 59 115 | `mongodb/docs`, 21 гілка |
| mongosh 2.13 (`content/mongodb-shell`) | 63 | 875 | `mongodb/docs`, `main` |
| mongosh 2.1 (старий репозиторій, гілка `v2.1.2`) | 47 | 149 | `mongodb/docs-mongodb-shell` |
| Database Tools 100.19 (`content/database-tools`) | 59 | 812 | `mongodb/docs`, `main` |

Разом 32 653 документи; фрагментів — 90 554 (`expected_passages` у `checks.json`). Замір `quality` (10 запитів): по
словах 9, за змістом 9, разом 10.

Сторінок посібника за лініями: 2.2 — 567, 2.4 — 830, 2.6 — 1 006, 3.0 — 1 029, 3.2 — 1 038, 3.4 — 1 117, 3.6 — 1 141,
4.0 — 1 188, 4.2 — 1 250, 4.4 — 1 259, 5.0 — 1 263, 5.1 — 1 327, 5.2 — 1 328, 5.3 — 1 341, 6.0 — 1 373, 6.1 — 1 439,
6.2 — 1 441, 6.3 — 1 447, 7.0 — 1 535, 7.1 — 1 561, 7.2 — 1 561, 7.3 — 1 501, 8.0 — 1 598, 8.3 — 1 656, 9.0 — 1 688.
Майбутня 9.1 (`content/manual/upcoming`) не взята: вона ще пишеться.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут
  немає: корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `raw/` — сховище сирих відповідей (138 МБ): кожен blob репозиторію один раз, під адресою raw.githubusercontent.com,
  і мапа `snooty-blobs.json` «sha blob → адреса», якою читач бере той самий текст для всіх гілок, де він не змінився.
  Не в git; в архіві разом із корпусом.
- `sources.json` — звідки корпус будується (5 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену й родини джерел.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — записи HTTP-серверів усієї родини.

Кроки нижче запускаються з кореня фабрики через `./df mongodb <крок>`.

## Звідки документація

Усі п'ять джерел читає новий читач `snooty-history` (`engine/readers/snooty.py`, перетворювач — `_snooty.py`): формат
Snooty rST, яким MongoDB пише всю свою документацію. Що він робить:

- **Сторінки `.txt` і вставки.** `.. include::` з `source/includes/`, `.. literalinclude::` (з `start-after` і
  `end-before`, мова за розширенням), `.. sharedinclude::` із репозиторію `10gen/docs-shared` (адреса —
  `sharedinclude_root` у `snooty.toml`), дочірні `.. replacement::` як підстановки всередині вставки.
- **Константи й підстановки.** `{+version+}`, `{+package-name-org+}` і решта — з `[constants]` `snooty.toml`; у гілках
  до 4.4 — із `source_constants` і `rst_epilog` у `conf.py`. `|newversion|`, `|arrow|`, `.. |x| replace::`,
  `.. |x| unicode::` — з файла, з його вставок (визначення збираються наперед), із `[substitutions]`; значення
  самі можуть містити підстановки й константи.
- **Вкладки.** `.. tabs::`/`.. tab::` нового запису і YAML-запис старих гілок (`tabs: - id: … content: |`) — кожна
  вкладка стає підзаголовком із назвою мови; `.. tabs-selector::`, `composable-tutorial` і `selected-content` —
  так само.
- **YAML старих гілок (до 4.4).** `includes/steps-*.yaml` (кроки з `inherit`, `pre`/`action`/`post`),
  `extracts-*.yaml` (витяги з `replacement {{key}}`), `release-*.yaml`, `toc-*.yaml`/`ref-toc-*.yaml` (зміст
  розділів 2.x, без якого сторінки-переліки були б порожні) — збираються в rST так, як це робив giza.
- **Об'єктні директиви** (`.. method::`, `.. dbcommand::`, `.. option::`, `.. setting::`, `.. serverstatus::`…) стають
  заголовками, тож `read_section` дає саме цей метод чи параметр; `list-table` — таблицею markdown.
- **Без мережі.** Сховище сирого засіяно з голого клону `mongodb/docs` і `10gen/docs-shared` інструментом
  `tools/seed_snooty_store.py --instance mongodb --clone mongodb/docs=<клон> --clone 10gen/docs-shared=<клон>`
  (кожен blob один раз за його sha, лише гілки й теки з `sources.json`); мережею взято лише дерева гілок через
  API. Далі `./df mongodb build` збирає корпус зі сховища за ~12 хвилин. Звичайний `refresh` по мережі теж працює,
  але ~1,3 файла/с — на сім годин.

Особливості:

- **Мітки версій.** Посібник — лінія «X.Y» (`version_line_depth: 2`): 2.2, 2.4, …, 8.3, 9.0. mongosh і Database Tools
  мають власну нумерацію, що плуталася б із сервером 2.x, тому їхні версії — з міткою: `mongosh-2.1`, `mongosh-2.13`,
  `database-tools-100.19`. Родини джерел у `config.json`: `manual` (монорепозиторій + гілки — одна сторінка в усіх
  версіях) і `mongosh` (2.13 + 2.1).
- **Імена документів** — шлях сторінки: `reference-method-db-collection-insertmany`,
  `reference-operator-aggregation-lookup`, `core-transactions`, `tutorial-deploy-replica-set`, `release-notes-7-0`,
  `reference-configuration-options`; mongosh — `reference-methods`, `crud-insert`; Database Tools — `mongodump`,
  `mongorestore`.
- **Приклади CRUD для драйверів** (`driver-examples/test_examples.py`, `DocumentationExamples.java` та ін.) у
  репозиторії документації відсутні в усіх версіях: сайт тягне їх із тестів драйверів під час збирання. У корпусі на
  їхньому місці рядок із назвою файла; самі приклади — у примірнику `node-mongodb` (для Node.js).
- **Пошук по словах** на такому корпусі ~0,5 с на запит (25 редакцій кожної сторінки), за змістом — ~0,1 с.

## Межі, про які треба пам'ятати

- Лише документація сервера, mongosh і Database Tools. Драйвери, Mongoose, Atlas, Compass, Ops/Cloud Manager,
  Kubernetes Operator, BI Connector — ні (для драйвера Node.js і Mongoose є примірники родини).
- 36 сторінок порожні у самому джерелі (заготовки інсталяційних сторінок у гілках 5.2 і 5.3, закоментована сторінка
  перевірки пакетів, згенерований `meta/includes` у 2.2) — читач їх відкидає, це не збій.
- Залишки розмітки: ~1 % документів тримають сирі спани ``x`` у літеральних блоках (так у джерелі) та в довгих
  перенесених спанах; ~0,2 % — підстановки `|newversion|` у назвах чужих сторінок, визначених лише там. Кілька
  десятків ролей `:ref:`/`:term:` лишилися всередині таблиць і через описки джерела.
- Rapid-випуски (5.1–5.3, 6.1–6.3, 7.1–7.3, 8.3) — документація є, хоч самі лінії давно не підтримуються.

## Родина Mongo: піднімати разом

Цей примірник — частина родини Mongo: сервер, офіційний драйвер Node.js і Mongoose з екосистемою. Питання про
`populate` впирається в `$lookup` сервера, питання про `insertMany` у драйвері — в семантику `ordered` сервера. Тому
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

**Де тексти.** В архіві `~/archives/docfactory/mongodb-corpus-2026-10-17.tar.gz` (116 МБ:
32 653 тексти, паспорт і сховище сирого `raw/` — 61 925 файлів; перед
видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на цій машині.

**Як винести** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/mongodb-corpus-РРРР-ММ-ДД.tar.gz -C instances/mongodb corpus raw
find instances/mongodb/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/mongodb/raw
gzip -9 -c instances/mongodb/index/passages.json > instances/mongodb/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/mongodb-corpus-2026-10-17.tar.gz -C instances/mongodb
./df mongodb smoke
```

**Оновлення.** Нова лінія сервера — новий рядок у `folders` джерела `manual-monorepo` («"content/manual/v9.1": "9.1"»,
коли 9.1 вийде і `upcoming` перейменують); нова версія mongosh чи Tools — нова мітка у `folders` відповідного джерела.
Далі `./df mongodb refresh` (мережею; або засів сховища з клону і `build`), `manifest`, `vectors` (лише змінені
фрагменти), `smoke`, `quality`.

## Установка venv

```
cd instances/mongodb
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df mongodb sources --why   # перелік джерел і білий список
./df mongodb refresh         # завантажити все задеклароване (мережею — довго; зі сховища — build, ~12 хв)
./df mongodb manifest        # оновити паспорт
./df mongodb setup           # Qdrant чи пошук лише по словах
./df mongodb vectors         # залити корпус у docs-mongodb (близько 4 год 40 хв: 90 тисяч фрагментів)
./df mongodb smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df mongodb serve          # порт 8850
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8850/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user mongodb-docs http://127.0.0.1:8850/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `mongodb-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера.
