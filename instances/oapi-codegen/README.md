# oapi-codegen — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про oapi-codegen (github.com/oapi-codegen/oapi-codegen) — генератор
коду Go з документів OpenAPI 3 — і про бібліотеки, на яких стоїть згенерований код: `github.com/oapi-codegen/runtime`,
middleware перевірки запитів `nethttp-middleware` і kin-openapi (github.com/getkin/kin-openapi), що завантажує й
перевіряє документ. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі
дані домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

У плані Go ([../go/LEARNING.md](../go/LEARNING.md), фаза 2) контракт пишуть спершу: `openapi.yaml`, з нього
oapi-codegen генерує типи й строгий сервер для `net/http`, а middleware на kin-openapi перевіряє кожен запит тим самим
документом; у фазі 4 той самий документ вирішує, які маршрути закриті входом. Ці три бібліотеки відповідають на одне
питання — «як зробити сервер із документа OpenAPI» — тож лежать разом. Головна документація oapi-codegen — його
README (понад тисячу рядків) і тека `docs/`, kin-openapi — README з рецептами й переліком несумісних змін, решта — API
на pkg.go.dev.

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| README і docs oapi-codegen | 43 | 26 | `README.md`, `docs/`, README прикладів з останнього тегу кожної мінорної 1.0–2.8 |
| Релізи oapi-codegen | 88 | 88 | GitHub Releases, лише стабільні |
| Код прикладів | 247 | — | `examples/` гілки main без згенерованих `*.gen.go` |
| runtime | 19 | 9 | pkg.go.dev, `github.com/oapi-codegen/runtime` 1.0–1.8 |
| nethttp-middleware | 3 + 4 | 4 | README і pkg.go.dev 1.0–1.3 |
| README kin-openapi | 51 | 152 | `README.md` з останнього тегу кожної мінорної 0.1–0.152 |
| Довідник kin-openapi | 18 | 12 | pkg.go.dev: openapi3, openapi3filter, routers, openapi3gen — 0.141–0.152 |

Документів менше, ніж версій: текст, що не мінявся між мінорними, — один документ із переліком версій.

Разом 473 записи паспорта. В індексі 2452 фрагменти (`expected_passages` у `checks.json`) із 457 документів. Замір
`quality`: по словах 8 із 10, за змістом 8, разом 9, «як модель» 10 із 10. Цілі доповнено справжніми відповідями:
`OapiRequestValidatorWithOptions` і тип `Validator` openapi3filter, загальний розділ README про розширення OpenAPI,
розділ «Using oapi-codegen» і `GenerateOptions` (ключ `embedded-spec`), опції `EnableMultiError` і `MultiErrors` та
тип `MultiError` у openapi3. Промах першої десятки — «свій тип Go замість згенерованого»: README каже це розширенням
`x-go-type`, і видача своїми словами приносить сторінки про схеми kin-openapi.

Чого немає:

- Внутрішніх пакетів самого генератора (`pkg/codegen`) на pkg.go.dev: їх не викликають із застосунку.
- Довідника kin-openapi раніше 0.141 — лише README тих версій (мінорних 0.x понад сто п'ятдесят).
- Пакетів kin-openapi для Swagger 2.0 (`openapi2`, `openapi2conv`).
- Специфікації OpenAPI і JSON Schema (примірники `webstandards` і `jsonschema`), генераторів клієнтів TypeScript
  (`orval`, `openapi-typescript`).

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

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df oapi-codegen <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| README, docs, README прикладів | дерева 26 тегів oapi-codegen (1.0.6–2.8.1) | `ghdocs-history` |
| релізи | api.github.com, `/repos/oapi-codegen/oapi-codegen/releases` | `ghreleases-stable` |
| код прикладів | `examples/` гілки main | `ghcode` |
| runtime, nethttp-middleware | pkg.go.dev з версією; README middleware з 4 тегів | `pkgsite` (`versions`), `ghdocs-history` |
| kin-openapi | README зі 152 тегів; pkg.go.dev останніх 12 мінорних | `ghdocs-history`, `pkgsite` (`versions`) |

Документи kin-openapi мають префікс імені `kin-openapi-`: README генератора й README kin-openapi в іншому разі мали б
однакове ім'я `readme`, і пошук згортав би їхні розділи як повтори.

## Версії

Кожна бібліотека має власну нумерацію: oapi-codegen 1.x–2.x, runtime 1.x, nethttp-middleware 1.x, kin-openapi 0.x
(`0.152.0`). Фільтр `version` приймає мажор, мінор або точну версію; `"1.5"` може зачепити кілька бібліотек, тож
промпт просить називати бібліотеку. Відповідь — для найновіших: oapi-codegen 2.8.1, runtime 1.8.0, nethttp-middleware
1.3.1, kin-openapi 0.152.0.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку. У `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant. Відповіді ті самі до символа, бо кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/oapi-codegen-corpus-2026-10-27.tar.gz` (473 тексти, паспорт і сховище
сирого `raw/`; перед видаленням текстів архів розпаковано окремо й звірено з диском) і в копії на Windows
`C:\Distr\oapi-codegen-corpus-2026-10-27.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/oapi-codegen/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/oapi-codegen-corpus-РРРР-ММ-ДД.tar.gz -C instances/oapi-codegen corpus raw
find instances/oapi-codegen/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/oapi-codegen/raw
gzip -9 -c instances/oapi-codegen/index/passages.json > instances/oapi-codegen/index/passages.json.gz
```

Після цього закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Тексти й сховище видаляють лише тоді,
коли архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із текстами повертається сховище сирого:

```
tar -xzf ~/archives/docfactory/oapi-codegen-corpus-2026-10-27.tar.gz -C instances/oapi-codegen
./df oapi-codegen smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Їхні
перевірки `smoke` чесно пропускає з позначкою «корпус в архіві».

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/oapi-codegen/index/passages.json.gz`.
Далі `./df oapi-codegen vectors` заллє колекцію Qdrant: секунди на відеокарті, хвилина на процесорі.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df oapi-codegen …` бере спільне середовище з кореня репозиторію (`.venvs/cpu`
або `.venvs/gpu`). Як збудувати його один раз і як `df` обирає між ними — у кореневому README, розділ «Спільне
середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df oapi-codegen sources --why   # перелік джерел і білий список
./df oapi-codegen refresh         # завантажити все задеклароване (близько десяти хвилин)
./df oapi-codegen manifest        # оновити паспорт
./df oapi-codegen setup           # Qdrant чи пошук лише по словах
./df oapi-codegen vectors         # залити корпус у docs-oapi-codegen
./df oapi-codegen smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити його працювати:

```
cd ~/Projects/docfactory
./df oapi-codegen serve          # порт 8919
```

Сервер готовий, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8919/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user oapi-codegen-docs http://127.0.0.1:8919/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування. Вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell або додати сервер кнопкою «Add server» у вікні
`/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` має показати `oapi-codegen-docs` і два інструменти: `search_docs` і `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта (scope запису, «address already in use») — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).

