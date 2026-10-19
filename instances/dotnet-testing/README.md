# dotnet-testing — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про тестування застосунків .NET бібліотеками xUnit.net (v2 і v3, з
аналізаторами й адаптером Visual Studio), NUnit (3–5 і NUnit 2, з адаптером, аналізаторами, консоллю й рушієм), bUnit
(компоненти Blazor), FluentAssertions і Shouldly (твердження), Moq і NSubstitute з NSubstitute.Analyzers (моки й
замінники), AngleSharp з усіма офіційними пакетами (Css, Js, Xml, XPath, Io, Wasm, Renderer, Wrappers, Diffing —
розбір і порівняння HTML, на Diffing стоїть `MarkupMatches` bUnit), FluentAssertions.Json та Respawn (очищення бази
між інтеграційними тестами). Документація англійською, усі стабільні мажорні й мінорні версії: сайти бібліотек (де
сайт має теги — на кожному випуску), README з кожного стабільного тегу, журнали змін і нотатки релізів; довідник API
кожної мінорної лінії з XML-документації пакетів NuGet; пакети NuGet з версіями, залежностями й README; код і тести на
останньому тезі кожної мажорної лінії. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Ці дев'ять бібліотек і їхні доповнення (пакети AngleSharp.*, FluentAssertions.Json) — не частина .NET: кожна має свою
нумерацію, свій сайт (або лише README) і свої пакети, і жоден інший примірник їх не тримає (testcontainers-dotnet знає
про xUnit.net лише те, як його використовують модулі Testcontainers). Разом вони — повний набір тестувальника .NET:
фреймворк тестів, твердження, моки, тести компонентів Blazor і чиста база між інтеграційними тестами. Звернувшись до
цієї одиниці з версією, дістаєш усе для впровадження саме на ній: сторінку сайту тієї версії, тип і член API того
випуску, пакет із залежностями, код і тест, нотатки релізу з несумісними змінами.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| xunit.net: посібники v2 і v3, правила аналізаторів, нотатки 101 стабільного випуску | 300 | 1 821 | xunit/xunit.net, тека `site/` |
| docs.nunit.org (сторінки правил аналізаторів ділять розділи з документацією NUnit.Analyzers, див. нижче) | 405 | 2 375 | nunit/docs, тека `docs/` (DocFX) |
| Документація NUnit 2.2.10, 2.4.8, 2.5.10, 2.6.4 | 323 | 1 171 | nunit/docs, `docs/legacy/` |
| bunit.dev, останній тег кожної з 54 мінорних ліній 1.0–2.12 | 1 910 | 587 | bUnit-dev/bUnit, `docs/site` (DocFX) |
| fluentassertions.com, 61 тег 4.19.3–8.11.0, сторінка releases і релізи, яких на ній немає | 296 | 872 | fluentassertions/fluentassertions |
| Shouldly, NSubstitute і NSubstitute.Analyzers, AngleSharp і Diffing, Moq, Respawn: документація з тегів, вікі, README, журнали, релізи; README FluentAssertions | 833 | 1 646 | репозиторії бібліотек |
| README xUnit.net, NUnit, bUnit з кожного тегу; релізи NUnit.Analyzers, журнал bUnit | 170 | 347 | xunit/xunit, nunit/nunit, nunit/nunit.analyzers, bUnit-dev/bUnit |
| Решта AngleSharp.* (Css, Js, Xml, XPath, Io, Wasm, Renderer, Scripting.JavaScript): `docs/` і README з тегів, журнали змін, релізи | 293 | 708 | AngleSharp/AngleSharp.* |
| FluentAssertions.Json: README з 59 тегів, релізи | 25 | 54 | fluentassertions/fluentassertions.json |
| NUnit.Analyzers (правила з 39 тегів), NUnit3TestAdapter (44 теги), консоль NUnit (38 тегів): документація й релізи | 685 | 2 079 | nunit/nunit.analyzers, nunit3-vs-adapter, nunit-console |
| Довідник API xUnit.net v2 (2.0–2.9, xunit.abstractions) і v3 (1.0–4.0, з консольним раннером) | 8 404 | 8 816 | XML-документація пакетів NuGet |
| Довідник API NUnit 2.5–2.6 і 3.0–5.0 | 6 810 | 5 364 | те саме |
| Довідник API bUnit, 54 лінії | 6 845 | 1 778 | те саме |
| Довідник API AngleSharp (25 ліній) і AngleSharp.Diffing (8) | 16 304 | 22 213 | те саме |
| Довідник API решти AngleSharp.*: Css (10 ліній), Js (6), Scripting.JavaScript (5), Xml (10), XPath (2), Io (12), Wasm (2), Renderer (6) | 4 514 | 6 529 | те саме |
| Довідник API FluentAssertions.Json (24 лінії) | 120 | 72 | те саме |
| Довідник API FluentAssertions (73 лінії), Shouldly (3), Moq (17), NSubstitute (24) | 18 291 | 7 851 | те саме |
| NuGet: версії, лінії, залежності й README 63 пакетів | 1 076 | 2 865 | реєстр NuGet |
| NuGet: ще 10 пакетів — AngleSharp.Css, Js, Xml, XPath, Io, Wasm, Renderer, Scripting.JavaScript, Wrappers, FluentAssertions.Json | 110 | 299 | те саме |
| Код і тести на останньому тезі кожної мажорної лінії (41 тег 10 репозиторіїв) | 13 527 | 82 497 | GitHub, поділені на типи й члени |

