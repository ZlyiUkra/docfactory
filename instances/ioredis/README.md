# ioredis — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про ioredis — повнофункціональний клієнт Redis для Node.js: підключення
standalone, Sentinel і Cluster, опції й події, конвеєри й автоконвеєр, транзакції, pub/sub і sharded pub/sub, потоки,
`scanStream`, скрипти Lua через `defineCommand`, TLS, черга офлайн і перепідключення, вбудовані типи TypeScript.
Документація — кожного стабільного випуску від 1.0.0 до 6.0.0: README (посібник), довідник `API.md` (2–4), журнал змін,
приклади, код `lib/` з коментарями JSDoc (для 5.x і 6.x це і є довідник — з нього генерується сайт TypeDoc), тести
останнього випуску кожної мінорної лінії, нотатки релізів GitHub, `@ioredis/commands` і типи спільноти `@types/ioredis`.
Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

README ioredis на GitHub показує лише головну гілку, а на проді живуть 4.x і 5.x одночасно: опція `retryStrategy`
чи поведінка `maxRetriesPerRequest` за замовчуванням (20) мінялися між 3 → 4 → 5, `API.md` зник у 5.0, і єдине
джерело сигнатур 5.x–6.x — код і TypeDoc. Тут кожен випуск — окремою редакцією: відповідь «що повертає
`cluster.nodes('slave')` у 4.28» береться з коду 4.28, а не з пам'яті. Сервер Redis (команди, `redis.conf`) — примірник
`redis`; node-redis і BullMQ — окремі примірники.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| README, `API.md`, Changelog, SECURITY, CONTRIBUTING, README прикладів | 363 | 1 052 | `redis/ioredis`, 221 тег |
| Код `lib/` (з розбиттям за будовою TypeScript) | 767 | 1 981 | ті самі теги |
| Тести `test/` | 856 | 4 046 | останній випуск 70 мінорних ліній |
| Приклади `examples/` | 35 | 61 | 221 тег |
| Нотатки релізів | 155 | 337 | GitHub Releases (з 1.13.2) |
| `@types/ioredis` (`index.d.ts`) | 127 | 277 | tarball кожної стабільної версії |
| `@ioredis/commands` (README, CHANGELOG) | 6 | 10 | ті самі |

