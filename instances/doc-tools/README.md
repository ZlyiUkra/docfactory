# doc-tools — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про файлові інструменти командного рядка й бібліотеки, якими
перевіряють, перетворюють і рендерять документи й зображення: poppler (`pdfinfo`, `pdftotext`, `pdftoppm`,
`pdftocairo`, `pdfimages` і решта poppler-utils), librsvg з `rsvg-convert`, `file` і libmagic, ImageMagick 6 і 7,
img2pdf, Ghostscript, qpdf і pikepdf, ExifTool, resvg і CairoSVG. До кожного — їхні обгортки для Node.js (npm) і
Python (PyPI) та сторінки man так, як їх ставить apt в Ubuntu 22.04, 24.04 і 26.04. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

Конвеєр «документ → PDF → зображення → текст» складається з десятка малих інструментів, і кожен документує себе
по-своєму: poppler — сторінками man у репозиторії на GitLab, `file` — сторінками mdoc, ImageMagick — сайтом, що жив у
теці `www/` самого репозиторію, Ghostscript — HTML до 9.56 і Sphinx з 10.0, qpdf — DocBook до 10.4 і Sphinx далі,
ExifTool — сайтом із таблицями тегів кожного формату. Версії на машинах різні: Ubuntu 22.04 і 24.04 ставлять
ImageMagick 6 (`convert`), 26.04 — ImageMagick 7 (`magick`), poppler 22.02, 24.02 чи 25.x. Тут кожен випуск — окремою
редакцією, і відповідь «чи є `-scale-to-x` у pdftoppm 0.20» береться з man-сторінки 0.20, а не з пам'яті. Поруч —
файли налаштувань, від яких залежить, чи перетворення взагалі дозволене: `policy.xml` ImageMagick (PDF, PS, SVG
«not authorized») і `delegates.xml` (через які програми ImageMagick читає PDF і SVG).

**Що свідомо окремо.** LibreOffice (`soffice --convert-to`) — примірник `libreoffice`. Tesseract і OCRmyPDF, MuPDF і
PyMuPDF, sharp і libvips, pandoc, бібліотеки PDF для JavaScript і Python (pdf.js, pdf-lib, pypdf, pdfplumber) —
кожна окремим примірником у черзі: кожен із цих наборів великий сам по собі.

## Скільки цього

| Інструмент | Документів | Фрагментів | Що взято |
|------------|-----------:|-----------:|----------|
| poppler | 543 | 3 714 | man 13 утиліт кожного стабільного випуску 0.5–26.10 (GitLab), NEWS, сайт, API glib/Qt5/Qt6/C++ |
| librsvg / rsvg-convert | 398 | 1 289 | man rsvg-convert 2.0–2.63, README, `doc/`, `devel-docs/`, заголовки C і Rust API, gi-docgen, NEWS |
| file / libmagic | 576 | 1 026 | file(1), magic(5), libmagic(3) 3.27–5.48, README, ChangeLog 5.18+, Magdir 5.48, прив'язки Python |
| ImageMagick 6 і 7 | 4 404 | 13 961 | сайт `www/` кожної лінії 7.0.1–7.1.2 і 6.9.4–6.9.13, чинний сайт, man, `config/*.xml`, ChangeLog |
| img2pdf | 65 | 289 | README, код із довідкою параметрів, CHANGES — 0.1.0–0.6.3 |
| Ghostscript | 3 879 | 10 629 | документація 6.0–9.56.1 (htm) і 10.0–10.08 (rst), News 10.x, man |
| qpdf | 687 | 2 112 | посібник DocBook 2.0–10.4 і Sphinx 10.5–12.4, man, ChangeLog до 11.10, заголовки C/C++ |
| pikepdf | 1 206 | 4 738 | документація кожного стабільного випуску, код і стаби `_core` з docstring |
| ExifTool | 2 560 | 14 262 | exiftool.org (тека `html/` із TagNames) кожного production release 9.76–13.59, Changes |
| resvg і CairoSVG | 378 | 831 | README, `docs/`, CHANGELOG, довідка CLI, C API resvg; сайт, NEWS і API CairoSVG |
| Обгортки npm з GitHub | 1 824 | 4 664 | node-poppler, file-type, exiftool-vendored, magick-wasm, resvg-js, gm: README, код, журнали |
| Обгортки PyPI з GitHub | 544 | 2 634 | pdf2image, Wand, python-magic, PyExifTool, python-poppler: документація й код |
| Реєстри npm і PyPI | 739 | 2 290 | таблиці версій і README кожної стабільної версії 12 пакетів npm і 11 PyPI |
| Ubuntu man | 160 | 1 143 | сторінки всіх інструментів у 22.04, 24.04, 26.04 (manpages.ubuntu.com) |

