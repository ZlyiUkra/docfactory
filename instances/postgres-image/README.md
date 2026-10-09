# postgres-image — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про офіційний Docker-образ PostgreSQL (`postgres` на Docker Hub) за його
документацією: сторінкою образу в кожній редакції з 2014 року й репозиторієм `docker-library/postgres` — Dockerfile усіх
стабільних мажорів від 8.4 до 18, скриптами входу, шаблонами та `versions.json`. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../../README.md).

## Що сюди входить

Образ — це не сервер PostgreSQL, а упаковка навколо нього: змінні середовища (`POSTGRES_PASSWORD`, `PGDATA`,
`POSTGRES_INITDB_ARGS`, `POSTGRES_HOST_AUTH_METHOD`, їхні `_FILE`-двійники для секретів Docker), теку
`/docker-entrypoint-initdb.d` зі скриптами першого запуску, том з даними, роботу від довільного користувача, локалі,
`--shm-size`, варіанти Debian і alpine. Усе це описує сторінка образу, а як воно працює — скрипт
`docker-entrypoint.sh` і Dockerfile. Тому в примірнику вони разом: сторінка відповідає «що робить», код — «як і з
якої версії».

Сам сервер PostgreSQL (SQL, `postgresql.conf`, реплікація) — у примірнику `postgresql`; Docker і Compose загалом — у
`docker`. Пакета npm у образу немає, тож і джерела npm тут немає.

## Скільки цього

| Шар | Документів | Звідки |
|-----|-----------:|--------|
| Сторінка образу (`README.md`, `compose.yaml`) у кожній редакції | 402 | `docker-library/docs`, тека `postgres/`, 610 комітів історії |
| Dockerfile мажорів 8.4–18, усі варіанти: Debian (стандартний, wheezy…trixie), alpine і всі alpine3.x | 1 775 | `docker-library/postgres`, 986 комітів |
| Скрипти входу `docker-entrypoint.sh`, `docker-ensure-initdb.sh` у теках мажорів і в корені | 1 152 | те саме |
| Шаблони, `update.sh`, `versions.sh`, `apply-templates.sh`, `generate-stackbrew-library.sh`, `versions.json` (194 редакції), `README.md` репозиторію | 466 | те саме |

Разом 3 795 документів; фрагментів в індексі — 7 233 (`expected_passages` у `checks.json`). Точні числа по шарах —
у `./df postgres-image sources --why` і в паспорті.

**Одиниця корпусу — неповторний вміст файла.** У репозиторію образу немає тегів: Dockerfile змінюється з кожним
мінорним випуском PostgreSQL. Читач `ghfile-history` проходить усі коміти, і пара «шлях, вміст» стає одним документом.
Першим рядком тіла стоять дати, між якими ця редакція була чинною (за комітами), тож у відповіді видно, коли саме
це було правдою.

**Версія документа.**
- Dockerfile — точна версія PostgreSQL з рядка `ENV PG_VERSION` (`14.24`; суфікс збірки Debian відкинуто).
  Фільтр `version: "14"` знаходить усі редакції лінії.
- Скрипт входу в теці мажору — цей мажор.
- Спільний файл (шаблон, `update.sh`, `versions.json`) — перелік стабільних мажорів, що були в деревах, де файл
  лежав саме таким.
- Сторінка образу — теги, що стояли в її переліку підтримуваних («18.6», «18», «17.11» …).

## Межі, про які треба пам'ятати

- **Бета не входить.** Мажор 19 на 09.10.2026 має лише `19beta4`; його Dockerfile, редакції з `beta`/`rc` у
  `PG_VERSION` і мажор без жодної стабільної редакції в цьому коміті в корпус не потрапляють. `versions.json` і
  сторінка образу про 19 згадують, бо так вони й написані.
- **Варіанти.** Взято всі, що коли-небудь були в репозиторії: стандартний (Debian), `alpine`, `wheezy`, `jessie`,
  `stretch`, `buster`, `bullseye`, `bookworm`, `trixie` і кожен `alpine3.x`. Спершу корпус зібрано лише з поточними
  варіантами (2 881 документ), 09.10.2026 — розширено до всіх. Різниця між варіантами — у назві документа:
  `14-bullseye-dockerfile`, `14-alpine3-17-dockerfile`.
- **Сторінка образу на Docker Hub** сама не читається: вона будується скриптами й повторює `docker-library/docs`.
  `content.md` окремо не береться: готовий `README.md` — це він плюс шаблони.
- **Маніфест тегів** (`docker-library/official-images`, файл `library/postgres`) не взято: перелік тегів кожної
  редакції видно в сторінці образу.

Замір `quality`: по словах 6 із 10, за змістом 10, разом 10; десятка «як модель» — 10 із 10 (на корпусі з поточними
варіантами по словах було 7).
Поле `max_per_doc` лишено 0: редакції одного файла різняться текстом, а однакові розділи злиття зводить саме.

## Що в цій теці

- `corpus/` — паспорт `index.json`; самих текстів тут немає: корпус в архіві (розділ «Архівний режим»).
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт 8807, колекція Qdrant `docs-postgres-image`, модель векторів, пауза між зверненнями.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — токен GitHub (лише для завантаження корпусу) і, якщо потрібен крок `ask`, ключ Anthropic;
  `.mcp.json` — запис HTTP-сервера для Claude Code.
- `.venv/` — власний venv примірника; `requirements.txt` — його склад.

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df postgres-image <крок>`.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/postgres-image-corpus-2026-10-09-all-variants.tar.gz` (7 МБ, 3 795 текстів і
паспорт; перед видаленням розпакований окремо й звірений із диском — нуль розбіжностей). В історії git текстів
немає. Архів лежить лише на цій машині.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/postgres-image-corpus-2026-10-09-all-variants.tar.gz -C instances/postgres-image
./df postgres-image smoke
```

**Як знову винести** — після оновлення, коли `vectors` і `smoke` пройшли:

```
tar -czf ~/archives/docfactory/postgres-image-corpus-РРРР-ММ-ДД.tar.gz -C instances/postgres-image corpus
find instances/postgres-image/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/postgres-image/index/passages.json > instances/postgres-image/index/passages.json.gz
```

і закомітити паспорт та `index/passages.json.gz`. Тексти видаляють лише після того, як архів звірено з диском
(`diff -r`); тоді ж видаляють попередній архів і міняють його ім'я тут.

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/postgres-image/index/passages.json.gz`,
далі `./df postgres-image vectors` заллє колекцію Qdrant (~18 хвилин).

## Установка venv

```
cd instances/postgres-image
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

```
./df postgres-image sources --why   # перелік джерел і білий список
./df postgres-image refresh         # завантажити все задеклароване (~2 години)
./df postgres-image manifest        # оновити паспорт
./df postgres-image setup           # Qdrant чи пошук лише по словах
./df postgres-image vectors         # залити корпус у docs-postgres-image (~18 хвилин)
./df postgres-image smoke           # перевірки
```

`refresh` довгий не через обсяг, а через перелік: читач бере дерево кожного з 986 комітів `docker-library/postgres`
і 610 комітів теки `postgres/` у `docker-library/docs` (близько 1 600 звернень до API), а для кожної редакції
Dockerfile ще й читає її текст, щоб дістати точну версію й відсіяти бета (старі варіанти збільшили перелік до 1,5 години). Перші півтори години журнал мовчить. Запускайте
окремим процесом (`setsid nohup`): довгі фонові команди сесії обриваються через 30 хвилин.

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df postgres-image serve          # порт 8807
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8807/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user postgres-image-docs http://127.0.0.1:8807/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `postgres-image-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
