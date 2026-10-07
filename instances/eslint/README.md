# eslint — примірник фабрики docfactory

Двадцять дев'ятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про ESLint — лінтер JavaScript і
TypeScript, який перевіряє код правилами й частину знахідок виправляє сам, — і про плагіни, без яких він у React- і
TypeScript-проєкті не обходиться. Тут документація з репозиторію eslint/eslint на кожній мінорній лінії 8, 9 і 10 та
на останній версії кожного старшого мажору, блог eslint.org, README кожної стабільної версії, нотатки релізів і реєстр
версій npm; поруч — README і CHANGELOG `eslint-plugin-react-hooks`, typescript-eslint, `eslint-plugin-react` і
`eslint-plugin-jsx-a11y`. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо

ESLint 9 зробив типовим плоский конфіг (flat config, файл `eslint.config.js`) замість `.eslintrc`, ESLint 10 старий
формат прибрав зовсім, а мінорні версії раз на два-чотири тижні додають правила, опції й функції конфігу
(`defineConfig`, `globalIgnores`, `extends` у плоскому конфігу). Робочі проєкти живуть на всіх трьох лініях: на день
збирання 9.x — 56% завантажень `eslint` за тиждень, 8.x — 22%, 10.x — 17%. Порада для однієї лінії в іншій не
спрацює, тому тут кожна мінорна лінія 8–10, а від старших мажорів — остання версія.

Плагіни взято тому, що в проєкті вони йдуть разом з ESLint: `eslint-plugin-react-hooks` — правила хуків
(`rules-of-hooks`, `exhaustive-deps`) і діагностика React Compiler, typescript-eslint — парсер і правила для TypeScript,
зокрема типізований лінт, `eslint-plugin-react` і `eslint-plugin-jsx-a11y` — правила JSX і доступності.

У яких фазах і днях планів навчання він потрібен — див. [../../docs/learning-map.md](../../docs/learning-map.md).

## Скільки цього

| Шар | Документів | Різних сторінок | Звідки |
|-----|-----------:|----------------:|--------|
| Документація ESLint: використання, конфіг, правила, розширення, інтеграція, міграції | 5 836 | 845 | тека `docs/` eslint/eslint на 119 тегах (0.24–10.12) |
| Блог eslint.org: анонс кожного релізу, розбори | 484 | — | `src/content/blog` eslint/eslint.org, гілка main |
| README стабільних версій `eslint`, однакові тексти зведено | 206 | — | тег релізу на GitHub |
| Нотатки релізів eslint/eslint | 389 | — | GitHub API |
| README і CHANGELOG `eslint-plugin-react-hooks` | 2 | 2 | `packages/eslint-plugin-react-hooks` react/react, гілка main |
| typescript-eslint: початок роботи, типізований лінт, пакети, правила; блог | 1 038 | 268 | typescript-eslint/typescript-eslint на 9 тегах (0.2–8.71) і main |
| `eslint-plugin-react`: правила, README, CHANGELOG | 259 | 110 | jsx-eslint/eslint-plugin-react на 7 тегах (1.6–7.37) |
| `eslint-plugin-jsx-a11y`: правила, README, CHANGELOG | 118 | 54 | jsx-eslint/eslint-plugin-jsx-a11y на 7 тегах (0.6–6.10) |
| Нотатки релізів трьох репозиторіїв плагінів | 663 | — | GitHub API |
| Реєстр версій npm восьми пакетів | 64 | — | registry.npmjs.org |

Разом 9 059 документів; фрагментів в індексі — 28 404 (`expected_passages` у `checks.json`). Фрагменти — це шматки
документів між заголовками, по яких іде пошук; однаковий текст різних версій зливається в один з усіма версіями.
Найбільше — сторінки правил: кожна має розділи з прикладами правильного й неправильного коду та опціями, і правка
однієї опції в новій версії дає новий текст сторінки.

