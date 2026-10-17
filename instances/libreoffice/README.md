# libreoffice — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про LibreOffice — офісний пакет (Writer, Calc, Impress, Draw, Math,
Base) і конвертер документів без вікна (`soffice --headless --convert-to`). Документація — уся англійська довідка
help.libreoffice.org для кінцевого випуску кожної лінії 3.3–26.8, текст `soffice --help` кожної лінії, оголошення
кожного фільтра імпорту й експорту та кожного типу файла, довідник UNO API (те, з чого генерується
api.libreoffice.org), посібник розробника (Developer's Guide), release notes, бюлетені безпеки, а також обгортки
для конвертації: libreoffice-convert і libreoffice-file-converter (npm), unoserver і unoconv (PyPI) — README кожної
версії, код, тести й журнали змін. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

LibreOffice часто працює не як редактор, а як сервіс: `soffice --headless --convert-to pdf` у контейнері, окремий
профіль користувача `-env:UserInstallation` для паралельних конвертацій, назва фільтра (`writer_pdf_Export`,
`"Text - txt - csv (StarCalc)"`) і рядок його параметрів (`44,34,76,1`, JSON для PDF). Усе це розкидано: ключі —
у довідці й у тексті `soffice --help`, точні назви фільтрів — в оголошеннях фільтрів у коді, параметри CSV і PDF —
на окремих сторінках довідки, які з'явилися не в усіх лініях, а доступ з коду — в UNO API й посібнику розробника.
Тут усе разом і за лініями: відповідь «чи є `--convert-to` з параметрами фільтра в 7.0» береться з довідки 7.0, а не
з пам'яті.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Довідка help.libreoffice.org | 28 905 | 40 526 | `LibreOffice/help`, кінцевий тег кожної з 32 ліній 3.3–26.8 |
| UNO API: IDL offapi і udkapi | 30 523 | 33 624 | `LibreOffice/core`, ті самі лінії |
| Фільтри й типи файлів | 2 096 | 1 530 | `LibreOffice/core`, `filter/source/config/fragments` |
| `soffice --help` | 24 | 31 | `LibreOffice/core`, `desktop/source/app/cmdlinehelp.cxx` |
| Developer's Guide | 25 | 3 130 | wiki.documentfoundation.org, `Documentation/DevGuide` |
| Release notes 3.4–26.8 і перелік можливостей 3.3 | 32 | 1 373 | wiki.documentfoundation.org |
| Бюлетені безпеки | 1 | 99 | libreoffice.org/security, CVE на розділ |
| Обгортки: npm, PyPI, код, тести, журнали | 380 | 867 | npm, PyPI, GitHub чотирьох репозиторіїв |

Разом 61 986 документів; фрагментів — 81 180 (`expected_passages` у `checks.json`): однакові тексти редакцій злито.
Замір `quality` (10 запитів): по словах 10, за змістом 9, разом 10.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (20 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df libreoffice <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| довідка | `ghdocs-history-xhp` (новий) |
| UNO IDL, фільтри й типи, `soffice --help` | `ghcode-history-lo` (новий) |
| Developer's Guide, release notes | `mediawiki-render` (новий) |
| бюлетені безпеки | `html-details` (новий) |
| код і тести обгорток, журнали, man-сторінка unoconv | `ghcode-history` |
| нотатки релізів libreoffice-file-converter | `ghreleases` |
| npm: таблиці версій і README; PyPI | `npm-versions`, `npm-tarball-files`, `pypi-versions` |

Нове в спільному коді:

- **Читач `ghdocs-history-xhp`** (розбір розмітки — `_xhp`). Сторінка довідки — XML `helpdocument`, а не markdown:
  заголовки (`<h1>` у нових файлах, `<paragraph role="heading">` у 3.x–5.x), абзаци коду, примітки, таблиці, списки.
  Сторінки вставляють розділи інших сторінок (`<embed>`, `<embedvar>`): без вставок у функцій Calc не було б
  розділів «Syntax» і «Example», а в таблицях — назв колонок. Вставки беруться з того самого тегу, і редакція
  сторінки враховує відбитки вставлених елементів, а не цілих файлів: файл-збірник рядків меню міняється з кожним
  випуском, а вставлений рядок — рідко. Варіанти для систем (`<switch select="sys">`) і програм підписано («On
  Windows:», «Ctrl (macOS: Command)»), терміни покажчика довідки («parameters;command line») стоять рядком «Index:»
  під найближчим заголовком. Посилання для ліній 6.0–26.8 ведуть на help.libreoffice.org, для 3.3–5.4 (їх сайт уже
  не тримає) — на GitHub.
- **Читач `ghcode-history-lo`.** Дерево `LibreOffice/core` цілком GitHub віддає обрізаним, тож дерева беруться
  потеково (`тег:тека`). Файл IDL ділиться на розділ на кожен член — метод, атрибут, властивість, поле, значення
  переліку, константу — з описом з коментаря (`@param`, `@returns`, `@throws`, `@since` підписами) й оголошенням.
  Фрагмент фільтра стає реченням «назва для `--convert-to` і `--infilter`, напрям, тип файла, служба документа» і
  таблицею всіх властивостей; `cmdlinehelp.cxx` — текстом, який друкує `soffice --help`, з розділами за рубриками.
- **Читач `mediawiki-render`** бере сторінки вікі через `?action=render`: шаблони вже розгорнуто, меню й посилань
  «edit» немає; навігацію версій нагорі відрізає поле `start`. **Читач `html-details`** — сторінка, де кожен запис —
  `<details><summary>`: кожен CVE стає розділом.
- **`tools/seed_git_store.py`** знає обидва нові читачі, а `--trees` кладе ще й дерева тегів для
  `ghdocs-history-xhp`: той читає сторінки вже під час переліку, і `list` тягнув би кожну мережею.

Особливості:

- **Мітки версій.** LibreOffice — лінією (`26.8`, `26.2`, `7.6`, `3.3`; з 2024 року лінії нумеруються роком і
  місяцем), обгортки — з назвою (`libreoffice-convert-1.8.2`, `libreoffice-file-converter-3.3.0`, `unoserver-3.7`,
  `unoconv-0.9.0`). Бюлетені безпеки, Developer's Guide і перелік можливостей 3.3 версій не мають. Без названої
  версії відповідь — для 26.8 («fresh»), з приміткою, де інакше 26.2 («still», лінія для обережних).
- **Тег лінії.** Кінцевий тег кожної лінії (`libreoffice-26.2.7.1`), без `x.y.99.z` — так позначено передрелізи
  наступної лінії. У `LibreOffice/core` лінія 3.4 закінчується тегом `libreoffice-3.4.2.3`, у `LibreOffice/help` —
  `libreoffice-3.4.6.2`.
- **ReleaseNotes/3.3** лише посилається на перелік можливостей 3.3 — береться він.
- **Запити `quality`** записано так, як їх ставить модель: назва з документації, далі опис.

## Межі, про які треба пам'ятати

- Довідка — англійська; переклади живуть в іншому репозиторії й не взяті.
- Посібники Getting Started, Writer, Calc… (books.libreoffice.org) не взято: вони про роботу в редакторах.
- UNO API — файли IDL, з яких генерується api.libreoffice.org; самі сторінки Doxygen і довідник C++
  (docs.libreoffice.org) не взято. Посилання IDL ведуть на GitHub.
- Сім файлів IDL без жодного тексту (лише `#include` чи порожній модуль) документами не стали.
- Docker-образи й Gotenberg — не тут.

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/libreoffice-corpus-2026-10-17.tar.gz` (61 986 текстів, паспорт і
сховище сирого `raw/`; перед видаленням розпакований окремо й звірений з диском). Лише на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/libreoffice-corpus-РРРР-ММ-ДД.tar.gz -C instances/libreoffice corpus raw
find instances/libreoffice/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/libreoffice/raw
gzip -9 -c instances/libreoffice/index/passages.json > instances/libreoffice/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/libreoffice-corpus-2026-10-17.tar.gz -C instances/libreoffice
./df libreoffice smoke
```

**Оновлення.** Нова лінія — першим рядком у `tags` джерел `help` і трьох джерел `core` (`soffice-help`, `filters`,
`uno-api`) («"libreoffice-27.2.1.2": "27.2"»), нова латка — заміною тегу лінії; сторінка `ReleaseNotes/<лінія>` —
у `pages` джерела `release-notes`; новий тег обгорток — у `tags` їхніх джерел коду. Довідку й `core` не тягнуть
мережею: голий клон `LibreOffice/help` (~530 МБ) і частковий клон потрібних тегів `LibreOffice/core` (лише дерева,
~35 МБ), далі засів сховища:

```
git clone --bare https://github.com/LibreOffice/help.git /tmp/help.git
git init --bare /tmp/core.git && git --git-dir /tmp/core.git remote add origin https://github.com/LibreOffice/core.git
git --git-dir /tmp/core.git config remote.origin.promisor true
git --git-dir /tmp/core.git config remote.origin.partialclonefilter blob:none
git --git-dir /tmp/core.git fetch --depth=1 --filter=blob:none --no-tags origin refs/tags/<тег>:refs/tags/<тег> …
./df libreoffice list soffice-help filters uno-api     # дерева core через API
instances/libreoffice/.venv/bin/python tools/seed_git_store.py --instance libreoffice --trees \
    --clone LibreOffice/help=/tmp/help.git --clone LibreOffice/core=/tmp/core.git
./df libreoffice build help soffice-help filters uno-api
./df libreoffice refresh release-notes release-notes-3-3 devguide security npm-libreoffice-convert …
```

Далі `manifest`, `vectors`, `smoke`, `quality`.

## Установка venv

```
cd instances/libreoffice
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
./df libreoffice sources --why   # перелік джерел і білий список
./df libreoffice manifest        # оновити паспорт
./df libreoffice setup           # Qdrant чи пошук лише по словах
./df libreoffice vectors         # залити корпус у docs-libreoffice (близько 2 годин)
./df libreoffice smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df libreoffice serve          # порт 8856
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8856/mcp`. Якщо порт зайнятий,
сервер скаже про це й вийде: значить, `serve` цього примірника вже десь запущений.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user libreoffice-docs http://127.0.0.1:8856/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Для проєкту в цій теці досить `.mcp.json`.

**3. Перевірити.** `/mcp` — має бути `libreoffice-docs` і два інструменти `search_docs`, `read_section`. Якщо сервер
у списку «failed», найчастіше `serve` просто не запущений.

Зупинка — Ctrl+C у терміналі сервера.
