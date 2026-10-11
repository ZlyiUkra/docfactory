# tanstack-router — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про TanStack Router і TanStack Start за офіційною документацією всіх
їхніх сталих версій — від 1.0.0 (2023) до поточної 1.x — і про їхнього попередника React Location (1.0.0–3.7.4,
2019–2022). Окрім документації, він знає приклади, журнали змін і нотатки релізів пакетів, записи блогу TanStack та
історію версій кожного пакета в реєстрі npm, зокрема пакетів, яких уже немає. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо вся історія

Мажорна версія в Router одна, 1.x, але API всередині неї мінявся не раз: `NotFoundRoute` поступився
`notFoundComponent`, опції `blockerFn` і `condition` хука `useBlocker` застаріли на користь `shouldBlockFn`, а в
Start «API routes» стали «server routes». Сайт тричі переносив сторінки між теками. Тож питання до документації
часто звучить «як це було в моїй версії», «з якої версії є `loaderDeps`» чи «на що замінили». Відповідь дає лише
документація саме тієї версії, тому корпус — не одна редакція сайту, а вся історія репозиторію, і кожен документ
несе свої версії. React Location — та сама бібліотека до перейменування: сторінка `migrate-from-react-location`
прямо веде з неї на Router, і без її документації половина такого переходу лишалася б без джерела.

## Скільки цього

| Шар | Документів | Звідки |
|-----|-----------:|--------|
| Документація Router і Start всіх 1 385 сталих тегів: кожен неповторний текст файла один раз, з усіма версіями, де він був таким | 2 889 | репозиторій TanStack/router |
| Документація React Location всіх 76 сталих версій | 114 | той самий репозиторій, коміт кожної версії |
| Приклади React, Solid і Vue (Router і Start) та приклади React Location 3.x | 137 | тека `examples/` |
| Журнали змін 42 пакетів `@tanstack/*` | 2 182 | `packages/*/CHANGELOG.md` |
| Нотатки сталих релізів: спільні теги v1.0.0–v1.166.7 і теги кожного пакета | 2 421 | GitHub API |
| Реєстр npm: огляд і лінії 81 пакета — 69 пакетів `@tanstack/*` (і чинних, і вже знятих) та 12 пакетів React Location | 191 | registry.npmjs.org |
| Блог TanStack: записи про Router і Start, постмортем атаки на пакети npm | 20 | репозиторій TanStack/tanstack.com |

Разом 7 954 документи; фрагментів в індексі — 23 576 (`expected_passages` у `checks.json`).

Найбільше фрагментів дають нотатки релізів (7 152) і документація (7 043): на кожен з 1 385 тегів документації
припадає 2 889 різних текстів, бо між релізами змінюються лише кілька сторінок.

Замір `quality` на першому корпусі: по словах 7 із 10, за змістом 7, разом 6; десятка «як модель» — 10 із 10.
Перша десятка — переказ питання своїми словами, і промахи тут такі:

- **Злиття губить влучання обох способів.** На «run code only on the server and call it from a component» сторінку
  server functions Start знаходять і пошук по словах, і пошук за змістом, але в об'єднаній видачі першими стоять
  правило ESLint `no-client-code-in-server-component` і сторінка selective SSR, де ті самі слова густіші.
- **Переказ без назв не доходить до сторінки.** «make an api client available to every loader» — це
  `router-context`, але слова «loader» і «client» тягнуть розділи `data-loading` про зовнішній кеш. «fetch the data a
  page needs before it renders» по словах веде на сторінку server components Start, а «send visitors who are not
  signed in to the login page» — на розділ redirect серверних функцій; за змістом обидва знаходять свої сторінки.

Дві цілі першої десятки доповнено сторінками, які справді відповідають: на «ask for confirmation before leaving a page
with unsaved changes» — приклад `react/navigation-blocking`, на «custom page when no route matches the address» —
довідник `defaultGlobalNotFoundComponent` і `notFoundComponent`.

Десятка «як модель» — запити назвами API, як велить промпт. На першому замірі вона дала 9 із 10: на «notFoundComponent»
видача ставила першою сторінку довідника `NotFoundComponent component`, а ціллю був лише розділ посібника. Довідник —
теж відповідь, і його дописано в ціль.

