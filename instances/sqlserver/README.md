# sqlserver — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Microsoft SQL Server і Azure SQL. Документація — сайт
learn.microsoft.com/sql англійською в кожній редакції: SQL Server 2017, 2019, 2022 і 2025 разом із SQL Server on
Linux тієї версії, SQL Server 2016 таким, яким сайт показував його до кінця підтримки, і ті самі сторінки для Azure SQL
Database, Azure SQL Managed Instance, Azure Synapse Analytics, Fabric Data Warehouse і SQL database у Fabric (T-SQL,
рушій бази, резервні копії й відновлення, групи доступності, безпека, темпоральні таблиці, JSON, Query Store, Linux і
контейнери, драйвери, ODBC, SSMS, sqlcmd, SqlPackage, Reporting Services, Integration Services, MDX і DMX, SSMA);
сайт learn.microsoft.com/azure/azure-sql і /data-migration; статті підтримки learn.microsoft.com/troubleshoot/sql;
сторінки життєвого циклу (дати початку й кінця підтримки) SQL Server 2014–2025 з learn.microsoft.com/lifecycle;
архів Books Online SQL Server 2014, 2012, 2008 R2, 2008 і 2005 з learn.microsoft.com/previous-versions; пакети
`mssql` і `tedious` (npm), `Microsoft.Data.SqlClient` (NuGet), `mssql-python` (PyPI), `mssql-jdbc` (Maven); теги
образу `mcr.microsoft.com/mssql/server` і README microsoft/mssql-docker; приклади sql-server-samples; журнали змін,
нотатки випусків і сталі релізи go-sqlcmd, DacFx, SqlClient, mssql-jdbc, mssql-python (з його вікі), node-mssql,
tedious і розширення MSSQL для VS Code. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`;
ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

SQL Server живе десятиліттями: у проєктах поруч стоять 2008 R2, 2016 і 2025, а сайт показує лише чинні версії,
причому одна сторінка в різних версіях каже різне. «Монікер» — так learn.microsoft.com називає мітку версії продукту
(`sql-server-ver16` — SQL Server 2022, `azuresqldb-current` — Azure SQL Database): блок сторінки чи ціла сторінка є
лише в тих версіях, які називає її вираз. Тому кожна версія тут — окрема «редакція» (повний набір сторінок, як сайт
показує їх для цієї версії), а все, що зникло з сайту, — з репозиторію на останньому коміті перед вирізанням (2016) чи з
архіву previous-versions (2014 і старші). Десять питань заміру — про T-SQL, резервні копії, безпеку, темпоральні
таблиці, Docker, Azure SQL, драйвер Node.js, перехід з 2012 на 2022, обмеження SQL Server 2012 і статтю підтримки.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| learn.microsoft.com/sql — 10 редакцій | 85 006 | 120 779 | sql-docs a73b10f (18.10.2026); 2016 — 3990900 |
| learn.microsoft.com/azure/azure-sql (3 редакції) і /data-migration | 724 | 10 678 | той самий коміт sql-docs |
| Статті підтримки | 379 | 3 698 | MicrosoftDocs/SupportArticles-docs, `support/sql`, коміт 2bc3403 |
| Життєвий цикл SQL Server 2014–2025 | 6 | 25 | learn.microsoft.com/en-us/lifecycle/products |
| Архів SQL Server 2014 | 8 206 | 37 130 | learn.microsoft.com/previous-versions/sql/2014 |
| Архів SQL Server 2012 | 11 925 | 64 556 | …/sql/sql-server-2012 (Books Online MSDN) |
| Архів SQL Server 2008 R2 | 16 804 | 46 120 | …/sql/sql-server-2008-r2 |
| Архів SQL Server 2008 | 16 940 | 17 959 | …/sql/sql-server-2008 |
| Архів SQL Server 2005 | 16 725 | 43 779 | …/sql/sql-server-2005 |
| Пакети mssql, tedious, SqlClient, mssql-python, mssql-jdbc | 214 | 1 143 | npm, NuGet, PyPI, Maven |
| Образ `mcr.microsoft.com/mssql/server` і README mssql-docker | 27 | 156 | реєстр MCR (290 тегів), коміт 17f17be |
| sql-server-samples: README і скрипти T-SQL | 1 528 | 4 082 | коміт e5d7bb9 |
| Журнали змін, нотатки випусків, релізи | 988 | 2 873 | 15 джерел, лише сталі випуски |
| go-sqlcmd і mssql-python: README, вікі | 66 | 467 | теги кожного сталого випуску, вікі |

Разом 159 538 документів, 353 445 фрагментів (`expected_passages` у `checks.json`). Редакції сайту зливаються сильно: 85
тисяч документів десяти редакцій дали 121 тисячу неповторних фрагментів, бо текстом вони різняться на сотні сторінок, а
не на тисячі. Архів — 59 % фрагментів. Вектори: 25 088 фрагментів на процесорі (~4,7 за секунду), решта 328 332 і
2 944 змінених — на відеокарті RTX 2070 за 7,7 хвилини (див. «Вектори на відеокарті»). Замір `quality` (10 запитів):
«як модель» — 10 з 10; своїми словами — по словах 5, за змістом 5, разом 5. `max_per_doc` і `fusion_depth` не
ставились. Сервер будує індекс із кешу за ~40 секунд і тримає ~3,7 ГБ (на `smoke` з моделлю — до 5,2 ГБ); пошук по
словах — близько 1,5 секунди на запит.

Замір 19.10.2026, запити своїми словами. Архів Books Online 2005, 2008, 2008 R2 і 2012 (62 394 документи, ім'я кожного
— ідентифікатор MSDN на кшталт `ms174979`) займав 67 із 150 місць видачі на 30 запитах-переказах без назв API і
відтісняв чинну документацію; у п'яти промахах `quality` таких сторінок у «разом» було 8 із 25. Тому в `config.json`
стоїть `demote` — `{"pattern": "^[a-z]{2}\\d{5,6}$", "places": 8}`: розділ, чиє ім'я документа без імені джерела
збігається з виразом, у списку кожного способу пошуку стоїть на 8 місць нижче, ніж його поставив пошук, і поступається
чинній сторінці, якщо та знайшлася поруч, але лишається, коли кращого немає. Вираз збігається рівно з 62 394
документами архіву 2005–2012 і з жодним іншим; архів 2014 має шляхи, як сайт, тож під нього не підпадає. Після правки
таких розділів у тих 30 запитах 30 із 150, а в промахах `quality` — жодного. Числа `quality` не змінились: 5, 5 і 5 із
10 переказом, «як модель» 10 із 10; `smoke` — 238 перевірок пройдено, 3 пропущено (корпус в архіві). Промахи змістові:
ціль стоїть шостою–тринадцятою за змістом (в одному запиті — поза першою шістдесяткою), а місця займають сусідні
сторінки чинної документації й приклади sql-server-samples. Запит з `version` «2005», «2008 R2», «2012» бачить лише
архів, зсув у ньому однаковий для всіх, і видача та сама; без `version` старі сторінки лишаються, коли чинної на цю
тему немає (`SQL Server 2005 Notification Services`), а коли є (`SQL Server 2005 DBCC SHOWCONTIG`) — поступаються їй.
З 5 місцями архіву в видачі 40 із 150, зате 45 із 48 перших трьох сторінок таких запитів лишаються; з 8 — 30 і 37; з
12 і більше — 28 і 26. `max_per_doc` 1–2 і `fusion_depth` 10–30, з `demote` чи без, опускали «як модель» до 8–9, тож
не ставились. Сервер перечитує `config.json` на старті, тож `serve` треба перезапустити.

Життєвий цикл, 19.10.2026. Сторінки з датами підтримки в корпусі не було, і запит «until when is SQL Server 2019
supported» віддавав нотатки випусків. Тепер шість сторінок «sql-server-2014» … «sql-server-2025» з
learn.microsoft.com/en-us/lifecycle/products (джерела `lifecycle-2014` … `lifecycle-2025`, читач `html-pages`; по
сторінці на джерело, бо `version` читача одна на все джерело) дають 6 документів і 25 фрагментів; їхні вектори
дорахувано на відеокарті за секунду, зайвих точок не знайшлося. Версії 2012 і старших сайт не має (404). Адреса — з
`/en-us/`: без нього сайт переадресовує, а оновлювач за переадресацією поза оголошеним не йде. Дати лежать у розділі
`#support-dates`: початок, кінець основної (mainstream) і розширеної (extended) підтримки. Сторінка показує час у UTC,
тому кінцеві дати на ній на день пізніші за тихоокеанські, які Microsoft називає в інших статтях (SQL Server 2019: на
сторінці 3/1/2025 і 1/9/2030, у статтях — 28 лютого 2025 і 8 січня 2030); дати початку збігаються. Замір `quality` не
змінився: 5, 5 і 5 із 10, «як модель» 10 із 10. Запити про дати: «SQL Server 2022 end of mainstream support date» і
«SQL Server 2025 lifecycle start date» дають розділ з датами першим, «when does extended support for SQL Server 2016
end» — другим; «until when is SQL Server 2019 supported» ставить сторінку третьою, але розділом `#head` без дат, а
`#support-dates` — сьомим: місця перед ним займають «Supported Version and Edition Upgrades» і сторінка PolyBase.
Запит про 2019 додано до `checks.json` в обидва десятки (тепер по 11): з `version` «2019» він знаходиться (по словах
ні, за змістом і разом так), «як модель» 11 із 11; своїми словами тепер 5, 6 і 6 із 11. У `prompts/search.txt`
дописано, що дати лежать у розділі `#support-dates` і що кінцеві дати на добу пізніші: модель має прочитати цей розділ
через `read_section` і відняти день.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа (83 МБ). Самих текстів
  тут немає: корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz` (67 МБ).
- `sources.json` — звідки корпус будується (77 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену, родини редакцій (`families`), відсув архіву
  MSDN нижче чинної документації (`demote`).
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df sqlserver <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| сайти learn.microsoft.com, статті підтримки | `docfx`, нові поля `monikers`, `yaml_pages`, `rows`, `icons` |
| сторінки життєвого циклу | `html-pages` — наявний, по сторінці на джерело |
| архів previous-versions 2014–2005 | `learn-archive` — новий |
| теги образу MCR | `registry-tags` — новий |
| npm: таблиця версій і README кожної сталої версії | `npm-versions`, `npm-tarball-files` |
| NuGet, PyPI, Maven | `nuget-package`, `pypi-versions`, `pkg-registry` (поле `variant`) |
| README, нотатки випусків, mssql-docker, приклади | `ghdocs-history`, `ghcode-history` |
| журнали змін | `changelog-regex` |
| релізи GitHub | `ghreleases` (поле `stable`), `ghreleases-stable` |
| вікі mssql-python | `ghwiki-page` |

Нове для sqlserver:

- **`docfx`, поле `monikers`.** Версії SQL Server звуться без номера в кінці (`sql-server-ver15`,
  `sql-server-linux-ver16`), а поряд стоять продукти без версії взагалі (`azuresqldb-current`, `fabric`). Поле дає
  порядок монікерів кожного продукту, як його показує learn.microsoft.com/api/familyTrees, і «>= sql-server-ver15» —
  це ver15 і новіші того самого продукту. `moniker` — перелік: редакція «2022» — це те, що сайт показує і для Windows,
  і для Linux. Монікери сторінки — як у сайту: шапка сторінки, інакше `fileMetadata.monikerRange` у docfx.json
  (останній збіг шаблону), інакше група, мінус `exclude_monikers`; 64 випадкові сторінки звірено з
  `<meta name="monikers">` сайту — усі збіглися. Ще поля: `yaml_pages` (FAQ у YAML — питаннями й відповідями),
  `rows` (сітка `:::row:::` — рядками), `icons` (значок «Applies to» стає «✓»), дерево однієї теки
  («КОМІТ:support/sql») для SupportArticles-docs, чиє повне дерево GitHub обрізає. Документи aspnetcore — ті самі до
  байта.
- **`learn-archive`** — архів previous-versions, що лишився на сайті лише сторінками: текст береться markdown-ом сайту
  (заголовок «Accept: text/markdown»), перелік — обходом від кореня змістом і посиланнями. Ім'я документа в архіві
  MSDN — ідентифікатор статті без версії (`ms174979` — CREATE TABLE у 2005–2012), у 2014 — шлях сторінки, як у
  `docfx`. Поле `workers` дає кілька звернень разом без зміни переліку.
- **`registry-tags`** — теги образу з реєстру OCI: документ на лінію (рік SQL Server) з CU, GDR, OD і варіантами Ubuntu
  за номером, плюс огляд.
- **`pkg-registry`, поле `variant`** — `mssql-jdbc` публікує кожну версію збірками під Java (`13.6.1.jre8`,
  `13.6.1.jre11`); без поля всі вони рахувалися передрелізами.
- **`ghreleases`, поле `stable`** — превʼю mssql-jdbc мають звичайні теги (`v13.5.1`), передреліз видно лише з позначки
  GitHub.
- **`tools/seed_git_store.py` знає `docfx`**: sql-docs і залежні репозиторії (dotnet/SqlClient, azure-cli-samples,
  azure-docs-powershell-samples, sql-server-samples, quickstart-templates, Azure/terraform) кладуться у сховище сирого з
  клонів, і `build` пише 86 тисяч документів за хвилини.

## Редакції й версії

- **SQL Server — рік:** `2025`, `2022`, `2019`, `2017`, `2016`; архів — `2014`, `2012`, `2008 R2`, `2008`, `2005`. Лінії
  мінорні (`version_line_depth: 2`), але рік — одне число, тож лінія — сам рік.
- **Хмарні продукти — назва:** `azure-sql-database`, `azure-sql-managed-instance`, `azure-synapse-analytics`,
  `fabric-data-warehouse`, `fabric-sql-database`, `sql-server-on-azure-vms`. Сторінки sql-docs і azure-sql для Azure
  SQL Database несуть ту саму мітку.
- **Драйвери й інструменти — з назвою:** `mssql-12.7.10` (npm `mssql`), `tedious-20.3.8`, `sqlclient-7.1.1`,
  `jdbc-13.6.1`, `mssql-python-1.16.0`, `go-sqlcmd-1.10.0`, `build-sql-2.3.0`, `vscode-mssql-1.47.0`; теги образу — рік
  лінії.
- **Без версії:** статті підтримки, data-migration, sql-server-samples, README mssql-docker — їх шукають без фільтра.
- **Родини (`families`):** `sql` — десять редакцій sql-docs і архів 2014 (ключ сторінки той самий — шлях); `azure-sql` —
  три редакції azure-sql; `msdn-archive` — 2012, 2008 R2, 2008 і 2005 (ключ — ідентифікатор MSDN). Однаковий розділ
  родини займає одне місце у видачі й показує найновішу редакцію; стара видна з фільтром версії. Спільних ключів між
  родинами немає.
- **SQL Server 2016** — з останнього коміту гілки live перед вирізанням монікера (39909008, «[SCOPED] SQL Server
  (#37654)», 16.07.2026; 17.07 PR «Retire SQL Server 2016 moniker segments» почав його прибирати): посилання ведуть на
  файли цього коміту на GitHub, бо сайт 2016 уже не показує.

## Межі, про які треба пам'ятати

- Монікерів Analytics Platform System (`aps-pdw-2016`) і Azure SQL Edge не взято: продукти зняті з підтримки. SQL
  Server 2016 на Linux не існувало.
- Приватний репозиторій `MicrosoftDocs/reusable-content` недоступний: його вставки (підготовка Azure CLI, шаблони
  сторінок Azure Monitor — 89 посилань на 40 сторінках) випадають; так само приклади з приватних `azure-dev-docs-pr` і
  `azure-compute-docs-pr`. Зображення й схеми не беруться.
- Довідника T-SQL в архіві 2014 немає (сторінки 2014 посилаються на чинний сайт), тож T-SQL 2014 відповідає редакція
  2016 і новіші; T-SQL 2012, 2008 R2, 2008 і 2005 — є. Сторінки-контейнери архіву без тексту (90 на всі п'ять версій)
  і 10 адрес архіву 2014, що переадресовують на чинний сайт, не записано. Сироти архіву, на які не веде ні зміст, ні
  посилання, обходом не знаходяться; згенерований довідник класів .NET (SMO, AMO, RMO) відкинуто полем `skip_meta`.
- Лише сталі випуски пакетів і релізів; нотатки DacFx і SqlPackage репозиторій тримає тільки для передвипусків, тож
  сталі нотатки SqlPackage — зі сторінки sql-docs `tools/sqlpackage/release-notes-sqlpackage`. Maven README не має.
- Статті підтримки, data-migration, mssql-docker і sql-server-samples — поточний стан без версій. `CHANGELOG.txt`
  node-mssql закінчується на 11.0.1, далі історія — у релізах GitHub.
- Сайт — англійською; переклади не взято.

## Вектори на відеокарті

На процесорі вектори цього корпусу йшли ~4,7 фрагмента за секунду — понад добу на все. Причина була не в довжині
фрагментів, а в їх змішуванні: модель доповнює кожну пачку з 32 фрагментів до найдовшого, і в sql-docs майже кожна
пачка мала хоч один розділ на 300–512 токенів. Спільний `server/setup._fill` тепер рахує фрагменти від коротких до
довгих (на процесорі ×2,3, вектори ті самі до біта), а `common/embed.py` бере відеокарту, коли у venv стоїть
onnxruntime-gpu і CUDA відповідає. У venv цього примірника замість `fastembed` — `fastembed-gpu` і
`onnxruntime-gpu[cuda,cudnn]` з колесами nvidia-* (~2,3 ГБ, див. `requirements/gpu.txt`); драйвер NVIDIA — у Windows.
RTX 2070 Super: ~500–800 фрагментів за секунду; з процесорними векторами найбільша різниця 8,4e-4, найменший косинус
0,999997. Без відеокарти той самий venv рахує на процесорі. Інші примірники не змінились: у їхніх venv провайдера CUDA
немає, і гілка відеокарти не виконується.

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/sqlserver-corpus-2026-10-19-lifecycle.tar.gz` (487 МБ: 159 538 текстів,
паспорт і сховище сирого `raw/` — 118 675 відповідей, серед них засіяні з клонів sql-docs; перед видаленням розпакований
окремо й звірений з диском — нуль розбіжностей). Лише на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar --sort=name -czf ~/archives/docfactory/sqlserver-corpus-РРРР-ММ-ДД.tar.gz -C instances/sqlserver corpus raw
find instances/sqlserver/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/sqlserver/raw
gzip -9 -c instances/sqlserver/index/passages.json > instances/sqlserver/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/sqlserver-corpus-2026-10-19-lifecycle.tar.gz -C instances/sqlserver
./df sqlserver smoke
```

**Оновлення.** sql-docs: новий коміт гілки `live` ставлять в адреси дерев і `within` джерел `docs-2017` … `docs-2025`,
`docs-azuresqldb` … `docs-fabricsqldb`, `azure-sql-*`, `data-migration` (у `docs-2016` коміт лишається), за потреби — і
коміти залежних репозиторіїв у `repos`. Найшвидше — частковий клон і засів сховища:

```
git clone --bare --filter=blob:none --shallow-since=<дата> --single-branch --branch live \
    https://github.com/MicrosoftDocs/sql-docs.git /шлях/sql-docs.git
