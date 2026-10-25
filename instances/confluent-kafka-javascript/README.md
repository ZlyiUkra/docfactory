# confluent-kafka-javascript — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Confluent JavaScript Client for Apache Kafka — пакет
`@confluentinc/kafka-javascript`, клієнт Kafka для Node.js від Confluent на бібліотеці librdkafka (репозиторій
confluentinc/confluent-kafka-javascript, посібник на docs.confluent.io) — за документацією всіх стабільних версій. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Примірник — третій у родині Kafka: сервер окремо (`kafka`), кожен клієнт Node окремо, як у родинах Redis і Mongo. Перед
ним — `kafkajs`, далі — `@platformatic/kafka`.

Клієнт Confluent — обгортка над librdkafka з двома API: проміфікованим, сумісним із KafkaJS (блок `kafkaJS` у
конфігурації), і callback API, сумісним із node-rdkafka. Confluent пропонує його як заміну обом; сторінка переходу
перелічує кожну опцію й метод KafkaJS, що поводиться інакше. Близько 660 тисяч завантажень за тиждень до 25.10.2026,
лінія 1 — уся: 1.10.0 — близько 22 %, 1.10.x — 31 %, 1.9.x — 20 %, 1.8.2 — 13 %, 1.3.2 — 12 %; найновіша 1.11.0 від
07.10.2026. Node.js 18 і новіший.

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Посібник docs.confluent.io, по одному на кожен текст | 3 | 1.0–1.11 | `overview.md` сайту |
| Сторінка переходу з KafkaJS і node-rdkafka | 1 | 1.0–1.11 | `migration.md` сайту |
| Документи репозиторію, кожен неповторний текст один раз | 17 | 15 тегів 0.2.1–1.11.0 | INTRODUCTION, MIGRATION, QUICKSTART, CONTRIBUTING, README Schema Registry |
| README пакета | 20 | стабільні версії npm | tarball кожної версії |
| Властивості конфігурації librdkafka | 7 | стабільні версії npm | `deps/librdkafka/CONFIGURATION.md` у tarball |
| Журнал змін | 27 | 0.1.0–1.11.0 | `CHANGELOG.md` на master |
| Реєстр npm | 3 | усі | registry.npmjs.org |

Разом 78 документів; фрагментів в індексі — 535 (`expected_passages` у `checks.json`). Замір `quality`: по словах 4 із
10, за змістом 5, разом 6, «як модель» 10 із 10. Посібник сайту й INTRODUCTION.md репозиторію розповідають ті самі теми
різними словами, тож для кожного питання в цілі обидва; промахи першої десятки — питання без жодного слова
документації («all-or-nothing step» замість transactions, «tokens issued by an identity provider» замість OAUTHBEARER).
Друга десятка — назвами документації, як шукає модель за промптом, — влучає всюди.

Чому властивості librdkafka. Конфігурація клієнта — це властивості librdkafka (`bootstrap.servers`,
`enable.auto.commit`, `linger.ms`…) тієї версії, що лежить у пакеті; їх опис — `CONFIGURATION.md` самої librdkafka, і
пакет кожної версії несе свою копію. Решти документації librdkafka (C API, INTRODUCTION) тут немає.

Чого немає. Документації самого Apache Kafka (примірник `kafka`), KafkaJS (примірник `kafkajs`), node-rdkafka, Confluent
Cloud, C API librdkafka. Довідки JSDoc з docs.confluent.io, типів `.d.ts` і прикладів `examples/`.

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа. Самих
  текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`, розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.mcp.json` — запис HTTP-сервера для Claude Code. `ANTHROPIC_API_KEY` (лише для кроку `ask`) і `GITHUB_TOKEN` (лише
  для завантаження корпусу) беруться з кореневого `.env`.

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df confluent-kafka-javascript <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| посібник і перехід | `overview.md` і `migration.md` на docs.confluent.io/kafka-clients/javascript/<версія>/ | `mdpage` |
| документи репозиторію | дерева 15 тегів `vX.Y.Z` confluentinc/confluent-kafka-javascript | `ghdocs-history` |
| README, CONFIGURATION.md | tarball `@confluentinc/kafka-javascript` кожної стабільної версії | `npm-tarball-files` |
| журнал змін | `CHANGELOG.md` на master | `changelog-regex` |
| реєстр npm | registry.npmjs.org | `npm-versions` |

