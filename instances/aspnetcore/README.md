# aspnetcore — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про ASP.NET Core і класичний ASP.NET — від хоста, middleware,
маршрутизації й Kestrel до Blazor, SignalR, автентифікації, тестування, розгортання й переходу з ASP.NET 4.x.
Документація англійською, усі стабільні мажорні й мінорні версії: сайт learn.microsoft.com/aspnet/core кожної
редакції 1.0–10.0 і сайт класичного ASP.NET; довідник API кожної лінії ASP.NET Core 1.0–10.0, класичних MVC, Web API,
Web Pages, SignalR, Identity, Katana і System.Web; версії, залежності й README пакетів NuGet і npm; markdown
репозиторію dotnet/aspnetcore, різниці API між версіями й нотатки релізів. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

Одна одиниця на всю лінію ASP.NET: звернувшись до неї з версією, дістаєш усе, що потрібно для документації й
впровадження продукту саме на цій версії, — сторінку посібника тієї редакції, тип і член API того випуску, пакет NuGet
з його залежностями, різницю API з попередньою версією. Класичний ASP.NET (Web Forms, MVC 5, Web API 2, Web Pages,
SignalR 2, Identity, OWIN/Katana, System.Web) тут таки: проєкти на ньому живі, і перехід з нього на ASP.NET Core
описано обома сторонами. Бібліотеки Microsoft.Extensions.* (DI, конфігурація, журнали, хост) як окремий довідник не
взято — вони спільні для всього .NET і чекають на свій примірник; їхнє застосування в ASP.NET Core описують сторінки
сайту.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Сайт ASP.NET Core, 13 редакцій 1.0–10.0 | 6 987 | 25 633 | dotnet/AspNetCore.Docs |
| Сайт класичного ASP.NET | 1 537 | 17 590 | dotnet/AspNetDocs |
| API ASP.NET Core, 15 ліній 1.0–10.0 | 32 287 | 29 937 | XML-документація пакетів NuGet |
| API Microsoft.AspNetCore.OData 9.5 | 413 | 2 548 | те саме |
| API класичних MVC, Web API, Web Pages, SignalR, Identity, Katana — кожна мінорна лінія | 7 839 | 13 096 | те саме |
| API інших класичних пакетів (OData, WebHooks, OutputCache, SessionState, Web.Optimization…) | 1 057 | 6 272 | те саме |
| API System.Web (.NET Framework 4.8.1) | 2 253 | 22 179 | Microsoft.NETFramework.ReferenceAssemblies.net481 |
| NuGet: версії, залежності й README 169 пакетів ASP.NET Core | 1 407 | 4 039 | реєстр NuGet |
| NuGet: те саме для 114 класичних пакетів | 586 | 1 505 | реєстр NuGet |
| npm: версії й README п'яти пакетів | 51 | 139 | реєстр npm |
| Різниці API 3.0–10.0 (api-diff) | 504 | 510 | dotnet/core |
| Нотатки релізів .NET 9 і 10 про ASP.NET Core | 20 | 230 | dotnet/core |
| Markdown dotnet/aspnetcore (`docs/`, `src/`), теги 2.1.33–10.0.13 | 961 | 2 057 | GitHub |
| Релізи dotnet/aspnetcore | 214 | 367 | GitHub Releases |
| Релізи AspNetWebStack, Katana, SignalR 2 | 37 | 92 | GitHub Releases |