Разом 81 241 документ, 149 944 фрагменти (`expected_passages` у `checks.json`); код і тести — 55 % фрагментів,
довідник API — 35 %. 54 105 документів власних фрагментів не дали: кожен їхній розділ дослівно є в іншій версії, і той
фрагмент лише дістав їхні версії — незмінна сторінка сайту чи незмінний член API десятків ліній у пошуку один. Перша
черга (75 233 документи) зібрана менш ніж за годину: код, тести, сторінки bunit.dev і docs.nunit.org — зі сховища
сирого, засіяного з голих клонів (`tools/seed_git_store.py`, 53 397 записів за 31 с), пакети NuGet довідника API —
паралельним завантаженням просто у сховище сирого (451 МБ) і `build` без мережі, решта — мережею за 27 хвилин.
Вектори: половину (76 800 фрагментів) за 33 хвилини пораховано на процесорі, решту — на відеокарті (RTX 2070 Super у
WSL, `fastembed-gpu` у venv цього примірника): 76 260 фрагментів за 133 с, близько 570 за секунду; числа процесора й
відеокарти збігаються, тож точки обох лишились однією колекцією. Друга черга (ще 119 джерел, 5 850 документів, 9 866
нових фрагментів): корпус розпаковано з архіву першої, нові джерела — мережею за 10 хвилин, їхній довідник API —
`build` зі сховища сирого (пакети докачано заздалегідь), вектори на відеокарті — 27 с. Оновлення bUnit до 2.12.5
(19.10.2026): +158 документів, але лише +14 фрагментів — сторінки сайту й довідник API лінії 2.12 дослівно повторюють
2.11 і лише дістали її версію (+8 фрагментів коду й тестів, +5 пакетів NuGet, +1 журнал змін); для векторів
нових фрагментів 1 335, зайвих точок прибрано 1 321 (ті самі розділи тепер стоять під ідентифікатором найновішої
редакції), пораховано за 3 с.

