# opentelemetry — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про OpenTelemetry — відкритий стандарт і набір інструментів для трас,
метрик, журналів подій і профілів: API і SDK мов (насамперед JavaScript для Node.js і браузера), поширення контексту й
baggage, ресурси, вибірка, експортери, протокол OTLP, семантичні домовленості, автоматична інструментація й
OpenTelemetry Collector. Документація — увесь англійський сайт opentelemetry.io з блогом і реєстром екосистеми,
специфікація кожного тегу 0.1–1.61, семантичні домовленості 1.21–1.44, файли `.proto` OTLP 0.3–1.11,
opentelemetry-js кожного випуску (README пакетів, посібники, код із TSDoc, тести, приклади, журнали змін), архівний
opentelemetry-js-api, 78 пакетів opentelemetry-js-contrib на кожному своєму випуску, Collector і contrib Collector
кожного випуску, декларативна конфігурація, OpAMP, `@vercel/otel` і реєстр npm ключових пакетів. Код спільний і лежить
у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

OpenTelemetry — це не одна бібліотека, а десяток репозиторіїв із власною нумерацією: специфікація 1.61, семантичні
домовленості 1.44, Collector 0.163, SDK для JS 2.12 разом з експериментальною лінією 0.223, API 1.9 і кожна
інструментація contrib зі своїм номером. Сайт показує лише поточний стан, а проєкти живуть на SDK 1.x і 2.x
водночас; назви атрибутів HTTP змінилися з `http.method` на `http.request.method`, і відповідь на «з якої версії»
лежить у журналах змін і коді конкретного випуску. Тут кожен випуск кожного репозиторію — окремою редакцією, з міткою
свого продукту.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Сайт opentelemetry.io: документація всіх мов, zero-code, Collector, Operator, FaaS, демо, блог | 765 | 6 676 | `open-telemetry/opentelemetry.io`, `content/en` на main |
| Реєстр екосистеми (`data/registry/*.yml`): інструментації, експортери, компоненти | 89 | 1 119 | той самий коміт сайту |
| Специфікація з OTEP і матрицею сумісності + журнал змін | 2 125 | 9 518 | `opentelemetry-specification`, 71 тег 0.1–1.61 |
| Семантичні домовленості + журнал змін | 3 131 | 13 119 | `semantic-conventions`, 26 тегів 1.21–1.44 |
| OTLP: документація, файли `.proto`, журнал змін | 205 | 722 | `opentelemetry-proto`, 33 теги 0.3–1.11 |
| opentelemetry-js: README пакетів, посібники `doc/`, журнали чотирьох ліній | 1 335 | 4 079 | `opentelemetry-js`, 143 коміти випусків |
| opentelemetry-js: код `src/` із TSDoc | 6 938 | 16 994 | ті самі коміти |
| opentelemetry-js: тести | 3 861 | 19 997 | ті самі коміти |
| opentelemetry-js: приклади, інтеграційні тести | 454 | 861 | ті самі коміти стабільної лінії |
| opentelemetry-js-api (архівний): документація, код, тести | 227 | 672 | `opentelemetry-js-api`, 15 тегів 0.17–1.2 |
| js-contrib: README і документація 78 пакетів | 917 | 1 867 | `opentelemetry-js-contrib`, 145 комітів випусків |
| js-contrib: код `src/` | 2 977 | 6 562 | ті самі коміти |
| js-contrib: тести | 1 888 | 8 152 | ті самі коміти |
| js-contrib: журнали змін пакетів | 3 275 | 5 207 | `CHANGELOG.md` кожного пакета |
| Collector (ядро): README компонентів, `docs/`, журнали змін і Go API | 1 687 | 4 575 | `opentelemetry-collector`, 192 випуски |
| contrib Collector: README 249 компонентів, `docs/`, журнали змін | 7 818 | 24 989 | `opentelemetry-collector-contrib`, 189 випусків |
| Декларативна конфігурація: документація, схема, приклади | 246 | 794 | `opentelemetry-configuration`, 10 тегів |
| OpAMP: специфікація, `.proto` | 50 | 1 042 | `opamp-spec`, 20 тегів |
| `@vercel/otel`: документація, код, журнал змін | 69 | 211 | `vercel/otel` |
| Реєстр npm 22 ключових пакетів | 62 | 1 303 | registry.npmjs.org |

