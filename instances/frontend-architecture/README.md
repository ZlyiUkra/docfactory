# frontend-architecture — примірник фабрики docfactory

Тридцятий примірник фабрики: захищений MCP-сервер, що допомагає обрати й застосувати архітектуру фронтенд-проєкту.
Тут методологія Feature-Sliced Design (документація, блог її авторів, лінтер Steiger), Bulletproof React, Flux, книга
Atomic Design, мікрофронтенди і першоджерела архітектурних стилів: шарова архітектура, MVC і MVP, порти й адаптери
(гексагональна), цибулева, чиста, вертикальні зрізи, острови, DDD. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо

Бібліотеки відповідають на питання «як зробити», архітектура — «де це має лежати і що від чого залежить». Ці
відповіді розкидані по статтях різних авторів і років, і кожен підхід розв'язує свою задачу: FSD ділить фронтенд на
шари й слайси з правилами імпортів, Bulletproof React — групує код за фічами, порти й адаптери та чиста архітектура
відгороджують предметну область від фреймворку й мережі, мікрофронтенди ділять застосунок між командами, острови —
сторінку між статикою та інтерактивом. Тут вони разом, щоб порівнювати їх за критеріями самих джерел — розмір і
кількість команд, зв'язність фіч, повторне використання, складність домену, тестованість — і бачити, хто що сказав.

Патерни коду (Strategy, Observer, патерни React) — у сусідньому примірнику `patterns`; тут — рівень вище, будова
проєкту.

## Корпус лише локально

Статті блогів, книга Atomic Design і сторінки martinfowler.com не мають вільної ліцензії. Тому, як у примірнику
`patterns`, **корпус і індекс у git не потрапляють** (`corpus/` та `index/` у `.gitignore`): у git лежать лише
налаштування примірника, а `refresh` відтворює корпус з нуля за кілька хвилин. З тієї ж причини промпт велить
переказувати своїми словами, цитувати коротко й давати адресу сторінки.

## Скільки цього

| Шар | Документів | Звідки |
|-----|-----------:|--------|
| Feature-Sliced Design: огляд, туторіал, довідник шарів, слайсів, сегментів і публічного API, гайди, міграції, розділ «About», CHANGELOG | 38 | feature-sliced/documentation, гілка main (сайт fsd.how) |
| Блог feature-sliced.design: архітектурні підходи до фронтенду | 97 | sitemap.xml сайту |
| Steiger: README, приклади конфігу, міграція, кожне правило плагіна FSD | 27 | feature-sliced/steiger, гілка master |
| Bulletproof React: структура за фічами, шар API, стан, тести, безпека | 13 | alan2207/bulletproof-react, гілка master |
| Flux: огляд, Dispatcher, Flux Utils | 6 | facebookarchive/flux, гілка main |
| micro-frontends.org | 1 | neuland/micro-frontends, гілка master |
| Atomic Design, Брад Фрост: п'ять розділів книги | 5 | atomicdesign.bradfrost.com |
| Martin Fowler: GUI Architectures, Presentation Domain Data Layering, Modularizing React Applications, Micro Frontends, Domain Driven Design, Bounded Context | 6 | martinfowler.com |
| Alistair Cockburn: Hexagonal Architecture (2005) | 1 | alistair.cockburn.us |
| Robert C. Martin: The Clean Architecture, Screaming Architecture | 2 | blog.cleancoder.com |
| Jeffrey Palermo: The Onion Architecture, частини 1–4 | 4 | jeffreypalermo.com |
| Herberto Graça: The Software Architecture Chronicles | 20 | herbertograca.com |
| Alexander Bespoyasov: Clean Architecture on Frontend | 1 | bespoyasov.me |
| Jimmy Bogard: Vertical Slice Architecture | 1 | jimmybogard.com |
| Jason Miller: Islands Architecture | 1 | jasonformat.com |

Разом 223 документи; фрагментів в індексі — 4 687 (`expected_passages` у `checks.json`). Фрагменти — це шматки
документів між заголовками, по яких іде пошук. Версій тут немає: кожне джерело взято в одному, поточному вигляді.

