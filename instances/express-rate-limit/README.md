# express-rate-limit — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про express-rate-limit — пакет npm, проміжний шар (middleware) Express,
який обмежує частоту запитів від одного клієнта, — і про шість пакетів його організації: express-slow-down,
rate-limit-redis, rate-limit-memcached, @acpr/rate-limit-postgresql, @express-rate-limit/cluster-memory-store і
ratelimit-header-parser. Відповідає за документацією всіх їхніх стабільних версій: сайтом
express-rate-limit.mintlify.app у стані на кожен реліз, README, типами й журналами змін пакетів, прикладами та
реєстром npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

README express-rate-limit і тека `docs/` гілки main уже є в примірнику express (як одна з супутніх бібліотек), але там
вони — одні з багатьох, без старих редакцій сайту, типів, реєстру й пакетів-сусідів. Тут екосистема повна й
самодостатня: middleware, усі його сховища (**сховище**, store — де лежать лічильники запитів: у пам'яті процесу, в
Redis, Memcached, PostgreSQL), уповільнення замість відмови й розбір заголовків `RateLimit` на боці клієнта — усе по
версіях, незалежно від express.

## Скільки цього

Лише стабільні версії; передрелізи (`0.0.0-typescript-beta-*` express-rate-limit, `3.0.0-pre.0` rate-limit-redis) не
беруться ніде, навіть у переліку реєстру npm.

| Пакет | Стабільних версій | Що є |
|-------|------------------:|------|
| express-rate-limit | 125 (1.0.0–8.7.1) | сайт, README, типи, журнал змін, реєстр |
| express-slow-down | 19 (1.0.1–3.1.1) | README, типи, журнал змін, реєстр |
| rate-limit-redis | 30 (1.0.0–6.0.1) | README, типи, журнал змін, реєстр |
| rate-limit-memcached | 8 (0.1.0–1.0.1) | README, типи, журнал змін, реєстр |
| @acpr/rate-limit-postgresql | 10 (1.0.1–1.4.1) | README, типи, журнал змін, реєстр |
| ratelimit-header-parser | 3 (0.1.0–0.2.1) | README, типи, приклади, реєстр (журналу змін немає) |
| @express-rate-limit/cluster-memory-store | 6 (0.1.0–0.3.1) | README, типи, журнал змін, приклад, реєстр |

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Сайт express-rate-limit.mintlify.app: знімки на кожну стабільну версію | 65 | 7.1.1–8.7.1 (33) | тека `docs/` репозиторію |
| README express-rate-limit: кожен неповторний текст один раз, з усіма версіями | 72 | 1.0.0–8.7.1 (124) | tarball кожної версії npm |
| Типи express-rate-limit | 36 | 6.0.0–8.7.1 (61) | tarball |
| Журнал змін express-rate-limit, по документу на версію | 60 | 2.x–8.7.1 | `docs/reference/changelog.mdx` гілки main |
| Реєстр npm express-rate-limit: огляд і лінії 1–8, з вимогами до Node (`engines`) | 9 | усі | registry.npmjs.org |
| README шести пакетів-сусідів | 44 | усі, крім rate-limit-redis 1.0.0–1.0.3 | tarball |
| Типи шести пакетів-сусідів | 25 | ті, що їх постачають | tarball |
| Журнали змін п'яти пакетів-сусідів | 50 | | `changelog.md` гілок main |
| Реєстр npm шести пакетів-сусідів | 20 | усі | registry.npmjs.org |
| Приклади ratelimit-header-parser і cluster-memory-store | 10 | | репозиторій на коміті кожної версії |

Разом 391 документ; фрагментів в індексі — 1098 (`expected_passages` у `checks.json`).

Замір `quality` на першому корпусі: по словах 5 із 10, за змістом 7, разом 8; десятка «як модель» — 10 із 10.
`max_per_doc` лишено 0: з 1 і 2 «як модель» падає до 9, з 3 — без змін.

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа.
  Самих текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`, розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — ключ Anthropic (лише для кроку `ask`) і токен GitHub (лише для завантаження корпусу); `.mcp.json` —
  запис HTTP-сервера для Claude Code.
- `.venv/` — власний venv примірника; `requirements.txt` — його склад.

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через
`./df express-rate-limit <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт | тека `docs/` репозиторію `express-rate-limit/express-rate-limit`, гілка `main`; знімок — вершина гілки перед виходом наступної версії | `ghsite-dated` |
| README | tarball `registry.npmjs.org/<пакет>/-/<пакет>-X.tgz` | `npm-tarball-files` |
| типи | той самий tarball: головний файл `.d.ts` | `npm-tarball-files` |
| журнали змін | `docs/reference/changelog.mdx` express-rate-limit, `changelog.md` сусідів, гілки `main` | `changelog-linked`, новий |
| приклади | `examples/` і `example/` репозиторію на коміті (`gitHead`) кожної версії | `npm-githead-files` |
| реєстр npm | registry.npmjs.org, одне звернення на пакет | `npm-versions` |