Разом 2 309 документів; фрагментів — 7 764 (`expected_passages` у `checks.json`). Замір `quality` (10 запитів): по
словах 10, за змістом 10, разом 10. `max_per_doc` 0 (1–3 дають те саме).

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (7 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df ioredis <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| README, `API.md`, журнал, README прикладів | `ghdocs-history` |
| код `lib/`, приклади, тести | `ghcode-history-ts` (розділи — за класами, методами, типами, `describe`/`it`) |
| нотатки релізів | `ghreleases` (пре-релізи відкинуто за `skip`) |
| `@ioredis/commands`, `@types/ioredis` | `npm-tarball-files` |

Нового коду для ioredis не знадобилось.

Особливості:

- **Імена документів.** `readme`, `api`, `changelog`; код — `src-lib-redis-ts`, `src-lib-cluster-clusteroptions-ts`,
  `src-lib-redis-js` (1.x–3.x писані на JavaScript, тож `.js` і `.ts` редакції одного файла — різні документи);
  тести — `test-test-functional-sentinel-ts`; релізи — `ioredis-v5.0.0`; типи — `types-ioredis-types`.
- **Мітки версій.** Кожен документ несе всі випуски, де файл був саме таким: редакція README з міткою 4.0.0–4.28.5
  описує ioredis 4. Перелік ліній у відповіді сервера — мінорний (`version_line_depth: 2`): 1.0, …, 4.28, 5.0, …,
  5.11, 6.0. Фільтр `version: "5"` лишає всі 5.x, `"4.28"` — 4.28.x.
- **Де довідник API.** `API.md` є у 2.0–4.28; з 5.0 його замінив сайт TypeDoc (HTML у `docs/`, сюди не взято — це
  рендер коду), тож для 5.x і 6.x довідник — розділи `src-lib-redis-ts`, `src-lib-redis-redisoptions-ts`,
  `src-lib-cluster-clusteroptions-ts`, `src-lib-utils-rediscommander-ts` з JSDoc над кожним методом і опцією.
- **Теги 1.x** в репозиторії без «v» (`1.9.0`) і з «v» (`v1.9.0`) для тієї самої версії — узято один раз.
- **Тести** взято з останнього випуску кожної мінорної лінії, а не з усіх 221 тегів: 856 документів замість
  кількох тисяч повторів.

## Межі, про які треба пам'ятати

- Лише стабільні випуски: бети, rc, alpha (6.1.0-beta, 5.0.0-beta, 4.0.0-0…3, 2.0.0-rc) не взято.
- Сайт TypeDoc (`docs/`, redis.github.io/ioredis) не завантажено: він генерується з `lib/`, який тут є.
- Документація самого Redis (команди, `redis.conf`, Sentinel і Cluster зсередини) — примірник `redis`; сторінки
  ioredis на redis.io (`develop-clients-ioredis-*`) теж там.
- `@types/ioredis` 5.0.0 — заглушка без типів, у корпус не потрапила; для ioredis 5+ типи вбудовані.

## Родина Redis: піднімати разом

Цей примірник — частина родини Redis: сервер, два клієнти для Node.js і черги поверх них. Питання про чергу впирається в клієнт (BullMQ працює через ioredis), питання про клієнт — у команду сервера. Тому примірники родини піднімають у Claude Code разом, а `.mcp.json` цієї теки перелічує всі п'ять серверів: підключивши будь-який із них, Claude Code бачить решту.

| Примірник | Сервер | Порт | Що |
|-----------|--------|-----:|----|
| `redis` | `redis-docs` | 8845 | сервер Redis: команди, `redis.conf`, збереження, реплікація, Sentinel, Cluster |
| `ioredis` | `ioredis-docs` | 8846 | клієнт ioredis для Node.js |
| `node-redis` | `node-redis-docs` | 8847 | офіційний клієнт node-redis (пакет `redis`) з модулями |
| `bullmq` | `bullmq-docs` | 8848 | черги BullMQ, Bull, панелі Bull Board і Arena, `@nestjs/bull*` |
| `upstash` | `upstash-docs` | 8849 | платформа Upstash: Redis по HTTP, ratelimit, QStash, Workflow, Vector, Search, Box… |

`prompts/loaded.txt` каже моделі, що цей набір — частина родини, і які сервери її доповнюють. Повний перелік родин — у розділі «Родини примірників» кореневого [README](../../README.md).

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/ioredis-corpus-2026-10-16.tar.gz` (16 МБ: 2 309 текстів,
паспорт і сховище сирого `raw/`; перед видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на
цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/ioredis-corpus-РРРР-ММ-ДД.tar.gz -C instances/ioredis corpus raw
find instances/ioredis/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/ioredis/raw
gzip -9 -c instances/ioredis/index/passages.json > instances/ioredis/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/ioredis-corpus-2026-10-16.tar.gz -C instances/ioredis
./df ioredis smoke
```

**Оновлення.** Новий випуск дописують першим рядком у `tags` джерел `ioredis-docs`, `ioredis-examples`, `ioredis-src`
(«"v6.0.1": "6.0.1"»), а в `ioredis-tests` — заміняють тег своєї мінорної лінії на новіший; нові версії
`@ioredis/commands` і `@types/ioredis` підхоплюються самі. Далі `./df ioredis refresh`, `manifest`, `vectors`, `smoke`,
`quality`.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df ioredis …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md,
розділ «Спільне середовище». Свій `.env` примірник тримає в `instances/ioredis/.env` (`cp .env.example .env`;
для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`, береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df ioredis sources --why   # перелік джерел і білий список
./df ioredis refresh         # завантажити все задеклароване (близько 15 хвилин)
./df ioredis manifest        # оновити паспорт
./df ioredis setup           # Qdrant чи пошук лише по словах
./df ioredis vectors         # залити корпус у docs-ioredis (близько 20 хвилин)
./df ioredis smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df ioredis serve          # порт 8846
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8846/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user ioredis-docs http://127.0.0.1:8846/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `ioredis-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера.
