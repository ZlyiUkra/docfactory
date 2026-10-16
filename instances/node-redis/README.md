# node-redis — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про node-redis — офіційний клієнт Redis для Node.js (пакет `redis` з
`@redis/client`, `@redis/json`, `@redis/search`, `@redis/time-series`, `@redis/bloom`, `@redis/entraid`): `createClient`
і його опції, методи команд з типами аргументів і відповідей, транзакції multi/exec і WATCH, конвеєри, pub/sub, ітератори
SCAN, кластер і Sentinel, пул підключень, RESP2 і RESP3, кешування на боці клієнта, скрипти й функції, автентифікація
Entra ID, метрики OpenTelemetry. Документація — кожного стабільного випуску від 0.3.5 до 6.3.0: README (у 0.x–3.x — увесь
довідник API), посібники `docs/`, журнал змін, приклади й doctests, код клієнта й модулів (для 4.x–6.x це і є довідник),
тести останнього випуску кожної мінорної лінії, нотатки релізів GitHub, README пакетів з npm і типи спільноти
`@types/redis`. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

node-redis тричі міняв API: 3.x з колбеками, 4.x з промісами й новими іменами методів, 5.x з новим API опцій команд і
пулом, 6.x; на проді живуть усі. README на GitHub показує лише головну гілку, довідник 4.x–6.x існує лише як код з типами.
Тут кожен випуск — окремою редакцією: «як називався `hGetAll` у 3.1» чи «що повертає `multi.exec()` у 4.6» береться з
документів тієї версії. Сервер Redis (команди, `redis.conf`) — примірник `redis`; ioredis і BullMQ — окремі примірники.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| README, `docs/` (20 посібників), CHANGELOG, SUPPORTED_REDIS_VERSIONS, CONTRIBUTING, SECURITY | 162 | 898 | `redis/node-redis`, 129 тегів |
| Код клієнта `packages/client/lib`, `lib/`, `index.js` | 2 406 | 5 721 | ті самі теги |
| Код модулів json, search, time-series, bloom, graph, entraid | 926 | 1 892 | ті самі теги |
| Тести `*.spec.ts`, `test/` | 1 971 | 7 745 | останній випуск 41 мінорної лінії |
| Приклади `examples/`, `doctests/` | 219 | 477 | 129 тегів |
| Нотатки релізів | 149 | 328 | GitHub Releases (з 1.0.0) |
| README `redis` з npm (усі 159 версій, і 30 без тегу) | 64 | 433 | tarball кожної стабільної версії |
| README `@redis/*`, `@node-redis/*` (13 пакетів) | 21 | 67 | ті самі |
| `@types/redis` (`index.d.ts`) | 41 | 138 | ті самі |

Разом 6 089 документів; фрагментів — 17 699 (`expected_passages` у `checks.json`). Замір `quality` (10 запитів): по
словах 10, за змістом 9, разом 10. `max_per_doc` 0 (1–3 дають те саме).

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (21 джерело), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df node-redis <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| README, `docs/`, журнал, README прикладів | `ghdocs-history` |
| код клієнта й модулів, приклади, тести | `ghcode-history-ts` (розділи — за класами, функціями, типами, `describe`/`it`) |
| нотатки релізів | `ghreleases` (пре-релізи відкинуто за `skip`) |
| README пакетів, `@types/redis` | `npm-tarball-files` |

Нового читача не знадобилось; у `ghreleases` розширено шаблон тега: випуски 2.x позначені `v.2.6.0` (крапка після `v`),
і без цього вони лишались без версії.

Особливості:

- **Імена документів.** `readme`, `changelog`, `docs-clustering`, `docs-v4-to-v5`; код —
  `src-packages-client-lib-client-index-ts`, `src-packages-client-lib-commands-hset-ts` (по файлу на команду),
  `src-lib-individualcommands-js` (3.x), `src-index-js` (0.x–3.x); модулі — `modules-packages-search-lib-commands-search-ts`;
  тести — `test-packages-client-lib-client-index-spec-ts`; релізи — `node-redis-redis-5.0.0`, `node-redis-v.2.6.0`;
  npm — `redis-markdown`, `at-redis-search-markdown`, `types-redis-types`.
