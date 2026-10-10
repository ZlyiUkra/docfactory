# nodemailer — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Nodemailer — пакет npm для надсилання електронної пошти з Node.js
(SMTP, пул з'єднань, sendmail, SES, DKIM, OAuth2) — за документацією всіх його стабільних версій: сайтом
nodemailer.com у стані на кожен реліз, README, типами, прикладами й журналом змін пакета та реєстром npm. Поруч —
те саме для супутніх пакетів проєкту: mailparser (розбір отриманого листа), smtp-server (SMTP- і LMTP-сервер для
прийому пошти), smtp-connection і mailcomposer як окремі пакети (SMTP-клієнт і збирач листа; останні випуски —
2017 рік). Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../../README.md).

## Скільки цього

Nodemailer — 295 стабільних версій (0.2.3–10.0.16); передрелізи (`2.0.0-beta.*`, `2.1.0-rc.*`, `2.4.0-beta.0`) не
беруться.

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Сайт nodemailer.com: знімки на кожну стабільну версію | 254 | 8.0.8–10.0.16 | репозиторій `nodemailer/nodemailer-homepage` |
| README: кожен неповторний текст один раз, з усіма версіями | 126 | 0.2.3–10.0.16 (295) | tarball кожної версії npm |
| `SECURITY.md` / `SECURITY.txt` | 5 | 6.9.0–10.0.16 | tarball |
| `CONTRIBUTING.md` | 2 | 4.x–6.0 | tarball |
| Типи 10.x: головний файл, Mailer, SMTP-транспорт, SMTP-з'єднання, MailComposer | 4 + 4 + 4 + 6 + 3 | 10.0.0–10.0.16 | tarball |
| Приклади `examples/` | 83 | версії з `gitHead` у реєстрі (192) | репозиторій `nodemailer/nodemailer` на коміті версії |
| Журнал змін, по документу на версію | 205 | 0.5.2–10.0.16 | `CHANGELOG.md` гілки master |
| Реєстр npm: огляд і лінії 0–10, з вимогами до Node (`engines`) | 12 | усі | registry.npmjs.org |

Супутні пакети — ті самі шари, де пакет їх має; передрелізи так само не беруться:

| Пакет | Версій | README | SECURITY | Приклади | Журнал змін | Реєстр npm |
|-------|-------:|-------:|---------:|---------:|------------:|-----------:|
| mailparser 0.1.0–3.9.37 | 154 | 43 | 2 (3.9.10–3.9.37) | 10 (94 версії з `gitHead`) | 50 (3.6.6–3.9.37) | 4 |
| smtp-server 1.0.0–3.19.18 | 98 | 24 | 1 (3.19.x) | 19 (усі 98) | 88 (1.1.0–3.19.18) | 4 |
| smtp-connection 0.1.0–4.0.2 | 53 | 22 | — | — | 38 (1.0.0–4.0.0) | 6 |
| mailcomposer 0.1.0–4.0.2 | 75 | 34 | — | — | — | 6 |

Разом 1059 документів: 708 Nodemailer і 351 супутніх пакетів; фрагментів в індексі — 3039
(`expected_passages` у `checks.json`).

Замір `quality` на першому корпусі (708 документів): по словах 9 із 10, за змістом 6, разом 10; десятка «як модель» —
10 із 10. Після супутніх пакетів (1059 документів) — те саме: 9, 6, 10 і 10 із 10.

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа.
  Самих текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`, розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки корпус будується, і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — ключ Anthropic (лише для кроку `ask`) і токен GitHub (лише для завантаження корпусу); `.mcp.json` —
  запис HTTP-сервера для Claude Code.
- `.venv/` — власний venv примірника; `requirements.txt` — його склад.

Кроки нижче, окрім установки venv, запускаються з кореня фабрики (`docfactory/`) через `./df nodemailer <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| сайт | репозиторій `nodemailer/nodemailer-homepage`, гілка `master`, тека `docs/`; знімок — вершина гілки перед виходом наступної версії | `ghsite-dated` |
| README, `SECURITY`, `CONTRIBUTING` | tarball `registry.npmjs.org/nodemailer/-/nodemailer-X.tgz` | `npm-tarball-files` |
| типи | той самий tarball (лише 10.x): `dist/cjs/nodemailer.d.ts` і модулі | `npm-tarball-files` |
| приклади | теки `examples/` репозиторію `nodemailer/nodemailer` на `gitHead` версії | `npm-githead-files` |
| журнал змін | `CHANGELOG.md` гілки master | `changelog-mixed`, новий |
| реєстр npm | registry.npmjs.org, одне звернення | `npm-versions` |

Супутні пакети беруться тими самими читачами: tarball пакета npm, `examples/` на `gitHead` версії з репозиторію
`nodemailer/<пакет>`, `CHANGELOG.md` його гілки master, реєстр npm.

