# emberjs — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Ember.js за його документацією: гайди guides.emberjs.com
(компоненти, шаблони, `@tracked` і автовідстеження, маршрути й `model()`, сервіси, Ember Data, тести, `<template>`
і `.gjs`, TypeScript, посібник-підручник, перехід на Octane) на кожну мінорну 1.10–7.2, довідник API api.emberjs.com —
Ember 1.0–7.3 і Ember Data 1.13–5.5, гайд застарілого deprecations.emberjs.com, гайди Ember CLI, гайди WarpDrive
(нова Ember Data), усі дописи блогу blog.emberjs.com, 267 RFC, журнали змін Ember і WarpDrive, релізи GitHub
`ember.js`, `ember-cli` і `warp-drive`, записи npm `ember-source`, `ember-cli` і `ember-data`. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

Ember живе довго й міняється хвилями: класичні компоненти й `this.get()` 1.x–3.x, Octane з Glimmer-компонентами й
`@tracked` (3.15), формат `<template>` у `.gjs` (5.x–6.x), Ember Data, що стає WarpDrive. Відповідь залежить від версії,
тож тут гайди кожної мінорної, довідник кожної версії і все, що пояснює переходи: застаріле, RFC, блог, журнали.

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Гайди guides.emberjs.com | 4 556 | 94 | `ember-learn/guides-source`, теки `guides/v1.10.0` … `guides/v7.2.0` |
| Довідник API Ember | 13 708 | 105 | `ember-learn/ember-api-docs-data`, `json-docs/ember/<версія>/` (1.0–7.3) |
| Довідник API Ember Data | 3 952 | 68 | те саме, `json-docs/ember-data/<версія>/` (1.13–5.5) |
| Гайд застарілого | 408 | — | `ember-learn/deprecation-app`, тека `content/` |
| Гайди Ember CLI | 37 | — | `ember-learn/cli-guides`, тека `guides/` |
| Гайди WarpDrive | 118 | — | `warp-drive-data/warp-drive`, тека `guides/` |
| Блог blog.emberjs.com | 459 | — | `ember-learn/ember-blog`, тека `content/` |
| RFC | 267 | — | `emberjs/rfcs`, тека `text/` |
| Журнали змін Ember і WarpDrive | 210 + 36 | 210 + 36 | `CHANGELOG.md` гілки `main`: Ember 2.1.0–7.4.0, WarpDrive 3.28.2–5.9.1 |
| Релізи GitHub | 281 + 222 + 131 | так само | `emberjs/ember.js`, `ember-cli/ember-cli`, `warp-drive-data/warp-drive`, без передрелізів |
| npm `ember-source`, `ember-cli`, `ember-data` | 7 + 9 + 6 | 236 / 260 / 257 | реєстр npm: версії, дати, мітки |

Разом 24 408 записів паспорта. В індексі 32 911 фрагментів (`expected_passages` у `checks.json`): однакові розділи
різних версій злито в один фрагмент з переліком версій. Замір `quality`: по словах 5 із 10, за змістом 6, разом 6,
«як модель» 10 із 10.

Чого немає:

- Передрелізів (alpha, beta, canary) — ні в релізах, ні в npm.
- Гайдів 7.3: у `guides-source` теки `v7.3.0` ще немає, хоч довідник 7.3 уже вийшов.
- Гайдів до 1.10 і довідника Ember Data до 1.13 — їх немає в джерелах сайтів.
- Приватних членів класів (`access: private`): сайт api.emberjs.com їх теж ховає.
- Версій у застарілого, гайдів CLI і WarpDrive, блогу й RFC: це знімок гілки на день збирання.

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

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df emberjs <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| гайди | `ember-learn/guides-source`, теки версій у `guides/` на одному коміті `master` | `ghdocs-folders` |
| довідник API | `ember-learn/ember-api-docs-data`, записи YUIDoc у JSON | `ember-api-json` |
| застаріле, CLI, WarpDrive, блог, RFC | теки п'яти репозиторіїв на одному коміті гілки, `.md` і `.mdx` | `ghdocs-history` |
| журнали змін | `CHANGELOG.md` `emberjs/ember.js` і `warp-drive-data/warp-drive` | `changelog-regex` |
| релізи Ember і Ember CLI | GitHub API релізів; тег — за виразом `tag_pattern` | `ghreleases-pattern` |
| релізи WarpDrive | GitHub API релізів, теги `v…` без передрелізів | `ghreleases-stable` |
| npm | `registry.npmjs.org/ember-source`, `ember-cli`, `ember-data` | `npm-versions` |

