# webstandards — примірник фабрики docfactory

Двадцять п'ятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про те, чого вимагають самі
вебстандарти, — за їхніми текстами англійською: WHATWG, W3C, RFC та чернетки IETF, OpenID Connect, OpenAPI, JSON
Schema й ERC. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо

Примірник `mdn` пояснює платформу й каже, які браузери що підтримують, але правила переказує. Коли питання —
«як саме це виконується за стандартом»: коли браузер шле preflight, що кеш має право зберегти, як визначено
`SameSite`, які claims JWT треба перевірити, чого вимагає критерій WCAG, — відповідь у самому тексті стандарту. Це
те саме, чим примірник `ecmascript` є для мови. Плани навчання React, NestJS і Next.js посилаються на RFC 6455,
OAuth 2.0 Security BCP, JWT, CSP, WCAG і ARIA; до цього примірника — з позначкою «поза корпусом». Карта того, яким
фазам потрібен `webstandards`, — у [../../docs/learning-map.md](../../docs/learning-map.md).

Версій тут немає: кожен стандарт — в одному виданні. Стандарти WHATWG і чернетки редакторів W3C — живі тексти, як
вони стоять сьогодні; рекомендації W3C і RFC — як опубліковано. Два тексти — не остаточні: RFC 6265bis (куки) —
чернетка 22 у черзі редактора RFC, JSON Schema 2020-12 опубліковано як чернетки IETF; відповідь на них каже, що
текст — чернетка.

## Скільки цього

| Група | Джерел | Документів | Фрагментів | Що там |
|-------|-------:|-----------:|-----------:|--------|
| WHATWG: HTML | 1 | 55 | 3 564 | сторінки стандарту: елементи, цикл подій, навігація, скрипти, воркери, SSE, сховище, розбір |
| WHATWG: решта | 16 | 131 | 1 740 | DOM, Fetch, URL, Streams, WebSockets, Infra, Web IDL, Encoding, MIME Sniffing, Storage, XHR, Cookie Store, Notifications, Fullscreen, Console, Compression |
| W3C | 12 | 120 | 1 415 | CSP 3, Fetch Metadata, Referrer Policy, Permissions Policy, Secure Contexts, Mixed Content, Service Workers, Manifest, Push API, WAI-ARIA 1.2, ARIA in HTML, WCAG 2.2 |
| WAI: Understanding WCAG 2.2 | 1 | 109 | 1 804 | пояснення до кожного критерію: навіщо, кому, приклади, техніки |
| WAI: Techniques for WCAG 2.2 | 1 | 435 | 3 415 | техніки й типові помилки: HTML, ARIA, CSS, скрипти, сервер, PDF |
| WAI: ARIA Authoring Practices | 2 | 39 | 468 | патерни віджетів і практики: ролі, клавіатура, фокус, назви |
| IETF і OpenID | 23 | 271 | 2 416 | RFC 9110, 9111, 9112, 6265 і чернетка 6265bis, 6455, 6585, 6797, 9457, 7519, 7515, 7517, 7518, 8725, 6749, 6750, 7636, 9700, 9106; JSON Schema 2020-12 (core, validation); OpenID Connect Core і Discovery |
| OpenAPI | 1 | 11 | 248 | OpenAPI Specification 3.1.1 |
| ERC | 3 | 3 | 91 | ERC-20, ERC-721, ERC-4361 (Sign-In with Ethereum) |

Разом 1 175 документів; фрагментів в індексі — 15 161 (`expected_passages` у `checks.json`). Фрагменти — це шматки
документів між заголовками, по яких іде пошук. Один документ фрагментів не має: розділ IANA в RFC 9700 — один рядок
«This document has no IANA actions.», коротший за поріг фрагмента.

Замір `quality` на першому корпусі (05.10.2026): перша десятка (питання своїми словами) — по словах 4 із 10, за
змістом 5, разом 5; друга, «як модель» (терміни самого стандарту, як велить промпт), — 10 із 10. Переказ без
термінів слабкий: «захистити код авторизації мобільного застосунку» знаходить OAuth BCP і OpenID, але не главу
протоколу PKCE; «вікно, що блокує решту сторінки» — патерн комбобокса, а не модального діалогу. Голі слова без
назви теж підводять: на «main fetch» по словах першими стоять розділи Mixed Content і Referrer Policy про
інтеграцію з Fetch, де ці два слова повторюються, а не глава 4.1 самого Fetch. Тому промпт пошуку велить писати
запит термінами стандарту — «CORS-preflight fetch», «SameSite attribute», «Success Criterion 2.4.11».

## Як влаштований документ

Документ — розділ верхнього рівня стандарту: `whatwg-fetch--4-fetching`, `rfc9110--15-status-codes`,
`w3c-wcag--2-operable`. Підрозділи — заголовки з номерами самого стандарту («## 4.1 Main fetch», «### 15.5.21 422
Unprocessable Content»), тож розділ можна назвати номером, як у тексті. Стандарт HTML — інакше: він видається
сторінками, і документ — сторінка видання (`whatwg-html--webappapis`). Сторінки Understanding WCAG, Techniques for
WCAG і APG названо за їхнім шляхом на w3.org.

