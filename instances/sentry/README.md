# sentry — примірник фабрики docfactory

Сорок другий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Sentry у проєктах на JavaScript і
TypeScript — підключення SDK до фреймворку, опції `Sentry.init`, помилки, трасування й вибірка, Session Replay,
профілювання, логи, cron-моніторинг, карти коду та їх завантаження, релізи, продукт sentry.io, токени, інтеграції й
REST API. Поруч — журнали змін і посібники міграції SDK, плагінів збирачів і sentry-cli та версії пакетів `@sentry/*`
з реєстру npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо

Збір помилок із картами коду стоїть у планах React (точка підключення — фаза 2, день 8) і Next.js (фаза 7, день 9).
Sentry міняє SDK швидко: мажор щороку (поточна лінія 11 вийшла 23.09.2026), `withSentryConfig` переїжджає між точками
входу, режим потокових span-ів замінює транзакції, а сторінки сайту для старших ліній лежать окремо. Відповідь з
пам'яті тут застаріває найшвидше — сам сайт просить асистентів не покладатися на вивчене.

У яких фазах і днях планів навчання він потрібен — див. [../../docs/learning-map.md](../../docs/learning-map.md).

## Скільки цього

| Шар | Документів | Звідки |
|-----|-----------:|--------|
| docs.sentry.io, розділ JavaScript: браузерний SDK | 134 | `/platforms/javascript/` |
| те саме, посібники 39 фреймворків і середовищ | 5 833 | `/platforms/javascript/guides/…/` |
| загальні розділи: продукт, поняття, sentry-cli, організація, акаунт, безпека й PII | 286 | `/product/`, `/concepts/` … |
| інтеграції (GitHub, GitLab, Slack, Jira, Vercel, Netlify …) | 108 | `/integrations/` |
| REST API, сторінка на ендпойнт | 279 | `/api/` |
| README, MIGRATION.md і 8 посібників міграції SDK (4 → 10, Replay, Feedback, профілювання) | 10 | getsentry/sentry-javascript |
| журнал змін SDK, лінії 4–11, запис на версію | 597 | `CHANGELOG.md`, `docs/changelog/v4…v8.md` |
| плагіни збирачів: README репозиторію, міграція, журнал змін | 103 | getsentry/sentry-javascript-bundler-plugins |
| README плагінів Vite, webpack, Rollup, esbuild з усіма опціями | 4 | реєстр npm |
| sentry-cli: README і журнал змін | 365 | getsentry/sentry-cli |
| реєстр npm: огляд і мажорні лінії 41 пакета | 239 | registry.npmjs.org |

Серед сторінок сайту 229 — сторінки старших ліній SDK (суфікс `__v10.x`, `__v8.x`, `__v7.x` … в адресі): сайт тримає
окремо лише ті, що для старшої лінії відрізняються.

Фреймворки: Angular, Astro, AWS Lambda, Azure Functions, Bun, Capacitor, Cloudflare, Cordova, Deno, Effect, Electron,
Elysia, Ember, Eve, Express, Fastify, Firebase, Flue, Gatsby, Google Cloud Functions, Hapi, Hono, Koa, Mastra, NestJS,
Next.js, Nitro, Node.js, Nuxt, React, React Router, Remix, Solid, SolidStart, Svelte, SvelteKit, TanStack Start, Vue,
Wasm.

Пакети npm: `@sentry/` + `angular`, `astro`, `aws-serverless`, `browser`, `bun`, `cloudflare`, `core`, `deno`, `effect`,
`elysia`, `ember`, `feedback`, `gatsby`, `google-cloud-serverless`, `hono`, `nestjs`, `nextjs`, `nitro`, `node`,
`node-native`, `nuxt`, `opentelemetry`, `profiling-node`, `react`, `react-router`, `remix`, `replay`, `replay-canvas`,
`solid`, `solidstart`, `svelte`, `sveltekit`, `tanstackstart-react`, `vercel-edge`, `vue`, `wasm`, `vite-plugin`,
`webpack-plugin`, `rollup-plugin`, `esbuild-plugin`, `cli`.

