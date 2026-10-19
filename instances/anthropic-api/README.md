# anthropic-api — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про API Anthropic — виклик моделей Claude (Haiku, Sonnet, Opus, Fable)
через Messages API та офіційні SDK. Документація — сайт platform.claude.com/docs цілком англійською (моделі й ціни,
ліміти, помилки, Messages API, потокова видача, thinking і effort, виклик інструментів, кешування промпту, пакетна
обробка, файли, структуровані відповіді, Managed Agents, Admin API, хмарні платформи, журнали змін і системні
промпти, HTTP-довідник API) разом із довідником API в редакціях Python і TypeScript; для кожного стабільного випуску
SDK TypeScript, Python, Go, Ruby, C# і CLI `ant` — README, `api.md`, helpers і MIGRATION з репозиторію та нотатки
релізів; код і приклади найновіших SDK TypeScript і Python; таблиці версій і README з npm і PyPI; рецепти
claude-cookbooks. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі
дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Примірник зібрано, щоб підключати Haiku: перемикати моделі, рахувати ціну й ліміти, переходити між версіями SDK
за документацією, а не з пам'яті. Тому шість із десяти питань заміру — про моделі й Haiku: ідентифікатор і вікно
контексту Haiku 5.5, ціна довгого промпту, перехід з Haiku 4.5, рекомендований effort, дата виходу з ужитку
Haiku 3.5, мінімальна довжина кешу. Моделі, ціни й ліміти міняються щомісяця, а SDK виходять щотижня: TypeScript SDK
дійшов до 0.135, Python — до 1.15. Сайт показує лише поточний стан, а в проєктах живуть різні версії SDK — тут кожен
випуск має свою редакцію README й `api.md`, свої нотатки релізу і рядок у таблиці версій npm чи PyPI.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Сайт: посібники, моделі, ціни, ліміти, журнали змін | 278 | 7 823 | llms.txt, markdown-двійники сторінок |
| Сайт: HTTP-довідник API | 505 | 26 568 | те саме |
| Довідник API в редакції Python SDK | 414 | 18 544 | зміст `/docs/en/api/python.md` |
| Довідник API в редакції TypeScript SDK | 416 | 18 884 | зміст `/docs/en/api/typescript.md` |
| TypeScript SDK: README, `api.md`, helpers, MIGRATION | 189 | 693 | 227 стабільних тегів v0.2.1–sdk-v0.135.0 |
| Python SDK: README, `api.md`, helpers, tools, MIGRATION | 197 | 662 | 237 тегів v0.2.1–v1.15.0 |
| Go SDK: README, `api.md`, tools | 178 | 515 | 102 теги v1.0.0–v1.82.0 |
| Ruby SDK: README, helpers | 111 | 256 | 96 тегів v1.0.0–v1.80.0 |
| C# SDK: README | 14 | 55 | 79 тегів v0.1.0–Anthropic-v12.58.0 |
| CLI `ant`: README | 12 | 44 | 56 тегів v1.0.0–v1.42.0 |
| Нотатки релізів (13 джерел) | 999 | 3 795 | GitHub Releases, лише стабільні |
| Код TypeScript SDK (`src/`) і Python SDK (`src/anthropic/`) | 2 598 | 10 755 | теги sdk-v0.135.0 і v1.15.0 |
| Приклади TypeScript і Python (`examples/`) | 64 | 166 | ті самі теги |
| npm: таблиці версій і README шести пакетів | 100 | 515 | реєстр npm |
| PyPI: таблиця версій і опис `anthropic` | 69 | 356 | PyPI |
| claude-cookbooks: зошити й сторінки | 172 | 2 773 | гілка main, знімок a162e01 |

