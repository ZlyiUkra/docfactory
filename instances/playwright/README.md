# playwright — примірник фабрики docfactory

Двадцять восьмий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Playwright — фреймворк для
наскрізного тестування й автоматизації браузерів (Chromium, Firefox, WebKit) і його тест-раннер Playwright Test. Тут
документація з репозиторію microsoft/playwright на кожній мінорній версії від 0.10 до 1.64, сайт playwright.dev для
Node.js, Playwright MCP і Playwright CLI для агентів, README кожної стабільної версії пакетів, нотатки релізів і реєстр
версій npm, а також Playwright для .NET: сайт playwright.dev для .NET на кожній мінорній версії від 1.12 до 1.64, пакети
NuGet і нотатки релізів microsoft/playwright-dotnet. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо

Playwright виходить мінорною версією раз на місяць-два, і майже кожна щось додає: локатори `getByRole` (1.27),
`page.clock` (1.45), знімки доступності, UI-режим, компонентні тести, агентів для тестів. Тест, написаний під одну
версію, може спиратися на те, чого в іншій ще немає. Тому тут документація кожної мінорної лінії, а довідник API біля
кожного методу й опції каже, з якої версії вони є (`since: v1.29`).

Документацію playwright.dev для всіх мов збирають із тієї самої теки `docs/src` репозиторію; тут вона на кожній
версії, а поточний сайт для Node.js — окремо, з прикладами лише JavaScript і TypeScript.

Playwright для .NET (пакет NuGet `Microsoft.Playwright`) має свій сайт: ті самі посібники й довідник API, але з
прикладами C# і окремою вкладкою для кожного раннера тестів — NUnit, MSTest, xUnit. Тут він на кожній мінорній версії
від 1.12, першої стабільної в NuGet.

У яких фазах і днях планів навчання він потрібен — див. [../../docs/learning-map.md](../../docs/learning-map.md).

## Скільки цього

| Шар | Документів | Різних сторінок | Звідки |
|-----|-----------:|----------------:|--------|
| Документація репозиторію: гайди, Playwright Test, довідник API по класах, нотатки релізів JS | 2 785 | 249 | тека `docs/` microsoft/playwright на 74 тегах (0.10–1.64) |
| Сайт playwright.dev для Node.js, поточний стабільний реліз | 148 | 148 | `nodejs/versioned_docs/version-stable` microsoft/playwright.dev |
| Сайт: Playwright MCP | 32 | 32 | `mcp/` microsoft/playwright.dev |
| Сайт: Playwright CLI для агентів | 23 | 23 | `agent-cli/` microsoft/playwright.dev |
| Сайт playwright.dev для .NET, кожна мінорна 1.24–1.64 | 1 997 | 98 | `dotnet/versioned_docs/version-stable` на 41 коміті |
| Сайт playwright.dev для .NET, кожна мінорна 1.12–1.23 | 783 | 91 | теки `dotnet/versioned_docs/version-1.X` з історії |
| README стабільних версій `playwright`, `@playwright/mcp`, `@playwright/cli`, однакові тексти зведено | 163 | — | тег релізу на GitHub |
| Нотатки релізів GitHub чотирьох репозиторіїв | 355 | — | GitHub API |
| Пакети NuGet Playwright для .NET: огляди, лінії, README | 280 | — | api.nuget.org |
| Реєстр версій npm чотирьох пакетів | 11 | — | registry.npmjs.org |

Разом 6 577 документів; фрагментів в індексі — 34 200 (`expected_passages` у `checks.json`). Фрагменти — це шматки
документів між заголовками, по яких іде пошук; однаковий текст різних версій зливається в один з усіма версіями.
Найбільше — довідник API: файл класу (`class-page`, `class-locator`) змінюється майже в кожній версії, і кожен
розділ-метод, що змінився, стає окремим фрагментом. Сторінки сайту для .NET міняються з кожною версією майже всі:
внизу кожної стоїть блок посилань на всі класи. Тому редакцій тут 2 780 на 119 сторінок, але незмінні розділи
однаково зливаються в один фрагмент.

Замір `quality` на першому корпусі: перша десятка (питання своїми словами, без версії) — по словах 7 із 10, за змістом
7, разом 7; друга, «як модель» (назви API, з `version: "1.63"`, як велить промпт), — 9 із 10. Промах другої десятки —
«getByRole locator»: знаходить метод `getByRole` у довіднику API (`class-locator`, `class-page`), а не гайд
«Locators»; відповідь з таких уривків правильна, але вужча.

Після оновлення 19.10.2026 (1.64 і .NET) три питання кожної десятки замінено питаннями про .NET (встановлення
браузерів, `.runsettings`, базовий клас `PageTest`), а версію другої — на «1.64». Перша десятка — по словах 8 із 10, за
змістом 9, разом 7; «як модель» — 10 із 10.

**Версія у відповіді.** Без названої версії — Playwright 1.63: на 19.10.2026 24% завантажень `@playwright/test` за
тиждень (1.64 — 14%, 1.62 — 14%). Для .NET — теж 1.63: це найновіша версія `Microsoft.Playwright` у NuGet (сайт для .NET
уже на 1.64), а тижневої статистики за версіями NuGet не дає. Фільтр `version` — мінорна лінія: «1.63» бере 1.63.x і
JavaScript, і .NET.

