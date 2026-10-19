# Оновлення корпусу typeorm

Дві різні роботи: звичайне оновлення, коли вийшли нові стабільні версії TypeORM, і збирання з нуля. Порядок усередині
кожної важливіший за самі команди.

Головне правило: **оновлювач тягне лише оголошене.** Дерева й файли репозиторію typeorm/typeorm — лише тегів, що
перелічені в полі `tags` джерел, і лише в межах `within`; релізи — лише з адреси джерела `releases`; журнал — лише
`CHANGELOG.md` гілки `master`; версії й README — з реєстру npm. Нова версія сама в документацію не потрапить, доки її
тег не дописано в `tags`.

Друге правило: **лише стабільні версії.** У `tags` — тільки голі номери `X.Y.Z` (теги TypeORM без префікса `v`), без
бет (`v1.0.0-beta.3`) і без нічних збірок (`1.1.2-nightly.20261019`, їх у реєстрі npm понад тисячу); поле
`skip_versions` джерел npm відкидає все з дефісом за номером.

Третє правило: **тег визначає джерело.** Документація однієї версії лежить у репозиторії на її тезі, але в трьох
розкладках, і тег іде в джерело своєї:

| Версії | Розкладка | Джерело | Адреса в шапці |
|--------|-----------|---------|----------------|
| 1.0.0 і новіші | Docusaurus, `docs/docs/**`, `docs/blog/**` | `docs-v1` | сторінка typeorm.io |
| 0.3.25–0.3.x | Docusaurus, `docs/docs/**` | `docs-v0` | сторінка v0.typeorm.io |
| 0.1.0–0.3.24 | плоска тека `docs/*.md` | `docs-flat` | blob на GitHub |

Код і тести беруть **усі** стабільні теги: до 1.1.1 — `src/` і `test/` кореня, з 1.1.2 — `packages/typeorm/src` і
`packages/typeorm/test` монорепозиторію (поле `include` джерел `src` і `tests` знає обидва шляхи, `slug_rewrite`
зводить ключі). Codemod — з тегів 1.x (`codemod-src`), з міткою версії пакета з `packages/codemod/package.json`.

Четверте правило: **нова версія змінює й старі документи.** Документ сторінки чи файла коду — неповторна редакція, а в
рядку `# версія:` стоять усі версії, де вона була саме такою. Тож після нового тегу джерела перезаписуються цілком
(`refresh <джерело>` чи `build <джерело>`), а не докачуються (`--missing`).

П'яте правило: **нічого не видаляється.** Ані `refresh`, ані `build`, ані `manifest` нічого не стирають самі;
`vectors` прибирає лише точки власної колекції, чиїх фрагментів у корпусі вже немає.

**Спершу — повернути тексти.** Корпус примірника в архіві: у `corpus/` лежить лише паспорт, а `check`, `refresh`,
`build` і `manifest` працюють із файлами. Перед будь-якою роботою нижче тексти й сховище сирого розпаковують, а після
неї — пакують і виносять знову; обидві дії описані в [README, розділ «Архівний
режим»](README.md#архівний-режим-сервер-без-корпусу).

## 1. Вийшла нова стабільна версія

**Крок 1. Знайти версію.** Стабільні версії й час публікації — у реєстрі npm (`https://registry.npmjs.org/typeorm`,
поле `time`), теги — на `https://github.com/typeorm/typeorm/tags`.

**Крок 2. Теги.** `"1.1.3": "1.1.3"` — на початок поля `tags` джерел `docs-v1`, `src` і `tests` (для патча лінії 0.3 —
`docs-v0`, `src` і `tests`); для 1.x — ще й `codemod-src` з міткою `codemod-<версія з packages/codemod/package.json>`.
Нові сторінки сайту дістають адресу typeorm.io лише тоді, коли їх дописано в поле `site` джерела (перевірити, що
адреса відповідає 200); без цього в шапці стоїть blob на GitHub.

**Крок 3. Перейменовані сторінки.** Якщо тег переклав сторінки (`git diff -M --name-status <попередній> <новий> --
docs`), пари «старе ім'я → нове» дописують у `slug_rewrite` у `config.json` (ключ — ім'я документа без джерела й хеша:
`docs-docs-advanced-topics-3-indices` → `docs-docs-indexes`), інакше редакції однієї сторінки не зливаються.