Разом 6 316 документів, 92 404 фрагменти (`expected_passages` у `checks.json`). Дві третини фрагментів — довідник
API: кожна сторінка ендпоінта повністю розгортає вкладені типи (`messages/create` — 140 КБ), а редакції Python і
TypeScript повторюють описи параметрів зі своїм синтаксисом. Вектори для всього корпусу рахувалися 3 години 6 хвилин.
Замір `quality` (10 запитів): по словах 9, за змістом 8, разом 10. `max_per_doc` і `fusion_depth` не ставились: 10 з
10 і без них.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (39 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df anthropic-api <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| сайт platform.claude.com/docs | `llms` (перелік llms.txt, кожна сторінка — її `.md`) |
| довідник API в редакціях Python і TypeScript | `md-index` — новий |
| сторінки репозиторіїв SDK, README `aws-sdk` у монорепозиторії | `ghdocs-history` |
| нотатки релізів | `ghreleases-stable` |
| код і приклади TypeScript SDK | `ghcode-history-ts` |
| код і приклади Python SDK | `ghcode-history`, `outline: ["python"]` |
| npm: таблиця версій і README | `npm-versions`, `npm-tarball-files` |
| PyPI: таблиця версій і опис | `pypi-versions` |
| claude-cookbooks | `ghdocs-history-ipynb` — новий |

Новий код для anthropic-api — два тонкі читачі:

- **`md-index`** бере сторінки зі змісту в markdown. Довідник API кожної мови SDK (`/docs/en/api/python/…`) не
  потрапляє ні в llms.txt, ні в sitemap.xml; є лише сторінка-зміст мови, де пункти вкладені, а заголовки теж
  посилання від кореня сайту. Читач `llms` бере або абсолютні адреси, або відносні пункти верхнього рівня, тож ці
  пропустив би. Текст сторінки готує той самий розбір, що й у `llms`; назва документа — «Python SDK: Create a
  Message».
- **`ghdocs-history-ipynb`** — `ghdocs-history`, у якому зошит Jupyter перед розбором стає markdown-ом: клітинки
  markdown як є, код блоками мови зошита, з виводу лише текст, обрізаний до 1 500 знаків. Картинки base64 і HTML
  виводу відкидаються: із 22 МБ зошитів у корпус лягає 2,6 МБ тексту.

Особливості:

- **Мітки версій.** Кожна SDK має власну нумерацію, тож версія несе назву SDK: `typescript-0.135.0`
  (`@anthropic-ai/sdk`), `python-1.15.0`, `go-1.82.0`, `ruby-1.80.0`, `csharp-12.58.0`, `cli-1.42.0`, обгортки —
  `bedrock-sdk-0.35.0`, `vertex-sdk-0.21.0`, `foundry-sdk-0.6.0`, `aws-sdk-0.8.0`, `google-cloud-sdk-0.1.0`. Лінії
  мінорні (`version_line_depth: 2`): `typescript-0.135`, `python-1.15`. Сторінки сайту й cookbooks версій не мають.
- **Теги TypeScript SDK двох епох.** До монорепозиторію теги основного пакета мали вигляд `v0.x.y` (0.2.1–0.12.3),
  далі — `sdk-v0.x.y`. Перші йдуть у те саме джерело сторінок і в окреме джерело релізів з префіксом `v0.`: голий
  `v` зачепив би теги `vertex-sdk-v…`.
- **Теги C# SDK двох епох.** Основний пакет мав теги `v0.1.0`–`v11.0.0`, з 12.0.0 — `Anthropic-v…`; обидві серії в
  одному джерелі сторінок, релізи — двома джерелами. Обгортки C# (Bedrock, Vertex, Foundry, AWS) не взято.
- **README пакета `@anthropic-ai/aws-sdk` немає.** У жодному з 27 tarball його немає, і в репозиторії
  `packages/aws-sdk/README.md` — порожній файл. Про цей пакет пише сторінка сайту «Claude Platform on AWS».
- **Імена документів.** Сайт — шлях сторінки (`docs-en-models-haiku-5-5-overview`, `docs-en-api-messages-create`,
  `docs-en-api-python-messages-create`); репозиторії — з назвою репозиторію (`anthropic-sdk-python-readme`,
  `anthropic-sdk-typescript-helpers`, `anthropic-sdk-go-api`); код — шлях файла
  (`anthropic-sdk-python-src-anthropic-resources-messages-messages-py`); cookbooks —
  `cookbooks-misc-prompt-caching-ipynb`.
- **Запити `quality`** записано так, як їх ставить модель за промптом: назва з документації, далі опис. Питання про
  мінімальну довжину кешу поставлено про Haiku 5.5: у загальному вигляді («per model») його перекривали 16 однакових
  розділів «Good to know» сторінок моделей, кожен з числом для своєї моделі. Тому цілі тепер дві: загальний перелік
  «Cache limitations» сторінки Prompt caching і розділ «Good to know» сторінки Haiku 5.5, де стоїть «512 tokens».

## Межі, про які треба пам'ятати

- Сайт — англійською. Переклади (11 мов по 288 сторінок, серед них російська) коротші за англійську версію (783
  сторінки), їх не взято.
- Довідник API в редакціях Go, Ruby, C#, Java, PHP і CLI не взято. Методи цих SDK дає HTTP-довідник з тими самими
  описами, `api.md` (Go) і README з тегів.
- Код — лише найновіших TypeScript і Python SDK, без тестів. Старі версії видно з `api.md`, README й релізів кожного
  тегу.
- Лише стабільні випуски: альфи й беты Go, Ruby і `0.34.0-alpha.0` TypeScript не взято.
- Не взято: Claude Code (code.claude.com), Claude Agent SDK (`@anthropic-ai/claude-agent-sdk`, `claude-agent-sdk`),
  репозиторії `skills`, `claude-quickstarts`, а також власний MCP-сервер документації platform.claude.com/docs/mcp.
- claude-cookbooks не має тегів: це знімок гілки main на 17.10.2026. Частина зошитів написана під старі моделі й
  ціни: число з рецепта звіряти зі сторінками сайту.

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/anthropic-api-corpus-2026-10-18.tar.gz` (215 МБ: 6 316 текстів,
паспорт і сховище сирого `raw/` з tarball npm; перед видаленням розпакований окремо й звірений з диском — нуль
розбіжностей). Лише на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/anthropic-api-corpus-РРРР-ММ-ДД.tar.gz -C instances/anthropic-api corpus raw
find instances/anthropic-api/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/anthropic-api/raw
gzip -9 -c instances/anthropic-api/index/passages.json > instances/anthropic-api/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/anthropic-api-corpus-2026-10-18.tar.gz -C instances/anthropic-api
./df anthropic-api smoke
```

**Оновлення.** Новий випуск SDK дописують першим рядком у `tags` його джерела сторінок («"sdk-v0.136.0":
"typescript-0.136.0"» у `typescript-docs`, «"v1.16.0": "python-1.16.0"» у `python-docs`), а для TypeScript і Python
переносять на новий тег і код з прикладами (`typescript-code`, `python-code`, `typescript-examples`,
`python-examples`). Сайт, довідник API, релізи, npm і PyPI підхоплюються самі; для cookbooks у `tags` джерела
`cookbooks` ставлять новий коміт main. Далі `./df anthropic-api refresh`, `manifest`, `vectors`, `smoke`, `quality`.
Оновлення сайту — це повний перепрохід довідника API, а вектори змінених сторінок рахуються заново.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df anthropic-api …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md,
розділ «Спільне середовище». Свій `.env` примірник тримає в `instances/anthropic-api/.env` (`cp .env.example .env`;
для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`, береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df anthropic-api sources --why   # перелік джерел і білий список
./df anthropic-api refresh         # завантажити все задеклароване (близько 50 хвилин)
./df anthropic-api manifest        # оновити паспорт
./df anthropic-api setup           # Qdrant чи пошук лише по словах
./df anthropic-api vectors         # залити корпус у docs-anthropic-api (близько 3 годин)
./df anthropic-api smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df anthropic-api serve          # порт 8860
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8860/mcp`. Якщо порт зайнятий,
сервер скаже про це й вийде: значить, `serve` цього примірника вже десь запущений; хто тримає порт, покаже
`ss -ltnp | grep 8860`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user anthropic-api-docs http://127.0.0.1:8860/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `anthropic-api-docs` і два інструменти `search_docs`, `read_section`. Якщо
`/mcp` показує `failed`, сервер не запущено або запущено з іншим портом.

Зупинка — Ctrl+C у терміналі сервера.
