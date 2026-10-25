# sanity — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Sanity — платформу вмісту: Sanity Studio (редактор, пакет npm
`sanity`), Content Lake (сховище документів у хмарі Sanity), мову запитів GROQ і бібліотеки JavaScript навколо них
(сайти www.sanity.io/docs і reference.sanity.io, репозиторії sanity-io/* на GitHub, реєстр npm). Код спільний і лежить
у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

Sanity — безголова CMS (система керування вмістом без власного сайту): схему документів описують кодом
(`defineType`, `defineField`), редактори працюють у Studio, а сайт бере вміст запитами GROQ через `@sanity/client` чи
`next-sanity`. У плані Next.js (фулстек-родина) Sanity стоїть у «знати, що існує» разом із Payload і Contentful, у
рядку «вміст редагують не розробники».

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Сайт www.sanity.io/docs | 687 | — | карта сайту й markdown-двійники сторінок |
| Довідник API reference.sanity.io | 3612 | — | карта сайту й markdown-двійники сторінок (TypeDoc) |
| README `sanity`, `groq`, `@sanity/vision` | 25 | усі стабільні | GitHub на коміті публікації чи тезі; `groq` — тарболи npm |
| README `@sanity/cli` | 31 | усі стабільні, крім 70 (переважно 6.x) | GitHub (sanity-io/sanity, sanity-io/cli) |
| README `@sanity/client` | 77 | усі стабільні, крім 50 старих | GitHub (sanity-io/client, sanity-io/sanity) |
| README `next-sanity`, `@sanity/image-url`, `@portabletext/react` | 109 | усі стабільні | тарболи npm |
| README `@sanity/visual-editing` | 18 | усі стабільні | GitHub (sanity-io/visual-editing) |
| Реєстр npm дев'яти пакетів | 80 | — | registry.npmjs.org |
| Релізи семи репозиторіїв | 3249 | — | GitHub Releases, лише стабільні |

Разом 7888 документів, фрагментів в індексі 49 042 (`expected_passages` у `checks.json`). README лише 260: однаковий
текст сусідніх версій записується один раз. Замір `quality`: по словах 0 із 10, за змістом 1, разом 1, «як модель» 10
із 10. Перша десятка навмисно уникає слів Sanity («editing app» замість «Studio»), а в корпусі половина фрагментів —
дрібні сторінки довідника API, тож без назв документації пошук мимо. Модель же шукає назвами, як велить промпт.

Два налаштування, що дали 10 із 10:

- `fusion_depth: 20` у `config.json`. Сторінки сайту «Reference» і «Array» (типи схеми) тонули під десятками сторінок
  довідника з тими самими словами (`ReferenceRule`, `ArrayDefinition`). Злиття, що бачить по 20 місць кожного способу
  пошуку, підняло їх у п'ятірку: 7 із 10 → 10 із 10, разом із двома цілями, доповненими справжніми відповідями.
- `heading_floor: 3` у джерелі довідника. TypeDoc ділить кожну властивість ще на «Type Parameters», «Parameters»,
  «Returns»; без поля довідник давав 30 тисяч фрагментів по кілька рядків, з полем — фрагмент на цілу властивість, і
  весь корпус зменшився з 60 691 до 49 042 фрагментів.

Чого немає. Next.js, React, Astro, Nuxt, Vercel і редакторів Portable Text інших проєктів як окремих проєктів, коду й
тестів пакетів, сторінок курсів sanity.io/learn. Пререлізи (canary, beta, rc, next) не беруться. README 14 найстаріших
версій `sanity` (переважно 0.x 2015–2016 років), 70 версій `@sanity/cli` (переважно 6.x), 50 старих `@sanity/client` і 6
`@sanity/vision` недоступні: у реєстрі для них немає ні коміту публікації, ні тегу в репозиторії. Одна сторінка
довідника (`EmptyProps`) порожня і не береться.

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

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df sanity <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт | www.sanity.io/docs/sitemap.xml і `.md` кожної сторінки | `sitemap-md-suffix` (поле `drop`) |
| довідник API | reference.sanity.io/sitemap.xml і `…/index.html.md` кожної сторінки | `sitemap-md-suffix` (поля `md_suffix`, `drop`, `heading_floor`) |
| README `sanity`, `@sanity/vision`, `@sanity/cli`, `@sanity/client`, `@sanity/visual-editing` | raw.githubusercontent.com на `gitHead` версії, без нього — на тезі | `npm-readme` |
| README `groq`, `next-sanity`, `@sanity/image-url`, `@portabletext/react` | тарболи реєстру npm | `npm-tarball-files` |
| реєстр npm | дев'ять пакетів | `npm-versions` |
| релізи | GitHub Releases sanity, client, next-sanity, cli, image-url, visual-editing, react-portabletext | `ghreleases` |

Новий читач `sitemap-md-suffix` — те саме, що `sitemap-md`, але markdown-двійник сторінки береться за адресою з
довільним суфіксом (довідник віддає його за `…/index.html.md`, а «.md» до адреси дає 404), а збіги виразів `drop`
прибираються з тексту: кожна сторінка сайту починається однаковою цитатою «For AI agents: …llms.txt», а сторінки
довідника несуть рядок «Defined in: src/…» біля кожного члена класу. Поле `heading_floor` перетворює глибші
заголовки на рядки жирним.

Спільним читачам додано два необов'язкові поля, без яких вони працюють, як і раніше: `npm-readme` дістав
`version_prefix` (як у `npm-tarball-files`) і `gzip: true` (як у `npm-versions`). Опис пакета `sanity` в реєстрі з
тисячами збірок canary важить 50,5 МБ, понад стелю відповіді в 50 МБ, а стиснутим проходить.

Чому README частини пакетів береться з GitHub, а не з тарболів. Усі стабільні тарболи `sanity` разом важать 10 ГБ
розпакованими, `@sanity/cli` — 5 ГБ, `@sanity/visual-editing` — 0,8 ГБ, `@sanity/client` — 0,6 ГБ. README з репозиторію на
коміті публікації — той самий файл за кілька кілобайтів. Шаблонів адреси кілька, бо пакети переїжджали: `@sanity/cli`
жив у монорепозиторії sanity-io/sanity, потім у sanity-io/cli з тегами `@sanity/cli@8.23.0`; `@sanity/client` — навпаки,
з монорепозиторію в sanity-io/client.

## Версії

Сторінки сайту й довідника версії не мають: вони описують поточний випуск. Версію несуть README, реєстр і релізи:
`sanity`, `groq` і `@sanity/vision` випускаються разом і мають просту версію (`6.20.0`; фільтр `"6"` чи `"6.20"`),
решта пакетів — з іменем попереду, бо в кожного своя нумерація: `client-8`, `cli-`, `next-sanity-`, `image-url-`,
`visual-editing-`, `portabletext-react-`. За завантаженнями npm за тиждень до 25.10.2026 лінія 6 пакета `sanity`
тримає 52 %, лінія 5 — 24 %; `@sanity/client` 7 — 51 %, 8 — 35 %; `next-sanity` 13 — 53 %. Промпт відповідає для поточних
ліній, а для старшої каже, що змінилося.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/sanity-corpus-2026-10-25.tar.gz` (7888 текстів, паспорт і сховище
сирого `raw/`; перед видаленням текстів розпакований окремо й звірений із диском) і в копії на Windows-диску
`C:\Distr\sanity-corpus-2026-10-25.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/sanity/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/sanity-corpus-РРРР-ММ-ДД.tar.gz -C instances/sanity corpus raw
find instances/sanity/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/sanity/raw
gzip -9 -c instances/sanity/index/passages.json > instances/sanity/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти й сховище — лише після того, як
архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із ними повертається й сховище `raw/`:

```
tar -xzf ~/archives/docfactory/sanity-corpus-2026-10-25.tar.gz -C instances/sanity
./df sanity smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/sanity/index/passages.json.gz`, далі
`./df sanity vectors` заллє колекцію Qdrant (хвилина на відеокарті, кілька десятків хвилин на процесорі).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df sanity …` бере спільне середовище з кореня репозиторію (`.venvs/cpu`
або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md, розділ «Спільне
середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df sanity sources --why   # перелік джерел і білий список
./df sanity refresh         # завантажити все задеклароване (близько 80 хвилин)
./df sanity manifest        # оновити паспорт
./df sanity setup           # Qdrant чи пошук лише по словах
./df sanity vectors         # залити корпус у docs-sanity
./df sanity smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df sanity serve          # порт 8899
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8899/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user sanity-docs http://127.0.0.1:8899/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `sanity-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
