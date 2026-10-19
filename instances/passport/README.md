# passport — примірник фабрики docfactory

Захищений MCP-сервер, що відповідає на питання про Passport.js — проміжний шар автентифікації для Node.js: застосунок
оголошує стратегії (логін і пароль, JWT, OAuth 2.0 через Google), а `passport.authenticate()` запускає одну з них на
запиті; працює з Express і Connect. Документація — всіх стабільних версій пакета passport (0.1–0.7) і тринадцяти
пакетів стратегій: passport-local, passport-jwt, passport-oauth2, passport-google-oauth20, passport-github2,
passport-facebook, passport-http-bearer, passport-openidconnect, passport-saml, passport-azure-ad, passport-twitter,
passport-discord та passport-strategy (базовий клас будь-якої стратегії). Джерела — офіційний сайт passportjs.org,
README і журнали змін, код і тести кожного тегу репозиторіїв та реєстр npm, лише англійською й лише стабільні версії.
Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../../README.md).

## Навіщо окремий примірник

План NestJS (фаза 4, блок A, день 5) будує вхід на Passport: `LocalStrategy` для пари email і пароль та `JwtStrategy`
для токена із заголовка, а `AuthGuard('jwt')` з `@nestjs/passport` запускає стратегію. Документація самого
`@nestjs/passport` живе в примірнику nestjs, але що саме робить Passport під цим шаром, там не сказано: контракт
функції перевірки (`done(err, user, info)`), параметри `passport.authenticate`, що робить `serializeUser`. Це лежить у
документації Passport і в його коді. До того ж пакет довго стояв на місці й раптом змінився: у 0.6.0 (20.05.2022)
`req.logout()` став асинхронним і вимагає зворотного виклику, а вхід і вихід почали перегенеровувати сесію (захист від
фіксації сесії); 0.5.0 переніс `req.login` та споріднені функції з прототипу запиту в проміжний шар; 0.7.0
(27.11.2023) змінив `assignProperty`. Код, що працює на 0.5, ламається на 0.6, тож відповідь мусить знати версію.

**Що є що.** **Стратегія** (strategy) — об'єкт, що вміє перевірити один вид облікових даних: пароль, JWT, код OAuth.
**Функція перевірки** (verify callback) — функція, яку застосунок передає стратегії; вона шукає користувача й
повертає результат через `done(err, user, info)`. **Сесія** — користувач, збережений між запитами: `serializeUser`
кладе в сесію ідентифікатор, `deserializeUser` за ним відновлює `req.user`. **Нормалізований профіль** — однакова
форма даних про людину від різних постачальників (Google, Facebook): `id`, `displayName`, `emails`, `photos`.
**PKCE** — захист коду авторизації OAuth від перехоплення: клієнт спершу надсилає хеш випадкового рядка, потім сам
рядок.

У яких фазах і днях планів навчання він потрібен — див. [../../docs/learning-map.md](../../docs/learning-map.md).

## Історія пакета

Ця історія пояснює, чому лінії версій такі нерівні й чому версії чотирнадцяти пакетів перетинаються.

