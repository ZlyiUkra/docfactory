# upstash — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про платформу Upstash — безсерверні дані з оплатою за запит. Ядро —
Upstash Redis: база, сумісна з командами Redis, доступна і по TCP, і через HTTP REST API для serverless і edge
(Vercel, Cloudflare Workers, Lambda); до неї — клієнти `@upstash/redis` (TypeScript) і `upstash-redis` (Python),
обмежувач частоти `@upstash/ratelimit` (`slidingWindow`, `fixedWindow`, `tokenBucket`), `@upstash/lock`, `queue`,
`query`, `realtime`, `semantic-cache`. Решта продуктів: QStash (черга повідомлень і планувальник по HTTP: `publishJSON`,
розклади, URL-групи, черги, DLQ, підписи), Workflow (довготривалі функції: `serve`, `context.run`, `sleep`, `call`,
`waitForEvent`, `invoke`, агенти), Vector (векторна база: `upsert`, `query`, namespaces, фільтри), Search, Realtime,
Blob, Box (пісочниці для AI-агентів), закритий Kafka, Context7 (документація для агентів: MCP-сервер, SDK, CLI
`ctx7`), Upstash CLI, MCP-сервери, провайдери Terraform і Pulumi, Developer API. Документація — сайт upstash.com/docs,
блог, і для кожного стабільного випуску кожного SDK та інструменту — README, журнали змін, код, тести й нотатки
релізів; таблиці версій і README пакетів npm, проєкти PyPI, приклади, skills. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

Upstash — не бібліотека, а платформа з десятком продуктів і півсотнею пакетів, кожен зі своєю нумерацією версій:
`@upstash/redis` 0.1–1.39, `@upstash/qstash` 0.0–2.12, `@upstash/workflow` 0.1–1.4, `@upstash/vector` 0.1–1.2,
Python-клієнти, Go, PHP. Сайт показує лише поточну редакцію й не версіонується; довідник API SDK — це код з типами.
Тут кожен випуск — окремою редакцією: «з якої версії `@upstash/redis` є auto-pipelining» чи «що змінилось у
`serve` Workflow між 0.2 і 1.0» береться з документів тієї версії. Сам сервер Redis (команди зсередини,
`redis.conf`, Cluster) — примірник `redis`; клієнти ioredis і node-redis та черги BullMQ — свої примірники родини.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Сайт: Redis — початок, можливості (REST API, глобальна реплікація, Search, Vector у Redis), довідник 334 команд, сторінки SDK TypeScript, Python і ratelimit, посібники, інтеграції, усунення несправностей | 925 | 4 292 | upstash.com/docs, sitemap.xml, знімок 16.10.2026 |
| Сайт: QStash | 122 | 637 | те саме |
| Сайт: Workflow | 151 | 748 | те саме |
| Сайт: Vector | 76 | 376 | те саме |
| Сайт: Search, Realtime, Blob, Box | 105 | 882 | те саме |
| Сайт: DevOps (Terraform, Pulumi, Developer API), довідник Developer API (OpenAPI), спільні сторінки, ресурси для агентів | 101 | 409 | те саме |
| Сайт: розділ Kafka, як він був перед видаленням (травень 2025) | 88 | 441 | `upstash/docs`, коміт перед «removing all kafka docs» |
| Блог (400 дописів 2021–2026) і глосарій | 408 | 5 025 | `upstash/upstash-web`, `data/blog` |
| SDK та інструменти TypeScript (38 репозиторіїв): README, журнали змін, README прикладів, skills | 446 | 1 907 | теги стабільних версій |
| …код | 3 872 | 10 606 | ті самі теги |
| …тести (у великих репозиторіях — останній випуск кожної мінорної лінії) | 1 711 | 7 230 | ті самі теги |
| …нотатки релізів | 551 | 1 136 | GitHub Releases |
| Box і AgentKit (монорепозиторії): документація, код, тести, Python SDK Box, релізи | 1 499 | 5 301 | теги пакетів `@upstash/box@…`, `@upstash/agentkit-*@…`, `python-sdk-v…` |
| Context7: документація, код, тести, релізи | 1 327 | 5 713 | теги `@upstash/context7-mcp@…`, `v1.0.x`, `ctx7@…` |
| SDK Python (upstash-redis, ratelimit, qstash, vector, workflow, search, semantic-cache): README, код, тести, релізи | 1 236 | 1 338 | теги `vX.Y.Z` |
| SDK Go (qstash, vector, workflow) і PHP (vector, Laravel) | 449 | 541 | теги `vX.Y.Z` |
| Провайдер Terraform (документація ресурсів, код, тести, релізи) і Pulumi (документація, релізи) | 385 | 551 | теги `vX.Y.Z` |
| Приклади: `upstash/examples`, старі `redis-examples`, `kafka-examples`, `qstash-examples`, теки `examples/` 14 SDK | 214 | 1 946 | один приклад — один документ з README і кодом |
| Skills для агентів (кожен продукт і SDK) | 166 | 1 547 | `upstash/skills`, знімок |
| npm: таблиці версій 66 пакетів `@upstash/*` і `upstash` (з canary, rc, next; без збірок ci) | 159 | 594 | registry.npmjs.org |
| npm: README кожної стабільної версії (з tarball) | 381 | 1 785 | registry.npmjs.org |
| PyPI: 8 проєктів — версії, вимоги до Python, залежності, описи | 60 | 310 | pypi.org |

