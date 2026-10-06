# express — примірник фабрики docfactory

Тридцять перший примірник фабрики: захищений MCP-сервер, що відповідає на питання про Express — мінімалістичний
вебфреймворк для Node.js: маршрути, проміжні обробники (middleware), об'єкти запиту й відповіді. Тут сайт
expressjs.com для Express 5.x і 4.x, довідник API 3.x і документація 2.x, спільні посібники й сторінки офіційних
middleware, блог, журнал змін `History.md`, README кожної стабільної версії, нотатки релізів і реєстр версій npm.
Поруч — README кожної версії й журнали змін п'ятнадцяти офіційних middleware, маршрутизатора `router`, синтаксису
шляхів `path-to-regexp`, заголовків безпеки `helmet` і обмежувача частоти `express-rate-limit` з його документацією. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../../README.md).

## Навіщо

Express — найпоширеніший легкий бекенд на Node.js і основа, на якій стоять NestJS (типовий HTTP-адаптер) і безліч
старих проєктів. Express 5 (жовтень 2024) змінив речі, на яких тримається робочий код: відхилений проміс з
асинхронного обробника тепер сам іде в обробник помилок, синтаксис шляхів перейшов на path-to-regexp 8 (іменовані
`*splat`, без регулярних виразів у рядку шляху), частину методів і сигнатур прибрано. На день збирання 5.x і 4.x
завантажують майже порівну — 52% і 48%, — тому тут обидві лінії, а відповідь без названої версії каже про обидві.

У яких фазах і днях планів навчання він потрібен — див. [../../docs/learning-map.md](../../docs/learning-map.md).

## Скільки цього

| Шар | Документів | Звідки |
|-----|-----------:|--------|
| Сайт для Express 5.x: початок роботи, посібники, довідник API | 22 | `src/content/docs/en/5x`, `src/content/api/5x` expressjs/expressjs.com |
| Сайт для Express 4.x: те саме | 22 | `src/content/docs/en/4x`, `src/content/api/4x` |
| Довідник API Express 3.x | 5 | `src/content/api/3x` |
| Документація Express 2.x | 7 | `legacy/2x/docs` на коміті 20332bef3b7e — останній старий сайт на Jekyll |
| Спільні сторінки: найкращі практики, міграції на 4 і 5, бази даних, офіційні middleware | 30 | `src/content/pages/en` |
| Блог: релізи 5.x, оголошення про вразливості | 21 | `src/content/blog` |
| `History.md` — журнал змін усіх версій | 1 | expressjs/express, гілка master |
| README стабільних версій `express`, однакові тексти зведено | 61 | тег релізу на GitHub |
| Нотатки релізів expressjs/express | 165 | GitHub API |
| Реєстр версій npm | 7 | registry.npmjs.org |
| README 15 офіційних middleware за версіями (перелік — в «Особливостях» нижче) | 284 | тег чи коміт публікації кожної стабільної версії |
| README `router` і `path-to-regexp` за версіями | 52 | pillarjs/router, pillarjs/path-to-regexp |
| README `helmet` і `express-rate-limit` за версіями | 134 | helmetjs/helmet, express-rate-limit/express-rate-limit |
| Документація `express-rate-limit`: налаштування, сховища, API, коди помилок, журнал змін | 13 | тека `docs/`, гілка main |
| Журнали змін (`HISTORY.md`, `CHANGELOG.md`) усіх цих пакетів, крім express-rate-limit | 18 | гілка за замовчуванням кожного репозиторію |

Разом 842 документи; фрагментів в індексі — 11 961 (`expected_passages` у `checks.json`). Фрагменти — це шматки
документів між заголовками, по яких іде пошук; однаковий текст різних версій зливається в один з усіма версіями.

Замір `quality` після доповнення (06.10.2026): перша десятка (питання своїми словами) — по словах 6 із 10, за змістом
6, разом 8; друга, «як модель» (назви API, з версією «5» чи «site», як велить промпт), — 10 із 10. На першому корпусі
було 7, 7, 8 і 10: README пакетів тепер змагаються зі сторінками сайту за ті самі питання.

**Версія у відповіді.** Без названої версії — Express 5 і Express 4 разом, із тим, де вони розходяться. Фільтр
`version` — мажор: «5», «4», «3», «2». Спільні сторінки мають мітку «site», блог — «blog», `History.md` і журнали
змін пакетів — «changelog». README пакетів міряються версіями самого пакета («2.3.0» у body-parser, «8.4.2» у
path-to-regexp), документація express-rate-limit — мажором «8».

## Що в цій теці

- `corpus/` — лише паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа (тексти — в архіві,
  див. нижче).
- `index/passages.json.gz` — стиснений кеш фрагментів, з якого підіймається сервер.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — ключ Anthropic (лише для кроку `ask`) і токен GitHub (лише для завантаження); `.mcp.json` — запис
  HTTP-сервера для Claude Code.