Разом 7 958 документів; фрагментів в індексі — 67 112 (`expected_passages` у `checks.json`). Фрагменти — це шматки
документів між заголовками, по яких іде пошук; однаковий текст різних версій зливається в один з усіма версіями.

Замір `quality` на першому корпусі: перша десятка (питання своїми словами, з названим фреймворком) — по словах 5 із 10,
за змістом 7, разом 6; друга, «як модель» (назви опцій і сторінок), — 10 із 10. `fusion_depth` заміряно з 0, 60, 120,
240 і 400: разом 7, 6, 4, 5 і 6 із 10, але з 0 видача неповна (три-чотири уривки з п'яти); стоїть 60.

**Версія у відповіді.** Сторінки розділу JavaScript несуть лінію SDK: «11» — поточна, сторінка старшої лінії — її номер
(«10», «8», «7»). Загальні розділи, інтеграції й REST API версій не мають: вони описують sentry.io як він є зараз.
Записи журналів змін несуть точну версію SDK («10.75.2»), плагінів («5.4.1») чи sentry-cli («3.8.0»), документи npm —
усі версії пакета, які описують. Номери різних продуктів перетинаються, тож із фільтром версії продукт треба називати й
у запиті. Без названої версії відповідь — для лінії 11, із тим, з якої версії щось змінилося.

**Фреймворк у запиті.** Більшість сторінок є в кожному з 39 посібників з тією самою назвою й майже тим самим текстом
(«Source Maps for Next.js», «Source Maps for React»). У видачі копії однієї сторінки займають одне місце (поле
`variant_pattern` у `config.json`), а якщо запит називає фреймворк, місце дістається його копії. Сторінки браузерного
SDK («… for Browser JavaScript») фреймворку не мають і лишаються окремими.

## Що в цій теці

- `corpus/` — завантажені документи і паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа.
- `index/passages.json` — кеш фрагментів, з якого підіймається сервер.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — ключ Anthropic (лише для кроку `ask`) і токен GitHub (тут не обов'язковий); `.mcp.json` — запис
  HTTP-сервера для Claude Code.
- `.venv/` — власний venv примірника; `requirements.txt` — його склад.

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df sentry <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сторінки docs.sentry.io | `sitemap.xml` сайту, текст — markdown-двійник сторінки з «.md» | `sentry-md` |
| README і MIGRATION.md SDK, README і міграція плагінів, README sentry-cli | raw.githubusercontent.com | `mdfile` |
| посібники міграції SDK | тека `docs/migration/` sentry-javascript | `ghdocs-heading` |
| журнал змін SDK | `CHANGELOG.md` і `docs/changelog/v4…v8.md` | `changelog` |
| журнали змін плагінів і sentry-cli | `CHANGELOG.md` | `sentry-changelog` |
| README плагінів Vite, webpack, Rollup, esbuild | реєстр npm, поле `readme` | `npm-readme-latest` |
| версії пакетів `@sentry/*` | реєстр npm | `npm-versions` |

Білий список — чотири хости: `docs.sentry.io`, `raw.githubusercontent.com`, `api.github.com` (одне звернення — перелік
файлів sentry-javascript) і `registry.npmjs.org`. Репозиторії беруться з основних гілок: `develop` у sentry-javascript,
`main` у плагінів, `master` у sentry-cli.

Особливості, які варто знати:

- **Новий модуль читачів `engine/readers/sentry.py`.** `sentry-md` — те саме, що `sitemap-md`, але версію сторінки
  старшої лінії бере із суфікса адреси (`…/streamed-spans__v10.x` → «10»), а не з джерела. Поле `slug_rewrite` у
  `config.json` дає такій сторінці той самий ключ, що й поточній, тож вони — редакції однієї сторінки: однаковий текст
  зливається, і пошук показує найновішу редакцію, а з фільтром версії — названу. `sentry-changelog` ділить журнал, де
  заголовок версії несе назву продукту («## sentry-cli 1.68.0» у записах до 1.69.0), і ставить перед іменем документа
  `name_prefix`: номери плагінів, CLI і SDK перетинаються, і однаковий запис двох журналів інакше злився б в один.
  `npm-readme-latest` бере README найновішої версії з реєстру npm: README плагінів з усіма опціями збирається з шаблону
  під час публікації, у репозиторії лежить лише шаблон.
- **Дві сторінки, що різняться лише регістром.** В Electron `…/integrations/childprocess` (ChildProcess) і
  `…/integrations/childProcess` (Child Process Integration) — різні тексти; друга лежить під іменем
  `…-child-process`, щоб не затерти першу.
- **Порожня сторінка сайту.** `concepts/key-terms/tracing/event-detail` на самому сайті порожня (заголовок «undefined
  | Sentry Docs»), читач її не пише, і кожен `refresh` повідомляє про один збій. Це не поломка примірника.
- **Глибина пошуку.** Кожна сторінка посібника має до 39 копій, і запасу, з яким пошук бере кандидатів (k × 6), не
  вистачало: на `tracePropagationTargets` п'ять місць займали копії однієї сторінки, і після згортання лишався один
  уривок. `fusion_depth: 60` у `config.json` дає повну видачу; 0 і 30 лишали три-чотири уривки з п'яти, а 120 і 240
  гірше зливали два способи пошуку (див. замір вище).
- **Довгі фрагменти.** Спільний поділ ріже розділ лише за порожніми рядками, а довгий список без них (журнал змін
  11.0.0, таблиці scopes у REST API) лишається одним фрагментом — 558 фрагментів довші за 3 000 символів. Пошук по
  словах бачить їх цілком, вектори — лише початок.

## Межі, про які треба пам'ятати

Тут немає SDK інших платформ (Python, Go, Java, .NET, PHP, Ruby, Rust, Android, Apple, Flutter, React Native, Unity),
самохостингу сервера Sentry, внутрішніх пакетів (`browser-utils`, `server-utils`, `server-runtime-injection`,
`bundler-plugins`) і конфігів розробки (`eslint-config-sdk`, `eslint-plugin-sdk`, `typescript`), а також розділів сайту
про ціни, внесок у документацію й Sentry для AI-асистентів. README окремих пакетів монорепозиторію не взято: це
однакові заглушки на кілька рядків із посиланням на сайт. Нотаток релізів GitHub теж немає — вони повторюють
`CHANGELOG.md`. Самі React, Next.js, NestJS, Node.js, Vite й Express — окремі примірники.

## Установка venv

```
cd instances/sentry
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # якщо потрібен крок ask, впишіть ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df sentry sources --why   # перелік джерел і білий список
./df sentry refresh         # завантажити все задеклароване (~2,5 години)
./df sentry manifest        # оновити паспорт
./df sentry setup           # Qdrant чи пошук лише по словах
./df sentry vectors         # залити корпус у docs-sentry (~2,5 години)
./df sentry smoke           # перевірки
```

Найдовша частина `refresh` — 6 640 сторінок сайту з паузою в секунду між зверненнями, ≈ 45 сторінок на хвилину.
Журнали змін діляться з одного завантаженого файла, реєстр npm — одне звернення на пакет. Токен GitHub не потрібен:
до api.github.com іде одне звернення. Обірваний `refresh` продовжується з `--missing`; `--missing site-js` докачує
лише сторінки розділу JavaScript.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df sentry serve           # порт 8802
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8802/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user sentry-docs http://127.0.0.1:8802/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `sentry-docs` і два інструменти `search_docs`, `read_section`. Якщо сесію Claude
Code відкрито раніше, ніж піднято сервер, вона покаже його як недоступний: у `/mcp` виберіть сервер і «Reconnect».

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