**Гайди.** Тегів версій у `guides-source` немає: кожна мінорна лежить окремою текою (`guides/v5.4.0/…`), 94 теки й
14 тисяч файлів на одному коміті. Більшість сторінок між сусідніми версіями не міняється, тож читач `ghdocs-folders`,
зроблений для цього примірника, бере кожен різний текст один раз (4 556 завантажень замість 14 127), а його версіями
стають усі теки, де він лежав саме таким. Назв у файлах немає (сайт тримає їх у `pages.yml`), тож назва береться зі
шляху: «Components / Component arguments and html attributes».

**Довідник API.** api.emberjs.com — застосунок, що читає JSON з репозиторію `ember-api-docs-data`: вивід YUIDoc на
кожну версію, без готового тексту сторінки. Читач `ember-api-json`, теж зроблений для цього примірника, складає
документ на клас, простір імен чи модуль: шапка (модуль, батьківський клас, домішки, файл), опис і підрозділ на кожен
власний метод, властивість чи подію з параметрами, `Since` і позначкою застарілого. Успадковане — лише перелік імен під
назвою джерела. Записи на зразок `@ember/test` і `Ember.Test` мають однаковий слаг, тож при збігу запис з «@» дістає в
імені «at-».

**Релізи.** З Ember 6.0 і Ember CLI 6.5 ім'я пакета стоїть у кінці тегу (`v7.4.0-ember-source`), а старші теги прості
(`v5.12.0`). Читач `ghreleases-pattern` бере тег за виразом і версією робить лише номер, тож обидва вигляди дають
«7.4.0» і «5.12.0», а бети й релізи сусідніх пакетів (`@glimmer/component`) випадають.

## Версії

Гайди й довідник Ember несуть мінорну лінію: `version: "6"` бере всю шосту мажорну, `"6.4"` — одну мінорну. Ember Data
нумерується окремо й несе мітку з префіксом: `"ember-data-5"`, `"ember-data-5.4"`; релізи й npm Ember CLI —
`"ember-cli-6"`. Застаріле, гайди CLI й WarpDrive, блог і RFC версії не мають і знаходяться завжди.

Без версії поточні гайди й довідник стоять попереду: поле `demote` у `config.json` опускає на десять місць RFC, блог,
журнали змін і релізи GitHub. Інакше на запит «як зробити» першими йшли обговорення RFC і дописи про випуски. З номером
RFC чи версії в запиті вони знаходяться як і раніше.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку. У `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant. Відповіді ті самі до символа, бо кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/emberjs-corpus-2026-11-01.tar.gz` (24 408 текстів, паспорт і сховище
сирого `raw/`; перед видаленням текстів архів розпаковано окремо й звірено з диском) і в копії на Windows
`C:\Distr\emberjs-corpus-2026-11-01.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/emberjs/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/emberjs-corpus-РРРР-ММ-ДД.tar.gz -C instances/emberjs corpus raw
find instances/emberjs/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/emberjs/raw
gzip -9 -c instances/emberjs/index/passages.json > instances/emberjs/index/passages.json.gz
```

Після цього закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Тексти й сховище видаляють лише тоді,
коли архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із текстами повертається сховище сирого:

```
tar -xzf ~/archives/docfactory/emberjs-corpus-2026-11-01.tar.gz -C instances/emberjs
./df emberjs smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Їхні
перевірки `smoke` чесно пропускає з позначкою «корпус в архіві».

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/emberjs/index/passages.json.gz`.
Далі `./df emberjs vectors` заллє колекцію Qdrant: менше хвилини на відеокарті, довше на процесорі.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df emberjs …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як збудувати його один раз і як `df` обирає між ними — у кореневому README, розділ
«Спільне середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df emberjs sources --why   # перелік джерел і білий список
./df emberjs refresh         # завантажити все задеклароване (близько 4 годин: 24 тисячі текстів, з них API — 17,7)
./df emberjs manifest        # оновити паспорт
./df emberjs setup           # Qdrant чи пошук лише по словах
./df emberjs vectors         # залити корпус у docs-emberjs
./df emberjs smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити його працювати:

```
cd ~/Projects/docfactory
./df emberjs serve          # порт 8940
```

Сервер готовий, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8940/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user emberjs-docs http://127.0.0.1:8940/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування. Вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell або додати сервер кнопкою «Add server» у вікні
`/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` має показати `emberjs-docs` і два інструменти: `search_docs` і `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта (scope запису, «address already in use») — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
