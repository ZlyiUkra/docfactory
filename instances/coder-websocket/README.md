# coder-websocket — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про coder/websocket (github.com/coder/websocket, раніше
nhooyr.io/websocket) — мінімальну бібліотеку WebSocket для Go поверх `net/http` і `context`: `Accept` у звичайному
обробнику, перевірка `Origin`, читання й запис з контекстом, JSON через `wsjson`, ping, коди закриття. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

У плані Go ([../go/LEARNING.md](../go/LEARNING.md), фаза 7) живі ціни йдуть звичайним WebSocket на `/api/ws` через
coder/websocket: хаб із кімнатами, вхід у з'єднанні, відключення повільних клієнтів, одне з'єднання з біржею. Приклад
`chat` бібліотеки — саме та схема хаба з буферизованим каналом на підписника, яку будує план. Документація — README
і коментарі коду на pkg.go.dev; у 1.8.12 модуль переїхав з `nhooyr.io/websocket` на `github.com/coder/websocket`, і
в чужому коді трапляються обидва шляхи імпорту.

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| README і README прикладів | 14 | 11 | з останнього тегу кожної мінорної 0.1–1.8 |
| Довідник `github.com/coder/websocket` | 2 | 1 | pkg.go.dev 1.8.15: пакет `websocket` і `wsjson` |
| Довідник `nhooyr.io/websocket` | 13 | 9 | pkg.go.dev, старий шлях модуля, 1.0–1.8 |
| Код прикладів | 8 | — | `internal/examples/` (chat, echo) і `example_test.go` гілки master |
| Релізи | 41 | 41 | GitHub Releases, лише стабільні |

Разом 78 записів паспорта. В індексі 280 фрагментів (`expected_passages` у `checks.json`) із 78 документів. Замір
`quality`: по словах 8 із 10, за змістом 9, разом 9, «як модель» 10 із 10. Кожна ціль має пару — той самий розділ
довідника за старим шляхом `nhooyr.io/websocket`: це та сама бібліотека, і пошук законно приносить будь-який із двох.
Промах першої десятки — «перевірити, що другий бік живий»: документація каже це методом `Ping`, а видача своїми
словами приносить сторінки про закриття.

Чого немає:

- Протоколу WebSocket (RFC 6455) і браузерного API — вони в примірниках `webstandards` і `mdn`.
- gorilla/websocket, gobwas/ws і socket.io — лише порівняння в README.

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

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df coder-websocket <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| README | дерева 11 тегів coder/websocket (0.1.0–1.8.15): `README.md`, `internal/examples/` | `ghdocs-history` |
| довідник | pkg.go.dev: `github.com/coder/websocket@v1.8.15` і `nhooyr.io/websocket@vX.Y.Z` (1.0.0–1.8.11) | `pkgsite` (`versions`) |
| код прикладів | `internal/examples/`, `example_test.go` гілки master | `ghcode` |
| релізи | api.github.com, `/repos/coder/websocket/releases` | `ghreleases-stable` |

## Версії

README, довідник і релізи несуть версію (`1.8.15`); код прикладів — без версії. Фільтр `version` приймає мінор
(`"1.8"`) або точну версію. Промпт відповідає для 1.8.15 і каже, для якого шляху імпорту відповідь.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку. У `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant. Відповіді ті самі до символа, бо кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/coder-websocket-corpus-2026-10-27.tar.gz` (78 текстів, паспорт і
сховище сирого `raw/`; перед видаленням текстів архів розпаковано окремо й звірено з диском) і в копії на Windows
`C:\Distr\coder-websocket-corpus-2026-10-27.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/coder-websocket/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/coder-websocket-corpus-РРРР-ММ-ДД.tar.gz -C instances/coder-websocket corpus raw
find instances/coder-websocket/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/coder-websocket/raw
gzip -9 -c instances/coder-websocket/index/passages.json > instances/coder-websocket/index/passages.json.gz
```

Після цього закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Тексти й сховище видаляють лише тоді,
коли архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із текстами повертається сховище сирого:

```
tar -xzf ~/archives/docfactory/coder-websocket-corpus-2026-10-27.tar.gz -C instances/coder-websocket
./df coder-websocket smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Їхні
перевірки `smoke` чесно пропускає з позначкою «корпус в архіві».

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/coder-websocket/index/passages.json.gz`.
Далі `./df coder-websocket vectors` заллє колекцію Qdrant: секунди на відеокарті, хвилина на процесорі.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df coder-websocket …` бере спільне середовище з кореня репозиторію (`.venvs/cpu`
або `.venvs/gpu`). Як збудувати його один раз і як `df` обирає між ними — у кореневому README, розділ «Спільне
середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df coder-websocket sources --why   # перелік джерел і білий список
./df coder-websocket refresh         # завантажити все задеклароване (кілька хвилин)
./df coder-websocket manifest        # оновити паспорт
./df coder-websocket setup           # Qdrant чи пошук лише по словах
./df coder-websocket vectors         # залити корпус у docs-coder-websocket
./df coder-websocket smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити його працювати:

```
cd ~/Projects/docfactory
./df coder-websocket serve          # порт 8922
```

Сервер готовий, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8922/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user coder-websocket-docs http://127.0.0.1:8922/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування. Вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell або додати сервер кнопкою «Add server» у вікні
`/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` має показати `coder-websocket-docs` і два інструменти: `search_docs` і `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта (scope запису, «address already in use») — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).