| Коли | Пакет | Версії | Що важливо |
|------|-------|--------|------------|
| жовтень 2011 — січень 2014 | passport | 0.1.0–0.1.18 | 19 випусків; перші 13 опубліковано в npm без README |
| січень 2014 — листопад 2015 | passport | 0.2.0–0.3.2 | шість випусків; 0.3.2 теж без README в npm |
| серпень 2017 — грудень 2019 | passport | 0.4.0–0.4.1 | 0.4.1 стояла до 2021 року |
| вересень 2021 — травень 2022 | passport | 0.5.0–0.5.3 | `login`, `logout`, `isAuthenticated` додає проміжний шар, а не прототип запиту (0.5.0 — `initialize()`, 0.5.1 — `authenticate()`); з цих версій починається `CHANGELOG.md` |
| 20.05.2022 | passport | 0.6.0 | `req.logout()` з обов'язковим зворотним викликом, перегенерація сесії при вході й виході, `keepSessionInfo` |
| 27.11.2023 | passport | 0.7.0 | `req.authInfo` виставляється і з `assignProperty`; найновіша, ≈77 % завантажень за тиждень до 19.10.2026 |
| серпень 2013 | passport-strategy | 1.0.0 | єдиний випуск базового класу |
| жовтень 2011 — січень 2019 | passport-facebook | 0.1.0–0.1.6, 1.0.0–1.0.3, 2.0.0–2.1.1, 3.0.0 | 15 випусків; 0.1.0–0.1.4 без README в npm |
| жовтень 2011 — серпень 2013 | passport-http-bearer | 0.1.0–0.1.2, 0.2.0–0.2.1, 1.0.0–1.0.1 | 7 випусків; 1.0.1 від 02.08.2013, ≈282 тис. завантажень за тиждень до 19.10.2026; 0.1.0–0.1.2 і 0.2.0 без README в npm |
| грудень 2014 — березень 2020 | passport-github2 | 0.1.8–0.1.12 | п'ять випусків; тег у репозиторії є лише в v0.1.11 |
| лютий 2013 — лютий 2024 | passport-openidconnect | 0.0.1, 0.0.2, 0.1.0–0.1.2 | 0.1.0 (17.11.2021) читає `profile.username` та `emails` зі стандартних claims і додає `loginHint`, `responseMode`, `claims`; 0.1.1 — `prompt`; 0.1.2 — оновлення залежності `oauth` |
| червень 2012 — жовтень 2022 | passport-saml | 0.0.1–3.2.4 (68 випусків) | усі позначено в npm застарілими: з 4.0 пакет живе як `@node-saml/passport-saml`, тож теги 4.x і 5.x репозиторію в корпус не беруться; код 0.x–1.x — JavaScript у `lib/`, 2.x–3.x — TypeScript у `src/` |
| травень 2013 — квітень 2023 | passport-azure-ad | 0.0.1–4.3.5 (53) | стратегії Microsoft для Azure AD, `OIDCStrategy` і `BearerStrategy`; усі версії позначено застарілими; три передрелізи не беруться |
| жовтень 2011 — січень 2016 | passport-twitter | 0.1.0–0.1.5, 1.0.0–1.0.4 (11) | 0.1.0–0.1.4 без README в npm |
| березень 2016 — червень 2020 | passport-discord | 0.1.1–0.1.4 | усі позначено непідтримуваними; репозиторій заархівовано, тегів лише два |
| жовтень 2011 — березень 2014 | passport-local | 0.1.0–0.1.6, 1.0.0 | 0.1.x без README в npm |
| серпень 2013 — лютий 2024 | passport-oauth2 | 1.0.0–1.8.0 | 12 випусків; 1.6.0 — сховище стану (`store: true`), 1.7.0 — відповіді OAuth у формі (form post), 1.8.0 — оновлення залежності `oauth` |
| листопад 2014 — грудень 2022 | passport-jwt | 0.1.0–4.0.1 | 16 випусків; 4.0.0 піднявся на `jsonwebtoken` 8 через вразливість, тому мажор |
| лютий 2016 — березень 2019 | passport-google-oauth20 | 1.0.0, 2.0.0 | 2.0.0 перейшла з Google+ на Google Sign-in (інший `userinfo`) |

Номери перетинаються густо: 0.1.x є у passport і восьми стратегій, а 1.0.0 — у більшості стратегій (passport-strategy,
passport-local, passport-google-oauth20, passport-oauth2, passport-facebook, passport-http-bearer, passport-twitter,
passport-jwt, passport-saml, passport-azure-ad).

## Скільки цього

Стабільні версії: passport-saml — 68, passport-azure-ad — 53, passport — 33, passport-jwt — 16, passport-facebook —
15, passport-oauth2 — 12, passport-twitter — 11, passport-local — 8, passport-http-bearer — 7, passport-github2 — 5,
passport-openidconnect — 5, passport-discord — 4, passport-google-oauth20 — 2, passport-strategy — 1; разом 240.
Передрелізи (alpha, beta, rc: три в passport-azure-ad) не беруться.

