# openapi-typescript — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про openapi-typescript і його родину — openapi-fetch,
openapi-react-query, swr-openapi, openapi-typescript-helpers, openapi-metadata (репозиторій openapi-ts/openapi-typescript,
сайт openapi-ts.dev) — за документацією всіх їхніх стабільних версій: сайт з тегу кожної мінорної версії, README кожної
версії шести пакетів, журнали змін, релізи, приклади та історія версій у реєстрі npm. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

openapi-typescript читає схему OpenAPI 3.0 чи 3.1 (YAML або JSON, файл чи адреса) і пише лише типи TypeScript — `paths`,
`components`, `operations` — без жодного коду під час виконання. На цих типах стоїть openapi-fetch: клієнт fetch на
кілька кілобайтів, де шлях, параметри, тіло й відповідь перевіряє компілятор (`createClient`, `GET`, `POST`, middleware
`onRequest`/`onResponse`). Поверх нього — хуки TanStack Query (openapi-react-query) і SWR (swr-openapi); openapi-metadata
робить зворотне — документ OpenAPI з декораторів контролерів. У плані NestJS (фулстек-родина) це другий шлях до
типізованого клієнта поруч з orval: лише типи й тонкий fetch замість згенерованого коду.

Версії розходяться: openapi-typescript — 7.x (7.0 у червні 2024 перейшов на Redocly, `defaultNonNullable` став
увімкненим, глоби замінив `redocly.yaml`), а openapi-fetch досі 0.x: 18 мінорних ліній з березня 2023. Сайт кожної
мінорної версії, кожен запис журналу змін і дата кожного випуску зібрані в одному місці, з номером версії біля кожного
уривка.

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Сайт, кожна сторінка один раз з усіма версіями | 105 | 19 тегів 6.2.9–7.13.0 | `docs/src/content/docs` (6.x), `docs/` (7.x) |
| README шести пакетів, кожен неповторний текст один раз | 86 | 307 версій | tarball кожної версії npm |
| Журнали змін (changesets) | 270 | openapi-typescript 0.1.0–7.13.0, openapi-fetch 0.0.1–0.17.0, react-query, helpers | `packages/*/CHANGELOG.md` |
| Старий сайт swr-openapi | 6 | 5.5.2, 5.6.0 | `htunnicliff/swr-openapi`, `docs/` |
| Релізи swr-openapi і openapi-metadata | 44 | swr 0.4–5.6, metadata 0.0–0.2 | обидва репозиторії |
| Приклади openapi-fetch | 3 | 0.17.0 | тег `openapi-fetch@0.17.0` |
| Реєстр npm — огляд і лінії шести пакетів | 24 | усі | registry.npmjs.org |

Разом 538 документів; фрагментів в індексі — 1260 (`expected_passages` у `checks.json`). Замір `quality`: по словах 5
із 10, за змістом 8, разом 8, «як модель» 10 із 10.

Чому сайт береться з репозиторію, а не з openapi-ts.dev. Сайт показує лише поточну версію, а зміст кожної лежить у
репозиторії на її тезі: у 6.2–6.7 — сайт Astro (`docs/src/content/docs`), з 7.0 — VitePress (`docs/`). Береться
остання латка кожної мінорної версії openapi-typescript від 6.2 (раніше сайту не було) до 7.13. Сторінка, що переїхала
між теками, лишається тією самою сторінкою: поле `slug_rewrite` у `config.json` зводить обидва шляхи до одного ключа
(`openapi-typescript-cli`). Переклади `ja/`, `zh/` і копія старого сайту `6.x/` у теці 7.x не беруться. Сторінки
openapi-fetch, openapi-react-query, swr-openapi й openapi-metadata лежать на тому ж сайті й мають версію тегу
openapi-typescript, з якого взяті.

Чому README кожної версії. До 6.2.4 README openapi-typescript і був документацією (18–49 КБ: CLI, Node API, опції);
README openapi-fetch 0.x — 4–12 КБ з налаштуванням і прикладами. README helpers і metadata короткі, але взяті для
повноти, як і реєстр усіх шести пакетів. swr-openapi до 5.x жив в окремому репозиторії htunnicliff/swr-openapi: його
README є в tarball, а сайт і релізи взято звідти ж.

