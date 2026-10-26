# contentful — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Contentful — headless-платформу вмісту з API (документація для
розробників contentful.com/developers/docs, репозиторії офіційних SDK та інструментів на GitHub, реєстр npm). Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Contentful зберігає вміст сайту окремо від коду: редактори наповнюють простір (space) записами (entries) і ресурсами
(assets) за типами вмісту (content types), а застосунок бере їх через API — Content Delivery API для опублікованого,
Content Preview API для чернеток, GraphQL Content API, — і пише через Content Management API. Середовища (environments)
і їхні псевдоніми (environment aliases) дають змінювати модель вмісту на копії даних, а міграції (contentful-migration)
— тримати ці зміни скриптами в git. У плані Next.js (фулстек-родина) Contentful — один із CMS у розділі «знати, що
існує», поряд із Sanity й Payload.

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Сайт developers/docs | 472 | — | markdown-двійники сторінок, перелік — обходом посилань |
| README й файли документації | 609 | 761 | 12 репозиторіїв contentful/*, останній тег кожної мінорної (901 тег) |
| Релізи GitHub | 3934 | 3251 | стабільні релізи тих самих репозиторіїв |
| Реєстр npm | 155 | — | двадцять пакетів |

Разом 5170 записів паспорта; в індексі 5088 документів і 15 194 фрагменти (`expected_passages` у `checks.json`):
однаковий текст різних версій — один уривок із переліком версій. Замір `quality`: по словах 6 із 10, за змістом 3,
разом 5, «як модель» 10 із 10. Своїми словами нижче, бо перша десятка питає побутовими словами («показати редакторам
чернетку на сайті, поки вони пишуть»), а сторінки говорять назвами API й функцій.

Репозиторії й теги:

| Репозиторій | Префікс | Теги | Мінорних | Що береться |
|-------------|---------|------|---------:|-------------|
| contentful.js | `contentful-js` | `vX.Y.Z` | 82 | README, ADVANCED, MIGRATION, TYPESCRIPT, DOCS |
| contentful-management.js | `cma-js` | `vX.Y.Z` | 272 | README, MIGRATION |
| contentful-cli | `cli` | `vX.Y.Z` | 76 | README і довідка команд `docs/` |
| contentful-migration | `migration` | `vX.Y.Z` | 64 | README, `docs/validation.md` |
| contentful-import | `import` | `vX.Y.Z` | 46 | README, `docs/exo-import.md` |
| contentful-export | `export` | `vX.Y.Z` | 48 | README, `docs/exo-export.md` |
| rich-text | `rich-text` | `@contentful/rich-text-types@…`, раніше `vX.Y.Z` | 48 | README кореня й шести пакетів |
| ui-extensions-sdk (App SDK) | `app-sdk` | `vX.Y.Z` | 117 | README, MIGRATION, `docs/` |
| live-preview | `live-preview` | `@contentful/live-preview@…`, раніше `vX.Y.Z` | 51 | README, content-source-maps |
| experience-builder | `experiences` | `vX.Y.Z` | 55 | README кореня й пакетів, `docs/guides` |
| create-contentful-app | `cca` | `@contentful/create-contentful-app@…` | 25 | README кореня й пакетів |
| contentful-mcp-server | `mcp` | `mcp-server@…` | 17 | README кореня й двох пакетів |

Чому сайт обходом. contentful.com стоїть за перевіркою Vercel: llms.txt, sitemap.xml, HTML-сторінки й сервер MCP сайту
відповідають 429 «This request requires a challenge». Пропускаються лише markdown-двійники сторінок документації
(адреса з «.md»), тож переліку сторінок немає ніде, крім посилань у самих двійниках. Читач `mdcrawl` обходить їх у межах
`/developers/docs/`, починаючи з адрес поля `pages` (знайдених попереднім обходом і в архіві Wayback); заглушки «Page
Not Found» документами не стають, а текст, який сайт віддає за кількома адресами (адреса підрозділу дає сторінку-батька),
лягає один раз під адресою, що збігається з назвою сторінки.

Чого немає. Help Center (contentful.com/help, вебзастосунок для редакторів) закритий перевіркою повністю, разом із
двійниками. Сторінки developers/docs, на які не посилається жодна інша й яких не було в стартовому переліку, обхід не
знайде, а звірити повноту нема з чим: сайт переліку не віддає (довідник Content Management API дав 177 сторінок,
Content Delivery API — 27). Forma 36 і field-editors, код і тести пакетів, пререлізи (`-beta`, `-alpha`,
`-experimental`), Next.js, React, Gatsby і GraphQL як окремі проєкти.

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

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df contentful <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт | www.contentful.com/developers/docs, двійники «.md» | `mdcrawl` (новий) |
| README й документація | дерева тегів 12 репозиторіїв contentful/* | `ghdocs-history` |
| релізи | api.github.com, `/repos/contentful/<репозиторій>/releases`, без передрелізів | `ghreleases` |
| реєстр npm | `contentful`, `contentful-management`, `contentful-cli`, `contentful-migration`, `contentful-import`, `contentful-export`, `@contentful/rich-text-*` (5), `app-sdk`, `live-preview`, `content-source-maps`, `experiences-sdk-react`, `create-contentful-app`, `app-scripts`, `react-apps-toolkit`, `node-apps-toolkit`, `mcp-server` | `npm-versions` |

Новий читач `mdcrawl` (`engine/readers/mdcrawl.py`) — обхід markdown-двійників сайту, що не віддає переліку сторінок;
поля описані в докстрінгу модуля. Релізам задано `skip: "-"`: передрелізи без позначки на GitHub `stable: true` не
відсіює.

## Версії

README й файли документації несуть версію тегу, з якого взяті (`11.12.10`), релізи — версію релізу, реєстр — версію
пакета; фільтр `version` бере мажор (`"11"`), мінор (`"10.6"`) або точну версію (`"11.5.25"`). Нумерація в кожного пакета
своя, тож разом із версією запит називає пакет. Сторінки сайту версії не мають — вони про платформу в день
завантаження.

За завантаженнями npm за тиждень до 26.10.2026: `contentful` — лінія 11 тримає 63 %, 10 — 19 %, 9 — 13 %;
`contentful-management` — 12 тримає 44 %, 11 — 39 %; `@contentful/rich-text-react-renderer` — 16 тримає 59 %, 15 — 37 %;
`@contentful/app-sdk` — уся лінія 4; `contentful-migration` — 4 тримає 71 %, 5 — 29 %. Промпт відповідає для
найновішої лінії пакета, а для коду на старшій мажорній каже, що змінилося.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/contentful-corpus-2026-10-26.tar.gz` (5170 текстів, паспорт і сховище
сирого `raw/`; перед видаленням текстів розпакований окремо й звірений із диском) і в копії на Windows-диску
`C:\Distr\contentful-corpus-2026-10-26.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/contentful/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/contentful-corpus-РРРР-ММ-ДД.tar.gz -C instances/contentful corpus raw
find instances/contentful/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/contentful/raw
gzip -9 -c instances/contentful/index/passages.json > instances/contentful/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти й сховище — лише після того, як
архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із ними повертається й сховище `raw/`:

```
tar -xzf ~/archives/docfactory/contentful-corpus-2026-10-26.tar.gz -C instances/contentful
./df contentful smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/contentful/index/passages.json.gz`,
далі `./df contentful vectors` заллє колекцію Qdrant (секунди на відеокарті, кілька хвилин на процесорі).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df contentful …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md, розділ
«Спільне середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df contentful sources --why   # перелік джерел і білий список
./df contentful refresh         # завантажити все задеклароване (близько 30 хвилин)
./df contentful manifest        # оновити паспорт
./df contentful setup           # Qdrant чи пошук лише по словах
./df contentful vectors         # залити корпус у docs-contentful
./df contentful smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df contentful serve          # порт 8904
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8904/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user contentful-docs http://127.0.0.1:8904/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `contentful-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