Замір `quality` (10 запитів своїми словами): по словах 6, за змістом 4, разом 8; «як модель» (ті самі теми назвами
документації, як велить промпт) — 10 із 10; після другої черги й після bUnit 2.12.5 те саме число в число, smoke —
239 перевірок. Перший замір давав 7 і 6 із 10: видачу на запити назвами API забирали тести бібліотек; дотюнінг —
нижче, в «Особливостях».

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут
  немає: корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (466 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену, родини джерел-версій (`families`: лінії
  довідника API кожної бібліотеки, 53 редакції bunit.dev, пари README репозиторію й пакета NuGet, правила
  NUnit.Analyzers на сайті й у репозиторії), правила `slug_rewrite` для сторінок, що переїжджали, `fusion_depth: 10` і
  `demote` для тестів коду.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `requirements.txt` — склад venv, зокрема `fastembed-gpu` і `onnxruntime-gpu` з колесами CUDA.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df dotnet-testing <крок>`.

## Звідки документація

| Бібліотека | Сайт і документація | NuGet | GitHub |
|------------|---------------------|-------|--------|
| xUnit.net | xunit.net у чинному стані (тека `site/` xunit/xunit.net): посібники v2 і v3, конфігурація, правило на сторінку для аналізаторів, нотатки кожного стабільного випуску v2, v3, аналізаторів і адаптера VS | 37 пакетів (xunit, xunit.v3 і їхні складові, раннери, адаптер, аналізатори); API v2 2.0–2.9 і v3 1.0–4.0 | README 2.0–4.0.2; код і тести 1.9.2, 2.9.3, v3 1.1.0, 2.0.3, 3.2.2, 4.0.2 |
| NUnit | docs.nunit.org у чинному стані (nunit/docs, DocFX, з прикладами з `docs/snippets`) і документація NUnit 2.2.10, 2.4.8, 2.5.10, 2.6.4 | 10 пакетів (NUnit, NUnitLite, адаптери, аналізатори, консоль, рушій); API 2.5–2.6 і 3.0–5.0 | README 3.0–5.0; код і тести 3.14.0, 4.6.1, 5.0.0; релізи NUnit.Analyzers |
| bUnit | bunit.dev (`docs/site`, DocFX, з прикладами з `docs/samples`) на останньому тезі кожної з 54 мінорних ліній 1.0–2.12 | 7 пакетів; API 54 ліній | README, CHANGELOG.md; код і тести 1.40.0, 2.12.5 |
| AngleSharp | `docs/` (до 0.15 — `doc/`) і README на кожному стабільному тезі 0.2–1.8.5, CHANGELOG.md | AngleSharp, AngleSharp.Diffing; API 25 і 8 ліній | код і тести 0.17.1, 1.8.5; Diffing — README, CHANGELOG.md, код 0.18.2, 1.1.0 |
| Respawn | README на кожному тезі 0.3.0–7.0.0 | пакет без XML — довідника API немає | релізи; код і тести на останньому тезі кожного з 8 мажорів |
| FluentAssertions | fluentassertions.com (тека `docs/`, Jekyll) на кожному тезі 4.19.3–8.11.0 з таблицями порад; сторінка releases (8.x і гілка 7.x) | пакет; API 73 ліній 1.3–8.11 | README; релізи, яких немає на сторінці releases; код і тести 2.2–8.11.0 |
| Shouldly | docs.shouldly.org (тека `documentation/`, GitBook) на кожному тезі з 4.0, до того README | пакет; API 4.1–4.3 | релізи; код і тести 1.1.1.1, 2.8.3, 3.0.2, 4.3.0 |
| Moq | вікі (Quickstart, FAQ), README і `docs/` на кожному тезі 4.0–4.21, CHANGELOG.md до 4.18.4 і changelog.md 4.20–4.21 | пакет; API 4.0–4.18 (4.20 і 4.21 XML не несуть) | код і тести 4.21.0 |
| NSubstitute | nsubstitute.github.io (тека `docs/`, до 3.0 — `Source/Docs`) на кожному тезі 0.1–6.2, CHANGELOG.md до 5.3.0 | NSubstitute, NSubstitute.Analyzers.CSharp і VisualBasic; API 0.9–6.2 | релізи 6.x; код і тести 1.10.0–6.2.0; NSubstitute.Analyzers — правила NS1000–NS5004 і нотатки |
| Решта AngleSharp.* | `docs/` і README на кожному стабільному тезі Css 0.10–1.1.2, Js 0.12–1.1.1, Scripting.JavaScript 0.3–0.5.1, Xml 0.11–1.2.0, XPath 1.1.0–2.0.9, Io 0.3.0–1.1.0, Wasm 0.13–1.1.0, Renderer 0.1–0.6.0; CHANGELOG.md | 8 пакетів (власник FlorianRappl; XPath — з організації AngleSharp, автор denis-ivanov), AngleSharp.Wrappers (egil); API Css 10, Js 6, Scripting.JavaScript 5, Xml 10, XPath 2, Io 12, Wasm 2, Renderer 6 ліній | релізи; код не береться |
| FluentAssertions.Json | README на кожному тезі 2.1–8.0.0 | пакет; API 24 ліній 4.6–8.0 | релізи 4.20–8.0.0; код не береться |
| NUnit.Analyzers, NUnit3TestAdapter, консоль NUnit | `documentation/` (правила) і README NUnit.Analyzers на 39 тегах; README, `docs/`, налагодження й фільтри адаптера на 44 тегах; README, VERSIONING.md, PLATFORM_SUPPORT.md консолі на 38 тегах | пакети вже в рядку NUnit; XML вони не несуть | релізи адаптера (27 з тегом «V…» і 17 без) і консолі; код не береться |

Читачі: `ghdocs-history-kramdown` (новий) — сайти й README з тегів, документація всіх нових джерел; `docfx` (нове поле
`title_from`) — docs.nunit.org і bunit.dev; `ghdocs-history-html` — документація NUnit 2; `nuget-xmldoc` і
`nuget-package` — NuGet; `ghcode-history` (нове поле `outline_tabs`) — код і тести; `ghreleases` і `ghreleases-stable`
(теги адаптера «V6.3.1»), `changelog-regex`, `ghwiki-page` — релізи, журнали й вікі Moq.

Ліцензії джерел (за реєстром NuGet): xUnit.net і Respawn — Apache-2.0; NUnit, bUnit, AngleSharp і AngleSharp.Diffing —
MIT, docs.nunit.org — CC BY-NC-SA 4.0; Shouldly, Moq і NSubstitute — BSD-3-Clause; FluentAssertions до 7.x —
Apache-2.0, з 8.0 — комерційна ліцензія Xceed, документація публічна. Тексти корпусу в git не потрапляють: вони
відновлюються з `sources.json`.

Що нового в коді фабрики для dotnet-testing:

- **Читач `ghdocs-history-kramdown`** — той самий `ghdocs-history` через обгортку контексту, а сторінка перед розбором
  очищується від розмітки генераторів сайтів .NET-бібліотек: списки атрибутів kramdown (`{: .issue-link }` — 244 рази
  в нотатках випусків xunit.net) і якорі заголовків (`## Class Fixtures{ #class-fixture }`), теги Liquid
  `{% examplecode csharp %}` (стають блоком коду) з прихованою заготовкою `{% requiredcode %}` (зникає) — сайт
  NSubstitute 1.x–2.x, виноски `> [!NOTE]`, рядки «snippet source | anchor» вставок mdsnippets (Shouldly). Поле
  `jekyll_data` розгортає вставки `{% include assertion-comparison.html … examples=site.data.tips.… %}` сторінки порад
  FluentAssertions: понад сотня пар «як було — як краще» з повідомленнями про збій лежить у YAML `docs/_data`, і без
  розгортання сторінка була б порожньою; файл даних, якого в тезі ще немає, Jekyll не малює, і вставка просто зникає.
- **`title_from: "heading"` у `docfx`**: docs.nunit.org пише в шапці сторінки лише `uid` («attribute-testcase»), і без
  поля назвою документа ставав саме він, а «# TestCase» — першим розділом.
- **`outline_tabs: true` у `ghcode-history`**: xUnit.net і bUnit пишуть код табуляцією, а поділ C# на типи й члени
  міряє відступ пробілами — клас лишався одним розділом (`BunitContext` — сім заголовків замість шістнадцяти).
- **`title_heading` у `ghdocs-history-html`**: документація NUnit 2 не має <h1> — назва стоїть у <h2> чи <h3>, а
  <title> у всіх 323 сторінок — «NUnit.org»; з полем назвою стає перший такий заголовок.
- **Поле пошуку `demote`** (`common/profile.py`, `server/spec_mcp.py`): розділ, чиє ім'я документа збігається з
  виразом, у списку кожного способу пошуку стоїть на N місць нижче. Тут вираз — тести коду (`…-src-…-tests-…`,
  `…-specs-…`), N = 5: тести повторюють імена API в назвах методів і на запит «xUnit1001 Fact methods cannot have
  parameters» займали три перші місця, а сторінка правила стояла четвертою. Без поля видача та сама, що й була.

Особливості:

- **Версії несуть назву продукту**: бібліотеки нумерують випуски незалежно, і без мітки `version: "4.3"` змішував би
  NUnit, NSubstitute і FluentAssertions. Мітки: `xunit-2.9.3` (xUnit.net v2 і його складові), `xunit-v3-3.2.2` (пакети
  xunit.v3), `xunit-runner-visualstudio-`, `xunit-analyzers-`, `xunit-abstractions-`, `nunit-` (NUnit і NUnitLite,
  `nunit-2.6.4` — NUnit 2), `nunit3testadapter-`, `nunittestadapter-`, `nunit-analyzers-`, `nunit-console-`, `bunit-`,
  `anglesharp-`, `anglesharp-diffing-`, `anglesharp-css-`, `-js-`, `-scripting-javascript-`, `-xml-`, `-xpath-`,
  `-io-`, `-wasm-`, `-renderer-`, `-wrappers-` (усі з префіксом `anglesharp-`), `fluentassertions-json-`, `respawn-`,
  `fluentassertions-`, `shouldly-`, `moq-`, `nsubstitute-`, `nsubstitute-analyzers-`. Лінії мінорні
  (`version_line_depth: 2`): `"nunit-3.13"` бере лінію, `"nunit-4"` — усі 4.x.
- **Сайти без тегів.** Репозиторії xunit.net і docs.nunit.org тегів не мають, тож їхні сторінки взято в чинному стані
  (xunit.net — коміт 7fc4111f від 07.10.2026, nunit/docs — eafa6cf5 від 13.10.2026) з версіями продуктів на день
  збирання: загальні сторінки xunit.net — `xunit-2.9.3, xunit-v3-4.0.2`, сторінки v2 чи v3 — свою, правила
  аналізаторів — `xunit-analyzers-2.2.0`, нотатки випуску — номер свого випуску; docs.nunit.org — `nunit-5.0.0`,
  розділи адаптера, аналізаторів і рушія — `nunit3testadapter-6.3.1`, `nunit-analyzers-4.15.0`,
  `nunit-console-3.22.0`. Фільтр старої лінії ці сторінки ховає, тож промпт велить шукати і з версією, і без неї.
- **Версія за замовчуванням** — найпопулярніша за завантаженнями в NuGet: xUnit.net 2.4.1 (v3 — 3.2.2), NUnit 3.13.3,
  NUnit3TestAdapter 4.5.0, bUnit 2.7.2 і 1.40.0 (завантажено майже порівну — відповідь для обох), FluentAssertions
  6.12.0, Shouldly 4.3.0, Moq 4.20.72, NSubstitute 5.3.0, AngleSharp 0.17.1, AngleSharp.Diffing 1.0.0, Respawn 6.2.1.
- **Сторінки, що переїжджали**, зведено правилами `slug_rewrite`: документація AngleSharp до 0.15 лежала в `doc/`
  плоско (далі `docs/general`, `docs/tutorials`), сторінки FluentAssertions до 5.7 — просто в `docs/` (далі
  `docs/_pages`), сторінки NSubstitute до 6.0 — у Jekyll `_posts` з датою в імені (далі
  `docs/help/<сторінка>/index.md`), документація NUnit 2 — у теці кожної версії (`docs/legacy/2.6.4/…`). Скан кешу
  фрагментів не знаходить жодного ключа розділу, спільного для джерел різних родин; README репозиторію і README пакета
  NuGet кожної бібліотеки — одна родина.
- **Довідник API** — з найновішої версії кожної мінорної лінії; без вкомпільованих поліфілів і анотацій (`System.*`,
  `Microsoft.CodeAnalysis.*`, `JetBrains.Annotations` — 81 тип на кожну лінію Shouldly), без простору
  `NUnit.Framework.Internal` і без 12 тисяч згенерованих обгорток DOM AngleSharp у bunit.web (`Bunit.Web.AngleSharp`,
  у 1.8–1.25 — `AngleSharpWrappers`). Пакети без XML довідника не дають: Respawn, Moq 4.20–4.21, NSubstitute 3.x,
  Shouldly до 4.1, NUnit.Engine, аналізатори, адаптери й консолі (крім консольного раннера xunit.v3),
  AngleSharp.Wrappers: за XML-документацією його версій 1.0–2.0 типів немає, тож обгортки, що заливали індекс у
  bunit.web, тут не повернулись.
- **Код і тести** — на останньому тезі кожної мажорної лінії. Асерти xUnit.net живуть у підмодулі xunit/assert.xunit і
  в код не входять (їх описує довідник API xunit.assert); код NUnit 2 і Moq 3 у цих репозиторіях не живе; код нових
  доповнень, аналізаторів, адаптерів і консолей не береться; знімки Verify тестів генератора bUnit (`*.verified.cs`,
  76 згенерованих обгорток по ~90 КБ) не беруться.
- **Решта AngleSharp.*.** Взято всі пакети власника AngleSharp на NuGet (FlorianRappl) — Css, Js, Xml, Io, Wasm,
  Renderer і старий AngleSharp.Scripting.JavaScript (під цим іменем жив нинішній Js до 0.12, тож теги, журнал і релізи
  репозиторію AngleSharp.Js розділено на два джерела з різною міткою версії) — і два зі списку користувача: XPath
  (репозиторій у організації AngleSharp, пакет denis-ivanov) і Wrappers (egil, репозиторій без тегів і документації).
  Репозиторії AngleSharp.Demos.*, Infrastructure.*, Specifications.Url і сайт anglesharp.github.io не взято. Сторінки,
  що перейменовано між тегами (Questions, Render-Tree), зведено правилами `slug_rewrite`. Релізи GitHub беруться разом
  із журналом CHANGELOG.md: імена записів журналу й релізів тегу без «v» (`1.0.0`) збігались, тож імена релізів несуть
  `-release`.
- **NUnit.Analyzers, NUnit3TestAdapter і консоль NUnit — без коду.** Сторінка правила NUnit.Analyzers на
  docs.nunit.org і в `documentation/` репозиторію — той самий текст: ключі зведено правилом `slug_rewrite` і родиною
  `nunit-analyzers-rules`, тож розділ займає одне місце й несе версії з обох джерел. Теги адаптера бувають «V6.3.1»,
  «v6.2.0» і «5.1.0»; `ghreleases` велику «V» не розбирає, тож релізи — двома джерелами (`ghreleases-stable` з
  `tag_prefix: "V"` і `ghreleases` без таких тегів). Релізи xunit/xunit, xunit.analyzers, visualstudio.xunit і
  nunit/nunit не беруться: це посилання на сторінки xunit.net і docs.nunit.org, що вже в корпусі.
- **FluentAssertions 8** — під комерційною ліцензією Xceed; документацію взято, бо вона публічна.
- **Головна гілка Shouldly** вже несе документацію 5.0 (передреліз), тож сторінки взято лише з тегів стабільних
  випусків. Сторінка releases FluentAssertions на тезі 8.11.0 тримає записи самого 8.11.0 під «Unreleased»: їх, як і
  записи 3.3–5.5, яких сторінка не має, дають релізи GitHub.
- **Дотюнінг якості.** Перший замір — «як модель» 6 із 10, своїми словами 7. Обгортки AngleSharp у bunit.web 1.8–1.25
  жили в іншому просторі імен (`AngleSharpWrappers`) і проскочили відсів — ще 12 121 фрагмент, що стояв на
  `QuerySelector` поряд із самим AngleSharp; їх прибрано. Далі — замір одним процесом із завантаженим індексом:
  `max_per_doc` 1–3 не дає нічого (видачу забирають тести, а не повтори однієї сторінки), `fusion_depth: 10` повертає
  класові фікстури xUnit.net (розділ дев'ятий по словах і третій за змістом); відсув тестів (`demote`) на 3 місця
  повертає сторінку правила xUnit1001 у трійку, на 5 — ще й дає своїми словами 8. Дві теми були розмиті й переписані:
  Moq — перевірка, що метод не викликали жодного разу (`Times.Never`, як у вікі Quickstart, яка `Times.Exactly` не
  згадує), AngleSharp — лише розбір рядка HTML, без запитів CSS. Цілей не дописувано.
- **Запити `quality`** записано так, як їх ставить людина своїми словами. Промахи своїми словами: попередження
  аналізатора xUnit1051 (знаходяться `TestContext.Current.CancellationToken` в API й коді — суміжне, але не правило) і
  розбір рядка HTML в AngleSharp (знаходяться `CreateHtmlDocument` і `ToHtml`); назвами документації знаходяться
  обидва.

## Межі, про які треба пам'ятати

- Усе англійською.
- Лише стабільні випуски: передрелізи NuGet і нотатки передрелізів не взято; xunit.net і docs.nunit.org — у стані на
  день збирання.
- Не взято: MSTest, Playwright, Testcontainers, Coverlet, AutoFixture, пакети розширень NUnit (`NUnit.Extension.*`),
  NUnitLite 0.x–1.x як окремий фреймворк, платформні пакети `xunit-console-tool.<rid>` і `xunit.v3.*.aot.*`, крім
  мета-пакетів, пакети AngleSharp.* інших авторів (Verify.AngleSharp тощо), код доповнень AngleSharp,
  FluentAssertions.Json, аналізаторів, адаптерів і консолей.
- bUnit доведено до 2.12.5 (19.10.2026, того самого дня, що й перша збірка): лінія 2.12 є на сайті, в довіднику API,
  README, журналі змін, пакетах NuGet і в коді з тестами. Випуски bUnit після 2.12.5 потраплять у корпус лише
  оновленням за схемою нижче.
- Довідник API з XML не перелічує успадкованих членів і не має прикладів, яких немає в самому XML.

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/dotnet-testing-corpus-2026-10-19-c.tar.gz` (627 МБ; 81 241 текст,
паспорт і сховище сирого `raw/`, 58 303 файли; перед видаленням розпакований окремо й звірений з диском — нуль
розбіжностей). Це третій архів: перший (75 233 тексти) і другий (81 083 тексти) після оновлень видалено. Лише на
цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/dotnet-testing-corpus-РРРР-ММ-ДД.tar.gz -C instances/dotnet-testing corpus raw
find instances/dotnet-testing/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/dotnet-testing/raw
gzip -9 -c instances/dotnet-testing/index/passages.json > instances/dotnet-testing/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/dotnet-testing-corpus-2026-10-19-c.tar.gz -C instances/dotnet-testing
./df dotnet-testing smoke
```

**Оновлення.** Генератор `sources.json` лишився поза репозиторієм, тож правка — руками за зразком сусідніх джерел.
Оновлення архівного примірника: розпакувати архів, додати джерела, `refresh` лише нових, `manifest`, `vectors`,
`smoke`, `quality`; новий архів — під новою назвою, розпакований окремо й звірений з диском, і лише тоді видалити
тексти, `raw/` і старий архів. Новий стабільний випуск бібліотеки: тег — першим у `tags` джерел README і сайту з
тегами (`*-readme`, `*-docs`, а в доповнень AngleSharp.*, FluentAssertions.Json, адаптера й консолі NUnit —
`anglesharp-<бібліотека>-docs`, `fluentassertions-json-docs`, `nunit3testadapter-docs`, `nunit-console-docs`); нова
мінорна лінія — ще й джерело довідника API `<бібліотека>-api-x-y` (пакети `Пакет/x.y.z`, адреса nupkg, `within`) і
його id у відповідній родині `families`, а для bUnit — джерело `bunit-docs-x-y` на новому тезі (попереднє найновіше
дістає `link: "github"`); новий мажор — тег у `tags` джерела коду `*-src`; нова мінорна лінія в уже взятому
мажорі — новий тег замість попереднього найновішого того мажору (bUnit: v2.12.5 замість v2.11.3, адреса журналу
`bunit-changelog` — теж на новий тег), а редакції файлів, що жили лише на старому тезі, лишаються в `corpus/`
сиротами: їх прибирають перед `manifest`. xunit.net і docs.nunit.org — новий коміт у
`tags` (`xunit-site`, `nunit2-docs`) чи в адресі дерева (`nunit-docs`) разом з мітками версій на день збирання.
Реєстри NuGet, релізи й журнали підхоплюються самі. Код, тести й сторінки DocFX тягнути не мережею, а голим клоном:
`./df dotnet-testing list <джерела *-src>` (дерева тегів через API), далі `tools/seed_git_store.py --instance
dotnet-testing --clone <власник/репо>=<клон> …` (сторінкам DocFX засів кладе й дерево) і `./df dotnet-testing build
<ті самі джерела й bunit-docs-*, nunit-docs>`; пакети NuGet довідника API — завантажити просто у сховище сирого, далі
`build`; решта — `./df dotnet-testing refresh <джерела>`. Далі `manifest`, `vectors`, `smoke`, `quality`.

## Установка venv

```
cd instances/dotnet-testing
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt     # ~2,6 ГБ: onnxruntime-gpu і колеса CUDA
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

Без відеокарти `onnxruntime-gpu` рахує на процесорі тими самими числами; тоді `vectors` іде годину-дві, а не хвилини.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не треба
— потрібен лише `vectors`, якщо колекції ще немає.

```
./df dotnet-testing sources --why   # перелік джерел і білий список
./df dotnet-testing refresh         # завантажити задеклароване (код, DocFX і API — краще з клонів, див. вище)
./df dotnet-testing manifest        # оновити паспорт
./df dotnet-testing setup           # Qdrant чи пошук лише по словах
./df dotnet-testing vectors         # залити корпус у docs-dotnet-testing (кілька хвилин на відеокарті)
./df dotnet-testing smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df dotnet-testing serve          # порт 8868
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8868/mcp`; індекс по словах
збирається з кешу кілька десятків секунд. Якщо порт зайнятий, сервер скаже про це й вийде: значить, `serve` цього
примірника вже десь запущений; хто тримає порт, покаже `ss -ltnp | grep 8868`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user dotnet-testing-docs http://127.0.0.1:8868/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Можна й не реєструвати глобально: `.mcp.json` цієї теки вже містить запис
сервера для сесії, відкритої тут.

**3. Перевірити.** `/mcp` — має бути `dotnet-testing-docs` і два інструменти `search_docs`, `read_section`. Якщо
`/mcp` показує `failed`, сервер не запущено або запущено з іншим портом.

Зупинка — Ctrl+C у терміналі сервера.
