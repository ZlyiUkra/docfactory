# astro-markdown-pipeline — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про конвеєр «Markdown → HTML» екосистеми unified, у тому вигляді, в
якому його збирає Astro: `unified`, `remark-parse`, `remark-rehype`, `rehype-sanitize` з `hast-util-sanitize`,
`remark-math` з `rehype-katex` і KaTeX, підсвітка коду Shiki з пакетами `@shikijs/*`, а також увесь сайт unifiedjs.com. Документація — усіх
стабільних версій пакетів, а не лише останньої. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо

Примірник потрібен для переписування Astro-проєкту на повний стек без зовнішніх сервісів: Markdown, який вводить
користувач, треба перетворити на HTML, очистити від небезпечного (санітизація — вилучення тегів, атрибутів і посилань,
що можуть виконати код на сторінці) та підсвітити код і формули. Кожна ланка конвеєра — окремий пакет зі своєю
версією, і поведінка між мажорними лініями міняється: пакети стали лише ESM, Shiki 1.0 переписано з нуля, KaTeX 0.16
змінив підтримку функцій. Тому корпус — усі стабільні версії, а питання про сумісність («яка версія `rehype-sanitize`
працює з моїм `remark-rehype`») дістають відповідь із документації саме тієї версії.

## Скільки цього

| Шар | Документів | Звідки |
|-----|-----------:|--------|
| README: кожен неповторний текст один раз, з усіма версіями, де він був таким | 305 | tarball кожної версії npm |
| Типи TypeScript, розділені за оголошеннями | 278 | tarball кожної версії npm |
| Журнал змін `@astrojs/markdown-remark` | 45 | `CHANGELOG.md` із tarball кожної версії |
| Реєстр npm: огляд і лінії з вимогами до Node, залежностями й датами | 171 | registry.npmjs.org |
| Документація Shiki (shiki.style) за знімком на кожен стабільний реліз | 305 | репозиторій `shikijs/shiki`, тека `docs/` |
| Документація KaTeX (katex.org) за знімком на кожен стабільний реліз | 474 | репозиторій `KaTeX/KaTeX`, тека `docs/` |
| Сайт unifiedjs.com: навчання, спільнота, каталог пакетів, проєктів і тем | 1326 | sitemap.xml сайту |

Разом 2904 документи; фрагментів в індексі — 18 362 (`expected_passages` у `checks.json`).

Двадцять шість пакетів npm (кількість стабільних версій у дужках):

- конвеєр: `unified` (56; версія 2.1.3 зникла з реєстру, пропущена), `remark-parse` (29), `remark-gfm` (6),
  `remark-rehype` (26), `rehype-raw` (12), `rehype-sanitize` (10), `hast-util-sanitize` (20), `rehype-stringify` (18);
- формули: `remark-math` (24), `micromark-extension-math` (12), `mdast-util-math` (9), `rehype-katex` (22), `katex` (117);
- Astro: `@astrojs/markdown-remark` (98);
- підсвітка коду: `shiki` (191) і 11 пакетів `@shikijs/*` — `core` (140), `types` (93), `engine-oniguruma` (92),
  `engine-javascript` (93), `rehype` (137), `transformers` (138), `markdown-it` (137), `monaco` (140), `twoslash` (140),
  `colorized-brackets` (77), `compat` (91). Пакети `@shikijs/langs` і `@shikijs/themes` не беруться: це дані мов і
  тем, а не документація.

Замір `quality`: по словах 6 із 10, за змістом 6, разом 7; десятка «як модель» — 10 із 10. Промахи — це запити
перефразом про санітизацію («strip dangerous tags»), де відповідь перебивають сторінки каталогу unifiedjs.com про
інші пакети. Дев'ять сторінок каталогу, що дублювали README наших пакетів (`unified`, `remark-parse`, `rehype-raw`,
`rehype-stringify`, `remark-rehype`, `rehype-sanitize`, `hast-util-sanitize`, `rehype-katex`, `remark-math`),
виключені (`exclude` у `sources.json`), і якість не просіла.

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа.
  Самих текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`, розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — ключ Anthropic (лише для кроку `ask`) і токен GitHub (лише для завантаження корпусу); `.mcp.json` —
  запис HTTP-сервера для Claude Code.
- `.venv/` — власний venv примірника; `requirements.txt` — його склад.

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df astro-markdown-pipeline <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| README, типи, журнал змін усіх версій | tarball `registry.npmjs.org/<пакет>/-/<пакет>-X.tgz` | `npm-tarball-files` |
| реєстр npm | registry.npmjs.org, одне звернення на пакет | `npm-versions` |
| документація Shiki і KaTeX | дерево `docs/` репозиторію на мить перед наступним релізом лінії | `ghsite-dated` |
| сайт unifiedjs.com | sitemap.xml і HTML сторінок | `sitemap-html` |

Особливості, які варто знати:

- **Чому tarball.** Реєстр записав `gitHead` лише для частини версій (у `shiki` — 38 зі 191, у `rehype-katex` — 4 з 22),
  тож README з репозиторію на коміті знайшовся б не для всіх. Tarball — це точно те, що отримує `npm install`.
- **Документація Shiki й KaTeX — з репозиторіїв.** Обидва сайти (VitePress і Docusaurus) показують лише поточний
  стан, а теки `docs/` репозиторіїв дають стан на кожен реліз. Окремо shiki.style і katex.org не завантажуються: це
  був би той самий текст ще раз. Для версій до появи `docs/` (Shiki до 1.0, старий KaTeX) документів-сторінок немає —
  там лишаються README й типи.
- **Документ — неповторний текст.** Версії, де файл не змінився, ділять один документ; у рядку `# версія:` стоять усі.
  `revision_suffix` у `config.json` зводить редакції README до спільного ключа розділу.
