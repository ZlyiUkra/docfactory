# entityframework — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Entity Framework Core, Entity Framework 6 і класичний Entity
Framework 4.1–5.0 та провайдери баз даних для них — від DbContext, моделювання, зв'язків, запитів LINQ і збереження до
міграцій, інструментів `dotnet ef` і Package Manager Console, продуктивності, тестування й несумісних змін кожного
випуску. Документація англійською, усі стабільні мажорні й мінорні версії: сайт learn.microsoft.com/ef кожної редакції
EF Core 1.0–10.0 і EF6; довідник API кожної лінії EF Core 1.0–10.0 і Entity Framework 4.2–6.5; пакети NuGet EF Core,
`dotnet-ef`, EF6 і всіх провайдерів з офіційних переліків; код і тести dotnet/efcore та dotnet/ef6; документація,
нотатки релізів і довідник API провайдерів. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Одна одиниця на весь Entity Framework: звернувшись до неї з версією, дістаєш усе, що потрібно для впровадження саме на
цій версії, — сторінку сайту тієї редакції, тип і член API того випуску, пакет NuGet з його залежностями, код методу
й тест з очікуваним SQL. EF6 і EF 4.1–5.0 тут таки, як класичний ASP.NET у примірнику `aspnetcore`: проєкти на них
живі, і перехід на EF Core описано обома сторонами. Провайдери — усі, що є на сторінках
learn.microsoft.com/ef/core/providers і learn.microsoft.com/ef/ef6/fundamentals/providers за всю їхню історію, а не
лише Microsoft: PostgreSQL (Npgsql), MySQL і MariaDB (Pomelo, Connector/NET від Oracle, SapientGuardian), Oracle,
MongoDB, Couchbase, Kafka (KEFCore), Firebird, InterBase, Db2 й Informix (IBM), Access (Jet), Spanner, Teradata, YDB,
DuckDB, Snowflake, Kusto, OpenEdge, SQL Server Compact, файлові FileContextCore і FileBaseContext, сімнадцять
провайдерів Devart, а для EF6 — Npgsql, Firebird, MySQL, Oracle ODP.NET, System.Data.SQLite, Visual FoxPro і Devart.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Сайт EF Core: 13 редакцій 1.0–10.0 і чинна гілка `main` | 1 894 | 7 616 | dotnet/EntityFramework.Docs |
| Сайт EF6: редакції 6.3, 6.4, 6.5 і чинна | 474 | 1 778 | те саме |
| API EF Core, 14 ліній 1.0–10.0 і 2.3 | 13 475 | 29 995 | XML-документація пакетів NuGet |
| API Entity Framework 4.2–6.5, 9 ліній | 5 106 | 15 011 | те саме |
| API провайдерів, 88 ліній (Npgsql, Pomelo, MySQL, MongoDB, KEFCore, Jet, DuckDB; для EF6 — MySQL, Npgsql) | 5 330 | 6 334 | те саме |
| NuGet: версії, лінії, залежності й README 31 пакета Microsoft і 62 пакетів провайдерів | 1 053 | 3 696 | реєстр NuGet |
| Код EF Core (`src/`), останній випуск кожної лінії 1.0.6–10.0.13 і 2.3.0 | 18 150 | 96 807 | GitHub dotnet/efcore |
| Тести EF Core (`test/`), ті самі теги | 13 060 | 126 827 | те саме |
| Код EF6 (`src/`), 6.0.2–6.5.2 | 3 823 | 24 963 | GitHub dotnet/ef6 |
| Тести EF6 (`test/`), ті самі теги | 3 475 | 30 471 | те саме |
| Релізи dotnet/efcore (194) і dotnet/ef6 (6) | 200 | 304 | GitHub Releases |
| Провайдери на GitHub: npgsql.org/efcore, mongodb.com/docs/entity-framework 8.0–10.0, README, журнали змін, релізи | 595 | 2 290 | GitHub |

Разом 66 635 документів, 346 092 фрагменти (`expected_passages` у `checks.json`). 17 553 документи власних
фрагментів не дали: кожен їхній розділ дослівно є в іншій редакції, і той фрагмент лише дістав їхні версії — незмінний
метод `DbContext.SaveChanges` чотирнадцяти ліній у пошуку один. Корпус зібрано за 15 хвилин: сайт, код і тести —
зі сховища сирого, засіяного з голих клонів (`tools/seed_git_store.py`), NuGet і GitHub провайдерів — мережею за 9
хвилин. Вектори — на відеокарті (RTX 2070 Super у WSL, `fastembed-gpu` у venv цього примірника): 11 хвилин, близько
520 фрагментів за секунду. Код і тести efcore — дві третини фрагментів.

