# testcontainers-go — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про testcontainers-go (github.com/testcontainers/testcontainers-go) —
бібліотеку Go, що запускає з тестів тимчасові контейнери Docker: PostgreSQL для інтеграційних тестів, очікування
готовності, рядок з'єднання, скрипти ініціалізації, знімки бази між тестами, прибирання контейнерів, CI. Код спільний
і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

У плані Go ([../go/LEARNING.md](../go/LEARNING.md), фаза 5, дні 3–4) тести сховища й сценарії безпеки йдуть на
справжньому PostgreSQL: один контейнер на пакет у `TestMain`, міграції goose одразу після старту, чиста база на кожен
тест через знімок модуля postgres. API модулів змінився в 0.32 (`postgres.Run` замість `RunContainer`,
`testcontainers.Run`, `CleanupContainer`), і старі статті показують старий, тож документація лежить на кожну мінорну.

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Сайт golang.testcontainers.org | 305 | 44 | тека `docs/` і README з останнього тегу кожної мінорної 0.0–0.44; модулі postgres, redis, compose |
| Довідник ядра | 78 | 44 | pkg.go.dev: пакет `testcontainers`, `wait`, `network` |
| Довідник модуля postgres | 11 | 25 | pkg.go.dev, `modules/postgres` 0.20–0.44 |
| Релізи | 57 | 57 | GitHub Releases, лише стабільні |

Документів менше, ніж версій: текст, що не мінявся між мінорними, — один документ із переліком версій.

Разом 451 запис паспорта. В індексі 1914 фрагментів (`expected_passages` у `checks.json`) із 416 документів. Замір
`quality`: по словах 8 із 10, за змістом 9, разом 10, «як модель» 10 із 10. До запиту про адресу бази додано справжні
відповіді — розділи `ConnectionString` сторінки модуля postgres і «Getting the container host». Усі документи несуть
версію, тож перевірку smoke «пошук без версії бачить документи без версії» вимкнено (`expect_unversioned: false`).

Чого немає:

- Модулів, крім postgres, redis і compose (їх у testcontainers-go понад сімдесят).
- testcontainers для інших мов, Docker і PostgreSQL як таких (примірники `docker` і `postgresql`).

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа. Самих
  текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого підіймається сервер. У git лежить стиснений `passages.json.gz`; розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки будується корпус. Він же білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.mcp.json` — запис HTTP-сервера для Claude Code. `ANTHROPIC_API_KEY` (лише для кроку `ask`) і `GITHUB_TOKEN` (лише
  для завантаження корпусу) беруться з кореневого `.env`.

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df testcontainers-go <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт | дерева 44 тегів testcontainers/testcontainers-go (0.0.10–0.44.0): `docs/`, `README.md` | `ghdocs-history` |
| довідник ядра | pkg.go.dev, `github.com/testcontainers/testcontainers-go@vX.Y.Z`, `wait`, `network` | `pkgsite` (`versions`) |
| довідник postgres | pkg.go.dev, `.../modules/postgres@vX.Y.Z` (окремий модуль зі своїми тегами `modules/postgres/vX.Y.Z`) | `pkgsite` (`versions`) |
| релізи | api.github.com, `/repos/testcontainers/testcontainers-go/releases` | `ghreleases-stable` |

Поле `exclude` джерела `docs` лишає з теки `docs/modules` лише postgres, redis і compose; сторінки внесків, бонусів і
метрик використання не беруться. Цитуються сторінки golang.testcontainers.org/… (поле `site`), довідник — pkg.go.dev з
версією.

## Версії

Усе несе версію testcontainers-go (`0.44.0`). Фільтр `version` приймає мінор (`"0.44"`) або точну версію. Промпт
відповідає для 0.44.0 і нагадує про зміну API модулів у 0.32.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку. У `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant. Відповіді ті самі до символа, бо кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/testcontainers-go-corpus-2026-10-27.tar.gz` (451 текст, паспорт і
сховище сирого `raw/`; перед видаленням текстів архів розпаковано окремо й звірено з диском) і в копії на Windows
`C:\Distr\testcontainers-go-corpus-2026-10-27.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/testcontainers-go/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/testcontainers-go-corpus-РРРР-ММ-ДД.tar.gz -C instances/testcontainers-go corpus raw
find instances/testcontainers-go/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/testcontainers-go/raw
gzip -9 -c instances/testcontainers-go/index/passages.json > instances/testcontainers-go/index/passages.json.gz
```

Після цього закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Тексти й сховище видаляють лише тоді,
коли архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із текстами повертається сховище сирого:

```
tar -xzf ~/archives/docfactory/testcontainers-go-corpus-2026-10-27.tar.gz -C instances/testcontainers-go
./df testcontainers-go smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Їхні
перевірки `smoke` чесно пропускає з позначкою «корпус в архіві».

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/testcontainers-go/index/passages.json.gz`.
Далі `./df testcontainers-go vectors` заллє колекцію Qdrant: секунди на відеокарті, хвилина на процесорі.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df testcontainers-go …` бере спільне середовище з кореня репозиторію (`.venvs/cpu`
або `.venvs/gpu`). Як збудувати його один раз і як `df` обирає між ними — у кореневому README, розділ «Спільне
середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df testcontainers-go sources --why   # перелік джерел і білий список
./df testcontainers-go refresh         # завантажити все задеклароване (близько п'ятнадцяти хвилин)
./df testcontainers-go manifest        # оновити паспорт
./df testcontainers-go setup           # Qdrant чи пошук лише по словах
./df testcontainers-go vectors         # залити корпус у docs-testcontainers-go
./df testcontainers-go smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити його працювати:

```
cd ~/Projects/docfactory
./df testcontainers-go serve          # порт 8923
```

Сервер готовий, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8923/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user testcontainers-go-docs http://127.0.0.1:8923/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування. Вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell або додати сервер кнопкою «Add server» у вікні
`/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` має показати `testcontainers-go-docs` і два інструменти: `search_docs` і `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта (scope запису, «address already in use») — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).