Замір `quality` на першому корпусі: перша десятка (питання своїми словами, без версії) — по словах 4 із 10, за змістом
6, разом 6; друга, «як модель» (назви правил і опцій, з `version: "9.39"`, для typescript-eslint — «8.71», як велить
промпт), — 10 із 10. Без версії питання своїми словами тонуть у сотнях однакових сторінок різних ліній: на «вимагай
строгої рівності» приходить стара сторінка `docs/rules/eqeqeq`, а не поточна `docs/src/rules/eqeqeq` — текст той самий,
але ціллю заміру стоїть нова; на «які глобальні змінні існують» — посібник з міграції на 2.0. З версією й назвою правила,
як пише модель, промахів немає.

**Версія у відповіді.** Без названої версії — ESLint 9: на день збирання 56% завантажень. Коли ESLint 10 робить
інакше, відповідь каже і про нього. Фільтр `version` — мінорна лінія: «9.39» бере 9.39.x. Плагіни мають власні номери
(typescript-eslint «8.71», `eslint-plugin-react` «7.37», `eslint-plugin-jsx-a11y` «6.10», `eslint-plugin-react-hooks`
«7.1»), і той самий номер може бути й у ESLint — назва документа каже, чий він.

## Пакети

| Пакет | Для чого | Документація | README | Реєстр | Релізи |
|-------|----------|:------------:|:------:|:------:|:------:|
| `eslint` | сам лінтер: CLI, конфіг, ядро правил, Node.js API | кожна мінорна 8–10, остання версія мажорів 0–7 | кожна версія | так | так |
| `@eslint/js` | конфіги `recommended` і `all` для плоского конфігу | — | з тегів ESLint | так | — |
| `eslint-plugin-react-hooks` | `rules-of-hooks`, `exhaustive-deps`, правила React Compiler | — | з main, плюс CHANGELOG | так | — |
| `typescript-eslint`, `@typescript-eslint/eslint-plugin`, `@typescript-eslint/parser` | парсер і правила TypeScript | остання версія кожного мажору | з тегів | так | так |
| `eslint-plugin-react` | правила JSX і компонентів (`react/…`) | остання версія кожного мажору | з тегів | так | так |
| `eslint-plugin-jsx-a11y` | правила доступності JSX (`jsx-a11y/…`) | остання версія кожного мажору | з тегів | так | так |

Збірки alpha, beta, rc, canary, next і experimental не беруться ні в README, ні в реєстр (поле `skip_versions`): у
`eslint-plugin-react-hooks` їх 2 745 із 2 798, у `@typescript-eslint/eslint-plugin` — 4 421 із 4 831.

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

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df eslint <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| документація ESLint | тека `docs/` eslint/eslint на останньому тезі кожної мінорної лінії 8–10 і кожного мажору 0–7 | `ghdocs-history` |
| блог | eslint/eslint.org, гілка main | `ghdocs-history` |
| `eslint-plugin-react-hooks` | react/react, гілка main | `ghdocs-history` |
| документація плагінів | репозиторії плагінів на останньому тезі кожного мажору | `ghdocs-history` |
| README `eslint` | тег релізу кожної стабільної версії на GitHub | `npm-readme` |
| нотатки релізів | GitHub API | `ghreleases` |
| версії пакетів | реєстр npm | `npm-versions` |

Білий список — три хости: `api.github.com`, `raw.githubusercontent.com`, `registry.npmjs.org`. Самі eslint.org і
typescript-eslint.io не читаються: сайти збираються з тих самих репозиторіїв. Посилання у відповідях можуть вести на
сайти.

Особливості, які варто знати:

- **Два розміщення документації ESLint.** До 8.x сторінки лежали в `docs/user-guide`, `docs/developer-guide` і
  `docs/rules`, з 8.x — у `docs/src` (`use`, `extend`, `integrate`, `rules`), з якої збирається eslint.org. Одна й та
  сама сторінка за різними шляхами — це історія, а не дублікат.
- **Однакові назви правил.** `no-unused-vars`, `no-shadow`, `no-redeclare` є і в ядрі ESLint, і в typescript-eslint.
  Поле `title_prefix` дає документам плагінів назву з пакетом: «@typescript-eslint: no-unused-vars»,
  «eslint-plugin-react: jsx-key», «jsx-a11y: alt-text».
