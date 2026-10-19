# dotnet — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про .NET 1.0–10.0 (колишній .NET Core) і мову C# — від нового в кожному
випуску, CLI `dotnet`, критичних змін, діагностики й вбудованих метрик, розгортання й контейнерів до основ (DI,
конфігурація, журналювання, хостинг, HttpClient, System.Text.Json), C#, F#, Visual Basic, .NET Framework, довідника
API базової бібліотеки й Microsoft.Extensions.*, стандарту й специфікацій C#, підтримки й CVE кожного випуску.
Документація англійською, усі стабільні мажорні й мінорні версії: сайт learn.microsoft.com/dotnet кожної версії; стандарт
C# і специфікації можливостей; документація компілятора Roslyn; довідник API з dotnet/dotnet-api-docs і з
XML-документації пакетів NuGet; метадані й нотатки випусків dotnet/core; документація dotnet/runtime і dotnet/sdk. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../../README.md).

**Документація мови C# є лише в цьому примірнику.** Окремого примірника C# немає: довідник і посібник мови
(learn.microsoft.com/dotnet/csharp), стандарт C# (ECMA-334), специфікації можливостей C# 7.0–14.0 і документація
компілятора Roslyn — тут, на сервері `dotnet-docs`. Так сказано й в описі інструмента пошуку, який бачить модель.

## Навіщо одна одиниця

Звернувшись до неї з версією, дістаєш усе, що потрібно для роботи саме на цій версії: сторінку сайту тієї редакції,
тип і член API того випуску, критичні зміни й нове цієї лінії, дату кінця підтримки й CVE кожного патча. ASP.NET Core,
Entity Framework і Testcontainers мають власні примірники (`aspnetcore`, `entityframework`, `testcontainers-dotnet`);
Microsoft.Extensions.*, які примірник `aspnetcore` свідомо не брав, — тут, усіма лініями.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Сайт learn.microsoft.com/dotnet: 13 знімків 1.0–10.0 | 147 236 | ≈228 000 | dotnet/docs |
| Сайт — чинна гілка `main` | 12 966 | ≈12 000 нових | те саме |
| Стандарт C# (ECMA-334 v5, v6, v7, чернетки v8, v9) і специфікація C# 6 | 172 | ≈4 800 | dotnet/csharpstandard, dotnet/csharplang |
| Специфікації можливостей C# 7.0–14.0 | 129 | ≈2 100 | dotnet/csharplang |
| Документація Roslyn і критичні зміни компіляторів C#, VB, Razor за версіями .NET | 253 | ≈2 200 | dotnet/roslyn |
| Специфікація Visual Basic | 13 | ≈750 | dotnet/vblang |
| Довідник API learn.microsoft.com/dotnet/api з прикладами C# | 11 485 | ≈175 600 | dotnet/dotnet-api-docs |
| API спільного фреймворку, 11 ліній 2.0–10.0 | 36 307 | ≈100 400 | XML пакетів Microsoft.NETCore.App(.Ref) |
| API Microsoft.Extensions.*, 1 589 ліній пакетів | 60 114 | ≈13 900 | XML пакетів NuGet |
| Випуски: огляд ліній, 13 ліній, 271 випуск | 285 | ≈1 400 | dotnet/core releases*.json |
| Нотатки випусків 1.0–10.0 | 4 704 | ≈13 300 | dotnet/core release-notes |
| Документація dotnet/runtime (`docs/`) і dotnet/sdk (`documentation/`) | 549 | ≈7 700 | GitHub |

Разом 274 213 документів, 562 355 фрагментів (`expected_passages` у `checks.json`). Фрагменти рахуються за першим
документом, де розділ трапився: незмінний розділ сусідніх знімків чи ліній — один фрагмент з усіма їхніми версіями, тож
60 тисяч документів Microsoft.Extensions.* дали лише 14 тисяч фрагментів. Корпус зібрано за 15 хвилин: сайт,
dotnet-api-docs і dotnet/core — зі сховища сирого, засіяного з голих клонів (`tools/seed_git_store.py`), пакети NuGet
(1 754, 0,6 ГБ) — паралельним завантаженням за 2,5 хвилини, репозиторії C#, Roslyn, runtime і sdk — мережею за 5
хвилин. Вектори — на відеокарті (RTX 2070 Super у WSL, `fastembed-gpu` у venv цього примірника): 12 хвилин, близько
800 фрагментів за секунду.