| Шар | Документів | Версій | Звідки |
|-----|-----------:|-------:|--------|
| Сайт passportjs.org: поняття, посібники (пароль, Google, лист із посиланням, Auth0), нормалізований профіль | 50 | 0.7.0 | `sitemap.xml` сайту |
| README passport: кожен неповторний текст один раз, з усіма версіями | 14 + 12 | усі 33 | tarball npm (14) і теги для версій без README (12) |
| Журнал змін passport | 6 | 0.5.0–0.7.0 | `CHANGELOG.md` гілки master |
| `CONTRIBUTING.md` passport | 1 | 0.4.1–0.7.0 | теги |
| Код `lib/` і тести `test/` passport | 156 | 0.1.0–0.7.0 (33) | теги jaredhanson/passport |
| Реєстр npm passport: огляд і лінія 0.x, з вимогами до Node (`engines`) | 2 | усі | registry.npmjs.org |
| passport-strategy: README, код і тести, реєстр | 1 + 6 + 2 | 1.0.0 | npm, теги |
| passport-jwt: README, посібники міграції `docs/`, код і тести, реєстр | 14 + 4 + 56 + 6 | 0.1.0–4.0.1 (16) | npm, теги mikenicholson/passport-jwt; 2.1.1 — коміт публікації |
| passport-oauth2: README, журнал змін, код і тести, реєстр | 8 + 4 + 73 + 2 | 1.0.0–1.8.0 | npm, `CHANGELOG.md`, теги |
| passport-local: README (з тегів для 0.1.x), код і тести, реєстр | 1 + 3 + 32 + 3 | 0.1.0–1.0.0 | npm, теги |
| passport-google-oauth20: README, журнал змін, `CONTRIBUTING.md`, код і тести, реєстр | 2 + 2 + 1 + 15 + 3 | 1.0.0–2.0.0 | npm, теги jaredhanson/passport-google-oauth2 |
| passport-github2: README, код і тести, реєстр | 3 + 16 + 2 | 0.1.8–0.1.12 | npm; тег v0.1.11 і коміти публікації cfsghost/passport-github |
| passport-facebook: README (з тегів для 0.1.0–0.1.4), `CONTRIBUTING.md`, код і тести, реєстр | 7 + 5 + 1 + 65 + 5 | 0.1.0–3.0.0 | npm, теги jaredhanson/passport-facebook |
| passport-http-bearer: README (з тегів для 0.1.0–0.1.2 і 0.2.0), журнал змін, код і тести, реєстр | 2 + 3 + 2 + 29 + 3 | 0.1.0–1.0.1 | npm, `CHANGELOG.md`, теги jaredhanson/passport-http-bearer |
| passport-openidconnect: README, журнал змін, код і тести, реєстр | 3 + 5 + 38 + 2 | 0.0.1–0.1.2 | npm, `CHANGELOG.md`, теги jaredhanson/passport-openidconnect |
| passport-saml: README, журнал змін (з тегу v3.2.4), `docs/` (ADFS), код і тести, реєстр | 41 + 64 + 5 + 138 + 5 | 0.0.1–3.2.4 (код — 65 з 68) | npm, теги node-saml/passport-saml |
| passport-azure-ad: README, `CHANGELOG.md` і `RELEASES.md` з tarball, код і тести, реєстр | 34 + 23 + 1 + 353 + 6 | 0.0.1–4.3.5 (код — 45 з 53) | npm, теги AzureAD/passport-azure-ad |
| passport-twitter: README (з тегів для 0.1.0–0.1.4), код і тести, реєстр | 3 + 4 + 40 + 3 | 0.1.0–1.0.4 | npm, теги jaredhanson/passport-twitter |
| passport-discord: README, код, реєстр | 4 + 5 + 2 | 0.1.1–0.1.4 | npm, теги й коміти публікації nicholastay/passport-discord |

Разом 1401 документ; фрагментів в індексі — 5418 (`expected_passages` у `checks.json`). Фрагменти — це шматки
документів між заголовками, по яких іде пошук. Документ — неповторна редакція файла, і в рядку `# версія:` стоять усі
версії, де він був саме таким; однаковий текст різних версій лягає одним фрагментом з усіма цими версіями. 79 %
фрагментів — код і тести.