Читач `changelog-mixed` додано разом із цим примірником (`engine/readers/changelogmixed.py`): журнал Nodemailer
міняв формат заголовка тричі, і всі три живуть в одному файлі — «## [10.0.16] з посиланням на порівняння і датою в дужках», «## 6.4.2 2019-12-11»,
«## v0.6.1 2014-01-26»; жоден із наявних читачів не бере всіх трьох. Особливості корпусу:

- **Сайт є лише з 2025 року.** Репозиторій `nodemailer-homepage` з'явився в травні 2025, тож для версій до 8.0.8 сайту
  в корпусі немає — лише README, журнал змін і приклади. Сторінки старого сайту (`usage/…`, `smtp/testing`) є в
  знімках 8.x і 9.x.
- **Типи є лише в 10.x.** До того їх давав окремий пакет `@types/nodemailer`, якого цей примірник не бере.
- **Приклади — лише для версій із `gitHead` у реєстрі** (192 із 295). Для старших пакет npm теки `examples/` не
  містить.
- **Вимога до Node (`engines`)** записана в документах реєстру npm: 0.x–2.x — Node 0.6–0.10, 3.x–9.x — Node 6,
  10.x — Node 20.
- **Документ — неповторний текст.** Версії, де файл не змінився, ділять один документ; у рядку `# версія:` стоять усі.
- **Передрелізи не беруться** ні в журналі змін, ні в реєстрі.
- **Ім'я документа несе назву пакета й файла** (поле `name_prefix` у `sources.json`, його розуміють `changelog-mixed`
  і `npm-tarball-files`): `mailparser-3.9.37`, `nodemailer-security-markdown-…`, `nodemailer-types-mailer-types-…`.
  Без нього запис «3.0.0» журналу Nodemailer і «3.0.0» журналу smtp-server, а також README і SECURITY одного пакета
  мали б однакове ім'я, і розділ з однаковим текстом злився б в один фрагмент.
- **Номери ліній у кожного пакета свої.** Фільтр `version` пакета не розрізняє: «3» бере і Nodemailer 3.x, і
  mailparser 3.x, і smtp-server 3.x. Тому опис `search_docs` велить про супутній пакет шукати без `version`, з назвою
  пакета в запиті.
- **smtp-connection і mailcomposer як окремі пакети не розвиваються з 2017 року** (останні — 4.0.2); mailcomposer
  реєстр npm позначає «This project is unmaintained», mailparser до 2.3.0 — «deprecated». Журнал змін mailparser
  починається з 3.6.6, у mailcomposer журналу й прикладів немає.
- **Вимога до Node** у реєстрі: mailparser від 2.0.0 — Node 6; smtp-server 1.x — Node 0.12, від 2.0.0 — Node 6;
  smtp-connection від 3.0.0 — Node 6.

## Межі, про які треба пам'ятати

Документації Node.js, стандартів SMTP і MIME та поштових провайдерів (Gmail, SES, SendGrid) тут немає — лише те, що
про них пишуть сайт Nodemailer і README пакетів. Код бібліотек (`lib/`, `src/`) не входить — лише документація.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/nodemailer-corpus-2026-10-10.tar.gz` (1059 текстів і паспорт). В історії
git текстів немає ніде. Архів лежить лише на цій машині.

**Як повернути тексти** — перед будь-яким оновленням корпусу:

```
tar -xzf ~/archives/docfactory/nodemailer-corpus-2026-10-10.tar.gz -C instances/nodemailer
./df nodemailer smoke
```

**Як знову винести** — після оновлення, коли `vectors` і `smoke` пройшли (вони ж збирають свіжий кеш):

```
ls -l instances/nodemailer/index/passages.json       # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/nodemailer-corpus-РРРР-ММ-ДД.tar.gz -C instances/nodemailer corpus
find instances/nodemailer/corpus -maxdepth 1 -name '*.txt' -delete
gzip -9 -c instances/nodemailer/index/passages.json > instances/nodemailer/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти — лише після того, як архів
звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти» і «Як повернути тексти».

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/nodemailer/index/passages.json.gz`,
далі `./df nodemailer vectors` заллє колекцію Qdrant (кілька хвилин).

## Установка venv

```
cd instances/nodemailer
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env          # впишіть GITHUB_TOKEN і, якщо потрібен крок ask, ANTHROPIC_API_KEY
cd ../..
```

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df nodemailer sources --why   # перелік джерел і білий список
./df nodemailer refresh         # завантажити все задеклароване (близько години; check — 30 хвилин)
./df nodemailer manifest        # оновити паспорт
./df nodemailer setup           # Qdrant чи пошук лише по словах
./df nodemailer vectors         # залити корпус у docs-nodemailer
./df nodemailer smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df nodemailer serve          # порт 8810
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8810/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user nodemailer-docs http://127.0.0.1:8810/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `nodemailer-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