Замір `quality` (10 запитів своїми словами): по словах 9, за змістом 5, разом 9; «як модель» (ті самі теми назвами
документації, як велить промпт) — 10 із 10 з першого заміру. `max_per_doc` і `fusion_depth` перевірено (0–3 і 0, 10,
20) — жодне значення не дає більше, тож поля не ставились.

Замір 19.10.2026, після скарги, що на питання про EF Core видачу забирають довідник API, код і тести. У `checks.json`
додано три питання (тепер по 13 запитів в обох десятках), кожне двома записами — своїми словами й назвами
документації. Цілі взято з документації чинної лінії EF Core 10.0, а не з видачі: про оптимістичну паралельність —
документ `core-saving-concurrency` цілком («Handling Concurrency Conflicts»); про тригери SQL Server — розділ
«SaveChanges, triggers and the OUTPUT clause» сторінки `core-providers-sql-server-misc` (у 10.0 він є під двома
назвами) і розділ про тригери в несумісних змінах 7.0; про стратегію виконання з власною транзакцією — розділи
«Execution strategies and transactions» і «Transaction commit failure and the idempotency issue» сторінки
`core-miscellaneous-connection-resiliency`. Запити «як модель»:
`ConcurrencyCheck Timestamp RowVersion DbUpdateConcurrencyException handling`,
`UseSqlOutputClause SQL Server triggers`, `ExecutionStrategy BeginTransaction resiliency`. До правки жоден із трьох не
знаходився: по словах 9, за змістом 6, разом 9 із 13, «як модель» 10 із 13. Сторінки стояли глибше за п'яте місце — по
словах 6-ю, 19-ю і 44-ю, за змістом 4-ю, 68-ю і 8-ю, — а над ними були розділи довідника API (`api-…`), коду (`src-…`)
і тестів (`test-…`): це 95 % фрагментів корпусу, і назва методу чи винятку повторюється в них десятки разів.

Правка лише в `config.json`: `demote` з виразом `^(src|test|api)-` на 30 місць. Пошук бере по 30 найкращих фрагментів
кожного способу (6 × k, k = 5), тож 30 — довжина цього вікна: розділ документації, що потрапив у вікно, стоїть вище за
будь-який розділ довідника, коду чи тесту, а де документації поруч немає, довідник і код лишаються, як були. Вираз
збігається лише з довідником API та кодом і тестами efcore й ef6 (звірено з усіма фрагментами). Після правки: по
словах 10, за змістом 7, разом 10 із 13, «як модель» 13 із 13; на старих десяти запитах числа ті самі (9, 5, 9 і 10 із
10), три нові «як модель» стоять 1-м, 1-м і 2-м. Перебір одним процесом (`fusion_depth` 0–60, `max_per_doc` 0–3, вираз
із `api` і без, відсув 5–60 місць — 360 сполук, ще 24 без відсуву): без `demote` найкраще виходить 1 нове «як модель»
із 3; без `api` у виразі — 2 із 3 (на два запити довідник API забирав видачу так само, як код); відсув 5 і 10 місць
без `max_per_doc` — теж 2; `max_per_doc` 1 опускає «разом» на старих десяти з 9 до 8, `fusion_depth` від 30 у
більшості сполук — так само, а нових не рятують.

Лишилося два нових запити своїми словами, яких «разом» не знаходить. Про тригери «разом» знаходить: розділ редакції
7.0 (`savechanges-and-database-triggers`), що займав місця в об'єднаній видачі, додано до цілі як справжню відповідь —
він про ті самі тригери, лише під старішою назвою; окремо по словах запит знаходиться 4-м, за змістом 3-м. Про
паралельність сторінки немає в перших п'яти ні по словах (там інші сторінки сайту), ні за змістом (там тести й код:
слів сторінки в запиті немає). Про транзакції (за змістом 5-м) видачу тримають сторінки EF6 про `user-initiated
transactions` і документація провайдерів. Запас малий: третій запит «як модель» стоїть другим лише завдяки пошуку за
змістом (по словах у вікні жодного розділу документації немає), а нижче за всіх по-старому стоїть перший із десяти «як
модель» — 4-м, як і до правки. `smoke` — 238 перевірок пройдено, 3 пропущено (корпус в архіві), як і до правки. Сервер
перечитує `config.json` на старті, тож `serve` треба перезапустити.