Замір `quality` на першому корпусі (шість пакетів, 479 документів): перша десятка (питання своїми словами, без версії)
— по словах 6 із 10, за змістом 7, разом 7; друга, «як модель» (назви Passport, як велить промпт), — 10 із 10, без
дотюнінгу. Три питання першої десятки зливання не знаходить. Два не знаходить жоден спосіб: «побудувати власний
механізм входу» (відповідь — README passport-strategy, але слів «власний» і «механізм» там немає) і «захистити
переспрямування від підроблених запитів» (відповідь — посібник про `state`). Третє, «на яких випусках Node працює
найновіша», пошук за змістом знаходить, а злиття губить: слова запиту збігаються з чужими сторінками про OAuth. Одну
ціль «як модель» виправлено за документацією, а не за видачею: питання про `success`, `fail`, `redirect`, `pass`,
`error` стратегії не має відповіді в README passport-strategy (цих слів там немає) — їх визначає код passport,
`lib/middleware/authenticate.js` та `lib/passport/context/http/actions.js`. `max_per_doc` не заміряно: «як модель» дав
10 із 10 одразу. Після додавання ще чотирьох стратегій (670 документів) замір той самий: 6, 7, 7 і 10 із 10. Після ще
чотирьох (passport-saml, passport-azure-ad, passport-twitter, passport-discord; 1401 документ) перша десятка дала 6,
6, 7, а «як модель» — 9: запит про `engines` і версію 0.7 приніс старі passport-saml 0.7.x. Причина в цілі, а не в
пошуку: єдине місце, де реєстр записує `engines` для passport (`node >= 0.4.0`, з 0.1.0 і досі), — розділ 0.1.x
документа лінії 0, а розділ 0.7.x про `engines` мовчить. Ціль двох питань про Node виправлено на розділ 0.1.x
(перевірено пошуком по тексту документа); «як модель» знову 10 із 10, перша десятка 6, 6, 7.

## Що в цій теці

- `corpus/` — паспорт `index.json`, тобто опис копії: адреса, дата завантаження й сума тексту кожного документа.
  Самих текстів тут немає: корпус в архіві (розділ «Архівний режим» нижче).
- `index/` — кеш фрагментів, з якого сервер підіймається: у git — стиснений `passages.json.gz`, розпакований
  `passages.json` лежить поруч і в git не потрапляє.
- `sources.json` — звідки корпус будується (61 джерело), і водночас білий список для оновлювача.
- `config.json` — порт, колекція Qdrant, модель векторів, пауза між зверненнями, спільні ключі README з тегів
  (`slug_rewrite`) і профіль домену.
- `prompts/` — описи інструментів для моделі, системний промпт власного агента, текст відмови.
- `checks.json` — чим `smoke` і `quality` перевіряють саме цей корпус.
- `.env` — ключ Anthropic (лише для кроку `ask`) і токен GitHub (лише для завантаження корпусу); `.mcp.json` —
  запис HTTP-сервера для Claude Code.

Кроки нижче запускаються з кореня фабрики (`docfactory/`) через `./df passport <крок>`.

## Звідки документація

| Що | Джерело | Читач |
|----|---------|-------|
| Сайт | `https://www.passportjs.org/sitemap.xml`, без дублів `/downloads/html/` | `sitemap-html` |
| README чотирнадцяти пакетів | tarball `registry.npmjs.org/<пакет>/-/<пакет>-X.tgz` | `npm-tarball-files` |
| README версій без README в npm | кореневий `README.md` на тезі (passport 0.1.0–0.1.12, 0.3.2; passport-local 0.1.0–0.1.6; passport-facebook 0.1.0–0.1.4; passport-http-bearer 0.1.0–0.1.2, 0.2.0; passport-twitter 0.1.0–0.1.4) | `ghdocs-history` |
| Журнали змін | `CHANGELOG.md` гілки master п'яти репозиторіїв; passport-saml — з тегу v3.2.4; passport-azure-ad — `CHANGELOG.md` і `RELEASES.md` з tarball | `changelog-keep`, `changelog-v`, `npm-tarball-files` |
| `CONTRIBUTING.md` (passport, passport-google-oauth20, passport-facebook), `docs/` passport-jwt і passport-saml (ADFS) | теги репозиторіїв | `ghdocs-history` |
| Код і тести | `lib/`, `src/` і `test/` на кожному стабільному тезі чотирнадцяти репозиторіїв | `ghcode-history` з `outline: true`; для passport-saml (JavaScript і TypeScript) — `ghcode-history-ts` |
| Реєстр npm | registry.npmjs.org, одне звернення на пакет | `npm-versions` |

Нових читачів примірник не потребував. Особливості корпусу:

- **Версії чотирнадцяти пакетів перетинаються.** «1.0.0» є майже в усіх стратегій, «0.1.x» — у passport і восьми
  стратегій, а `version: "0.7"` бере і passport 0.7, і старі passport-saml 0.7.x (в passport-saml випусків 0.x — 39).
  Назва кожного документа називає пакет, і промпт велить писати ім'я пакета в запиті та дивитися на нього, перш ніж
  називати версію. Лінії для фільтра — з двох чисел (`version_line_depth: 2`).
