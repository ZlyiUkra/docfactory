# cloudflare — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Cloudflare за його документацією: увесь сайт
developers.cloudflare.com — платформа розробника (Workers і їхні API, прив'язки, Wrangler, Pages, R2, D1, KV, Durable
Objects, Queues, Workflows, Workers AI, Vectorize, Hyperdrive, AI Gateway, Agents, Containers), DNS, кеш і CDN, правила,
SSL/TLS, WAF, захист від DDoS, боти, Zero Trust і Cloudflare One, Tunnel, мережеві сервіси, аналітика, дописи журналу
змін; README кожної стабільної версії шести пакетів і журнали змін workers-sdk. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

Cloudflare — платформа розгортання з безкоштовним планом, яку плани навчання називають поряд із Vercel і Netlify
([../react/LEARNING.md](../react/LEARNING.md) — перший викот статичної збірки, [../astro/LEARNING.md](../astro/LEARNING.md)
— адаптер платформи). Документація Astro і Vite описує лише шар підключення, а не сам Cloudflare: прив'язки, ліміти,
`wrangler.jsonc`, DNS, кеш. Тут — сам Cloudflare, увесь сайт, а не лише платформа розробника.

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Сайт | 8 706 | — | developers.cloudflare.com, кожна сторінка `sitemap-0.xml`, поточний знімок |
| README `wrangler` | 22 | 537 | npm, стабільні 0.0.x–4.156; текст — з тегу `wrangler@версія` workers-sdk |
| README `@cloudflare/workers-types` | 16 | 569 | npm 1.0–5.2026…; з 4.x — workerd, раніше — архівний cloudflare/workers-types |
| README `miniflare` | 45 | 299 | npm 0.1–4.2026…; 1.x–2.x — cloudflare/miniflare, з 3.x — workers-sdk |
| README `create-cloudflare` | 7 | 280 | npm 0.0–2.74; 0.x–1.x — lukeed/create-cloudflare, з 2.x — C3 у workers-sdk |
| README `@cloudflare/vitest-pool-workers` | 1 | 315 | npm 0.1–0.23, workers-sdk |
| README `@cloudflare/vitest-plugin` | 1 | 43 | npm 1.0–1.4, workers-sdk; наступник `vitest-pool-workers` під новим ім'ям |
| Журнали змін | 1 400 | 1 400 | workers-sdk: `wrangler` 525, `miniflare` 230, `create-cloudflare` 279, `vitest-pool-workers` 366 записів |

Разом 10 198 записів паспорта. В індексі 65 309 фрагментів (`expected_passages` у `checks.json`). Замір `quality`:
по словах 5 із 10, за змістом 3, разом 5, «як модель» 10 із 10. Перша десятка своїми словами низька: сайт тримає
кожну тему в кількох місцях (продукт, розв'язки `use-cases`, навчальні шляхи, Cloudflare One і окремий розділ
Tunnel), і видача своїми словами приносить сусідні сторінки. Запити назвами документації знаходять ціль усі.

У частини версій README немає ні на тезі, ні на коміті публікації (вони названі в журналі `refresh`): wrangler 0.0.1–0.0.5,
3.63.2, 3.78.3, 4.45.2, 4.152.0; workers-types 2.2.1–2.2.2; miniflare 3.20240909.2; create-cloudflare 0.0.0–0.0.3,
2.0.0, 2.0.1, 2.20.0, 2.74.3; vitest-pool-workers 0.1.0, 0.2.1, 0.4.10, 0.4.15, 0.5.3, 0.10.2, 0.23.0; vitest-plugin
0.0.0 (заглушка імені) і 1.4.7. Разом 29 версій.

Чого немає:

- Довідника REST API (`developers.cloudflare.com/api/`): його немає в sitemap сайту.
- Сторінок-переліків журналу змін (`/changelog/product/…`, `/changelog/2/` тощо): вони повторюють дописи, і
  `exclude` їх відкидає.