Разом 14 432 документи; фрагментів — 53 287 (`expected_passages` у `checks.json`). Замір `quality` (10 запитів):
по словах 9, за змістом 10, разом 10. `max_per_doc` 0 (2 дає те саме, 1 — гірше).

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут
  немає: корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (371 джерело), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, правила перейменування ключів і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — записи HTTP-серверів родини Redis
  для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df upstash <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| сайт upstash.com/docs (Mintlify): markdown-двійник кожної адреси з sitemap.xml; компоненти стають текстом, шматок OpenAPI сторінки Developer API — розділами Request і Response | `sitemap-mintlify` |
| розділ Kafka з історії `upstash/docs`, блог і глосарій, README, журнали, документація репозиторіїв, skills | `ghdocs-history` |
| код і тести TypeScript (розділи — за класами, функціями, типами, `describe`/`it`) | `ghcode-history-ts` |
| код і тести Python, Go, PHP (файл — один документ) | `ghcode-history` |
| нотатки релізів: звичайні репозиторії — `ghreleases` з полем `version_prefix`; монорепозиторії — `ghreleases-stable` з `tag_prefix` пакета | `ghreleases`, `ghreleases-stable` |
| приклади з власним `package.json` | `ghexamples` (поле `name_prefix`) |
| таблиці версій npm | `npm-versions` |
| README кожної версії з tarball пакета | `npm-tarball-files` (поле `version_prefix`) |
| версії й описи PyPI | `pypi-versions` (поле `version_prefix`) |

Нового читача не знадобилось; трьом читачам додано необов'язкове поле `version_prefix`, одному — `name_prefix`
(без полів вони працюють, як раніше), а читач Mintlify навчився знімати блок «Documentation index» і з малої літери.

Особливості:

- **Версії — з назвою пакета.** Нумерацій у платформі десятки, тож версія кожного документа SDK починається з
  назви пакета: `redis-1.39.0` — `@upstash/redis`, `ratelimit-2.2.0`, `qstash-2.12.0`, `workflow-1.4.0`,
  `vector-1.2.3`, `search-0.1.7`, `cli-1.5.0`; Python — за назвою на PyPI: `upstash-redis-1.8.0`, `upstash-vector-0.8.0`,
  `qstash-py-3.4.0`; Go і PHP — `qstash-go-1.0.0`, `vector-php-1.2.0`; монорепозиторії — `box-0.7.9`, `box-cli-0.3.5`,
  `agentkit-sdk-0.9.0`, `context7-mcp-4.4.2`, `ctx7-0.2.1`; провайдери — `terraform-2.1.0`, `pulumi-0.5.0`. Фільтр
  `version: "redis-1.39"` лишає 1.39.x клієнта TypeScript, `"qstash-2"` — усі 2.x клієнта QStash. Сторінки сайту,
  блог, приклади, skills і знімки репозиторіїв без тегів версій не несуть: це поточний стан.
- **Імена документів.** Сайт — за адресою: `docs-redis-commands-string-get`, `docs-redis-sdks-ts-pipelining-auto-pipeline`,
  `docs-qstash-howto-publishing`, `docs-workflow-basics-serve`, `docs-vector-features-namespaces`,
  `docs-devops-developer-api-redis-create-database-global`, `docs-kafka-rest-restintro`; блог — `blog-2021-04-01-serverless-database-connections`;
  репозиторії — з префіксом репозиторію: `redis-js-readme`, `redis-js-pkg-pipeline-ts`, `redis-js-test-pkg-commands-get-test-ts`,
  `ratelimit-js-src-single-ts`, `workflow-js-src-context-context-ts`, `redis-py-upstash-redis-asyncio-client-py`;
  релізи — `redis-js-v1.39.0`, `box-box-upstash-box-0.7.9`; приклади — `redis-js-examples-nextjs-app-router`,
  `examples-nextjs-todo`; skills — `skills-upstash-redis-js-skill`; npm — `redis-overview`, `redis-line-1`,
  `redis-readme-markdown-…`; PyPI — `upstash-redis-overview`, `upstash-redis-line-1`. Правила `slug_rewrite` у
  `config.json` зводять блог, глосарій, Kafka, skills і тести до цих імен.
- **Де довідник API.** Для `@upstash/redis` — сторінки сайту `docs-redis-sdks-ts-commands-*` (по методу на команду) і код
  `redis-js-pkg-commands-*`; для ratelimit — `docs-redis-sdks-ratelimit-ts-methods` і `ratelimit-js-src-*`; для QStash —
  `docs-qstash-api-reference-*` (OpenAPI) і `qstash-js-src-client-*`; для Workflow — `workflow-js-src-context-context-ts`;
  для Developer API — `docs-api-reference-*` і `docs-devops-developer-api-*` (метод, адреса, параметри, поля
  відповіді зі шматка OpenAPI).