Разом 17 963 документи; фрагментів — 63 582 (`expected_passages` у `checks.json`): однакові тексти сусідніх випусків
злито в один фрагмент з усіма версіями. Замір `quality` (10 запитів): по словах 9, за змістом 7, разом 10.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (109 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df doc-tools <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| man poppler з gitlab.freedesktop.org | `gitlab-history` (новий) |
| сайти в HTML з тегів: ImageMagick `www/`, Ghostscript `doc/*.htm`, ExifTool `html/`, чинний сайт ImageMagick | `ghdocs-history-html` (новий) |
| NEWS, ChangeLog, CHANGES, Changes, CHANGELOG будь-якого формату | `changelog-regex` (новий) |
| man у roff і mdoc з тегів (`rsvg-convert.1`, `file.man`, `utilities/*.1`, `man/*.1`) | `ghdocs-history-roff` (доповнено) |
| посібник qpdf до 10.4 | `docbook-gh` |
| markdown і Sphinx з тегів (librsvg, Ghostscript 10, qpdf, pikepdf, Wand, обгортки) | `ghdocs-history` |
| код і заголовки | `ghcode-history`, `ghcode-history-ts` |
| API poppler, gi-docgen librsvg, сайт poppler | `html-pages` (доповнено полем `heading`) |
| npm, PyPI | `npm-versions`, `npm-tarball-files`, `pypi-versions` |
| Ubuntu | `ubuntu-man` |
| релізи file-type | `ghreleases-stable` |

Нове в спільному коді:

- **`gitlab-history`.** Poppler живе на GitLab freedesktop, дзеркала на GitHub у нього немає. Читач бере теки
  (`utils`) з кожного тегу через API GitLab за числовим id проєкту, документ — неповторна пара «шлях, blob», як у
  `ghdocs-history`; тег, де теки ще немає (poppler до 0.5), просто нічого не дає.
- **`ghdocs-history-html`.** Обгортка над `ghdocs-history`, що перед розбором перетворює HTML на markdown: поля
  `start`/`end` — де текст сторінки починається й закінчується (меню й підвал різні в кожній епосі сайту ImageMagick),
  `drop` — що вирізати (реклама, скрипти, іконки SVG), `title_strip` — що зрізати з назви. Сторінка Jekyll із шапкою
  YAML (чинний сайт ImageMagick) бере назву з шапки.
- **`changelog-regex`.** Десяток журналів пишуть запис по-своєму («Release 26.10.0:», «* release 5.46»,
  «Oct. 10, 2026 - Version 13.40», «## [7.1.2-34] - 2026-10-14» з посиланням на порівняння тегів), тож формат —
  вираз у `sources.json` з групами `v` і `d`, а простий текст стає markdown (спільний відступ знімається, пункти «*»
  — «- »).
- **mdoc у `ghdocs-history-roff`.** Сторінки `file` написано в mdoc (`.Nm`, `.Fl`, `.Bl -tag`), а не в man(7): новий
  перетворювач `_mdoc`. Опція розділу OPTIONS стає власним підрозділом («### `-i`, `--mime`»): сорок опцій одним
  фрагментом пошук не розрізняв, і `--mime-type` не знаходився. Поля `roff_match` (файли `.man`) і `substitute`
  (заглушки збирання `__CSECTION__`, `__MAGIC__`).
- **`html-pages`** дістав поле `heading` — вираз назви сторінки замість `<h1>`: gtk-doc і Doxygen пишуть назву в
  `<h2>` чи `<div class="title">`. **`refuse_html`** відхиляє лише справжній HTML: `delegates.xml.in` ImageMagick
  починається з `<!DOCTYPE delegatemap` і раніше вважався сторінкою помилки. **`ghcode`**: `.pyi` — Python (стаби
  pikepdf діляться на класи й методи), `.hh` — C++.

Особливості:

- **Мітки версій — з назвою інструмента**: `poppler-26.10.0`, `imagemagick-7.1.1-47`, `ghostscript-9.56.1`,
  `file-5.48`, `qpdf-12.4.2`, `exiftool-13.59`, обгортки — з назвою пакета (`node-poppler-11.0.0`, `wand-0.7.2`),
  сторінки Ubuntu — випуском (`ubuntu-24.04`). Інакше `version: "10.0"` змішав би Ghostscript 10.0 з qpdf 10.0.
- **Стабільні випуски.** poppler — без непарних мінорних 0.7–0.25 (серії розробки); librsvg — без непарних мінорних до
  2.54 і без x.y.90+; ExifTool — production releases з `Changes` і найновіший; решта — без rc, beta, alpha.
- **ImageMagick: лінії, а не кожен тег.** Сайт `www/` міняється раз на кілька випусків, тож береться останній тег
  кожної лінії (7.0.1…7.1.2, 6.9.4…6.9.13). 7.1.2-28 і 6.9.13-53 замінили `www/` віддзеркаленням нового сайту, тож для
  цих ліній узято теги перед тим; чинний сайт — з репозиторію ImageMagick/Website. Doxygen Magick++ не взято.
- **Ghostscript.** До 9.56.1 — `doc/*.htm` (і `gs/doc/` у старих тегах), з 10.0 — `doc/src/*.rst`. Величезні
  `History*.htm` (до 8 МБ журналу комітів) не взято.

## Межі, про які треба пам'ятати

- API poppler (glib, Qt5, Qt6, C++) — лише чинний стан сайту, без версій: сайт будується з master.
- README pdf-poppler не взято: tarball пакета з вкладеними бінарниками poppler більший за 50 МБ; таблиця версій є.
- Код ядер на C і C++ (poppler, ImageMagick, Ghostscript) не взято — лише документацію, заголовки qpdf і librsvg.
- `magick-wasm` — код лише найновішого випуску: `magick-image.ts` — 190 КБ на кожен із 44 випусків.
- exiftool-vendored — код останнього випуску кожної мажорної лінії, без згенерованого `Tags.ts` (532 КБ).
- darwinsys.com (сайт file) на час збирання не відповідав; змісту там — одна сторінка посилань.

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/doc-tools-corpus-2026-10-18.tar.gz` (17 963 тексти, паспорт і сховище
сирого `raw/`; перед видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/doc-tools-corpus-РРРР-ММ-ДД.tar.gz -C instances/doc-tools corpus raw
find instances/doc-tools/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/doc-tools/raw
gzip -9 -c instances/doc-tools/index/passages.json > instances/doc-tools/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/doc-tools-corpus-2026-10-18.tar.gz -C instances/doc-tools
./df doc-tools smoke
```

**Оновлення.** Новий випуск дописують першим рядком у `tags` (чи `refs`) відповідних джерел — тег і мітку з назвою
інструмента («"poppler-26.11.0": "poppler-26.11.0"»); журнали змін читаються з найновішого тегу, тож у їхній
адресі міняють тег. npm, PyPI, релізи file-type, Ubuntu man і чинний сайт ImageMagick підхоплюються самі. Далі
`./df doc-tools refresh`, `manifest`, `vectors`, `smoke`, `quality`.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df doc-tools …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md,
розділ «Спільне середовище». Свій `.env` примірник тримає в `instances/doc-tools/.env` (`cp .env.example .env`;
для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`, береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df doc-tools sources --why   # перелік джерел і білий список
./df doc-tools refresh         # завантажити все задеклароване (близько 2 годин)
./df doc-tools manifest        # оновити паспорт
./df doc-tools setup           # Qdrant чи пошук лише по словах
./df doc-tools vectors         # залити корпус у docs-doc-tools (близько 2,5 години)
./df doc-tools smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df doc-tools serve          # порт 8857
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8857/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user doc-tools-docs http://127.0.0.1:8857/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `doc-tools-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера.