- **Сайт — один знімок.** passportjs.org не має версій: його сторінки записано під 0.7.0 (останнє оновлення джерела
  сайту `passport/www.passportjs.org` — 16.08.2024, після 0.7.0). Головну сторінку не взято: це лендинг без статті.
  Блоки коду на сторінках сайту втрачають мову (у HTML вона в класі `<code class="js">`, а не в `lang`) — для пошуку
  це байдуже.
- **README — з tarball, а де його там немає, — з тегу.** Чотирнадцять версій passport, сім passport-local, п'ять
  passport-facebook, чотири passport-http-bearer і п'ять passport-twitter опубліковано без README. Їхній текст
  береться з кореня репозиторію на тезі, а правило `slug_rewrite` дає йому той самий ключ, що й README з пакета, тож
  однакові розділи зливаються.
- **Версії без тегу беруться з коміту публікації.** У реєстрі npm запис версії має поле `gitHead`: воно стоїть ключем
  у `tags` для passport-jwt 2.1.1, passport-github2 0.1.8–0.1.10, passport-azure-ad 1.2.1 і 4.0.0, passport-discord
  0.1.3–0.1.4. Коміту passport-github2 0.1.12 у репозиторії немає, тож для неї взято останній коміт master перед днем
  публікації (27.03.2020). Репозиторій cfsghost/passport-github має ще теги v0.1.0–v0.1.5, яким не відповідає жодна
  версія passport-github2 у npm, — вони не беруться.
- **Журнали змін — не в усіх.** passport веде `CHANGELOG.md` лише з 0.5.0, passport-oauth2 — з 1.6.0,
  passport-google-oauth20 — з 1.0.0, passport-http-bearer — з 1.0.0, passport-openidconnect — з 0.0.1; у
  passport-local, passport-jwt, passport-facebook, passport-github2, passport-twitter, passport-discord і
  passport-strategy його немає.
- **passport-saml.** Репозиторій node-saml/passport-saml веде вже пакет `@node-saml/passport-saml` (теги 4.x і 5.x):
  його не беруть, а `CHANGELOG.md` читають з тегу v3.2.4, останнього, що належить passport-saml, — на гілці master
  журнал уже чужий. Код 0.x–1.x — JavaScript у `lib/`, 2.x–3.x — TypeScript у `src/`; їх бере один читач. Версій
  0.0.1, 0.0.2 і 0.0.4 у git немає (ні тегу, ні коміту публікації): їхні README й записи реєстру в корпусі є, коду
  немає. `docs/` — нотатки про ADFS.
- **passport-azure-ad.** Реєстр npm приписує версіям 4.3.1–4.3.5 репозиторій msal-js, а коміти публікації цих версій —
  з нього, і passport-azure-ad там немає; у справжньому репозиторії AzureAD/passport-azure-ad (заархівовано) для них
  немає тегу. Тож код і тести є для 45 версій з 53 (не мають 0.0.1–0.0.3 і 4.3.1–4.3.5), а README, `CHANGELOG.md` і
  `RELEASES.md` береться з tarball кожної версії — вони є для всіх 53.
- **Код і тести поділено на розділи** за оголошеннями й викликами `describe`/`it`: назва тесту стає назвою розділу,
  тож перелік тестів читається як перелік поведінок («logout / existing session but not passing a callback argument»).
- **Вимога до Node (`engines`)** записана в документах реєстру npm: passport 0.1.0 — Node ≥ 0.4.0.
- **Документ — неповторний текст.** Версії, де файл не змінився, ділять один документ; у рядку `# версія:` стоять усі.

## Межі, про які треба пам'ятати

Документації Express, express-session, NestJS і `@nestjs/passport`, інших стратегій (passport-apple, passport-auth0,
passport-steam і решти каталогу сайту), пакета `@node-saml/passport-saml` (наступник passport-saml з версії 4), OAuth
2.0, OpenID Connect і JWT як специфікацій, Auth.js, Better Auth, jose та хешування паролів тут немає. Типи
`@types/passport` не входять. Код — лише на тегах і на комітах публікації: коміти гілки master після 0.7.0 без тегу в
корпус не потрапляють.

## Архівний режим: сервер без корпусу

Корпус примірника в архіві від самого початку: у `corpus/` лежить лише паспорт `index.json`, а сервер підіймається з
кешу фрагментів (`index/passages.json`) і колекції Qdrant; відповіді ті самі до символа — кеш тримає повний текст
кожного фрагмента.