.venvs/cpu/bin/python tools/seed_git_store.py --instance sqlserver \
    --clone MicrosoftDocs/sql-docs=/шлях/sql-docs.git --clone dotnet/SqlClient=/шлях/SqlClient.git …
./df sqlserver build docs-2016 docs-2017 … data-migration
```

(клон залежного репозиторію — `git init --bare`, потім `git fetch --depth=1 --filter=blob:none origin <коміт>`).
Новий монікер (наступна версія SQL Server) дописують у кінець переліку продукту в полі `monikers` кожного джерела
sql-docs і додають редакцію-джерело в родину `sql` і джерело `lifecycle-<рік>` (сторінка життєвого циклу цієї версії,
адреса з `/en-us/`). Статті підтримки — новий коміт main у `support`. Архів не змінюється; його повторний обхід —
тисячі звернень, тож без потреби його не питають (`refresh` з іменами джерел). Решта —
`./df sqlserver refresh <джерела>`, далі `manifest`, `vectors`, `smoke`, `quality`.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df sqlserver …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md,
розділ «Спільне середовище». Свій `.env` примірник тримає в `instances/sqlserver/.env` (`cp .env.example .env`;
для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`, береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df sqlserver sources --why   # перелік джерел і білий список
./df sqlserver build …         # sql-docs і залежні — зі сховища, засіяного з клонів (хвилини)
./df sqlserver refresh …       # решта мережею: пакети, GitHub, підтримка (~15 хв); архів — 5 процесів (~2,5 год)
./df sqlserver manifest        # оновити паспорт
./df sqlserver setup           # Qdrant чи пошук лише по словах
./df sqlserver vectors         # залити корпус у docs-sqlserver (відеокарта — ~10 хв, процесор — години)
./df sqlserver smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df sqlserver serve          # порт 8864
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8864/mcp`; індекс із кешу 353 тисяч
фрагментів будується ~40 секунд і займає ~3,7 ГБ пам'яті. Якщо порт зайнятий, сервер скаже про це й вийде: значить,
`serve` цього примірника вже десь запущений; хто тримає порт, покаже `ss -ltnp | grep 8864`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user sqlserver-docs http://127.0.0.1:8864/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож ту саму команду треба виконати в PowerShell, або додати сервер кнопкою «Add
server» у вікні `/mcp` (тип HTTP, рівень User). Можна й без команди: `.mcp.json` цієї теки вже описує запис
`sqlserver-docs`.

**3. Перевірити.** `/mcp` — має бути `sqlserver-docs` і два інструменти `search_docs`, `read_section`. Якщо `/mcp`
показує `failed`, сервер не запущено або запущено з іншим портом.

Зупинка — Ctrl+C у терміналі сервера.
