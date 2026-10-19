# tesseract — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Tesseract OCR — рушій розпізнавання тексту на зображеннях
(командний рядок `tesseract`, C++ API `TessBaseAPI` і C API, мовні моделі tessdata, навчання й донавчання LSTM) — і про
обгортки над ним: OCRmyPDF (текстовий шар для сканів PDF через Tesseract, Ghostscript і pikepdf), tesseract.js
(Tesseract у WebAssembly для браузера й Node), pytesseract і tesserocr (Python), node-tesseract-ocr (Node).
Документація — сайт tesseract-ocr.github.io/tessdoc цілком, а для кожного стабільного випуску tesseract 1.03–5.5.3 —
сторінки man, README, публічні заголовки API, файли конфігурацій, ChangeLog і релізи; tesstrain і README репозиторіїв
tessdata; для кожного стабільного випуску обгорток — документація, код API, нотатки випусків, README з npm і PyPI.
Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Tesseract живе на машинах у різних версіях: Ubuntu 22.04 ставить 4.1.1, 24.04 — 5.3.4, а з джерел збирають 5.5.x.
Між ними мінялися опції й поведінка: `--oem` і рушій LSTM прийшли в 4.0, параметри виводу (TSV, ALTO, PAGE) додавалися
від версії до версії, мовні моделі поділилися на tessdata, tessdata_best і tessdata_fast. Сайт tessdoc показує лише
поточний стан, тож відповідь «що робить `--psm 13` у 4.1» береться зі сторінки man 4.1, а не з пам'яті. Обгортки лежать
поруч із самим рушієм, бо питання про них — це питання про Tesseract: `--psm` і `-l ukr` в OCRmyPDF, tesseract.js чи
pytesseract передаються тому самому `tesseract`. OCRmyPDF до того ж зв'язує Tesseract з Ghostscript і pikepdf з
примірника doc-tools — тут його документація повна, там її немає.

## Скільки цього

| Шар | Документів | Фрагментів | Звідки |
|-----|-----------:|-----------:|--------|
| Сайт tessdoc (зокрема навчання 3.x, 4.x, 5.x) і приклади C++ API | 61 | 718 | `tesseract-ocr/tessdoc`, знімок `main` |
| Сторінки man (AsciiDoc): tesseract(1), утиліти навчання, формати | 86 | 540 | `tesseract-ocr/tesseract`, 28 тегів 3.00–5.5.3 |
| Публічні заголовки C/C++ API (розділ на оголошення) | 145 | 829 | 35 тегів 1.03–5.5.3 |
| README, INSTALL.GIT, CONTRIBUTING, SECURITY; старі README, ReleaseNotes, NEWS | 61 | 115 | ті самі теги |
| Конфігурації `tessdata/configs` (`tsv`, `hocr`, `pdf`, `alto`…) | 124 | 121 | ті самі теги |
| ChangeLog 1.0–5.5.0 і релізи GitHub | 57 | 83 | файл журналу, GitHub Releases |
| tesstrain: README, Makefile, скрипти; README tessdata, tessdata_best, tessdata_fast | 33 | 99 | знімки `main` і теги |
| OCRmyPDF: сайт ocrmypdf.readthedocs.io, README, нотатки випусків | 493 | 1 445 | `ocrmypdf/OCRmyPDF`, 256 тегів v3.0–v17.13.0 |
| OCRmyPDF: API `ocrmypdf.ocr()`, плагіни, аргументи CLI; таблиця версій PyPI | 291 | 846 | ті самі теги, PyPI |
| tesseract.js: `docs/`, типи, константи, приклади, релізи | 153 | 351 | `naptha/tesseract.js`, 59 тегів 0.1.0–7.0.0 |
| tesseract.js і tesseract.js-core: README і таблиці версій npm | 66 | 203 | реєстр npm |
| pytesseract, tesserocr: код модуля, опис і таблиця версій PyPI | 77 | 317 | 30 і 25 тегів, PyPI |
| node-tesseract-ocr: код, README і таблиця версій npm | 15 | 37 | 3 теги, реєстр npm |