**Крок 4. Завантажити.** Код і тести тисяч файлів мережею не тягнуть: `list` бере дерева тегів через API, голий
частковий клон кладе blob-и в сховище сирого, а `build` збирає без мережі.

```
./df typeorm sources --why
./df typeorm list > /dev/null
git clone --bare --filter=blob:none https://github.com/typeorm/typeorm.git /tmp/typeorm.git
instances/typeorm/.venv/bin/python tools/seed_git_store.py --instance typeorm --clone typeorm/typeorm=/tmp/typeorm.git
./df typeorm build src tests codemod-src
./df typeorm refresh docs-v1 docs-v0 readme-typeorm npm-typeorm npm-codemod readme-codemod changelog releases
./df typeorm manifest
./df typeorm vectors
./df typeorm smoke
# Ctrl+C у терміналі з serve, і знову: ./df typeorm serve
```

Названий `refresh` інших джерел не чіпає зовсім. Джерела `docs-flat` і `readme-typeorm-untagged` застигли: плоскої
теки `docs/` і версій без тегу більше не буде.

**Крок 5. Промпти.** Версії за замовчуванням (найпопулярніші за завантаженнями npm:
`https://api.npmjs.org/versions/typeorm/last-week`) записано в `prompts/search.txt` (абзац «Which version to answer
for») і `prompts/agent.txt`; межі версій — ще й у `prompts/loaded.txt`.

## 2. Сайт змінив розмітку

Якщо в тексті з'явилися службові рядки MDX (теги компонентів `<…>`, рядки `import`), правиться модуль
`engine/readers/ghtypeorm.py` (вкладки `<DatabaseTabs>` — поле `custom_tabs` джерел `docs-v1` і `docs-v0`). Правка
читача не вимагає нового завантаження: `./df typeorm build docs-v1 docs-v0` збирає тексти зі сховища сирого.

Корпус не комітиться: після оновлення пишуть новий архів і знову виносять тексти й сховище (README, розділ «Архівний
режим»), а в git ідуть лише паспорт і кеш. Старий архів видаляють, коли новий звірено з диском.

Якщо `smoke` скаржиться на число фрагментів — це наслідок того, що документація підросла. Нове число записують у
`checks.json` полем `expected_passages`, а в `expected_note` — коли й чому його знято.

## 3. Збирання з нуля

**Крок 1. Токен.** Покладіть `GITHUB_TOKEN=…` у `.env` цієї теки: дерев тегів 111, і анонімних 60 звернень на годину
не вистачить.

**Крок 2. Перелік, клон і код без мережі** — команди `list`, `git clone`, `seed_git_store.py` і `build src tests
codemod-src` з кроку 4 розділу 1: код і тести — 18 714 файлів за хвилину.

**Крок 3. Документація й решта мережею**, окремим процесом:

```
PYTHONUNBUFFERED=1 setsid nohup ./df typeorm refresh docs-v1 docs-v0 docs-flat readme-typeorm readme-typeorm-untagged npm-typeorm npm-codemod readme-codemod npm-legacy-naming-strategies readme-legacy-naming-strategies changelog releases > refresh.log 2>&1 < /dev/null &
```

Близько 14 хвилин: 1 045 документів. Обірваний прогін продовжують `./df typeorm refresh <джерело, де зупинився>`, далі
`refresh --missing`.

**Крок 4.** `manifest`, `vectors`, `smoke`, `quality`; далі — архів і винесення текстів.

Очікуваних збоїв `refresh` немає.
