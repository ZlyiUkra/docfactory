# cares — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про c-ares — асинхронний DNS-резолвер на C, на якому стоять `dns.resolve*`
і `dns.Resolver` у Node.js: канал (`ares_channel_t`), `ares_init_options`, `ares_getaddrinfo`, `ares_query`,
`ares_process`, сервери й тайм-аути, розбір відповідей (`ares_dns_record`). Документація — сторінки man кожної функції,
заголовки, README і посібники, нотатки кожного випуску (зміни, виправлені вразливості), вихідний код і тести всіх випусків
від 1.1.0 до 1.34.8. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Документація Node.js описує `dns` зверху. Чому `dns.lookup` і `dns.resolve` поводяться по-різному, які тайм-аути й
повтори має резолвер, у якому випуску закрито вразливість у розборі відповіді — відповідає c-ares, а його версія в кожному
випуску Node своя (які — у примірнику `nodejs`, документ кожної лінії). Сайт c-ares показує лише найновіший випуск; тут — кожен.

## Скільки цього

| Шар | Документів | Звідки |
|-----|-----------:|--------|
| Сторінки man (`ares_*.3`, `adig.1`, `ahost.1`) | 720 | `docs/` і корінь старих тегів |
| README, INSTALL, FEATURES, DEVELOPER-NOTES, SECURITY, нотатки випусків (`RELEASE-NOTES.md`) | 67 | кожен тег |
| Текстові файли без розширення (`RELEASE-NOTES` до 1.19, `CHANGES.0`, `NEWS`, `TODO`) | 92 | кожен тег |
| Публічні заголовки (`include/*.h`) | 148 | кожен тег |
| Внутрішні заголовки й реалізація (`src/lib`, `src/tools`) | 1 783 | кожен тег |
| Тести (`test/*.cc`) | 360 | кожен тег |

Разом 3 170 документів у 65 випусках 1.1.0–1.34.8; фрагментів — 3 464 (`expected_passages` у `checks.json`). Замір
`quality` (12 запитів): по словах 9, за змістом 11, разом 12. `max_per_doc` 0.

## Що в цій теці

- `corpus/` — паспорт `index.json`: адреса, дата завантаження й сума тексту кожного документа. Самих текстів тут немає:
  корпус в архіві.
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub і, для кроку `ask`, ключ Anthropic; `.mcp.json` — запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики через `./df cares <крок>`.

## Звідки документація

Один репозиторій `c-ares/c-ares`, 65 тегів (`cares-1_1_0`, `c-ares-1_17_0`, `v1.34.8`). Шість джерел:

| Що | Читач |
|----|-------|
| сторінки man | `ghdocs-history-roff`, новий: groff → markdown тим самим перетворювачем, що й у `man-pages` |
| README і `.md` | `ghdocs-history` |
| файли без розширення | `ghcode-history` |
| публічні й внутрішні заголовки, тести | `ghcode-history`, у заголовків з `outline` (розділ на коментар Doxygen) |

Особливості:

- **Три розкладки репозиторію.** До 1.10 усе лежить у корені (`ares_init.3`, `ares.h`, `ares_init.c`); далі `docs/`, `include/`,
  `src/lib`. Імена документів зведено: `ares-init-options-3`, `api-ares-h`, `int-ares-process-c` — однакові файли різних
  розкладок зливаються.
- **Журнал змін двічі.** До 1.19 нотатки — текстовий `RELEASE-NOTES`, потім `RELEASE-NOTES.md`; старий журнал змін
  `CHANGES.0` (ручний) є до 1.19.
- Теги `curl-*` (c-ares у дереві curl) і `-rc` не беруться.

## Межі, про які треба пам'ятати

Документації Node.js `dns`, системного резолвера (`getaddrinfo(3)` libc) і інших DNS-бібліотек тут немає. Окремого
репозиторію дизайн-документів у c-ares немає: їхню роль несуть `DEVELOPER-NOTES.md`, `FEATURES.md` і `TODO`.

## Архівний режим: сервер без корпусу

Корпус в архіві від самого початку: у `corpus/` лежить лише паспорт, а сервер підіймається з кешу фрагментів і
колекції Qdrant; відповіді ті самі до символа.

**Де тексти.** В архіві `~/archives/docfactory/cares-corpus-2026-10-15.tar.gz` (19 МБ, 3 170 текстів, паспорт і сховище
сирого `raw/`; перед видаленням розпакований окремо й звірений з диском — нуль розбіжностей). Лише на цій машині.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/cares-corpus-РРРР-ММ-ДД.tar.gz -C instances/cares corpus raw
find instances/cares/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/cares/raw
gzip -9 -c instances/cares/index/passages.json > instances/cares/index/passages.json.gz
```

**Як повернути тексти** — перед будь-яким оновленням:

```
tar -xzf ~/archives/docfactory/cares-corpus-2026-10-15.tar.gz -C instances/cares
./df cares smoke
```

**Оновлення.** Новий тег дописують першим рядком у `tags` усіх шести джерел («"v1.34.9": "1.34.9"»). Далі
`./df cares refresh`, `manifest`, `vectors`, `smoke`, `quality`.

## Установка venv

```
cd instances/cares
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
./df cares sources --why   # перелік джерел і білий список
./df cares refresh         # завантажити все задеклароване (близько 25 хвилин)
./df cares manifest        # оновити паспорт
./df cares setup           # Qdrant чи пошук лише по словах
./df cares vectors         # залити корпус у docs-cares (близько 10 хвилин)
./df cares smoke           # перевірки
```

Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df cares serve          # порт 8841
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8841/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user cares-docs http://127.0.0.1:8841/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User).

**3. Перевірити.** `/mcp` — має бути `cares-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера.