Разом 1 662 документи, 5 704 фрагменти (`expected_passages` у `checks.json`). Замір `quality` (10 запитів, серед них
обов'язкові для проєкту користувача: CLI, вихід TSV, `--psm` і `--oem`, мова `ukr`, `OMP_THREAD_LIMIT`): по словах 8,
за змістом 10, разом 10. `fusion_depth` 10 узято з ollama і не міряно: замір одразу дав 10 з 10.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (33 джерела), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df tesseract <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| сайт tessdoc, README, tesstrain, README tessdata, тека `docs/` tesseract.js | `ghdocs-history` |
| сторінки man `doc/*.asc` | `ghdocs-history-asciidoc` (новий) |
| сайт OCRmyPDF (rST до 15-ї версії, MyST з 16-ї) і нотатки випусків | `ghdocs-history-myst` (новий), поле `sphinx` |
| ChangeLog | `changelog-tesseract` (новий) |
| заголовки API, конфігурації, код Python і Cython | `ghcode-history` (`outline`) |
| типи й приклади tesseract.js, код node-tesseract-ocr | `ghcode-history-ts` |
| релізи | `ghreleases`, `ghreleases-stable` |
| npm і PyPI | `npm-versions`, `npm-tarball-files`, `pypi-versions` |

Особливості:

- **Сторінки man в AsciiDoc.** Заголовки підкресленням, списки означень `'FILE'::`, буквальні блоки `....`, `[verse]`,
  перехресні посилання `<<LANGUAGES,…>>` стають markdown. Кожен термін списку означень — опція (`--psm N`, `--oem N`),
  параметр (`tessedit_create_tsv`, `tessedit_char_whitelist`), мова (`ukr`) чи змінна (`OMP_THREAD_LIMIT`) — стає
  підрозділом: поки опції були жирними рядками всередині довгого «OPTIONS», поділеного за довжиною, запит про `--oem`
  його не знаходив (замір 9 з 10). Тип і змовчання параметра (`(bool, default: 0) [Both]`) — першим рядком тексту, не
  в заголовку, щоб ключ розділу не мінявся разом зі змовчанням.
- **OCRmyPDF у MyST.** З 16-ї версії сайт написано в MyST Markdown: `:::{note}`, `:::{list-table}`,
  `:::{versionadded}`, вставки ```` ```{eval-rst} ````, ролі `` {issue}`1234` ``. Читач розгортає їх у текст, таблиці й
  підписи; вставки rST іде тим самим розбором Sphinx, що й сторінки `.rst` старих тегів. Нотатки випусків узято зі
  знімка найновішого тегу (`docs/releasenotes/version02.md`…`version17.md` тримають усю історію); копію
  `release_notes.rst` у кожному тезі виключено.
- **ChangeLog.** З 5.5.1 файл у репозиторії — заглушка з посиланням на коміт `64eab6c`; журнал 1.0–5.5.0 узято з нього,
  пізніші зміни дають релізи GitHub. Передрелізи (`5.4.0-rc2`, `3.03(rc1)`) пропущено.
- **Мітки версій.** Tesseract — числом (`5.5.3`, `3.05.02`), обгортки — з назвою пакета (`ocrmypdf-17.13.0`,
  `tesseract.js-7.0.0`, `tesseract.js-core-6.1.2`, `pytesseract-0.3.13`, `tesserocr-2.11.0`, `node-tesseract-ocr-2.2.1`),
  `tesstrain-1.0.0`. Лінії мінорні (`version_line_depth: 2`). Сайт tessdoc, знімки `main` tesstrain і tessdata версій
  не мають. Без названої версії — найновіша: tesseract.js 7 бере 69 % тижневих завантажень npm.
- **Назви сторінок обгорток.** Сторінки OCRmyPDF і tesseract.js дістають назву продукту (`OCRmyPDF: Advanced
  features`, `tesseract.js: API`): назва йде в контекст кожного фрагмента, і «Advanced features» OCRmyPDF не плутається
  з однойменними розділами Tesseract.
- **Конфігурації.** Файли `tessdata/configs/*` лежать у репозиторії tesseract і встановлюються разом із ним; у
  репозиторіях tessdata це лише підмодулі, тож джерело бере їх з тегів tesseract.

## Межі, про які треба пам'ятати

- Лише стабільні випуски: 34 передрелізні й службові теги tesseract (rc, alpha, beta, dev, `1.04b`) не взято.
- Самі моделі `.traineddata` (гігабайти) і словники `langdata_lstm` не взято: є README репозиторіїв і перелік мов і
  скриптів на сайті й у man.
- Довідник tessapi (Doxygen) окремо не взято: він генерується з тих самих заголовків, що лежать тут з коментарями.
- Leptonica, Ghostscript, pikepdf, unpaper і jbig2 — лише в межах того, що про них каже документація OCRmyPDF і
  Tesseract; Ghostscript, qpdf і pikepdf мають власну документацію в примірнику doc-tools.
- README tesseract.js 1.0.0 (лише заголовок) і 1.0.9 (tarball реєстр не віддає) пропущено.

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/tesseract-corpus-2026-10-17.tar.gz` (364 МБ: 1 662 тексти, паспорт і
сховище сирого `raw/`; перед видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на цій
машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/tesseract-corpus-РРРР-ММ-ДД.tar.gz -C instances/tesseract corpus raw
find instances/tesseract/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/tesseract/raw
gzip -9 -c instances/tesseract/index/passages.json > instances/tesseract/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/tesseract-corpus-2026-10-17.tar.gz -C instances/tesseract
./df tesseract smoke
```

**Оновлення.** Новий випуск tesseract дописують першим рядком у `tags` джерел `man`, `readme`, `text`, `api`,
`tessdata-configs` («"5.5.4": "5.5.4"»), випуск OCRmyPDF — у `ocrmypdf-docs`, `ocrmypdf-readme`, `ocrmypdf-code`
(«"v17.14.0": "ocrmypdf-17.14.0"») і переносять ключ `ocrmypdf-releasenotes` на новий тег; випуск tesseract.js — у
`tjs-docs` і `tjs-code`, pytesseract і tesserocr — у їхні джерела коду. Сайт tessdoc, tesstrain і tessdata — новий
SHA гілки `main` замість старого. Релізи, npm і PyPI підхоплюються самі. Далі `./df tesseract list`, `refresh`,
`manifest`, `vectors`, `smoke`, `quality`.

Код і документацію з тегів швидше брати з голих клонів, ніж мережею: `git clone --bare --filter=blob:none` кожного
репозиторію, `./df tesseract list`, потім `tools/seed_git_store.py --instance tesseract --clone власник/репо=шлях …`,
`./df tesseract build` для засіяних джерел і `refresh` для решти (man, сайт OCRmyPDF, ChangeLog, релізи, npm, PyPI).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df tesseract …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md,
розділ «Спільне середовище». Свій `.env` примірник тримає в `instances/tesseract/.env` (`cp .env.example .env`;
для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`, береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають. Для роботи сервера збирати нічого не
треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df tesseract sources --why   # перелік джерел і білий список
./df tesseract refresh         # завантажити все задеклароване
./df tesseract manifest        # оновити паспорт
./df tesseract setup           # Qdrant чи пошук лише по словах
./df tesseract vectors         # залити корпус у docs-tesseract (близько 15 хвилин)
./df tesseract smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df tesseract serve          # порт 8858
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8858/mcp`. Якщо порт зайнятий,
сервер скаже про це й вийде: значить, `serve` цього примірника вже десь запущений; хто тримає порт, покаже
`ss -ltnp | grep 8858`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user tesseract-docs http://127.0.0.1:8858/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Замість запису на рівні користувача можна відкрити Claude Code у цій теці:
`.mcp.json` тут уже називає сервер.

**3. Перевірити.** `/mcp` — має бути `tesseract-docs` і два інструменти `search_docs`, `read_section`. Якщо там
«failed / not connected» — майже завжди сервер не піднятий (крок 1) або адреса не збігається з полем `port` у
`config.json`.

Зупинка — Ctrl+C у терміналі сервера.