Замір 19.10.2026 ввечері, за запитами із завдання про втрачене оновлення. Запит «як модель»
`DbUpdateConcurrencyException IsRowVersion OriginalValue GetDatabaseValuesAsync` з `version` «10.0» посібника
«Handling Concurrency Conflicts» (`core-saving-concurrency`) не знаходив: назви методів повторюються в довіднику API й
тестах сотні разів, і навіть після `demote` на 30 місць посібник у вікно з 30 розділів не потрапляв (по словах він
стояв 56-м, за змістом 14-м). Правка лише в `config.json`: `fusion_depth` 1500, а `demote` — 1000 місць (стеля поля).
Вікно кожного способу тепер 1500 розділів, тож посібник у нього потрапляє, а зсув у 1000 місць ставить розділи
документації вище за будь-який розділ довідника, коду й тестів. Після правки: «як модель» 15 із 15 (посібник — 2-й),
своїми словами по словах 11, за змістом 10, разом 11 із 14; `smoke` — 238 перевірок пройдено, 3 пропущено (корпус в
архіві). До `checks.json` додано два запити «як модель» (названий вище й `HasConversion ulong rowversion timestamp`,
розділ «Use ulong for timestamp/rowversion») і один своїми словами (про `ulong` замість масиву байтів).

Ціна правки: запит з точною назвою методу тепер частіше повертає сторінки документації, а не довідник API —
«DbContext.SaveChanges Method» раніше мав `api-…-dbcontext#savechanges-method` п'ятим, тепер його в перших п'яти
немає. Затримка запиту зросла з ~300 до ~500 мс. Запас малий: запит «ExecutionStrategy BeginTransaction resiliency»
при `fusion_depth` 1000 губиться, при 1500 стоїть 3-м. Відкотити — повернути `demote.places` 30 і прибрати
`fusion_depth`.