- **Kafka.** Продукт закрито 11.03.2025, розділ прибрано з сайту 06.05.2025; тут він із коміту перед видаленням
  (`docs-kafka-*`), плюс `@upstash/kafka` (`kafka-js-*`, архів), `kafka-examples` і README конекторів Kafka Connect.
- **Context7** — окремий продукт Upstash (документація для AI-агентів): монорепозиторій з MCP-сервером, SDK, CLI
  `ctx7`, інструментами для Vercel AI SDK, плагінами; документація лише англійською (переклади відкинуто).
- **Skills** живуть двічі: у репозиторії `upstash/skills` (`skills-upstash-*`, знімок) і в теках `skills/` самих SDK
  (`redis-js-skills-*`, з версіями); текст той самий, ключі різні.
- **Тести** великих репозиторіїв (понад 30 стабільних тегів) взято з останнього випуску кожної мінорної лінії; тести
  з тек прикладів не беруться. Код і документація — з усіх стабільних тегів.
- **npm.** Таблиці версій беруть усі версії з реєстру, крім збірок `-ci.<коміт>` (у `@upstash/redis` їх понад тисячу);
  README — лише стабільних версій. У 20 пакетів реєстр не віддає README в описі — README узято з tarball.

## Межі, про які треба пам'ятати

- Лише стабільні випуски SDK: alpha, beta, rc, canary і next не взято (у таблицях версій npm вони є).
- Сервер Redis (команди зсередини, `redis.conf`, збереження, Sentinel, Cluster) — примірник `redis`; клієнти — `ioredis` і
  `node-redis`; черги — `bullmq`.
- Керовані Redis інших хмар (ElastiCache, Azure Cache, Redis Cloud), Vercel KV як продукт Vercel — поза межами.
- Демо-застосунки Upstash (wikipedia-semantic-search, degree-guru, botstreet, hacker-trends тощо), jstack, форки й
  сторонні пакети npm зі словом «upstash» — не взято.
- У `@upstash/chatbox`, `edge-flags`, `feedback`, `react-ui` README в tarball немає (28-байтова заглушка); релізів
  Python SDK Box, панелі edge-flags і плагіна Strapi на GitHub немає.

## Родина Redis: піднімати разом

Цей примірник — частина родини Redis: сервер, два клієнти для Node.js, черги поверх них і керована платформа. Питання
про `@upstash/redis` впирається в команду сервера, питання про чергу — у клієнт. Тому примірники родини підіймають у
Claude Code разом, а `.mcp.json` цієї теки перелічує всі п'ять серверів: підключивши будь-який із них, Claude Code
бачить решту.

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

**Де тексти.** В архіві `~/archives/docfactory/upstash-corpus-2026-10-16.tar.gz` (198 МБ: 14 432 тексти, паспорт і
сховище сирого `raw/`; перед видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на цій
машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/upstash-corpus-РРРР-ММ-ДД.tar.gz -C instances/upstash corpus raw
find instances/upstash/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/upstash/raw
gzip -9 -c instances/upstash/index/passages.json > instances/upstash/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/upstash-corpus-2026-10-16.tar.gz -C instances/upstash
./df upstash smoke
```

**Оновлення.** Сайт, блог, приклади і skills — знімки: `./df upstash refresh site-redis blog …` перечитує їх (для блогу,
skills і знімків репозиторіїв спершу замінити SHA коміту в `tags` джерела). Новий випуск SDK дописують першим рядком у
`tags` джерел `<репозиторій>-docs` і `<репозиторій>-src` («"v1.40.0": "redis-1.40.0"»), у `<репозиторій>-tests` — заміняють
тег своєї мінорної лінії; для монорепозиторіїв — тег пакета («"@upstash/box@0.8.0": "box-0.8.0"»). Релізи, таблиці
версій npm і PyPI та README нових версій підхоплюються самі. Оголошення (371 джерело) зібране скриптом за переліками
тегів — простіше дописати теги, ніж переписувати. Далі `./df upstash refresh`, `manifest`, `vectors`, `smoke`, `quality`.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df upstash …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md,
розділ «Спільне середовище». Свій `.env` примірник тримає в `instances/upstash/.env` (`cp .env.example .env`;
для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`, береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df upstash sources --why   # перелік джерел і білий список
./df upstash refresh         # завантажити все задеклароване (близько 1,5 години чотирма процесами: сайт і блог, npm і PyPI, великі репозиторії, решта)
./df upstash manifest        # оновити паспорт
./df upstash setup           # Qdrant чи пошук лише по словах
./df upstash vectors         # залити корпус у docs-upstash (близько 2 годин: 53 тисячі фрагментів)
./df upstash smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df upstash serve       # порт 8849
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8849/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user upstash-docs http://127.0.0.1:8849/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `upstash-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера.
