# uploadthing — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про UploadThing — сервіс і бібліотеку завантаження файлів для
фулстек-застосунків на TypeScript (сайт docs.uploadthing.com, репозиторій pingdotgg/uploadthing, реєстр npm). Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

UploadThing бере на себе завантаження файлів: на сервері застосунку описують файлові маршрути (`createUploadthing`,
`f({ image: { maxFileSize: "4MB" } })`, `middleware` для авторизації, `onUploadComplete` після завантаження) і
підключають обробник `createRouteHandler`, а в браузері ставлять `UploadButton`, `UploadDropzone` чи хук
`useUploadThing`; файли лежать у сховищі UploadThing, і з сервера ними керує `UTApi`. У плані Next.js (фулстек-родина)
UploadThing — інструмент завантаження файлів.

## Скільки цього

| Шар | Документів | Неповторних | Версій | Звідки |
|-----|-----------:|------------:|-------:|--------|
| Сайт 7.0–7.7 | 276 | 101 | 8 | тека `docs/src/app` з тегів `uploadthing@7.*` |
| Сайт 6.0–6.13 | 279 | 79 | 13 | тека `docs/src/pages` (Nextra) з тегів `uploadthing@6.*` |
| Сайт 3.0–5.7 | 112 | 64 | 11 | те саме, теги `uploadthing@3.*`–`5.*` |
| Журнали змін 10 пакетів | 402 | 317 | — | `packages/*/CHANGELOG.md` на тезі 7.7.4 (`dropzone` — 6.13.3) |
| Реєстр npm | 44 | 44 | — | registry.npmjs.org |
| Приклади `examples/` | 24 | 24 | 7.7.4 | репозиторій на тезі 7.7.4 |

Разом 1137 записів паспорта, з них неповторних 620; в індексі 694 документи й 1790 фрагментів (`expected_passages` у
`checks.json`): однаковий текст різних версій — один уривок із переліком версій. Замір `quality`: по словах 1 із 10, за
змістом 3, разом 3, «як модель» 10 із 10. Своїми словами низько, бо перша десятка питає побутовими словами («змінити
колір кнопки»), а сторінки говорять назвами пропсів і функцій.

Чому сайт береться з репозиторію. Сайт docs.uploadthing.com зібрано з теки `docs/` монорепозиторію, і кожен тег
`uploadthing@X.Y.Z` тримає сайт тієї версії; береться останній тег кожної мінорної, 3.0–7.7 (32 знімки; тегу 6.11 немає,
ранніх 0.x–2.x — теж). Сторінки 7.x цитуються адресами docs.uploadthing.com, 6.x — v6.docs.uploadthing.com; сайту
ліній 3–5 уже немає, тож вони цитуються файлами на GitHub.

Чого немає. README пакетів з npm: у більшості це рядок «Learn more: docs.uploadthing.com», зміст — на сайті й у
журналах. Релізи GitHub повторюють журнали змін слово в слово. Код і тести пакетів, сам дашборд uploadthing.com,
Next.js, React, Nuxt, Express і S3 як окремі проєкти. Пререлізи (`-canary`, `-next`) не беруться.

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

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df uploadthing <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт кожної мінорної | дерево тегу `uploadthing@X.Y.Z`, тека `docs/src/app` чи `docs/src/pages` | `ghdocs-history` |
| журнали змін | `packages/*/CHANGELOG.md` | `changelog-regex` |
| реєстр npm | `uploadthing` і дев'ять `@uploadthing/*` | `npm-versions` |
| приклади | тека `examples/` на тезі 7.7.4 | `ghexamples` |

Нових читачів не знадобилося. Читачеві `ghdocs-history` додано поле `protocol_mdx` — сайт на шаблоні Tailwind UI
Protocol: тег `<Property name type default since>` стає рядком «`token` (`string`; default `…`; since 7.0): опис»
(інакше від опції лишався б опис без назви, типу й версії появи), позначка заголовка `{{ tag: 'function', since: '5.0'
}}` — дужками «(function, since 5.0)», назва сторінки береться з `docsMetadata({ title })`. Разом із цим спільний розбір
MDX тепер прибирає багаторядкові `import`/`export` цілими, а не лише їхній перший рядок.

`config.json`: `slug_rewrite` зводить ключі тек `docs/src/app/(docs)/…/page.mdx` (7.x) і `docs/src/pages/….mdx` (до 6.x)
до одного імені й ловить перейменування (`auth-security` → `concepts/auth-security`, `errors` → `concepts/error-handling`,
`nextjs/appdir` → `getting-started/appdir`), тож однаковий текст версій зливається. `title_match` ставить першим розділ,
чию назву-ідентифікатор запит містить дослівно: на запит `onUploadComplete` першим ішов вступ сторінки File Routes з
прикладом, де ця назва трапляється частіше, — «як модель» 9 → 10 із 10.

## Версії

Сторінки сайту несуть версію тегу, з якого взяті (`7.7.4`), журнали — версію запису, реєстр — версію пакета; фільтр
`version` бере мажор (`"7"`), мінор (`"7.7"`) або точну версію (`"6.13.3"`). За завантаженнями npm за тиждень до
25.10.2026 лінія 7 `uploadthing` тримає 90 % (найновіша 7.7.4 від 17.08.2025), лінія 6 — 7 %, тож промпт відповідає для
7.x, а для коду на v6 (`UPLOADTHING_SECRET` замість `UPLOADTHING_TOKEN`) каже, що змінилося.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/uploadthing-corpus-2026-10-25.tar.gz` (1137 текстів, паспорт і сховище
сирого `raw/`; перед видаленням текстів розпакований окремо й звірений із диском) і в копії на Windows-диску
`C:\Distr\uploadthing-corpus-2026-10-25.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/uploadthing/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/uploadthing-corpus-РРРР-ММ-ДД.tar.gz -C instances/uploadthing corpus raw
find instances/uploadthing/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/uploadthing/raw
gzip -9 -c instances/uploadthing/index/passages.json > instances/uploadthing/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти й сховище — лише після того, як
архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із ними повертається й сховище `raw/`:

```
tar -xzf ~/archives/docfactory/uploadthing-corpus-2026-10-25.tar.gz -C instances/uploadthing
./df uploadthing smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/uploadthing/index/passages.json.gz`,
далі `./df uploadthing vectors` заллє колекцію Qdrant (секунди на відеокарті, кілька хвилин на процесорі).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df uploadthing …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md, розділ
«Спільне середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df uploadthing sources --why   # перелік джерел і білий список
./df uploadthing refresh         # завантажити все задеклароване (близько 9 хвилин)
./df uploadthing manifest        # оновити паспорт
./df uploadthing setup           # Qdrant чи пошук лише по словах
./df uploadthing vectors         # залити корпус у docs-uploadthing
./df uploadthing smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df uploadthing serve          # порт 8900
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8900/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user uploadthing-docs http://127.0.0.1:8900/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `uploadthing-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