- **README `katex` — 116 документів** замість кількох: у кожній версії в тексті зашито її номер (посилання на CDN),
  тож усі редакції різні. Шуму в пошуку це додає небагато, бо розділи зводяться за ключем.
- **Сторінки unifiedjs.com — без `explore/keyword`.** Це 710 переліків пакетів за ключовим словом без власного
  тексту (по 400 КБ кожна); їх пропущено за згодою користувача. Решта сайту — навчання (`learn`), спільнота
  (`community`), пакети (`explore/package`, 482 сторінки з README екосистеми remark, rehype, retext, unist, mdast,
  hast), проєкти й теми.
- **Зайвих дублікатів немає.** Каталог unifiedjs.com містить копії README багатьох пакетів, і дев'ять копій наших
  пакетів у корпус не беруться — оригінали є з версіями.
- **`@astrojs/markdown-remark` не має README** у жодній версії пакета; документація — журнал змін, типи й реєстр.
- **Порожній README `shiki` 0.2.7** (0 символів) у корпус не потрапляє; `refresh` повідомляє про це як про один збій.
- **Передреліз-мітки.** README, типи й документація беруть лише стабільні версії (`skip_versions: "-"`, `only`);
  реєстр npm (`npm-versions`) показує й передрелізи (наприклад, `shiki 0.0.3-next.3`).

## Межі, про які треба пам'ятати

Документації Astro поза його markdown-пакетом (маршрутизація, компоненти, колекції контенту), MDX, `markdown-it`,
`marked` та інших обробників Markdown тут немає. Решта пакетів екосистеми (`mdast-util-to-hast`, `hast-util-to-html`,
`unist-util-visit`, `rehype-highlight` тощо) присутні лише як сторінки каталогу unifiedjs.com — без версій і без
історії. Код бібліотек не входить.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/astro-markdown-pipeline-corpus-2026-10-09.tar.gz` (2904 тексти і паспорт).
В історії git текстів немає ніде. Архів лежить лише на цій машині.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/astro-markdown-pipeline-corpus-2026-10-09.tar.gz -C instances/astro-markdown-pipeline
./df astro-markdown-pipeline smoke
```

**Як знову винести** — після оновлення, коли `vectors` і `smoke` пройшли (вони ж збирають свіжий кеш):

```
ls -l instances/astro-markdown-pipeline/index/passages.json       # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/astro-markdown-pipeline-corpus-РРРР-ММ-ДД.tar.gz -C instances/astro-markdown-pipeline corpus
find instances/astro-markdown-pipeline/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/astro-markdown-pipeline/index/passages.json > instances/astro-markdown-pipeline/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти» і «Як повернути тексти».

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати:
`gunzip -k instances/astro-markdown-pipeline/index/passages.json.gz`, далі `./df astro-markdown-pipeline vectors` заллє колекцію
Qdrant (близько години: 18 тисяч векторів).

## Установка venv

```
cd instances/astro-markdown-pipeline
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df astro-markdown-pipeline sources --why   # перелік джерел і білий список
./df astro-markdown-pipeline refresh         # завантажити все задеклароване (хвилини)
./df astro-markdown-pipeline manifest        # оновити паспорт
./df astro-markdown-pipeline setup           # Qdrant чи пошук лише по словах
./df astro-markdown-pipeline vectors         # залити корпус у docs-markdown-pipeline
./df astro-markdown-pipeline smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df astro-markdown-pipeline serve          # порт 8808
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8808/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user astro-markdown-pipeline-docs http://127.0.0.1:8808/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `astro-markdown-pipeline-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
