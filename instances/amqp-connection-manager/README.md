# amqp-connection-manager — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про amqp-connection-manager — бібліотеку для Node.js, що обгортає
amqplib автоматичним перепідключенням до RabbitMQ (репозиторій jwalton/node-amqp-connection-manager, пакет
`amqp-connection-manager` на npm) — за README кожної стабільної версії, нотатками релізів та історією версій у реєстрі
npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

Примірник — третій у родині RabbitMQ: сервер окремо (`rabbitmq`), кожен клієнт Node окремо, як у родинах Redis, Mongo і
Kafka. Перед ним — `amqplib`, далі — `@golevelup/nestjs-rabbitmq`.

amqp-connection-manager тримає з'єднання з кількома брокерами й перепідключається сам, а `ChannelWrapper` повторює
функції `setup` (оголошення черг, обмінників, прив'язок) після кожного перепідключення й тримає в пам'яті повідомлення,
надіслані, поки брокер недоступний. Разом з amqplib на ньому стоїть транспорт RabbitMQ мікросервісів NestJS. Близько
585 тисяч завантажень за тиждень до 25.10.2026: лінія 4.1 — близько 46 % (4.1.15 — 29 %), лінія 5 — близько 45 % (5.0.0
— 42 %; найновіша 5.0.1 від 17.10.2026 вимагає Node.js 22).

## Скільки цього

| Шар | Документів | Неповторних | Версій | Звідки |
|-----|-----------:|------------:|-------:|--------|
| README пакета, кожен неповторний текст один раз | 21 | 20 | стабільні версії npm 1.0–5.0 | tarball кожної версії |
| Нотатки релізів | 55 | 55 | стабільні релізи GitHub | jwalton/node-amqp-connection-manager |
| Реєстр npm | 6 | 6 | усі | registry.npmjs.org |

Разом 82 документи; фрагментів в індексі — 195 (`expected_passages` у `checks.json`). Замір `quality`: по словах 6 із 10,
за змістом 6, разом 6, «як модель» 10 із 10.

Чому лише README. Окремого сайту в бібліотеки немає, у репозиторії — тільки README і CONTRIBUTING; README і є
документацією, а зміни кожного випуску (semantic-release) лежать у нотатках релізів GitHub, журналу змін немає.

Чого немає. Документації amqplib (примірник `amqplib`), самого RabbitMQ (примірник `rabbitmq`), NestJS. Коду, типів і
тестів.

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа. Самих
  текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`, розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.mcp.json` — запис HTTP-сервера для Claude Code. `ANTHROPIC_API_KEY` (лише для кроку `ask`) і `GITHUB_TOKEN` (лише
  для завантаження корпусу) беруться з кореневого `.env`.

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df amqp-connection-manager <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| README | tarball `registry.npmjs.org/amqp-connection-manager/-/amqp-connection-manager-X.tgz` кожної стабільної версії | `npm-tarball-files` |
| нотатки релізів | релізи GitHub jwalton/node-amqp-connection-manager, без передрелізів | `ghreleases` |
| реєстр npm | registry.npmjs.org | `npm-versions` |

Усі читачі вже були у фабриці; нових не додавалося.

## Версії

Версія — номер випуску. Фільтр `version` бере мажор (`"4"`), мінор (`"4.1"`) або точну версію (`"5.0.1"`). Лінії 4.1
і 5 мають майже порівну завантажень, тож на питання «як це зробити зараз» промпт велить шукати для обох і казати, де
вони різняться. README, що не змінився між версіями, — один документ з усіма ними, тож перелік версій уривка сам
показує, відколи й доки документація казала саме це.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/amqp-connection-manager-corpus-2026-10-25.tar.gz` (82 тексти, паспорт і сховище
сирого `raw/`; перед видаленням текстів розпакований окремо й звірений із диском) і в копії на Windows-диску
`C:\Distr\amqp-connection-manager-corpus-2026-10-25.tar.gz` (звірено за SHA-256). В історії git текстів немає ніде.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/amqp-connection-manager/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/amqp-connection-manager-corpus-РРРР-ММ-ДД.tar.gz -C instances/amqp-connection-manager corpus raw
find instances/amqp-connection-manager/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/amqp-connection-manager/raw
gzip -9 -c instances/amqp-connection-manager/index/passages.json > instances/amqp-connection-manager/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти й сховище — лише після того, як
архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із ними повертається й сховище `raw/`:

```
tar -xzf ~/archives/docfactory/amqp-connection-manager-corpus-2026-10-25.tar.gz -C instances/amqp-connection-manager
./df amqp-connection-manager smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/amqp-connection-manager/index/passages.json.gz`,
далі `./df amqp-connection-manager vectors` заллє колекцію Qdrant (секунди на відеокарті, кілька хвилин на процесорі).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df amqp-connection-manager …` бере спільне середовище з кореня репозиторію (`.venvs/cpu`
або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md, розділ «Спільне
середовище».

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df amqp-connection-manager sources --why   # перелік джерел і білий список
./df amqp-connection-manager refresh         # завантажити все задеклароване (близько хвилини)
./df amqp-connection-manager manifest        # оновити паспорт
./df amqp-connection-manager setup           # Qdrant чи пошук лише по словах
./df amqp-connection-manager vectors         # залити корпус у docs-amqp-connection-manager
./df amqp-connection-manager smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df amqp-connection-manager serve          # порт 8892
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8892/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user amqp-connection-manager-docs http://127.0.0.1:8892/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server» у
вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `amqp-connection-manager-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у [README
примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