Поле `max_per_doc` заміряно 0/1/2/3: «як модель» 10, 9, 10, 10, перша десятка разом 4, 5, 4, 4 (до доповнення двох
цілей). Одиниця коштує десятці «як модель» влучання, 2 і 3 нічого не змінюють — поле не ввімкнене.

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа.
  Самих текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`, розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача. Перелік усіх 1 385 тегів
  документації лежить саме тут, у полі `tags` джерела `tsr-docs`, а 76 комітів React Location — у полі `tags`
  джерела `rl-docs`: оновлювач не питає в GitHub, які теги існують.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — ключ Anthropic (лише для кроку `ask`) і токен GitHub (лише для завантаження корпусу); `.mcp.json` —
  запис HTTP-сервера для Claude Code.
- `.venv/` — власний venv примірника; `requirements.txt` — його склад.

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df tanstack-router <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| документація всіх версій Router і Start | дерево кожного тегу через GitHub API, текст — `raw.githubusercontent.com` | `ghdocs-history` |
| документація React Location | дерево коміту кожної версії, текст — `raw.githubusercontent.com` | `ghdocs-history` |
| приклади | тека `examples/` на тезі чи коміті | `ghexamples` |
| журнали змін пакетів | `packages/*/CHANGELOG.md` гілки main | `changelog-named` |
| нотатки релізів | GitHub API, відбір за префіксом тегу, лише сталі | `ghreleases-stable`, новий |
| реєстр npm | registry.npmjs.org, одне звернення на пакет | `npm-versions` |
| блог | `src/blog/*.md` репозиторію tanstack.com | `mdfile` |

Читач `ghreleases-stable` додано разом із цим примірником (`engine/readers/ghreleasesstable.py`). Розбір у нього той
самий, що в `ghreleases-tagged`, з двома відмінностями. Перша — передрелізи відкидаються: у потоці релізів
TanStack Router 3 146 записів, з них 579 — беты 0.0.1, альфи 1.121 і 1.132 та лінія Solid 2.0 у rc. Друга —
сторінки потоку читаються раз за прогін: інакше 43 джерела релізів гортали б ті самі 32 сторінки API кожне.

Особливості, які варто знати:

- **Сайт будується з репозиторію.** tanstack.com/router і tanstack.com/start беруть сторінки з теки `docs/`
  репозиторію. Тож текст береться прямо з тегу, а адреса в шапці документа — blob на GitHub.
- **Де лежала документація.** 1.0 — `docs/guide/` і `docs/api/`; далі `docs/framework/react/…` з окремою підтекою
  `start`; далі `docs/router/framework/<фреймворк>/…` і `docs/start/framework/<фреймворк>/…`; тепер сторінки
  роутера — `docs/router/{guide,api,routing,how-to,installation}/…`, одні на всі фреймворки, а Start тримає
  `docs/start/framework/{react,solid}/guide/`. Поле `slug_rewrite` зводить переїзди до теперішнього імені: 806
  різних шляхів дають 361 сторінку, і незмінний розділ різних епох зливається в один фрагмент. Сторінки React і
  спільні сторінки злито; старі сторінки саме для Solid лишилися окремими, щоб не ховатися за спільною редакцією.
- **Назви сторінок.** Сторінки Start мають назву «TanStack Start: …» (з фреймворком у дужках), сторінки React
  Location — «React Location: …» (поле `title_prefix`): заголовки «Overview», «Quick Start» чи «Server Functions»
  інакше не розрізняли б продукти.
- **Теги.** До v1.166.7 репозиторій ставив спільні теги `vX.Y.Z` (1 305 сталих). Далі — лише теги окремих пакетів, і
  версією документації служать 80 тегів `@tanstack/react-router@X.Y.Z`: документація одна на всі пакети, а
  React-адаптер — найпопулярніший. Передрелізи не беруться зовсім: ні документація, ні нотатки релізів. Реєстр npm
  перелічує й передрелізи, як і в решті примірників: це те, що можна встановити.
- **React Location — з комітів.** Тегів React Location у репозиторії не лишилося, але історія main ціла. Кожна стала
  версія з npm (react-location 1.0.0–3.3.4 і `@tanstack/react-location` 3.4.0–3.7.4) прив'язана до коміту: коміт
  релізу («release: v3.7.4»), якщо є; інакше `gitHead` з реєстру; інакше останній коміт main перед публікацією.
  1.x–2.x документовано лише кореневим `README.md`, 3.x — ще й сторінками сайту react-location.tanstack.com.
- **Версії пакетів розходяться.** З 1.166.8 кожен пакет нумерується сам: `@tanstack/react-router` на 1.170.x,
  `@tanstack/react-start` — на 1.168.x, `@tanstack/router-core` — на 1.171.x. Журнали змін і релізи пакета несуть
  його власну версію.
- **Номери React Location і Router перетинаються.** React Location 1.0.0–1.1.2 має ті самі номери, що й Router
  1.0.0–1.1.2, а лінії 2 і 3 — лише React Location. Промпт велить моделі називати React Location у запиті.
- **Знято з реєстру — теж історія.** 27 пакетів, що були в репозиторії й зникли (`@tanstack/start`,
  `react-router-with-query`, `router-zod-adapter`, `start-api-routes`…), мають у корпусі свої документи npm: з
  якої до якої версії вони жили і що прийшло на заміну, видно з дат.
- **Приклади — лише на останньому тезі** (`@tanstack/react-router@1.170.42`) і на коміті React Location 3.7.4;
  `package.json` у кожному прикладі каже, на якій версії він написаний.
- **Блог — без версії.** Записи блогу TanStack версії не мають, тож `expect_unversioned` у `checks.json` — `true`.

## Межі, про які треба пам'ятати

TanStack Query, Table, Form, Virtual і решти TanStack тут немає, як і React Router, Remix чи Next.js. Solid Router і
Solid Start 2.0 ще в rc — їхньої документації немає, лише рядки передрелізів у документах реєстру npm. Сторінки
`how-to/drafts` і службовий `docs/AGENTS.md` на сайт не йдуть і не беруться. Сторінки прикладів сайту React Location
(`docs/src/pages/examples/*.md`) — лише рамка CodeSandbox; код тих самих прикладів є в `rl-examples`.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/tanstack-router-corpus-2026-10-11.tar.gz` (9 МБ, 7 954 тексти й
паспорт; перед видаленням розпакований окремо й звірений із диском — нуль розбіжностей). В історії git текстів
немає ніде. Архів лежить лише на цій машині.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/tanstack-router-corpus-2026-10-11.tar.gz -C instances/tanstack-router
./df tanstack-router smoke
```

**Як знову винести** — після оновлення, коли `vectors` і `smoke` пройшли (вони ж збирають свіжий кеш):

```
ls -l instances/tanstack-router/index/passages.json       # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/tanstack-router-corpus-РРРР-ММ-ДД.tar.gz -C instances/tanstack-router corpus
find instances/tanstack-router/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/tanstack-router/index/passages.json > instances/tanstack-router/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти» і «Як повернути тексти».

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»): звірка індексу з документами і звірка паспорта з файлами.

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k
instances/tanstack-router/index/passages.json.gz`, далі `./df tanstack-router vectors` заллє колекцію Qdrant (~1
година).

## Установка venv

```
cd instances/tanstack-router
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
./df tanstack-router sources --why   # перелік джерел і білий список
./df tanstack-router refresh         # завантажити все задеклароване (~2 год 45 хв)
./df tanstack-router manifest        # оновити паспорт
./df tanstack-router setup           # Qdrant чи пошук лише по словах
./df tanstack-router vectors         # залити корпус у docs-tanstack-router (~1 година)
./df tanstack-router smoke           # перевірки
```

Перші ~50 хвилин `refresh` журнал мовчить, а `corpus/` порожній: читач проходить дерево кожного з 1 385 тегів (дерево
новітнього тегу — 4 МБ JSON) і лише потім починає писати файли. Документація далі пишеться ~65 хвилин, приклади —
~45. Без токена GitHub перелік тегів ішов би годинними вікнами по 60 звернень.

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df tanstack-router serve          # порт 8822
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8822/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user tanstack-router-docs http://127.0.0.1:8822/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `tanstack-router-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