Замір `quality` (10 запитів своїми словами): по словах 5, за змістом 1, разом 5; «як модель» (ті самі теми назвами
документації, як велить промпт) — 10 із 10. Чотирнадцять редакцій того самого сайту роблять запити своїми словами
важкими: старі редакції сторінок під давніми іменами забирають місця у видачі.

## Що в цій теці

- `sources.json` — звідки корпус будується (193 джерела), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену, родини джерел-версій (`families`: сайт,
  довідник API, стандарт C#).
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `requirements.txt` — склад venv, зокрема `fastembed-gpu` і `onnxruntime-gpu` з колесами CUDA.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.
- `corpus/`, `index/`, `raw/` — лише локально, у git не йдуть (див. «Корпус лише локально»).

Кроки нижче запускаються з кореня фабрики через `./df dotnet <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| сайт learn.microsoft.com/dotnet (dotnet/docs) | `docfx` (нові поля `tilde_root`, `snippet_prefix`) |
| довідник API dotnet/dotnet-api-docs (ECMA XML) | `ecma-xml` (новий) |
| довідник API з XML-документації пакетів NuGet | `nuget-xmldoc` |
| releases-index.json і releases.json dotnet/core | `dotnet-releases` (новий) |
| нотатки випусків, стандарт і специфікації C#, Roslyn, VB, runtime, sdk | `ghdocs` (дерево однієї теки, пробіли й «#» в іменах), `mdfile` |

Ліцензії джерел: документація dotnet/docs і dotnet/dotnet-api-docs — CC BY 4.0 (приклади коду — MIT); dotnet/core,
dotnet/runtime, dotnet/sdk, dotnet/roslyn, dotnet/csharplang, dotnet/vblang — MIT; dotnet/csharpstandard — CC BY 4.0
(текст) і MIT (код); пакети NuGet — під ліцензіями їхніх авторів. Корпус у git не потрапляє (див. нижче).

Що нового в коді фабрики для dotnet:

- **Читач `ecma-xml`** — джерело довідника API сайту: документ на тип (простір імен, збірки, підпис C#, базовий тип,
  опис, «Applies to» з `xml/FrameworksIndex`, зауваження з підрозділами, приклади C# з `snippets/`) і розділ на кожен
  член з тим самим заголовком, що дає `nuget-xmldoc` («GetAsync(String) method»). Ім'я документа теж те саме, тож
  опис типу з dotnet-api-docs і з XML пакетів однієї лінії — одна родина `api` і одне місце у видачі. Версії документа —
  номери .NET і Windows Desktop з монікерів (8.0–10.0); типи й члени лише прев'ю 11.0 (`skip_monikers`) не беруться.
  Приклади VB, F# і C++ не вставляються — інакше той самий приклад лягав би у фрагменти чотири рази.
- **Читач `dotnet-releases`** — огляд ліній, документ на лінію (тип LTS/STS словами, фаза, кінець підтримки, таблиця
  всіх стабільних випусків) і документ на випуск (дата, CVE, runtime, SDK з версіями C#, F#, VB і Visual Studio,
  ASP.NET Core з модулем IIS, Windows Desktop). Фаза й кінець підтримки — лише в документі лінії: повторені в кожному
  випуску, вони забирали всю видачу на «end of support».
- **`docfx`**: `tilde_root` — тека, від якої рахується «~/» (у dotnet/docs docfx.json лежить у корені, і
  «~/includes/…» веде в корінь, а не в docs/); `snippet_prefix: "Snippet"` — dotnet/docs пише `:::code … id="Assignment"`,
  а в коді позначає фрагмент `// <SnippetAssignment>`. Без полів читач поводиться як раніше.
- **`ghdocs`**: адреса `…/git/trees/ТЕГ:ТЕКА` — дерево однієї теки (повні дерева dotnet/runtime і dotnet/roslyn
  GitHub обрізає); пробіл і «#» в імені файла («Compiler Breaking Changes - DotNet 9.md», «Getting-Started-C#-…»)
  кодуються в адресі.

Особливості:

- **Версії сайту — знімки репозиторію.** dotnet/docs монікерів не має: редакція версії — останній коміт `main` (за
  першим батьком) за тиждень після виходу x.y.0 (дати — з releases.json dotnet/core): 1.0 — 04.07.2016 (тоді сайт мав
  лише 126 сторінок .NET Core), 1.1 — 23.11.2016, 2.0 — 21.08.2017, … 10.0 — 18.11.2025. Для 9.0 узято справжню дату
  виходу 12.11.2024: releases.json лінії замінив запис 9.0.0 грудневим (3.12.2024, SDK 9.0.101). Посилання знімків
  ведуть на файли коміту в GitHub, чинної гілки — на learn.microsoft.com; чинна гілка несе версію 10.0. Сторінки прев'ю
  .NET 11 і C# 15 (що нового, критичні зміни 11) не беруться.
- **Приклади коду старих знімків.** До листопада 2020 року приклади жили в окремому репозиторії dotnet/samples
  (залежний репозиторій збирання сайту): у знімках 1.0–3.1 приклади, на які сторінки посилаються як
  `../../samples/snippets/…`, не вставлено. Так само не вставлено приклади із залежних репозиторіїв чинного сайту
  (`~/../azure-dev-docs/…`, `_roslyn/…`) — це кільканадцять сторінок.
- **Стандарт і специфікації C#.** Те, що сайт показує як «C# language specification»
  (learn.microsoft.com/dotnet/csharp/language-reference/language-specification/…), — текст dotnet/csharpstandard;
  «Feature specifications» (…/language-reference/proposals/…) — dotnet/csharplang `proposals/csharp-X.Y`; критичні
  зміни компілятора (…/csharp/whats-new/breaking-changes/…) — dotnet/roslyn `docs/compilers/CSharp`. Тут вони взяті з
  репозиторіїв, з посиланнями на GitHub: стандарт — гілки `standard-v5`, `standard-v6`, `standard-v7` (опубліковані
  видання ECMA-334) і `draft-v8`, `draft-v9` (чернетки комітету); стара специфікація C# 6 — тека `spec/` csharplang;
  специфікації можливостей — лише випущені версії 7.0–14.0, без нотаток зустрічей LDM і нереалізованих пропозицій.
  Номери розділів стандарту між виданнями зсуваються, тож однаковий текст різних видань зливається лише там, де номер
  розділу той самий.
- **Мітки версій** (`version_line_depth: 2`). .NET — голий номер: сайт і довідник API — лінія (`8.0`), випуски й
  нотатки — повний номер (`8.0.5`). Пакети dotnet/extensions (Http.Resilience, Compliance, Telemetry, AI…) виходять
  щомісячними мінорними — `8.1` … `10.11`. Пакети Microsoft.Extensions.* з власною нумерацією несуть назву:
  `azure-1.14`, `configuration-azureappconfiguration-8.6`, `logging-applicationinsights-2.23`, `ml-5.0`,
  `caching-cosmos-1.8`, `caching-postgres-1.2`, `configuration-dockersecrets-unofficial-1.1`. C# — з міткою `csharp-`:
  видання стандарту `csharp-5` … `csharp-9`, специфікація C# 6 — `csharp-6`, специфікації можливостей `csharp-7.0` …
  `csharp-14.0`; `csharp-12` знаходить увесь C# 12. Документація runtime, sdk, Roslyn і специфікація VB — без версії.
- **Довідник API з пакетів** — лише пакети, що несуть XML: Microsoft.NETCore.App 2.0–2.2 і Microsoft.NETCore.App.Ref
  3.0–10.0 (останній патч лінії; у 1.0 і 1.1 XML немає) і всі 123 ідентифікатори з префіксом Microsoft.Extensions —
  зокрема сторонні (Jakeuj, Log4Net.AspNetCore, Slack, Splunk, DockerSecrets.Unofficial…), — кожна стабільна мінорна
  лінія, останній патч; 20 ідентифікаторів XML не несуть зовсім (інструменти, тести специфікації, аналізатори) і не
  дають нічого. Простори імен `.Internal` і класи рядків ресурсів не беруться.
- **Запити `quality`** записано так, як їх ставить людина своїми словами. Цілі доповнено справжніми відповідями, яких не
  було в першій чернетці: метрика `http.client.request.duration` у редакції 8.0 (тоді розділ звався «Instrument»),
  сторінка single-file під давнім іменем (`core/deploying/single-file`), розділ «Object Initializers with the required
  modifier», документи дизайну runtime про багаторівневу компіляцію.

## Межі, про які треба пам'ятати

- Усе англійською. Переклади сайту не взято.
- Лише стабільні випуски: .NET 11 (прев'ю і RC), C# 15, preview і rc ліній 1.0–10.0 не взято.
- Не взято код і тести dotnet/runtime, docs-desktop (WinForms, WPF), docs-maui, Aspire; ASP.NET Core і Entity
  Framework — у своїх примірниках.
- Довідник API з XML пакетів не перелічує успадкованих членів; прикладів у ньому немає — вони в dotnet-api-docs.
- «Applies to» dotnet-api-docs — те, що несе `xml/FrameworksIndex` сьогодні: .NET 8–10, .NET Framework 4.6.2–4.8.1 і
  .NET Standard 2.0–2.1 лише для пакетів, Windows Desktop 3.0–10.0. Старші лінії .NET дає довідник із пакетів.

## Корпус лише локально

Корпус, кеш фрагментів і сховище сирого **у git не потрапляють** (`corpus/` і `index/` у `.gitignore` цієї теки,
`raw/` — у кореневому): паспорт `corpus/index.json` на 274 тисячі документів важить 156 МБ, кеш фрагментів — 637 МБ
(стиснений — понад 100 МБ), а GitHub відхиляє файли від 100 МіБ. Користувач вирішив 19.10.2026 тримати їх лише на
цій машині, як корпуси `patterns` і `frontend-architecture`. У git — лише налаштування примірника; `refresh` (і засів
з клонів, див. «Оновлення») відтворює корпус з `sources.json`.

**Резервна копія** — архів на диску Windows, поза WSL: `C:\Distr\dotnet-corpus-2026-10-19.tar.gz` (з WSL —
`/mnt/c/Distr/dotnet-corpus-2026-10-19.tar.gz`), усередині теки `corpus/` (тексти й паспорт) і `raw/` (сховище
сирого). Архів звірено з диском файл за файлом. Тексти лишаються й на диску: сервер, `refresh` і `build` працюють з
ними як завжди.

**Відновлення**, якщо корпусу немає, — з кореня `docfactory/`:

```
tar -xzf /mnt/c/Distr/dotnet-corpus-2026-10-19.tar.gz -C instances/dotnet
./df dotnet smoke
```

Кеш фрагментів (`index/`) збереться з корпусу сам при першому старті сервера (близько хвилини); вектори лежать у
Qdrant, а якщо їх там немає — `./df dotnet vectors` (12 хвилин на відеокарті).

**Оновлення.** Новий патч: у джерелі `api-<лінія>` — номер пакета Microsoft.NETCore.App.Ref (адреса nupkg і
`within`); лінії Microsoft.Extensions.* — у джерелах `ext-*` (генератор джерел лежав у scratchpad сесії збирання:
нова лінія пакета додається руками за зразком сусідньої). Новий мажор: `site-11-0` (коміт `main` dotnet/docs за
тиждень після виходу), `api-11-0`, `notes-11-0`, лінія `11.0` у `lines` джерела `releases`, нові
`csharp-proposals-15-0` і `roslyn-breaking-*-11`; усе — у `families`; правила `dotnet-11`, `csharp-15`, `/11/` в
`exclude` знімків і `skip_monikers` в `api-docs` прибрати. Сайт, dotnet-api-docs і dotnet/core тягнути не мережею, а
голим клоном: `tools/seed_git_store.py --instance dotnet --clone dotnet/docs=<клон>` для знімків сайту, далі
`./df dotnet build <джерела>`; решта — `./df dotnet refresh <джерела>`. Далі `manifest`, `vectors`, `smoke`, `quality`
і новий архів на `C:\Distr` (старий — видалити після звірки нового).

## Установка venv

```
cd instances/dotnet
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt     # ~2,6 ГБ: onnxruntime-gpu і колеса CUDA
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

Без відеокарти `onnxruntime-gpu` рахує на процесорі тими самими числами; тоді `vectors` іде добу, а не хвилини.

## Збирання корпусу

```
./df dotnet sources --why   # перелік джерел і білий список
./df dotnet refresh         # завантажити все задеклароване (сайт — краще з клону, див. «Оновлення»)
./df dotnet manifest        # паспорт
./df dotnet setup           # Qdrant чи пошук лише по словах
./df dotnet vectors         # залити корпус у docs-dotnet (12 хвилин на відеокарті)
./df dotnet smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df dotnet serve          # порт 8866
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8866/mcp`. Індекс по словах на 562
тисячах фрагментів з кешу збирається близько хвилини, і сервер тримає в пам'яті близько 7 ГБ — найбільше з усіх
примірників. Якщо порт зайнятий, сервер скаже про це й вийде: значить, `serve` цього примірника вже десь запущений; хто
тримає порт, покаже `ss -ltnp | grep 8866`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user dotnet-docs http://127.0.0.1:8866/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож ту саму команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Можна й через `.mcp.json` цієї теки.

**3. Перевірити.** `/mcp` — має бути `dotnet-docs` і два інструменти `search_docs`, `read_section`. Якщо `/mcp`
показує `failed`, сервер не запущено або запущено з іншим портом.

Зупинка — Ctrl+C у терміналі сервера.
