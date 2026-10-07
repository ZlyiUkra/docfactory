# testing-library — примірник фабрики docfactory

Двадцять шостий примірник фабрики: захищений MCP-сервер, що відповідає на питання про сімейство Testing Library —
тестування інтерфейсу так, як ним користується людина. Тут увесь сайт testing-library.com з усіма обгортками (React,
React Native, Vue, Angular, Svelte, Preact, Solid, Qwik, Marko, Cypress, Puppeteer, Nightwatch, TestCafe,
WebdriverIO), ядро DOM Testing Library, user-event, jest-dom, правила обох eslint-плагінів, а для пакетів React-лінії
ще й README кожної опублікованої версії, нотатки релізів і реєстр версій npm. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо

Testing Library — не одна бібліотека, а сімейство: ядро `@testing-library/dom` дає запити (`getByRole`, `findByText`…)
і очікування (`waitFor`), а обгортка під фреймворк додає `render` для свого фреймворку. Тому примірник **загальний**:
сайт узято цілком, з усіма обгортками, а не лише сторінки React. Коли згодом знадобиться інший фреймворк (скажімо,
Angular у його секції тестів), його пакет докачується в цей самий примірник окремими джерелами — README, реєстр npm,
релізи, — а не заводиться новий примірник.

**Прив'язка до фреймворку — у запиті.** Промпти велять моделі називати обгортку в запиті: працюючи з React, писати
«React Testing Library …», щоб пошук обирав сторінки саме React-обгортки, а не однойменні сторінки Vue чи Svelte. Без
названого фреймворку відповідь іде для React — основної лінії навчання.

**Старі версії теж тут.** Проєкти з давньою історією й легасі-кодом живуть на старих версіях: `wait` і
`waitForElement` замість `waitFor`, user-event 13 із синхронними викликами, `@testing-library/react-hooks` замість
`renderHook`. Тому, крім поточного сайту, взято чотири його знімки, README кожної версії пакетів і правила
eslint-плагінів на кожному мажорі.

У яких фазах і днях планів навчання він потрібен — див. [../../docs/learning-map.md](../../docs/learning-map.md).

## Скільки цього

| Шар | Документів | Різних сторінок | Звідки |
|-----|-----------:|----------------:|--------|
| Сайт testing-library.com: ядро DOM, запити, user-event, гайди, приклади, екосистема, сторінки кожної обгортки | 346 | 125 | тека `docs/` testing-library/testing-library-docs: гілка main і чотири знімки |
| Правила eslint-plugin-testing-library і гайди міграції | 128 | 42 | тека `docs/` і README на main і мажорах 3–7 |
| Правила eslint-plugin-jest-dom | 43 | 13 | тека `docs/` і README на main і мажорах 3–5 |
| Документація `@testing-library/react-hooks` (застарілий пакет) | 24 | 12 | тека `docs/` на мажорах 1–8 |
| README усіх версій семи пакетів, однакові тексти зведено | 494 | — | тег релізу на GitHub |
| README гілки main семи пакетів (ще не випущені правки) | 5 + 2 | — | гілка main |
| Реєстр версій npm семи пакетів: документ на мажорну лінію | 63 | — | registry.npmjs.org |
| Нотатки релізів GitHub семи пакетів | 1 217 | — | GitHub API |

Разом 2 320 документів; фрагментів в індексі — 6 105 (`expected_passages` у `checks.json`). Фрагменти — це шматки
документів між заголовками, по яких іде пошук; однаковий текст різних версій зливається в один з усіма версіями.
README гілки main eslint-плагінів лежать разом з їхньою документацією («+ 2» у таблиці).

Замір `quality` на першому корпусі: перша десятка (питання своїми словами, без версії) — по словах 4 із 10, за змістом
3, разом 4; друга, «як модель» (назви API з обгорткою, як велить промпт), — 8 із 10. Слабке місце — старі версії й
нотатки релізів: на питання своїми словами пошук за змістом охоче бере короткі записи релізів («bug fixes»), а обидва
промахи другої десятки — влучання в ту саму тему, але старої версії. «React Testing Library getByRole query options»
знаходить розділ ByRole сторінки запитів знімка 2020-02 (тоді запити жили на одній сторінці), «user-event type()» —
`type` з документації user-event 13, а не 14. Тому промпти велять називати версію, а відповідь — казати, якої версії
вона стосується.

**Версія у відповіді.** Без названої версії — найпопулярніша лінія за завантаженнями npm на день збирання:
`@testing-library/react` 16 (84% завантажень за тиждень), `@testing-library/dom` 10 (83%), `@testing-library/user-event`
14 (92%), `@testing-library/jest-dom` 6 (77%; найновіша 7 — 14%).

## Пакети

| Пакет | Для чого | README | Реєстр | Релізи |
|-------|----------|:------:|:------:|:------:|
| `@testing-library/react` | `render`, `renderHook`, `act` для React | так | так | так |
| `@testing-library/dom` | ядро: запити, `waitFor`, `fireEvent`, конфігурація | так | так | так |
| `@testing-library/user-event` | дії користувача: клік, набір тексту, клавіатура, буфер обміну | так | так | так |
| `@testing-library/jest-dom` | матчери `toBeInTheDocument`, `toBeVisible`, `toHaveValue`… (і для Vitest) | так | так | так |
| `@testing-library/react-hooks` | тест хуків до RTL 13.1; застарілий, замінений `renderHook` | так | так | так |
| `eslint-plugin-testing-library` | правила лінтера для тестів Testing Library | у документації | так | так |
| `eslint-plugin-jest-dom` | правила лінтера для матчерів jest-dom | у документації | так | так |