Читач `changelog-linked` додано разом із цим примірником (`engine/readers/changeloglinked.py`): журнали організації
пишуть версію як `## [8.7.1](…)` (номер — посилання на реліз), без дати, а express-slow-down ще й `## v3.1.1` —
жоден наявний читач такого заголовка не впізнає. Особливості корпусу:

- **Сайт є лише з лінії 7.x.** Тека `docs/` з'явилася 20.10.2023; до того (1.x–7.0) повна документація — налаштування,
  сховища, приклади — жила в README, тож для старих версій питання знаходять README. З 7.1 README короткий і
  відсилає на сайт. Сторінку журналу змін зі знімків сайту відкинуто: журнал — окреме джерело, поділене на версії.
- **Підсумки старих ліній.** Журнал express-rate-limit описує 2.x, 3.x, 4.x і 5.x одним записом на лінію: документ
  має версію «4.x», і фільтр «4» його знаходить.
- **Вимога до Node (`engines`)** записана в документах реєстру npm: express-rate-limit 7.x і 8.x — Node 16; у 6.x вона
  стрибала (12.9 у 6.0.0–6.0.2 і 6.3.0–6.7.0, 14 у 6.0.3–6.2.x і від 6.7.1); 5.x і старші її не оголошують. Там же —
  peer-залежності сховищ: яка версія сховища з якою express-rate-limit працює.
- **Типи.** express-rate-limit постачає їх з 6.0 (6.0.0–6.0.1 — `dist/cjs/types.d.ts`, далі — `dist/index.d.ts`);
  у сусідів — з переходу на TypeScript (express-slow-down 2.0, rate-limit-redis 3.0). У @acpr/rate-limit-postgresql
  1.0–1.2 головний файл лише реекспортує модулі, повні оголошення — з 1.3.
- **Документ — неповторний текст.** Версії, де файл не змінився, ділять один документ; у рядку `# версія:` стоять усі.
- **Номери ліній у кожного пакета свої.** Фільтр `version: "8"` бере 8.x express-rate-limit, але й будь-яку 8.x
  іншого пакета; питання про сусідів шукають без фільтра, з назвою пакета в запиті (так і сказано в описі пошуку).

## Межі, про які треба пам'ятати

Документації Express, клієнтів Redis, Memcached і PostgreSQL, чернеток IETF про заголовки `RateLimit` і Node.js тут
немає, як і інших проміжних шарів безпеки (helmet, cors). Код бібліотек (`source/`) і міграції SQL сховища PostgreSQL
не входять — лише документація. Не взято також: вікі репозиторію (лише сторінки «Moved to mintlify» і застарілі коди
помилок, які тепер на сайті), релізи GitHub (повторюють журнал змін), `security.md`, `contributing.md` і
`code_of_conduct.md` репозиторіїв (порядок участі в розробці; для express-rate-limit він є на сайті).

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/express-rate-limit-corpus-2026-10-09.tar.gz` (391 текст і паспорт).
В історії git текстів немає ніде. Архів лежить лише на цій машині.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/express-rate-limit-corpus-2026-10-09.tar.gz -C instances/express-rate-limit
./df express-rate-limit smoke
```

**Як знову винести** — після оновлення, коли `vectors` і `smoke` пройшли (вони ж збирають свіжий кеш):

```
ls -l instances/express-rate-limit/index/passages.json           # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/express-rate-limit-corpus-РРРР-ММ-ДД.tar.gz -C instances/express-rate-limit corpus
find instances/express-rate-limit/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/express-rate-limit/index/passages.json > instances/express-rate-limit/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти» і «Як повернути тексти».

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати:
`gunzip -k instances/express-rate-limit/index/passages.json.gz`, далі `./df express-rate-limit vectors` заллє колекцію
Qdrant (близько трьох хвилин).

## Установка venv

```
cd instances/express-rate-limit
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df express-rate-limit sources --why   # перелік джерел і білий список
./df express-rate-limit refresh         # завантажити все задеклароване (близько 12 хвилин)
./df express-rate-limit manifest        # оновити паспорт
./df express-rate-limit setup           # Qdrant чи пошук лише по словах
./df express-rate-limit vectors         # залити корпус у docs-express-rate-limit
./df express-rate-limit smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df express-rate-limit serve          # порт 8812
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8812/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user express-rate-limit-docs http://127.0.0.1:8812/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `express-rate-limit-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