Разом 56 153 документи, 126 194 фрагменти (`expected_passages` у `checks.json`). 37 242 документи власних фрагментів
не дали: кожен їхній розділ дослівно є в іншій редакції, і той фрагмент лише дістав їхні версії — так опис
`HttpContext.Request`, однаковий у чотирнадцяти лініях API, у пошуку один. Корпус завантажувався 3 години 36 хвилин,
вектори рахувалися 3 години 4 хвилини (11,4 фрагмента за секунду). Замір `quality` (10 запитів): по словах 9, за
змістом 8, разом 10. `max_per_doc` і `fusion_depth` не ставились.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (148 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену, родини джерел-версій (`families`).
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df aspnetcore <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| сайти ASP.NET Core і класичного ASP.NET | `docfx` — новий |
| довідник API з XML-документації пакетів NuGet | `nuget-xmldoc` — новий |
| версії, залежності й README пакетів NuGet | `nuget-package` — новий |
| markdown dotnet/aspnetcore, api-diff і нотатки релізів dotnet/core | `ghdocs` (нові поля `files`, `exclude`, `title_from`) |
| релізи GitHub | `ghreleases` |
| npm: версії й README | `npm-versions`, `npm-tarball-files` |

Новий код для aspnetcore — три читачі:

- **`docfx`** читає джерело сайту Learn так, як його збирає DocFX: дерево гілки чи коміту, front matter кожної
  статті (`monikerRange` відкидає сторінки, яких у редакції немає), блоки `:::moniker range`, вставки
  `[!INCLUDE]`, приклади коду `[!code-csharp]` і `:::code` (за тегом `<snippet>`, `#region` чи діапазоном рядків),
  зокрема із сусідніх репозиторіїв (`~/../AspNetCore.Docs.Samples`, blazor-samples, maui-samples), посилання
  `xref:` — назвою статті чи типу, вкладки й зони `:::zone pivot` — підзаголовками. Сам сайт показує сторінку
  лише після JavaScript і лише для редакцій 3.1–10.0, а джерело дає кожну редакцію одним проходом по одному дереву.
  Редакції 1.0–2.2 взято з коміту `6fa2d33` (19.09.2019), 3.0 — з `998d59e` (07.11.2020): пізніше їхні монікери
  з джерела прибрано. Посилання редакцій 3.1–10.0 ведуть на learn.microsoft.com з `?view=aspnetcore-X`, старіших —
  на файл того коміту в GitHub.
- **`nuget-xmldoc`** будує довідник API з XML-документації, яку пакет NuGet несе поруч зі збіркою (`ref/` має
  перевагу над `lib/`, з цільових платформ — найновіша). Документ на тип, розділ на член: сигнатура, параметри, що
  повертає, винятки, зауваги, приклад. Той самий XML лежить в основі довідника learn.microsoft.com/dotnet/api, а
  пакет кожного випуску дає точний стан саме того випуску; посилання ведуть на learn.microsoft.com з `?view=`.
  Лінії 3.0–10.0 — з `Microsoft.AspNetCore.App.Ref` і окремих пакетів поза спільним фреймворком, 1.0–2.3 і 3.2
  (Blazor WebAssembly) — з окремих пакетів `Microsoft.AspNetCore.*`, System.Web — з еталонних збірок .NET Framework
  4.8.1. Поле `exclude_types` прибирає внутрішні простори імен (`.Internal`) і класи ресурсів (`Resources`,
  `CoreStrings`): у шумних лініях вони давали тисячі фрагментів без змісту.
- **`nuget-package`** бере реєстр NuGet (`registration5-semver1`) і дає на пакет огляд з усіма стабільними версіями
  й датами, документ на кожну мінорну лінію (версії, платформи й залежності найновішої версії, зміни опису) і README
  найновішої версії кожної лінії; однакові README — один документ з усіма версіями.

Особливості:

- **Мітки версій.** ASP.NET Core — голий номер: сторінки сайту й довідник API — лінія (`10.0`), репозиторій,
  релізи й пакети NuGet — повний номер (`10.0.13`); лінії мінорні (`version_line_depth: 2`). Класичний ASP.NET
  нумерує кожен продукт окремо, тож версія несе назву продукту: `mvc-5.2` у довіднику API і `mvc-5.2.9` у пакеті
  NuGet, так само `webapi-5.3`, `webpages-3.3`, `signalr-2.4`, `identity-2.2`, `katana-4.2`, `netfx-4.8.1`
  (System.Web), `webstack-3.3.0` (релізи AspNetWebStack), `aspnet-…` (інші класичні пакети). Так само позначено
  пакети з власною нумерацією поруч з ASP.NET Core: `odata-9.5.0`,
  `systemwebadapters-2.3.0`, `datasync-6.1.0`, `extensions-10.11.0` (`Microsoft.AspNetCore.Diagnostics.Middleware`
  та інші з dotnet/extensions). Сторінки сайту класичного ASP.NET версій не мають — їх шукають без версії.
- **SignalR у лініях 2.1–2.3** має власні номери 1.0–1.2; пакети SignalR і `Http.Connections` узято за лінією
  продукту.
- **Родини** (`families` у `config.json`) зводять редакції сайту, лінії API і теги репозиторію: однаковий текст
  різних редакцій — один фрагмент з переліком версій.
- **Пакети без XML-документації** (Cors, FriendlyUrls, DynamicData.EFProvider, ScriptManager, Providers.LocalDb та
  інші) довідника API не мають — лише версії й залежності з реєстру. MVC 3.0 і Web Pages 1.0 у NuGet несуть збірки
  без XML, тож довідник класичного MVC починається з 4.0, Web Pages — з 2.0.
- **Запити `quality`** записано так, як їх ставить людина своїми словами. Двом запитам додано справжні відповіді,
  яких не було в першій чернетці цілей: про `HttpContext.RequestAborted` — розділ «RequestAborted» сторінки «Use
  HttpContext» (усі способи ставлять його першим, і пояснює він більше за опис властивості в довіднику API); про
  виклик методів клієнта з хаба SignalR 2 — розділ «SignalR Hubs in the ChatHub.cs» підручника SignalR 2. Посібник
  хабів SignalR 1.x майже дослівно повторює посібник 2.x, а його назва несе «SignalR 1.x», тож на питання про
  SignalR 2 він виходить вище за посібник 2.x.

## Межі, про які треба пам'ятати

- Усе англійською. Переклади сайту не взято.
- Лише стабільні випуски: preview і rc не взято. Винятки: нотатки релізів .NET 9 і 10 — з усіма preview і rc, бо
  саме в них описано нове кожного випуску; таблиці версій npm перелічують і передрелізи.
- Microsoft.Extensions.*, Entity Framework Core, Azure і IIS як окремі довідники не взято — лише те, що про них
  каже сайт ASP.NET Core.
- Приклади коду — ті, що сторінки вставляють; повні проєкти прикладів не взято.
- Довідник API з XML не перелічує успадкованих членів і не має прикладів, яких немає в самому XML.
- Сторінка класичного Identity «two-factor authentication using SMS and email» у джерелі порожня (один байт).

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/aspnetcore-corpus-2026-10-18.tar.gz` (366 МБ: 56 153 тексти,
паспорт і сховище сирого `raw/`; перед видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише
на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/aspnetcore-corpus-РРРР-ММ-ДД.tar.gz -C instances/aspnetcore corpus raw
find instances/aspnetcore/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/aspnetcore/raw
gzip -9 -c instances/aspnetcore/index/passages.json > instances/aspnetcore/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/aspnetcore-corpus-2026-10-18.tar.gz -C instances/aspnetcore
./df aspnetcore smoke
```

**Оновлення.** Новий патч-випуск ASP.NET Core: у джерелах `api-<лінія>` перенести номер пакетів (`/10.0.13` →
`/10.0.14`, разом з адресою nupkg і `within`), у `repo-<лінія>` — тег. Новий мажор: додати `site-11-0` (монікер
`aspnetcore-11.0`), `api-11-0`, `repo-11-0`, `api-diff-11-0`, `notes-11-0` і вписати їх у `families`. Сайт на
`main`, реєстри NuGet і npm, релізи підхоплюються самі. Далі `./df aspnetcore refresh`, `manifest`, `vectors`,
`smoke`, `quality`. `refresh` з наявним сховищем сирого питає лише змінене; `build` перерендерює корпус без мережі.

## Установка venv

```
cd instances/aspnetcore
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df aspnetcore sources --why   # перелік джерел і білий список
./df aspnetcore refresh         # завантажити все задеклароване (близько 3,5 години)
./df aspnetcore manifest        # оновити паспорт
./df aspnetcore setup           # Qdrant чи пошук лише по словах
./df aspnetcore vectors         # залити корпус у docs-aspnetcore (близько 3 годин)
./df aspnetcore smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df aspnetcore serve          # порт 8862
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8862/mcp`. Якщо порт зайнятий,
сервер скаже про це й вийде: значить, `serve` цього примірника вже десь запущений; хто тримає порт, покаже
`ss -ltnp | grep 8862`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user aspnetcore-docs http://127.0.0.1:8862/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `aspnetcore-docs` і два інструменти `search_docs`, `read_section`. Якщо
`/mcp` показує `failed`, сервер не запущено або запущено з іншим портом.

Зупинка — Ctrl+C у терміналі сервера.
