# shadcn — примірник фабрики docfactory

Тридцять дев'ятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про shadcn/ui і Radix UI. Тут
документація shadcn/ui кожної мінорної версії CLI від 0.1 до 4.21 — поточний сайт ui.shadcn.com і сайт для Tailwind CSS
v3 — з прикладами й кодом компонентів, а також Radix Primitives (кожна версія кожного компонента до 2025 року і пакет
`radix-ui` 1.1–1.7), Radix Themes 1.0–3.3 і Radix Colors 0.1–3.0. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо

shadcn/ui — не бібліотека з пакета, а набір компонентів, які CLI (`npx shadcn add dialog`) копіює в проєкт; далі код
компонента — ваш. Більшість компонентів обгортає примітиви Radix: shadcn дає вигляд і розмітку, Radix — поведінку,
доступність, керування фокусом і клавіатуру. Тому на питання «як зробити діалог керованим» чи «чому меню не
закривається» відповідь лежить у двох документаціях одразу: як компонент поставити й ужити — на сторінці shadcn, а
пропси (`open`, `onOpenChange`, `asChild`), атрибути `data-*` і клавіші частин — на сторінці Radix того самого
компонента. Через це обидві — в одному примірнику.

Версії тут важать не менше: Tailwind CSS v3 і v4 мають різні сайти shadcn з різним налаштуванням тем, CLI міняв
`components.json` і команди, з 3.x кожен компонент існує в трьох варіантах — на Radix, на Base UI і на React Aria, а
Radix 2025 року замінив пакет на кожен компонент (`@radix-ui/react-dialog`) одним пакетом `radix-ui`. Проєкт клієнта
може стояти на будь-якій з цих точок.

**Етапи.** Примірник збирається трьома етапами: 1) shadcn/ui і Radix — цей; 2) Base UI; 3) React Aria. Кожен етап
лишає робочий примірник, наступні лише додають джерела. Сторінки shadcn для варіантів на Base UI і React Aria
(`components/base/…`, `components/aria/…`) є вже тут; власної документації Base UI і React Aria поки немає.

У яких фазах і днях планів навчання він потрібен — див. [../../docs/learning-map.md](../../docs/learning-map.md).

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| shadcn/ui, поточний сайт (2.6–4.21) | 867 | 7 178 | `shadcn-ui/ui`, тека `apps/v4/content/docs` |
| shadcn/ui, сайт для Tailwind CSS v3 (0.1–3.8) | 519 | 1 580 | там само, `apps/www/…`, згодом `deprecated/www/…` |
| Radix Primitives | 282 | 1 536 | `radix-ui/website`, тека `data/primitives/docs` |
| Radix Themes 1.0–3.3 | 262 | 956 | там само, `data/themes/docs` |
| Radix Colors 0.1–3.0 | 28 | 146 | там само, `data/colors` |

Разом 1 958 документів; фрагментів в індексі — 11 396 (`expected_passages` у `checks.json`). Фрагменти — це шматки
документів між заголовками, по яких іде пошук. Документ — це одна редакція сторінки: сторінка, що не мінялася від 4.0
до 4.21, — один документ із двадцятьма двома версіями, а змінена — кілька. Однаковий текст розділу в різних редакціях
зливається в один фрагмент зі списком версій. Поточний сайт 4.21 — 316 сторінок (кожен компонент тричі: Radix, Base
UI, React Aria), сайт для Tailwind CSS v3 у 3.8 — 86, у 0.1 — 45; Radix Primitives у 1.7 — 43, Radix Themes у 3.3 — 70.
У текстах вставлено 5 220 прикладів і файлів компонентів — кодом, а не назвою.

Замір `quality`: перша десятка (питання своїми словами) — по словах 4 із 10, за змістом 5, разом 5; друга, «як модель»
(назви компонентів, пропсів і файлів, з версією, як велить промпт), — 10 із 10. Заміряно сітку `max_per_doc` 0–3 на
`fusion_depth` 0, 60, 120 і 200: з будь-якою `fusion_depth` гірше (разом 1–5, «як модель» 5–8). Без неї `max_per_doc`
1 і 2 дають разом 6 із 10 (додається сторінка форм), але видача стає неповною: на `sidebar` з k=10 приходить 8
фрагментів, на `select` — 6, бо обмеження на документ лишає менше, ніж просили. Тож обидва поля не стоять.

**Що пропускає пошук своїми словами.** «Змінити фірмові кольори всіх компонентів в одному місці» (theming), «анімація
появи й зникнення спливного вікна», «таблиця записів із сортуванням і сторінками», «свій елемент замість типового зі
збереженням поведінки». З назвами (`CSS variables --primary`, `data-state`, `useReactTable`, `asChild`), як велить
промпт, пошук знаходить потрібне.

