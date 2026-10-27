# golang-jwt — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про golang-jwt (github.com/golang-jwt/jwt) — реалізацію JSON Web Token
для Go: створення й підпис токена, розбір і перевірка, методи підпису й типи ключів, опції перевірки
(`WithValidMethods`, `WithLeeway`, `WithExpirationRequired`), помилки й перехід з v4 на v5. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Навіщо окремий примірник

У плані Go ([../go/LEARNING.md](../go/LEARNING.md), фаза 4, дні 2–3) access-токен — JWT, підписаний HS256 через
golang-jwt v5, а middleware входу перевіряє його з `WithValidMethods` і `WithExpirationRequired`. Між v4 і v5 модель
перевірки змінилася повністю (новий `Validator`, `ParserOption`, `ClaimsValidator`), а в чужому коді живуть обидві
лінії, тож довідник лежить на кожну мінорну обох.

## Скільки цього

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Сайт golang-jwt.github.io/jwt | 4 | — | репозиторій golang-jwt/jwt-docs, гілка main: вступ, створення, розбір, методи підпису |
| Документи репозиторію | 25 | 13 | README, MIGRATION_GUIDE, VERSION_HISTORY, SECURITY з останнього тегу кожної мінорної 3.0–5.3 |
| Релізи | 21 | 21 | GitHub Releases, лише стабільні |
| Довідник v5 | 5 | 4 | pkg.go.dev, `github.com/golang-jwt/jwt/v5@vX.Y.Z` і підпакет `request`, 5.0–5.3 |
| Довідник v4 | 8 | 6 | pkg.go.dev, `github.com/golang-jwt/jwt/v4@vX.Y.Z` і `request`, 4.0–4.5 |

Разом 63 записи паспорта. В індексі 510 фрагментів (`expected_passages` у `checks.json`) із 58 документів. Замір
`quality`: по словах 6 із 10, за змістом 8, разом 7, «як модель» 10 із 10. Цілі доповнено справжніми відповідями:
розділ посібника переходу про опції розбору й перевірки, тип `ValidationError` лінії 4 і змінні-помилки v5, нотатки
релізу 5.0.0. Промахи першої десятки — запити своїми словами про допуск розбіжності годинників, токен без терміну
дії й перехід v4 → v5: довідник каже це назвами `WithLeeway`, `WithExpirationRequired` і `MIGRATION_GUIDE`, і пошук
своїми словами приносить сусідні сторінки.

Чого немає:

- Специфікацій JWT і JOSE (RFC 7519, RFC 7515) — вони в примірнику `webstandards`.
- Інших бібліотек JWT (lestrrat-go/jwx, go-jose) і JWE (`golang-jwt/jwe`).
- Ліній 1.x і 2.x на pkg.go.dev — лише їхні записи у VERSION_HISTORY.

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

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df golang-jwt <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт | гілка main golang-jwt/jwt-docs: `docs/` | `ghdocs-history` |
| документи репозиторію | дерева 13 тегів golang-jwt/jwt (3.0.0–5.3.1): `README.md`, `MIGRATION_GUIDE.md`, `VERSION_HISTORY.md`, `SECURITY.md` | `ghdocs-history` |
| релізи | api.github.com, `/repos/golang-jwt/jwt/releases` | `ghreleases-stable` |
| довідник | pkg.go.dev, v5 (5.0.0–5.3.1) і v4 (4.0.0–4.5.2) | `pkgsite` (`versions`) |

Сторінки сайту цитуються адресами golang-jwt.github.io/jwt/… (поле `site`), решта — файлами на GitHub і сторінками
pkg.go.dev з версією.

## Версії

Документи репозиторію, релізи й довідник несуть версію golang-jwt (`5.3.1`); сайт — поточна редакція без версії.
Фільтр `version` приймає мажор (`"5"`, `"4"`), мінор або точну версію. Промпт відповідає для v5, якщо користувач не
назвав v4.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку. У `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant. Відповіді ті самі до символа, бо кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/golang-jwt-corpus-2026-10-27.tar.gz` (63 тексти, паспорт і сховище
сирого `raw/`; перед видаленням текстів архів розпаковано окремо й звірено з диском) і в копії на Windows
`C:\Distr\golang-jwt-corpus-2026-10-27.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/golang-jwt/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/golang-jwt-corpus-РРРР-ММ-ДД.tar.gz -C instances/golang-jwt corpus raw
find instances/golang-jwt/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/golang-jwt/raw
gzip -9 -c instances/golang-jwt/index/passages.json > instances/golang-jwt/index/passages.json.gz
```

Після цього закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Тексти й сховище видаляють лише тоді,
коли архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із текстами повертається сховище сирого:

```
tar -xzf ~/archives/docfactory/golang-jwt-corpus-2026-10-27.tar.gz -C instances/golang-jwt
./df golang-jwt smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Їхні
перевірки `smoke` чесно пропускає з позначкою «корпус в архіві».

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/golang-jwt/index/passages.json.gz`.
Далі `./df golang-jwt vectors` заллє колекцію Qdrant: секунди на відеокарті, хвилина на процесорі.

## Установка venv

Власний venv цьому примірнику не потрібен: `./df golang-jwt …` бере спільне середовище з кореня репозиторію (`.venvs/cpu`
або `.venvs/gpu`). Як збудувати його один раз і як `df` обирає між ними — у кореневому README, розділ «Спільне
середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df golang-jwt sources --why   # перелік джерел і білий список
./df golang-jwt refresh         # завантажити все задеклароване (кілька хвилин)
./df golang-jwt manifest        # оновити паспорт
./df golang-jwt setup           # Qdrant чи пошук лише по словах
./df golang-jwt vectors         # залити корпус у docs-golang-jwt
./df golang-jwt smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити його працювати:

```
cd ~/Projects/docfactory
./df golang-jwt serve          # порт 8921
```

Сервер готовий, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8921/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user golang-jwt-docs http://127.0.0.1:8921/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування. Вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell або додати сервер кнопкою «Add server» у вікні
`/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` має показати `golang-jwt-docs` і два інструменти: `search_docs` і `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта (scope запису, «address already in use») — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).