- **Репозиторій React переїхав** з `facebook/react` у `react/react`; на старе ім'я GitHub відповідає лише
  переадресацією, а фабрика за адреси поза `sources.json` не ходить, тож у джерелі записано нове.
- **`eslint-plugin-react-hooks`** окремих тегів у репозиторії React не має: README і CHANGELOG — з гілки main, мітка
  «7.1» — лінія останньої стабільної версії на день збирання; після нового релізу її треба змінити. Сторінка кожного
  правила плагіна (`purity`, `refs`, `set-state-in-effect`…) — на react.dev, у примірнику `react`.
- **Мажори плагінів — лише останні версії**: мінорні зміни між ними описують CHANGELOG і нотатки релізів.

## Межі, про які треба пам'ятати

Тут немає документації Prettier, Biome, Oxlint і stylelint, самого компілятора TypeScript (примірник `typescript`),
React (примірник `react`) і сторінок правил `eslint-plugin-react-hooks` на react.dev (теж примірник `react`). Інших
плагінів ESLint (`eslint-plugin-import`, `eslint-plugin-testing-library` — він у примірнику `testing-library`,
`@next/eslint-plugin-next` — у примірнику `nextjs`) тут теж немає. Issues і GitHub Discussions свідомо не взято.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку, як у playwright: у `corpus/` лежить лише паспорт `index.json`, а сервер
підіймається з кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає
повний текст кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/eslint-corpus-2026-10-07-readme.tar.gz` (5,5 МБ, 9 059 текстів і паспорт;
перед видаленням розпакований окремо й звірений із диском — нуль розбіжностей). В історії git текстів немає ніде.
Архів лежить лише на цій машині.

**Зайві точки.** У колекції `docs-eslint` 33 253 точки на 33 244 фрагменти: 9 лишилися від п'яти нотаток передрелізів
1.0 і 2.0 (`v1.0.0-rc-1`…), які вже після заливки виключено полем `skip` — з тегу з дефісом у мітці не читається
номер версії. Пошук їх не показує; прибрати фізично можна лише знесенням колекції й новим `vectors`.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/eslint/index/passages.json         # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/eslint-corpus-РРРР-ММ-ДД.tar.gz -C instances/eslint corpus
find instances/eslint/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/eslint/index/passages.json > instances/eslint/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/eslint-corpus-РРРР-ММ-ДД.tar.gz -C instances/eslint
./df eslint smoke
```

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/eslint/index/passages.json.gz`, далі
`./df eslint vectors` заллє колекцію Qdrant (66 хвилин на цій машині).

## Установка venv

```
cd instances/eslint
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df eslint sources --why   # перелік джерел і білий список
./df eslint refresh         # завантажити все задеклароване (~3 години 15 хвилин)
./df eslint manifest        # оновити паспорт
./df eslint setup           # Qdrant чи пошук лише по словах
./df eslint vectors         # залити корпус у docs-eslint (~66 хвилин)
./df eslint smoke           # перевірки
```

Найдовша частина `refresh` — документація ESLint: спершу читаються дерева 119 тегів (журнал тим часом мовчить),
потім пишуться 5 836 текстів, приблизно 44 за хвилину — між зверненнями стоїть пауза в секунду. README читаються по
одному на кожну стабільну версію. Без `GITHUB_TOKEN` у `.env` анонімного ліміту GitHub API (60 звернень на годину) не
вистачить уже на дерева. Довший за 30 хвилин крок із Claude Code запускають окремим процесом (`setsid nohup …`);
обірваний `refresh` продовжується з `--missing`.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd /mnt/c/Projects/fwdays/docfactory
./df eslint serve           # порт 8789
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8789/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user eslint-docs http://127.0.0.1:8789/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `eslint-docs` і два інструменти `search_docs`, `read_section`. Якщо сесію Claude
Code відкрито раніше, ніж піднято сервер, вона покаже його як недоступний: у `/mcp` виберіть сервер і «Reconnect».

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