Замір `quality` на першому корпусі: перша десятка (питання своїми словами) — по словах 4 із 10, за змістом 6, разом 5;
друга, «як модель» (назви з джерел: «ports and adapters hexagonal architecture», «dependency rule clean architecture»),
— 9 із 10. Промах другої десятки — «feature-sliced design layers»: на нього відповідають статті блогу FSD, де шари
пояснено своїми словами, а довідник `Layers` з документації опускається нижче п'ятірки. Відповідь із таких уривків
правильна, але для точного правила імпортів між шарами варто прочитати сам довідник.

## Що в цій теці

- `corpus/` — тексти й паспорт `index.json`. Лише локально, див. вище.
- `index/` — кеш фрагментів. Лише локально.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — ключ Anthropic (лише для кроку `ask`) і токен GitHub (лише для завантаження); `.mcp.json` — запис
  HTTP-сервера для Claude Code.
- `.venv/` — власний venv примірника; `requirements.txt` — його склад.

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через
`./df frontend-architecture <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| FSD, Steiger, Bulletproof React, Flux, micro-frontends.org | markdown із репозиторіїв GitHub | `ghdocs-history` |
| блог feature-sliced.design | сторінки з sitemap.xml, текст — від заголовка до кінця статті | `sitemap-html` |
| статті й книга | явний перелік сторінок кожного сайту | `html-list` |

Білий список — хости кожного сайту з таблиці вище, `api.github.com` і `raw.githubusercontent.com`. Сайт fsd.how не
читається: він збирається з репозиторію feature-sliced/documentation. Посилання у відповідях можуть вести на fsd.how.

Особливості, які варто знати:

- **Хто що написав.** Блог feature-sliced.design пишуть автори FSD; його порівняння FSD з іншими підходами — їхній
  погляд, і промпт велить так його й подавати. Стилі визначено там, де їх уперше описали: порти й адаптери —
  Кокберн, чиста — Мартін, цибулева — Палермо, вертикальні зрізи — Богард, острови — Міллер; Граса й Беспоясов
  пояснюють і поєднують їх.
- **Переклади FSD** (російською, корейською, в'єтнамською та іншими) не взято: лише англійська.
- **Назви з джерелом.** Документи FSD, Steiger, Bulletproof React і Flux дістають назву з префіксом джерела полем
  `title_prefix`: «FSD: Layers», «Steiger rule: no-cross-imports».
- **Залишки сторінок.** У текстах статей подекуди лишилися підпис автора, «Edit this page» чи «Related» — пошуку це не
  заважає.

## Межі, про які треба пам'ятати

Тут немає патернів коду (примірник `patterns`), документації фреймворків і бібліотек (React, Next.js, Astro, Redux
та інші — власні примірники) і бекенд-архітектури поза тим, що пояснюють самі статті. Книг «Clean Architecture» і
«Domain-Driven Design» тут немає: є статті їхніх авторів і пояснення інших.

## Установка venv

```
cd instances/frontend-architecture
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df frontend-architecture sources --why   # перелік джерел і білий список
./df frontend-architecture refresh         # завантажити все задеклароване (~5 хвилин)
./df frontend-architecture manifest        # оновити паспорт
./df frontend-architecture setup           # Qdrant чи пошук лише по словах
./df frontend-architecture vectors         # залити корпус у docs-frontend-architecture (~8 хвилин)
./df frontend-architecture smoke           # перевірки
```

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df frontend-architecture serve           # порт 8790
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8790/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user frontend-architecture-docs http://127.0.0.1:8790/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `frontend-architecture-docs` і два інструменти `search_docs`, `read_section`.
Якщо сесію Claude Code відкрито раніше, ніж піднято сервер, вона покаже його як недоступний: у `/mcp` виберіть сервер
і «Reconnect».

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).

## На іншій машині

На іншій машині (теж WSL) бракує venv примірника, корпусу й векторів у Qdrant — їх немає в git:

1. venv — за розділом «Установка venv» вище;
2. корпус і пошук — за розділом «Збирання корпусу»;
3. `./df frontend-architecture smoke`, `./df frontend-architecture serve` і кроки 2–3 розділу «Сервер під Claude
   Code».