Не виправлено: запит своїми словами «two users edit the same record and the second save must not silently overwrite
the first» не знаходить посібника — його фрагмент стоїть 270-м по словах і 1274-м за змістом (з перших 3000), і жодна
комбінація `fusion_depth`, `demote` і `max_per_doc` цього не змінює. До `checks.json` він не доданий: нічого б не
стеріг.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (211 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену, родини джерел-версій (`families`), відсув
  довідника API, коду й тестів (`demote`) і правила `slug_rewrite` для сторінок, що переїхали.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df entityframework <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| сайт learn.microsoft.com/ef (EF Core і EF6), npgsql.org/efcore | `docfx` |
| довідник API з XML-документації пакетів NuGet | `nuget-xmldoc` |
| версії, залежності й README пакетів NuGet | `nuget-package` (нове поле `registration`) |
| код і тести dotnet/efcore і dotnet/ef6 | `ghcode-history` (новий поділ C# на типи й члени) |
| mongodb.com/docs/entity-framework | `snooty-history` (нове поле `name_prefix`) |
| README, журнали змін і документація провайдерів у репозиторіях | `ghdocs`, `ghwiki-page`, `mdfile` |
| релізи GitHub | `ghreleases`, `ghreleases-stable` |

Ліцензії джерел: документація dotnet/EntityFramework.Docs — CC BY 4.0 (приклади коду — MIT), dotnet/efcore і
dotnet/ef6 — MIT; провайдери — кожен під своєю ліцензією (PostgreSQL License у Npgsql, MIT у Pomelo, Apache 2.0 у
Couchbase, KEFCore і Spanner тощо), закриті комерційні (Devart, Oracle, IBM, Teradata, InterBase) — лише те, що
видає NuGet. Тексти корпусу в git не потрапляють: вони відновлюються з `sources.json`.

Що нового в коді фабрики для entityframework:

- **Поділ C# на члени** (`outline: ["csharp"]` у `ghcode-history`). Файл `.cs` стає розділами «## class DbContext» і
  «### DbContext.SaveChanges()»: член разом зі своїм коментарем `///` і атрибутами, перевантаження поспіль — одним
  розділом. Рядки-продовження оголошень і багаторядкові рядки (`"""…"""`, `@"…"` — очікуваний SQL тестів) членами
  не стають. Поділені за довжиною, тридцять тисяч редакцій файлів різалися б посеред методу, і незмінний метод
  сусідніх версій не зливався б; з поділом на члени він — один фрагмент з усіма версіями.
- **Реєстр SemVer 2.0** (`registration: "gz-semver2"` у `nuget-package`). MySql.EntityFrameworkCore публікує версії з
  метаданими («9.0.15+MySQL9.7.0», за «+» — версія Connector/NET), і реєстру semver1 такого пакета не знає зовсім.
- **`name_prefix` у `snooty-history`**: сторінки MongoDB «limitations», «quick-start», «faq» інакше ділили б ключ
  розділу зі сторінками інших провайдерів.

Особливості:

- **Версії сайту — знімки репозиторію.** Набір `entity-framework/` монікерів не має: сайт показує одну редакцію, тож
  редакція версії — стан dotnet/EntityFramework.Docs за тиждень після виходу лінії в NuGet (у ці дні документацію
  доводять до випуску: знімають позначки прев'ю, дописують «What's new»). EF Core 1.0 — з 14.11.2016, останнього
  коміту перед документацією 1.1: до 31.10.2016 сайт жив у Sphinx (docs.efproject.net). EF Core 2.3 (збірка 2.1 для
  .NET Framework, 2025) знімка сайту не має — тоді сайт описував 9.0. Сторінки EF6 з'явилися в репозиторії восени
  2018 року, тож знімки EF6 — 6.3, 6.4, 6.5. Посилання знімків ведуть на файли коміту в GitHub, чинної гілки — на
  learn.microsoft.com. Сторінки прев'ю EF Core 11 не беруться.
- **Сторінки, що переїхали** (`core/miscellaneous/cli/*` → `core/cli/*`, `querying/raw-sql` → `querying/sql-queries`
  та ще сім пар), зведено правилами `slug_rewrite` за перенаправленнями самого сайту: пару лишено, лише коли стара й
  нова сторінка мають спільний кінець адреси чи назву і ніколи не стоять в одному знімку.
- **Мітки версій.** EF Core — голий номер: сайт і довідник API — лінія (`10.0`), код, тести, пакети й релізи — повний
  номер (`10.0.13`); лінії мінорні (`version_line_depth: 2`). Класичний Entity Framework — з міткою `ef-` (`ef-6.5`,
  `ef-6.4.4`, `ef-4.3`). Кожен провайдер нумерує свої випуски сам, тож версія несе його назву: `npgsql-10.0`,
  `pomelo-9.0`, `mysql-9.0` (MySql.EntityFrameworkCore), `mysql-data-8.0` (старий MySql.Data.EntityFrameworkCore),
  `oracle-23.26`, `mongodb-9.1`, `kefcore-2.6`, `firebird-13.0`, `jet-9.0`, `spanner-4.1`, `duckdb-1.27`,
  `devart-postgresql-9.2`, `ibm-10.0`, `npgsql-ef6-6.4`, `mysql-ef6-9.7` тощо. Документація Npgsql — `npgsql-10.0`,
  крім нотаток випусків, що несуть свою лінію (`npgsql-9.0`).
- **Довідник API** береться з пакетів, що несуть XML-документацію: у EF Core — усі, крім метапакетів і інструментів
  (Tools, Templates, Analyzers, Tasks, `dotnet-ef`), зокрема тести специфікації `*.Specification.Tests`; простори
  імен `.Internal` і класи рядків ресурсів (`CoreStrings`) не беруться — тексти помилок є в коді (`*Strings.Designer.cs`).
  EF 4.1 XML у пакеті не має, тож довідник Entity Framework починається з 4.2. Більшість провайдерів (Oracle, Devart,
  IBM, Firebird, Spanner та інші) XML не несуть — для них лише реєстр NuGet і, де є, репозиторій.
- **Код і тести** — `src/` і `test/` на тегах останнього випуску кожної лінії; 2.3.0 тегу не має — узято коміт гілки
  `release/2.3` на день публікації. З EF6 не взято дизайнер EF для Visual Studio (`EFTools`, `PowerTools`). Файли
  понад 400 КБ не беруться.
- **Запити `quality`** записано так, як їх ставить людина своїми словами. Чотирьом запитам додано справжні відповіді,
  яких не було в першій чернетці цілей: про масове оновлення — розділ «Approach 2: ExecuteUpdate and ExecuteDelete»
  сторінки «Saving Data»; про декартів вибух — розділ «Avoid cartesian explosion when loading related entities»
  сторінки «Efficient Querying»; про пул контекстів — давня сторінка «DbContext pooling» (2.x); про масиви PostgreSQL —
  вступ сторінки «Array Type Mapping» Npgsql. Промах лишився один: «standalone executable that upgrades the
  production database schema» не знаходить розділу «Bundles» — пошук за змістом віддає вище тести міграцій EF6.

## Межі, про які треба пам'ятати

- Усе англійською. Переклади сайту не взято.
- Лише стабільні випуски: preview, rc, EF Core 11 і теги смуг SDK (`v10.0.104`) не взято.
- Документація закритих провайдерів (Devart, Oracle, IBM, InterBase, Teradata) і сайт MySQL Connector/NET
  (dev.mysql.com) — поза корпусом: лише NuGet і README репозиторію там, де він є.
- Microsoft.Data.Sqlite як окремий пакет NuGet не взято — його код є в `src/` efcore.
- Приклади коду — ті, що сторінки вставляють; повні проєкти прикладів (`samples/`) не взято.
- Довідник API з XML не перелічує успадкованих членів і не має прикладів, яких немає в самому XML.

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/entityframework-corpus-2026-10-19.tar.gz` (66 635 текстів, паспорт і
сховище сирого `raw/`; перед видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на цій
машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/entityframework-corpus-РРРР-ММ-ДД.tar.gz -C instances/entityframework corpus raw
find instances/entityframework/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/entityframework/raw
gzip -9 -c instances/entityframework/index/passages.json > instances/entityframework/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/entityframework-corpus-2026-10-19.tar.gz -C instances/entityframework
./df entityframework smoke
```

**Оновлення.** Новий патч-випуск EF Core: у джерелах `api-<лінія>` перенести номер пакетів (`/10.0.13` → `/10.0.14`,
разом з адресою nupkg і `within`), у `efcore-src` і `efcore-test` — тег лінії в `tags`. Новий мажор: додати
`site-11-0` (коміт репозиторію документації за тиждень після випуску), `api-11-0`, тег у `tags` коду й тестів і
вписати їх у `families`; правило `ef-core-11\.0` в `exclude` знімків прибрати. Нова лінія провайдера з XML — нове
джерело `api-<провайдер>-<лінія>` у його родині. Сайт на `main`, реєстри NuGet, релізи й документація провайдерів
підхоплюються самі. Код і тести тягнути не мережею, а голим клоном: `./df entityframework list efcore-src efcore-test`
(дерева тегів через API), далі `tools/seed_git_store.py --instance entityframework --clone
dotnet/efcore=<клон> --clone dotnet/ef6=<клон> --clone dotnet/EntityFramework.Docs=<клон>` і `./df entityframework
build <джерела>`; решта — `./df entityframework refresh <джерела>`. Далі `manifest`, `vectors`, `smoke`, `quality`.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df entityframework …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md,
розділ «Спільне середовище». Свій `.env` примірник тримає в `instances/entityframework/.env` (`cp .env.example .env`;
для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`, береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df entityframework sources --why   # перелік джерел і білий список
./df entityframework refresh         # завантажити все задеклароване (код і тести — краще з клонів, див. вище)
./df entityframework manifest        # оновити паспорт
./df entityframework setup           # Qdrant чи пошук лише по словах
./df entityframework vectors         # залити корпус у docs-entityframework (11 хвилин на відеокарті)
./df entityframework smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df entityframework serve          # порт 8865
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8865/mcp`. Індекс по словах на
346 тисячах фрагментів збирається близько хвилини, і сервер тримає в пам'яті близько 5,6 ГБ — більше за будь-який
менший примірник: дві третини фрагментів — код і тести efcore. Якщо порт зайнятий,
сервер скаже про це й вийде: значить, `serve` цього примірника вже десь запущений; хто тримає порт, покаже
`ss -ltnp | grep 8865`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user entityframework-docs http://127.0.0.1:8865/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `entityframework-docs` і два інструменти `search_docs`, `read_section`. Якщо
`/mcp` показує `failed`, сервер не запущено або запущено з іншим портом.

Зупинка — Ctrl+C у терміналі сервера.
