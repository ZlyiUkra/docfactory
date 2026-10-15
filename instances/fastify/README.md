# fastify — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Fastify — швидкий вебфреймворк для Node.js (альтернативу Express):
маршрути зі схемами JSON (валідація й серіалізація), система плагінів з інкапсуляцією, хуки життєвого циклу запиту,
декоратори, обробка помилок, логування (pino), TypeScript. Документація — довідник і посібники кожного стабільного випуску
від 1.0.0 до 5.12.7 (з них збирається сайт fastify.dev), код ядра, тести, приклади, нотатки випусків, а також README і
типи TypeScript близько 160 пакетів екосистеми: офіційних плагінів `@fastify/*`, складників ядра (`fastify-plugin`,
`avvio`, `find-my-way`, `light-my-request`, `fast-json-stringify`, `secure-json-parse`, `fastify-cli`) і старих
плагінів `fastify-*`. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Fastify живе плагінами: більшість питань («як увімкнути CORS», «як перевірити JWT», «як згенерувати OpenAPI») — це питання
до README плагіна, а не до ядра. Сайт fastify.dev показує лише поточну версію, а плагіни розкидані по десятках
репозиторіїв. Тут — усе в одному місці, з історією версій і міграціями 3 → 4 → 5.

## Скільки цього

| Шар | Документів | Звідки |
|-----|-----------:|--------|
| Документація (`docs`), README, SECURITY, GOVERNANCE | 1 513 | `fastify/fastify`, 298 тегів |
| Код ядра (`fastify.js`, `lib`, `types`, `build`) | 1 629 | ті самі |
| Тести (`test`, `integration`) | 2 521 | ті самі |
| Приклади (`examples`, `benchmarks`) | 116 | ті самі |
| Нотатки випусків | 298 | GitHub Releases |
| README пакетів npm (163 пакети) | 1 994 | tarball кожної стабільної версії |
| Типи TypeScript пакетів | 1 143 | ті самі |

Разом 9 214 документів; фрагментів — 20 103 (`expected_passages` у `checks.json`). Замір `quality` (12 запитів): по словах
10, за змістом 12, разом 12. `max_per_doc` 0.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується (≈410 джерел), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df fastify <крок>`.

## Звідки документація

| Що | Читач |
|----|-------|
| `docs` ядра | `ghdocs-history` |
| код, тести, приклади ядра | `ghcode-history` (код і типи — з `outline`) |
| нотатки випусків | `ghreleases` |
| README і типи пакетів | `npm-tarball-files`, по два джерела на пакет |

Нового коду для Fastify не знадобилось.

Особливості:

- **Імена документів.** Ядро: `docs-reference-hooks`, `docs-guides-migration-guide-v5`, `code-lib-hooks-js`,
  `test-test-hooks-test-js`. Пакети: `at-fastify-cors-markdown` для `@fastify/cors`, `pkg-fastify-plugin-markdown` для
  `fastify-plugin`, `…-types` для типів.
- **Версія пакета — своя.** README `@fastify/cors` 11.x несе версію плагіна, а не Fastify; який мажор Fastify підтримує
  плагін, сказано в самому README.
- **Типи в нестандартному місці.** Для пакетів, де `.d.ts` лежить не в `index.d.ts` (наприклад, `plugin.d.ts`), є друге
  джерело `*-types2`.
- **Старі імена.** До 2021 плагіни називались `fastify-cors`, `fastify-static`; вони теж є — для проєктів на Fastify 2–3.

## Межі, про які треба пам'ятати

- Лише стабільні випуски: Fastify 6 (alpha, rc) не взято; пре-релізи пакетів теж.
- pino (логер) — окремий проєкт; його документації тут немає, лише те, що про нього кажуть документи Fastify.
- Інші сторонні плагіни спільноти, яких немає в організації fastify, не беруться; їх перелік — у `docs-guides-ecosystem`.
- Сайт fastify.dev збирається з `docs/` ядра, тож окремо його не завантажено.

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/fastify-corpus-2026-10-15.tar.gz` (604 МБ: 9 214 текстів, паспорт і сховище
сирого `raw/` з tarball пакетів; перед видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на
цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/fastify-corpus-РРРР-ММ-ДД.tar.gz -C instances/fastify corpus raw
find instances/fastify/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/fastify/raw
gzip -9 -c instances/fastify/index/passages.json > instances/fastify/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/fastify-corpus-2026-10-15.tar.gz -C instances/fastify
./df fastify smoke
```

**Оновлення.** Новий тег ядра дописують першим рядком у `tags` джерел із тегами («"v5.12.8": "5.12.8"»); нові версії
пакетів підхоплюються самі (читач бере все з реєстру npm). Далі `./df fastify refresh`, `manifest`, `vectors`, `smoke`,
`quality`. `./df fastify list` довго (завантажує все): краще одразу `refresh`.

## Установка venv

```
cd instances/fastify
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
./df fastify sources --why   # перелік джерел і білий список
./df fastify refresh         # завантажити все задеклароване (близько 50 хвилин)
./df fastify manifest        # оновити паспорт
./df fastify setup           # Qdrant чи пошук лише по словах
./df fastify vectors         # залити корпус у docs-fastify (близько 45 хвилин)
./df fastify smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df fastify serve          # порт 8844
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8844/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user fastify-docs http://127.0.0.1:8844/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `fastify-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера.