Пакети інших обгорток (Vue, Angular, Svelte…) поки не взято: їхні сторінки сайту є, а README, реєстр і релізи
докачуються, коли фреймворк з'явиться в навчанні.

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

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df testing-library <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт testing-library.com | тека `docs/` testing-library/testing-library-docs на гілці main і чотирьох комітах | `ghdocs-history` |
| правила eslint-плагінів, react-hooks | теки `docs/` і README на тегах мажорів і main | `ghdocs-history` |
| README пакетів | тег релізу кожної версії на GitHub | `npm-readme` |
| README гілки main | корінь репозиторію на main | `ghdocs-history` |
| нотатки релізів | GitHub API | `ghreleases` |
| версії пакетів | реєстр npm | `npm-versions` |

Білий список — три хости: `api.github.com`, `raw.githubusercontent.com`, `registry.npmjs.org`. Сам сайт
testing-library.com і npmjs.com не читаються: сайт збирається з тієї самої теки `docs/`, а вкладка версій npmjs.com
показує те, що віддає реєстр. Посилання у відповідях можуть вести на testing-library.com.

Особливості, які варто знати:

- **Знімки сайту.** Тегів версій репозиторій сайту не має, тож, крім main (мітка `current`), взято останні коміти
  перед великими переходами: `2020-02` (DOM 6, RTL 9, ще `wait` і `waitForElement`), `2022-02` (RTL 12, DOM 8,
  user-event 13), `2023-01` (RTL 13 з React 18), `2024-04` (RTL 14–15, DOM 9). Мітка — місяць знімка.
- **Представник злитого тексту.** Коли сторінка однакова в main і в знімку `2024-04`, у відповіді стоїть адреса
  знімка: мітка `2024-04` за числами старша за `current`. Текст той самий, лише посилання веде на коміт, а не на main.
- **Назви з обгорткою.** Сторінки обгорток на сайті мають однакові заголовки — 32 сторінки «API», 27 «Setup». Поле
  `title_prefix` читача додає назву обгортки з теки: «React Testing Library: API», «Vue Testing Library: API». Так
  само названо README гілки main («@testing-library/react, гілка main: README») і сторінки react-hooks.
- **Правила eslint-плагінів — з мажора 3.** У версіях 1–2 теки `docs/` ще не було; їхні правила описано в README,
  а README усіх версій узято окремо.
- **README з HTML-шапкою.** README пакетів починаються з логотипа в HTML; назва пакета в шапці документа є завжди.

## Межі, про які треба пам'ятати

Тут немає Jest і Vitest (окремий примірник `vitest`), Playwright і Cypress як окремих інструментів, MSW, jsdom і
happy-dom. Пакетів обгорток, окрім React, поки немає (є лише їхні сторінки сайту). Issues і GitHub Discussions свідомо
не взято: це рецепти окремих проблем, а не документація.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку, як у vitest і webstandards: у `corpus/` лежить лише паспорт
`index.json`, а сервер підіймається з кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до
символа — кеш тримає повний текст кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/testing-library-corpus-2026-10-07-readme.tar.gz` (1,5 МБ, 2 320 текстів і
паспорт; перед видаленням розпакований окремо й звірений із диском — нуль розбіжностей). В історії git текстів немає
ніде. Архів лежить лише на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/testing-library/index/passages.json         # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/testing-library-corpus-РРРР-ММ-ДД.tar.gz -C instances/testing-library corpus
find instances/testing-library/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/testing-library/index/passages.json > instances/testing-library/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/testing-library-corpus-РРРР-ММ-ДД.tar.gz -C instances/testing-library
./df testing-library smoke
```

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/testing-library/index/passages.json.gz`,
далі `./df testing-library vectors` заллє колекцію Qdrant (43 хвилини на цій машині).

## Установка venv

```
cd instances/testing-library
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df testing-library sources --why   # перелік джерел і білий список
./df testing-library refresh         # завантажити все задеклароване (~40 хвилин)
./df testing-library manifest        # оновити паспорт
./df testing-library setup           # Qdrant чи пошук лише по словах
./df testing-library vectors         # залити корпус у docs-testing-library (~45 хвилин)
./df testing-library smoke           # перевірки
```

`refresh` довший за 30 хвилин: із Claude Code його треба запускати окремим процесом (`setsid nohup …`), інакше
фонову задачу обірве оболонка. Обірваний `refresh` продовжується з `--missing`: уже записане він не тягне вдруге.
Найдовша частина — README: реєстр npm віддає текст лише найновішої версії, тож кожна з майже тисячі версій семи
пакетів читається окремо. Без `GITHUB_TOKEN` у `.env` анонімного ліміту GitHub API (60 звернень на годину) не вистачить
на релізи всіх пакетів.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd /mnt/c/Projects/fwdays/docfactory
./df testing-library serve           # порт 8786
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8786/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user testing-library-docs http://127.0.0.1:8786/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `testing-library-docs` і два інструменти `search_docs`, `read_section`. Якщо сесію
Claude Code відкрито раніше, ніж піднято сервер, вона покаже його як недоступний: у `/mcp` виберіть сервер і
«Reconnect».

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