**Повнота видачі.** На 20 пробних словах (`dialog`, `sidebar`, `asChild`, `radius`, `keyboard`…) видача на 5 і на 10
результатів повна.

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

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df shadcn <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| shadcn/ui | `shadcn-ui/ui`: останній патч кожної мінорної, `shadcn-ui@0.1.3` … `shadcn@4.21.4` | `ghdocs-history` |
| Radix Primitives | `radix-ui/website`: коміт 46f80eb0, коміти випусків `radix-ui` 1.1–1.6, `main` | `ghdocs-history` |
| Radix Themes | там само: коміти випусків 1.0, 1.1, 2.0, 3.0, 3.1, 3.2, `main` (3.3) | `ghdocs-history` |
| Radix Colors | там само: коміти випусків 0.1, 1.0, 2.0, 2.1, `main` (3.0) | `ghdocs-history` |

Білий список — `api.github.com` (дерева двох репозиторіїв) і `raw.githubusercontent.com`: у кожного джерела — лише його
теки на його тегах і комітах, для shadcn/ui ще теки реєстру (`apps/v4/examples`, `apps/v4/registry`,
`apps/www/registry`, `deprecated/www/registry`, `apps/www/components`), з яких сторінки вставляють код. Посилання у
відповідях ведуть на файл сторінки на GitHub на тезі чи коміті версії: сайти показують лише поточну.

Особливості, які варто знати:

- **Версія shadcn/ui — мінорна CLI.** Документація лежить у тому ж репозиторії, що й CLI, тож знімок — останній патч
  кожної мінорної (`shadcn@4.21.4` → «shadcn-4.21»). Версії 1.0 тегу немає — знімок узято з коміту випуску. Мінорної
  2.2 не випускали.
- **Два сайти shadcn/ui.** Сайт для Tailwind CSS v3 (`apps/www`, з 3.x — `deprecated/www`) до 2.5 був єдиним, а з 4.0
  його в репозиторії немає; поточний (`apps/v4`, Tailwind CSS v4) — з 2.6. Тому мітки «shadcn-tw3-…» і «shadcn-…»
  різні: та сама сторінка `components/dialog` на двох сайтах — два різні тексти.
- **Код замість назви.** Сторінка компонента показує приклади тегом `<ComponentPreview name="dialog-demo" />`, а сам
  компонент — `<ComponentSource name="dialog" />`; на сайті там живий приклад і код, а у файлі сторінки — лише назва.
  Поле `jsx_sources` читача бере файл прикладу з реєстру того самого тегу (шаблони шляхів — у `sources.json`: реєстр
  кілька разів переїжджав) і вставляє його блоком коду з назвою й описом прикладу.
- **Radix: файл на версію компонента.** До 23.01.2025 сайт Radix тримав окремий файл на кожну версію кожного компонента
  (`components/dialog/1.1.2.mdx`). Поле `path_version` бере мітку з шляху — «radix-dialog-1.1.2», а `slug_rewrite`
  зводить усі такі файли до однієї сторінки «radix-dialog», тож однаковий текст різних версій — один фрагмент. Після
  переходу на один пакет `radix-ui` сайт тримає одну редакцію, і знімки — коміти на мить випусків 1.1–1.7.
- **Таблиці API Radix.** Пропси, атрибути `data-*`, клавіші й змінні CSS на сайті — компоненти таблиць
  (`<PropsTable data={[…]}>`, `DataAttributesTable`, `KeyboardTable`, `CssVariablesTable`) з даними в JSX. Поле
  `jsx_props` читача розбирає їх у списки: «Props:» (`open` (boolean, default: false) — опис), «Data attributes:»,
  «Keyboard interactions:», «CSS variables:».
- **Ключі сторінок.** `slug_rewrite` у `config.json` прибирає службові частини шляхів: `shadcn-components-dialog`
  (варіант на Radix), `shadcn-components-base-dialog`, `shadcn-components-aria-dialog`, `shadcn-theming`,
  `shadcn-tw3-components-dialog`, `radix-dialog`, `radix-themes-components-button`, `radix-colors-overview-usage`.
  Сторінки Radix Colors 0.1 (`getting-started/…`, `the-scales`) зведено до сучасних імен.

## Версії у відповіді

