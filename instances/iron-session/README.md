# iron-session — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про iron-session — пакет npm, який тримає сесію в підписаній і
зашифрованій («запечатаній») куці, без сховища сесій на сервері: дані їдуть у самій куці. Працює з Next.js (App
Router, Pages Router, Route Handlers, Server Actions, middleware і proxy), Express, Koa, модулем `http` Node, Bun і
Deno. Документація — всіх стабільних версій iron-session, його попередника next-iron-session і бібліотеки шифрування
iron-webcrypto, на якій він стоїть. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Сайту документації в iron-session немає: усе, що є, — README, типи, нотатки релізів і приклади в репозиторії, і все це
змінювалося з кожною мажорною лінією. Тричі мінявся сам API: `withIronSession` у next-iron-session, обгортки
`withIronSessionApiRoute` і `withIronSessionSsr` у 6.x–7.x, одна функція `getIronSession` з 8.0; у 9.0 — лише ESM і
Node 22.13+. Документація Next.js (глава `How to implement authentication`) радить iron-session як бібліотеку сесій,
але власного опису не має. Тут — усі версії поруч, тож на питання «як це в моїй версії» є відповідь саме для неї.

## Історія пакета

Ця історія пояснює, чому в корпусі три пакети і чому їхні номери перетинаються.

| Коли | Пакет | Версії | Що важливо |
|------|-------|--------|------------|
| березень 2020 | iron-session | 1.0.1–1.0.4 | перша публікація під цим іменем |
| березень 2020 — червень 2021 | next-iron-session | 1.1.0–4.2.0 | лише Next.js і Express, `withIronSession`, `ironSession`, `applySession`; у npm позначений застарілим |
| 04.11.2021 | iron-session | 2.0.0, 6.0.0 | повернення до імені iron-session, переписано на TypeScript; 5-ї лінії немає |
| 2021–2022 | iron-session | 6.0–6.3 | входи `iron-session/next`, `/express`, `/koa`, `/edge`; `withIronSessionApiRoute`, `withIronSessionSsr` |
| 08.06.2022 | iron-session | 7.0.0–7.0.6 | усі сім за один день, тегів у git не мають; далі продовжилися 6.2–6.3 |
| листопад 2023 | iron-session | 8.0–8.0.4 | одна функція `getIronSession`, App Router |
| 30.08.2026 | iron-session | 9.0.0–9.0.1 | лише ESM, Node 22.13+, сесії в proxy, куки понад 4 КБ (`chunk`) |