- Передрелізів пакетів і сторінок інших сайтів Cloudflare (блог, cloudflare.com).

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа. Самих
  текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого підіймається сервер. У git лежить стиснений `passages.json.gz`; розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки будується корпус. Він же білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.mcp.json` — запис HTTP-сервера для Claude Code. `ANTHROPIC_API_KEY` (лише для кроку `ask`) і `GITHUB_TOKEN` (лише
  для завантаження корпусу) беруться з кореневого `.env`.

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df cloudflare <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт | `developers.cloudflare.com/sitemap-0.xml`; кожна сторінка — markdown, який сайт віддає на `Accept: text/markdown` | `sitemap-accept` |
| README | реєстр npm шести пакетів; текст — raw.githubusercontent.com з тегу версії або коміту публікації | `npm-readme` |
| журнали змін | `packages/<пакет>/CHANGELOG.md` гілки main workers-sdk (changesets, запис на версію) | `changelog-regex` |

Поле `drop` джерела `site` вирізає навігацію, однакову на кожній сторінці: посилання «Skip to content», примітку про
llms.txt, рядок «Last updated | Copy as Markdown», усе від «Was this helpful?» до кінця («On this page», JSON-LD), у
дописах журналу змін — «View RSS feeds / Back to all posts» і блок JSON-LD, а ще позначку зовнішнього посилання «↗︎».

## Версії

Сайт версії не несе: його сторінки описують Cloudflare на день завантаження. Версію несуть README і журнали змін
пакетів: `wrangler` — без префікса (`version: "4"`, `"4.156"`), решта — з префіксом пакета (`"miniflare-4"`,
`"create-cloudflare-2"`, `"vitest-pool-workers-0"`, `"vitest-plugin-1"`, `"workers-types-4"`), щоб нумерації не
змішувалися. Журнал змін інтеграції з Vitest — один на обидва імені (тека `packages/vitest-plugin/`), і всі його
записи, 1.x теж, несуть префікс `vitest-pool-workers-`. Промпт
шукає «як зробити» без версії, а версію передає лише для питань про історію пакета.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку. У `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant. Відповіді ті самі до символа, бо кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/cloudflare-corpus-2026-10-31-vitest-plugin.tar.gz` (10 198 текстів, паспорт і
сховище сирого `raw/`; перед видаленням текстів архів розпаковано окремо й звірено з диском) і в копії на Windows
`C:\Distr\cloudflare-corpus-2026-10-31-vitest-plugin.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/cloudflare/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/cloudflare-corpus-РРРР-ММ-ДД.tar.gz -C instances/cloudflare corpus raw
find instances/cloudflare/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/cloudflare/raw
gzip -9 -c instances/cloudflare/index/passages.json > instances/cloudflare/index/passages.json.gz
```

Після цього закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Тексти й сховище видаляють лише тоді,
коли архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із текстами повертається сховище сирого:

```
tar -xzf ~/archives/docfactory/cloudflare-corpus-2026-10-31-vitest-plugin.tar.gz -C instances/cloudflare
./df cloudflare smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Їхні
перевірки `smoke` чесно пропускає з позначкою «корпус в архіві».

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/cloudflare/index/passages.json.gz`.
Далі `./df cloudflare vectors` заллє колекцію Qdrant: півтори хвилини на відеокарті, довше на процесорі.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df cloudflare …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як збудувати його один раз і як `df` обирає між ними — у кореневому README, розділ
«Спільне середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df cloudflare sources --why   # перелік джерел і білий список
./df cloudflare refresh         # завантажити все задеклароване (близько півтори години: 8 706 сторінок сайту)
./df cloudflare manifest        # оновити паспорт
./df cloudflare setup           # Qdrant чи пошук лише по словах
./df cloudflare vectors         # залити корпус у docs-cloudflare
./df cloudflare smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити його працювати:

```
cd ~/Projects/docfactory
./df cloudflare serve          # порт 8937
```

Сервер готовий, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8937/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user cloudflare-docs http://127.0.0.1:8937/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування. Вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell або додати сервер кнопкою «Add server» у вікні
`/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` має показати `cloudflare-docs` і два інструменти: `search_docs` і `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта (scope запису, «address already in use») — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