**Де тексти.** В архіві `~/archives/docfactory/passport-corpus-2026-10-19-all14.tar.gz` (26 МБ: 1401 текст, паспорт і
сховище сирого `raw/` — разом 3003 файли; перед видаленням текстів розпакований окремо й звірений із диском — нуль
розбіжностей). В історії git текстів немає ніде. Архів лежить лише на цій машині. Сховище `raw/` після звірки теж
видалено з диска.

**Як винести знову** — після оновлення, коли `vectors` і `smoke` пройшли:

```
ls -l instances/passport/index/passages.json  # кеш має бути на місці й свіжий
tar -czf ~/archives/docfactory/passport-corpus-РРРР-ММ-ДД.tar.gz -C instances/passport corpus raw
find instances/passport/corpus -maxdepth 1 -name '*.txt' -delete
rm -rf instances/passport/raw
gzip -9 -c instances/passport/index/passages.json > instances/passport/index/passages.json.gz
```

і закомітити паспорт `corpus/index.json` та `index/passages.json.gz`. Видаляти тексти й сховище — лише після того, як
архів звірено з диском. Тоді ж видаляють попередній архів, а ім'я нового пишуть у «Де тексти».

**Як повернути тексти** — перед будь-яким оновленням корпусу; разом із ними повертається й сховище `raw/`:

```
tar -xzf ~/archives/docfactory/passport-corpus-2026-10-19-all14.tar.gz -C instances/passport
./df passport smoke
```

**Що перестає працювати.** `check`, `refresh` і `manifest` читають файли, і без текстів їм нема з чим працювати. Дві
перевірки `smoke` чесно пропускаються («корпус в архіві»).

**На іншій машині** після клонування кеш треба розпакувати: `gunzip -k instances/passport/index/passages.json.gz`,
далі `./df passport vectors` заллє колекцію Qdrant (кілька секунд на відеокарті).

## Установка venv

Власний venv цьому примірнику не потрібен: `./df passport …` бере спільне середовище з кореня репозиторію
(`.venvs/cpu` або `.venvs/gpu`). Як його збудувати один раз і як `df` обирає між ними — у кореневому README.md,
розділ «Спільне середовище». Свій `.env` примірник тримає в `instances/passport/.env` (`cp .env.example .env`;
для кроку `ask` потрібен `ANTHROPIC_API_KEY`); `GITHUB_TOKEN`, якого немає в цьому `.env`, береться з кореневого.

## Збирання корпусу

Корпус в архіві: щоб оновити чи перезібрати його, тексти спершу повертають (розділ «Архівний режим»). Для роботи
сервера збирати нічого не треба — потрібен лише `vectors`, якщо колекції ще немає.

```
./df passport sources --why   # перелік джерел і білий список
./df passport refresh         # завантажити все задеклароване (близько 40 хвилин)
./df passport manifest        # оновити паспорт
./df passport setup           # Qdrant чи пошук лише по словах
./df passport vectors         # залити корпус у docs-passport
./df passport smoke           # перевірки
```

Порядок оновлення — у [UPDATE.md](UPDATE.md). Після будь-якого оновлення корпусу `serve` треба перезапустити.

## Сервер під Claude Code

**1. Підняти сервер** в окремому терміналі WSL і лишити жити:

```
cd ~/Projects/docfactory
./df passport serve          # порт 8871
```

Готовий він тоді, коли надрукував кількість фрагментів і адресу `http://127.0.0.1:8871/mcp`.

**2. Додати сервер у Claude Code** — у тому середовищі, де відкрито вікно:

```
claude mcp add --transport http --scope user passport-docs http://127.0.0.1:8871/mcp
```

У WSL і у Windows Claude Code тримає окремі налаштування: вікно VS Code на боці Windows читає
`C:\Users\<ім'я>\.claude.json`, тож команду треба виконати в PowerShell, або додати сервер кнопкою «Add server»
у вікні `/mcp` (тип HTTP, рівень User). Сам сервер з Windows доступний за тією ж адресою: WSL2 прокидає порт.

**3. Перевірити.** `/mcp` — має бути `passport-docs` і два інструменти `search_docs`, `read_section`.

Зупинка — Ctrl+C у терміналі сервера. Решта — scope запису, «address already in use» — так само, як у
[README примірника react-router](../react-router/README.md#спосіб-б--сервер-під-claude-code-http).
