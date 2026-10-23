# testcontainers-dotnet — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Testcontainers for .NET — бібліотеку для тестів з одноразовими
контейнерами Docker: будівники контейнерів, образів, мереж і томів, стратегії очікування, Resource Reaper, повторне
використання, Docker Compose, налаштування й автентифікацію Docker, віддалений Docker і Docker у Docker, CI/CD,
інтеграцію з xUnit.net і всі модулі (PostgreSQL, MS SQL, MySQL, MongoDB, Redis, Kafka, RabbitMQ, LocalStack, Azurite,
Cosmos DB, Elasticsearch і ще п'ятдесят), — а також про Docker.DotNet.Enhanced, клієнт Docker Engine API, на якому
стоїть бібліотека. Документація англійською, усі стабільні версії 0.0.4–4.16.0: сайт dotnet.testcontainers.org на
кожному тезі і README, яким документація була до сайту; довідник API кожної мінорної лінії з XML-документації пакетів
NuGet; пакети NuGet з версіями й залежностями; код, тести й приклади репозиторію; релізи GitHub. Код спільний і лежить
у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

Testcontainers — не частина .NET і не частина Docker: це окрема бібліотека зі своєю нумерацією, своїм сайтом і
шістьма десятками модулів, і жоден інший примірник її не тримає. Звернувшись до цієї одиниці з версією, дістаєш усе для
впровадження саме на ній: сторінку сайту тієї версії разом з прикладами, які сайт вставляє з тестів, тип і член API того
випуску, пакет модуля з залежностями, код будівника й тест, з якого взято приклад, нотатки релізу з несумісними
змінами. Docker.DotNet.Enhanced тут таки: це підтримуваний тією самою командою форк Docker.DotNet, на якому ядро стоїть
з 4.1 (до того — на первісному Docker.DotNet 3.125), і `CreateContainerParameters`, `WithCreateParameterModifier` чи
версія Docker Engine API без нього не пояснюються.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Сайт dotnet.testcontainers.org: 32 стабільні теги 2.2.0–4.16.0 | 844 | 568 | тека `docs/` репозиторію |
| README 0.0.4–2.1.0 — документація до появи сайту, 16 тегів | 13 | 53 | те саме |
| API ядра й модулів, 31 мінорна лінія 2.2–4.16 (1 346 пакетів-ліній) | 7 919 | 4 990 | XML-документація пакетів NuGet |
| API Docker.DotNet.Enhanced 4.2–4.3 | 530 | 1 752 | те саме |
| NuGet: версії, лінії, залежності й README 69 пакетів Testcontainers | 1 792 | 5 017 | реєстр NuGet |
| NuGet: DotNet.Testcontainers 0.0.1–1.6.0 і 8 пакетів Docker.DotNet.Enhanced | 78 | 216 | те саме |
| Код (`src/`) на останньому тезі кожної мінорної лінії 0.0.9–4.16.0, 41 тег | 2 522 | 6 786 | GitHub testcontainers/testcontainers-dotnet |
| Тести (`tests/`), ті самі теги | 1 099 | 2 798 | те саме |
| Приклади `examples/` (WeatherForecast, Flyway, Respawn), 2.2–4.16 | 241 | 308 | те саме |
| Релізи (48) і CHANGELOG.md 2.1–2.3 | 51 | 219 | GitHub Releases, репозиторій |
| Docker.DotNet: README, таблиця версій Docker API, код і тести 12 ліній 3.125–4.3, 22 релізи | 2 181 | 4 144 | GitHub testcontainers/Docker.DotNet |

Разом 17 270 документів, 26 851 фрагмент (`expected_passages` у `checks.json`). 7 957 документів власних фрагментів не
дали: кожен їхній розділ дослівно є в іншій версії, і той фрагмент лише дістав їхні версії — незмінна сторінка сайту
32 тегів чи незмінний член API 31 лінії в пошуку один. Корпус зібрано за 15 хвилин: код, тести й README — зі сховища
сирого, засіяного з голих клонів (`tools/seed_git_store.py`, 6 006 записів за 3 с), сайт і релізи — мережею за 4
хвилини, пакети NuGet і довідник API — трьома паралельними процесами за 10 хвилин. Вектори — на відеокарті (RTX 2070
Super у WSL, `fastembed-gpu` у venv цього примірника): 32 секунди, близько 840 фрагментів за секунду.

Замір `quality` (10 запитів своїми словами): по словах 5, за змістом 3, разом 7; «як модель» (ті самі теми назвами
документації, як велить промпт) — 10 із 10 з першого заміру, тож `max_per_doc` і `fusion_depth` не мірялись.

Замір 19.10.2026, за запитами із завдання про SQL Server у тестах. Запит своїми словами «start a throwaway SQL Server
in Docker for my tests» знаходить сторінку модуля `modules-mssql` (по словах 1-й, за змістом 4-й). Запит «як модель»
`MsSqlBuilder Testcontainers.MsSql GetConnectionString` її не знаходив: сторінка стоїть 36-ю по словах і 211-ю за
змістом, а перші місця займають довідник API й код `MsSqlBuilder`. Жодна з 123 комбінацій `demote` (вирази з `api`,
`src`, `tests`, `examples`, зсув 5–60 місць), `fusion_depth` (0–250) і `max_per_doc` (0–3) цього не змінила. Запит
переписано так, як його поставила б модель, що хоче підняти SQL Server у тесті, — з назвою модуля: `MsSqlBuilder
MsSqlContainer StartAsync Microsoft SQL Server module` з `version` «4.16»; сторінка модуля тепер перша і по словах, і
за змістом. Довідник API на запит самими назвами `MsSqlBuilder` і `GetConnectionString` лишається прийнятною
відповіддю, але ціллю не став. Обидва запити додано до `checks.json` (тепер по 11): своїми словами по словах 6, за
змістом 4, разом 8; «як модель» 11 із 11.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (48 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену, родини джерел-версій (`families`: 31 лінія
  API Testcontainers і 2 лінії API Docker.DotNet.Enhanced) і правила `slug_rewrite` для сторінки, що переїжджала.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df testcontainers-dotnet <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| сайт dotnet.testcontainers.org (MkDocs Material з теки `docs/`) | `site-history` (нові поля `snippet_sections`, `site`) |
| README 0.0.4–2.1.0, README прикладів, README і таблиця версій Docker.DotNet | `ghdocs-history` |
| довідник API з XML-документації пакетів NuGet | `nuget-xmldoc` (нове поле `link`) |
| версії, залежності й README пакетів NuGet | `nuget-package` (нове поле `since`) |
| код, тести й приклади обох репозиторіїв | `ghcode-history` (нове поле `outline_indent`) |
| релізи GitHub | `ghreleases` |
| CHANGELOG.md 2.1–2.3 | `changelog-keep` |

Ліцензії джерел: testcontainers/testcontainers-dotnet і testcontainers/Docker.DotNet — MIT. Тексти корпусу в git не
потрапляють: вони відновлюються з `sources.json`.

Що нового в коді фабрики для testcontainers-dotnet:

- **Вставки `--8<--` з іменованими розділами** (`snippet_sections: true` у `site-history`, разом із `snippets: "."` —
  шляхи від кореня репозиторію). Сайт не переписує прикладів у сторінку, а вставляє їх із тестів:
  `--8<-- "tests/…/PostgreSqlContainerTest.cs:UsePostgreSqlContainer"` — лише рядки між мітками
  `// # --8<-- [start:UsePostgreSqlContainer]` і `[end:…]`, зі знятим спільним відступом, як у pymdownx.snippets з
  `dedent_subsections: true`; так само розділ `PackageReferences` з файла `.csproj` тесту. Рядки-мітки з вставленого
  тексту прибираються, а вставка поза огорожею коду розбирається як markdown (виноска з `_call_out_test_projects.txt`).
  Без поля такий рядок шукав файл з іменем «…cs:UsePostgreSqlContainer» і зникав разом із прикладом. Перевірено на 82
  сторінках mkdocs-джерел kubernetes і linux: без поля текст той самий байт у байт.
- **Посилання на сторінки сайту** (`site` у `site-history`, як у `ghdocs-history`): 45 сторінок найновішого тегу
  перелічено поіменно; прибрані раніше сторінки цитують свій файл на GitHub, а не мертву адресу.
- **`since` у `nuget-package`** — найстаріша версія пакета, що береться (див. нижче про Testcontainers 0.0.x).
- **`link: "nuget"` у `nuget-xmldoc`**: learn.microsoft.com генерує довідник лише для бібліотек Microsoft, тож тип
  Testcontainers чи Docker.DotNet посилається на сторінку своєї версії пакета на nuget.org.
- **`outline_indent: "auto"` у `ghcode-history`**: Testcontainers пише код з відступом у два пробіли (простір імен
  блоком, тип на 2, члени на 4), а тести — на чотири, тож відступ членів береться з першого рядка тіла типу. Під
  правилом «тип плюс чотири» клас `ContainerBuilder<…>` на 28 тисяч символів лишався одним розділом; тепер це 34
  розділи — `WithPortBinding()`, `WithResourceMapping()`, `WithNetwork()`… Без поля поділ той самий (1 555 файлів).

Особливості:

- **Версії — точні номери випусків.** Сторінки сайту, довідник API, код, тести й релізи несуть номер тегу (`4.16.0`,
  `4.8.1`, `0.0.9`); лінії мінорні (`version_line_depth: 2`), тож `version: "4.16"` бере лінію, `"4"` — усі 4.x.
  Docker.DotNet.Enhanced нумерує випуски сам (3.125–4.3 перетинаються з Testcontainers 4.x), тому його версії несуть
  мітку: `docker-dotnet-4.3.3`, `docker-dotnet-3.132`. DotNet.Testcontainers 0.0.1–1.6.0 — та сама бібліотека до
  перейменування в 2.0, тож її версії без мітки.
- **Testcontainers 0.0.1–0.0.2.107 у NuGet — чужий пакет.** Під ідентифікатором `Testcontainers` реєстр тримає й
  версії 2018–2019 років автора swissarmykirpan: опис «Package Description», жодного README, жодної XML-документації,
  інший проєкт. Бібліотека testcontainers-dotnet дістала цей ідентифікатор з 2.0.0 (до того вона жила як
  DotNet.Testcontainers), тож старі версії відсічено полем `since` — інакше вони стали б лінією «0.0» самого
  Testcontainers в огляді пакета й у фільтрі версій, поряд зі справжніми 0.0.4–0.0.9 з GitHub.
- **Довідник API** — з найновішої версії кожної мінорної лінії: ядро з 2.2 (2.0–2.1 XML не несли), модулі з 3.0,
  Testcontainers.Xunit з 4.1 і XunitV3 з 4.2, знятий модуль — до своєї останньої лінії (Minio 4.15, SqlEdge 3.10,
  EventStoreDb 4.9). Docker.DotNet.Enhanced несе XML лише з 4.2. Testcontainers.Xunit і Testcontainers.XunitV3
  оголошують ті самі типи в тому самому просторі імен, тож тип показує члени обох пакетів, а посилання веде на
  перший (v2).
- **Сторінка, що переїжджала** (`examples/compose.md` 2.4–3.0 → `examples/dind.md` 3.1–4.3 → `dind/index.md` з 4.4;
  git бачить обидва перейменування), зведена двома правилами `slug_rewrite`; `api/resource-reaper.md` →
  `api/resource_reaper.md` дає той самий ключ і так. `api/compose.md` з 4.15 — інша сторінка (ComposeBuilder) і
  лишається окремою.
- **Код і тести** — `src/` і `tests/` на останньому тезі кожної мінорної лінії; до 1.6 тести лежали в `src/` і
  входять у код. Docker.DotNet — лише лінії форка 3.125.15–4.3.3: старші теги репозиторію належать первісному
  Docker.DotNet (Microsoft) і пакетом Docker.DotNet.Enhanced не виходили. Журналу змін Docker.DotNet не веде —
  зміни описують релізи. CHANGELOG.md бібліотеки вели лише 2.1–2.3, з 2.4 він відсилає до релізів.
- **Запити `quality`** записано так, як їх ставить людина своїми словами. Двом запитам додано справжні відповіді, яких
  не було в першій чернетці цілей: про очікування HTTP-відповіді — член `UntilHttpRequestIsSucceeded` інтерфейсу
  `IWaitForContainerOS` у довіднику API і в коді; про тести, що самі біжать у контейнері, — розділи «Docker Desktop»
  тієї самої сторінки dind у редакціях 2.4–3.8 (`TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal`). Промахи своїми
  словами: вимкнення Resource Reaper (знаходиться `CleanUpAsync`), перехід на обов'язковий образ у конструкторі
  будівника (реліз 4.10.0) і залежності пакета ядра; назвами документації («як модель») знаходяться всі три.

## Межі, про які треба пам'ятати

- Усе англійською.
- Лише стабільні випуски: beta- і preview-збірки NuGet, гілка `develop` (живий сайт може бути на крок попереду 4.16.0)
  не взято.
- Пакети інших авторів з «Testcontainers» в імені (WireMock.Net.Testcontainers, Dapr.Testcontainers,
  Microcks.Testcontainers, TestContainers.Container.* та інші) — поза корпусом.
- Testcontainers для Java, Go, Node.js, Python і сайт testcontainers.com — поза корпусом.
- Docker, Docker Compose, бази й сервіси, які піднімають модулі, і xUnit.net самі по собі — їхня власна документація.
- Довідник API з XML не перелічує успадкованих членів і не має прикладів, яких немає в самому XML.

## Родина .NET: піднімати разом

Цей примірник — частина родини .NET: платформа, мова, веб, дані, тестування й менеджер пакетів Microsoft. Питання про
C# впирається в бібліотеку класів, про EF — у SQL Server, про тест із базою — у Testcontainers, про пакет — у NuGet.
Тому примірники родини піднімають у Claude Code разом, а `.mcp.json` цієї теки перелічує всі вісім серверів:
підключивши будь-який із них, Claude Code бачить решту.

| Примірник | Сервер | Порт | Що |
|-----------|--------|-----:|----|
| `dotnet` | `dotnet-docs` | 8866 | платформа .NET 1.0–10.0: сайт, CLI `dotnet`, довідник API, F#, Visual Basic, .NET Framework |
| `csharp` | `csharp-docs` | 8878 | мова C#: сайт на день виходу 7.0–14, ECMA-334 усіх видань, пропозиції, Roslyn |
| `aspnetcore` | `aspnetcore-docs` | 8862 | ASP.NET Core 1.0–10.0 і класичний ASP.NET |
| `entityframework` | `entityframework-docs` | 8865 | EF Core 1.0–10.0, EF6, провайдери |
| `sqlserver` | `sqlserver-docs` | 8864 | SQL Server 2016–2025, Azure SQL, T-SQL |
| `dotnet-testing` | `dotnet-testing-docs` | 8870 | xUnit, NUnit, bUnit, Moq, NSubstitute, FluentAssertions, Shouldly, AngleSharp, Respawn |
| `testcontainers-dotnet` | `testcontainers-dotnet-docs` | 8867 | Testcontainers for .NET |
| `nuget` | `nuget-docs` | 8869 | NuGet: сайт, `nuget.exe` і `dotnet nuget`, пакети, протокол V3 |

Поза родиною, але за потреби підключається так само: `playwright` (`playwright-docs`, порт 8788) — у ньому є Playwright
для .NET (пакет NuGet `Microsoft.Playwright`) поруч із версіями для Node.js, Python і Java.

`prompts/loaded.txt` каже моделі, що цей набір — частина родини, і які сервери її доповнюють. Повний перелік родин — у
розділі «Родини примірників» кореневого [README](../../README.md).

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/testcontainers-dotnet-corpus-2026-10-19.tar.gz` (17 270 текстів, паспорт
і сховище сирого `raw/`; перед видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на цій
машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/testcontainers-dotnet-corpus-РРРР-ММ-ДД.tar.gz -C instances/testcontainers-dotnet corpus raw
find instances/testcontainers-dotnet/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/testcontainers-dotnet/raw
gzip -9 -c instances/testcontainers-dotnet/index/passages.json > instances/testcontainers-dotnet/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/testcontainers-dotnet-corpus-2026-10-19.tar.gz -C instances/testcontainers-dotnet
./df testcontainers-dotnet smoke
```

**Оновлення.** Новий випуск Testcontainers `x.y.z`: тег у `refs` джерела `site` (першим) і в `site`-переліку сторінок
нові сторінки найновішого тегу; у `tags` джерел `src`, `tests`, `examples`, `examples-readme` — тег замість
попереднього тієї самої лінії; нова лінія — ще й джерело `api-x-y` (пакети `Пакет/x.y.z` усіх модулів, що вийшли в
цій лінії, адреса nupkg ядра і `within`) і його id в `families.api`; новий модуль — у `packages` джерела
`nuget-testcontainers`. Генератор `sources.json` лишився поза репозиторієм, тож правка — руками за зразком
сусідніх джерел. Новий випуск Docker.DotNet.Enhanced — тег у `tags` джерел `docker-dotnet-*` і, якщо нова лінія,
джерело `api-docker-x-y`. Реєстри NuGet і релізи підхоплюються самі. Код, тести й README тягнути не мережею, а голим
клоном: `./df testcontainers-dotnet list src tests examples examples-readme readme-history docker-dotnet-readme
docker-dotnet-src docker-dotnet-test` (дерева тегів через API), далі `tools/seed_git_store.py --instance
testcontainers-dotnet --clone testcontainers/testcontainers-dotnet=<клон> --clone testcontainers/Docker.DotNet=<клон>`
і `./df testcontainers-dotnet build <ті самі джерела>`; решта — `./df testcontainers-dotnet refresh <джерела>`. Далі
`manifest`, `vectors`, `smoke`, `quality`.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df testcontainers-dotnet …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md, розділ
«Спільне середовище». Свій `.env` примірник тримає в `instances/testcontainers-dotnet/.env` (`cp .env.example .env`;
для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`, береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df testcontainers-dotnet sources --why   # перелік джерел і білий список
./df testcontainers-dotnet refresh         # завантажити все задеклароване (код і тести — краще з клонів, див. вище)
./df testcontainers-dotnet manifest        # оновити паспорт
./df testcontainers-dotnet setup           # Qdrant чи пошук лише по словах
./df testcontainers-dotnet vectors         # залити корпус у docs-testcontainers-dotnet (пів хвилини на відеокарті)
./df testcontainers-dotnet smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df testcontainers-dotnet serve          # порт 8867
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8867/mcp`; індекс по словах
збирається кілька секунд. Якщо порт зайнятий, сервер скаже про це й вийде: значить, `serve` цього примірника вже десь
запущений; хто тримає порт, покаже `ss -ltnp | grep 8867`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user testcontainers-dotnet-docs http://127.0.0.1:8867/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `testcontainers-dotnet-docs` і два інструменти `search_docs`, `read_section`. Якщо
`/mcp` показує `failed`, сервер не запущено або запущено з іншим портом.

Зупинка — Ctrl+C у терміналі сервера.