## Пакети

| Пакет | Для чого | README | Реєстр | Релізи |
|-------|----------|:------:|:------:|:------:|
| `@playwright/test` | тест-раннер: `test`, `expect`, фікстури, конфігурація, репортери | заглушка, не взято | так | microsoft/playwright |
| `playwright` | бібліотека автоматизації браузерів (і CLI `npx playwright`) | так | так | microsoft/playwright |
| `@playwright/mcp` | сервер MCP: агент керує браузером через знімки доступності | так | так | microsoft/playwright-mcp |
| `@playwright/cli` | CLI для агентів: сесії, команди, знімки | так | так | microsoft/playwright-cli |

`playwright-core` має ті самі версії, що й `playwright`, тож його реєстр не взято. Збірки alpha, beta, next і canary
(у `playwright` їх понад п'ять тисяч, щоденні) не беруться ні в README, ні в реєстр: поле `skip_versions` читача
`npm-versions` відсіває їх, бо кожен фрагмент документа реєстру повторював би перелік усіх версій — 230 МБ із 258 у
кеші фрагментів.

Пакети NuGet (Playwright для .NET):

| Пакет | Для чого |
|-------|----------|
| `Microsoft.Playwright` | бібліотека: `Playwright`, `IBrowser`, `IPage`, `ILocator`, перевірки `Expect` |
| `Microsoft.Playwright.NUnit`, `.MSTest`, `.Xunit`, `.Xunit.v3` | базові класи тестів (`PageTest`, `ContextTest`) для свого раннера |
| `Microsoft.Playwright.TestAdapter` | спільна основа цих пакетів: налаштування з `.runsettings` |
| `Microsoft.Playwright.CLI` | давній глобальний інструмент `playwright` (1.0–1.2); його версії — з міткою «dotnet-cli-» |

Від кожного пакета — огляд з усіма стабільними версіями й датами, документ на кожну лінію (платформи, залежності) і
README тих версій, що його несуть (54 тексти). Огляд — про всі версії разом, тож версії не має; тому
`expect_unversioned` у `checks.json` — `true`.

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

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df playwright <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| документація всіх версій | тека `docs/` microsoft/playwright на останньому тезі кожної мінорної лінії | `ghdocs-history` |
| сайт для Node.js, MCP, CLI | microsoft/playwright.dev, гілка main | `ghdocs-history` |
| сайт для .NET 1.24–1.64 | microsoft/playwright.dev, останній коміт «roll to 1.X Playwright» кожної лінії | `ghdocs-history` |
| сайт для .NET 1.12–1.23 | теки `dotnet/versioned_docs/version-1.X` microsoft/playwright.dev в останній редакції | `ghdocs-history` |
| README пакетів | тег релізу кожної стабільної версії на GitHub | `npm-readme` |
| нотатки релізів | GitHub API | `ghreleases` |
| версії пакетів | реєстр npm | `npm-versions` |
| пакети .NET | реєстр NuGet | `nuget-package` |

Білий список — чотири хости: `api.github.com`, `raw.githubusercontent.com`, `registry.npmjs.org`, `api.nuget.org`. Сам
playwright.dev не читається: сайт збирається з репозиторіїв microsoft/playwright і microsoft/playwright.dev. Посилання
у відповідях можуть вести на playwright.dev.

Особливості, які варто знати:

- **Інші мови.** Тека `docs/src` спільна для JavaScript, Python, Java і C#: у спільних сторінках поруч стоять
  приклади всіх мов, а частина розділів позначена як лише для однієї мови. Сторінки, зроблені лише для Python, Java
  чи C# (`*-python.md`, `*-java.md`, `*-csharp.md`), з цієї теки не взято: C# — на сайті для .NET, де інших мов немає.
  Чистий JavaScript без інших мов — у сайті для Node.js, але лише для поточного релізу.
- **Формат довідника API** — вихідний, а не сайтовий: заголовок `## async method: Locator.click`, під ним `* since:
  v1.14`, опції — підрозділами. Посилання на інші члени записано як `[`method: Page.goto`]`.
- **Мітки сайту.** Сайт для Node.js має мітку «1.64», MCP — «0.0.83», CLI — «0.1.22»: це версії на день збирання,
  записані в `sources.json`. Після нового релізу їх треба змінити разом з оновленням.
- **Сайт для .NET за версіями.** З 1.24 playwright.dev тримає лише стабільну версію (`version-stable`), тож знімок
  кожної лінії — останній коміт «roll to 1.X Playwright» цієї лінії. До липня 2022 кожна версія лежала у своїй теці
  `version-1.X`, і старі теки згодом видаляли; їх узято з історії репозиторію в останній редакції. `{version}` у полі
  `folders` читача бере на кожному коміті лише теку його версії, `slug_rewrite` у `config.json` дає сторінкам старих
  тек той самий ключ, що й `version-stable`, а `families` — одну родину: редакції однієї сторінки зливаються, а не
  займають кілька місць у видачі. Тека `dotnet/docs/` (наступна версія) збігається з `version-stable` файл у файл і не
  береться.
- **Вкладки раннерів.** Код для NUnit, MSTest, xUnit і xUnit v3 стоїть у вкладках; поле `docusaurus_tabs` читача
  ставить перед кожною підпис «NUnit:», «MSTest:» (на сайті для Node.js — «npm:», «yarn:», «pnpm:»). Виноски
  `:::note` стають підписом «Note:» (поле `admonitions`).
- **Мітка «1.64» сайту для .NET** — з самого сайту: на день збирання в NuGet найновіша `Microsoft.Playwright` 1.63.0.
- **Релізи playwright-dotnet** починаються з 0.111: так нумерувалися випуски PlaywrightSharp до 1.0.
- **Стара документація (0.10–1.9)** лежала в корені `docs/`, з 1.10 — у `docs/src`; одна й та сама сторінка за
  різними шляхами — це історія, а не дублікат.
- **Назви класів сайту** («Fixtures», «Clock») збігаються з назвами гайдів, тож поле `title_prefix` додає їм «API:».
- **Тег `v.0.0.26`** у microsoft/playwright-mcp (із зайвою крапкою) не береться: номер версії з нього не читається.
- **Без README** лишилися найперші збірки `playwright` 0.0–0.9 і сім версій `@playwright/cli` 0.0.60–0.0.66.

## Межі, про які треба пам'ятати

Тут немає Playwright для Python і Java, документації Jest і Vitest (окремий примірник `vitest`), Testing Library
(примірник `testing-library`), MSW (примірник `msw`), Cypress, Selenium і Puppeteer, протоколу DevTools і самої
вебплатформи (примірник `mdn`). Issues і GitHub Discussions свідомо не взято.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку, як у testing-library і msw: у `corpus/` лежить лише паспорт
`index.json`, а сервер підіймається з кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до
символа — кеш тримає повний текст кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/playwright-corpus-2026-10-19.tar.gz` (69 МБ, 6 577 текстів, паспорт і
сховище сирого `raw/`; перед видаленням розпакований окремо й звірений із диском — нуль розбіжностей). В історії git
текстів немає ніде. Архів лежить лише на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/playwright/index/passages.json         # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/playwright-corpus-РРРР-ММ-ДД.tar.gz -C instances/playwright corpus raw
find instances/playwright/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/playwright/raw
gzip -9 -c instances/playwright/index/passages.json > instances/playwright/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/playwright-corpus-РРРР-ММ-ДД.tar.gz -C instances/playwright
./df playwright smoke
```

**Оновлення.** Новий випуск Playwright `1.x.y`: тег `v1.x.y` першим у `tags` джерела `pw-docs` (замість попереднього
тегу тієї самої лінії); мітка гілки `main` джерела `site-nodejs`; останній коміт «roll to 1.x Playwright» теки
`dotnet/versioned_docs/version-stable` — першим у `tags` джерела `site-dotnet`; мітки `site-mcp` і `site-agent-cli` — за
версіями `@playwright/mcp` і `@playwright/cli` у npm. README, реєстри npm і NuGet та релізи підхоплюються самі. Далі
`refresh`, `manifest`, `vectors`, `smoke`, `quality`.

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/playwright/index/passages.json.gz`, далі
`./df playwright vectors` заллє колекцію Qdrant (на відеокарті близько хвилини, на процесорі — близько двох годин).

## Установка venv

```
cd instances/playwright
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt     # ~2,6 ГБ: onnxruntime-gpu і колеса CUDA
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

Без відеокарти `onnxruntime-gpu` рахує на процесорі тими самими числами; тоді `vectors` іде години, а не хвилину.

## Збирання корпусу

```
./df playwright sources --why   # перелік джерел і білий список
./df playwright refresh         # завантажити все задеклароване (~2,5 години)
./df playwright manifest        # оновити паспорт
./df playwright setup           # Qdrant чи пошук лише по словах
./df playwright vectors         # залити корпус у docs-playwright (~1 хвилина на відеокарті)
./df playwright smoke           # перевірки
```

Найдовші частини `refresh` — документація репозиторію і сайт для .NET, близько години кожна: спершу читаються дерева
74 тегів чи 53 комітів (журнал тим часом мовчить), потім пишуться 2 785 і 2 780 текстів, і великі файли довідника API
йдуть повільно. README читаються по одному на кожну
стабільну версію. Без `GITHUB_TOKEN` у `.env` анонімного ліміту GitHub API (60 звернень на годину) не вистачить уже на
дерева. Довший за 30 хвилин крок із Claude Code запускають окремим процесом (`setsid nohup …`); обірваний `refresh`
продовжується з `--missing`.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df playwright serve           # порт 8788
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8788/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user playwright-docs http://127.0.0.1:8788/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `playwright-docs` і два інструменти `search_docs`, `read_section`. Якщо сесію Claude
Code відкрито раніше, ніж піднято сервер, вона покаже його як недоступний: у `/mcp` виберіть сервер і «Reconnect».

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