- **Алгоритми** — кроки пронумеровано, вкладені кроки зсунуто: на крок посилаються номером («step 12 of main
  fetch»), і без номерів і відступів «If …, then: return failure» читалося б як два незалежні речення.
- **Що відкинуто** — зміст, анотації MDN і тестів WPT, спливні панелі визначень, покажчики, бібліографія, подяки,
  колонтитули сторінок RFC і адреси авторів.
- **Адреса документа** веде на сам розділ: `https://fetch.spec.whatwg.org/#fetching`,
  `https://www.rfc-editor.org/rfc/rfc9110.html#section-15`. В OpenID Connect якорі розділів — слова, а не номери,
  тож там адреса — сторінка специфікації.

## Що в цій теці

- `corpus/` — лише паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа (тексти — в архіві,
  див. нижче).
- `index/passages.json.gz` — стиснений кеш фрагментів, з якого підіймається сервер.
- `sources.json` — шістдесят джерел, по одному на стандарт чи сайт; водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.mcp.json` — запис HTTP-сервера для Claude Code; `.env` потрібен лише для кроку `ask` (ключ Anthropic).
- `.venv/` — власний venv примірника; `requirements.txt` — його склад.

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df webstandards <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| стандарти WHATWG, CSP, Fetch Metadata, Service Workers та інші, зібрані Bikeshed; WCAG, WAI-ARIA, Manifest, Push, OpenAPI, зібрані ReSpec | сторінка специфікації однією сторінкою | `spec-html` |
| стандарт HTML | багатосторінкове видання html.spec.whatwg.org/multipage | `whatwg-html` |
| RFC, чернетки IETF, OpenID Connect | текст xml2rfc (rfc-editor.org, ietf.org, openid.net) | `ietf-text` |
| Understanding WCAG, Techniques for WCAG, APG | сторінки w3.org/WAI за їхніми змістами | `html-pages` |
| ERC-20, ERC-721, ERC-4361 | markdown репозиторію ethereum/ERCs | `erc-md` |

Читачі `spec-html`, `whatwg-html`, `ietf-text` і `erc-md` — нові, у
[../../engine/readers/webspecs.py](../../engine/readers/webspecs.py). Свій розбір HTML, а не спільний: спільний
ставить замість номера кроку дефіс. Окремо від читача `bikeshed` примірника `wasm`: той збирає назад формули
KaTeX, а тут формул немає, зате є ReSpec і Wattsi.

## Межі, про які треба пам'ятати

Тут немає підтримки браузерами (вона в `mdn`), підручників, HTTP/2 і HTTP/3, TLS, специфікацій CSS і ECMAScript
(остання — у примірнику `ecmascript`). IEEE 754 і стандарт SQL не взято: їхні тексти платні. Документація бібліотек
(Passport, Auth.js, socket.io, viem) — окремі примірники чи поза фабрикою.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку, як у kubernetes, linux, vitest і mdn: у `corpus/` лежить лише
паспорт `index.json`, а сервер підіймається з кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді
ті самі до символа — кеш тримає повний текст кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/webstandards-corpus-2026-10-05.tar.gz` (3,3 МБ, 1 175 текстів і
паспорт; перед видаленням розпакований окремо й звірений із диском — нуль розбіжностей). В історії git текстів немає
ніде. Архів лежить лише на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/webstandards/index/passages.json        # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/webstandards-corpus-РРРР-ММ-ДД.tar.gz -C instances/webstandards corpus
find instances/webstandards/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/webstandards/index/passages.json > instances/webstandards/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/webstandards-corpus-РРРР-ММ-ДД.tar.gz -C instances/webstandards
./df webstandards smoke
```

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/webstandards/index/passages.json.gz`,
далі `./df webstandards vectors` заллє колекцію Qdrant.

## Установка venv

```
cd instances/webstandards
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # ANTHROPIC_API_KEY — лише якщо потрібен крок ask
cd ../..
```

## Збирання корпусу

```
./df webstandards sources --why   # перелік джерел і білий список
./df webstandards refresh         # завантажити все задеклароване
./df webstandards manifest        # оновити паспорт
./df webstandards setup           # Qdrant чи пошук лише по словах
./df webstandards vectors         # залити корпус у docs-webstandards
./df webstandards smoke           # перевірки
```

Обірваний `refresh` продовжується з `--missing`: уже записане він не тягне вдруге; з `--missing` імена джерел
звужують прогін (`./df webstandards refresh --missing rfc9110`).

**Коли вийде RFC 6265bis**, джерело `rfc6265bis` треба перевести з чернетки 22 на текст RFC (поля `url`, `cite`,
`title`, `label`); так само — на новішу редакцію, коли зміниться номер чернетки.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df webstandards serve           # порт 8785
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8785/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user webstandards-docs http://127.0.0.1:8785/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `webstandards-docs` і два інструменти `search_docs`, `read_section`. Якщо сесію
Claude Code відкрито раніше, ніж піднято сервер, вона покаже його як недоступний: у `/mcp` виберіть сервер і
«Reconnect».

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