Нових читачів не додавалося. Дві правки спільного коду: `mdpage` упізнає назву сторінки, перед якою стоять якорі
`<a id="…"></a>` (так markdown-двійник docs.confluent.io починає кожну сторінку), а `split_long_tables` ріже й таблицю
без крайніх рисок `|` (CONFIGURATION.md librdkafka) — без цього вся таблиця властивостей була одним уривком на 60 тисяч
символів. Теги репозиторію записано в `sources.json` (ключ — коміт тегу); тег `v2.16.0` — спадок node-rdkafka, від якого
відгалужено репозиторій, і не береться.

## Версії

Версія — номер випуску; документи репозиторію мають версію тегу, з якого взято (остання латка мінорної), сторінки
docs.confluent.io — версії сайту, де стояв саме цей текст (посібник мінявся двічі: у 1.6 і в 1.11; сторінка переходу
однакова в усіх). Фільтр `version` бере мажор (`"1"`), мінор (`"1.10"`) або точну версію (`"1.10.1"`). На питання «як це
зробити зараз» промпт велить шукати для 1.10 (найбільше завантажень), а про нове — ще й для 1.11. Сторінка, що не змінилася між версіями, — один документ з усіма ними, тож перелік версій уривка сам показує,
відколи й доки документація казала саме це.

## Родина Kafka: піднімати разом

Цей примірник — частина родини Kafka: сам Apache Kafka і три клієнти для Node.js. Питання про клієнта впирається в
поведінку брокера (`acks`, `min.insync.replicas`, ребаланс груп, транзакції), а питання про брокер часто звучить мовою
клієнта. Тому примірники родини піднімають у Claude Code разом, а `.mcp.json` цієї теки перелічує всі чотири сервери:
підключивши будь-який із них, Claude Code бачить решту.

| Примірник | Сервер | Порт | Що |
|-----------|--------|-----:|----|
| `kafka` | `kafka-docs` | 8886 | сам Apache Kafka 0.7–4.4: брокери, KRaft, конфігурація, протокол, Connect, Streams |
| `kafkajs` | `kafkajs-docs` | 8887 | клієнт KafkaJS для Node.js (на ньому транспорт Kafka NestJS) |
| `confluent-kafka-javascript` | `confluent-kafka-javascript-docs` | 8888 | клієнт Confluent `@confluentinc/kafka-javascript` на librdkafka |
| `platformatic-kafka` | `platformatic-kafka-docs` | 8889 | клієнт `@platformatic/kafka` на чистому TypeScript |

`prompts/loaded.txt` каже моделі, що цей набір — частина родини, і які сервери її доповнюють. Повний перелік родин — у
розділі «Родини примірників» кореневого [README](../../README.md).

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/confluent-kafka-javascript-corpus-2026-10-25.tar.gz` (78 текстів, паспорт і сховище
сирого `raw/`; перед видаленням текстів розпакований окремо й звірений із диском) і в копії на Windows-диску
`C:\Distr\confluent-kafka-javascript-corpus-2026-10-25.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/confluent-kafka-javascript/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/confluent-kafka-javascript-corpus-РРРР-ММ-ДД.tar.gz -C instances/confluent-kafka-javascript corpus raw
find instances/confluent-kafka-javascript/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/confluent-kafka-javascript/raw
gzip -9 -c instances/confluent-kafka-javascript/index/passages.json > instances/confluent-kafka-javascript/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти й сховище — лише після того, як
архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із ними повертається й сховище `raw/`:

```
tar -xzf ~/archives/docfactory/confluent-kafka-javascript-corpus-2026-10-25.tar.gz -C instances/confluent-kafka-javascript
./df confluent-kafka-javascript smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/confluent-kafka-javascript/index/passages.json.gz`,
далі `./df confluent-kafka-javascript vectors` заллє колекцію Qdrant (секунди на відеокарті, кілька хвилин на процесорі).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df confluent-kafka-javascript …` бере спільне середовище з кореня репозиторію (`.venvs/cpu`
або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md, розділ «Спільне
середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df confluent-kafka-javascript sources --why   # перелік джерел і білий список
./df confluent-kafka-javascript refresh         # завантажити все задеклароване (близько двох хвилин)
./df confluent-kafka-javascript manifest        # оновити паспорт
./df confluent-kafka-javascript setup           # Qdrant чи пошук лише по словах
./df confluent-kafka-javascript vectors         # залити корпус у docs-confluent-kafka-javascript
./df confluent-kafka-javascript smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df confluent-kafka-javascript serve          # порт 8888
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8888/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user confluent-kafka-javascript-docs http://127.0.0.1:8888/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `confluent-kafka-javascript-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