Чого немає. Документації OpenAPI, TypeScript, TanStack Query, SWR і Redocly: сторінки пакетів лише показують, як ними
користуватися. Згенерованих типів з `packages/openapi-typescript/examples` (github-api.ts, stripe-api.ts — мегабайти
виводу) і коду самих пакетів.

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа. Самих
  текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`, розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями, `slug_rewrite` і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.mcp.json` — запис HTTP-сервера для Claude Code. `ANTHROPIC_API_KEY` (лише для кроку `ask`) і `GITHUB_TOKEN` (лише
  для завантаження корпусу) беруться з кореневого `.env`.

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df openapi-typescript <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт | дерева 19 тегів `openapi-typescript@X.Y.Z` репозиторію openapi-ts/openapi-typescript | `ghdocs-history` |
| README | tarball `registry.npmjs.org/<пакет>/-/<пакет>-X.tgz` кожної стабільної версії шести пакетів | `npm-tarball-files` |
| журнали змін | `packages/<пакет>/CHANGELOG.md` на `main` | `changelog-regex` |
| старий сайт swr-openapi | дерева тегів v5.5.2 і v5.6.0 репозиторію htunnicliff/swr-openapi | `ghdocs-history` |
| релізи | API GitHub: htunnicliff/swr-openapi (теги `v…`) і монорепо (теги `swr-openapi@…`, `openapi-metadata@…`), лише сталі | `ghreleases-stable` |
| приклади | дерево тегу `openapi-fetch@0.17.0`, тека `packages/openapi-fetch/examples` | `ghexamples` |
| реєстр npm | registry.npmjs.org, по зверненню на пакет | `npm-versions` |

Нових читачів не додавалося. Читач VitePress (`_vitepress`) тепер підставляє в текст і поля шапки сторінки:
заголовок `# {{ $frontmatter.title }}` сторінок openapi-react-query і swr-openapi інакше лишався назвою розділу
буквально. Перелік версій README й реєстру береться з опису пакета в реєстрі; теги сайту записано в `sources.json`
(ключ — коміт тегу).

## Версії

Версія — номер випуску. openapi-typescript — без префікса (`"7"`, `"6.7"`, `"7.13.0"`), решта пакетів — з префіксом:
`fetch-` (openapi-fetch), `react-query-`, `swr-`, `helpers-`, `metadata-` (`"fetch-0.17"`, `"swr-5"`). Сторінки сайту
мають версію тегу openapi-typescript, з якого взято (остання латка мінорної). Без названої версії промпт велить шукати
для лінії 7 openapi-typescript — на неї за тиждень до 24.10.2026 припадало близько 94 % завантажень (7.13.0 від
11.02.2026), на 6 — близько 4 %; для openapi-fetch — 0.17 (46 %), далі 0.14 (23 %) і 0.13 (16 %). Сторінка, що не
змінилася між версіями, — один документ з усіма ними, тож перелік версій уривка сам показує, відколи й доки
документація казала саме це.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/openapi-typescript-corpus-2026-10-24.tar.gz` (556 текстів, паспорт і
сховище сирого `raw/`; перед видаленням текстів розпакований окремо й звірений із диском) і в копії на Windows-диску
`C:\Distr\openapi-typescript-corpus-2026-10-24.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/openapi-typescript/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/openapi-typescript-corpus-РРРР-ММ-ДД.tar.gz -C instances/openapi-typescript corpus raw
find instances/openapi-typescript/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/openapi-typescript/raw
gzip -9 -c instances/openapi-typescript/index/passages.json > instances/openapi-typescript/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти й сховище — лише після того, як
архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із ними повертається й сховище `raw/`:

```
tar -xzf ~/archives/docfactory/openapi-typescript-corpus-2026-10-24.tar.gz -C instances/openapi-typescript
./df openapi-typescript smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати:
`gunzip -k instances/openapi-typescript/index/passages.json.gz`, далі `./df openapi-typescript vectors` заллє колекцію
Qdrant (секунди на відеокарті, менше хвилини на процесорі).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df openapi-typescript …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md, розділ
«Спільне середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df openapi-typescript sources --why   # перелік джерел і білий список
./df openapi-typescript refresh         # завантажити все задеклароване (близько 15 хвилин)
./df openapi-typescript manifest        # оновити паспорт
./df openapi-typescript setup           # Qdrant чи пошук лише по словах
./df openapi-typescript vectors         # залити корпус у docs-openapi-typescript
./df openapi-typescript smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df openapi-typescript serve          # порт 8884
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8884/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user openapi-typescript-docs http://127.0.0.1:8884/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `openapi-typescript-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