| Що | Мітка | Фільтр `version` |
|----|-------|------------------|
| shadcn/ui, поточний сайт | «shadcn-4.21» … «shadcn-2.6» | «shadcn-4» — уся 4.x |
| shadcn/ui, сайт для Tailwind CSS v3 | «shadcn-tw3-3.8» … «shadcn-tw3-0.1» | «shadcn-tw3-3» — уся 3.x |
| Radix Primitives, пакет `radix-ui` | «radix-ui-1.7» … «radix-ui-1.1» | «radix-ui-1» — усі |
| Radix Primitives, пакет на компонент | «radix-dialog-1.1.2», «radix-dialog-0.1.7» | «radix-dialog-1» — 1.x Dialog |
| Radix Themes | «radix-themes-3.3» … «radix-themes-1.0» | «radix-themes-3» — уся 3.x |
| Radix Colors | «radix-colors-3.0» … «radix-colors-0.1» | «radix-colors-3.0» — лише вона |

Без названої версії відповідь — з поточного сайту («shadcn-4.21» і «radix-ui-1.7»). Проєкт на Tailwind CSS v3 — фільтр
за мажором CLI на сайті для v3; старі пакети `@radix-ui/react-*` — за компонентом і його мажором.

## Межі, про які треба пам'ятати

- **Таблиць пропсів Radix Themes немає.** Сайт будує їх із коду самої бібліотеки (`<ThemesPropsTable>`), у файлі
  сторінки даних немає. Опис, приклади й варіанти компонентів Themes — є.
- **Три приклади не знайдено** — їхніх файлів у реєстрі на тезі сторінки немає: `input-otp-form`, `native-select-form`,
  `native-select-input-group`. На їхньому місці лишилася назва.
- **Кілька вставок лишилися назвою файла**: допоміжні файли таблиці даних (`components/data-table-pagination`,
  `data-table-view-options`, `data-table-column-header`) лежать у демо-застосунку сайту (`app/(app)/examples`), поза
  теками реєстру з білого списку; `actions.ts` і `schema.ts` сторінок форм та `use-toast` старого сайту — файли `.ts`,
  а шаблони шукають `.tsx`.
- **Шкали Radix Colors** на сторінках палітр — малюнки (кольорові смуги); у тексті лишилися заголовки шкал і порожні
  дужки на місці малюнка.
- **Немає:** власної документації Base UI і React Aria (етапи 2 і 3), інших бібліотек компонентів (Material UI, Chakra,
  Mantine, Headless UI, Ark UI), блоків і шаблонів shadcn як коду сторінок. Сам Tailwind CSS — у примірнику `tailwind`,
  React Hook Form і zod — у своїх, React — у `react`.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку, як у nginx: у `corpus/` лежить лише паспорт `index.json`, а сервер
підіймається з кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає
повний текст кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/shadcn-corpus-2026-10-07.tar.gz` (2,8 МБ, 1 958 текстів і паспорт;
перед видаленням розпакований окремо й звірений із диском — нуль розбіжностей). В історії git текстів немає ніде.
Архів лежить лише на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/shadcn/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/shadcn-corpus-РРРР-ММ-ДД.tar.gz -C instances/shadcn corpus
find instances/shadcn/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/shadcn/index/passages.json > instances/shadcn/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/shadcn-corpus-РРРР-ММ-ДД.tar.gz -C instances/shadcn
./df shadcn smoke
```

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/shadcn/index/passages.json.gz`, далі
`./df shadcn vectors` заллє колекцію Qdrant (близько 50 хвилин).

## Установка venv

```
cd instances/shadcn
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df shadcn sources --why   # перелік джерел і білий список
./df shadcn refresh         # завантажити все задеклароване (~1,5 години)
./df shadcn manifest        # оновити паспорт
./df shadcn setup           # Qdrant чи пошук лише по словах
./df shadcn vectors         # залити корпус у docs-shadcn (~50 хвилин)
./df shadcn smoke           # перевірки
```

Дерев тегів і комітів тут понад сімдесят, а кожна сторінка компонента тягне файли прикладів, тож без `GITHUB_TOKEN` у
`.env` анонімного ліміту GitHub API (60 звернень на годину) не вистачить. Тексти йдуть з raw.githubusercontent.com, що
до ліміту не рахується. Обірваний `refresh` продовжується з `--missing`.

**Нова мінорна shadcn** (4.22): знімок не з'являється сам. Дописати тег `shadcn@4.22.x` у `tags` джерел `shadcn` і
`shadcn-tw3` з мітками «shadcn-4.22» і «shadcn-tw3-4.22» та адреси його тек у `within`. **Нова мінорна `radix-ui`,
Themes чи Colors**: коміт `radix-ui/website` на мить випуску — у `tags` свого джерела, мітку `main` підняти.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd /mnt/c/Projects/fwdays/docfactory
./df shadcn serve             # порт 8799
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8799/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user shadcn-docs http://127.0.0.1:8799/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `shadcn-docs` і два інструменти `search_docs`, `read_section`. Якщо сесію Claude
Code відкрито раніше, ніж піднято сервер, вона покаже його як недоступний: у `/mcp` виберіть сервер і «Reconnect».

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