Разом 38 119 документів; фрагментів — 128 459 (`expected_passages` у `checks.json`). Замір `quality` (10 запитів): по
словах 7, за змістом 9, разом 10.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут
  немає: корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `raw/` — сховище сирих відповідей (252 МБ): дерева й файли GitHub, журнали змін, реєстр npm. Не в git; в архіві
  разом із корпусом.
- `sources.json` — звідки корпус будується (376 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену, правила `slug_rewrite` і родина `families`.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера.

Кроки нижче запускаються з кореня фабрики через `./df opentelemetry <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| сайт opentelemetry.io | `ghdocs-history` з полем `otel_hugo` (нове): шорткоди Hugo розгортаються з файлів того самого коміту |
| реєстр екосистеми | `otel-registry` — новий: записи групами за типом і мовою, запис — розділ |
| специфікація, домовленості, документація репозиторіїв | `ghdocs-history` з полем `lead_comment` (нове) |
| код і тести TypeScript, схема конфігурації | `ghcode-history-ts` (нове поле `max_file`), `ghcode-history` |
| файли `.proto` OTLP і OpAMP | `ghcode-history-proto` — новий: розділ на кожне `message`, `enum`, `service` |
| журнали змін усіх репозиторіїв | `changelog-otel` — новий: п'ять видів заголовка версії, подвійний номер Collector |
| реєстр npm | `npm-versions` |

Особливості:

- **Шорткоди сайту.** Сторінка opentelemetry.io у репозиторії — не те, що бачить людина: номери версій приходять
  через `{{% param vers %}}` з `cascade` розділу чи `hugo.yaml`, спільні шматки — через `{{% include %}}` з тек
  `_includes`, вступ сторінки мови — із шаблону шорткода й `data/instrumentation.yaml`, версії пакетів — із записів
  реєстру, команди npm/yarn/pnpm і TypeScript/JavaScript — у вкладках. `_otelhugo.py` розгортає все це; залишки
  `{{…}}` лишилися на 8 сторінках, і всі вони — справжні шаблони в прикладах коду (Helm, Go-шаблони).
- **Шапка Hugo в коментарі.** Специфікація й домовленості з 2023 року починають кожен файл коментарем
  «`<!--- Hugo front matter … --->`»; без поля `lead_comment` назвою документа ставало ім'я файла («sdk»).
- **Мітки версій** — з назвою продукту, щоб нумерації не змішувались: стабільна лінія SDK JS — голий номер
  (`2.12.0`, `1.30.1`, `0.27.0`), решта — `api-1.9.1`, `experimental-0.223.0` (sdk-node, OTLP-експортери, logs,
  instrumentation), `semantic-conventions-1.43.0` (пакет констант JS), `spec-1.61.0`, `semconv-1.44.0`,
  `proto-1.11.1`, `collector-0.163.0` (ядро й contrib — одна лінія випусків), `configuration-1.2.0`, `opamp-0.20.0`,
  `vercel-otel-2.1.3`; пакети js-contrib — своєю назвою (`instrumentation-express-0.71.1`), до release-please (2021)
  — спільне `contrib-0.24.0`; таблиці npm — `npm-sdk-node-0.223.0`. Лінія в переліку — мажор продукту
  (`spec-1`, `collector-0`, `experimental-0`). Сторінки сайту й реєстр версії не мають.
- **Випуски монорепозиторіїв — за комітом.** У js-contrib 3 396 тегів 78 пакетів стоять на 145 комітах, у Collector
  7 094 теги модулів — на 195, у contrib Collector 37 946 — на 236. Дерево береться раз на коміт випуску, а кожен
  пакет js-contrib — окремими джерелами з тегами саме своїх випусків, тож README `instrumentation-pg` має версії
  `instrumentation-pg-…`, а не сусідів по коміту.
- **Переїзди файлів зливаються.** Пакети js-contrib переїхали з `plugins/node/opentelemetry-instrumentation-*` у
  `packages/instrumentation-*` (64 правила `slug_rewrite`). Семантичні домовленості до 1.21 жили в специфікації, а в
  `semantic-conventions` теж переїжджали (`database/` → `db/`): 73 правила за назвами документів (лише пари, що ніколи
  не співіснували в одній версії) і родина `families` `semconv` зі `spec` і `semconv`. Стара й нова редакція займають
  одне місце у видачі, показується найновіша. Розділи HTTP з однофайлових домовленостей специфікації 0.1–0.3
  зливаються з `http-spans` теж.
- **Журнали Collector** пишуть подвійний номер «v1.69.0/v0.163.0» (стабільні модулі й решта); версією стає лінія
  0.x, якою нумеруються випуски. Журнал Go API (`CHANGELOG-API.md`) названо окремо (`collector-api-0.163.0`).
- **Знятий з main пакет contrib** (fastify, redis-4, react-load, propagation-utils, browser-extension-autoinjection,
  grpc-census-binary, resource-detector-docker) — журнал змін із коміту його останнього випуску.
- **Версія за замовчуванням** за завантаженнями npm: SDK 2.x (81–84 %, 1.x — 15–18 %), API 1.x (99 %) — коли версію
  не названо, відповідь для SDK 2.x і рядок, де 1.x інакше.

## Межі, про які треба пам'ятати

- Сайт — знімок поточного стану, версій не має; переклади (uk, ja, zh…) не взято.
- Репозиторії SDK інших мов (Java, Python, Go, .NET…) не взято: їхні сторінки на сайті — є, коду й журналів — немає.
- Код Collector (Go) не взято: лише README компонентів, `docs/` і журнали змін.
- GitHub Releases не взято: у всіх репозиторіях вони дослівно повторюють журнали змін.
- Jaeger, Prometheus, Grafana й бекенди постачальників — поза примірником.
- Файли коду понад 150 КБ не беруться (згенеровані константи `@opentelemetry/semantic-conventions` — їх зміст є в
  самих домовленостях).
- 35 «збоїв» `build` — порожні в самому журналі записи версій (наприклад, Collector 0.146.1).

## Архівний режим: сервер без корпусу

Корпус в архіві від дня збирання: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/opentelemetry-corpus-2026-10-17.tar.gz` (234 МБ:
38 119 текстів, паспорт і сховище сирого `raw/` — 35 958 файлів; перед видаленням розпакований окремо й звірений з
диском — нуль розбіжностей). Лише на цій машині.

**Як винести** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/opentelemetry-corpus-РРРР-ММ-ДД.tar.gz -C instances/opentelemetry corpus raw
find instances/opentelemetry/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/opentelemetry/raw
gzip -9 -c instances/opentelemetry/index/passages.json > instances/opentelemetry/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/opentelemetry-corpus-2026-10-17.tar.gz -C instances/opentelemetry
./df opentelemetry smoke
```

**Оновлення.** Новий випуск — новий коміт у `tags` відповідних джерел (ключ — повний SHA коміту випуску, значення —
мітки всіх тегів на ньому). Журнали змін і npm підтягуються самі. Мережею тягнуться лише дерева й журнали, а файли —
із голих клонів:

```
git clone --bare https://github.com/open-telemetry/opentelemetry-js.git      # і решта репозиторіїв з sources.json;
git clone --bare --filter=blob:none https://github.com/open-telemetry/opentelemetry-collector-contrib.git
./df opentelemetry list                                                      # дерева через API (~800 запитів)
instances/opentelemetry/.venv/bin/python tools/seed_git_store.py --instance opentelemetry \
    --clone open-telemetry/opentelemetry-js=/шлях/opentelemetry-js.git …    # файли з клонів у сховище
./df opentelemetry build
./df opentelemetry manifest
```

Далі `vectors` (лише змінені фрагменти), `smoke`, `quality`.

## Установка venv

```
cd instances/opentelemetry
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df opentelemetry sources --why   # перелік джерел і білий список
./df opentelemetry list            # дерева комітів, журнали змін і npm — у сховище сирого (~12 хв)
# засів файлів із голих клонів — tools/seed_git_store.py (див. «Оновлення» вище; секунди)
./df opentelemetry build           # корпус зі сховища, без мережі (~5 хв)
./df opentelemetry manifest        # оновити паспорт
./df opentelemetry setup           # Qdrant чи пошук лише по словах
./df opentelemetry vectors         # залити корпус у docs-opentelemetry (~5 годин: 128 тисяч фрагментів)
./df opentelemetry smoke           # перевірки
```

Без клонів `./df opentelemetry refresh` тягне все мережею по файлу — це десятки годин.

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df opentelemetry serve         # порт 8853
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8853/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user opentelemetry-docs http://127.0.0.1:8853/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Так само через `.mcp.json` цієї теки.

**3. Перевірити.** `/mcp` — має бути `opentelemetry-docs` і два інструменти `search_docs`, `read_section`. Зайнятий
порт видно одразу: `serve` падає з «address already in use»; невдале з'єднання — у `/mcp` сервер червоний, тоді
перевірте, що `serve` живий.

Зупинка — Ctrl+C у терміналі сервера.