- **Мітки версій.** Кожен документ несе всі випуски `redis`, де файл був саме таким; `@redis/client` 1.x відповідає
  redis 4.x. Перелік ліній у відповіді сервера — мінорний (`version_line_depth: 2`): 0.3, …, 4.7, 5.0, …, 6.3. Фільтр
  `version: "4"` лишає всі 4.x, `"5.1"` — 5.1.x.
- **Де довідник API.** У 0.x–3.x — README; з 4.0 README став вступом, а довідник — код: опції клієнта в
  `src-packages-client-lib-client-index-ts` і `…-socket-ts`, кожна команда у своєму файлі з типами аргументів і
  відповіді, посібники `docs/` про кластер, Sentinel, pub/sub, транзакції, пул, ітератори, програмованість, RESP і
  міграції v3 → v4 → v5 → v6.
- **Три форми тегів** у репозиторії (`v0.3.5`, `v.2.8.0`, `redis@4.0.0`) — усі зведено до версії пакета `redis`;
  30 версій npm без тегу (ранні 0.x, 2.2.1, 3.0.1, 5.5.5) покриті README з tarball.
- **Тести** взято з останнього випуску кожної з 41 мінорної лінії, а не з усіх 129 тегів.
- **Порожні README** `@redis/graph` 1.0.1, `@node-redis/bloom` 1.0.1 і `@node-redis/graph` 1.0.0 (лише заголовок) читач
  відкинув.

## Межі, про які треба пам'ятати

- Лише стабільні випуски: next, rc, beta і нумеровані пре-релізи (`v.2.6.0-0`, `2.5.0-1`) не взято.
- Документація самого Redis (команди, `redis.conf`, Sentinel і Cluster зсередини) — примірник `redis`; сторінки
  node-redis на redis.io (`develop-clients-nodejs-*`) теж там.
- `@types/redis` 4.0.x — заглушка без типів, у корпус не потрапила; для redis 4+ типи вбудовані.
- Сайт redis.io і сайти модулів (RedisJSON, RediSearch) — поза межами; тут лише те, що каже сам клієнт.

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/node-redis-corpus-2026-10-16.tar.gz` (43 МБ: 6 089 текстів,
паспорт і сховище сирого `raw/`; перед видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на
цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/node-redis-corpus-РРРР-ММ-ДД.tar.gz -C instances/node-redis corpus raw
find instances/node-redis/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/node-redis/raw
gzip -9 -c instances/node-redis/index/passages.json > instances/node-redis/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/node-redis-corpus-2026-10-16.tar.gz -C instances/node-redis
./df node-redis smoke
```

**Оновлення.** Новий випуск дописують першим рядком у `tags` джерел `node-redis-docs`, `node-redis-examples`,
`node-redis-src`, `node-redis-modules-src` («"redis@6.3.1": "6.3.1"»), а в `node-redis-tests` — заміняють тег своєї
мінорної лінії на новіший; нові версії пакетів npm підхоплюються самі. Далі `./df node-redis refresh`, `manifest`,
`vectors`, `smoke`, `quality`.

## Установка venv

```
cd instances/node-redis
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df node-redis sources --why   # перелік джерел і білий список
./df node-redis refresh         # завантажити все задеклароване (близько 35 хвилин)
./df node-redis manifest        # оновити паспорт
./df node-redis setup           # Qdrant чи пошук лише по словах
./df node-redis vectors         # залити корпус у docs-node-redis (близько 35 хвилин)
./df node-redis smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df node-redis serve       # порт 8847
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8847/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user node-redis-docs http://127.0.0.1:8847/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `node-redis-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера.