iron-webcrypto (0.0.1–2.0.0) — реалізація формату «iron» (запечатані об'єкти hapi: шифрування й підпис) на Web Crypto.
На ньому iron-session стоїть із 7.0 і 6.2; до того брав `@hapi/iron`.

## Скільки цього

Стабільні версії: iron-session — 32, next-iron-session — 28, iron-webcrypto — 31. Передрелізи (`9.0.0-beta`,
`8.0.0-alpha/beta`, `5.0.0-alpha` next-iron-session) не беруться, крім як у переліку реєстру npm.

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| README iron-session: кожен неповторний текст один раз, з усіма версіями | 20 | 1.0.1–9.0.1 (32) | tarball кожної версії npm |
| `MIGRATION.md` (як перейти на 9 і з 6 на 8) | 2 | 9.0.0–9.0.1 | tarball |
| Типи iron-session: головний файл і входи `next`, `edge`, `express`, `koa` | 7 + 2 + 1 + 1 + 1 | 2.0.0–9.0.1 | tarball |
| `SECURITY.md`: що бібліотека захищає і чого ні, ротація паролів | 1 | 9.0.0–9.0.1 | теги репозиторію |
| Журнал змін iron-session, по документу на версію | 3 | 8.0.0-alpha.0, 9.0.0, 9.0.1 | `CHANGELOG.md` гілки main |
| Нотатки релізів GitHub, лише стабільні (v6.0.0 і v8.0.0 — інструкції переходу) | 36 | 1.0.1–9.0.1 | API релізів `vvo/iron-session` |
| Приклади з тегів: express, koa, next.js у 3.3–6.x; застосунок Next.js у 8.x–9.x | 187 | 3.3.0–9.0.1 | теги `vvo/iron-session` |
| README next-iron-session | 18 | 1.1.0–4.2.0 (28) | tarball |
| Типи next-iron-session | 8 | 4.1.0–4.2.0 | tarball |
| README iron-webcrypto | 21 | 0.0.1–2.0.0 (31) | tarball |
| Типи iron-webcrypto | 16 | 0.0.1–2.0.0 | tarball |
| Журнал змін iron-webcrypto | 18 | 0.0.1–2.0.0 | `CHANGELOG.md` гілки main |
| Реєстр npm трьох пакетів: огляд і лінії, з вимогами до Node (`engines`) | 7 + 6 + 4 | усі | registry.npmjs.org |

Разом 359 документів; фрагментів в індексі — 1053 (`expected_passages` у `checks.json`). Ще 12 записів журналу
iron-webcrypto в оригіналі порожні (лише заголовок версії) і не записуються.

Замір `quality` на першому корпусі: по словах 6 із 10, за змістом 5, разом 7; десятка «як модель» — 10 із 10. Дві цілі
«як модель» доповнено прикладами з репозиторію, бо в README 8.x відповіді немає, а приклад — це вона і є: Server Action
з `getIronSession` — файл `app-router-server-component-and-action/actions.ts`, вхід за посиланням через `sealData` —
`app-router-magic-links/session/route.ts` і `magic-login/route.ts`. Так само ціль про Node доповнено нотатками релізу
v9.0.0 («Needs Node 22.13+»), а ціль про `withIronSessionApiRoute` — нотатками v6.0.0, де ця обгортка показана в коді.
`max_per_doc` заміряно: 1 знижує «як модель» до 9, 2 і 3 нічого не змінюють — лишено 0.

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

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df iron-session <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| README, `MIGRATION.md`, типи трьох пакетів | tarball `registry.npmjs.org/<пакет>/-/<пакет>-X.tgz` | `npm-tarball-files` |
| `SECURITY.md` | теги v9.0.0 і v9.0.1 репозиторію `vvo/iron-session` | `ghdocs-history` |
| журнали змін | `CHANGELOG.md` гілки main `vvo/iron-session` і `brc-dd/iron-webcrypto` | `changelog-conventional` |
| нотатки релізів | API релізів `vvo/iron-session` | `ghreleases` |
| приклади | тека `examples/` на кожному стабільному тезі `vvo/iron-session` | `ghcode-history-ts` |
| реєстр npm | registry.npmjs.org, одне звернення на пакет | `npm-versions` |

Нових читачів примірник не потребував. Особливості корпусу:

- **Версії трьох пакетів перетинаються.** «2.0.0» є і в iron-session, і в next-iron-session, і в iron-webcrypto;
  фільтр `version: "2"` бере всі три. Назва кожного документа називає пакет, і промпт велить дивитися на неї, перш
  ніж називати версію.
- **Релізи — один потік.** Репозиторій той самий з 2020 року: v1.0.1–v4.2.0 у потоці релізів — це next-iron-session,
  v6.0.0 і новіші — iron-session. Тегів 7.x немає, тож прикладів 7.x у корпусі теж немає.
- **README — з tarball, а не з тегів**: так є й версії без тегів (7.x), і текст точно той, що отримує `npm install`.
- **Приклади — код, поділений на розділи** за оголошеннями (функція, компонент, константа); службові файли (конфіги
  Next.js, Tailwind, PostCSS, логотип, аналітика, стилі) відкинуто.
- **Вимога до Node (`engines`)** записана в документах реєстру npm: 2.0–7.x — Node 12+, 9.x — Node 22.13+; у 8.x
  поля немає.
- **Документ — неповторний текст.** Версії, де файл не змінився, ділять один документ; у рядку `# версія:` стоять усі.

## Межі, про які треба пам'ятати

Документації Next.js, бібліотек автентифікації (Auth.js, Better Auth, Clerk), JWT і бібліотеки jose, кук і HTTP
взагалі, Node.js тут немає. Код бібліотеки (`src/`), тести, `AGENTS.md` і `CONTRIBUTING.md` не входять — лише
документація й приклади. Попередній шар шифрування `@hapi/iron` (iron-session до 6.1) теж не входить.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/iron-session-corpus-2026-10-13.tar.gz` (359 текстів, паспорт і сховище
сирого `raw/`; перед видаленням текстів розпакований окремо й звірений із диском). В історії git текстів немає ніде.
Архів лежить лише на цій машині. Сховище `raw/` після звірки теж видалено з диска.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/iron-session/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/iron-session-corpus-РРРР-ММ-ДД.tar.gz -C instances/iron-session corpus raw
find instances/iron-session/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/iron-session/raw
gzip -9 -c instances/iron-session/index/passages.json > instances/iron-session/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти й сховище — лише після того, як
архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із ними повертається й сховище `raw/`:

```
tar -xzf ~/archives/docfactory/iron-session-corpus-2026-10-13.tar.gz -C instances/iron-session
./df iron-session smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/iron-session/index/passages.json.gz`,
далі `./df iron-session vectors` заллє колекцію Qdrant (кілька хвилин).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df iron-session …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md,
розділ «Спільне середовище». Свій `.env` примірник тримає в `instances/iron-session/.env` (`cp .env.example .env`;
для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`, береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df iron-session sources --why   # перелік джерел і білий список
./df iron-session refresh         # завантажити все задеклароване (близько 7 хвилин)
./df iron-session manifest        # оновити паспорт
./df iron-session setup           # Qdrant чи пошук лише по словах
./df iron-session vectors         # залити корпус у docs-iron-session
./df iron-session smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df iron-session serve          # порт 8833
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8833/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user iron-session-docs http://127.0.0.1:8833/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `iron-session-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