- `.venv/` — власний venv примірника; `requirements.txt` — його склад.

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df express <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт для 5.x, 4.x, 3.x, спільні сторінки, блог | expressjs/expressjs.com, гілка main | `ghdocs-history` |
| документація 2.x | expressjs/expressjs.com, коміт 20332bef3b7e | `ghdocs-history` |
| журнал змін | `History.md` expressjs/express, гілка master | `ghdocs-history` |
| README пакета | тег релізу кожної стабільної версії на GitHub | `npm-readme` |
| нотатки релізів | GitHub API | `ghreleases` |
| версії пакета | реєстр npm | `npm-versions` |
| README middleware, `router`, `path-to-regexp`, `helmet`, `express-rate-limit` | коміт публікації чи тег кожної стабільної версії | `npm-readme` |
| журнали змін цих пакетів, документація express-rate-limit | гілка за замовчуванням кожного репозиторію | `ghdocs-history` |

Білий список — три хости: `api.github.com`, `raw.githubusercontent.com`, `registry.npmjs.org`. Сам expressjs.com не
читається: сайт збирається з репозиторію expressjs/expressjs.com. Посилання у відповідях можуть вести на сайт.

Особливості, які варто знати:

- **Сайт переписано** на Astro на початку 2026 року. Документацію 2.x новий сайт не переніс, тож вона взята з
  останнього коміту старого сайту на Jekyll (тека `legacy/2x/docs`). Довідник API 3.x на новому сайті є.
- **Офіційні middleware** — body-parser, cors, cookie-parser, express-session, cookie-session, multer, morgan,
  serve-static, compression, method-override, response-time, serve-index, connect-timeout, vhost, errorhandler — тут
  двічі: сторінки сайту в поточному стані (мітка «site») і README кожної стабільної версії самих пакетів із журналами
  змін. Версія README — версія пакета (`body-parser` 2.3.0), а не Express. Реєстрів npm і нотаток релізів цих пакетів
  тут немає: журнал змін каже те саме.
- **Найперші версії без README** пропущено: у збірках 0.0.x репозиторій його ще не мав (cors, multer, helmet та
  інші). Версії `router` 0.x на npm опубліковано не з pillarjs/router — їх теж немає.
- **`path-to-regexp`** визначає синтаксис шляхів: Express 4 стоїть на 0.1.x, Express 5 — на 8.x (іменовані `*splat`,
  необов'язкові частини у `{}`, без регулярних виразів у рядку шляху). Питання про шлях маршруту — з версією і цього
  пакета.
- **Теги релізів** старих версій пишуться без «v» (`4.18.2`), новіших — з «v»; README кожної версії читається за
  тегом, а коли реєстр записав коміт публікації, — за ним.
- **Переклади сайту** (німецький, іспанський, японський та інші) не взято: лише англійська.

## Межі, про які треба пам'ятати

Тут немає документації самого Node.js, інших фреймворків (Koa, Fastify; NestJS — окремий примірник `nestjs`),
шаблонізаторів (Pug, EJS), баз даних і ORM, Passport, сторонніх middleware поза helmet і express-rate-limit, а також
вебплатформи (HTTP, куки, CORS — примірники `mdn` і `webstandards`). Issues і GitHub Discussions свідомо не взято.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку, як у eslint: у `corpus/` лежить лише паспорт `index.json`, а сервер
підіймається з кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає
повний текст кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/express-corpus-2026-10-06-middleware.tar.gz` (0,7 МБ, 842 тексти й
паспорт; перед видаленням розпакований окремо й звірений із диском — нуль розбіжностей). Попередній архів першого
корпусу, `express-corpus-2026-10-06.tar.gz` (341 текст), лишився поруч. В історії git текстів немає ніде. Архіви
лежать лише на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/express/index/passages.json         # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/express-corpus-РРРР-ММ-ДД.tar.gz -C instances/express corpus
find instances/express/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/express/index/passages.json > instances/express/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/express-corpus-РРРР-ММ-ДД.tar.gz -C instances/express
./df express smoke
```

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/express/index/passages.json.gz`, далі
`./df express vectors` заллє колекцію Qdrant (кілька хвилин).

## Установка venv

```
cd instances/express
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df express sources --why   # перелік джерел і білий список
./df express refresh         # завантажити все задеклароване (~10 хвилин)
./df express manifest        # оновити паспорт
./df express setup           # Qdrant чи пошук лише по словах
./df express vectors         # залити корпус у docs-express (кілька хвилин)
./df express smoke           # перевірки
```

Найдовша частина `refresh` — README: реєстр npm віддає текст лише найновішої версії, тож кожна з ~1 150 стабільних
версій двадцяти пакетів читається окремо (06.10.2026 нові дев'ятнадцять пакетів — 50 хвилин). Без `GITHUB_TOKEN` у
`.env` анонімного ліміту GitHub API (60 звернень на годину) не вистачить на релізи. Обірваний `refresh` продовжується
з `--missing`.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd /mnt/c/Projects/fwdays/docfactory
./df express serve           # порт 8791
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8791/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user express-docs http://127.0.0.1:8791/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `express-docs` і два інструменти `search_docs`, `read_section`. Якщо сесію Claude
Code відкрито раніше, ніж піднято сервер, вона покаже його як недоступний: у `/mcp` виберіть сервер і «Reconnect».

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
