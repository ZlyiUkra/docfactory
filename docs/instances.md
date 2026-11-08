# Каталог примірників

Цей файл збирає `python3 tools/catalog.py`, руками його не правлять. Рядки «Коли піднімати» лежать у
`docs/instance-topics.json`, а все інше береться з теки кожного примірника.

Примірників: 196. Кожен має власний порт, власну назву сервера й власну колекцію Qdrant, тому
їх можна піднімати в будь-якому поєднанні. Скрипт перевіряє це щоразу й без цього файл не запише.
Зайняті порти: 8760–8956, вільний усередині: 8769. Наступний новий: 8957.

## Як обирати

1. Назвіть, що розробляєте. Перегляньте таблиці теми нижче й випишіть примірники, чий рядок підходить.
2. Прочитайте картку кожного кандидата в другій частині файла: там є склад і межі примірника.
3. Кожен сервер запускають окремою командою `./df <примірник> serve` в окремому терміналі.
4. Якщо в картці є рядок «Родина», підніміть і названі там сервери, інакше частину питань не буде кому
   відповісти.

Кожен запущений сервер тримає в пам'яті фрагменти свого примірника, тому чим більше число фрагментів, тим
більше пам'яті він забере. Вектори лежать у контейнері Qdrant, і він має працювати для всіх серверів.

## Вибір за темою

### Мова JavaScript і середовища виконання

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`ecmascript`](#ecmascript) | 8760 | Потрібна точна поведінка мови JavaScript за специфікацією: порядок кроків алгоритму, що змінилося між редакціями, як працює Intl за стандартом. |
| [`typescript`](#typescript) | 8772 | Питання про типи, `tsconfig`, помилки компілятора або про те, в якій версії TypeScript з'явилася можливість. |
| [`nodejs`](#nodejs) | 8796 | Пишете код на Node.js: API модулів, npm, `package.json`, різниця між мажорними версіями, склад релізу. |
| [`v8`](#v8) | 8773 | Питання про рушій під Node.js і Chrome: збирач сміття, оптимізації, прапорці запуску. |
| [`libuv`](#libuv) | 8838 | Питання про цикл подій, пул потоків і ввід-вивід, на яких стоїть Node.js. |
| [`openssl`](#openssl) | 8839 | Питання про `crypto`, `tls`, сертифікати, алгоритми шифрування або C API бібліотеки OpenSSL. |
| [`icu`](#icu) | 8840 | Питання про `Intl`, нормалізацію рядків, сортування за мовою, часові пояси. |
| [`cares`](#cares) | 8841 | Питання про `dns.resolve*` у Node.js або про бібліотеку c-ares. |
| [`llhttp`](#llhttp) | 8842 | Питання про розбір HTTP/1.x у Node.js: помилки парсера, сувора й м'яка перевірка заголовків. |
| [`nghttp2`](#nghttp2) | 8843 | Питання про модуль `http2` у Node.js або про бібліотеку nghttp2. |
| [`deno`](#deno) | 8938 | Пишете для Deno: API середовища, JSR, стандартна бібліотека `@std/*`, відмінності версій. |
| [`bun`](#bun) | 8939 | Пишете для Bun: середовище, менеджер пакетів, тести, збирач, типи `bun-types`. |
| [`wasm`](#wasm) | 8774 | Працюєте з WebAssembly на рівні специфікації: формат, виконання, JavaScript-інтерфейс. |

### Браузер і вебстандарти

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`mdn`](#mdn) | 8784 | Пишете для браузера: Web API, HTML, CSS, JavaScript-довідка, таблиці сумісності браузерів. |
| [`webstandards`](#webstandards) | 8785 | Потрібне точне слово стандарту WHATWG або W3C: HTML, Fetch, CSP, Service Workers. |
| [`webdev`](#webdev) | 8800 | Працюєте над швидкодією сторінки: Core Web Vitals, поради Chrome, бібліотека `web-vitals`. |

### Фреймворки інтерфейсу

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`react`](#react) | 8761 | Пишете на React: хуки, компоненти, серверні компоненти, зміни між версіями. |
| [`nextjs`](#nextjs) | 8779 | Пишете застосунок на Next.js: маршрути, рендеринг, серверні дії, кеш, конфігурація. |
| [`react-router`](#react-router) | 8765 | Маршрути в застосунку React через React Router, зокрема режим фреймворка. |
| [`tanstack-router`](#tanstack-router) | 8822 | Маршрути з перевіркою типів через TanStack Router. |
| [`tanstack-start`](#tanstack-start) | 8941 | Повний застосунок на TanStack Start: серверні функції, рендеринг, розгортання. |
| [`angular`](#angular) | 8927 | Пишете на Angular, Angular Material, CDK або підтримуєте старий AngularJS. |
| [`vue`](#vue) | 8929 | Пишете на Vue: сам фреймворк, Vue Router, Pinia, Vuex, Vue Test Utils. |
| [`vueuse`](#vueuse) | 8930 | Шукаєте готову функцію-композабл для Vue у VueUse або її пакетах-супутниках. |
| [`svelte`](#svelte) | 8931 | Пишете компоненти Svelte: руни, реактивність, інструменти `sv` і `svelte-check`. |
| [`sveltekit`](#sveltekit) | 8932 | Пишете застосунок на SvelteKit: маршрути, завантаження даних, адаптери. |
| [`solidjs`](#solidjs) | 8928 | Пишете на SolidJS, Solid Router, SolidStart або беретеся за Solid 2.0. |
| [`emberjs`](#emberjs) | 8940 | Пишете або підтримуєте застосунок на Ember, Ember Data, Ember CLI. |
| [`alpine`](#alpine) | 8815 | Додаєте поведінку до сторінки через Alpine.js без збирання. |
| [`astro`](#astro) | 8763 | Будуєте сайт на Astro: контентні колекції, острови, інтеграції. |
| [`astro-markdown-pipeline`](#astro-markdown-pipeline) | 8808 | Налаштовуєте обробку Markdown в Astro: remark, rehype, очищення HTML, формули. |
| [`react-native`](#react-native) | 8818 | Пишете мобільний застосунок на React Native. |
| [`expo`](#expo) | 8819 | Збираєте мобільний застосунок через Expo: EAS, модулі, конфігурація. |

### Стан і дані на клієнті

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`redux`](#redux) | 8776 | Керуєте станом через Redux або Redux Toolkit, RTK Query. |
| [`zustand`](#zustand) | 8771 | Керуєте станом через Zustand. |
| [`tanstack-query`](#tanstack-query) | 8767 | Завантажуєте й кешуєте дані сервера через TanStack Query. |
| [`swr`](#swr) | 8817 | Завантажуєте й кешуєте дані сервера через SWR. |
| [`nuqs`](#nuqs) | 8836 | Тримаєте стан інтерфейсу в рядку запиту адреси через nuqs. |
| [`rxjs`](#rxjs) | 8872 | Працюєте з потоками подій через RxJS: оператори, зміни між версіями. |

### Вигляд, форми, анімація, переклади

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`tailwind`](#tailwind) | 8775 | Верстаєте через Tailwind CSS: класи, конфігурація, перехід між версіями. |
| [`shadcn`](#shadcn) | 8799 | Будуєте інтерфейс із компонентів shadcn/ui, Radix UI, Base UI або React Aria. |
| [`motion`](#motion) | 8823 | Анімуєте інтерфейс через Motion, колишній Framer Motion. |
| [`react-hook-form`](#react-hook-form) | 8768 | Робите форми через React Hook Form. |
| [`next-themes`](#next-themes) | 8835 | Перемикаєте світлу й темну тему в Next.js через next-themes. |
| [`tanstack-virtual`](#tanstack-virtual) | 8803 | Показуєте довгі списки через TanStack Virtual. |
| [`react-window`](#react-window) | 8804 | Показуєте довгі списки через react-window. |
| [`i18next`](#i18next) | 8816 | Перекладаєте застосунок через i18next або react-i18next. |
| [`next-intl`](#next-intl) | 8837 | Перекладаєте застосунок Next.js через next-intl. |

### Графіки й 3D

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`d3`](#d3) | 8933 | Малюєте власні графіки через D3 або його модулі. |
| [`observable-plot`](#observable-plot) | 8934 | Хочете швидкий графік через Observable Plot. |
| [`lightweight-charts`](#lightweight-charts) | 8826 | Малюєте фінансові графіки через Lightweight Charts. |
| [`threejs`](#threejs) | 8935 | Робите 3D у браузері через three.js. |
| [`react-three-fiber`](#react-three-fiber) | 8936 | Робите 3D у React через React Three Fiber і drei. |

### Збирання, перевірка коду, тести

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`vite`](#vite) | 8778 | Налаштовуєте збирання через Vite: плагіни, сервер розробки, конфігурація. |
| [`turborepo`](#turborepo) | 8906 | Ведете монорепозиторій через Turborepo. |
| [`eslint`](#eslint) | 8789 | Налаштовуєте перевірку коду через ESLint. |
| [`biome`](#biome) | 8832 | Форматуєте й перевіряєте код через Biome. |
| [`storybook`](#storybook) | 8821 | Описуєте компоненти в Storybook. |
| [`vitest`](#vitest) | 8783 | Пишете тести на Vitest. |
| [`testing-library`](#testing-library) | 8786 | Тестуєте компоненти через Testing Library. |
| [`playwright`](#playwright) | 8788 | Пишете наскрізні тести браузера через Playwright. |
| [`msw`](#msw) | 8787 | Підміняєте мережеві запити в тестах через Mock Service Worker. |
| [`supertest`](#supertest) | 8876 | Тестуєте HTTP-сервер Node.js через supertest. |

### Бекенд на Node.js

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`nestjs`](#nestjs) | 8762 | Пишете бекенд на NestJS: модулі, провайдери, гарди, мікросервіси. |
| [`nestjs-cls`](#nestjs-cls) | 8879 | Передаєте контекст запиту або транзакцію в NestJS через nestjs-cls. |
| [`nestjs-pino`](#nestjs-pino) | 8880 | Пишете журнали в NestJS через nestjs-pino. |
| [`express`](#express) | 8791 | Пишете сервер на Express. |
| [`express-rate-limit`](#express-rate-limit) | 8812 | Обмежуєте частоту запитів до Express. |
| [`fastify`](#fastify) | 8844 | Пишете сервер на Fastify. |
| [`trpc`](#trpc) | 8903 | З'єднуєте клієнт і сервер TypeScript через tRPC. |
| [`next-safe-action`](#next-safe-action) | 8905 | Робите серверні дії Next.js із перевіркою вхідних даних через next-safe-action. |
| [`zod`](#zod) | 8770 | Перевіряєте дані через Zod, зокрема перехід з версії 3 на 4. |
| [`class-validator`](#class-validator) | 8874 | Перевіряєте об'єкти через декоратори class-validator, зазвичай у NestJS. |
| [`class-transformer`](#class-transformer) | 8875 | Перетворюєте звичайні об'єкти на класи через class-transformer. |
| [`jsonschema`](#jsonschema) | 8855 | Пишете JSON Schema або перевіряєте дані через Ajv. |
| [`orval`](#orval) | 8883 | Генеруєте клієнт API з OpenAPI через orval. |
| [`openapi-typescript`](#openapi-typescript) | 8884 | Генеруєте типи й клієнт з OpenAPI через openapi-typescript. |
| [`helmet`](#helmet) | 8809 | Ставите заголовки безпеки в Express через Helmet. |
| [`csrf-csrf`](#csrf-csrf) | 8881 | Захищаєте Express від підробки міжсайтових запитів через csrf-csrf. |
| [`nodemailer`](#nodemailer) | 8810 | Надсилаєте пошту з Node.js через Nodemailer. |
| [`socketio`](#socketio) | 8793 | Робите двосторонній зв'язок реального часу через Socket.IO. |
| [`ws`](#ws) | 8877 | Робите сервер або клієнт WebSocket на Node.js через ws. |
| [`partysocket`](#partysocket) | 8820 | Потрібен клієнт WebSocket із повторним підключенням PartySocket. |

### Вхід користувачів і безпека

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`auth`](#auth) | 8797 | Робите вхід користувачів через Better Auth, NextAuth.js або Auth.js. |
| [`clerk`](#clerk) | 8766 | Робите вхід користувачів через керований сервіс Clerk. |
| [`passport`](#passport) | 8871 | Робите вхід через Passport.js та його стратегії. |
| [`casl`](#casl) | 8882 | Описуєте права доступу через CASL. |
| [`jose`](#jose) | 8834 | Підписуєте або перевіряєте JWT, JWE, JWK через бібліотеку jose. |
| [`iron-session`](#iron-session) | 8833 | Тримаєте сесію в зашифрованому cookie через iron-session. |
| [`argon2`](#argon2) | 8814 | Хешуєте паролі через argon2 або `@node-rs/argon2`. |
| [`bcrypt`](#bcrypt) | 8873 | Хешуєте паролі через bcrypt або bcryptjs. |
| [`owasp`](#owasp) | 8795 | Перевіряєте безпеку застосунку: шпаргалки OWASP, Top 10, вимоги ASVS. |

### Бази даних і ORM

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`postgresql`](#postgresql) | 8792 | Пишете запити або адмініструєте сервер PostgreSQL. |
| [`postgres-image`](#postgres-image) | 8807 | Запускаєте PostgreSQL в офіційному образі Docker: змінні, томи, початкові скрипти. |
| [`node-postgres`](#node-postgres) | 8805 | Звертаєтеся до PostgreSQL із Node.js через пакет `pg`. |
| [`mysql`](#mysql) | 8952 | Пишете запити до MySQL, адмініструєте сервер або звертаєтеся до нього через драйвер, зокрема `mysql2`. Працює лише на цій машині. |
| [`mariadb`](#mariadb) | 8953 | Пишете запити до MariaDB, налаштовуєте Galera чи MaxScale або звертаєтеся до сервера через конектор, зокрема пакет `mariadb`. |
| [`postgrator`](#postgrator) | 8806 | Виконуєте міграції PostgreSQL через postgrator. |
| [`drizzle`](#drizzle) | 8830 | Працюєте з базою через Drizzle ORM. |
| [`prisma`](#prisma) | 8831 | Працюєте з базою через Prisma. |
| [`typeorm`](#typeorm) | 8868 | Працюєте з базою через TypeORM. |
| [`mikro-orm`](#mikro-orm) | 8885 | Працюєте з базою через MikroORM. |
| [`supabase`](#supabase) | 8764 | Будуєте застосунок на Supabase: база, вхід, сховище, функції. |
| [`sqlserver`](#sqlserver) | 8864 | Працюєте із SQL Server: мова T-SQL, адміністрування, життєвий цикл версій. |
| [`mongodb`](#mongodb) | 8850 | Працюєте із сервером MongoDB, mongosh або його інструментами. |
| [`node-mongodb`](#node-mongodb) | 8851 | Звертаєтеся до MongoDB із Node.js через офіційний драйвер. |
| [`mongoose`](#mongoose) | 8852 | Описуєте моделі MongoDB через Mongoose. |
| [`redis`](#redis) | 8845 | Працюєте із сервером Redis: команди, збереження, реплікація, Sentinel, Cluster. |
| [`ioredis`](#ioredis) | 8846 | Звертаєтеся до Redis із Node.js через ioredis. |
| [`node-redis`](#node-redis) | 8847 | Звертаєтеся до Redis із Node.js через офіційний клієнт node-redis. |
| [`bullmq`](#bullmq) | 8848 | Робите черги завдань через BullMQ або Bull, зокрема в NestJS. |
| [`upstash`](#upstash) | 8849 | Використовуєте керовані сервіси Upstash: Redis, QStash, Vector. |

### Черги повідомлень

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`kafka`](#kafka) | 8886 | Працюєте із сервером Apache Kafka: налаштування, теми, групи споживачів. |
| [`kafkajs`](#kafkajs) | 8887 | Звертаєтеся до Kafka з Node.js через KafkaJS. |
| [`confluent-kafka-javascript`](#confluent-kafka-javascript) | 8888 | Звертаєтеся до Kafka з Node.js через клієнт Confluent. |
| [`platformatic-kafka`](#platformatic-kafka) | 8889 | Звертаєтеся до Kafka з Node.js через `@platformatic/kafka`. |
| [`rabbitmq`](#rabbitmq) | 8890 | Працюєте із сервером RabbitMQ: обміни, черги, налаштування. |
| [`amqplib`](#amqplib) | 8891 | Звертаєтеся до RabbitMQ із Node.js через amqplib. |
| [`amqp-connection-manager`](#amqp-connection-manager) | 8892 | Потрібне автоматичне перепідключення до RabbitMQ через amqp-connection-manager. |
| [`golevelup-nestjs-rabbitmq`](#golevelup-nestjs-rabbitmq) | 8893 | Підключаєте RabbitMQ до NestJS через модуль Golevelup. |
| [`nats`](#nats) | 8894 | Працюєте із сервером NATS або JetStream. |
| [`nats-js`](#nats-js) | 8895 | Звертаєтеся до NATS із JavaScript через `nats` або `@nats-io/*`. |

### Мова Go й її бібліотеки

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`go`](#go) | 8913 | Пишете на Go: мова, стандартна бібліотека, інструменти, зміни між версіями. |
| [`learning-go`](#learning-go) | 8914 | Вчите Go за книжками: Learning Go, Go by Example, 100 Go Mistakes, Go 101. |
| [`sqlc`](#sqlc) | 8916 | Генеруєте код Go із запитів SQL через sqlc. |
| [`pgx`](#pgx) | 8915 | Звертаєтеся до PostgreSQL із Go через pgx. |
| [`goose`](#goose) | 8917 | Виконуєте міграції бази в Go через goose. |
| [`golang-migrate`](#golang-migrate) | 8918 | Виконуєте міграції бази в Go через golang-migrate. |
| [`oapi-codegen`](#oapi-codegen) | 8919 | Генеруєте код Go з OpenAPI через oapi-codegen. |
| [`golang-x`](#golang-x) | 8920 | Використовуєте пакети `golang.org/x`: argon2, bcrypt, errgroup, rate. |
| [`golang-jwt`](#golang-jwt) | 8921 | Працюєте з JWT у Go через golang-jwt. |
| [`coder-websocket`](#coder-websocket) | 8922 | Робите WebSocket у Go через coder/websocket. |
| [`river`](#river) | 8924 | Робите черги завдань у Go через River. |
| [`testcontainers-go`](#testcontainers-go) | 8923 | Запускаєте контейнери в тестах Go через Testcontainers. |
| [`golangci-lint`](#golangci-lint) | 8925 | Налаштовуєте перевірку коду Go через golangci-lint. |

### .NET

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`dotnet`](#dotnet) | 8866 | Пишете на .NET: бібліотека класів, середовище, інструмент `dotnet`. |
| [`csharp`](#csharp) | 8878 | Питання про мову C#: синтаксис, можливості за версіями. |
| [`aspnetcore`](#aspnetcore) | 8862 | Пишете вебзастосунок на ASP.NET Core. |
| [`entityframework`](#entityframework) | 8865 | Працюєте з базою через Entity Framework. |
| [`nuget`](#nuget) | 8869 | Створюєте або підключаєте пакети NuGet. |
| [`dotnet-testing`](#dotnet-testing) | 8870 | Пишете тести .NET: бібліотеки тестування й підміни. |
| [`testcontainers-dotnet`](#testcontainers-dotnet) | 8867 | Запускаєте контейнери в тестах .NET через Testcontainers. |

### Python і обробка даних

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`python`](#python) | 8944 | Пишете на Python: мова, стандартна бібліотека, PEP, pip, uv, Poetry. |
| [`data-cleaning`](#data-cleaning) | 8949 | Чистите або об'єднуєте таблиці через pandas, openpyxl чи RapidFuzz. |
| [`xgboost`](#xgboost) | 8954 | Навчаєте дерева рішень, градієнтний бустинг чи випадковий ліс через XGBoost: параметри, GPU, формат моделі, прогноз. |
| [`lightgbm`](#lightgbm) | 8955 | Навчаєте градієнтний бустинг чи випадковий ліс через LightGBM: параметри та їхні псевдоніми, GPU, прогноз, зміни між версіями. |
| [`numpy`](#numpy) | 8956 | Працюєте з масивами NumPy: сигнатури функцій, dtype і правила приведення типів, broadcasting, що змінилося між версіями 1.3–2.5. |

### PHP

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`php`](#php) | 8951 | Пишете на PHP або ставите пакети через Composer: мова, функції, перехід між версіями, RFC, `composer.json`. |

### Сервери, контейнери, розгортання

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`linux`](#linux) | 8782 | Адмініструєте Linux: команди, сторінки man, налаштування Ubuntu. |
| [`docker`](#docker) | 8780 | Працюєте з Docker: Dockerfile, Compose, рушій, збирання образів. |
| [`kubernetes`](#kubernetes) | 8781 | Працюєте з Kubernetes: об'єкти, `kubectl`, адміністрування, підготовка до CKAD чи CKA. |
| [`gvisor`](#gvisor) | 8859 | Ізолюєте контейнери через gVisor і `runsc`. |
| [`nvidia-container-toolkit`](#nvidia-container-toolkit) | 8861 | Даєте контейнерам доступ до відеокарти NVIDIA. |
| [`nginx`](#nginx) | 8798 | Налаштовуєте nginx як вебсервер або зворотний проксі. |
| [`certbot`](#certbot) | 8811 | Отримуєте й поновлюєте сертифікати TLS через Certbot. |
| [`cloudflare`](#cloudflare) | 8937 | Працюєте з Cloudflare: Workers, Pages, DNS, wrangler. |
| [`oracle-cloud`](#oracle-cloud) | 8825 | Розгортаєте на Oracle Cloud: безплатний рівень, обчислення, мережа, OKE. |
| [`github-actions`](#github-actions) | 8794 | Пишете процеси CI в GitHub Actions. |
| [`argocd`](#argocd) | 8907 | Розгортаєте в Kubernetes за підходом GitOps через Argo CD. |
| [`flux`](#flux) | 8908 | Розгортаєте в Kubernetes за підходом GitOps через Flux. |
| [`sealed-secrets`](#sealed-secrets) | 8909 | Зберігаєте секрети Kubernetes у git через Sealed Secrets. |

### Спостереження за застосунком

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`prometheus`](#prometheus) | 8910 | Збираєте метрики через Prometheus, Alertmanager або prom-client. |
| [`grafana`](#grafana) | 8902 | Будуєте панелі й сповіщення в Grafana. |
| [`loki`](#loki) | 8911 | Збираєте журнали через Loki. |
| [`opentelemetry`](#opentelemetry) | 8853 | Додаєте трасування й метрики через OpenTelemetry. |
| [`sentry`](#sentry) | 8802 | Відстежуєте помилки JavaScript через Sentry. |

### Сайти, контент, сервіси для бізнесу

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`wordpress`](#wordpress) | 8946 | Будуєте або підтримуєте сайт на WordPress: хуки, Gutenberg, WP-CLI, плагіни форм. |
| [`civicrm`](#civicrm) | 8950 | Ведете контакти, внески чи членство організації через CiviCRM. |
| [`payload`](#payload) | 8901 | Будуєте сайт на CMS Payload. |
| [`sanity`](#sanity) | 8899 | Будуєте сайт на CMS Sanity. |
| [`contentful`](#contentful) | 8904 | Будуєте сайт на CMS Contentful. |
| [`sender`](#sender) | 8945 | Надсилаєте розсилки через Sender.net. |
| [`resend`](#resend) | 8896 | Надсилаєте пошту через сервіс Resend. |
| [`react-email`](#react-email) | 8897 | Верстаєте листи через React Email. |
| [`uploadthing`](#uploadthing) | 8900 | Приймаєте файли від користувачів через UploadThing. |
| [`stripe`](#stripe) | 8863 | Приймаєте платежі через Stripe. |
| [`payments-pt`](#payments-pt) | 8948 | Приймаєте платежі в Португалії через ifthenpay, Easypay, Eupago чи SIBS: MB WAY, Multibanco, дебет. |
| [`rgpd`](#rgpd) | 8947 | Обробляєте персональні дані в Португалії: RGPD, закони, рішення CNPD, настанови EDPB. |

### Штучний інтелект

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`anthropic-api`](#anthropic-api) | 8860 | Викликаєте Claude через API: моделі, ціни, інструменти, кеш запитів. |
| [`claude-code`](#claude-code) | 8926 | Налаштовуєте Claude Code, Agent SDK, навички чи плагіни. |
| [`vercel-ai-sdk`](#vercel-ai-sdk) | 8898 | Будуєте застосунок із моделями через AI SDK від Vercel. |
| [`ollama`](#ollama) | 8854 | Запускаєте локальні моделі через Ollama. |

### Обробка файлів

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`ffmpeg`](#ffmpeg) | 8813 | Обробляєте відео чи аудіо через FFmpeg. |
| [`tesseract`](#tesseract) | 8858 | Розпізнаєте текст на зображеннях через Tesseract. |
| [`libreoffice`](#libreoffice) | 8856 | Перетворюєте документи через LibreOffice без вікна або працюєте з UNO API. |
| [`doc-tools`](#doc-tools) | 8857 | Обробляєте файли через poppler та інші інструменти для PDF і документів. |

### Блокчейн і біржі

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`wagmi`](#wagmi) | 8827 | Підключаєте гаманець у застосунку React через Wagmi. |
| [`viem`](#viem) | 8828 | Звертаєтеся до Ethereum із TypeScript через Viem. |
| [`foundry`](#foundry) | 8829 | Пишете й тестуєте смартконтракти через Foundry. |
| [`binance-spot`](#binance-spot) | 8801 | Працюєте з API спотової торгівлі Binance. |
| [`kraken-spot`](#kraken-spot) | 8824 | Працюєте з API спотової торгівлі Kraken. |

### Навчальні матеріали й архітектура

| Примірник | Порт | Коли піднімати |
|---|---:|---|
| [`patterns`](#patterns) | 8777 | Обираєте шаблон проєктування або рефакторинг за refactoring.guru. |
| [`frontend-architecture`](#frontend-architecture) | 8790 | Обираєте будову фронтенду: Feature-Sliced Design та інші підходи. |
| [`htdp`](#htdp) | 8912 | Читаєте книжку How to Design Programs або виконуєте її вправи в Racket. |
| [`agent-harness-course`](#agent-harness-course) | 8942 | Вчитеся будувати оболонку для агентів за курсом Agent Harness Course. |
| [`devops-core-course`](#devops-core-course) | 8943 | Виконуєте лабораторні курсу DevOps Core Course. |

## Картки

<!-- тема: Мова JavaScript і середовища виконання -->

### ecmascript

**Коли піднімати.** Потрібна точна поведінка мови JavaScript за специфікацією: порядок кроків алгоритму, що змінилося між редакціями, як працює Intl за стандартом.

**Порт** 8760, сервер `ecma-spec`. Підняти: `./df ecmascript serve`. Адреса: `http://127.0.0.1:8760/mcp`.

**Обсяг.** Документів: 28 678, фрагментів: 25 305.

**Опис.**

Перший примірник фабрики: захищений MCP-сервер, що відповідає на питання про специфікацію ECMAScript. Пошук — з
практики модуля 5, чотири шари захисту — з модуля 6. Ця тека тримає самі дані домену; код спільний і лежить у
`../../server/` (сервер, агент, шари) та `../../common/` (пошук). Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Loaded right now: every published edition of ECMA-262 (ES1 1997, ES2 1998, ES3 1999, ES5 2009, ES5.1 2011, ES2015 to
ES2026) and the ES2027 draft, every edition of ECMA-402 (Intl 1.0 2012, 2015 to 2026) and its draft, the TC39 tables
of finished proposals with the edition year of each, ECMA-404 (JSON), ECMA-414 and the free documents the Intl
specification builds on -- RFC 4647 and the Unicode reports UAX #29, UTS #10 and UTS #35. If something about
JavaScript or its internationalization is not found here, it is unlikely to be anywhere in these standards.

**Далі в [README](../instances/ecmascript/README.md):** Що в цій теці; Редакції; Архівний режим: сервер без корпусу;
Установка venv; Спосіб А — власний захищений агент (усі чотири шари); Спосіб Б — сервер під Claude Code (HTTP); Пошук
за змістом (необов'язковий); Оновлення корпусу; Межа захисту, коротко.

### typescript

**Коли піднімати.** Питання про типи, `tsconfig`, помилки компілятора або про те, в якій версії TypeScript з'явилася можливість.

**Порт** 8772, сервер `typescript-docs`. Підняти: `./df typescript serve`. Адреса: `http://127.0.0.1:8772/mcp`.

**Обсяг.** Документів: 2 170, фрагментів: 8 520.

**Опис.**

Дванадцятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про TypeScript за офіційною
документацією всіх його версій — текстом сайту typescriptlang.org на кожен стабільний реліз від 1.4 (2015) до поточної
7.x, README кожної версії npm (зокрема нічних збірок, beta, rc й insiders), нотатками релізів, README й `CHANGES.md`
нативного порту `typescript-go` і реєстром версій npm. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official TypeScript documentation -- the text of the typescriptlang.org documentation as it stood at
every stable release since 2015 (the TypeScript-Handbook repository until August 2020, then the TypeScript-Website
repository: handbook, reference, modules reference, declaration files, project configuration, release notes, the
tsconfig options reference, the playground handbook and the glossary), each distinct text once with all the versions
it belongs to; the README of every release on npm, nightly builds included; the GitHub release notes of TypeScript and
of typescript-go, the native port behind 7.0, with its README and CHANGES.md; and the npm registry list of every
published version with its date, dist-tag, entry points and dependencies. Frameworks, bundlers, linters and type
packages from DefinitelyTyped are not here; if something about TypeScript is not found in these documents, it is
unlikely to be anywhere in its official documentation.

**Межі.**

Тут немає документації JavaScript (для мови — примірник `ecmascript`), Node.js, фреймворків і збирачів,
typescript-eslint і пакетів типів DefinitelyTyped (`@types/…`). Блог devblogs.microsoft.com/typescript і Bluesky
свідомо не взято: анонси повторюють release notes. Нічні збірки, beta, rc й insiders — не релізи: текст, що є лише в
них, міг так і не вийти, і промпт велить моделі казати про це прямо.

**Далі в [README](../instances/typescript/README.md):** Навіщо вся історія; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code; На іншій машині.

### nodejs

**Коли піднімати.** Пишете код на Node.js: API модулів, npm, `package.json`, різниця між мажорними версіями, склад релізу.

**Порт** 8796, сервер `nodejs-docs`. Підняти: `./df nodejs serve`. Адреса: `http://127.0.0.1:8796/mcp`.

**Обсяг.** Документів: 2 784, фрагментів: 30 621.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `cares-docs` (8841), `icu-docs`
(8840), `libuv-docs` (8838), `llhttp-docs` (8842), `nghttp2-docs` (8843), `openssl-docs` (8839), `v8-docs` (8773).

**Опис.**

Тридцять шостий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Node.js і npm. Тут довідник API
Node.js усіх мажорів 10–26 (парних і непарних) з історією кожної функції, розклад ліній і склад кожного релізу,
Notable Changes кожної версії, посібники nodejs.org/learn, сторінки nodejs.org про кінець підтримки й безпекові
релізи, doc/contributing, undici, журнали змін npm 6–12, документація CLI npm 12, 11, 10, 9, 8, 7 і 6 (команди,
`package.json`, `package-lock.json`, `.npmrc`, scripts, workspaces) і посібники docs.npmjs.com про реєстр, публікацію
й безпеку пакетів. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі
дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents about Node.js and npm in English -- the Node.js API reference of every major from 10 to 26 with the history
of every function, the nodejs.org/learn guides, the npm CLI documentation of npm 12 to 6 (every command, package.json,
package-lock.json, .npmrc, scripts, workspaces) and the docs.npmjs.com guides on the registry, publishing and securing
packages; the release schedule and every release with the versions of npm, V8, libuv and OpenSSL it ships, the Notable
Changes of each Node.js release, the npm CLI changelog, undici and the doc/contributing guides. Frameworks built on
Node.js, other runtimes, other package managers, and the documentation of libuv, OpenSSL, ICU, c-ares, llhttp and
nghttp2 themselves are not here. This set is NOT complete on its own. Node.js is built from components that have their
own documentation sets, each served by a separate server of this project: v8-docs (V8, 8773), libuv-docs (event loop
and thread pool, 8838), openssl-docs (crypto and TLS, 8839), icu-docs (Intl, 8840), cares-docs (dns, 8841),
llhttp-docs (http parser, 8842), nghttp2-docs (http2, 8843). When a question goes below the Node.js API into one of
these, use that server; if it is not connected, say so instead of answering from memory.

**Межі.**

Тут немає довідника API Node до 10 (розклад і перелік релізів 0.x і 4–9 є), переліку комітів у журналах змін,
вбудованих у Node бібліотек (libuv, OpenSSL, ICU, c-ares, llhttp, nghttp2 — їхні примірники ще попереду; V8 —
примірник `v8`), блогу nodejs.org поза розділами про безпеку, мажори й розклад, образів Docker `node`, інших
рантаймів (Deno, Bun) і менеджерів пакетів (pnpm, Yarn), а також фреймворків на Node — вони в своїх примірниках
(`express`, `nestjs`, `nextjs`, `socketio`).

**Далі в [README](../instances/nodejs/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Межі,
про які треба пам'ятати; Екосистема: піднімати разом; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### v8

**Коли піднімати.** Питання про рушій під Node.js і Chrome: збирач сміття, оптимізації, прапорці запуску.

**Порт** 8773, сервер `v8-docs`. Підняти: `./df v8 serve`. Адреса: `http://127.0.0.1:8773/mcp`.

**Обсяг.** Документів: 1 026, фрагментів: 3 437.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `cares-docs` (8841), `icu-docs`
(8840), `libuv-docs` (8838), `llhttp-docs` (8842), `nghttp2-docs` (8843), `nodejs-docs` (8796), `openssl-docs` (8839).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про рушій JavaScript і WebAssembly V8 за його офіційним сайтом v8.dev —
документацією, блогом і поясненнями можливостей — в усіх редакціях сайту від V8 7.0 (жовтень 2018) до поточної 15.4.
Поруч — неофіційні навчальні нотатки й код `danbev/learning-v8`: як V8 влаштований усередині, показано на вихідному
коді й тестах C++ API. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official V8 site v8.dev -- the documentation (v8.dev/docs), the blog (v8.dev/blog, the "V8 release
vX.Y" posts included) and the JavaScript and WebAssembly feature explainers (v8.dev/features, with the feature support
table), as the site stood at every V8 version since 7.0 (October 2018), each distinct text once with every version and
year it belongs to; and the unofficial learning-v8 notes and C++ embedding code by danbev
(github.com/danbev/learning-v8), with no labels. Chromium, Node.js, Blink, the V8 source code, its C++ API reference
and the web tools at v8.github.io/tools are not here -- only what v8.dev and the learning-v8 notes say about them; if
something about V8 is not found in these documents, it is unlikely to be anywhere on v8.dev. This set is one component
of the Node.js family: the servers nodejs-docs (Node.js API and npm), v8-docs, libuv-docs, openssl-docs, icu-docs,
cares-docs, llhttp-docs and nghttp2-docs cover the other components and are meant to be connected together -- when a
question belongs to another component, name its server.

**Межі.**

Тут немає самої мови JavaScript (для неї — примірник `ecmascript`), Node.js, Chromium, Blink, вихідного коду V8 і
довідника його C++ API — лише те, що про них кажуть v8.dev і нотатки learning-v8 (вони цитують шматки вихідного коду
й показують кілька класів API в тестах, але довідником не є). Допис блогу описує V8 на мить написання: порада 2017
року може вже не діяти, і промпт велить моделі називати дату, на яку спирається відповідь.

**Далі в [README](../instances/v8/README.md):** Навіщо історія; Скільки цього; Що в цій теці; Звідки документація;
Межі, про які треба пам'ятати; Родина Node: піднімати разом; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code; На іншій машині.

### libuv

**Коли піднімати.** Питання про цикл подій, пул потоків і ввід-вивід, на яких стоїть Node.js.

**Порт** 8838, сервер `libuv-docs`. Підняти: `./df libuv serve`. Адреса: `http://127.0.0.1:8838/mcp`.

**Обсяг.** Документів: 594, фрагментів: 1 322.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `cares-docs` (8841), `icu-docs`
(8840), `llhttp-docs` (8842), `nghttp2-docs` (8843), `nodejs-docs` (8796), `openssl-docs` (8839), `v8-docs` (8773).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про libuv — бібліотеку C, на якій стоїть цикл подій Node.js: цикл
(`uv_loop_t`, `uv_run`), handles і requests, потоки й мережа, файлова система, пул потоків, процеси, сигнали, таймери.
Документація — Sphinx-сайт docs.libuv.org кожної стабільної версії від 0.10.2 до 1.53.0, README, перелік підтримуваних
платформ, політика безпеки і ChangeLog кожного випуску. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the libuv documentation -- the Sphinx documentation at every stable release from 0.10.2, the README,
supported platforms and security policy, and the ChangeLog of every release. The documentation of Node.js, V8, OpenSSL
and other libraries is not here; if something about libuv is not found in these documents, it is unlikely to be in its
official documentation. This set is one component of the Node.js family: the servers nodejs-docs (Node.js API and
npm), v8-docs, libuv-docs, openssl-docs, icu-docs, cares-docs, llhttp-docs and nghttp2-docs cover the other components
and are meant to be connected together -- when a question belongs to another component, name its server.

**Межі.**

Документації Node.js (вона в `nodejs`), V8 (`v8`), OpenSSL, ICU й інших вбудованих бібліотек, а також обгорток libuv в
інших мовах (Luv, libuv-rs) тут немає. Приклади коду `docs/code` не беруться: вони підключені до сторінок директивою
`literalinclude`, яку розбір Sphinx не розкриває; коментарів у вихідному коді libuv теж немає.

**Далі в [README](../instances/libuv/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Node: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### openssl

**Коли піднімати.** Питання про `crypto`, `tls`, сертифікати, алгоритми шифрування або C API бібліотеки OpenSSL.

**Порт** 8839, сервер `openssl-docs`. Підняти: `./df openssl serve`. Адреса: `http://127.0.0.1:8839/mcp`.

**Обсяг.** Документів: 6 833, фрагментів: 24 527.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `cares-docs` (8841), `icu-docs`
(8840), `libuv-docs` (8838), `llhttp-docs` (8842), `nghttp2-docs` (8843), `nodejs-docs` (8796), `v8-docs` (8773).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про OpenSSL: команди `openssl` (req, x509, verify, s_client, pkcs12,
dgst, enc …), файли конфігурації (`openssl.cnf`, `x509v3_config`, `fips_config`), довідник C API бібліотек libcrypto і
libssl (`EVP_*`, `SSL_*`, `X509_*`, `BIO_*`, `OSSL_PROVIDER_*`) і оглядові сторінки концепцій (провайдери, модуль
FIPS, міграція 1.1.1 → 3.0). Документація — сторінки man кожного випуску від 0.9.8 до 4.0.3. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the OpenSSL documentation -- the manual pages (commands, C API, configuration formats, concepts) of every
release of the lines 0.9.8 to 4.0. The documentation of Node.js, other TLS libraries and the TLS and X.509 standards
is not here; if something about OpenSSL is not found in these documents, it is unlikely to be in its official
documentation. This set is one component of the Node.js family: the servers nodejs-docs (Node.js API and npm),
v8-docs, libuv-docs, openssl-docs, icu-docs, cares-docs, llhttp-docs and nghttp2-docs cover the other components and
are meant to be connected together -- when a question belongs to another component, name its server.

**Межі.**

Документації Node.js, V8, libuv, ICU, TLS і X.509 як стандартів, а також інших бібліотек TLS (BoringSSL, LibreSSL,
GnuTLS) теж немає.

**Далі в [README](../instances/openssl/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Node: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### icu

**Коли піднімати.** Питання про `Intl`, нормалізацію рядків, сортування за мовою, часові пояси.

**Порт** 8840, сервер `icu-docs`. Підняти: `./df icu serve`. Адреса: `http://127.0.0.1:8840/mcp`.

**Обсяг.** Документів: 8 300, фрагментів: 51 997.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `cares-docs` (8841), `libuv-docs`
(8838), `llhttp-docs` (8842), `nghttp2-docs` (8843), `nodejs-docs` (8796), `openssl-docs` (8839), `v8-docs` (8773).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про ICU (International Components for Unicode) — бібліотеку, на якій
стоять `Intl` у Node.js і браузерах: рядки й Unicode, локалі, форматування чисел, дат і повідомлень, колація
(сортування), межі слів і речень, перетворення кодувань, транслітерація, календарі й часові пояси. Документація —
посібник користувача (як він був до ICU 65 і від 65.1 до 78.3), довідник C/C++ API (коментарі Doxygen публічних і
внутрішніх заголовків ICU4C кожного випуску 1.4.0–78.3) і дизайн-документи. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the ICU documentation -- the User Guide (releases 65.1 to 78.3) and the Doxygen comments of the public
C/C++ headers of ICU4C (every release from 1.4.0 to 78.3). The documentation of Node.js `Intl`, the Unicode Standard
and CLDR is not here; if something about ICU is not found in these documents, it is unlikely to be in its official
documentation. This set is one component of the Node.js family: the servers nodejs-docs (Node.js API and npm),
v8-docs, libuv-docs, openssl-docs, icu-docs, cares-docs, llhttp-docs and nghttp2-docs cover the other components and
are meant to be connected together -- when a question belongs to another component, name its server.

**Межі.**

- Посібник у git є лише з 65.1; для випусків 1.4–64 відповідь стоїть на заголовках і старому посібнику (він один, без
  історії).
- ICU 1.2.x–1.3.x не взято: публічних заголовків там ще немає. Реалізація (`.cpp`) не береться — лише заголовки.
- Java-класи ICU4J — лише в посібнику; довідника ICU4J тут немає.
- CLDR і Unicode Standard — окремі специфікації, тут їх нема; дизайн-документи містять лише технічні звіти UTC, які ICU
  реалізує (TR10, TR15, TR18, TR29).

**Далі в [README](../instances/icu/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Node: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### cares

**Коли піднімати.** Питання про `dns.resolve*` у Node.js або про бібліотеку c-ares.

**Порт** 8841, сервер `cares-docs`. Підняти: `./df cares serve`. Адреса: `http://127.0.0.1:8841/mcp`.

**Обсяг.** Документів: 3 170, фрагментів: 3 464.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `icu-docs` (8840), `libuv-docs`
(8838), `llhttp-docs` (8842), `nghttp2-docs` (8843), `nodejs-docs` (8796), `openssl-docs` (8839), `v8-docs` (8773).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про c-ares — асинхронний DNS-резолвер на C, на якому стоять
`dns.resolve*` і `dns.Resolver` у Node.js: канал (`ares_channel_t`), `ares_init_options`, `ares_getaddrinfo`,
`ares_query`, `ares_process`, сервери й тайм-аути, розбір відповідей (`ares_dns_record`). Документація — сторінки man
кожної функції, заголовки, README і посібники, нотатки кожного випуску (зміни, виправлені вразливості), вихідний код і
тести всіх випусків від 1.1.0 до 1.34.8. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`;
ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the c-ares documentation -- manual pages, public headers, README and guides, release notes and the
library sources of every release from 1.1.0 to 1.34.8. The documentation of Node.js `dns`, the OS resolver and other
DNS libraries is not here; if something about c-ares is not found in these documents, it is unlikely to be in its
official documentation. This set is one component of the Node.js family: the servers nodejs-docs (Node.js API and
npm), v8-docs, libuv-docs, openssl-docs, icu-docs, cares-docs, llhttp-docs and nghttp2-docs cover the other components
and are meant to be connected together -- when a question belongs to another component, name its server.

**Межі.**

Документації Node.js `dns`, системного резолвера (`getaddrinfo(3)` libc) і інших DNS-бібліотек тут немає. Окремого
репозиторію дизайн-документів у c-ares немає: їхню роль несуть `DEVELOPER-NOTES.md`, `FEATURES.md` і `TODO`.

**Далі в [README](../instances/cares/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Node: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### llhttp

**Коли піднімати.** Питання про розбір HTTP/1.x у Node.js: помилки парсера, сувора й м'яка перевірка заголовків.

**Порт** 8842, сервер `llhttp-docs`. Підняти: `./df llhttp serve`. Адреса: `http://127.0.0.1:8842/mcp`.

**Обсяг.** Документів: 777, фрагментів: 1 529.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `cares-docs` (8841), `icu-docs`
(8840), `libuv-docs` (8838), `nghttp2-docs` (8843), `nodejs-docs` (8796), `openssl-docs` (8839), `v8-docs` (8773).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про llhttp — парсер HTTP/1.x на C, на якому стоїть модуль `http`
Node.js (він замінив `http_parser`): ініціалізація й виконання (`llhttp_init`, `llhttp_execute`), зворотні виклики
`on_*`, коди помилок `HPE_*`, прапорці лояльності (`lenient`), chunked, upgrade, pipelining, випадки request
smuggling. Документація — README, згенерований публічний заголовок, вихідний код генератора й автомата, тести (сирі
HTTP-повідомлення з очікуваними подіями розбору) і нотатки випусків усіх версій від 1.0.1 до 9.4.3. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the llhttp documentation -- README, the public header, generator and native sources, generated parser,
tests and release notes of every release from 1.0.1 to 9.4.3. The documentation of Node.js `http`, HTTP/2 and other
HTTP parsers is not here; if something about llhttp is not found in these documents, it is unlikely to be in its
official documentation. This set is one component of the Node.js family: the servers nodejs-docs (Node.js API and
npm), v8-docs, libuv-docs, openssl-docs, icu-docs, cares-docs, llhttp-docs and nghttp2-docs cover the other components
and are meant to be connected together -- when a question belongs to another component, name its server.

**Межі.**

Документації модуля `http` Node.js, HTTP/2 (nghttp2) і інших парсерів (`http-parser`, picohttpparser) тут немає. Окремого
сайту документації в llhttp немає: його роль виконує README.

**Далі в [README](../instances/llhttp/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Node: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### nghttp2

**Коли піднімати.** Питання про модуль `http2` у Node.js або про бібліотеку nghttp2.

**Порт** 8843, сервер `nghttp2-docs`. Підняти: `./df nghttp2 serve`. Адреса: `http://127.0.0.1:8843/mcp`.

**Обсяг.** Документів: 6 337, фрагментів: 8 619.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `cares-docs` (8841), `icu-docs`
(8840), `libuv-docs` (8838), `llhttp-docs` (8842), `nodejs-docs` (8796), `openssl-docs` (8839), `v8-docs` (8773).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про nghttp2 — реалізацію HTTP/2 і HPACK на C, на якій стоїть модуль
`http2` Node.js: сесії (`nghttp2_session_*`), подання запитів і відповідей (`nghttp2_submit_*`), зворотні виклики,
коди помилок `NGHTTP2_ERR_*`, керування потоком, SETTINGS, динамічна таблиця HPACK, утиліти `nghttp`, `nghttpd`,
`nghttpx` (проксі) і `h2load` (навантаження). Документація — посібник програміста, туторіали, довідкові сторінки
утиліт, публічний заголовок з коментарями Doxygen, вихідний код бібліотеки й утиліт, тести, приклади й нотатки кожного
випуску від 0.1.0 до 1.70.0. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека
тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the nghttp2 documentation -- guides, manual pages, the public header with the C API reference, library
and tool sources, tests, examples and release notes of every release from 0.1.0 to 1.70.0. The documentation of
Node.js `http2`, HTTP/1.x parsers and other HTTP/2 libraries is not here; if something about nghttp2 is not found in
these documents, it is unlikely to be in its official documentation. This set is one component of the Node.js family:
the servers nodejs-docs (Node.js API and npm), v8-docs, libuv-docs, openssl-docs, icu-docs, cares-docs, llhttp-docs
and nghttp2-docs cover the other components and are meant to be connected together -- when a question belongs to
another component, name its server.

**Межі.**

Документації модуля `http2` Node.js, HTTP/1.x (llhttp) і інших бібліотек HTTP/2 тут немає. `third-party/` (стороннє) і
`fuzz`-корпуси не беруться.

**Далі в [README](../instances/nghttp2/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Node: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### deno

**Коли піднімати.** Пишете для Deno: API середовища, JSR, стандартна бібліотека `@std/*`, відмінності версій.

**Порт** 8938, сервер `deno-docs`. Підняти: `./df deno serve`. Адреса: `http://127.0.0.1:8938/mcp`.

**Обсяг.** Документів: 6 727, фрагментів: 30 557.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Deno за його документацією: сайт docs.deno.com (Runtime,
конфігурація `deno.json`, дозволи, TypeScript, сумісність із Node.js і npm, перехід з Node.js, довідник CLI, тести,
лінтер, форматер, робочі простори, Web API, Deno KV, Deno Deploy, Subhosting, Sandbox, правила лінтера, посібники й
приклади) на кожну мінорну 1.37–2.9, старий посібник 1.0–1.36, довідник API з файлів типів `lib.deno.*.d.ts` кожної
мінорної 1.0–2.9, журнал змін і релізи, запис npm пакета `deno`, усі дописи блогу deno.com, документація реєстру JSR і
стандартна бібліотека `@std/*`. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека
тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Deno documentation -- the docs.deno.com site at every minor 1.37–2.9, the manual of Deno 1.0–1.36,
the API types lib.deno.*.d.ts of every minor 1.0–2.9, Releases.md and the GitHub release notes, the npm record of the
deno package, every deno.com blog post, the JSR documentation, and the standard library @std/* at every stable minor
of each package, plus every 0.x minor of the twelve packages without a stable release, marked unstable. The JSR site
and the blog carry no version. Prereleases are not here.

**Далі в [README](../instances/deno/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### bun

**Коли піднімати.** Пишете для Bun: середовище, менеджер пакетів, тести, збирач, типи `bun-types`.

**Порт** 8939, сервер `bun-docs`. Підняти: `./df bun serve`. Адреса: `http://127.0.0.1:8939/mcp`.

**Обсяг.** Документів: 4 753, фрагментів: 27 077.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Bun за його документацією: bun.com/docs (runtime, `bunfig.toml`,
сумісність із Node.js, Web API, `Bun.serve`, `Bun.file`, `Bun.spawn`, `bun:sqlite`, SQL, Redis, S3, FFI, shell
`Bun.$`; менеджер пакетів `bun install`, робочі простори, каталоги, `bunx`; збирач `bun build`, плагіни, виконувані
файли `--compile`; тести `bun test`; `bun lint` і його правила; посібники) на кожен сталий патч 1.0.0–1.4.4 і останній
патч кожної мінорної 0.1–0.8, довідник API з файлів типів `packages/bun-types` на ті самі версії, релізи GitHub,
записи npm пакетів `bun`, `bun-types` і `@types/bun`, теги образу Docker `oven/bun` і всі дописи блогу bun.com. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Bun documentation -- bun.com/docs at every stable patch 1.0.0–1.4.4 and the last patch of every minor
0.1–0.8, the API types of packages/bun-types at the same releases, the GitHub release notes, the npm records of bun,
bun-types and @types/bun, the Docker Hub tags of oven/bun, and every bun.com blog post. The blog carries no version.
Canary builds and prereleases are not here.

**Далі в [README](../instances/bun/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### wasm

**Коли піднімати.** Працюєте з WebAssembly на рівні специфікації: формат, виконання, JavaScript-інтерфейс.

**Порт** 8774, сервер `wasm-docs`. Підняти: `./df wasm serve`. Адреса: `http://127.0.0.1:8774/mcp`.

**Обсяг.** Документів: 846, фрагментів: 6 923.

**Опис.**

Чотирнадцятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про WebAssembly за офіційною
специфікацією всіх її видань — Core Specification, JavaScript Interface і Web API у виданнях 1.0, 2.0, 3.0 та в
поточній чернетці — і за обговореннями в issues репозиторію WebAssembly/spec. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the WebAssembly specification -- the Core Specification, the JavaScript Interface and the Web API, each
in its 1.0 edition (W3C Recommendation, 2019), 2.0 edition (W3C Candidate Recommendation, 2024), 3.0 edition (2025)
and the current editor's draft, one document per top-level chapter with numbered sections and the formulas written out
as text, each distinct text once with all the editions it belongs to; and every issue of the WebAssembly/spec
repository with all its comments. Engines (V8, SpiderMonkey, Wasmtime), toolchains (Emscripten, wasm-bindgen, wabt),
WASI and proposals that have not been merged are not here.

**Межі.**

Тут немає реалізацій (V8 — окремий примірник `v8`, SpiderMonkey, Wasmtime), інструментів (Emscripten,
wasm-bindgen, wabt, Binaryen), WASI і пропозицій, ще не злитих у специфікацію (репозиторій WebAssembly/proposals).
Pull request-и репозиторію специфікації свідомо не взято. Додатки Metadata і Legacy Exceptions з того ж сайту не
взято: це не частина видань.

**Далі в [README](../instances/wasm/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Межі, про
які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code; На
іншій машині.

<!-- тема: Браузер і вебстандарти -->

### mdn

**Коли піднімати.** Пишете для браузера: Web API, HTML, CSS, JavaScript-довідка, таблиці сумісності браузерів.

**Порт** 8784, сервер `mdn-docs`. Підняти: `./df mdn serve`. Адреса: `http://127.0.0.1:8784/mcp`.

**Обсяг.** Документів: 76 853, фрагментів: 179 893.

**Опис.**

Двадцять четвертий примірник фабрики: захищений MCP-сервер, що відповідає на питання про саму вебплатформу —
JavaScript, Web API, CSS, HTML, HTTP, доступність, безпеку й продуктивність вебу — за документацією MDN Web Docs
англійською. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of MDN Web Docs in English -- twenty sections of developer.mozilla.org: Web APIs, JavaScript, CSS, HTML,
HTTP, accessibility, the Learn web development course, the glossary, performance, security, privacy, progressive web
apps, media, URI, SVG, WebAssembly, WebDriver, XML, MathML and games. Each page is the text a reader of the site sees,
with its specifications and a Baseline summary of browser support. Besides the pages, browser-compat-data: one
document per feature with the first version of every browser, Node. Firefox release notes, the documentation of
browser extensions, the MDN blog and other languages are not here.

**Межі.**

Тут немає документації бібліотек і фреймворків (React, Next.js, NestJS, TypeScript — окремі примірники), Node.js і
його API, а також текстів самих стандартів (WHATWG, W3C,
IETF) — розділ Specifications лише називає їх і дає адресу. Стандарти записано в карті навчання «на потім».

**Далі в [README](../instances/mdn/README.md):** Навіщо; Скільки цього; Як влаштований документ; browser-compat-data;
Що в цій теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### webstandards

**Коли піднімати.** Потрібне точне слово стандарту WHATWG або W3C: HTML, Fetch, CSP, Service Workers.

**Порт** 8785, сервер `webstandards-docs`. Підняти: `./df webstandards serve`. Адреса: `http://127.0.0.1:8785/mcp`.

**Обсяг.** Документів: 1 175, фрагментів: 15 161.

**Опис.**

Двадцять п'ятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про те, чого вимагають самі
вебстандарти, — за їхніми текстами англійською: WHATWG, W3C, RFC та чернетки IETF, OpenID Connect, OpenAPI, JSON
Schema й ERC. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of web standards in English -- the WHATWG living standards (HTML, DOM, Fetch, URL, Streams, WebSockets and
eleven more), W3C specifications (CSP 3, Fetch Metadata, Referrer Policy, Permissions Policy, Secure Contexts, Mixed
Content, Service Workers, Web App Manifest, Push API, WAI-ARIA 1.2, ARIA in HTML, WCAG 2.2 with Understanding,
Techniques and the ARIA Authoring Practices Guide), IETF RFCs on HTTP, cookies, WebSocket, HSTS, problem details, JWT,
OAuth 2.0, PKCE and Argon2, OpenID Connect Core and Discovery, OpenAPI 3.1.1, JSON Schema 2020-12 and ERC-20, ERC-721
and ERC-4361. Browser support tables, tutorials, HTTP/2, HTTP/3, TLS, CSS and ECMAScript specifications are not here.

**Межі.**

Тут немає підтримки браузерами (вона в `mdn`), підручників, HTTP/2 і HTTP/3, TLS, специфікацій CSS і ECMAScript
(остання — у примірнику `ecmascript`). IEEE 754 і стандарт SQL не взято: їхні тексти платні. Документація бібліотек
(Passport, Auth.js, socket.io, viem) — окремі примірники чи поза фабрикою.

**Далі в [README](../instances/webstandards/README.md):** Навіщо; Скільки цього; Як влаштований документ; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### webdev

**Коли піднімати.** Працюєте над швидкодією сторінки: Core Web Vitals, поради Chrome, бібліотека `web-vitals`.

**Порт** 8800, сервер `webdev-docs`. Підняти: `./df webdev serve`. Адреса: `http://127.0.0.1:8800/mcp`.

**Обсяг.** Документів: 1 407, фрагментів: 16 148.

**Опис.**

Сороковий примірник фабрики: захищений MCP-сервер, що відповідає на питання про те, як робити сайти швидкими,
доступними й надійними. Тут web.dev — сайт команди Chrome у Google: курси Learn, статті й блог, — і бібліотека
`web-vitals`, якою міряють метрики швидкості в браузерах справжніх відвідувачів: README кожного стабільного випуску
від 0.1.0 до 6.2.3, журнал змін і настанови з переходу на v4, v5 і v6. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents in English -- web.dev, the site of the Chrome team on building for the web (the Learn courses, the articles,
among them Core Web Vitals and the other metrics with their thresholds, and the blog), and the web-vitals JavaScript
library (the README of every stable release 0.1.0 to 6.2.3, the changelog and the guides for upgrading to v4, v5 and
v6). Version lines (web-vitals only; web. MDN, the specifications and the Chrome DevTools and Lighthouse documentation
are not here.

**Межі.**

Тут немає перекладів web.dev, відео й подкастів сайту (shows), кейсів компаній (case-studies), розсилки, тестів
курсів, а також developer.chrome.com — документації Chrome DevTools, Lighthouse і розширень Chrome. Довідник HTML, CSS
і Web API — у примірнику `mdn`, специфікації — у `webstandards`, React і Next.js — у своїх примірниках.

**Далі в [README](../instances/webdev/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Версії
у відповіді; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

<!-- тема: Фреймворки інтерфейсу -->

### react

**Коли піднімати.** Пишете на React: хуки, компоненти, серверні компоненти, зміни між версіями.

**Порт** 8761, сервер `react-docs`. Підняти: `./df react serve`. Адреса: `http://127.0.0.1:8761/mcp`.

**Обсяг.** Документів: 3 657, фрагментів: 12 803.

**Опис.**

Другий примірник фабрики: захищений MCP-сервер, що відповідає на питання про React за офіційною документацією всіх
його версій — від першого публічного релізу 0.3 (травень 2013) до поточної 19.3. Код спільний і лежить у
`../../engine/` (завантаження корпусу), `../../server/` (сервер, агент, шари) та `../../common/` (пошук); ця тека
тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official React documentation -- react.dev (19.3) and its blog, 18.react.dev (18.3.1), the old-style
docs of 18.2.0, 17.0.2 and 16.14.0, the documentation as it stood on the release day of every line in between
(16.1-16.13, 18.0-18.1, 19.0-19.2), the docs kept in the React repository for 16.0 and every minor line from 0.3 to
15.6, the blog archive back to 2013, CHANGELOG.md split into one document per version, the GitHub release notes of
every release, the react.dev versions page that maps them, and the initial public commit of May 29, 2013. React
Native, Next.js and other projects built on React are not here; if something about React itself is not found in these
documents, it is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/react/README.md):** Навіщо окремий примірник; Що в цій теці; Звідки документація;
Версії у відповідях; Архівний режим: сервер без корпусу; Установка venv; Спосіб А — власний захищений агент (усі
чотири шари); Спосіб Б — сервер під Claude Code (HTTP); Пошук за змістом; Оновлення корпусу; Межа захисту, коротко.

### nextjs

**Коли піднімати.** Пишете застосунок на Next.js: маршрути, рендеринг, серверні дії, кеш, конфігурація.

**Порт** 8779, сервер `nextjs-docs`. Підняти: `./df nextjs serve`. Адреса: `http://127.0.0.1:8779/mcp`.

**Обсяг.** Документів: 15 332, фрагментів: 47 061.

**Опис.**

Дев'ятнадцятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Next.js за офіційною
документацією всіх версій — обох роутерів, App Router і Pages Router, — поясненнями помилок, README кожної версії
пакета `next` і дев'яти пакетів поруч, нотатками релізів, реєстром версій npm, блогом nextjs.org, прикладами з
репозиторію, шаблонами з галереї Vercel і сторінкою showcase. Код спільний і лежить у `../../engine/`, `../../server/`
та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official documentation of Next.js -- the docs and errors folders of vercel/next.js on every tag where
they exist (docs from 9.1.7, errors from 5.x), canary builds included, each distinct text once with all the versions
it belongs to, the App Router and the Pages Router as separate documents; the README of every version of next (the
whole documentation before 9.1) and of nine packages around it; the GitHub release notes of every release and canary;
the npm registry list of every published version, with dates, dist-tags, dependencies and peer dependencies; the
nextjs.org blog; the official examples of the repository at 16.3.8, with code; the Next.js templates of the Vercel
gallery; and the showcase. React itself, the Vercel platform documentation and third-party libraries are not here.

**Межі.**

Тут немає документації самого React (окремий примірник `react`), платформи Vercel (звідти лише галерея шаблонів),
Turborepo і Turbopack як окремих інструментів, бібліотек навколо (Auth.js, Prisma, SWR) та курсу nextjs.org/learn.
Issues і GitHub Discussions свідомо не взято: це рецепти окремих проблем, а не документація.

**Довгі переліки версій.** Оглядовий документ реєстру пакета `next` несе всі 3 968 версій, а кожен п'ятий фрагмент
документації — понад сорок. Пошук показує сорок найновіших (з фільтром `version` — сорок із тієї лінії), а поруч
`versions_total` — скільки їх усього, і `versions_oldest` — найстарішу; повний перелік віддає `read_section`. Без
цього відповідь на питання про реєстр сягала 147 тисяч символів і не влазила в ліміт клієнта; тепер — близько 10
тисяч. Сам пошук і фільтр версії працюють по всіх версіях, обрізається лише показ.

**Далі в [README](../instances/nextjs/README.md):** Навіщо; Скільки цього; Два роутери; Мітки версій і canary; Пакети;
Що в цій теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code; На іншій машині.

### react-router

**Коли піднімати.** Маршрути в застосунку React через React Router, зокрема режим фреймворка.

**Порт** 8765, сервер `react-router-docs`. Підняти: `./df react-router serve`. Адреса: `http://127.0.0.1:8765/mcp`.

**Обсяг.** Документів: 4 125, фрагментів: 12 465.

**Опис.**

Шостий примірник фабрики: захищений MCP-сервер, що відповідає на питання про React Router за офіційною документацією
всіх його версій — від 0.x (2014) до поточної 8.4, разом з кожним pre-release, nightly й experimental-збіркою, — за
довідником API, журналами змін і нотатками релізів. Код спільний і лежить у `../../engine/` (завантаження корпусу),
`../../server/` (сервер, агент, шари) та `../../common/` (пошук); ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official React Router documentation -- the docs kept in the repository on every one of its 820 tags
(every release from 0.0 to the current line, every pre-release, beta and release candidate, and the nightly and
experimental builds), each distinct text once with all the versions it belongs to; the TypeDoc API reference of
api.reactrouter.com for 8.4.0 and 7.18.4; the release notes in CHANGELOG.md from v6.0.0 on, the changelog of the
react-router package, and the GitHub release notes of every release. React itself, Remix before React Router 7,
Next.js and other routers are not here; if something about React Router is not found in these documents, it is
unlikely to be anywhere in its official documentation.

**Межі.**

Документації React, Remix до його злиття з React Router 7, Next.js, TanStack Router та інших бібліотек тут немає —
лише згадки про них у тексті роутера. Для React поруч є окремий примірник `react`. Nightly й experimental — не
релізи: текст, що є лише в них, міг так і не вийти, і промпт велить моделі казати про це прямо.

**Далі в [README](../instances/react-router/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Межі, про які треба пам'ятати; Токен GitHub; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Спосіб А — власний захищений агент (усі чотири шари); Спосіб Б — сервер під Claude Code (HTTP).

### tanstack-router

**Коли піднімати.** Маршрути з перевіркою типів через TanStack Router.

**Порт** 8822, сервер `tanstack-router-docs`. Підняти: `./df tanstack-router serve`. Адреса: `http://127.0.0.1:8822/mcp`.

**Обсяг.** Документів: 7 954, фрагментів: 23 576.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про TanStack Router і TanStack Start за офіційною документацією всіх
їхніх сталих версій — від 1.0.0 (2023) до поточної 1.x — і про їхнього попередника React Location (1.0.0–3.7.4,
2019–2022). Окрім документації, він знає приклади, журнали змін і нотатки релізів пакетів, записи блогу TanStack та
історію версій кожного пакета в реєстрі npm, зокрема пакетів, яких уже немає. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md). **Start тепер є окремим примірником.** З 02.11.2026 документація TanStack Start живе
в [`tanstack-start`](../instances/tanstack-start/README.md), свіжіша й без сторінок Router. Тут вона поки лишається
станом на 11.10.2026 і під час наступного оновлення цього примірника вилучається
([UPDATE.md](../instances/tanstack-router/UPDATE.md)).

**Склад (так його описано моделі, англійською).**

Documents of the official TanStack Router and TanStack Start documentation -- the docs kept in the repository on every
stable release tag (1.0.0 to the current 1.x), each distinct text once with all the versions it belongs to; the docs
of its predecessor React Location (1.0.0 to 3.7.4); the example apps; the changelogs of all @tanstack/* router and
start packages; the GitHub release notes; the TanStack blog posts about Router and Start; and the npm registry history
of every package, current and retired. x and 3.x are React Location only). TanStack Query, Table, Virtual and the
frameworks themselves are not here; if something about TanStack Router or Start is not found in these documents, it is
unlikely to be anywhere in their official documentation.

**Межі.**

TanStack Query, Table, Form, Virtual і решти TanStack тут немає, як і React Router, Remix чи Next.js. Solid Router і
Solid Start 2.0 ще в rc — їхньої документації немає, лише рядки передрелізів у документах реєстру npm. Сторінки
`how-to/drafts` і службовий `docs/AGENTS.md` на сайт не йдуть і не беруться. Сторінки прикладів сайту React Location
(`docs/src/pages/examples/*.md`) — лише рамка CodeSandbox; код тих самих прикладів є в `rl-examples`.

**Далі в [README](../instances/tanstack-router/README.md):** Навіщо вся історія; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### tanstack-start

**Коли піднімати.** Повний застосунок на TanStack Start: серверні функції, рендеринг, розгортання.

**Порт** 8941, сервер `tanstack-start-docs`. Підняти: `./df tanstack-start serve`. Адреса: `http://127.0.0.1:8941/mcp`.

**Обсяг.** Документів: 4 370, фрагментів: 13 342.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про TanStack Start за його документацією: серверні функції
(`createServerFn`), `createMiddleware`, серверні маршрути, SSR, вибірковий SSR, статичне попереднє рендерення, режим
SPA, змінні оточення, автентифікація, розгортання. Тут сайт tanstack.com/start на день знімка, документація з
репозиторію на кожну мінорну 1.49–1.169, README пакетів від 1.31, приклади, навички для агентів із самих пакетів,
дописи блогу про Start, журнали змін і нотатки релізів, реєстр npm. Код спільний — у `../../engine/`, `../../server/`
та `../../common/`; ця тека тримає самі дані домену. Загальний опис фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official TanStack Start documentation -- the site as it stands today; the docs from the repository on
the last release of every minor version, each distinct text once with all the versions it belongs to; the READMEs of
@tanstack/react-start, solid-start and start; the example apps; the agent skills shipped in the packages; the TanStack
blog posts about Start; the changelogs of all Start packages; the GitHub release notes; and the npm registry history
of every Start package, current and retired. TanStack Router, Query, Table and the frameworks themselves are not here;
if something about TanStack Start is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Далі в [README](../instances/tanstack-start/README.md):** Навіщо окремий примірник; Скільки цього; Що тут означає
«сталий»; Що в цій теці; Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### angular

**Коли піднімати.** Пишете на Angular, Angular Material, CDK або підтримуєте старий AngularJS.

**Порт** 8927, сервер `angular-docs`. Підняти: `./df angular serve`. Адреса: `http://127.0.0.1:8927/mcp`.

**Обсяг.** Документів: 33 504, фрагментів: 96 473.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Angular — фреймворк Google для вебзастосунків (компоненти й
шаблони, сигнали, впровадження залежностей, маршрутизатор, форми, HttpClient, рендеринг на сервері, тестування, CLI),
а також про AngularJS 1.x, Angular Material і CDK. Документація — кожної стабільної мінорної лінії: Angular 2.0–22.2
(67 ліній), AngularJS 1.0 і 1.2–1.8, Material і CDK 5.0–22.2. Джерела — офіційні сайти angular.dev, angular.io усіх
мажорів, v2.angular.io і code.angularjs.org, репозиторії angular/angular, angular/components, angular/angular-cli,
angular/angular.js і angular/material2-docs-content, пакети й реєстр npm; лише англійською й лише стабільні версії.
Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Angular documentation -- the guides of angular.dev and angular.io for every stable minor line (4.0 to
22.2) with their example code, the API and CLI reference of every major site (4 to 22), the site v2.angular.io (2.4),
the AngularJS documentation of 1.0 and 1.2 to 1.8, Angular Material and the CDK (5.0 to 22.2), the old Angular CLI
documentation (1.0 to 8.3), the changelogs of angular/angular, angular/components, angular/angular-cli and
angular/angular.js, the README of every repository tag and the npm registry history of the @angular packages and of
angular (AngularJS). Prereleases, RxJS, NgRx, Nx and other third-party libraries are not here.

**Межі.**

- Посібники Angular 2.0–2.3 недосяжні: тексти 2.x жили в репозиторії angular.io без тегів, шаблонами Jade. Є сайт
  v2.angular.io (2.4.10) і довідник API з коду кожної мінорної 2.0–2.4.
- Довідник API Material і CDK 6.0–6.3 — з пакета npm, а не з сайту: розмітка інша, ніж у сторінок 5.x і 6.4+ (символ —
  документ, як у довіднику API Angular з коду), тож редакції цих ліній з 5.x і 6.4+ в одне місце видачі не складаються.
- Сторінки сайтів — один знімок на мажор (остання мінорна); версії інших мінорних — з тегів і довідника з коду.
- Нотатки релізів GitHub angular/angular і angular/components не беруться: їх складено з того самого журналу змін.
- Передрелізів (next, rc, beta), RxJS, NgRx, Nx, Ionic, AngularFire та інших сторонніх бібліотек тут немає; RxJS має
  свій примірник `rxjs`.

**Далі в [README](../instances/angular/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### vue

**Коли піднімати.** Пишете на Vue: сам фреймворк, Vue Router, Pinia, Vuex, Vue Test Utils.

**Порт** 8929, сервер `vue-docs`. Підняти: `./df vue serve`. Адреса: `http://127.0.0.1:8929/mcp`.

**Обсяг.** Документів: 5 452, фрагментів: 16 953.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `vueuse-docs` (8930).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Vue.js — прогресивний фреймворк інтерфейсів (реактивність,
компоненти, однофайлові компоненти й `<script setup>`, шаблони й директиви, композиційні функції, вбудовані
компоненти, рендеринг на сервері), а також про офіційні бібліотеки екосистеми: Vue Router, Pinia, Vuex і Vue Test
Utils. Документація — на кожен стабільний реліз: сайт vuejs.org на релізи vue 3.0–3.5, v2.vuejs.org на релізи 2.0–2.7,
давній vuejs.org на релізи 0.7–1.0; документація Router, Pinia, Vuex і Test Utils — з тегу кожної мінорної версії.
Єдиний нестабільний шар — журнал змін передрелізу Vue 3.6 (альфа, бета, реліз-кандидат) з позначкою в назві кожного
документа. Джерела — репозиторії vuejs/docs, vuejs/v2.vuejs.org, vuejs/core, vuejs/vue, vuejs/router,
vuejs/vue-router, vuejs/pinia, vuejs/vuex, vuejs/test-utils, vuejs/vue-test-utils, vuejs/v3-migration-guide,
vuejs/blog, vuejs/rfcs, пакети й реєстр npm; лише англійською. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Vue documentation -- vuejs.org as it stood at every stable release of vue 3.0 to 3.5, v2.vuejs.org at
every stable release 2.0 to 2.7, the old vuejs.org of 0.7 to 1.0, the Vue 3 migration guide, the blog and the accepted
RFCs, the documentation of Vue Router, vue-router, Pinia, Vuex and Vue Test Utils at the last release of every minor
line, the changelogs (with the Vue 3.6 pre-release line, not stable) and GitHub release notes, the README of every
stable version and the npm registry history of vue, vue-router, pinia, vuex, @vue/test-utils, create-vue, vue-tsc,
@vitejs/plugin-vue and eslint-plugin-vue. Other prereleases and third-party libraries are not here. This set is part
of the Vue family: vue-docs (this one: Vue itself, Vue Router, Pinia, Vuex and Vue Test Utils) and vueuse-docs
(VueUse, the collection of Vue composition utilities, with @vueuse/motion, @vueuse/gesture, @vueuse/sound and
@vueuse/head) are meant to be connected together -- when a question belongs to the other member, name its server.

**Межі.**

- Найраніший знімок давнього сайту — 0.7.1: репозиторій сайту починається 04.01.2014, і раніших версій він не описує.
- Довідник API Router у репозиторії лежить лише в 4.1–4.5 (далі його генерують під час збирання сайту); у Pinia 0.x
  документації в репозиторії не було — лише README.
- Порожні записи журналів (версії без нотаток — 58 записів, здебільшого Vue 2 і Vuex) не пишуться.
- Посібник переходу, блог і RFC — без версії: пошук із фільтром версії їх не бачить.
- Переклади, Nuxt, Vuetify, Quasar, PrimeVue та інші сторонні бібліотеки, сам Vite і передрелізи, крім 3.6, тут не
  входять. VueUse — у примірнику `vueuse` тієї самої родини Vue (розділ нижче). Плагін `@vitejs/plugin-vue` — лише
  README і реєстр: його журнал пише заголовки в `<small>`, яких читач журналів не впізнає.

**Далі в [README](../instances/vue/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Родина Vue: піднімати разом; Архівний режим: сервер без
корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### vueuse

**Коли піднімати.** Шукаєте готову функцію-композабл для Vue у VueUse або її пакетах-супутниках.

**Порт** 8930, сервер `vueuse-docs`. Підняти: `./df vueuse serve`. Адреса: `http://127.0.0.1:8930/mcp`.

**Обсяг.** Документів: 3 237, фрагментів: 6 226.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `vue-docs` (8929).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про VueUse — збірку композиційних функцій для Vue: стан і сховище
браузера, елементи й DOM, сенсори, мережа, час і анімація, помічники `watch`, утиліти, компоненти й директиви,
інтеграції (axios, Fuse.js, focus-trap, Sortable, universal-cookie тощо), помічники Vue Router, RxJS, Firebase,
Electron і математика. Документація — з тегу кожної стабільної мінорної версії 4.0–15.0 і на кожен реліз ліній 2.x і
3.x 2020 року. Окремі проєкти організації з власною нумерацією — `@vueuse/motion` (анімації), `@vueuse/gesture`
(жести), `@vueuse/sound` і `@vueuse/head`. Джерела — репозиторії vueuse/vueuse (він же сайт vueuse.org),
vueuse/motion, vueuse/gesture, vueuse/sound і vueuse/head, релізи GitHub і реєстр npm чотирнадцяти пакетів
`@vueuse/*`; лише англійською. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека
тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md). Сам Vue, Vue Router, Pinia,
Vuex і Vue Test Utils — у примірнику [`vue`](../instances/vue/README.md) тієї самої родини Vue.

**Склад (так його описано моделі, англійською).**

Documents of the VueUse documentation -- vueuse.org (every function page, the guide, add-ons, ecosystem and package
READMEs) at the last release of every minor line 4.0 to 15.0, the function pages of the 2020 lines 2.x and 3.x, the
GitHub release notes, the README of every stable version of @vueuse/core and the npm registry history of the ten
@vueuse packages, and the separate projects @vueuse/motion and @vueuse/gesture (documentation, README, registry),
@vueuse/sound and @vueuse/head (README, registry, head release notes) with their own numbering under the prefixes
motion-, gesture-, sound- and head-. Prereleases and other libraries are not here. This set is part of the Vue family:
vue-docs (Vue itself, Vue Router, Pinia, Vuex and Vue Test Utils) and vueuse-docs (this one: VueUse and its separate
projects) are meant to be connected together -- when a question belongs to the other member, name its server.

**Межі.**

- Частини сторінок, які vueuse.org генерує під час збирання (оголошення типів, журнал змін функції, автори, розмір),
  у репозиторії не лежать; у старих тегах оголошення типів ще були в самих `index.md`, тож там вони є.
- У прикладах коду лишаються службові рядки twoslash (`// @include: main`, `// ---cut---`).
- У сторінках `@vueuse/motion` лишаються порожні рядки компонентів Nuxt Content (`::person`), що на сайті
  показували живі приклади.
- Передрелізи, сам Vue (примірник `vue`), Nuxt, Unhead і переклади тут не входять.

**Далі в [README](../instances/vueuse/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Родина Vue: піднімати разом; Архівний режим: сервер без
корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### svelte

**Коли піднімати.** Пишете компоненти Svelte: руни, реактивність, інструменти `sv` і `svelte-check`.

**Порт** 8931, сервер `svelte-docs`. Підняти: `./df svelte serve`. Адреса: `http://127.0.0.1:8931/mcp`.

**Обсяг.** Документів: 2 818, фрагментів: 6 492.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `sveltekit-docs` (8932).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Svelte — компілятор інтерфейсів (руни й реактивність, синтаксис
шаблонів, прив'язки, події, переходи й анімації, дії, сховища, контекст, спеціальні елементи, стилі, компілятор і
рантайм), а також про CLI `sv`, `@sveltejs/vite-plugin-svelte` і `svelte-check`. Документація — з тегу кожної
стабільної мінорної версії 3.0–5.57 і на кожен реліз 1.x–2.x. Джерела — репозиторії sveltejs/svelte,
sveltejs/v2.svelte.dev, sveltejs/svelte.dev, sveltejs/cli, sveltejs/vite-plugin-svelte, sveltejs/language-tools,
пакети й реєстр npm; лише англійською. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Svelte documentation -- svelte.dev at the last release of every minor line 3.0 to 5.57, the Svelte
1.x and 2.x guide, the Svelte 5 tutorial, the blog, examples and AI section of svelte.dev, the documentation of the sv
CLI and vite-plugin-svelte, the changelogs and svelte-check release notes, the README of every stable version and the
npm registry history of svelte, sv, @sveltejs/vite-plugin-svelte and svelte-check. Prereleases and other libraries are
not here. This set is part of the Svelte family: svelte-docs (this one: Svelte itself, the sv CLI, vite-plugin-svelte
and svelte-check) and sveltekit-docs (SvelteKit, its adapters, @sveltejs/package, @sveltejs/enhanced-img and Sapper)
are meant to be connected together -- when a question belongs to the other member, name its server.

**Межі.**

- Документації 0.x у репозиторіях немає; посібник 1.x–2.x — лише сторінки `content/guide`.
- Розділ AI svelte.dev частково згенерований (підказки MCP-сервера) і дає кілька дуже довгих фрагментів.
- SvelteKit, адаптери й Sapper тут не входять; передрелізи (`5.0.0-next`) теж.

**Далі в [README](../instances/svelte/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Родина Svelte: піднімати разом; Архівний режим: сервер без
корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### sveltekit

**Коли піднімати.** Пишете застосунок на SvelteKit: маршрути, завантаження даних, адаптери.

**Порт** 8932, сервер `sveltekit-docs`. Підняти: `./df sveltekit serve`. Адреса: `http://127.0.0.1:8932/mcp`.

**Обсяг.** Документів: 2 244, фрагментів: 4 644.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `svelte-docs` (8931).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про SvelteKit — фреймворк застосунків на Svelte (маршрути й файли
`+page`/`+layout`/`+server`, функції `load`, form actions, параметри сторінок, хуки, помилки й переадресації, модулі
`$app` і `$env`, адаптери й розгортання), а також про адаптери, `@sveltejs/package`, `@sveltejs/enhanced-img` і
попередника SvelteKit — Sapper. Документація — з тегу кожної стабільної мінорної версії 1.0–3.1. Джерела — репозиторії
sveltejs/kit, sveltejs/svelte.dev і sveltejs/sapper, пакети й реєстр npm; лише англійською. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md). Сам Svelte, CLI `sv`, vite-plugin-svelte і svelte-check — у примірнику
[`svelte`](../instances/svelte/README.md) тієї самої родини Svelte.

**Склад (так його описано моделі, англійською).**

Documents of the SvelteKit documentation -- svelte.dev/docs/kit at the last release of every minor line 1.0 to 3.1,
the SvelteKit part of the svelte.dev tutorial, the Sapper documentation, the changelogs, the README of every stable
version and the npm registry history of @sveltejs/kit, the adapters, @sveltejs/package, @sveltejs/enhanced-img,
create-svelte and sapper. Prereleases and other libraries are not here. This set is part of the Svelte family:
svelte-docs (Svelte itself, the sv CLI, vite-plugin-svelte and svelte-check) and sveltekit-docs (this one: SvelteKit,
its adapters, @sveltejs/package, @sveltejs/enhanced-img and Sapper) are meant to be connected together -- when a
question belongs to the other member, name its server.

**Межі.**

- Документації передрелізів `1.0.0-next` (2021–2022) і SvelteKit 0.x тут немає.
- `create-svelte` (колишній спосіб створити проєкт; тепер `npx sv create`) — лише README і реєстр.
- Сам Svelte, `sv`, vite-plugin-svelte і svelte-check — у примірнику `svelte`; адаптер `cloudflare-workers`
  (застарілий) не береться.

**Далі в [README](../instances/sveltekit/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в
цій теці; Звідки документація; Межі, про які треба пам'ятати; Родина Svelte: піднімати разом; Архівний режим: сервер
без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### solidjs

**Коли піднімати.** Пишете на SolidJS, Solid Router, SolidStart або беретеся за Solid 2.0.

**Порт** 8928, сервер `solidjs-docs`. Підняти: `./df solidjs serve`. Адреса: `http://127.0.0.1:8928/mcp`.

**Обсяг.** Документів: 4 588, фрагментів: 13 687.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про SolidJS — бібліотеку інтерфейсів на дрібнозернистій реактивності
(сигнали, ефекти, мемо, сховища, компоненти, керування потоком, ресурси, рендеринг на сервері), а також про Solid
Router, SolidStart, Solid Meta і Solid Primitives. Документація — на кожен стабільний реліз: сайт docs.solidjs.com на
релізи solid-js 1.8–1.9 і на релізи Router, Start і Meta, давня документація solidjs.com 1.0–1.8, і єдиний
нестабільний шар — реліз-кандидат Solid 2.0 (2.0.0-rc.19) з позначкою в кожному документі. Джерела — репозиторії
solidjs/solid-docs, solidjs/solid-docs-legacy, solidjs/solid, solid-router, solid-start, solid-meta,
solidjs-community/solid-primitives, пакети й реєстр npm; лише англійською. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the SolidJS documentation -- docs.solidjs.com (the Solid core, Solid Router, SolidStart and Solid Meta)
as it stood at every stable release of solid-js 1.8 to 1.9 and of each of those packages, the old solidjs.com
documentation (API, guides, tutorial) of every stable release 1.0 to 1.8, the Solid 2.0 release-candidate
documentation (2.0.0-rc.19, not stable), the changelogs and GitHub release notes, the README of every stable version
and the npm registry history of solid-js, @solidjs/router, @solidjs/start, solid-start, @solidjs/meta,
@solidjs/testing-library, vite-plugin-solid and babel-preset-solid, and Solid Primitives (every @solid-primitives
package: README of every stable version, changelog, registry). Other prereleases and third-party libraries are not
here.

**Межі.**

- Сайт docs.solidjs.com став основним на початку 2024 року; для solid-js 1.0–1.8 основна документація — давня
  solidjs.com. Знімки 1.8, зроблені до появи `src/routes/`, нової документації не мають.
- Давня документація — англійська частина solid-docs-legacy (`langs/en/`); переклади не беруться.
- Пакет `@solid-primitives/match` журналу змін не має.
- Передрелізів (крім реліз-кандидата 2.0), Kobalte, Solid UI, TanStack та інших сторонніх бібліотек тут немає.

**Далі в [README](../instances/solidjs/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### emberjs

**Коли піднімати.** Пишете або підтримуєте застосунок на Ember, Ember Data, Ember CLI.

**Порт** 8940, сервер `emberjs-docs`. Підняти: `./df emberjs serve`. Адреса: `http://127.0.0.1:8940/mcp`.

**Обсяг.** Документів: 24 408, фрагментів: 32 911.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Ember.js за його документацією: гайди guides.emberjs.com
(компоненти, шаблони, `@tracked` і автовідстеження, маршрути й `model()`, сервіси, Ember Data, тести, `<template>` і
`.gjs`, TypeScript, посібник-підручник, перехід на Octane) на кожну мінорну 1.10–7.2, довідник API api.emberjs.com —
Ember 1.0–7.3 і Ember Data 1.13–5.5, гайд застарілого deprecations.emberjs.com, гайди Ember CLI, гайди WarpDrive (нова
Ember Data), усі дописи блогу blog.emberjs.com, 267 RFC, журнали змін Ember і WarpDrive, релізи GitHub `ember.js`,
`ember-cli` і `warp-drive`, записи npm `ember-source`, `ember-cli` і `ember-data`. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Ember documentation -- the Ember Guides for every minor 1.10–7.2, the API reference of Ember 1.0–7.3
and Ember Data 1.13–5.5, the deprecations guide, the Ember CLI and WarpDrive guides, the RFCs, the blog, the
changelogs and GitHub releases, and the npm records of ember-source, ember-cli and ember-data. Prereleases (beta,
canary) are not here.

**Далі в [README](../instances/emberjs/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### alpine

**Коли піднімати.** Додаєте поведінку до сторінки через Alpine.js без збирання.

**Порт** 8815, сервер `alpine-docs`. Підняти: `./df alpine serve`. Адреса: `http://127.0.0.1:8815/mcp`.

**Обсяг.** Документів: 704, фрагментів: 2 043.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Alpine.js за офіційною документацією всіх його версій — від 0.1
(2019) до поточної 3.x — разом із CSP-збіркою `@alpinejs/csp`: її кодом і тестами на кожному релізі 3.x, нотатками
релізів і історією версій ядра, CSP-збірки й плагінів у реєстрі npm. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Alpine.js documentation -- the docs kept in the repository on every one of its releases (the
README of 0.1-2.x and the alpinejs.dev pages of 3.x), each distinct text once with all the versions it belongs to; the
source code and tests of the CSP build (@alpinejs/csp) on every 3.x release; the GitHub release notes; and the npm
registry history of alpinejs, @alpinejs/csp and every official plugin. Livewire, htmx, Vue and the premium components
of alpinejs.dev are not here; if something about Alpine.js is not found in these documents, it is unlikely to be
anywhere in its official documentation.

**Межі.**

Livewire, htmx, Vue і самої специфікації Content-Security-Policy тут немає (CSP як стандарт — у примірниках
`webstandards` і `owasp`). Опція `allowGlobals` згадана лише в нотатці релізу 3.15.1: на сторінці CSP її немає. Гілку
`main` після 3.17.4 (підняття версії до 3.17.5 без тегу) не взято: знімки — лише релізи.

**Далі в [README](../instances/alpine/README.md):** Навіщо CSP-збірка окремо; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### astro

**Коли піднімати.** Будуєте сайт на Astro: контентні колекції, острови, інтеграції.

**Порт** 8763, сервер `astro-docs`. Підняти: `./df astro serve`. Адреса: `http://127.0.0.1:8763/mcp`.

**Обсяг.** Документів: 22 747, фрагментів: 23 141.

**Опис.**

Четвертий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Astro за офіційною документацією всіх
його ліній — від 0.23 (лютий 2022) до поточної 7.3 — за нотатками релізів, блогом, розборами впроваджень і трьома
каталогами: інтеграцій, тем і вітрини сайтів. Код спільний і лежить у `../../engine/` (завантаження корпусу),
`../../server/` (сервер, агент, шари) та `../../common/` (пошук); ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Astro documentation -- every release line from 1 to the current 7, each taken from the
documentation repository as it stood on that line's release day, the release notes of every astro release, the Astro
blog and case studies, and the catalogs of integrations, themes and showcase sites. Nothing exists here from before
line 1 of August 2022: Astro had no stable release until then. The blog, the case studies and the catalogs carry no
version by intent. React, Vue, Svelte, Vite, Tailwind, Starlight and the hosting platforms Astro integrates with are
not here; only Astro's own integration layer is.

**Далі в [README](../instances/astro/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Токен GitHub; Установка venv; Спосіб А — власний захищений агент (усі чотири шари); Спосіб Б — сервер
під Claude Code (HTTP); Архівний режим: сервер без корпусу; Оновлення корпусу.

### astro-markdown-pipeline

**Коли піднімати.** Налаштовуєте обробку Markdown в Astro: remark, rehype, очищення HTML, формули.

**Порт** 8808, сервер `astro-markdown-pipeline-docs`. Підняти: `./df astro-markdown-pipeline serve`. Адреса: `http://127.0.0.1:8808/mcp`.

**Обсяг.** Документів: 2 904, фрагментів: 18 362.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про конвеєр «Markdown → HTML» екосистеми unified, у тому вигляді, в
якому його збирає Astro: `unified`, `remark-parse`, `remark-rehype`, `rehype-sanitize` з `hast-util-sanitize`,
`remark-math` з `rehype-katex` і KaTeX, підсвітка коду Shiki з пакетами `@shikijs/*`, а також увесь сайт
unifiedjs.com. Документація — усіх стабільних версій пакетів, а не лише останньої. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the documentation of the unified Markdown pipeline -- the README, TypeScript declarations and npm
registry history (with the Node requirement) of @astrojs/markdown-remark (and its changelog), remark-rehype,
rehype-sanitize, hast-util-sanitize, rehype-katex, remark-math, micromark-extension-math, mdast-util-math, katex and
shiki, every stable version; the documentation of Shiki and of KaTeX at every stable release; and unifiedjs.com
(guides, recipes, community, the ecosystem catalogue). The documentation of Astro outside its markdown package, of MDX
and of other Markdown processors is not here; if something about this pipeline is not found in these documents, it is
unlikely to be anywhere in its official documentation.

**Межі.**

Документації Astro поза його markdown-пакетом (маршрутизація, компоненти, колекції контенту), MDX, `markdown-it`,
`marked` та інших обробників Markdown тут немає. Решта пакетів екосистеми (`mdast-util-to-hast`, `hast-util-to-html`,
`unist-util-visit`, `rehype-highlight` тощо) присутні лише як сторінки каталогу unifiedjs.com — без версій і без
історії. Код бібліотек не входить.

**Далі в [README](../instances/astro-markdown-pipeline/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### react-native

**Коли піднімати.** Пишете мобільний застосунок на React Native.

**Порт** 8818, сервер `react-native-docs`. Підняти: `./df react-native serve`. Адреса: `http://127.0.0.1:8818/mcp`.

**Обсяг.** Документів: 3 503, фрагментів: 14 038.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про React Native — фреймворк для нативних застосунків Android та iOS на
React — за офіційною документацією всіх стабільних версій, від 0.1 (березень 2015) до поточної 0.x: сайт
reactnative.dev у стані кожної мінорної версії, розділ Architecture, блог, сторінки про релізи, нотатки релізів на
GitHub, журнал змін і історія пакета в реєстрі npm. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md). Expo —
фреймворк і платформа поверх React Native — має власний примірник [`expo`](../instances/expo/README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official React Native documentation -- the site reactnative.dev on every stable minor release, each
distinct text once with all the versions it belongs to; the docs of 0.1-0.4; the Architecture section, the blog and
the release-policy pages; the GitHub release notes and the change log of every stable release; and the npm registry
history of the react-native package. Expo, React Navigation and other community libraries are not here; if something
about React Native is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

Expo, React Navigation, Reanimated, Gesture Handler та інших бібліотек спільноти тут немає, як і React загалом — лише
те, що про них пише документація React Native; для Expo є примірник `expo`. Сайт 0.60–0.76 читається з репозиторію,
а не з архівних сайтів, тож посилання документів цих версій ведуть на GitHub. Код прикладів SnackPlayer лишається
блоками коду, а живих прикладів Snack (запуску в браузері) в тексті немає. Діаграми розділу Architecture — картинки,
і в тексті від них лишається лише підпис.

**Далі в [README](../instances/react-native/README.md):** Навіщо вся історія; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### expo

**Коли піднімати.** Збираєте мобільний застосунок через Expo: EAS, модулі, конфігурація.

**Порт** 8819, сервер `expo-docs`. Підняти: `./df expo serve`. Адреса: `http://127.0.0.1:8819/mcp`.

**Обсяг.** Документів: 7 701, фрагментів: 35 632.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Expo — фреймворк і платформу для застосунків на React Native — за
офіційною документацією всіх стабільних SDK, від SDK 23 (листопад 2017) до поточного: довідник модулів кожного SDK
разом з API, довідник `app.json`, посібники docs.expo.dev у стані на кінець кожного SDK (Expo Router, EAS, Expo
Modules API, config plugins, tutorial), приклади застосунків, шаблони create-expo-app, журнал змін, дописи про випуск
SDK і історія пакета в реєстрі npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md). Сам React Native — ядро,
компоненти, Turbo Native Modules і Fabric — має власний примірник
[`react-native`](../instances/react-native/README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Expo documentation -- the site docs.expo.dev for every stable SDK: the module reference with
the API of each SDK, the app.json reference and the guides as they stood at the end of each SDK, each distinct text
once with all the SDKs it belongs to; the example apps and create-expo-app templates; the change log, the SDK release
posts and the npm registry history of the expo package. React Native core, React Navigation and other community
libraries are not here; if something about Expo is not found in these documents, it is unlikely to be anywhere in its
official documentation.

**Межі.**

Ядра React Native, React Navigation, Reanimated та інших бібліотек спільноти тут немає — лише те, що про них пише
документація Expo; для React Native є примірник `react-native`. Документація SDK до 23 (2017) у репозиторії не
збереглася. Посилання документів прибраних SDK і старих редакцій посібників ведуть на GitHub, бо сайт їх уже не
показує. Відео й інтерактивні приклади Snack у тексті лишаються лише підписом чи кодом.

**Далі в [README](../instances/expo/README.md):** Навіщо вся історія; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

<!-- тема: Стан і дані на клієнті -->

### redux

**Коли піднімати.** Керуєте станом через Redux або Redux Toolkit, RTK Query.

**Порт** 8776, сервер `redux-docs`. Підняти: `./df redux serve`. Адреса: `http://127.0.0.1:8776/mcp`.

**Обсяг.** Документів: 3 368, фрагментів: 13 183.

**Опис.**

Шістнадцятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Redux і бібліотеки поруч із ним —
Redux Toolkit з RTK Query, React Redux, Reselect, Immer, redux-thunk, redux-saga, redux-persist і Redux DevTools — за
офіційною документацією всіх їхніх версій, README кожної опублікованої версії пакетів, нотатками релізів і реєстром
версій npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official documentation of Redux and the libraries around it -- the docs folder of reduxjs/redux,
reduxjs/redux-toolkit (with RTK Query), reduxjs/react-redux and reduxjs/reselect on every release tag, the Immer and
redux-saga docs on every tag, the current Redux DevTools docs and the archived redux-devtools-extension docs, each
distinct text once with all the versions it belongs to; the README of every published version of redux,
@reduxjs/toolkit, react-redux, reselect, redux-thunk, immer, redux-persist, redux-saga and @redux-devtools/extension;
the GitHub release notes of all these repositories; and the npm registry list of every published version, with dates,
dist-tags, dependencies and peer dependencies, of those packages and of @rtk-query/codegen-openapi and
redux-devtools-extension. React itself, other state libraries and the frameworks are not here.

**Межі.**

Тут немає документації самого React (окремий примірник `react`), інших бібліотек стану (Zustand — окремий
примірник `zustand`, MobX, Jotai), NgRx та фреймворків. Issues і GitHub Discussions свідомо не взято: це рецепти
окремих проблем, а не документація.

**Далі в [README](../instances/redux/README.md):** Навіщо; Скільки цього; Бібліотеки; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code; На іншій машині.

### zustand

**Коли піднімати.** Керуєте станом через Zustand.

**Порт** 8771, сервер `zustand-docs`. Підняти: `./df zustand serve`. Адреса: `http://127.0.0.1:8771/mcp`.

**Обсяг.** Документів: 571, фрагментів: 2 191.

**Опис.**

Одинадцятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Zustand за офіційною документацією
всіх його версій — від 0.0.1 (квітень 2019) до поточної 5.x, разом з alpha, beta й rc, — за README кожної версії npm,
нотатками релізів і реєстром версій npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`;
ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Zustand documentation -- the docs/ folder of the pmndrs/zustand repository on every release
tag (from 4.0 in 2022 to the current 5.x, the source of the zustand.docs.pmnd.rs site), each distinct text once with
all the versions it belongs to; the README of every stable, alpha, beta and rc release on npm (the whole documentation
up to 3.x); the GitHub release notes; and the npm registry list of every published version with its date, dist-tag,
import paths and dependencies. Libraries built on Zustand and other state managers (Redux, Jotai, Valtio) are not
here; if something about Zustand is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Межі.**

Бібліотек довкола Zustand тут немає: `zustand-x`, `zundo`, `use-context-selector`, як і документації Jotai чи Valtio
з того ж pmndrs. Alpha, beta й rc — не релізи: текст, що є лише в них, міг так і не вийти, і промпт велить моделі
казати про це прямо.

**Далі в [README](../instances/zustand/README.md):** Навіщо вся історія; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code; На іншій машині.

### tanstack-query

**Коли піднімати.** Завантажуєте й кешуєте дані сервера через TanStack Query.

**Порт** 8767, сервер `tanstack-query-docs`. Підняти: `./df tanstack-query serve`. Адреса: `http://127.0.0.1:8767/mcp`.

**Обсяг.** Документів: 11 672, фрагментів: 45 057.

**Опис.**

Восьмий примірник фабрики: захищений MCP-сервер, що відповідає на питання про TanStack Query (до v4 — React Query) за
офіційною документацією всіх його версій — від 0.x (2019) до поточної 5.x, разом з кожним alpha, beta й release
candidate, — за довідником API кожного фреймворку, прикладами, журналами змін пакетів і нотатками релізів. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official TanStack Query documentation -- the docs kept in the repository on every one of its release
tags (from 0.0.3 to the current 5.x, with every alpha, beta and release candidate), each distinct text once with all
the versions it belongs to, including the API reference of every framework adapter; the example apps of every major
line; the changelogs of all @tanstack/*-query packages; the GitHub release notes; and the TanStack blog posts about
Query. TanStack Router, Start, Table, Form and the frameworks themselves are not here; if something about TanStack
Query is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

TanStack Router, Start, Table, Form і DB тут немає — лише два записи блогу про DB поверх Query. Немає й сторінки
Community Resources: сайт малює її з даних, markdown-тексту в неї немає. Alpha, beta й rc — не релізи: текст, що є
лише в них, міг так і не вийти, і промпт велить моделі казати про це прямо.

**Далі в [README](../instances/tanstack-query/README.md):** Навіщо вся історія; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### swr

**Коли піднімати.** Завантажуєте й кешуєте дані сервера через SWR.

**Порт** 8817, сервер `swr-docs`. Підняти: `./df swr serve`. Адреса: `http://127.0.0.1:8817/mcp`.

**Обсяг.** Документів: 430, фрагментів: 1 095.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про SWR — бібліотеку хуків React для отримання даних від Vercel — за
офіційною документацією всіх стабільних версій, від 0.1.2 (жовтень 2019) до поточної 2.x: сайт swr.vercel.app у стані
на кожен реліз, README кожної версії, нотатки релізів, приклади застосунків трьох ліній і історія пакета в реєстрі
npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official SWR documentation -- the site swr.vercel.app on every stable release, each distinct text
once with all the versions it belongs to; the README of every stable version (the main documentation of 0.x); the
GitHub release notes of every stable release; the npm registry history of the swr package; and the example
applications of the 0.x, 1.x and 2.x lines. TanStack Query, Apollo and RTK Query are not here; if something about SWR
is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

TanStack Query, Apollo, RTK Query й інших бібліотек отримання даних тут немає, як і React чи Next.js загалом — лише те,
що про них пише документація SWR. Бети й RC (97 версій, зокрема 2.6.0-beta.0) не беруться: ні знімки сайту, ні
README, ні нотатки релізів. Блог сайту — два дописи, про 1.0 і про 2.0. Діаграми сторінки «Understanding SWR» —
картинки, і в тексті від них лишається лише підпис.

**Далі в [README](../instances/swr/README.md):** Навіщо вся історія; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### nuqs

**Коли піднімати.** Тримаєте стан інтерфейсу в рядку запиту адреси через nuqs.

**Порт** 8836, сервер `nuqs-docs`. Підняти: `./df nuqs serve`. Адреса: `http://127.0.0.1:8836/mcp`.

**Обсяг.** Документів: 312, фрагментів: 971.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про nuqs — пакет npm, який тримає стан React у рядку адреси (query
string) з типами: `useQueryState` і `useQueryStates` працюють як `useState`, а значення живе в URL — фільтри,
сортування, сторінка переживають оновлення й копіювання посилання. Парсери, опції, кеш для серверних компонентів і
адаптери для Next.js (app і pages router), React SPA, Remix, React Router v6/v7/v8, TanStack Router і тестів.
Документація — усіх стабільних версій nuqs разом із попередником next-usequerystate. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the nuqs documentation -- the nuqs.dev site (docs and blog) at every stable release from 1.15.0 on; the
README of every stable version of nuqs and of next-usequerystate, its earlier name; the notes of every stable GitHub
release; and the npm registry history of both packages, including the peer dependencies (next, react, react-router,
@tanstack/react-router ...) and the date of every release. The documentation of Next.js, React Router, Remix, TanStack
Router, the URL standard and schema libraries is not here; if something about nuqs is not found in these documents, it
is unlikely to be anywhere in its official documentation.

**Межі.**

Документації Next.js, React Router, Remix, TanStack Router, стандарту URL і `URLSearchParams` (вони в примірниках
`nextjs`, `react-router`, `tanstack-router`, `mdn`), zod та інших бібліотек схем тут немає. Код бібліотеки, тести,
приклади застосунків e2e, `CONTRIBUTING.md` і типи з пакета не входять — сайт описує API повністю.

**Далі в [README](../instances/nuqs/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### rxjs

**Коли піднімати.** Працюєте з потоками подій через RxJS: оператори, зміни між версіями.

**Порт** 8872, сервер `rxjs-docs`. Підняти: `./df rxjs serve`. Адреса: `http://127.0.0.1:8872/mcp`.

**Обсяг.** Документів: 5 196, фрагментів: 23 924.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про RxJS — бібліотеку для складання асинхронних програм і подій з
послідовностей Observable: значення приходять у часі, а оператори (`map`, `switchMap`, `debounceTime`…) перетворюють і
поєднують потоки. Документація — всіх стабільних версій пакета rxjs (5.0–7.8: 70 версій у 22 мінорних лініях). Джерела
— офіційні сайти rxjs.dev і v6.rxjs.dev, README і журнал змін, документація з тегів репозиторію ReactiveX/rxjs, його
код і тести та реєстр npm, лише англійською й лише стабільні версії. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the RxJS documentation -- the official site rxjs.dev (RxJS 7.8: guides, deprecations, the 6-to-7 change
list and the API reference) and the site v6.rxjs.dev (RxJS 6.6); the README of every stable version of the rxjs
package; the changelog of every stable release; the documentation folders (doc/, docs_app/content), MIGRATION.md and
CONTRIBUTING.md of every tagged release of ReactiveX/rxjs; the source code (src/) and the tests (spec/, spec-dtslint/)
of every tagged release; and the npm registry history of rxjs, including dependencies, the TypeScript and Node
requirements and the date of every release. The documentation of Angular, NgRx, redux-observable, rxjs-compat and
other packages, of RxJS 8 and 9 (prereleases) and of the other ReactiveX languages is not here; if something about
RxJS is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

Документації Angular, NgRx, redux-observable, `rxjs-compat`, `rxjs-tslint`, `eslint-plugin-rxjs`, RxJS 8 і 9 (є лише
передрелізи), інших мов ReactiveX (RxJava та ін.) і пропозиції Observable в TC39 тут немає. Типи `@types/*` не входять.
Код — лише на тегах: коміти гілки master після 7.8.2 без тегу в корпус не потрапляють (master зараз веде 9.0).
Інтерактивне «дерево вибору оператора» (`operator-decision-tree`) на сайті — застосунок, у корпусі його немає.

**Далі в [README](../instances/rxjs/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

<!-- тема: Вигляд, форми, анімація, переклади -->

### tailwind

**Коли піднімати.** Верстаєте через Tailwind CSS: класи, конфігурація, перехід між версіями.

**Порт** 8775, сервер `tailwind-docs`. Підняти: `./df tailwind serve`. Адреса: `http://127.0.0.1:8775/mcp`.

**Обсяг.** Документів: 1 800, фрагментів: 15 926.

**Опис.**

П'ятнадцятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Tailwind CSS за офіційною
документацією всіх його версій — v4.3, v3.4, v2.2, v1.9 і v0.7 — з посібниками встановлення під кожен фреймворк,
журналом змін від 0.1.0 і реєстром версій npm самого `tailwindcss` та пакетів, з якими його використовують. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Tailwind CSS documentation -- every page of the v4.3, v3.4, v2.2 and v1.9 sites with their
class tables, the v0.7 docs from the site's repository, the "Install Tailwind CSS with ..." guide for every framework
with all of its tabs, the CHANGELOG entry of every release from 0.1.0 to today; and the npm registry list of every
published version, with dates, dist-tags, dependencies and peer dependencies, of tailwindcss, @tailwindcss/vite,
@tailwindcss/postcss, @tailwindcss/typography, @tailwindcss/forms, prettier-plugin-tailwindcss, @headlessui/react,
@headlessui/vue, tailwind-merge, clsx, class-variance-authority, tailwind-variants, daisyui, flowbite, flowbite-react,
flowbite-vue, flowbite-angular, preline, shadcn, shadcn-vue, @spartan-ng/cli, @spartan-ng/brain and @astrojs/tailwind.
The documentation of those libraries themselves (components, props) and of the frameworks is not here.

**Межі.**

Тут немає документації самих фреймворків (React, Vue, Angular, Astro — окремі примірники там, де вони є) і
документації компонентів бібліотек (пропси, приклади) поза їхніми README. Issues і GitHub Discussions репозиторію
Tailwind свідомо не взято: це рецепти окремих проблем, а не документація.

**Далі в [README](../instances/tailwind/README.md):** Навіщо; Скільки цього; Пакети поруч із Tailwind; Що в цій теці;
Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code; На іншій машині.

### shadcn

**Коли піднімати.** Будуєте інтерфейс із компонентів shadcn/ui, Radix UI, Base UI або React Aria.

**Порт** 8799, сервер `shadcn-docs`. Підняти: `./df shadcn serve`. Адреса: `http://127.0.0.1:8799/mcp`.

**Обсяг.** Документів: 3 538, фрагментів: 20 985.

**Опис.**

Тридцять дев'ятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про shadcn/ui і бібліотеки
примітивів під ним — Radix UI, Base UI і React Aria. Тут документація shadcn/ui кожної мінорної версії CLI від 0.1 до
4.21 — поточний сайт ui.shadcn.com і сайт для Tailwind CSS v3 — з прикладами й кодом компонентів; Radix Primitives
(кожна версія кожного компонента до 2025 року і пакет `radix-ui` 1.1–1.7), Radix Themes 1.0–3.3 і Radix Colors
0.1–3.0; Base UI 1.0–1.8 з демо й таблицями API; React Aria — поточний сайт із таблицями API, React Aria Components
1.0–1.19 і хуки `react-aria` 3.0–3.47. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents about shadcn/ui, Radix UI, Base UI and React Aria in English -- the shadcn/ui documentation of every minor
CLI release 0.1 to 4.21 (the current site and the site for Tailwind CSS v3, with the examples and the component source
code), Radix Primitives (every version of every component up to 2025 and radix-ui 1.1 to 1.7, with props, data
attributes, CSS variables, keyboard interactions and release notes), Radix Themes 1.0 to 3.3, Radix Colors 0.1 to 3.0,
Base UI 1.0 to 1.8 (with demos and API tables) and React Aria -- the current site with API tables (1.21), React Aria
Components 1.0 to 1.19 and the react-aria hooks 3.0 to 3.47. Other component libraries are not here.

**Межі.**

- **Таблиць пропсів Radix Themes немає.** Сайт будує їх із коду самої бібліотеки (`<ThemesPropsTable>`), у файлі
  сторінки даних немає. Опис, приклади й варіанти компонентів Themes — є.
- **Три приклади не знайдено** — їхніх файлів у реєстрі на тезі сторінки немає: `input-otp-form`, `native-select-form`,
  `native-select-input-group`. На їхньому місці лишилася назва.
- **Кілька вставок лишилися назвою файла**: допоміжні файли таблиці даних (`components/data-table-pagination`,
  `data-table-view-options`, `data-table-column-header`) лежать у демо-застосунку сайту (`app/(app)/examples`), поза
  теками реєстру з білого списку; `actions.ts` і `schema.ts` сторінок форм та `use-toast` старого сайту — файли `.ts`,
  а шаблони шукають `.tsx`.
- **Шкали Radix Colors** на сторінках палітр — малюнки (кольорові смуги); у тексті лишилися заголовки шкал і порожні
  дужки на місці малюнка.
- **Таблиць API старих версій React Aria немає.** Сайт генерував їх із коду TypeScript (`<PropTable>`), у файлах
  сторінок репозиторію даних немає; є текст і приклади. Повні таблиці — лише на поточному сайті («rac-1.21»).
- **React Aria Components 1.20** окремого знімка не має: на 1.20 документація вже переїхала на новий сайт, а той тримає
  лише поточну редакцію; від 1.20 лишилися нотатки випуску. Хуки 3.48–3.52 — так само, лише на поточному сайті.
- **Чотири сторінки-переліки сайту React Aria** (головна, `blog/index`, `examples/index`, `releases/index`) — самі
  компоненти-списки без тексту; `refresh` відкидає їх як «не документ» і пише чотири збої. Так і має бути.
- **Немає:** інших бібліотек компонентів (Material UI, Chakra, Mantine, Headless UI, Ark UI, компоненти Spectrum),
  блоків і шаблонів shadcn як коду сторінок. Сам Tailwind CSS — у примірнику `tailwind`,
  React Hook Form і zod — у своїх, React — у `react`.

**Далі в [README](../instances/shadcn/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Версії
у відповіді; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### motion

**Коли піднімати.** Анімуєте інтерфейс через Motion, колишній Framer Motion.

**Порт** 8823, сервер `motion-docs`. Підняти: `./df motion serve`. Адреса: `http://127.0.0.1:8823/mcp`.

**Обсяг.** Документів: 2 413, фрагментів: 8 350.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Motion — бібліотеку анімацій для React, JavaScript і Vue, яка до
листопада 2024 року звалася Framer Motion, — за її офіційною документацією. Він знає кожну сторінку motion.dev у
теперішній редакції (документацію, Motion+, Motion UI, AI Kit, приклади й посібники, журнал помилок, статті), журнал
змін Motion від Framer Motion 0.3.0 (2019) до поточної 14.x, README й історію в реєстрі npm кожної стабільної версії
пакетів `framer-motion`, `motion`, `framer-motion-3d`, `motion-v` (Motion для Vue) і Motion One (`@motionone/*`), а
також попередника Framer Motion — бібліотеку Popmotion разом із Pose. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Motion documentation -- every page of motion.dev as it stands now (Motion for React,
JavaScript and Vue, Motion+, Motion UI, AI Kit, examples and tutorials, troubleshooting, Magazine, changelog), the
Motion CHANGELOG from Framer Motion 0.3.0 to the current release, and the README and npm registry record of every
stable version of framer-motion, motion, motion-dom, motion-utils, framer-motion-3d, motion-v and Motion One
(@motionone/*), with the Motion One and Motion for Vue changelogs and release notes. Only stable releases are here. If
something about Motion is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

GSAP, React Spring, CSS-анімацій без Motion, React, Vue чи Framer (редактора) тут немає — лише сторінки motion.dev,
що порівнюють Motion із ними. Старої документації Framer Motion на framer.com, сайту Motion One і старих редакцій
motion.dev немає ніде, крім README відповідних версій. Код прикладів і компонентів Motion+ закритий. Дві чернетки
блогу Popmotion (`blog/draft-*`) порожні — `refresh` рахує їх збоями, це очікувано. Порожній запис журналу змін Motion
0.8.8 так само не пишеться.

**Далі в [README](../instances/motion/README.md):** Навіщо стільки історії; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### react-hook-form

**Коли піднімати.** Робите форми через React Hook Form.

**Порт** 8768, сервер `react-hook-form-docs`. Підняти: `./df react-hook-form serve`. Адреса: `http://127.0.0.1:8768/mcp`.

**Обсяг.** Документів: 3 474, фрагментів: 6 421.

**Опис.**

Дев'ятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про React Hook Form (RHF) за офіційною
документацією всіх його версій — від 0.0.12 (березень 2019) до поточної 7.x і бет 8.0, разом з кожним alpha, beta, rc
і next, — за TypeScript-сигнатурами публічного API, README кожної версії, журналом змін і нотатками релізів. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official React Hook Form documentation -- the text of react-hook-form.com as it stood at every one of
the npm releases (from 0.0.12 in March 2019 to the current 7.x and the 8.0 betas, with every alpha, beta, rc and next
build), each distinct text once with all the versions it belongs to; the README of every release; the TypeScript
signatures of the public API (API Extractor report) since December 2021; the CHANGELOG; the GitHub release notes; and
the Resources section of the site (articles, videos, newsletters, 3rd party bindings -- as annotated links, not the
articles themselves). @hookform/resolvers, @hookform/ devtools, the Form Builder and the libraries RHF is used with
(Zod, Yup, MUI) are not here; if something about React Hook Form is not found in these documents, it is unlikely to be
anywhere in its official documentation.

**Межі.**

`@hookform/resolvers`, `@hookform/devtools`, `@hookform/error-message` і Form Builder тут немає, як і документації
бібліотек, з якими RHF використовують (Zod, Yup, MUI). Alpha, beta, rc і next — не релізи: текст, що є лише в них,
міг так і не вийти, і промпт велить моделі казати про це прямо.

**Далі в [README](../instances/react-hook-form/README.md):** Навіщо вся історія; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code; На іншій машині.

### next-themes

**Коли піднімати.** Перемикаєте світлу й темну тему в Next.js через next-themes.

**Порт** 8835, сервер `next-themes-docs`. Підняти: `./df next-themes serve`. Адреса: `http://127.0.0.1:8835/mcp`.

**Обсяг.** Документів: 71, фрагментів: 198.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про next-themes — пакет npm, який перемикає тему React-застосунку
(світлу, темну, системну чи будь-яку власну): ставить клас або атрибут `data-*` на елемент `html`, пам'ятає вибір у
`localStorage` і вставляє на сторінку маленький скрипт, щоб під час завантаження не блимала чужа тема. Працює з
Next.js App Router і Pages Router та з будь-яким застосунком React. Документація — усіх стабільних версій пакета. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the next-themes documentation -- the README of every stable version of the next-themes npm package (0.0.2
to 0.4.6; the package of 0.3.0 shipped without one, so its README comes from the v0.3.0 tag), the TypeScript
declarations of the versions that ship them, the GitHub release notes of 0.2.0-0.4.6 (the project keeps no changelog
file), the example apps of every stable version (Pages Router, App Router, Tailwind CSS, multiple themes) and the npm
registry history, including the peerDependencies and the date of every release. The documentation of Next.js, React,
Tailwind CSS and other theming libraries is not here; if something about next-themes is not found in these documents,
it is unlikely to be anywhere in its official documentation.

**Межі.**

Документації Next.js, React, Tailwind CSS, CSS загалом і інших бібліотек тем та інтерфейсу (shadcn/ui, Radix, MUI)
тут немає. Код бібліотеки (`src/`), тести й демо-сайт не входять — лише документація й приклади.

**Далі в [README](../instances/next-themes/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в
цій теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### tanstack-virtual

**Коли піднімати.** Показуєте довгі списки через TanStack Virtual.

**Порт** 8803, сервер `tanstack-virtual-docs`. Підняти: `./df tanstack-virtual serve`. Адреса: `http://127.0.0.1:8803/mcp`.

**Обсяг.** Документів: 947, фрагментів: 2 115.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про TanStack Virtual (до v3 — react-virtual) за офіційною документацією
всіх його версій — від react-virtual 1.0 (2020) до поточної 3.x, разом з кожним alpha й beta лінії 3, — за прикладами
кожної лінії, журналами змін і нотатками релізів пакетів, записами блогу TanStack і історією версій пакетів у реєстрі
npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official TanStack Virtual documentation -- the docs kept in the repository on every one of its
release tags (from react-virtual 1.0.0 to the current 3.x, with every alpha and beta of 3.0), each distinct text once
with all the versions it belongs to; the example apps of every major line; the changelogs of all @tanstack/*-virtual
packages; the GitHub release notes; the TanStack blog posts about Virtual; and the npm registry history of every
package. TanStack Query, Table, Router and the frameworks themselves are not here; if something about TanStack Virtual
is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

TanStack Query, Table, Router і решти TanStack тут немає, як і react-window чи react-virtualized. Приклади Marko
лежать без коду: читач прикладів бере `.ts`, `.tsx`, `.vue`, `.svelte` і подібні файли, а `.marko` серед них немає,
тож від 19 прикладів Marko в корпусі лише `package.json`; сама сторінка Marko-адаптера — повна. Сторінки прикладів
сайту react-virtual 2.x (`docs/src/pages/examples/*.md`) — лише рамка CodeSandbox без тексту; код тих самих прикладів
є в `tv-examples-v2`. Alpha й beta — не релізи: текст, що є лише в них, міг так і не вийти, і промпт велить моделі
казати про це прямо.

**Далі в [README](../instances/tanstack-virtual/README.md):** Навіщо вся історія; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### react-window

**Коли піднімати.** Показуєте довгі списки через react-window.

**Порт** 8804, сервер `react-window-docs`. Підняти: `./df react-window serve`. Адреса: `http://127.0.0.1:8804/mcp`.

**Обсяг.** Документів: 357, фрагментів: 666.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про react-window за офіційною документацією всіх його стабільних версій
— від 1.0.0 (2018) до поточної 2.x, — разом із журналом змін і нотатками релізів, документацією супутніх пакетів
react-window-infinite-loader і react-virtualized-auto-sizer, типами `@types/react-window` з DefinitelyTyped і історією
версій чотирьох пакетів у реєстрі npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official react-window documentation -- the README on every stable release, the pages of the 1.x site
(website/ in the repository) and of the 2.x site (react-window.vercel.app) on every stable release of their line, each
distinct text once with all the versions it belongs to; the changelog and the GitHub release notes; the README and
changelog of react-window-infinite-loader and react-virtualized-auto-sizer; the @types/react-window type definitions
from DefinitelyTyped as every version shipped them; and the npm registry history of all four packages. React itself,
react-virtualized and TanStack Virtual are not here; if something about react-window is not found in these documents,
it is unlikely to be anywhere in its official documentation.

**Межі.**

React, react-virtualized і TanStack Virtual тут немає (для TanStack Virtual є свій примірник `tanstack-virtual`).
Сайти супутніх пакетів не взято — лише README і журнали змін. README сторінок 2.x містить довідник у таблицях HTML;
у корпусі це рядки «назва — опис» без розмітки, а охайні розділи по властивостях дають сторінки `List: props` і
`Grid: props` сайту 2.x.

**Далі в [README](../instances/react-window/README.md):** Навіщо обидві лінії; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### i18next

**Коли піднімати.** Перекладаєте застосунок через i18next або react-i18next.

**Порт** 8816, сервер `i18next-docs`. Підняти: `./df i18next serve`. Адреса: `http://127.0.0.1:8816/mcp`.

**Обсяг.** Документів: 4 937, фрагментів: 8 445.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про i18next за офіційною документацією всіх його стабільних версій —
від 0.0.1 (2012) до поточної 26.x: сайт у стані на день кожного релізу, журнал змін, нотатки релізів GitHub, README
кожної версії й історія версій у реєстрі npm. Поруч — тими самими шарами всі пакети організації i18next у npm: п'ять
найпоширеніших (react-i18next, next-i18next, i18next-http-backend, i18next-browser-languagedetector, i18next-cli) і ще
35 — бекенди, middleware, формати, постпроцесори, інструменти, прив'язки до фреймворків, застарілі пакети. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official i18next documentation -- the site on every stable release (www.i18next.com from 8.3, the
older i18next.com of 2.x-8.2, the 1.x site), each distinct text once with all the versions it belongs to; the
CHANGELOG of i18next and of i18next-node; the GitHub release notes; the README of every version; and the npm registry
history of the i18next package -- together with every package the i18next organization publishes to npm: react-i18next
(its site react.i18next.com on every release from 4.1.0), next-i18next, i18next-http-backend,
i18next-browser-languagedetector, i18next-cli, i18next-vue (its site for Vue 3 and Vue 2), the backends, middleware,
formats, post processors, tools, bindings and deprecated packages, each with the README of every version, its
CHANGELOG, release notes and npm history where the package has them. locize, next-intl, react-intl and vue-i18n are
not here; if something about the i18next packages is not found in these documents, it is unlikely to be anywhere in
their official documentation.

**Межі.**

Тут усі пакети організації i18next у npm. Немає того, що поза нею: locize і його пакетів (`i18next-locize-backend`,
`locize-cli`), next-intl, react-intl, FormatJS, vue-i18n — документація тут лише згадує їх і посилається. Немає й
портів i18next-android та i18next-ios: вони не з npm і давно не оновлюються. Код і типи TypeScript пакетів не взято —
лише документацію; що кажуть сторінки TypeScript, те й є.

**Далі в [README](../instances/i18next/README.md):** Три епохи сайту; Супутні пакети; Скільки цього; Що в цій теці;
Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### next-intl

**Коли піднімати.** Перекладаєте застосунок Next.js через next-intl.

**Порт** 8837, сервер `next-intl-docs`. Підняти: `./df next-intl serve`. Адреса: `http://127.0.0.1:8837/mcp`.

**Обсяг.** Документів: 1 121, фрагментів: 2 987.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про next-intl — бібліотеку інтернаціоналізації (i18n) для Next.js:
повідомлення у форматі ICU (підстановки, множина, вибір за значенням, rich text), форматування дат, часу, чисел і
списків, маршрутизація за мовою з проміжним шаром (`middleware`, у Next.js 16 — `proxy`) і навігацією, App Router
(серверні й клієнтські компоненти) і Pages Router. Разом із ним — use-intl, ядро тієї самої бібліотеки без прив'язки
до Next.js, і два пакети 4.x з того самого репозиторію: icu-minify і next-intl-swc-plugin-extractor. Документація —
усіх стабільних версій. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the next-intl documentation -- the next-intl.dev site (docs and blog) at every stable release from 1.2.0
on; the README of every stable version of next-intl, use-intl, icu-minify and next-intl-swc-plugin-extractor; the
changelog of every release; and the npm registry history of all four packages, including the peer dependencies (next,
react) and the date of every release. The documentation of Next.js, React, the JavaScript Intl API, ICU and other i18n
libraries is not here; if something about next-intl is not found in these documents, it is unlikely to be anywhere in
its official documentation.

**Межі.**

Документації Next.js (маршрутизація, `middleware`, `generateMetadata`), React, Intl API JavaScript (вона в
примірнику `mdn`), специфікації синтаксису ICU, i18next і react-intl тут немає. Код бібліотеки, тести, приклади
застосунків з `examples/` і типи з пакета не входять: сайт описує API повністю й показує код прикладів на сторінках.

**Далі в [README](../instances/next-intl/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в
цій теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

<!-- тема: Графіки й 3D -->

### d3

**Коли піднімати.** Малюєте власні графіки через D3 або його модулі.

**Порт** 8933, сервер `d3-docs`. Підняти: `./df d3 serve`. Адреса: `http://127.0.0.1:8933/mcp`.

**Обсяг.** Документів: 3 122, фрагментів: 10 300.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `observable-plot-docs` (8934).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про D3 — бібліотеку візуалізації даних (виділення й приєднання даних,
переходи, шкали, осі, фігури, ієрархії, сили, географічні проєкції, масиви й статистика, кольори й інтерполятори,
формати, час, завантаження даних, масштабування, перетягування, пензель, хорди, контури, Делоне й Вороний).
Документація — на кожен стабільний реліз d3 і кожного його модуля, від D3 3.x до 7.9. Джерела — репозиторії d3/d3,
d3/d3-3.x-api-reference і 42 репозиторії модулів організації d3, пакети й реєстр npm, зошити Observable команди D3;
лише англійською. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі
дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the D3 documentation -- d3js.org at every stable release of d3 since 7.8.5, the D3 3.x API reference (the
former d3/d3 wiki), the README of every stable version of the d3 package and of each of its modules (d3-array to
d3-zoom, the removed d3-collection, d3-queue, d3-request and d3-voronoi, and d3-geo-projection, d3-sankey, d3-hexbin,
d3-tile, d3-geo-polygon, d3-selection-multi, d3-require, d3-hsv), API.md and CHANGES.md of d3, the GitHub release
notes and the npm registry history of all these packages, and the Observable notebooks of the D3 team (the gallery,
Learn D3 and the examples of every module). Prereleases and other libraries are not here. This set is part of the D3
family: d3-docs (this one: D3 and its modules) and observable-plot-docs (Observable Plot, the high-level charting
library built on D3 by the same team) are meant to be connected together -- when a question belongs to the other
member, name its server.

**Межі.**

- Документація 1.x–2.x — лише README тих релізів; довідник вікі 2.x не зберігся.
- Архівні плагіни доби 3.x (`d3/d3-plugins`) не взято: їхні README мають однакові імена, і `ghdocs` злив би їх в один
  документ. Ті з них, що стали модулями (sankey, hexbin, tile, geo-projection), тут є.
- Зошити Observable — поточна редакція, без історії; частина старих зошитів позначена самим D3 як застаріла («Update
  May 2023: This notebook has been deprecated») і має новішу пару з `/2` у шляху.
- Observable Plot (примірник `observable-plot`), TopoJSON, бібліотеки-обгортки для React чи Vue тут не входять;
  передрелізи теж.

**Далі в [README](../instances/d3/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Родина D3: піднімати разом; Архівний режим: сервер без
корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### observable-plot

**Коли піднімати.** Хочете швидкий графік через Observable Plot.

**Порт** 8934, сервер `observable-plot-docs`. Підняти: `./df observable-plot serve`. Адреса: `http://127.0.0.1:8934/mcp`.

**Обсяг.** Документів: 455, фрагментів: 2 443.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `d3-docs` (8933).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Observable Plot — бібліотеку графіків на основі D3 від команди
Observable (`Plot.plot` і його опції, позначки, канали, шкали, перетворення, фасети, легенди, проєкції, взаємодії
`pointer` і `tip`). Документація — з тегу кожного релізу 0.6.6–0.6.17 і README кожної стабільної версії 0.1–0.6.17.
Джерела — репозиторій observablehq/plot, пакет і реєстр npm, зошити Observable про Plot; лише англійською. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Observable Plot documentation -- the Plot site (repository observablehq/plot, folder docs) at every
release 0.6.6 to 0.6.17, the README of every stable version of @observablehq/plot (before 0.6.6 the README was the
whole reference), the changelogs 2021 to 2025, the npm registry history, and the Observable notebooks about Plot (the
early documentation, examples, cheatsheets and the course). Prereleases and other libraries are not here. This set is
part of the D3 family: d3-docs (D3 and its modules) and observable-plot-docs (this one: Observable Plot, built on D3
by the same team) are meant to be connected together -- when a question belongs to the other member, name its server.

**Межі.**

- Релізи GitHub не взято: їхні нотатки — ті самі записи журналу змін.
- Зошити — поточна редакція, без історії; частина давньої документації в зошитах описує API 0.1–0.5.
- Сам D3 (примірник `d3`), Observable Framework, Vega-Lite тут не входять; передрелізи (`0.6.7-rc.1`) теж.

**Далі в [README](../instances/observable-plot/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього;
Що в цій теці; Звідки документація; Межі, про які треба пам'ятати; Родина D3: піднімати разом; Архівний режим: сервер
без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### lightweight-charts

**Коли піднімати.** Малюєте фінансові графіки через Lightweight Charts.

**Порт** 8826, сервер `lightweight-charts-docs`. Підняти: `./df lightweight-charts serve`. Адреса: `http://127.0.0.1:8826/mcp`.

**Обсяг.** Документів: 2 052, фрагментів: 3 630.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Lightweight Charts™ — безкоштовну бібліотеку фінансових графіків
від TradingView (пакет npm `lightweight-charts`): як створити графік і додати серію свічок, лінії чи гістограми, у
якому вигляді віддавати дані й час, як налаштувати шкали цін і часу, панелі, перехрестя, маркери, лінії цін, водяний
знак і форматування цін, як підписатися на рух миші й прокручування, як писати власні плагіни, як підключити графік у
React, Vue чи веб-компоненті і як він працює в обгортках для Android та iOS. Джерела — офіційний сайт
tradingview.github.io/lightweight-charts, репозиторій GitHub і реєстр npm, лише англійською. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Lightweight Charts(TM) documentation -- the site of every release line it keeps (5.2, 5.1,
5.0, 4.2, 4.1, 4.0, 3.8) with guides and the full API reference, the tutorials and the official plugin catalogue, the
release notes from 1.0.0, the repository docs and typings of 1.0-3.7, the README of every stable npm version, the
plugin changelogs, examples and agent skills of the repository, and the Android and iOS wrappers. Only stable releases
are here. If something about Lightweight Charts is not found in these documents, it is unlikely to be anywhere in its
official documentation.

**Межі.**

Тут немає TradingView Charting Library і Advanced Charts (інші, закриті продукти), віджетів TradingView, Pine Script,
невипущеної документації `/docs/next` і передрелізів (rc, beta). Інші бібліотеки графіків — поза примірником. React
як такий — у примірнику `react`.

**Далі в [README](../instances/lightweight-charts/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки
документація; Версії у відповіді; Межі, про які треба пам'ятати; Сховище сирого; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### threejs

**Коли піднімати.** Робите 3D у браузері через three.js.

**Порт** 8935, сервер `threejs-docs`. Підняти: `./df threejs serve`. Адреса: `http://127.0.0.1:8935/mcp`.

**Обсяг.** Документів: 10 661, фрагментів: 29 897.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `react-three-fiber-docs` (8936).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про three.js — бібліотеку 3D-графіки для браузера (сцена, камери,
рендерери WebGL і WebGPU, геометрії, матеріали, текстури, світло й тіні, завантажувачі моделей, анімація, raycasting,
контроли, постобробка, WebXR, TSL). Документація — сайт threejs.org з тегу кожного релізу r54–r186 (2013–2026),
офіційні приклади з кодом, вікі, README і реєстр npm пакета `three`, нотатки релізів; лише англійською. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the three.js documentation -- threejs.org (the API reference, the add-ons reference and the manual) at
every release r54 to r186, the official examples of the latest release with their full code, the wiki (Migration
Guide, Three.js Shading Language, the editor manual, the JSON formats), the README of every stable version and the npm
registry history of the three package, and the GitHub release notes of every release. Prereleases, React Three Fiber
and other wrappers are not here. This set is part of the three.js family: threejs-docs (this one: three.js itself) and
react-three-fiber-docs (React Three Fiber, the React renderer for three.js, and drei, its library of ready-made
components) are meant to be connected together -- when a question belongs to the other member, name its server.

**Межі.**

- Довідника до r54 немає; Migration Guide веде зміни з r41.
- Приклади — лише r186; `llms-full.txt` сайту не взято: це той самий довідник одним файлом.
- React Three Fiber і drei (примірник `react-three-fiber`), A-Frame тут не входять; передрелізи теж.

**Далі в [README](../instances/threejs/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Родина three.js: піднімати разом; Архівний режим: сервер без
корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### react-three-fiber

**Коли піднімати.** Робите 3D у React через React Three Fiber і drei.

**Порт** 8936, сервер `react-three-fiber-docs`. Підняти: `./df react-three-fiber serve`. Адреса: `http://127.0.0.1:8936/mcp`.

**Обсяг.** Документів: 1 625, фрагментів: 4 285.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `threejs-docs` (8935).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про React Three Fiber — React-рендерер для three.js (`Canvas`, об'єкти
three.js як JSX, хуки `useFrame`, `useThree`, `useLoader`, події, продуктивність, тестування) — і drei, бібліотеку
готових компонентів тієї ж команди pmndrs (контроли, камери, завантажувачі, `Environment`, `Html`, `Text`,
`Instances`). Документація — з останнього тегу кожної мінорної Fiber 1.0–9.8 і drei 10.0–10.7, README кожної
стабільної версії п'яти пакетів, релізи GitHub; лише англійською. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the React Three Fiber documentation -- the docs of @react-three/fiber (docs.pmnd.rs) at the last release
of every minor line 1.0 to 9.8, the docs of drei 10.0 to 10.7 and the README of drei 1.5 to 9.x (its whole reference
until 10.0), the README of every stable version and the npm registry history of @react-three/fiber, react-three-fiber,
@react-three/drei, drei and @react-three/test-renderer, and the GitHub release notes of both. Prereleases and other
libraries are not here. This set is part of the three.js family: threejs-docs (three.js itself) and
react-three-fiber-docs (this one: React Three Fiber and drei) are meant to be connected together -- when a question
belongs to the other member, name its server.

**Межі.**

- Мінорна Fiber 8.4 відсутня (див. вище); сусідні 8.3 і 8.5 є.
- Інші бібліотеки pmndrs (`@react-three/rapier`, `postprocessing`, `xr`, `uikit`, zustand, leva) не входять; сам
  three.js — у примірнику `threejs`; передрелізи теж не беруться.

**Далі в [README](../instances/react-three-fiber/README.md):** Навіщо окремий примірник; Історія пакетів; Скільки
цього; Що в цій теці; Звідки документація; Межі, про які треба пам'ятати; Родина three.js: піднімати разом; Архівний
режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

<!-- тема: Збирання, перевірка коду, тести -->

### vite

**Коли піднімати.** Налаштовуєте збирання через Vite: плагіни, сервер розробки, конфігурація.

**Порт** 8778, сервер `vite-docs`. Підняти: `./df vite serve`. Адреса: `http://127.0.0.1:8778/mcp`.

**Обсяг.** Документів: 2 821, фрагментів: 4 904.

**Опис.**

Вісімнадцятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Vite і його офіційні плагіни —
React (Babel, SWC, Oxc), React Server Components, Vue, Vue JSX, legacy, basic-ssl — і про create-vite за офіційною
документацією всіх версій, README кожної опублікованої версії пакетів, нотатками релізів і реєстром версій npm. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official documentation of Vite and its official plugins -- the docs folder of vitejs/vite on every
release tag from 2.0 to 8.x, each distinct text once with all the versions it belongs to; the README of every
published version of vite, create-vite, @vitejs/plugin-react, @vitejs/plugin-react-swc, @vitejs/plugin-rsc,
@vitejs/plugin-react-oxc, @vitejs/plugin-vue, @vitejs/plugin-vue-jsx, @vitejs/plugin-legacy, @vitejs/plugin-basic-ssl,
@vitejs/create-app and @vitejs/plugin-react-refresh; the GitHub release notes of these packages (Vite itself since
2.7); and the npm registry list of every published version, with dates, dist-tags, dependencies and peer dependencies,
of the same packages. Vitest, the frameworks built on Vite and third-party plugins (Svelte, Angular) are not here.

**Межі.**

Тут немає документації Vitest, Rollup, Rolldown, esbuild і Oxc як окремих інструментів, фреймворків на Vite (Nuxt,
SvelteKit; Astro і React Router — окремі примірники `astro` і `react-router`) і самих React та Vue (React — окремий
примірник `react`). Issues і GitHub Discussions свідомо не взято: це рецепти окремих проблем, а не документація.

**Далі в [README](../instances/vite/README.md):** Навіщо; Скільки цього; Пакети; Що в цій теці; Звідки документація;
Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code; На іншій машині.

### turborepo

**Коли піднімати.** Ведете монорепозиторій через Turborepo.

**Порт** 8906, сервер `turborepo-docs`. Підняти: `./df turborepo serve`. Адреса: `http://127.0.0.1:8906/mcp`.

**Обсяг.** Документів: 1 812, фрагментів: 6 471.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Turborepo — систему збирання монорепозиторіїв JavaScript і
TypeScript від Vercel (сайт turborepo.dev, колишні turbo.build і turborepo.com; репозиторій vercel/turborepo; реєстр
npm). Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Turborepo documentation -- the build system for JavaScript and TypeScript monorepos by Vercel (site
turborepo.dev, repository vercel/turborepo, the npm registry): the pages of the site at the last tag of every minor of
Turborepo 0.8 to 2.11 (core concepts, structuring a repository, configuring and running tasks, caching and Remote
Caching, environment variables, CI, the guides for frameworks and tools, the API reference of turbo.json and every
command, the Remote Cache API, the error messages, the blog), the README files of the root and of every package at the
same tags, the agent skill of the repository, the GitHub releases, the npm registry of nine packages and the examples
of the repository. The documentation of Turbopack, Next.js and the package managers as their own projects is not here;
if something about Turborepo is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Далі в [README](../instances/turborepo/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### eslint

**Коли піднімати.** Налаштовуєте перевірку коду через ESLint.

**Порт** 8789, сервер `eslint-docs`. Підняти: `./df eslint serve`. Адреса: `http://127.0.0.1:8789/mcp`.

**Обсяг.** Документів: 9 059, фрагментів: 28 404.

**Опис.**

Двадцять дев'ятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про ESLint — лінтер JavaScript і
TypeScript, який перевіряє код правилами й частину знахідок виправляє сам, — і про плагіни, без яких він у React- і
TypeScript-проєкті не обходиться. Тут документація з репозиторію eslint/eslint на кожній мінорній лінії 8, 9 і 10 та
на останній версії кожного старшого мажору, блог eslint.org, README кожної стабільної версії, нотатки релізів і реєстр
версій npm; поруч — README і CHANGELOG `eslint-plugin-react-hooks`, typescript-eslint, `eslint-plugin-react` і
`eslint-plugin-jsx-a11y`. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the ESLint documentation in English -- the docs of the eslint/eslint repository on every minor line of
ESLint 8, 9 and 10 and on the last release of every older major (user guide, configuration, rules reference,
extending, integrating, migration guides), the eslint.org blog, the README of every stable version, the GitHub release
notes and the npm registry lists of eslint and @eslint/js; next to it the README and CHANGELOG of
eslint-plugin-react-hooks, and typescript-eslint, eslint-plugin-react and eslint-plugin-jsx-a11y on the last release
of every major with their release notes and registry lists. Prettier, Biome, Oxlint, stylelint and the rule pages of
eslint-plugin-react-hooks on react.dev are not here.

**Межі.**

Тут немає документації Prettier, Biome, Oxlint і stylelint, самого компілятора TypeScript (примірник `typescript`),
React (примірник `react`) і сторінок правил `eslint-plugin-react-hooks` на react.dev (теж примірник `react`). Інших
плагінів ESLint (`eslint-plugin-import`, `eslint-plugin-testing-library` — він у примірнику `testing-library`,
`@next/eslint-plugin-next` — у примірнику `nextjs`) тут теж немає. Issues і GitHub Discussions свідомо не взято.

**Далі в [README](../instances/eslint/README.md):** Навіщо; Скільки цього; Пакети; Що в цій теці; Звідки документація;
Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### biome

**Коли піднімати.** Форматуєте й перевіряєте код через Biome.

**Порт** 8832, сервер `biome-docs`. Підняти: `./df biome serve`. Адреса: `http://127.0.0.1:8832/mcp`.

**Обсяг.** Документів: 9 326, фрагментів: 18 059.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Biome — набір інструментів для вебпроєктів від biomejs:
форматувальник, лінтер із правилами для JavaScript, TypeScript, JSX, JSON, CSS, GraphQL, HTML і Markdown, асист із
діями над кодом (сортування імпортів тощо), CLI, сервер мови для редакторів і плагіни GritQL. Джерела — сайт
biomejs.dev (до квітня 2024 — тека `website/` репозиторію biomejs/biome, далі — репозиторій biomejs/website), журнали
змін репозиторію biomejs/biome і реєстр npm, лише англійською й лише стабільні версії. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Biome documentation -- the site biomejs.dev as it stood for every stable Biome release from
0.1.2 to 2.5.15, with getting started, installation, configuration (biome.json), the CLI reference, the page of every
lint rule and assist action with its examples, diagnostics and options, the formatter, the language support, migrating
from ESLint and Prettier and to Biome 2, editors, recipes and the blog; the changelogs of Biome 1.0.0-1.9.4 and
2.0.0-2.5.15; and the npm version table of @biomejs/biome. Only stable releases are here: nightly builds and the 2.0
betas are not. If something about stable Biome is not found in these documents, it is unlikely to be anywhere in its
official documentation.

**Межі.**

Тут немає нічних збірок і бет 2.0, попередника Rome, ESLint і Prettier поза сторінками порівняння й переходу (є
окремий примірник `eslint`), самих мов JavaScript, TypeScript і CSS (є `mdn`, `typescript`), редакторів як таких,
фреймворків. Розширення редакторів (biome-vscode, biome-zed, biome-intellij) описано сторінками сайту, власних
журналів змін розширень тут немає.

**Далі в [README](../instances/biome/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Версії у
відповіді; Межі, про які треба пам'ятати; Сховище сирого; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### storybook

**Коли піднімати.** Описуєте компоненти в Storybook.

**Порт** 8821, сервер `storybook-docs`. Підняти: `./df storybook serve`. Адреса: `http://127.0.0.1:8821/mcp`.

**Обсяг.** Документів: 1 119, фрагментів: 9 309.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Storybook — майстерню для розробки, документування й тестування
UI-компонентів окремо від застосунку — за офіційною документацією останньої мінорної кожної мажорної версії: 6.5, 7.6,
8.6, 9.1 і поточної 10.x. Сторінки документації з прикладами коду всіх фреймворків, README кожної лінії, рецепти
інтеграцій сайту storybook.js.org, посібник з переходу між версіями, журнали змін, релізи латок і історія пакета
`storybook` у реєстрі npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Storybook documentation -- the docs/ pages of the storybookjs/storybook repository on the
last minor of every major line (6.5, 7.6, 8.6, 9.1 and the current 10.x), with the code examples of every framework in
place, each distinct text once with all the versions it belongs to; the README of every line; the fourteen integration
recipes of storybook.js.org/recipes; the MIGRATION.md guide, one section per version step; the CHANGELOG of every
stable release from 6.0 on; the GitHub releases of the late patches missing from the CHANGELOG; and the npm registry
history of the storybook package. Chromatic, the Storybook blog, the addon catalog and the internals of Vite, Webpack,
Vitest or Playwright are not here beyond what these pages say; if something about Storybook is not found in these
documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

Chromatic як продукт, блог Storybook, каталог сторонніх аддонів, туторіали storybook.js.org/tutorials і внутрішня
будова Vite, Webpack, Vitest, Playwright, Jest чи MSW тут не беруться. Документацію MSW, Vitest, Playwright і Testing
Library мають окремі примірники `msw`, `vitest`, `playwright`, `testing-library`. Мінорні лінії між останніми (6.0–6.4,
7.0–7.5, 8.0–8.5, 9.0, 10.0–10.5) окремих знімків документації не мають: що змінювалося в них, кажуть журнали змін і
MIGRATION.md.

**Далі в [README](../instances/storybook/README.md):** Навіщо сторінки з репозиторію, а не з сайту; Скільки цього; Що
в цій теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### vitest

**Коли піднімати.** Пишете тести на Vitest.

**Порт** 8783, сервер `vitest-docs`. Підняти: `./df vitest serve`. Адреса: `http://127.0.0.1:8783/mcp`.

**Обсяг.** Документів: 3 679, фрагментів: 10 325.

**Опис.**

Двадцять третій примірник фабрики: захищений MCP-сервер, що відповідає на питання про тестовий фреймворк Vitest, його
пакети (UI, браузерний режим і провайдери, покриття v8 та istanbul, web-worker, vite-node) і правила лінтера
`@vitest/eslint-plugin` за офіційною документацією всіх версій, README кожної опублікованої версії пакетів, нотатками
релізів і реєстром версій npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека
тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official documentation of Vitest and its packages -- the docs folder of vitest-dev/vitest on every
release tag from 0.1 to 5.x, each distinct text once with all the versions it belongs to; the rule pages and README of
@vitest/eslint-plugin on every tag; the README of every published version of vitest, @vitest/ui, @vitest/browser,
@vitest/browser-playwright, @vitest/browser-webdriverio, @vitest/browser-preview, @vitest/coverage-v8,
@vitest/coverage-istanbul, @vitest/web-worker, @vitest/snapshot, @vitest/expect, @vitest/mocker, @vitest/pretty-format
and vite-node (up to 3.x); the GitHub release notes of Vitest and of @vitest/eslint-plugin; and the npm registry list
of every published version, with dates, dist-tags, dependencies and peer dependencies, of the same packages and of the
deprecated @vitest/coverage-c8, @vitest/spy, @vitest/runner, @vitest/utils, @vitest/ws-client and the old
eslint-plugin-vitest. Vite itself, Jest, Playwright Test and the testing libraries (Testing Library, MSW) are not
here.

**Межі.**

Тут немає документації Vite (окремий примірник `vite`), Jest, Playwright Test, Testing Library, MSW і happy-dom чи
jsdom як окремих бібліотек. Issues і GitHub Discussions свідомо не взято: це рецепти окремих проблем, а не
документація.

**Далі в [README](../instances/vitest/README.md):** Навіщо; Скільки цього; Пакети; Що в цій теці; Звідки документація;
Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### testing-library

**Коли піднімати.** Тестуєте компоненти через Testing Library.

**Порт** 8786, сервер `testing-library-docs`. Підняти: `./df testing-library serve`. Адреса: `http://127.0.0.1:8786/mcp`.

**Обсяг.** Документів: 2 320, фрагментів: 6 105.

**Опис.**

Двадцять шостий примірник фабрики: захищений MCP-сервер, що відповідає на питання про сімейство Testing Library —
тестування інтерфейсу так, як ним користується людина. Тут увесь сайт testing-library.com з усіма обгортками (React,
React Native, Vue, Angular, Svelte, Preact, Solid, Qwik, Marko, Cypress, Puppeteer, Nightwatch, TestCafe,
WebdriverIO), ядро DOM Testing Library, user-event, jest-dom, правила обох eslint-плагінів, а для пакетів React-лінії
ще й README кожної опублікованої версії, нотатки релізів і реєстр версій npm. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Testing Library documentation in English -- the whole site testing-library.com (DOM Testing Library,
queries, user-event, guides, examples, ecosystem, and the page of every framework wrapper: React, React Native, Vue,
Angular, Svelte, Preact, Solid, Qwik, Marko, Cypress, Puppeteer, Nightwatch, TestCafe, WebdriverIO), the rules of
eslint-plugin-testing-library and eslint-plugin-jest-dom, the deprecated @testing-library/react-hooks, and for the
React line the README of every version, the GitHub release notes and the npm registry lists of @testing-library/react,
dom, user-event, jest-dom, react-hooks and both eslint plugins. The npm packages of the other wrappers, the test
runners (Jest, Vitest), MSW and React itself are not here.

**Межі.**

Тут немає Jest і Vitest (окремий примірник `vitest`), Playwright і Cypress як окремих інструментів, MSW, jsdom і
happy-dom. Пакетів обгорток, окрім React, поки немає (є лише їхні сторінки сайту). Issues і GitHub Discussions свідомо
не взято: це рецепти окремих проблем, а не документація.

**Далі в [README](../instances/testing-library/README.md):** Навіщо; Скільки цього; Пакети; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### playwright

**Коли піднімати.** Пишете наскрізні тести браузера через Playwright.

**Порт** 8788, сервер `playwright-docs`. Підняти: `./df playwright serve`. Адреса: `http://127.0.0.1:8788/mcp`.

**Обсяг.** Документів: 6 577, фрагментів: 34 200.

**Опис.**

Двадцять восьмий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Playwright — фреймворк для
наскрізного тестування й автоматизації браузерів (Chromium, Firefox, WebKit) і його тест-раннер Playwright Test. Тут
документація з репозиторію microsoft/playwright на кожній мінорній версії від 0.10 до 1.64, сайт playwright.dev для
Node.js, Playwright MCP і Playwright CLI для агентів, README кожної стабільної версії пакетів, нотатки релізів і
реєстр версій npm, а також Playwright для .NET: сайт playwright.dev для .NET на кожній мінорній версії від 1.12 до
1.64, пакети NuGet і нотатки релізів microsoft/playwright-dotnet. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Playwright documentation in English -- the docs of the microsoft/playwright repository on every minor
version from 0.10 to 1.64 (guides, Playwright Test, the API reference, the JavaScript release notes), the
playwright.dev site for Node.js, Playwright MCP and the Playwright CLI, and the README of every stable version, the
GitHub release notes and the npm registry lists of playwright, @playwright/test, @playwright/mcp and @playwright/cli;
and Playwright for .NET -- the playwright.dev site for .NET on every minor version from 1.12 to 1.64, the NuGet
packages Microsoft.Playwright (with NUnit, MSTest, xUnit, xUnit v3, TestAdapter and CLI) and the playwright-dotnet
release notes. The pages made only for Python and Java, other test runners and the web platform are not here.

**Межі.**

Тут немає Playwright для Python і Java, документації Jest і Vitest (окремий примірник `vitest`), Testing Library
(примірник `testing-library`), MSW (примірник `msw`), Cypress, Selenium і Puppeteer, протоколу DevTools і самої
вебплатформи (примірник `mdn`). Issues і GitHub Discussions свідомо не взято.

**Далі в [README](../instances/playwright/README.md):** Навіщо; Скільки цього; Пакети; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### msw

**Коли піднімати.** Підміняєте мережеві запити в тестах через Mock Service Worker.

**Порт** 8787, сервер `msw-docs`. Підняти: `./df msw serve`. Адреса: `http://127.0.0.1:8787/mcp`.

**Обсяг.** Документів: 1 066, фрагментів: 3 568.

**Опис.**

Двадцять сьомий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Mock Service Worker (MSW) —
бібліотеку, яка перехоплює мережеві запити на рівні мережі й віддає підготовлені відповіді, у браузері (Service
Worker) і в Node.js. Тут офіційний сайт mswjs.io для MSW 3, 2 і 1, записані рішення команди, README кожної версії
пакетів, нотатки релізів і реєстр версій npm. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Mock Service Worker documentation in English -- the site mswjs.io for MSW 3, as it stood for MSW 2
(with source.mswjs.io) and for MSW 1, the design decisions of the msw repository, and the README of every version, the
GitHub release notes and the npm registry lists of msw, @mswjs/interceptors, @msw/data, @msw/source and @msw/serve
(with their former @mswjs names). Test runners, Testing Library, the Web APIs and the frameworks MSW integrates with
are not here.

**Межі.**

Тут немає документації тест-раннерів (Vitest — окремий примірник `vitest`, Jest, Playwright), Testing Library
(примірник `testing-library`), Web API `fetch`, `Request`, `Response`, `WebSocket` (примірник `mdn`) і фреймворків,
з якими MSW інтегрується. Issues і GitHub Discussions свідомо не взято.

**Далі в [README](../instances/msw/README.md):** Навіщо; Скільки цього; Пакети; Що в цій теці; Звідки документація;
Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### supertest

**Коли піднімати.** Тестуєте HTTP-сервер Node.js через supertest.

**Порт** 8876, сервер `supertest-docs`. Підняти: `./df supertest serve`. Адреса: `http://127.0.0.1:8876/mcp`.

**Обсяг.** Документів: 125, фрагментів: 224.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про пакет npm `supertest` (перевірка HTTP-серверів Node.js зручним
ланцюжком викликів поверх superagent, репозиторій forwardemail/supertest) — за документацією усіх його стабільних
версій: README кожної версії, History.md ранніх версій, нотатки релізів GitHub та історія версій у реєстрі npm. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the supertest documentation -- the npm package supertest: the README of every stable version, the
History.md of the early versions (0.1.0 to 3.4.1), the GitHub release notes of the later ones and the npm registry
history of the package, including the Node.js requirement (engines), the dependencies (superagent) and the date of
every release. The documentation of superagent, Jest, Mocha, Express and the other test or web frameworks is not here;
if something about the package is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Далі в [README](../instances/supertest/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

<!-- тема: Бекенд на Node.js -->

### nestjs

**Коли піднімати.** Пишете бекенд на NestJS: модулі, провайдери, гарди, мікросервіси.

**Порт** 8762, сервер `nestjs-docs`. Підняти: `./df nestjs serve`. Адреса: `http://127.0.0.1:8762/mcp`.

**Обсяг.** Документів: 1 122, фрагментів: 5 391.

**Опис.**

Третій примірник фабрики: захищений MCP-сервер, що відповідає на питання про NestJS за офіційною документацією його
версій — від лінії 6 (березень 2019) до поточної 12 — і за нотатками релізів, які сягають лютого 2018. Код спільний і
лежить у `../../engine/` (завантаження корпусу), `../../server/` (сервер, агент, шари) та `../../common/` (пошук); ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official NestJS documentation -- the current docs at docs.nestjs.com, the documentation as it stood
on the release day of lines 11, 10, 9, 8, 7 and 6, the chapters of lines 5 and 4 read out of the Angular templates the
site used before it had markdown, and the GitHub release notes of every NestJS release back to 4.6.1 of February 2018.
Lines 1 to 3 have nothing here at all, neither documentation nor release notes, because the project tagged nothing
before v4.4.0. TypeORM, Prisma, Passport, Express, Fastify and the other libraries NestJS integrates with are not
here; only Nest's own integration layer is.

**Межі.**

Корпус каже, що документація *описувала* на той час, а не що код *робив*. Нотатки релізу називають зміну, але не
завжди пояснюють її наслідки. Якщо на питання відповіді в документах немає, сервер так і скаже — це його робота.

**Далі в [README](../instances/nestjs/README.md):** Навіщо окремий примірник; Що в цій теці; Звідки документація;
Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Спосіб А —
власний захищений агент (усі чотири шари); Спосіб Б — сервер під Claude Code (HTTP).

### nestjs-cls

**Коли піднімати.** Передаєте контекст запиту або транзакцію в NestJS через nestjs-cls.

**Порт** 8879, сервер `nestjs-cls-docs`. Підняти: `./df nestjs-cls serve`. Адреса: `http://127.0.0.1:8879/mcp`.

**Обсяг.** Документів: 389, фрагментів: 1 074.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про `nestjs-cls` — модуль continuation-local storage (контекст запиту
на `AsyncLocalStorage`, сумісний із впровадженням залежностей NestJS; репозиторій Papooch/nestjs-cls, сайт
papooch.github.io/nestjs-cls) — за документацією всіх його стабільних версій: сторінки сайту на тегах кожної версії
ядра від 3.5.1, README кожної версії (до 3.5.1 README і був документацією), нотатки релізів GitHub та історія версій у
реєстрі npm. Разом із ядром — плагін транзакцій `@nestjs-cls/transactional` і вісім його адаптерів
(`@nestjs-cls/transactional-adapter-prisma`, `-typeorm`, `-drizzle-orm`, `-kysely`, `-knex`, `-mongoose`, `-mongodb`,
`-pg-promise`): README кожної версії, релізи й реєстр npm кожного пакета. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the nestjs-cls documentation -- the npm package `nestjs-cls` (continuation-local storage for NestJS on
AsyncLocalStorage): the pages of the documentation site (papooch.github.io/nestjs-cls) at the tag of every core
version from 3.5.1 to 7.0.1, the README of every stable version (before 3.5.1 the README was the whole documentation),
the GitHub release notes and the npm registry history of the package, including the peer dependencies on NestJS, the
Node.js requirement (engines) and the date of every release; and the same for the Transactional plugin
`@nestjs-cls/transactional` and its eight adapters (Prisma, TypeORM, Drizzle ORM, Kysely, Knex, Mongoose, MongoDB,
pg-promise), whose versions are written with a prefix ("transactional-4.0.1", "adapter-prisma-2.0.1"). The
documentation of NestJS itself, of AsyncLocalStorage and of the database libraries behind the adapters is not here; if
something about the package is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Далі в [README](../instances/nestjs-cls/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### nestjs-pino

**Коли піднімати.** Пишете журнали в NestJS через nestjs-pino.

**Порт** 8880, сервер `nestjs-pino-docs`. Підняти: `./df nestjs-pino serve`. Адреса: `http://127.0.0.1:8880/mcp`.

**Обсяг.** Документів: 82, фрагментів: 259.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про `nestjs-pino` — логер для NestJS на pino і pino-http з контекстом
запиту в кожному рядку логу (репозиторій iamolegga/nestjs-pino) — за документацією всіх його стабільних версій: README
кожної версії (сайту пакет не має, README і є документацією), нотатки релізів GitHub та історія версій у реєстрі npm.
Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the nestjs-pino documentation -- the npm package `nestjs-pino` (a logger for NestJS built on pino and
pino-http, with the request context in every log line): the README of every stable version from 0.1.0 to 5.3.1 (the
package has no documentation site -- the README is the documentation: LoggerModule.forRoot and forRootAsync, the
`Params` fields, `Logger`, `PinoLogger` and `NativeLogger`, `@InjectPinoLogger`, `assign`, `runInContext`,
microservices, testing, the migration guides to v1, v2 and v5, the FAQ), the GitHub release notes of every version
from 2.0.1 to 5.3.1, and the npm registry history of the package, including the peer dependencies on pino, pino-http,
@nestjs/common and @nestjs/core, the Node.js requirement (engines) and the date of every release. The documentation of
pino, pino-http, pino-pretty and of NestJS itself is not here; if something about the package is not found in these
documents, it is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/nestjs-pino/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### express

**Коли піднімати.** Пишете сервер на Express.

**Порт** 8791, сервер `express-docs`. Підняти: `./df express serve`. Адреса: `http://127.0.0.1:8791/mcp`.

**Обсяг.** Документів: 842, фрагментів: 4 823.

**Опис.**

Тридцять перший примірник фабрики: захищений MCP-сервер, що відповідає на питання про Express — мінімалістичний
вебфреймворк для Node.js: маршрути, проміжні обробники (middleware), об'єкти запиту й відповіді. Тут сайт
expressjs.com для Express 5.x і 4.x, довідник API 3.x і документація 2.x, спільні посібники й сторінки офіційних
middleware, блог, журнал змін `History.md`, README кожної стабільної версії, нотатки релізів і реєстр версій npm.
Поруч — README кожної версії й журнали змін п'ятнадцяти офіційних middleware, маршрутизатора `router`, синтаксису
шляхів `path-to-regexp`, заголовків безпеки `helmet` і обмежувача частоти `express-rate-limit` з його документацією.
Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Express documentation in English -- the expressjs.com site for Express 5.x and 4.x (getting started,
routing, writing and using middleware, error handling, template engines, behind proxies, debugging, overriding the
API, and the API reference of express(), app, req, res and router), the API reference of 3.x, the 2.x documentation
from the old site, the pages shared by all versions (best practices for security and performance, health checks and
graceful shutdown, security updates, database integration, the migration guides to 4 and to 5, and the official
middleware: body-parser, cors, cookie-parser, cookie-session, compression, morgan, multer, express-session,
serve-static and others), the Express blog, the History.md changelog, the README of every stable version, the GitHub
release notes and the npm registry list. Node.js itself, Koa, Fastify, NestJS and the databases are not here.

**Межі.**

Тут немає документації самого Node.js, інших фреймворків (Koa, Fastify; NestJS — окремий примірник `nestjs`),
шаблонізаторів (Pug, EJS), баз даних і ORM, Passport, сторонніх middleware поза helmet і express-rate-limit, а також
вебплатформи (HTTP, куки, CORS — примірники `mdn` і `webstandards`). Issues і GitHub Discussions свідомо не взято.

**Далі в [README](../instances/express/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Межі,
про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### express-rate-limit

**Коли піднімати.** Обмежуєте частоту запитів до Express.

**Порт** 8812, сервер `express-rate-limit-docs`. Підняти: `./df express-rate-limit serve`. Адреса: `http://127.0.0.1:8812/mcp`.

**Обсяг.** Документів: 391, фрагментів: 1 098.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про express-rate-limit — пакет npm, проміжний шар (middleware) Express,
який обмежує частоту запитів від одного клієнта, — і про шість пакетів його організації: express-slow-down,
rate-limit-redis, rate-limit-memcached, @acpr/rate-limit-postgresql, @express-rate-limit/cluster-memory-store і
ratelimit-header-parser. Відповідає за документацією всіх їхніх стабільних версій: сайтом
express-rate-limit.mintlify.app у стані на кожен реліз, README, типами й журналами змін пакетів, прикладами та
реєстром npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the express-rate-limit documentation -- the express-rate-limit.mintlify.app site as it stood at every
stable release of the express-rate-limit npm package (from 7.x, when the site appeared; configuration, stores,
instance and request API, error codes, proxy troubleshooting, debugging, writing a store); the README of every stable
version (up to 7.0 the README was the whole documentation); the TypeScript declarations; the changelog; and the npm
registry history of the package, including the Node requirement (engines), dependencies and the date of every release.
The same -- README, types, changelog, npm registry -- for the other packages of the express-rate-limit organisation:
express-slow-down, rate-limit-redis, rate-limit-memcached, @acpr/rate-limit-postgresql,
@express-rate-limit/cluster-memory-store and ratelimit-header-parser, with the examples of the last two. The
documentation of Express itself, of Redis, Memcached or PostgreSQL clients, of the IETF RateLimit header drafts and of
Node.js is not here; if something about express-rate-limit is not found in these documents, it is unlikely to be
anywhere in its official documentation.

**Межі.**

Документації Express, клієнтів Redis, Memcached і PostgreSQL, чернеток IETF про заголовки `RateLimit` і Node.js тут
немає, як і інших проміжних шарів безпеки (helmet, cors). Код бібліотек (`source/`) і міграції SQL сховища PostgreSQL
не входять — лише документація. Не взято також: вікі репозиторію (лише сторінки «Moved to mintlify» і застарілі коди
помилок, які тепер на сайті), релізи GitHub (повторюють журнал змін), `security.md`, `contributing.md` і
`code_of_conduct.md` репозиторіїв (порядок участі в розробці; для express-rate-limit він є на сайті).

**Далі в [README](../instances/express-rate-limit/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### fastify

**Коли піднімати.** Пишете сервер на Fastify.

**Порт** 8844, сервер `fastify-docs`. Підняти: `./df fastify serve`. Адреса: `http://127.0.0.1:8844/mcp`.

**Обсяг.** Документів: 9 214, фрагментів: 20 103.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Fastify — швидкий вебфреймворк для Node.js (альтернативу Express):
маршрути зі схемами JSON (валідація й серіалізація), система плагінів з інкапсуляцією, хуки життєвого циклу запиту,
декоратори, обробка помилок, логування (pino), TypeScript. Документація — довідник і посібники кожного стабільного
випуску від 1.0.0 до 5.12.7 (з них збирається сайт fastify.dev), код ядра, тести, приклади, нотатки випусків, а також
README і типи TypeScript близько 160 пакетів екосистеми: офіційних плагінів `@fastify/*`, складників ядра
(`fastify-plugin`, `avvio`, `find-my-way`, `light-my-request`, `fast-json-stringify`, `secure-json-parse`,
`fastify-cli`) і старих плагінів `fastify-*`. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Fastify documentation -- the official docs and README of every stable release of the core, its
source, tests, examples and release notes, and the README and TypeScript declarations of the official plugins, core
components and legacy plugin packages. The documentation of Node.js, pino and other frameworks is not here; if
something about Fastify is not found in these documents, it is unlikely to be in its official documentation. The
Node.js runtime itself is documented by the nodejs-docs server.

**Межі.**

- Лише стабільні випуски: Fastify 6 (alpha, rc) не взято; пре-релізи пакетів теж.
- pino (логер) — окремий проєкт; його документації тут немає, лише те, що про нього кажуть документи Fastify.
- Інші сторонні плагіни спільноти, яких немає в організації fastify, не беруться; їх перелік — у `docs-guides-ecosystem`.
- Сайт fastify.dev збирається з `docs/` ядра, тож окремо його не завантажено.

**Далі в [README](../instances/fastify/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### trpc

**Коли піднімати.** З'єднуєте клієнт і сервер TypeScript через tRPC.

**Порт** 8903, сервер `trpc-docs`. Підняти: `./df trpc serve`. Адреса: `http://127.0.0.1:8903/mcp`.

**Обсяг.** Документів: 1 603, фрагментів: 5 037.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про tRPC — бібліотеку типобезпечних API на TypeScript без схем і
генерації коду (сайт trpc.io, репозиторій trpc/trpc, реєстр npm). Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the tRPC documentation -- the library for end-to-end typesafe APIs in TypeScript without schemas or code
generation (site trpc.io, repository trpc/trpc, the npm registry): the pages of the site at the last tag of every
minor of tRPC 3.3 to 11.21 (the server: routers, procedures, context, middlewares, validators, errors, data
transformers, server-side calls, adapters, subscriptions; the client: links, the TanStack React Query and classic
React Query integrations, Next.js; the migration guides, the FAQ and the blog), the README files of the root and of
every package at the same tags (0.7 to 3.2 have only these), the agent skills of the packages, the GitHub releases,
the npm registry of eight @trpc/* packages and the examples of the repository. The documentation of Next.js, React,
TanStack Query and Zod as their own projects is not here; if something about tRPC is not found in these documents, it
is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/trpc/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### next-safe-action

**Коли піднімати.** Робите серверні дії Next.js із перевіркою вхідних даних через next-safe-action.

**Порт** 8905, сервер `next-safe-action-docs`. Підняти: `./df next-safe-action serve`. Адреса: `http://127.0.0.1:8905/mcp`.

**Обсяг.** Документів: 577, фрагментів: 1 955.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про next-safe-action — бібліотеку типобезпечних перевірених Server
Actions для Next.js (сайт next-safe-action.dev, репозиторій next-safe-action/next-safe-action, реєстр npm). Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the next-safe-action documentation -- the library for type-safe, validated Server Actions in Next.js
(site next-safe-action.dev, repository next-safe-action/next-safe-action, the npm registry): the pages of the site at
the last tag of every minor of next-safe-action 4.0 to 8.7 (the action client, input and output validation, the action
result, error handling, middleware, the hooks, form actions, optimistic updates, bind arguments, metadata,
integrations with React Hook Form, TanStack Query and Better Auth, the API reference, the migration guides), the
README files of the root and of the package at the same tags (1.0 to 3.4 have only these), the README and changelog of
the adapter packages, the GitHub releases and the npm registry of four packages. The documentation of Next.js, React,
Zod and the integrated libraries as their own projects is not here; if something about next-safe-action is not found
in these documents, it is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/next-safe-action/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### zod

**Коли піднімати.** Перевіряєте дані через Zod, зокрема перехід з версії 3 на 4.

**Порт** 8770, сервер `zod-docs`. Підняти: `./df zod serve`. Адреса: `http://127.0.0.1:8770/mcp`.

**Обсяг.** Документів: 701, фрагментів: 3 446.

**Опис.**

Десятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Zod за офіційною документацією всіх його
версій — від 1.0.0 (березень 2020) до поточної 4.x, разом з alpha, beta й canary, — за README кожної версії npm,
нотатками релізів і реєстром версій npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`;
ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Zod documentation -- the docs kept in the colinhacks/zod repository on every release tag
(from 1.x in 2020 to the current 4.x), the zod.dev site since 3.25 with Zod Mini and @zod/core, the blog, each
distinct text once with all the versions it belongs to; the README of every stable, alpha, beta and canary release on
npm (the whole documentation up to 3.x, and the only text of the 2.x line, which never had a stable release); the
GitHub release notes; and the npm registry list of every published version with its date, dist-tag, import paths and
dependencies. Libraries built on Zod (tRPC, react-hook-form resolvers, zod-to-json-schema) are not here; if something
about Zod is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

Бібліотек довкола Zod тут немає: `@hookform/resolvers`, `zod-to-json-schema`, tRPC та інших. Документація `zod/v3`
у пакетах 4.x — та сама, що в `packages/docs-v3`, окремо не збиралася.

**Далі в [README](../instances/zod/README.md):** Навіщо вся історія; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code; На іншій машині.

### class-validator

**Коли піднімати.** Перевіряєте об'єкти через декоратори class-validator, зазвичай у NestJS.

**Порт** 8874, сервер `class-validator-docs`. Підняти: `./df class-validator serve`. Адреса: `http://127.0.0.1:8874/mcp`.

**Обсяг.** Документів: 85, фрагментів: 405.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про пакет npm `class-validator` (валідація класів декораторами для
TypeScript і JavaScript, репозиторій typestack/class-validator) — за документацією усіх його стабільних версій: README
кожної версії, теки `docs` репозиторію, журналу змін, релізів GitHub та історії версій у реєстрі npm. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the class-validator documentation -- the npm package class-validator (TypeStack): the README of every
stable version, the pages of the `docs` folder of the GitHub repository, the changelog and the GitHub release notes,
and the npm registry history of the package, including the dependencies (validator, libphonenumber-js) and the date of
every release. The documentation of class-transformer, the NestJS ValidationPipe, validator.js and other validation
libraries is not here; if something about the package is not found in these documents, it is unlikely to be anywhere
in its official documentation.

**Далі в [README](../instances/class-validator/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### class-transformer

**Коли піднімати.** Перетворюєте звичайні об'єкти на класи через class-transformer.

**Порт** 8875, сервер `class-transformer-docs`. Підняти: `./df class-transformer serve`. Адреса: `http://127.0.0.1:8875/mcp`.

**Обсяг.** Документів: 31, фрагментів: 137.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про пакет npm `class-transformer` (перетворення простих об'єктів у
екземпляри класів і назад декораторами для TypeScript і JavaScript, репозиторій typestack/class-transformer) — за
документацією усіх його стабільних версій: README кожної версії, теки `docs` репозиторію, журналу змін та історії
версій у реєстрі npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі
дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the class-transformer documentation -- the npm package class-transformer (TypeStack): the README of every
stable version, the pages of the `docs` folder of the GitHub repository, the changelog, and the npm registry history
of the package, including the date of every release. The documentation of class-validator, the NestJS ValidationPipe
and other validation or mapping libraries is not here; if something about the package is not found in these documents,
it is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/class-transformer/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### jsonschema

**Коли піднімати.** Пишете JSON Schema або перевіряєте дані через Ajv.

**Порт** 8855, сервер `jsonschema-docs`. Підняти: `./df jsonschema serve`. Адреса: `http://127.0.0.1:8855/mcp`.

**Обсяг.** Документів: 2 214, фрагментів: 9 670.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про JSON Schema — мову перевірки й анотування JSON — і про Ajv,
валідатор JSON Schema та JSON Type Definition для JavaScript і TypeScript. Документація — сайт json-schema.org цілком
(книга Understanding JSON Schema, Learn, нотатки випусків і міграції кожного draft, блог), тексти всіх виданих
специфікацій draft-03…2020-12 і наступного випуску, що ще в розробці, метасхеми, офіційний JSON Schema Test Suite,
сайт ajv.js.org для кожного стабільного тегу 7.0.0–8.20.0, документація Ajv до 7.0, код і тести Ajv, README, релізи й
версії npm самого Ajv і пакетів ajv-formats, ajv-errors, ajv-keywords, ajv-i18n, ajv-cli, ajv-merge-patch,
ajv-draft-04, json-schema-traverse, типи @types/json-schema. Код спільний і лежить у `../../engine/`, `../../server/`
та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the JSON Schema and Ajv documentation -- the site json-schema.org (Understanding JSON Schema, Learn,
specification pages, release and migration notes, blog), the specification texts of draft-03 to 2020-12 and of the
next release in development, the meta-schemas, the JSON Schema Test Suite, the site ajv.js.org for every stable Ajv
7.0-8.20, the Ajv documentation before 7.0, the Ajv source code and tests, the README, release notes and npm versions
of Ajv and its packages (ajv-formats, ajv-errors, ajv-keywords, ajv-i18n, ajv-cli, ajv-merge-patch, ajv-draft-04,
json-schema-traverse), @types/json-schema. If something about JSON Schema or Ajv is not found in these documents, it
is unlikely to be in their official documentation.

**Межі.**

- Лише стабільні версії Ajv і пакетів: бет, rc й альф не взято (у самого Ajv таких тегів 42). README
  ajv-merge-patch 1.0.0 немає: реєстр не віддає її tarball.
- «next» — не виданий випуск: тексти гілки main json-schema-spec на 17.10.2026 змінюються.
- Чернетки draft-00…02 (2009–2010) і Relative JSON Pointer Луффа 2013 року не взято.
- Інші валідатори (jsonschema для Python, Zod, Joi), OpenAPI і сам формат JSON (RFC 8259) — не тут.
- Сторінки сайту з даних, а не з markdown (FAQ, перелік інструментів, приклади використання), не взято.

**Далі в [README](../instances/jsonschema/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### orval

**Коли піднімати.** Генеруєте клієнт API з OpenAPI через orval.

**Порт** 8883, сервер `orval-docs`. Підняти: `./df orval serve`. Адреса: `http://127.0.0.1:8883/mcp`.

**Обсяг.** Документів: 751, фрагментів: 4 319.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про orval — генератор типізованих клієнтів TypeScript зі специфікації
OpenAPI (репозиторій orval-labs/orval, сайт orval.dev) — за документацією всіх його стабільних версій: сайт з тегу
кожної мінорної версії, README ранніх версій, нотатки релізів, приклади репозиторію та історія версій у реєстрі npm.
Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the orval documentation -- the generator of typed TypeScript clients from an OpenAPI (Swagger)
specification (repository orval-labs/orval, site orval.dev): the pages of the site taken from the tag of every minor
version from 3.0 to 8.44 (introduction, installation, quick start, the configuration reference -- input, output,
hooks, a full example --, the CLI, programmatic use, the guides for axios, fetch, React, Vue, Svelte, Solid and
Angular Query, Angular, SWR, Zod, Effect, MSW and Faker mocks, fixtures, enums, Hono, MCP, Pinia Colada, SolidStart,
the base URL, NDJSON streams, and the upgrade page to v8); the README of versions 1.0 to 4.x; the GitHub release notes
of every version from 2.2.0 to 8.44.0 and the old changelog of 1.x to 2.1; the sample projects of samples/ at the tag
v8.44.0; and the npm registry history of the package, including the Node.js requirement (engines) and the date of
every release. The documentation of OpenAPI, TanStack Query, SWR, Zod, MSW, Faker, Hono, Angular, axios and Effect is
not here; if something about orval is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Далі в [README](../instances/orval/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### openapi-typescript

**Коли піднімати.** Генеруєте типи й клієнт з OpenAPI через openapi-typescript.

**Порт** 8884, сервер `openapi-typescript-docs`. Підняти: `./df openapi-typescript serve`. Адреса: `http://127.0.0.1:8884/mcp`.

**Обсяг.** Документів: 556, фрагментів: 1 260.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про openapi-typescript і його родину — openapi-fetch,
openapi-react-query, swr-openapi, openapi-typescript-helpers, openapi-metadata (репозиторій
openapi-ts/openapi-typescript, сайт openapi-ts.dev) — за документацією всіх їхніх стабільних версій: сайт з тегу
кожної мінорної версії, README кожної версії шести пакетів, журнали змін, релізи, приклади та історія версій у реєстрі
npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the openapi-typescript documentation -- the generator of TypeScript types from an OpenAPI 3.0/3.1 schema
and its family: openapi-fetch, openapi-react-query, swr-openapi, openapi-typescript-helpers and openapi-metadata
(repository openapi-ts/openapi-typescript, site openapi-ts.dev): the pages of the site taken from the tag of every
minor version of openapi-typescript from 6.2 to 7.13 (introduction, CLI, Node API, advanced use, examples, the
migration guide to 7.x, the openapi-fetch and openapi-react-query pages); the README of every stable version of the
six packages; the changelogs of openapi-typescript, openapi-fetch, openapi-react-query and openapi-typescript-helpers;
the old site and release notes of swr-openapi (htunnicliff/swr-openapi) and the release notes of swr-openapi and
openapi-metadata in the monorepo; the sample projects of openapi-fetch; and the npm registry history of the six
packages, including the date of every release. The documentation of OpenAPI, TypeScript, TanStack Query, SWR and
Redocly is not here; if something about these packages is not found in these documents, it is unlikely to be anywhere
in their official documentation.

**Далі в [README](../instances/openapi-typescript/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій
теці; Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під
Claude Code.

### helmet

**Коли піднімати.** Ставите заголовки безпеки в Express через Helmet.

**Порт** 8809, сервер `helmet-docs`. Підняти: `./df helmet serve`. Адреса: `http://127.0.0.1:8809/mcp`.

**Обсяг.** Документів: 374, фрагментів: 1 138.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Helmet — пакет npm, який виставляє заголовки безпеки HTTP
(`Content-Security-Policy`, `Strict-Transport-Security` та інші) у застосунках Node.js, насамперед на Express, — за
документацією всіх його стабільних версій: сайтом helmetjs.github.io у стані на кожен реліз, README, типами й журналом
змін пакета та реєстром npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека
тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Helmet documentation -- the helmetjs.github.io site as it stood at every stable release of the helmet
npm package (the Jekyll pages of 2016-2023 and the Hugo pages of 2023 onwards: the reference of every header and the
FAQ); the README of every stable version; SECURITY.md and CONTRIBUTING.md; the TypeScript declarations of the versions
that ship them; the changelog; and the npm registry history of the package, including the Node requirement (engines),
dependencies and the date of every release. The documentation of Express, of the HTTP headers themselves (MDN, the
specifications) and of Node.js is not here; if something about Helmet is not found in these documents, it is unlikely
to be anywhere in its official documentation.

**Межі.**

Документації Express, самих заголовків HTTP (MDN, специфікації) і Node.js тут немає, як і інших проміжних шарів
безпеки (cors, csurf, express-rate-limit). Код бібліотеки (`src/`) не входить — лише документація. Wiki в репозиторія
helmet порожня (лише рядок привітання), тож у корпус не входить.

**Далі в [README](../instances/helmet/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### csrf-csrf

**Коли піднімати.** Захищаєте Express від підробки міжсайтових запитів через csrf-csrf.

**Порт** 8881, сервер `csrf-csrf-docs`. Підняти: `./df csrf-csrf serve`. Адреса: `http://127.0.0.1:8881/mcp`.

**Обсяг.** Документів: 48, фрагментів: 235.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про `csrf-csrf` — пакет npm для захисту застосунків Express від CSRF
(Cross-Site Request Forgery, підробка міжсайтового запиту) за схемою підписаного Double Submit Cookie (репозиторій
Psifi-Solutions/csrf-csrf) — за документацією всіх його стабільних версій: README кожної версії (сайту пакет не має,
README і є документацією), FAQ, посібник переходу між мажорами, журнал змін, приклади репозиторію та історія версій у
реєстрі npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the csrf-csrf documentation -- the npm package `csrf-csrf` (CSRF protection for Express by the signed
Double Submit Cookie pattern): the README of every stable version from 1.0.0 to 4.0.3 and the README of the main
branch with the corrected configuration examples (the package has no documentation site -- the README is the
documentation: doubleCsrf and its options, doubleCsrfProtection, generateCsrfToken, validateRequest,
invalidCsrfTokenError, sessions, asynchronous use), the FAQ, the upgrade guide from 3.x to 4.x, the changelog of every
version from 3.0.0 to 4.0.3, the examples of the repository (Express with an HTML form; an Express backend with
sessions and a React client) and the npm registry history of the package, including the Node.js requirement (engines)
and the date of every release. The documentation of Express, express-session, cookie-parser and NestJS is not here; if
something about the package is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Далі в [README](../instances/csrf-csrf/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### nodemailer

**Коли піднімати.** Надсилаєте пошту з Node.js через Nodemailer.

**Порт** 8810, сервер `nodemailer-docs`. Підняти: `./df nodemailer serve`. Адреса: `http://127.0.0.1:8810/mcp`.

**Обсяг.** Документів: 1 059, фрагментів: 3 039.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Nodemailer — пакет npm для надсилання електронної пошти з Node.js
(SMTP, пул з'єднань, sendmail, SES, DKIM, OAuth2) — за документацією всіх його стабільних версій: сайтом
nodemailer.com у стані на кожен реліз, README, типами, прикладами й журналом змін пакета та реєстром npm. Поруч — те
саме для супутніх пакетів проєкту: mailparser (розбір отриманого листа), smtp-server (SMTP- і LMTP-сервер для прийому
пошти), smtp-connection і mailcomposer як окремі пакети (SMTP-клієнт і збирач листа; останні випуски — 2017 рік). Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Nodemailer documentation -- the nodemailer.com site as it stood at every stable release of the
nodemailer npm package (messages, SMTP and the other transports, DKIM, plugins, guides, errors, the extra modules);
the README of every stable version; SECURITY.md and CONTRIBUTING.md; the TypeScript declarations of the 10.x versions
that ship them; the examples/ folder of the repository at every release that recorded a commit; the changelog; and the
npm registry history of the package, including the Node requirement (engines), dependencies and the date of every
release. The same -- README, changelog, npm registry, and where the package has them SECURITY.md and examples -- for
the companion packages of the Nodemailer project: mailparser, smtp-server, and smtp-connection and mailcomposer as
standalone packages (last released in 2017). The documentation of Node.js, of the SMTP and MIME standards and of the
mail providers (Gmail, SES and others) is not here; if something about Nodemailer or its companion packages is not
found in these documents, it is unlikely to be anywhere in their official documentation.

**Межі.**

Документації Node.js, стандартів SMTP і MIME та поштових провайдерів (Gmail, SES, SendGrid) тут немає — лише те, що
про них пишуть сайт Nodemailer і README пакетів. Код бібліотек (`lib/`, `src/`) не входить — лише документація.

**Далі в [README](../instances/nodemailer/README.md):** Скільки цього; Що в цій теці; Звідки документація; Межі, про
які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### socketio

**Коли піднімати.** Робите двосторонній зв'язок реального часу через Socket.IO.

**Порт** 8793, сервер `socketio-docs`. Підняти: `./df socketio serve`. Адреса: `http://127.0.0.1:8793/mcp`.

**Обсяг.** Документів: 553, фрагментів: 3 781.

**Опис.**

Тридцять третій примірник фабрики: захищений MCP-сервер, що відповідає на питання про Socket.IO — бібліотеку
двобічного обміну подіями в реальному часі між сервером Node.js і клієнтом: події й підтвердження, кімнати й простори
імен, middleware і автентифікація, відновлення з'єднання, кілька серверів через адаптери. Тут сайт socket.io для 4.x,
3.x і 2.x, посібники Get started і How-to, сторінки змін і блог, журнали змін і README пакетів монорепозиторію,
специфікації протоколів, README прикладів, адаптери Redis, Redis Streams, Postgres і MongoDB, Admin UI, README кожної
стабільної версії `socket.io` і `socket.io-client`, нотатки релізів і реєстр npm. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Socket.IO documentation in English -- the socket.io site for 4.x (documentation, tutorial, server and
client API and options, emit cheatsheet), the 3.x and 2.x documentation, the Get started and How-to guides, the
changelog pages, the Socket.IO blog, the CHANGELOG of every package of the socketio/socket.io monorepo, the README of
engine.io, the parsers, the cluster adapter and engine and the emitters, the Engine.IO and Socket.IO protocol
specifications, the README of the examples, the Redis, Redis Streams, Postgres and MongoDB adapters and the Admin UI,
the README of every stable version of socket.io and socket.io-client, the GitHub release notes and the npm registry
list. Node.js itself, Redis, PostgreSQL, MongoDB, NestJS and the raw WebSocket API are not here.

**Межі.**

Тут немає документації самого Node.js, браузерного WebSocket API і пакета `ws` (вебплатформа — примірники `mdn` і
`webstandards`), Redis, PostgreSQL і MongoDB як таких (PostgreSQL — окремий примірник `postgresql`), NestJS (примірник
`nestjs`, глави `@nestjs/websockets`), клієнтів іншими мовами (Java, Swift, C++, Python) і адаптерів хмар поза сайтом
(AWS SQS, Azure Service Bus, Google Pub/Sub описані лише сторінками сайту). Issues і GitHub Discussions свідомо не взято.

**Далі в [README](../instances/socketio/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Межі,
про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### ws

**Коли піднімати.** Робите сервер або клієнт WebSocket на Node.js через ws.

**Порт** 8877, сервер `ws-docs`. Підняти: `./df ws serve`. Адреса: `http://127.0.0.1:8877/mcp`.

**Обсяг.** Документів: 444, фрагментів: 1 162.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про пакет npm `ws` (клієнт і сервер WebSocket для Node.js, репозиторій
websockets/ws) — за документацією усіх його стабільних версій: README кожної версії, довідник API `doc/ws.md` на тегах
репозиторію, History.md ранніх версій, нотатки релізів GitHub та історія версій у реєстрі npm. Разом із ним — три
супутні пакети тієї ж організації: `bufferutil` і `utf-8-validate` (необов'язкові нативні доповнення, що прискорюють
`ws`) та `wscat` (консольний клієнт і сервер WebSocket): їхні README та історія версій у реєстрі npm. Окремо — типи
TypeScript `@types/ws` (файл `index.d.ts` кожної стабільної версії та історія версій у реєстрі npm), бо сама `ws`
типів не несе. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the ws documentation -- the npm package `ws` (WebSocket client and server for Node.js): the README of
every stable version, the API reference doc/ws.md of the repository at the tag of every stable version from 0.4.12,
the History.md of the early versions (0.1.2 to 0.6.4), the GitHub release notes of the later ones and the npm registry
history of the package, including the Node.js requirement (engines), the optional dependencies (bufferutil,
utf-8-validate) and the date of every release; and the README and npm registry history of the companion packages
bufferutil, utf-8-validate and wscat; the index.d.ts and the npm registry history of the typings @types/ws. The
documentation of socket.io, engine.io, the browser WebSocket API and the HTTP module of Node.js is not here; if
something about the package is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Далі в [README](../instances/ws/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### partysocket

**Коли піднімати.** Потрібен клієнт WebSocket із повторним підключенням PartySocket.

**Порт** 8820, сервер `partysocket-docs`. Підняти: `./df partysocket serve`. Адреса: `http://127.0.0.1:8820/mcp`.

**Обсяг.** Документів: 257, фрагментів: 1 139.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про PartySocket — клієнт WebSocket із перепідключенням для PartyKit і
PartyServer (пакет npm `partysocket`) — за офіційною документацією всіх стабільних версій, від 0.0.2 (серпень 2023) до
поточної 1.x: сторінки сайту docs.partykit.io про клієнт у стані на кожен реліз, README кожної версії, код і тести
пакета на кожну версію, журнал змін і історія пакета в реєстрі npm. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official PartySocket documentation -- the pages of docs.partykit.io that cover PartySocket (the
PartySocket API reference and the guides and tutorials that use it) on every stable release, each distinct text once
with all the versions it belongs to; the README of every stable version; the CHANGELOG of the package; the npm
registry history of the partysocket package; and the source code and tests of the package on every stable release.
Socket.IO, ws, reconnecting-websocket on its own and the PartyKit or PartyServer server internals are not here beyond
what these pages say; if something about PartySocket is not found in these documents, it is unlikely to be anywhere in
its official documentation.

**Межі.**

Socket.IO, пакета `ws`, браузерного WebSocket API загалом, Durable Objects і внутрішньої будови серверів PartyKit і
PartyServer тут немає — лише те, що про них показують сторінки поруч із клієнтом. Решта сайту docs.partykit.io (CLI,
конфігурація, сховище, розгортання) не береться: на тих сторінках клієнта немає. Бета-збірки не беруться ні в README,
ні в коді.

**Далі в [README](../instances/partysocket/README.md):** Навіщо код поруч зі сторінками; Скільки цього; Що в цій теці;
Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

<!-- тема: Вхід користувачів і безпека -->

### auth

**Коли піднімати.** Робите вхід користувачів через Better Auth, NextAuth.js або Auth.js.

**Порт** 8797, сервер `auth-docs`. Підняти: `./df auth serve`. Адреса: `http://127.0.0.1:8797/mcp`.

**Обсяг.** Документів: 2 640, фрагментів: 16 597.

**Опис.**

Тридцять сьомий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Better Auth і NextAuth.js /
Auth.js. Тут документація Better Auth кожної мінорної версії від 0.0 до 1.7, NextAuth.js кожної мінорної від 1.1 до
4.24, Auth.js (NextAuth.js v5) на кожній беті від 5.0.0-beta.4 до 5.0.0-beta.32 і довідник API authjs.dev. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents about Better Auth and NextAuth.js / Auth.js in English -- the Better Auth documentation of every minor
version from 0.0 to 1.7 with its endpoints, options and database tables, the NextAuth.js documentation of every minor
version from 1.1 to 4.24, the Auth.js (NextAuth.js v5) documentation of every beta from 5.0.0-beta.4 to 5.0.0-beta.32
and the authjs.dev API reference. Other authentication products and the frameworks themselves are not here.

**Межі.**

Тут немає патчів окремими версіями (у межах мінорної API не змінюється, а текст між патчами різниться правками), бет і
canary Better Auth, журналів змін, документації інших продуктів автентифікації (Clerk і Supabase Auth — у своїх
примірниках, Lucia, Passport, Firebase Auth — ніде) і самих протоколів OAuth 2.0 та OpenID Connect (тексти RFC — у
примірнику `webstandards`). Довідник authjs.dev — лише поточне видання: старіших сайт не публікує.

**Далі в [README](../instances/auth/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Версії у
відповіді; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер
під Claude Code.

### clerk

**Коли піднімати.** Робите вхід користувачів через керований сервіс Clerk.

**Порт** 8766, сервер `clerk-docs`. Підняти: `./df clerk serve`. Адреса: `http://127.0.0.1:8766/mcp`.

**Обсяг.** Документів: 4 129, фрагментів: 30 908.

**Опис.**

Сьомий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Clerk (автентифікація й керування
користувачами) за його офіційною документацією — поточною лінією Core 3 і двома архівними, Core 2 та Core 1, — за
довідниками Backend, Frontend і Platform API, журналом змін і блогом. Код спільний і лежить у `../../engine/`
(завантаження корпусу), `../../server/` (сервер, агент, шари) та `../../common/` (пошук); ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Clerk documentation -- the current line from clerk.com (Core 3, every page in the variant of
every SDK), the archived lines Core 2 and Core 1 from the branches of the clerk/clerk-docs repository, the OpenAPI
references of the Backend, Frontend and Platform APIs, every changelog entry since 2021 and every blog post. Community
SDKs (Angular, Svelte, SolidJS, Rust and others) live outside clerk.com and are not here; if something about Clerk is
not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

Community SDK (Angular, Svelte, SolidJS, Rust, Flutter та інші) живуть поза clerk.com, у своїх репозиторіях, — їх
тут немає. Сторінки C#, Java, PHP і Python на сайті — посилання на GitHub тих SDK, тож їх теж немає. Документації
самих фреймворків (Next.js, Expo, React) тут немає — лише згадки про них у тексті Clerk.

**Далі в [README](../instances/clerk/README.md):** Навіщо архівні лінії; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Токен GitHub; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Спосіб А — власний захищений агент (усі чотири шари); Спосіб Б — сервер під Claude Code (HTTP).

### passport

**Коли піднімати.** Робите вхід через Passport.js та його стратегії.

**Порт** 8871, сервер `passport-docs`. Підняти: `./df passport serve`. Адреса: `http://127.0.0.1:8871/mcp`.

**Обсяг.** Документів: 1 401, фрагментів: 5 418.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Passport.js — проміжний шар автентифікації для Node.js: застосунок
оголошує стратегії (логін і пароль, JWT, OAuth 2.0 через Google), а `passport.authenticate()` запускає одну з них на
запиті; працює з Express і Connect. Документація — всіх стабільних версій пакета passport (0.1–0.7) і тринадцяти
пакетів стратегій: passport-local, passport-jwt, passport-oauth2, passport-google-oauth20, passport-github2,
passport-facebook, passport-http-bearer, passport-openidconnect, passport-saml, passport-azure-ad, passport-twitter,
passport-discord та passport-strategy (базовий клас будь-якої стратегії). Джерела — офіційний сайт passportjs.org,
README і журнали змін, код і тести кожного тегу репозиторіїв та реєстр npm, лише англійською й лише стабільні версії.
Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Passport.js documentation -- the official site passportjs.org (concepts, tutorials, the normalized
profile); the README of every stable version of passport and of the strategies passport-local, passport-jwt,
passport-oauth2, passport-google-oauth20, passport-github2, passport-facebook, passport-http-bearer,
passport-openidconnect, passport-saml, passport-azure-ad, passport-twitter, passport-discord and passport-strategy;
the changelogs and the passport-jwt migration guides; the source code (lib/, src/) and the tests (test/) of every
tagged release of those fourteen packages; and the npm registry history of each, including the Node requirement
(engines), dependencies and the date of every release. The documentation of Express, express-session, NestJS, of
strategies of other packages, and of OAuth, OpenID Connect and JWT as specifications is not here; if something about
Passport is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

Документації Express, express-session, NestJS і `@nestjs/passport`, інших стратегій (passport-apple, passport-auth0,
passport-steam і решти каталогу сайту), пакета `@node-saml/passport-saml` (наступник passport-saml з версії 4), OAuth
2.0, OpenID Connect і JWT як специфікацій, Auth.js, Better Auth, jose та хешування паролів тут немає. Типи
`@types/passport` не входять. Код — лише на тегах і на комітах публікації: коміти гілки master після 0.7.0 без тегу в
корпус не потрапляють.

**Далі в [README](../instances/passport/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в
цій теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### casl

**Коли піднімати.** Описуєте права доступу через CASL.

**Порт** 8882, сервер `casl-docs`. Підняти: `./df casl serve`. Адреса: `http://127.0.0.1:8882/mcp`.

**Обсяг.** Документів: 575, фрагментів: 1 701.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про CASL — ізоморфну бібліотеку авторизації JavaScript (монорепозиторій
stalniy/casl, сайт casl.js.org) — за документацією всіх її стабільних версій: сайт v4–v7 і старий сайт v1–v3, README
кожної версії семи пакетів `@casl/*` і старого пакета `casl`, журнали змін, приклади stalniy/casl-examples та історія
версій у реєстрі npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі
дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the CASL documentation -- the isomorphic JavaScript authorization library (monorepo stalniy/casl, site
casl.js.org): the pages of the site v4 to v7 taken from the tags of @casl/ability 4.0.8 to 7.0.2 (guide, advanced,
cookbook, API of @casl/ability and @casl/ability/extra) and of the old Jekyll site v1 to v3; the README of every
stable version of @casl/ability (2.0.1 to 7.0.2), @casl/react, @casl/vue, @casl/angular, @casl/aurelia,
@casl/mongoose, @casl/prisma and of the old package `casl` (0.2.0 to 1.1.0); the changelog of every package; the
example applications of stalniy/casl-examples (Express, Fastify with Prisma and with ucast SQL, React, Vue, Angular);
and the npm registry history of every package, including the peer dependencies on React, Vue, Angular, Mongoose and
Prisma and the date of every release. The documentation of React, Vue, Angular, Aurelia, Mongoose, Prisma, MongoDB,
Express and NestJS is not here; if something about CASL is not found in these documents, it is unlikely to be anywhere
in its official documentation.

**Далі в [README](../instances/casl/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### jose

**Коли піднімати.** Підписуєте або перевіряєте JWT, JWE, JWK через бібліотеку jose.

**Порт** 8834, сервер `jose-docs`. Підняти: `./df jose serve`. Адреса: `http://127.0.0.1:8834/mcp`.

**Обсяг.** Документів: 7 301, фрагментів: 8 413.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про jose — пакет npm, який реалізує стандарти JOSE: JSON Web Token
(JWT), підпис (JWS), шифрування (JWE), ключі (JWK) і набори ключів (JWKS) на Web Crypto API — у Node.js, браузерах,
Deno, Bun, Cloudflare Workers та інших середовищах edge. Документація — усіх стабільних версій бібліотеки panva/jose
разом із її першою назвою @panva/jose. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the jose documentation -- the README, SECURITY.md and docs/ folder of the panva/jose repository at every
stable release tag (the single API document of 1.x-2.x and @panva/jose, the TypeDoc reference of 3.x-6.x: JWT, JWS,
JWE, JWK, JWKS, key import and export, utilities, error classes, types); the changelog from 0.9.0 on; the GitHub
release notes that add to it (patches of older lines, longer release texts); and the npm registry history of jose and
@panva/jose, including the Node requirement (engines) and the date of every release. The JOSE and JWT RFCs, OAuth and
OpenID Connect clients, the authentication libraries built on jose and Node.js crypto are not here; if something about
jose is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

Текстів RFC (JWT, JWS, JWE, JWK, JWA) тут немає — вони в примірнику `webstandards`; немає й клієнтів OAuth та
OpenID Connect (openid-client), бібліотек автентифікації, що беруть jose всередину (Auth.js, Better Auth, Clerk,
iron-session — для них є свої примірники `auth`, `clerk`, `iron-session`), Next.js і модуля `crypto` Node.js. Код
бібліотеки (`src/`), тести, `CONTRIBUTING.md` і `CODE_OF_CONDUCT.md` не входять. Чужа бібліотека jose 0.1–0.3 (2015)
— лише рядком реєстру.

**Далі в [README](../instances/jose/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### iron-session

**Коли піднімати.** Тримаєте сесію в зашифрованому cookie через iron-session.

**Порт** 8833, сервер `iron-session-docs`. Підняти: `./df iron-session serve`. Адреса: `http://127.0.0.1:8833/mcp`.

**Обсяг.** Документів: 359, фрагментів: 1 053.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про iron-session — пакет npm, який тримає сесію в підписаній і
зашифрованій («запечатаній») куці, без сховища сесій на сервері: дані їдуть у самій куці. Працює з Next.js (App
Router, Pages Router, Route Handlers, Server Actions, middleware і proxy), Express, Koa, модулем `http` Node, Bun і
Deno. Документація — всіх стабільних версій iron-session, його попередника next-iron-session і бібліотеки шифрування
iron-webcrypto, на якій він стоїть. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the iron-session documentation -- the README of every stable version of iron-session, of its predecessor
next-iron-session and of iron-webcrypto (the sealing library underneath); MIGRATION.md and SECURITY.md of 9.x; the
TypeScript declarations of the versions that ship them (including the iron-session/next, /edge, /express and /koa
entry points of 6.x-7.x); the changelogs; the GitHub release notes, among them the upgrade guides of 6.0.0 and 8.0.0;
the example apps of every tagged release (Next.js App Router and Pages Router, Express, Koa); and the npm registry
history of the three packages, including the Node requirement (engines), dependencies and the date of every release.
The documentation of Next.js, of authentication libraries, of JWT and jose, and of Node.js is not here; if something
about iron-session is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

Документації Next.js, бібліотек автентифікації (Auth.js, Better Auth, Clerk), JWT і бібліотеки jose, кук і HTTP
взагалі, Node.js тут немає. Код бібліотеки (`src/`), тести, `AGENTS.md` і `CONTRIBUTING.md` не входять — лише
документація й приклади. Попередній шар шифрування `@hapi/iron` (iron-session до 6.1) теж не входить.

**Далі в [README](../instances/iron-session/README.md):** Навіщо окремий примірник; Історія пакета; Скільки цього; Що
в цій теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### argon2

**Коли піднімати.** Хешуєте паролі через argon2 або `@node-rs/argon2`.

**Порт** 8814, сервер `argon2-docs`. Підняти: `./df argon2 serve`. Адреса: `http://127.0.0.1:8814/mcp`.

**Обсяг.** Документів: 222, фрагментів: 595.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про хешування паролів Argon2 у Node.js — за документацією двох пакетів
npm усіх стабільних версій: `argon2` (node-argon2, прив'язка до еталонної реалізації на C) і `@node-rs/argon2`
(прив'язка на Rust із готовими збірками під платформи), — а також еталонної реалізації P-H-C/phc-winner-argon2 і
специфікації алгоритму. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the argon2 documentation -- the npm package argon2 (node-argon2): the README, TypeScript declarations and
GitHub release notes of every stable version and the GitHub wiki (Options, Migrating from another hash function); the
npm package @node-rs/argon2: the README, TypeScript declarations, changelog and release notes of every stable version;
the npm registry history of both packages, including the Node requirement (engines), dependencies and the date of
every release; and the reference implementation P-H-C/phc-winner-argon2: its README at every release, its changelog
and the Argon2 specification version 1.3. The documentation of node:crypto, bcrypt, RFC 9106 and the OWASP guidance is
not here; if something about these packages is not found in these documents, it is unlikely to be anywhere in their
official documentation.

**Межі.**

Документації `node:crypto` (там `crypto.argon2` з Node 24.7 — примірник `nodejs`), RFC 9106 (примірник `webstandards`),
порад OWASP щодо параметрів (примірник `owasp`), bcrypt, scrypt і фреймворків тут немає. Код бібліотек — ні C, ні Rust,
ні JavaScript — не входить, лише документація. Сторінка man утиліти командного рядка еталонної реалізації не береться:
її прапорці описано в README. Інші пакети Argon2 (`argon2-browser`, `hash-wasm`, `@phc/argon2`) не беруться.

**Далі в [README](../instances/argon2/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### bcrypt

**Коли піднімати.** Хешуєте паролі через bcrypt або bcryptjs.

**Порт** 8873, сервер `bcrypt-docs`. Підняти: `./df bcrypt serve`. Адреса: `http://127.0.0.1:8873/mcp`.

**Обсяг.** Документів: 144, фрагментів: 407.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про хешування паролів bcrypt у Node.js — за документацією двох пакетів
npm усіх стабільних версій: `bcrypt` (репозиторій kelektiv/node.bcrypt.js, прив'язка до реалізації алгоритму на C++) і
`bcryptjs` (репозиторій dcodeIO/bcrypt.js, той самий алгоритм на чистому JavaScript, без нативного модуля). README
кожної версії, типи bcryptjs, журнал змін bcrypt, релізи GitHub, вікі репозиторіїв, політика безпеки bcrypt і історія
версій у реєстрі npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі
дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the bcrypt documentation -- the npm package bcrypt (node.bcrypt.js): the README of every stable version,
the changelog and the GitHub release notes, the GitHub wiki (Installation Instructions, Frequently Asked Questions,
Security Issues and Concerns, Windows Support, bcrypt vs bcrypt.js) and the security policy; the npm package bcryptjs
(bcrypt.js, plain JavaScript): the README, TypeScript declarations and GitHub release notes of every stable version
and the GitHub wiki (Benchmark); and the npm registry history of both packages, including the Node requirement
(engines), dependencies and the date of every release. The documentation of argon2, node:crypto and the OWASP guidance
is not here; if something about these packages is not found in these documents, it is unlikely to be anywhere in their
official documentation.

**Далі в [README](../instances/bcrypt/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### owasp

**Коли піднімати.** Перевіряєте безпеку застосунку: шпаргалки OWASP, Top 10, вимоги ASVS.

**Порт** 8795, сервер `owasp-docs`. Підняти: `./df owasp serve`. Адреса: `http://127.0.0.1:8795/mcp`.

**Обсяг.** Документів: 328, фрагментів: 5 269.

**Опис.**

Тридцять п'ятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про безпеку вебзастосунків і API за
документацією OWASP (Open Worldwide Application Security Project — відкрита спільнота, що пише стандарти й посібники з
безпеки застосунків). Тут усі шпаргалки OWASP Cheat Sheet Series з покажчиками й чернетками, OWASP Top 10 редакцій
2025, 2021, 2017 і 2013, API Security Top 10 редакцій 2023 і 2019, стандарт перевірки ASVS 5.0 і 4.0.3 та Top 10
Proactive Controls редакцій 2024 і 2018 з архівними сторінками 2016 і 2014. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of OWASP in English -- the Cheat Sheet Series (every cheat sheet, its introduction, its index pages mapping
cheat sheets to the Top 10, ASVS, MASVS and the Proactive Controls, two drafts), the OWASP Top 10 of 2025, 2021, 2017
and 2013, the API Security Top 10 of 2023 and 2019, the Application Security Verification Standard 5.0 and 4.0.3, and
the Top 10 Proactive Controls of 2024 and 2018 with the archive pages of 2016 and 2014. The Mobile and LLM lists,
OWASP tools and the documentation of frameworks are not here.

**Межі.**

Тут немає Top 10 2010, 2007, 2004 і 2003 (їх тексту немає ні в репозиторіях OWASP, ні на owasp.org), ASVS 3.0 (від
неї лишилися тільки таблиці), перекладів, Mobile (MASVS, MASTG) і LLM Top 10, Testing Guide (WSTG), інструментів OWASP
(ZAP, Dependency-Check, Juice Shop) і документації фреймворків — вона в своїх примірниках.

**Далі в [README](../instances/owasp/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Межі,
про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

<!-- тема: Бази даних і ORM -->

### postgresql

**Коли піднімати.** Пишете запити або адмініструєте сервер PostgreSQL.

**Порт** 8792, сервер `postgresql-docs`. Підняти: `./df postgresql serve`. Адреса: `http://127.0.0.1:8792/mcp`.

**Обсяг.** Документів: 3 620, фрагментів: 30 609.

**Опис.**

Тридцять другий примірник фабрики: захищений MCP-сервер, що відповідає на питання про PostgreSQL — мову SQL і її
розширення в PostgreSQL, індекси, транзакції й рівні ізоляції, продуктивність і `EXPLAIN`, налаштування сервера,
автентифікацію й ролі, резервне копіювання, реплікацію, обслуговування й `VACUUM`, PL/pgSQL, довідник команд і програм
(`psql`, `pg_dump`, `pg_restore`). Тут офіційна документація кожного мажору від 9.0 до 19 разом із нотатками релізів.
Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the PostgreSQL documentation in English, for every major version from 9.0 to 19 -- the tutorial, the SQL
language (syntax, data definition, queries, data types, functions and operators, indexes, full text search,
concurrency control, performance tips), server administration (installation, server configuration, client
authentication, roles, maintenance, backup and restore, high availability and replication, monitoring, WAL, logical
replication), client interfaces (libpq, ECPG, the information schema), server programming (extensions, PL/pgSQL,
triggers, rules), the reference of every SQL command and client and server application, internals, and the appendixes
(error codes, date and time, additional modules, release notes). Drivers and ORMs (node-postgres, Prisma, TypeORM),
extensions outside the core distribution (PostGIS, TimescaleDB) and managed services are not here.

**Межі.**

Тут немає документації драйверів і ORM (node-postgres, Prisma, TypeORM, Drizzle), розширень поза `contrib` (PostGIS,
TimescaleDB, pgvector), керованих сервісів (Supabase — окремий примірник `supabase`, RDS, Neon), операторів Kubernetes і
пулерів (PgBouncer). Wiki postgresql.org і розсилки свідомо не взято.

**Далі в [README](../instances/postgresql/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація;
Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### postgres-image

**Коли піднімати.** Запускаєте PostgreSQL в офіційному образі Docker: змінні, томи, початкові скрипти.

**Порт** 8807, сервер `postgres-image-docs`. Підняти: `./df postgres-image serve`. Адреса: `http://127.0.0.1:8807/mcp`.

**Обсяг.** Документів: 3 795, фрагментів: 7 233.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про офіційний Docker-образ PostgreSQL (`postgres` на Docker Hub) за
його документацією: сторінкою образу в кожній редакції з 2014 року й репозиторієм `docker-library/postgres` —
Dockerfile усіх стабільних мажорів від 8.4 до 18, скриптами входу, шаблонами та `versions.json`. Код спільний і лежить
у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Docker image of PostgreSQL ("postgres" on Docker Hub) -- the image page
(docker-library/docs, postgres/README.md and the compose example) in every revision since 2014, and the image
repository docker-library/postgres: the Dockerfile of every stable PostgreSQL major from 8.4 to 18 in every variant
the repository ever had (Debian default, wheezy to trixie, alpine and every alpine3.x) in every revision with its
exact PostgreSQL version, the docker-entrypoint.sh and docker-ensure-initdb.sh scripts, the Dockerfile templates,
update.sh, versions.sh, apply-templates.sh, generate-stackbrew-library.sh and versions.json, each distinct text once
with all the versions it belongs to. Beta releases and the PostgreSQL server documentation itself are not here; if
something about running PostgreSQL in Docker is not found in these documents, it is unlikely to be anywhere in the
official image documentation.

**Межі.**

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

**Далі в [README](../instances/postgres-image/README.md):** Що сюди входить; Скільки цього; Межі, про які треба
пам'ятати; Що в цій теці; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### node-postgres

**Коли піднімати.** Звертаєтеся до PostgreSQL із Node.js через пакет `pg`.

**Порт** 8805, сервер `node-postgres-docs`. Підняти: `./df node-postgres serve`. Адреса: `http://127.0.0.1:8805/mcp`.

**Обсяг.** Документів: 587, фрагментів: 1 551.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про node-postgres — пакет `pg` для роботи з PostgreSQL з Node.js — за
офіційною документацією всіх стабільних версій: сайтом node-postgres.com у стані на кожен реліз `pg` з 2019 року,
README кожної версії кожного пакета монорепозиторію й супутніх пакетів, журналом змін, сторінками вікі, типами
`@types/pg` з DefinitelyTyped і історією версій одинадцяти пакетів у реєстрі npm. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official node-postgres documentation -- the node-postgres.com site as it stood at every stable
release of pg since 2019, each distinct text once with all the versions it belongs to; the README of every stable
release of pg, pg-pool, pg-cursor, pg-query-stream, pg-connection-string, pg-native, pg-protocol, pg-types,
pg-copy-streams and pg-format; the changelog of the monorepo; the FAQ and Extras pages of the GitHub wiki; the
@types/pg type definitions from DefinitelyTyped as every version shipped them; and the npm registry history of all
eleven packages. PostgreSQL itself, Node.js, ORMs and query builders are not here; if something about node-postgres is
not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

PostgreSQL (SQL, індекси, налаштування сервера) — у примірнику `postgresql`, Node.js — у `nodejs`. ORM і будівників
запитів на основі `pg` (Prisma, TypeORM, Knex, Drizzle, Sequelize) тут немає. Журнал змін `pg` пише лише мажорні й
мінорні релізи; про виправлення в патчах кажуть README і документи реєстру npm. Сайтів супутніх пакетів немає — лише
README.

**Далі в [README](../instances/node-postgres/README.md):** Що сюди входить і чому одним примірником; Скільки цього; Що
в цій теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### mysql

**Коли піднімати.** Пишете запити до MySQL, адмініструєте сервер або звертаєтеся до нього через драйвер, зокрема `mysql2`. Працює лише на цій машині.

**Порт** 8952, сервер `mysql-docs`. Підняти: `./df mysql serve`. Адреса: `http://127.0.0.1:8952/mcp`.

**Обсяг.** Документів: 12 935, фрагментів: 29 275.

**Опис.**

Цей примірник шукає в документації MySQL. MySQL — це сервер реляційної бази даних: він зберігає дані в таблицях і
виконує запити мовою SQL. Застосунок звертається до сервера через драйвер, тобто бібліотеку для своєї мови
програмування. Тому тут лежать і довідник самого сервера, і документація драйверів. MariaDB — окремий продукт, що
колись відгалузився від MySQL. Її документація лежить у примірнику [`mariadb`](../instances/mariadb/README.md).

**Склад (так його описано моделі, англійською).**

Documents of the MySQL documentation: the Reference Manual, the official drivers, the npm packages and the Docker
image.

**Далі в [README](../instances/mysql/README.md):** Що всередині; Чого тут немає; Чому файли завантажує людина; Корпус
лише локально; Як запустити.

### mariadb

**Коли піднімати.** Пишете запити до MariaDB, налаштовуєте Galera чи MaxScale або звертаєтеся до сервера через конектор, зокрема пакет `mariadb`.

**Порт** 8953, сервер `mariadb-docs`. Підняти: `./df mariadb serve`. Адреса: `http://127.0.0.1:8953/mcp`.

**Обсяг.** Документів: 9 283, фрагментів: 56 847.

**Опис.**

Цей примірник шукає в документації MariaDB. MariaDB — це сервер реляційної бази даних: він зберігає дані в таблицях і
виконує запити мовою SQL. Колись MariaDB відгалузилася від MySQL, але тепер це окремий продукт, і багато що в ньому
працює інакше. Тому документація MySQL лежить в окремому примірнику [`mysql`](../instances/mysql/README.md).

**Склад (так його описано моделі, англійською).**

Documents of the MariaDB documentation: the server, release notes, connectors, Galera, MaxScale, ColumnStore, tools,
the npm package and the Docker image. The site has one current edition and carries no version.

**Далі в [README](../instances/mariadb/README.md):** Що всередині; Важливі межі; Ліцензія; Архівний режим; Як
запустити.

### postgrator

**Коли піднімати.** Виконуєте міграції PostgreSQL через postgrator.

**Порт** 8806, сервер `postgrator-docs`. Підняти: `./df postgrator serve`. Адреса: `http://127.0.0.1:8806/mcp`.

**Обсяг.** Документів: 104, фрагментів: 264.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про postgrator — бібліотеку міграцій SQL для Node.js (PostgreSQL,
MySQL, SQL Server, SQLite) — за документацією всіх його 65 версій npm, від 0.0.1 (2012) до 8.0.0 (2024). Код спільний
і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the postgrator documentation -- the README of every one of its 65 npm versions (0.0.1 to 8.0.0), each
distinct text once with all the versions it belongs to; the TypeScript declarations (postgrator.d.ts) of every version
that ships them; the example scripts (examples/) of the repository at the commit of every version; the changelog; and
the npm registry history of the package, including the Node requirement (engines), dependencies and the date of every
release. The documentation of the database drivers (pg, mysql, mssql, sqlite3), of SQL and of Node.js is not here; if
something about postgrator is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Межі.**

Документації драйверів (`pg`, `mysql2`, `tedious`, `sqlite3`), SQL і Node.js тут немає, як і інших інструментів
міграцій (knex, Flyway, node-pg-migrate). Журнал змін на master неповний для найстарших версій: до 2.0.0 записів
немає, а для 41 версії з 65 запис є. Код бібліотеки (`lib/`) не входить — лише документація.

**Далі в [README](../instances/postgrator/README.md):** Навіщо вся історія; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### drizzle

**Коли піднімати.** Працюєте з базою через Drizzle ORM.

**Порт** 8830, сервер `drizzle-docs`. Підняти: `./df drizzle serve`. Адреса: `http://127.0.0.1:8830/mcp`.

**Обсяг.** Документів: 1 404, фрагментів: 4 383.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Drizzle — ORM для TypeScript від drizzle-team (PostgreSQL, MySQL,
SQLite, SingleStore) разом із CLI міграцій drizzle-kit, Drizzle Studio, генератором тестових даних drizzle-seed і
генераторами схем валідації (drizzle-zod, drizzle-typebox, drizzle-valibot, drizzle-arktype). Джерела — сайт
orm.drizzle.team (репозиторій drizzle-team/drizzle-orm-docs), монорепозиторій drizzle-team/drizzle-orm і реєстр npm,
лише англійською й лише стабільні версії. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`;
ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Drizzle documentation -- the site orm.drizzle.team as it stood for every stable drizzle-orm
release from 0.29.1 to 0.45.4, with get started for every driver, schema, queries, relational queries, migrations,
drizzle-kit, Drizzle Studio, seeding, validators, guides and tutorials; the markdown of the drizzle-team/drizzle-orm
repository at every stable tag from 0.17.0; the changelogs of every package; the release notes of drizzle-kit
0.17.0-0.23.1; and the npm version table of every Drizzle package. Only stable releases are here: Drizzle 1.0 beta and
RC are not. If something about stable Drizzle is not found in these documents, it is unlikely to be anywhere in its
official documentation.

**Межі.**

Тут немає Drizzle 1.0 (бет і RC), Prisma, TypeORM, Kysely й Knex поза сторінками порівняння й інтеграції, мови SQL і
самих серверів баз (є окремий примірник `postgresql`), API драйверів (є `node-postgres`), бібліотек Zod, Valibot і
TypeBox як таких (є `zod`). Сайт до грудня 2023 є лише в README монорепозиторію.

**Далі в [README](../instances/drizzle/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Версії
у відповіді; Межі, про які треба пам'ятати; Сховище сирого; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### prisma

**Коли піднімати.** Працюєте з базою через Prisma.

**Порт** 8831, сервер `prisma-docs`. Підняти: `./df prisma serve`. Адреса: `http://127.0.0.1:8831/mcp`.

**Обсяг.** Документів: 13 686, фрагментів: 39 131.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Prisma — ORM для TypeScript і Node.js (схема Prisma, Prisma Client,
Prisma Migrate, CLI `prisma`) для PostgreSQL, MySQL, MariaDB, SQLite, SQL Server, CockroachDB і MongoDB, разом із
платформою навколо нього (Prisma Postgres, Accelerate, Optimize, Studio, Console) і з документацією попереднього
продукту, Prisma 1. Джерела — сайт prisma.io/docs (репозиторій prisma/web, раніше prisma/docs), монорепозиторій
prisma/orm (раніше prisma/prisma), архівний репозиторій prisma/prisma1 і реєстр npm, лише англійською й лише стабільні
версії. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Prisma documentation -- the site prisma.io/docs as it stood for every stable Prisma release
from 2.0.0 to 7.10.0, with getting started, the Prisma schema, Prisma Client, Prisma Migrate, the CLI and
prisma.config.ts, driver adapters, Prisma Postgres, Accelerate, Optimize, Pulse, Studio, the Console, guides and the
reference; the markdown of the prisma/prisma repository at every stable tag; the release notes of every stable
release; and the npm version table of the CLI, Prisma Client, the driver adapters and the extensions. Only stable
releases are here: Prisma ORM 8 (its release candidates) and Prisma Next are not. If something about stable Prisma is
not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

Тут немає Prisma ORM 8 (кандидатів 8.0.0-rc) і Prisma Next, блогу prisma.io/blog, Drizzle, TypeORM, Sequelize,
MikroORM, Kysely й Knex поза сторінками порівняння й переходу (є окремий примірник `drizzle`), мови SQL і самих
серверів баз (є `postgresql`), API драйверів (є `node-postgres`), NestJS і Next.js поза посібниками Prisma (є `nestjs` і
`nextjs`).

**Далі в [README](../instances/prisma/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Версії
у відповіді; Межі, про які треба пам'ятати; Сховище сирого; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### typeorm

**Коли піднімати.** Працюєте з базою через TypeORM.

**Порт** 8868, сервер `typeorm-docs`. Підняти: `./df typeorm serve`. Адреса: `http://127.0.0.1:8868/mcp`.

**Обсяг.** Документів: 19 759, фрагментів: 54 916.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про TypeORM — ORM для TypeScript і JavaScript (PostgreSQL, CockroachDB,
MySQL, MariaDB, SQLite, Microsoft SQL Server, Oracle, SAP HANA, Google Spanner, MongoDB, sql.js, Capacitor, Cordova,
Expo, React Native): сутності й колонки, зв'язки, `DataSource` і його параметри, `EntityManager` і `Repository`,
параметри `find`, QueryBuilder, міграції й CLI, транзакції, підписники, драйвери кожної бази й перехід з 0.3 на 1.0.
Джерела — головний репозиторій typeorm/typeorm на кожному стабільному тезі (документація, код і тести), його
`CHANGELOG.md` і релізи GitHub та реєстр npm, лише англійською й лише стабільні версії. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the TypeORM documentation -- the documentation of every stable release from 0.1.0 to 1.1.2 (the
typeorm.io site of 1.x, the v0.typeorm.io site of 0.3.25-0.3.31, the docs/*.md pages before), the README of every
stable npm release from 0.0.1, CHANGELOG.md and the GitHub release notes, the source code with its JSDoc and the tests
of every stable tag, @typeorm/codemod and @typeorm/legacy-naming-strategies, the npm version table of each package.
The database servers, @nestjs/typeorm and other ORMs are not here; if something about TypeORM is not found in these
documents, it is unlikely to be in its official documentation.

**Межі.**

Тут немає бет 1.0 і нічних збірок, перекладу документації китайською (`docs/zh_CN`), модуля інтеграції
`@nestjs/typeorm` (є примірник `nestjs`), самих серверів баз (є `postgresql`, `sqlserver`, `mongodb`), драйвера `pg`
(є `node-postgres`), інших ORM (є `prisma`, `drizzle`, `mongoose`). У 0.0.x теки `docs/` не було: документацію тих
версій дає лише README. Пакет `@typeorm/legacy-naming-strategies` представлено README й реєстром, без коду.

**Далі в [README](../instances/typeorm/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Версії
у відповіді; Межі, про які треба пам'ятати; Сховище сирого; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### mikro-orm

**Коли піднімати.** Працюєте з базою через MikroORM.

**Порт** 8885, сервер `mikro-orm-docs`. Підняти: `./df mikro-orm serve`. Адреса: `http://127.0.0.1:8885/mcp`.

**Обсяг.** Документів: 1 217, фрагментів: 4 901.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про MikroORM — ORM для TypeScript і Node.js (репозиторій
mikro-orm/mikro-orm, сайт mikro-orm.io) — і його модуль NestJS @mikro-orm/nestjs за документацією всіх стабільних
версій: сайт з тегу кожної мінорної версії, README кожної версії, журнали змін, релізи модуля NestJS та історія версій
у реєстрі npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the MikroORM documentation -- the TypeScript ORM for Node.js on the Data Mapper, Unit of Work and
Identity Map patterns (repository mikro-orm/mikro-orm, site mikro-orm.io) and its NestJS module @mikro-orm/nestjs: the
pages of the site taken from the tag of every minor version from 3.0 to 7.2 (entities, relations, EntityManager,
repositories, QueryBuilder, filters, populate, transactions, RequestContext, migrations, seeders, entity generator,
CLI, drivers and configuration, events, serialization, use with NestJS, Express and Fastify, upgrade pages between
majors); the old Jekyll site of 2.0 to 2.7; the README of every stable version of the package mikro-orm; the changelog
of every version from 2.0.0 to 7.2.x; the README, changelog and release notes of @mikro-orm/nestjs; and the npm
registry history of mikro-orm, @mikro-orm/core and @mikro-orm/nestjs, including the Node.js requirement (engines) and
the date of every release. The documentation of SQL, the databases, Knex, Kysely, TypeScript and NestJS is not here;
if something about MikroORM is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Далі в [README](../instances/mikro-orm/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### supabase

**Коли піднімати.** Будуєте застосунок на Supabase: база, вхід, сховище, функції.

**Порт** 8764, сервер `supabase-docs`. Підняти: `./df supabase serve`. Адреса: `http://127.0.0.1:8764/mcp`.

**Обсяг.** Документів: 1 717, фрагментів: 20 330.

**Опис.**

П'ятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Supabase — як його налаштувати й як ним
користуватися — за офіційною документацією: гайдами й статтями troubleshooting, референсом клієнтських бібліотек
(поточним і старими мажорними версіями), CLI, Management API і REST API серверів, довідниками налаштувань
`config.toml` і змінних оточення self-hosting, а також каталогом функцій, журналом змін, Supabase Library, блогом і
кейсами. Код спільний і лежить у `../../engine/` (завантаження корпусу), `../../server/` (сервер, агент, шари) та
`../../common/` (пошук); ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Supabase documentation -- every guide page and troubleshooting article of supabase.com/docs,
the features catalog, the current reference of the JavaScript, Dart, Swift, Kotlin, Python and C# client libraries and
the older majors the site still shows (marked legacy), the Server SDK and its middleware, the CLI and the Management
API, the REST APIs of the Auth, Storage and Analytics servers, the configuration references of `supabase/config.toml`
and of the self-hosted Auth, Storage, Realtime, Analytics and Edge Functions servers, Supabase Library, the changelog,
the blog and customer stories. There is no version filter: this is the current text of a continuously deployed
platform. Postgres, PostgREST, Deno and the frameworks and hosts Supabase integrates with are not here; only
Supabase's own side of each integration is.

**Межі.**

Корпус каже, що документація *описує* зараз, а не що робить конкретний проєкт: панель Supabase змінюється частіше
за документацію, і назва кнопки в гайді може вже не збігатися з тим, що на екрані. Документації Postgres,
PostgREST, Deno, Astro, Next.js та інших інструментів, з якими Supabase працює, тут немає — лише бік Supabase в
кожній інтеграції. Якщо на питання відповіді в документах немає, сервер так і скаже — це його робота.

**Далі в [README](../instances/supabase/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Спосіб А — власний захищений агент (усі чотири шари); Спосіб Б — сервер під Claude Code (HTTP).

### sqlserver

**Коли піднімати.** Працюєте із SQL Server: мова T-SQL, адміністрування, життєвий цикл версій.

**Порт** 8864, сервер `sqlserver-docs`. Підняти: `./df sqlserver serve`. Адреса: `http://127.0.0.1:8864/mcp`.

**Обсяг.** Документів: 159 538, фрагментів: 353 445.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `aspnetcore-docs` (8862),
`csharp-docs` (8878), `dotnet-docs` (8866), `dotnet-testing-docs` (8870), `entityframework-docs` (8865), `nuget-docs`
(8869), `testcontainers-dotnet-docs` (8867).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Microsoft SQL Server і Azure SQL. Документація — сайт
learn.microsoft.com/sql англійською в кожній редакції: SQL Server 2017, 2019, 2022 і 2025 разом із SQL Server on Linux
тієї версії, SQL Server 2016 таким, яким сайт показував його до кінця підтримки, і ті самі сторінки для Azure SQL
Database, Azure SQL Managed Instance, Azure Synapse Analytics, Fabric Data Warehouse і SQL database у Fabric (T-SQL,
рушій бази, резервні копії й відновлення, групи доступності, безпека, темпоральні таблиці, JSON, Query Store, Linux і
контейнери, драйвери, ODBC, SSMS, sqlcmd, SqlPackage, Reporting Services, Integration Services, MDX і DMX, SSMA); сайт
learn.microsoft.com/azure/azure-sql і /data-migration; статті підтримки learn.microsoft.com/troubleshoot/sql; сторінки
життєвого циклу (дати початку й кінця підтримки) SQL Server 2014–2025 з learn.microsoft.com/lifecycle; архів Books
Online SQL Server 2014, 2012, 2008 R2, 2008 і 2005 з learn.microsoft.com/previous-versions; пакети `mssql` і `tedious`
(npm), `Microsoft.Data.SqlClient` (NuGet), `mssql-python` (PyPI), `mssql-jdbc` (Maven); теги образу
`mcr.microsoft.com/mssql/server` і README microsoft/mssql-docker; приклади sql-server-samples; журнали змін, нотатки
випусків і сталі релізи go-sqlcmd, DacFx, SqlClient, mssql-jdbc, mssql-python (з його вікі), node-mssql, tedious і
розширення MSSQL для VS Code. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека
тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the SQL Server documentation -- the pages of learn.microsoft.com/sql for SQL Server 2016, 2017, 2019,
2022 and 2025 (with SQL Server on Linux) and for Azure SQL Database, Azure SQL Managed Instance, Azure Synapse
Analytics, Fabric Data Warehouse and SQL database in Fabric; learn.microsoft.com/azure/azure-sql and /data-migration;
the SQL Server troubleshooting articles; the archived Books Online of SQL Server 2014, 2012 and 2008 R2; the npm,
NuGet, PyPI and Maven packages of the drivers; the mcr.microsoft.com/mssql/server image tags; sql-server-samples; the
docs and release notes of go-sqlcmd, DacFx, SqlClient, mssql-jdbc, mssql-python, node-mssql, tedious and the MSSQL
extension for VS Code. .. 2008 R2), cloud products carry their name (azure-sql-database, fabric-sql-database ...),
drivers and tools carry their own name (mssql-12.7, sqlclient-7.1, jdbc-13.6 ...). If something about SQL Server is
not found in these documents, it is unlikely to be in its official documentation. This set is part of the .NET family:
dotnet-docs (the .NET platform: runtime, base class library, CLI, F#, Visual Basic), csharp-docs (the C# language, its
standard and compiler), aspnetcore-docs (ASP.NET Core and classic ASP.NET), entityframework-docs (EF Core and EF6),
sqlserver-docs (SQL Server and Azure SQL), dotnet-testing-docs (xUnit, NUnit, bUnit, Moq, NSubstitute,
FluentAssertions, Shouldly, AngleSharp, Respawn), testcontainers-dotnet-docs (Testcontainers for .NET) and nuget-docs
(NuGet) are meant to be connected together -- when a question belongs to another member, name its server. Playwright
for .NET is outside the family, on playwright-docs.

**Межі.**

- Монікерів Analytics Platform System (`aps-pdw-2016`) і Azure SQL Edge не взято: продукти зняті з підтримки. SQL
  Server 2016 на Linux не існувало.
- Приватний репозиторій `MicrosoftDocs/reusable-content` недоступний: його вставки (підготовка Azure CLI, шаблони
  сторінок Azure Monitor — 89 посилань на 40 сторінках) випадають; так само приклади з приватних `azure-dev-docs-pr` і
  `azure-compute-docs-pr`. Зображення й схеми не беруться.
- Довідника T-SQL в архіві 2014 немає (сторінки 2014 посилаються на чинний сайт), тож T-SQL 2014 відповідає редакція
  2016 і новіші; T-SQL 2012, 2008 R2, 2008 і 2005 — є. Сторінки-контейнери архіву без тексту (90 на всі п'ять версій)
  і 10 адрес архіву 2014, що переадресовують на чинний сайт, не записано. Сироти архіву, на які не веде ні зміст, ні
  посилання, обходом не знаходяться; згенерований довідник класів .NET (SMO, AMO, RMO) відкинуто полем `skip_meta`.
- Лише сталі випуски пакетів і релізів; нотатки DacFx і SqlPackage репозиторій тримає тільки для передвипусків, тож
  сталі нотатки SqlPackage — зі сторінки sql-docs `tools/sqlpackage/release-notes-sqlpackage`. Maven README не має.
- Статті підтримки, data-migration, mssql-docker і sql-server-samples — поточний стан без версій. `CHANGELOG.txt`
  node-mssql закінчується на 11.0.1, далі історія — у релізах GitHub.
- Сайт — англійською; переклади не взято.

**Далі в [README](../instances/sqlserver/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Редакції й версії; Межі, про які треба пам'ятати; Вектори на відеокарті; Родина .NET: піднімати разом;
Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### mongodb

**Коли піднімати.** Працюєте із сервером MongoDB, mongosh або його інструментами.

**Порт** 8850, сервер `mongodb-docs`. Підняти: `./df mongodb serve`. Адреса: `http://127.0.0.1:8850/mcp`.

**Обсяг.** Документів: 32 653, фрагментів: 90 554.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `mongoose-docs` (8852),
`node-mongodb-docs` (8851).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про сервер MongoDB: CRUD і агрегація, індекси, транзакції, реплікація,
шардинг, безпека, конфігурація `mongod`/`mongos`, журнал змін кожної версії, mongosh і Database Tools (mongodump,
mongorestore, mongoimport…). Документація — офіційний Database Manual кожної лінії від 2.2 до 9.0 у тому вигляді, яким
він був для тієї лінії: усі мажорні й мінорні, разом із rapid-випусками 5.1–5.3, 6.1–6.3, 7.1–7.3 і 8.3; вкладки
прикладів усіх мов (mongosh, Compass, Python, Java, Node.js, C#, Go, Rust, PHP, Ruby, Scala, Kotlin, Swift, C, C++)
збережено. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the MongoDB documentation -- the Database Manual of every version from 2.2 to 9.0 (every major, minor and
rapid release line as its documentation stood when that line was current), the mongosh documentation (2.1 and 2.13)
and the Database Tools documentation (100.19). Drivers (Node.js, Python and the others), Mongoose, Atlas, Compass and
Ops/Cloud Manager are not here; if something about the server, mongosh or the tools is not found in these documents,
it is unlikely to be in the official documentation. This set is part of the Mongo family: mongodb-docs (the server,
mongosh, Database Tools), node-mongodb-docs (the official Node.js driver and bson) and mongoose-docs (Mongoose and its
ecosystem) are meant to be connected together -- when a question belongs to another member, name its server.

**Межі.**

- Лише документація сервера, mongosh і Database Tools. Драйвери, Mongoose, Atlas, Compass, Ops/Cloud Manager,
  Kubernetes Operator, BI Connector — ні (для драйвера Node.js і Mongoose є примірники родини).
- 36 сторінок порожні у самому джерелі (заготовки інсталяційних сторінок у гілках 5.2 і 5.3, закоментована сторінка
  перевірки пакетів, згенерований `meta/includes` у 2.2) — читач їх відкидає, це не збій.
- Залишки розмітки: ~1 % документів тримають сирі спани ``x`` у літеральних блоках (так у джерелі) та в довгих
  перенесених спанах; ~0,2 % — підстановки `|newversion|` у назвах чужих сторінок, визначених лише там. Кілька
  десятків ролей `:ref:`/`:term:` лишилися всередині таблиць і через описки джерела.
- Rapid-випуски (5.1–5.3, 6.1–6.3, 7.1–7.3, 8.3) — документація є, хоч самі лінії давно не підтримуються.

**Далі в [README](../instances/mongodb/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Mongo: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### node-mongodb

**Коли піднімати.** Звертаєтеся до MongoDB із Node.js через офіційний драйвер.

**Порт** 8851, сервер `node-mongodb-docs`. Підняти: `./df node-mongodb serve`. Адреса: `http://127.0.0.1:8851/mcp`.

**Обсяг.** Документів: 12 030, фрагментів: 31 286.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `mongodb-docs` (8850),
`mongoose-docs` (8852).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про офіційний драйвер MongoDB для Node.js (пакет `mongodb`) і
бібліотеку `bson`: підключення й пул, CRUD, агрегація, транзакції, change streams, GridFS, індекси, типізація у
TypeScript, шифрування полів, перехід між мажорними версіями. Документація — кожної мінорної лінії драйвера від 3.6 до
7.7 у тому вигляді, якою вона була для тієї лінії; код `src/` із TSDoc і `lib/` із JSDoc, тести integration і unit,
журнал `HISTORY.md` і нотатки релізів кожного стабільного випуску; реєстр npm і README семи пакетів. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the MongoDB Node.js driver documentation -- the driver documentation of every minor version from 3.6 to
7.7 (guides, fundamentals, usage examples, API notes as they stood for that line), the source code with its
TSDoc/JSDoc comments and the integration and unit tests of every stable release, HISTORY.md and the GitHub release
notes, the npm registry and README of every version of mongodb, bson, mongodb-legacy, mongodb-client-encryption,
@mongodb-js/zstd, kerberos and @types/mongodb. The server itself, mongosh and Mongoose are not here; if something
about the driver is not found in these documents, it is unlikely to be in its official documentation. This set is part
of the Mongo family: mongodb-docs (the server, mongosh, Database Tools), node-mongodb-docs (this one: the official
Node.js driver and bson) and mongoose-docs (Mongoose and its ecosystem) are meant to be connected together -- when a
question belongs to another member, name its server.

**Межі.**

- Лише стабільні випуски: alpha, beta, rc не взято ні в код, ні в релізи, ні в npm.
- Сервер, mongosh, Database Tools — у примірнику `mongodb`; Mongoose — у `mongoose`.
- `@mongodb-js/zstd`, `@nestjs/*` і DefinitelyTyped не кладуть README у tarball: для zstd є лише реєстр версій, для
  `@types/mongodb` — самі типи.
- Версія за замовчуванням: за завантаженнями npm 6.x (44 %) і 7.x (34 %) — коли версію не названо, відповідь для обох.

**Далі в [README](../instances/node-mongodb/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Межі, про які треба пам'ятати; Родина Mongo: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### mongoose

**Коли піднімати.** Описуєте моделі MongoDB через Mongoose.

**Порт** 8852, сервер `mongoose-docs`. Підняти: `./df mongoose serve`. Адреса: `http://127.0.0.1:8852/mcp`.

**Обсяг.** Документів: 18 058, фрагментів: 48 158.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `mongodb-docs` (8850),
`node-mongodb-docs` (8851).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Mongoose — ODM для MongoDB у Node.js: схеми й типи, моделі й
документи, запити, валідація, middleware, populate, дискримінатори, транзакції, change streams, TypeScript, переходи
між мажорними версіями; а також про його екосистему: `@nestjs/mongoose`, Typegoose, mongodb-memory-server,
connect-mongo і плагіни mongoose-autopopulate, mongoose-lean-virtuals, mongoose-unique-validator,
mongoose-paginate-v2. Документація — `docs/*.md` кожного стабільного випуску від 5.13.0 до найновішого 9.x, знімки
сайту 3.8.x і 4.x, код `lib/` із JSDoc, типи `types/` і тести кожного випуску, `CHANGELOG.md` від 1.0.1, нотатки
релізів, реєстр npm і README; у додатків — документація, код, релізи й npm кожного випуску. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Mongoose documentation -- the docs/ pages of every stable release from 5.13 to the newest (guides,
schema types, models, documents, queries, validation, middleware, populate, discriminators, transactions, change
streams, TypeScript, the migration guides to 5, 6, 7, 8 and 9), the site snapshots of Mongoose 3.8 and 4, the source
code lib/ with JSDoc, the TypeScript types and the tests of every stable release, CHANGELOG.md since 1.0.1 and the
GitHub release notes, the npm registry and README of every version; plus @nestjs/mongoose, Typegoose,
mongodb-memory-server, connect-mongo and the plugins mongoose-autopopulate, mongoose-lean-virtuals,
mongoose-unique-validator and mongoose-paginate-v2 (their docs, code, releases and npm). The MongoDB server, mongosh
and the raw Node.js driver are not here; if something about Mongoose is not found in these documents, it is unlikely
to be in its official documentation. This set is part of the Mongo family: mongodb-docs (the server, mongosh, Database
Tools), node-mongodb-docs (the official Node.js driver and bson) and mongoose-docs (this one) are meant to be
connected together -- when a question belongs to another member, name its server.

**Межі.**

- Лише стабільні випуски: rc, alpha, beta не взято ні в код, ні в релізи, ні в npm.
- Сервер MongoDB, mongosh, Database Tools — у примірнику `mongodb`; драйвер — у `node-mongodb`.
- Без README у tarball — `@nestjs/mongoose`, `@typegoose/typegoose` і DefinitelyTyped: для них є документація й код з
  репозиторіїв, для `@types/mongoose` — самі типи. GitHub Releases немає в mongoose-autopopulate і
  mongoose-lean-virtuals — у них журнал змін у `History.md`.
- `mongoose-autopopulate` має лише два теги (1.2.0, 1.2.1): старіші випуски без тегів — у npm (реєстр версій і
  README).

**Далі в [README](../instances/mongoose/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Mongo: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### redis

**Коли піднімати.** Працюєте із сервером Redis: команди, збереження, реплікація, Sentinel, Cluster.

**Порт** 8845, сервер `redis-docs`. Підняти: `./df redis serve`. Адреса: `http://127.0.0.1:8845/mcp`.

**Обсяг.** Документів: 19 678, фрагментів: 97 242.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `bullmq-docs` (8848), `ioredis-docs`
(8846), `node-redis-docs` (8847), `upstash-docs` (8849).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Redis — сервер структур даних у пам'яті: команди й типи даних,
`redis.conf` і `sentinel.conf`, збереження на диск (RDB, AOF), реплікація, Sentinel, Cluster, ACL, транзакції, Lua і
Functions, потоки, витіснення, клієнтське кешування, протокол RESP. Документація — офіційна, кожної мінорної лінії від
1.3 до 8.10 у тому вигляді, якою вона була на день виходу наступної лінії: сайт redis.io, конфігураційні файли й
нотатки усіх 269 стабільних випусків, код `src/` і тести першого та останнього випуску кожної лінії. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Redis documentation -- the official documentation of every minor line, redis.conf and sentinel.conf,
the source and tests of the first and last release of each minor line, the release notes of every stable release.
Client libraries (ioredis, node-redis), BullMQ and managed services are not here; if something about Redis is not
found in these documents, it is unlikely to be in its official documentation. This set is part of the Redis family:
redis-docs (the Redis server), ioredis-docs and node-redis-docs (the Node.js clients), bullmq-docs (BullMQ, Bull, Bull
Board, Arena) and upstash-docs (the Upstash platform: Redis over HTTP, ratelimit, QStash, Workflow, Vector) are meant
to be connected together -- when a question belongs to another member, name its server.

**Межі.**

- Лише стабільні випуски: rc, alpha, beta, milestone-теги і Releases не взято.
- Клієнтських бібліотек тут немає: сторінки `develop-clients-*` сайту — це лише вступ до кожного клієнта. ioredis,
  node-redis і BullMQ — окремі примірники.
- Для лінії 1.3 знімка сайту немає (репозиторій `redis-doc` молодший за вихід 2.0); від 1.3 є лише `redis.conf` і
  README тега 1.3.6.
- Сторінки Enterprise і Cloud присутні, але відповіді за замовчуванням — для open source; про це сказано в промптах.

**Далі в [README](../instances/redis/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Redis: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### ioredis

**Коли піднімати.** Звертаєтеся до Redis із Node.js через ioredis.

**Порт** 8846, сервер `ioredis-docs`. Підняти: `./df ioredis serve`. Адреса: `http://127.0.0.1:8846/mcp`.

**Обсяг.** Документів: 2 309, фрагментів: 7 764.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `bullmq-docs` (8848),
`node-redis-docs` (8847), `redis-docs` (8845), `upstash-docs` (8849).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про ioredis — повнофункціональний клієнт Redis для Node.js: підключення
standalone, Sentinel і Cluster, опції й події, конвеєри й автоконвеєр, транзакції, pub/sub і sharded pub/sub, потоки,
`scanStream`, скрипти Lua через `defineCommand`, TLS, черга офлайн і перепідключення, вбудовані типи TypeScript.
Документація — кожного стабільного випуску від 1.0.0 до 6.0.0: README (посібник), довідник `API.md` (2–4), журнал
змін, приклади, код `lib/` з коментарями JSDoc (для 5.x і 6.x це і є довідник — з нього генерується сайт TypeDoc),
тести останнього випуску кожної мінорної лінії, нотатки релізів GitHub, `@ioredis/commands` і типи спільноти
`@types/ioredis`. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі
дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the ioredis documentation -- README, API reference, changelog, examples, source code with JSDoc and
GitHub release notes of every stable release, the tests of the last release of each minor line, @ioredis/commands and
@types/ioredis. The Redis server itself (commands, redis.conf), node-redis and BullMQ are separate instances; if
something about ioredis is not found in these documents, it is unlikely to be in its official documentation. This set
is part of the Redis family: redis-docs (the Redis server), ioredis-docs and node-redis-docs (the Node.js clients),
bullmq-docs (BullMQ, Bull, Bull Board, Arena) and upstash-docs (the Upstash platform: Redis over HTTP, ratelimit,
QStash, Workflow, Vector) are meant to be connected together -- when a question belongs to another member, name its
server.

**Межі.**

- Лише стабільні випуски: бети, rc, alpha (6.1.0-beta, 5.0.0-beta, 4.0.0-0…3, 2.0.0-rc) не взято.
- Сайт TypeDoc (`docs/`, redis.github.io/ioredis) не завантажено: він генерується з `lib/`, який тут є.
- Документація самого Redis (команди, `redis.conf`, Sentinel і Cluster зсередини) — примірник `redis`; сторінки
  ioredis на redis.io (`develop-clients-ioredis-*`) теж там.
- `@types/ioredis` 5.0.0 — заглушка без типів, у корпус не потрапила; для ioredis 5+ типи вбудовані.

**Далі в [README](../instances/ioredis/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Redis: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### node-redis

**Коли піднімати.** Звертаєтеся до Redis із Node.js через офіційний клієнт node-redis.

**Порт** 8847, сервер `node-redis-docs`. Підняти: `./df node-redis serve`. Адреса: `http://127.0.0.1:8847/mcp`.

**Обсяг.** Документів: 6 089, фрагментів: 17 699.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `bullmq-docs` (8848), `ioredis-docs`
(8846), `redis-docs` (8845), `upstash-docs` (8849).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про node-redis — офіційний клієнт Redis для Node.js (пакет `redis` з
`@redis/client`, `@redis/json`, `@redis/search`, `@redis/time-series`, `@redis/bloom`, `@redis/entraid`):
`createClient` і його опції, методи команд з типами аргументів і відповідей, транзакції multi/exec і WATCH, конвеєри,
pub/sub, ітератори SCAN, кластер і Sentinel, пул підключень, RESP2 і RESP3, кешування на боці клієнта, скрипти й
функції, автентифікація Entra ID, метрики OpenTelemetry. Документація — кожного стабільного випуску від 0.3.5 до
6.3.0: README (у 0.x–3.x — увесь довідник API), посібники `docs/`, журнал змін, приклади й doctests, код клієнта й
модулів (для 4.x–6.x це і є довідник), тести останнього випуску кожної мінорної лінії, нотатки релізів GitHub, README
пакетів з npm і типи спільноти `@types/redis`. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the node-redis documentation -- README, guides, changelog, examples, source code of the client and its
modules, GitHub release notes and npm README of every stable release, the tests of the last release of each minor
line, and @types/redis. The Redis server itself (commands, redis.conf), ioredis and BullMQ are separate instances; if
something about node-redis is not found in these documents, it is unlikely to be in its official documentation. This
set is part of the Redis family: redis-docs (the Redis server), ioredis-docs and node-redis-docs (the Node.js
clients), bullmq-docs (BullMQ, Bull, Bull Board, Arena) and upstash-docs (the Upstash platform: Redis over HTTP,
ratelimit, QStash, Workflow, Vector) are meant to be connected together -- when a question belongs to another member,
name its server.

**Межі.**

- Лише стабільні випуски: next, rc, beta і нумеровані пре-релізи (`v.2.6.0-0`, `2.5.0-1`) не взято.
- Документація самого Redis (команди, `redis.conf`, Sentinel і Cluster зсередини) — примірник `redis`; сторінки
  node-redis на redis.io (`develop-clients-nodejs-*`) теж там.
- `@types/redis` 4.0.x — заглушка без типів, у корпус не потрапила; для redis 4+ типи вбудовані.
- Сайт redis.io і сайти модулів (RedisJSON, RediSearch) — поза межами; тут лише те, що каже сам клієнт.

**Далі в [README](../instances/node-redis/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Redis: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### bullmq

**Коли піднімати.** Робите черги завдань через BullMQ або Bull, зокрема в NestJS.

**Порт** 8848, сервер `bullmq-docs`. Підняти: `./df bullmq serve`. Адреса: `http://127.0.0.1:8848/mcp`.

**Обсяг.** Документів: 13 882, фрагментів: 35 922.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `ioredis-docs` (8846),
`node-redis-docs` (8847), `redis-docs` (8845), `upstash-docs` (8849).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про BullMQ — черги задач поверх Redis для Node.js: `Queue.add` і опції
задачі (`delay`, `attempts`, `backoff`, `priority`, `jobId`, `removeOnComplete`), `Worker` і його обробник
(`concurrency`, `lockDuration`, застряглі задачі, `limiter`, sandboxed-процесори), повторювані задачі та планувальники
(`JobScheduler`), потоки батьківських і дочірніх задач (`FlowProducer`), події (`QueueEvents`), дедуплікація,
телеметрія, Lua-скрипти, що рухають задачу між станами, бекенд Postgres у 6.x, BullMQ Pro (групи, пакети,
observables). Поруч — попередник Bull з довідником і типами, панелі Bull Board (з кодом React-інтерфейсу) та Arena,
модулі `@nestjs/bull` і `@nestjs/bullmq`, порти BullMQ на Python, Elixir, Rust, PHP і .NET. Документація — кожного
стабільного випуску: сайт docs.bullmq.io, README, журнали змін, код, тести останнього випуску кожної мінорної лінії,
нотатки релізів GitHub. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the BullMQ documentation -- docs.bullmq.io (guide, patterns, BullMQ Pro, ports Python, Elixir, Rust, PHP,
.NET), README, changelogs, source code with the Lua scripts, tests and GitHub release notes of every stable BullMQ
release, plus Bull (README, REFERENCE, PATTERNS, MIGRATION, code, tests, @types/bull), Bull Board (site, packages,
code, examples), Arena and the NestJS modules @nestjs/bull and @nestjs/bullmq. The Redis server, ioredis and
node-redis are separate instances; if something about BullMQ is not found in these documents, it is unlikely to be in
its official documentation. This set is part of the Redis family: redis-docs (the Redis server), ioredis-docs and
node-redis-docs (the Node.js clients), bullmq-docs (BullMQ, Bull, Bull Board, Arena) and upstash-docs (the Upstash
platform: Redis over HTTP, ratelimit, QStash, Workflow, Vector) are meant to be connected together -- when a question
belongs to another member, name its server.

**Межі.**

- Лише стабільні випуски: alpha, beta, rc і next не взято.
- Сервер Redis (команди, `redis.conf`, Sentinel і Cluster зсередини) — примірник `redis`; клієнти — `ioredis` і
  `node-redis`; глава Queues документації NestJS — примірник `nestjs`.
- Інші черги (Bee-Queue, Agenda, RabbitMQ, Kafka, SQS) і панель Taskforce.sh — поза межами.
- `@types/bull` 4.10.x — заглушки без типів, у корпус не потрапили; для Bull 4.x типи вбудовані.

**Далі в [README](../instances/bullmq/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Redis: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### upstash

**Коли піднімати.** Використовуєте керовані сервіси Upstash: Redis, QStash, Vector.

**Порт** 8849, сервер `upstash-docs`. Підняти: `./df upstash serve`. Адреса: `http://127.0.0.1:8849/mcp`.

**Обсяг.** Документів: 14 432, фрагментів: 53 287.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `bullmq-docs` (8848), `ioredis-docs`
(8846), `node-redis-docs` (8847), `redis-docs` (8845).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про платформу Upstash — безсерверні дані з оплатою за запит. Ядро —
Upstash Redis: база, сумісна з командами Redis, доступна і по TCP, і через HTTP REST API для serverless і edge
(Vercel, Cloudflare Workers, Lambda); до неї — клієнти `@upstash/redis` (TypeScript) і `upstash-redis` (Python),
обмежувач частоти `@upstash/ratelimit` (`slidingWindow`, `fixedWindow`, `tokenBucket`), `@upstash/lock`, `queue`,
`query`, `realtime`, `semantic-cache`. Решта продуктів: QStash (черга повідомлень і планувальник по HTTP:
`publishJSON`, розклади, URL-групи, черги, DLQ, підписи), Workflow (довготривалі функції: `serve`, `context.run`,
`sleep`, `call`, `waitForEvent`, `invoke`, агенти), Vector (векторна база: `upsert`, `query`, namespaces, фільтри),
Search, Realtime, Blob, Box (пісочниці для AI-агентів), закритий Kafka, Context7 (документація для агентів:
MCP-сервер, SDK, CLI `ctx7`), Upstash CLI, MCP-сервери, провайдери Terraform і Pulumi, Developer API. Документація —
сайт upstash.com/docs, блог, і для кожного стабільного випуску кожного SDK та інструменту — README, журнали змін, код,
тести й нотатки релізів; таблиці версій і README пакетів npm, проєкти PyPI, приклади, skills. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Upstash documentation -- the site upstash.com/docs (Redis with the command reference and the
TypeScript and Python SDK pages, QStash, Workflow, Vector, Search, Realtime, Blob, Box, DevOps, Developer API, the
Kafka section as it stood before its removal), the blog and glossary, and for every stable release of every official
SDK and tool (redis-js, ratelimit-js, qstash-js, vector-js, workflow-js, search-js, realtime, lock, queue, query,
semantic-cache, blob, box, agentkit, cli, mcp-server, kafka-js, context7, the Python, Go and PHP SDKs, the Terraform
and Pulumi providers) the README, changelogs, source code, tests and GitHub release notes, plus the version tables and
READMEs of the @upstash packages on npm and the Upstash projects on PyPI, examples and agent skills. The Redis server
itself, ioredis, node-redis and BullMQ are separate instances; if something about Upstash is not found in these
documents, it is unlikely to be in its official documentation. This set is part of the Redis family: redis-docs (the
Redis server), ioredis-docs and node-redis-docs (the Node.js clients), bullmq-docs (BullMQ, Bull, Bull Board, Arena)
and upstash-docs (the Upstash platform) are meant to be connected together -- when a question belongs to another
member, name its server.

**Межі.**

- Лише стабільні випуски SDK: alpha, beta, rc, canary і next не взято (у таблицях версій npm вони є).
- Сервер Redis (команди зсередини, `redis.conf`, збереження, Sentinel, Cluster) — примірник `redis`; клієнти — `ioredis` і
  `node-redis`; черги — `bullmq`.
- Керовані Redis інших хмар (ElastiCache, Azure Cache, Redis Cloud), Vercel KV як продукт Vercel — поза межами.
- Демо-застосунки Upstash (wikipedia-semantic-search, degree-guru, botstreet, hacker-trends тощо), jstack, форки й
  сторонні пакети npm зі словом «upstash» — не взято.
- У `@upstash/chatbox`, `edge-flags`, `feedback`, `react-ui` README в tarball немає (28-байтова заглушка); релізів
  Python SDK Box, панелі edge-flags і плагіна Strapi на GitHub немає.

**Далі в [README](../instances/upstash/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина Redis: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

<!-- тема: Черги повідомлень -->

### kafka

**Коли піднімати.** Працюєте із сервером Apache Kafka: налаштування, теми, групи споживачів.

**Порт** 8886, сервер `kafka-docs`. Підняти: `./df kafka serve`. Адреса: `http://127.0.0.1:8886/mcp`.

**Обсяг.** Документів: 1 911, фрагментів: 10 816.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `confluent-kafka-javascript-docs`
(8888), `kafkajs-docs` (8887), `platformatic-kafka-docs` (8889).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Apache Kafka — розподілену платформу потоків подій (сайт
kafka.apache.org, репозиторії apache/kafka-site і apache/kafka) — за документацією всіх мінорних версій: сайт кожної
версії від 0.7 до 4.4 з повними таблицями параметрів і схемами протоколу, оголошення релізів, сторінки завантажень і
вразливостей, README репозиторію на кожній мінорній. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Apache Kafka documentation -- the distributed event streaming platform (site kafka.apache.org,
repositories apache/kafka-site and apache/kafka): the documentation of every minor version from 0.7 to 4.4 (getting
started, upgrade notes, APIs, configuration with the full generated tables of broker, topic, producer, consumer,
admin, Connect, Streams and MirrorMaker parameters, design, the wire protocol with every request schema and error
code, implementation, operations with KRaft, MirrorMaker 2, monitoring and tiered storage, security with SSL, SASL and
ACLs, Kafka Connect, Kafka Streams); the release announcements of 3.5.0 to 4.3.1; the download page with the date of
every release, the CVE list and the security policy; and the README of the repository at the last patch of every minor
from 0.8.0 to 4.4.0. The documentation of Kafka clients outside Apache Kafka (KafkaJS, librdkafka, Spring for Apache
Kafka), of Confluent products, ZooKeeper and Java is not here; if something about Apache Kafka is not found in these
documents, it is unlikely to be anywhere in its official documentation. This set is part of the Kafka family:
kafka-docs (this one: Apache Kafka itself: brokers, KRaft, configuration, protocol, Connect, Streams), kafkajs-docs
(the KafkaJS client for Node.js), confluent-kafka-javascript-docs (the Confluent client @confluentinc/kafka-javascript
on librdkafka) and platformatic-kafka-docs (the @platformatic/kafka client) are meant to be connected together -- when
a question belongs to another member, name its server.

**Далі в [README](../instances/kafka/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Родина Kafka: піднімати разом; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### kafkajs

**Коли піднімати.** Звертаєтеся до Kafka з Node.js через KafkaJS.

**Порт** 8887, сервер `kafkajs-docs`. Підняти: `./df kafkajs serve`. Адреса: `http://127.0.0.1:8887/mcp`.

**Обсяг.** Документів: 196, фрагментів: 709.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `confluent-kafka-javascript-docs`
(8888), `kafka-docs` (8886), `platformatic-kafka-docs` (8889).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про KafkaJS — клієнт Apache Kafka для Node.js на чистому JavaScript
(репозиторій tulios/kafkajs, сайт kafka.js.org, пакет kafkajs на npm) — за документацією всіх стабільних версій:
сторінки сайту з тегу кожної мінорної версії, README кожної версії, журнал змін та історія версій у реєстрі npm. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the KafkaJS documentation -- the Apache Kafka client for Node.js in pure JavaScript (repository
tulios/kafkajs, site kafka.js.org): the pages of the site taken from the tag of every minor version from 0.1 to 2.2
(configuration, SSL and SASL, retries, producer, consumer, transactions, admin client, instrumentation events, custom
logger and authentication, testing, FAQ, the migration guide to 2.0.0); the README of every stable version of the
package; the changelog of every version up to 2.2.4; and the npm registry history of kafkajs, including the Node.js
requirement (engines) and the date of every release. The documentation of Apache Kafka itself, librdkafka, other Kafka
clients, NestJS and Node.js is not here; if something about KafkaJS is not found in these documents, it is unlikely to
be anywhere in its official documentation. This set is part of the Kafka family: kafka-docs (Apache Kafka itself:
brokers, KRaft, configuration, protocol, Connect, Streams), kafkajs-docs (this one: the KafkaJS client for Node.js),
confluent-kafka-javascript-docs (the Confluent client @confluentinc/kafka-javascript on librdkafka) and
platformatic-kafka-docs (the @platformatic/kafka client) are meant to be connected together -- when a question belongs
to another member, name its server.

**Далі в [README](../instances/kafkajs/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Родина Kafka: піднімати разом; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### confluent-kafka-javascript

**Коли піднімати.** Звертаєтеся до Kafka з Node.js через клієнт Confluent.

**Порт** 8888, сервер `confluent-kafka-javascript-docs`. Підняти: `./df confluent-kafka-javascript serve`. Адреса: `http://127.0.0.1:8888/mcp`.

**Обсяг.** Документів: 78, фрагментів: 535.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `kafka-docs` (8886), `kafkajs-docs`
(8887), `platformatic-kafka-docs` (8889).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Confluent JavaScript Client for Apache Kafka — пакет
`@confluentinc/kafka-javascript`, клієнт Kafka для Node.js від Confluent на бібліотеці librdkafka (репозиторій
confluentinc/confluent-kafka-javascript, посібник на docs.confluent.io) — за документацією всіх стабільних версій. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the documentation of the Confluent JavaScript Client for Apache Kafka -- the package
@confluentinc/kafka-javascript on librdkafka, with a KafkaJS-compatible promisified API and a node-rdkafka-compatible
callback API (repository confluentinc/confluent-kafka-javascript): the client guide and the migration page of
docs.confluent.io for 1.0 to 1.11; INTRODUCTION.md, MIGRATION.md, QUICKSTART.md and the Schema Registry client README
from the tag of every minor version 0.2 to 1.11; the README of every stable version; the librdkafka configuration
properties bundled in every version; the changelog up to 1.11.0; and the npm registry history, including the Node.js
requirement and the date of every release. The documentation of Apache Kafka itself, KafkaJS, node-rdkafka, Confluent
Cloud and the librdkafka C API is not here; if something about this client is not found in these documents, it is
unlikely to be anywhere in its official documentation. This set is part of the Kafka family: kafka-docs (Apache Kafka
itself: brokers, KRaft, configuration, protocol, Connect, Streams), kafkajs-docs (the KafkaJS client for Node.js),
confluent-kafka-javascript-docs (this one: the Confluent client @confluentinc/kafka-javascript on librdkafka) and
platformatic-kafka-docs (the @platformatic/kafka client) are meant to be connected together -- when a question belongs
to another member, name its server.

**Далі в [README](../instances/confluent-kafka-javascript/README.md):** Навіщо окремий примірник; Скільки цього; Що в
цій теці; Звідки документація; Версії; Родина Kafka: піднімати разом; Архівний режим: сервер без корпусу; Установка
venv; Збирання корпусу; Сервер під Claude Code.

### platformatic-kafka

**Коли піднімати.** Звертаєтеся до Kafka з Node.js через `@platformatic/kafka`.

**Порт** 8889, сервер `platformatic-kafka-docs`. Підняти: `./df platformatic-kafka serve`. Адреса: `http://127.0.0.1:8889/mcp`.

**Обсяг.** Документів: 181, фрагментів: 597.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `confluent-kafka-javascript-docs`
(8888), `kafka-docs` (8886), `kafkajs-docs` (8887).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про @platformatic/kafka — сучасний клієнт Apache Kafka для Node.js на
чистому TypeScript від Platformatic (репозиторій platformatic/kafka, пакет `@platformatic/kafka` на npm) — за
документацією всіх стабільних версій. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the documentation of @platformatic/kafka -- a modern Apache Kafka client for Node.js in pure TypeScript
by Platformatic (repository platformatic/kafka): the `docs/` of the repository taken from the tag of every minor
version from 0.1 to 2.14 (base options, producer, consumer and message streams, admin client, transactions, metrics,
diagnostics, supported KIPs, Confluent Schema Registry, troubleshooting); the README of every stable version of the
package; the GitHub release notes of every stable version; and the npm registry history, including the Node.js
requirement and the date of every release. The documentation of Apache Kafka itself, KafkaJS, the Confluent client and
Node.js is not here; if something about @platformatic/kafka is not found in these documents, it is unlikely to be
anywhere in its official documentation. This set is part of the Kafka family: kafka-docs (Apache Kafka itself:
brokers, KRaft, configuration, protocol, Connect, Streams), kafkajs-docs (the KafkaJS client for Node.js),
confluent-kafka-javascript-docs (the Confluent client @confluentinc/kafka-javascript on librdkafka) and
platformatic-kafka-docs (this one: the @platformatic/kafka client) are meant to be connected together -- when a
question belongs to another member, name its server.

**Далі в [README](../instances/platformatic-kafka/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій
теці; Звідки документація; Версії; Родина Kafka: піднімати разом; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### rabbitmq

**Коли піднімати.** Працюєте із сервером RabbitMQ: обміни, черги, налаштування.

**Порт** 8890, сервер `rabbitmq-docs`. Підняти: `./df rabbitmq serve`. Адреса: `http://127.0.0.1:8890/mcp`.

**Обсяг.** Документів: 1 726, фрагментів: 12 640.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `amqp-connection-manager-docs`
(8892), `amqplib-docs` (8891), `golevelup-nestjs-rabbitmq-docs` (8893).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про RabbitMQ — брокер повідомлень з відкритим кодом для AMQP 0-9-1,
AMQP 1.0, MQTT, STOMP і потоків RabbitMQ Streams (сайт rabbitmq.com, репозиторії rabbitmq/rabbitmq-website і
rabbitmq/rabbitmq-server) — за документацією всіх версій, які зберіг сайт, і нотатками кожного релізу. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the RabbitMQ documentation -- the open source message broker for AMQP 0-9-1, AMQP 1.0, MQTT, STOMP and
Streams (site rabbitmq.com, repositories rabbitmq-website and rabbitmq-server): the documentation of the site for 3.13
to 4.4 and of the older site for 3.11 and 3.12 (queue types, exchanges, confirms and acknowledgements, dead lettering,
TTL, limits, policies, access control, TLS, OAuth 2.0, clustering, Khepri, feature flags, upgrades, rabbitmq.conf, the
CLI tools, monitoring, the management UI and HTTP API, plugins); the JavaScript tutorials; the client library pages;
the Kubernetes operators; the deprecated features list; the blog of 2010 to 2026; and the release notes of every
release from 1.1.1 to 4.4.0. The documentation of client libraries as their own projects (amqplib,
amqp-connection-manager, NestJS), of the AMQP specifications, Erlang and Kubernetes is not here; if something about
RabbitMQ is not found in these documents, it is unlikely to be anywhere in its official documentation. This set is
part of the RabbitMQ family: rabbitmq-docs (this one: RabbitMQ itself: queue types, exchanges, confirms, clustering,
rabbitmq.conf, release notes), amqplib-docs (the amqplib client for Node.js), amqp-connection-manager-docs
(reconnection on top of amqplib) and golevelup-nestjs-rabbitmq-docs (the @golevelup/nestjs-rabbitmq module for NestJS)
are meant to be connected together -- when a question belongs to another member, name its server.

**Далі в [README](../instances/rabbitmq/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Родина RabbitMQ: піднімати разом; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### amqplib

**Коли піднімати.** Звертаєтеся до RabbitMQ із Node.js через amqplib.

**Порт** 8891, сервер `amqplib-docs`. Підняти: `./df amqplib serve`. Адреса: `http://127.0.0.1:8891/mcp`.

**Обсяг.** Документів: 88, фрагментів: 398.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `amqp-connection-manager-docs`
(8892), `golevelup-nestjs-rabbitmq-docs` (8893), `rabbitmq-docs` (8890).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про amqplib — клієнт AMQP 0-9-1 для Node.js, яким працюють з RabbitMQ
(репозиторій amqp-node/amqplib, сайт amqp-node.github.io/amqplib, пакет amqplib на npm) — за документацією всіх
стабільних версій: сторінки сайту на час кожної мінорної версії, README кожної версії, журнал змін та історія версій у
реєстрі npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the amqplib documentation -- the AMQP 0-9-1 client for Node.js used with RabbitMQ (repository
amqp-node/amqplib, site amqp-node.github.io/amqplib): the pages of the site as they stood during every minor version
from 0.0 to 2.2 (the introduction, the Channel API reference for the promise and the callback API, SSL); the README of
every stable version of the package; the changelog up to 2.2.0; and the npm registry history of amqplib, including the
Node.js requirement and the date of every release. The documentation of RabbitMQ itself, amqp-connection-manager,
NestJS and Node.js is not here; if something about amqplib is not found in these documents, it is unlikely to be
anywhere in its official documentation. This set is part of the RabbitMQ family: rabbitmq-docs (RabbitMQ itself: queue
types, exchanges, confirms, clustering, rabbitmq.conf, release notes), amqplib-docs (this one: the amqplib client for
Node.js), amqp-connection-manager-docs (reconnection on top of amqplib) and golevelup-nestjs-rabbitmq-docs (the
@golevelup/nestjs-rabbitmq module for NestJS) are meant to be connected together -- when a question belongs to another
member, name its server.

**Далі в [README](../instances/amqplib/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Родина RabbitMQ: піднімати разом; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### amqp-connection-manager

**Коли піднімати.** Потрібне автоматичне перепідключення до RabbitMQ через amqp-connection-manager.

**Порт** 8892, сервер `amqp-connection-manager-docs`. Підняти: `./df amqp-connection-manager serve`. Адреса: `http://127.0.0.1:8892/mcp`.

**Обсяг.** Документів: 82, фрагментів: 195.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `amqplib-docs` (8891),
`golevelup-nestjs-rabbitmq-docs` (8893), `rabbitmq-docs` (8890).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про amqp-connection-manager — бібліотеку для Node.js, що обгортає
amqplib автоматичним перепідключенням до RabbitMQ (репозиторій jwalton/node-amqp-connection-manager, пакет
`amqp-connection-manager` на npm) — за README кожної стабільної версії, нотатками релізів та історією версій у реєстрі
npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the amqp-connection-manager documentation -- the Node.js library that wraps amqplib with automatic
reconnection to RabbitMQ (repository jwalton/node-amqp-connection-manager): the README of every stable version from
1.0 to 5.0, which is the whole documentation of the package (connect with failover, ChannelWrapper, setup functions,
publishing while disconnected, events); the GitHub release notes of every stable version; and the npm registry
history, including the Node.js requirement and the date of every release. The documentation of amqplib, RabbitMQ and
NestJS is not here; if something about amqp-connection-manager is not found in these documents, it is unlikely to be
anywhere in its official documentation. This set is part of the RabbitMQ family: rabbitmq-docs (RabbitMQ itself: queue
types, exchanges, confirms, clustering, rabbitmq.conf, release notes), amqplib-docs (the amqplib client for Node.js),
amqp-connection-manager-docs (this one: reconnection on top of amqplib) and golevelup-nestjs-rabbitmq-docs (the
@golevelup/nestjs-rabbitmq module for NestJS) are meant to be connected together -- when a question belongs to another
member, name its server.

**Далі в [README](../instances/amqp-connection-manager/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій
теці; Звідки документація; Версії; Родина RabbitMQ: піднімати разом; Архівний режим: сервер без корпусу; Установка
venv; Збирання корпусу; Сервер під Claude Code.

### golevelup-nestjs-rabbitmq

**Коли піднімати.** Підключаєте RabbitMQ до NestJS через модуль Golevelup.

**Порт** 8893, сервер `golevelup-nestjs-rabbitmq-docs`. Підняти: `./df golevelup-nestjs-rabbitmq serve`. Адреса: `http://127.0.0.1:8893/mcp`.

**Обсяг.** Документів: 116, фрагментів: 311.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `amqp-connection-manager-docs`
(8892), `amqplib-docs` (8891), `rabbitmq-docs` (8890).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про @golevelup/nestjs-rabbitmq — модуль NestJS для RabbitMQ від
Golevelup на amqplib і amqp-connection-manager (репозиторій golevelup/nestjs, пакет `@golevelup/nestjs-rabbitmq` на
npm) — за сторінкою модуля на сайті, README кожної стабільної версії, журналом змін та історією версій у реєстрі npm.
Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the @golevelup/nestjs-rabbitmq documentation -- the NestJS module for RabbitMQ by Golevelup on amqplib
and amqp-connection-manager (repository golevelup/nestjs): the page of the module on golevelup.github.io/nestjs (as of
9.1.1); the README of every stable version from 1.6 to 9.1 (module registration, exchanges and queues, RabbitSubscribe
and RabbitRPC handlers, AmqpConnection, error handling, multiple connections, testing); the changelog of every
version; and the npm registry history, including the peer dependencies on NestJS and the date of every release. The
documentation of NestJS, its RMQ transport, amqplib, amqp-connection-manager and RabbitMQ is not here; if something
about the module is not found in these documents, it is unlikely to be anywhere in its official documentation. This
set is part of the RabbitMQ family: rabbitmq-docs (RabbitMQ itself: queue types, exchanges, confirms, clustering,
rabbitmq.conf, release notes), amqplib-docs (the amqplib client for Node.js), amqp-connection-manager-docs
(reconnection on top of amqplib) and golevelup-nestjs-rabbitmq-docs (this one: the @golevelup/nestjs-rabbitmq module
for NestJS) are meant to be connected together -- when a question belongs to another member, name its server.

**Далі в [README](../instances/golevelup-nestjs-rabbitmq/README.md):** Навіщо окремий примірник; Скільки цього; Що в
цій теці; Звідки документація; Версії; Родина RabbitMQ: піднімати разом; Архівний режим: сервер без корпусу; Установка
venv; Збирання корпусу; Сервер під Claude Code.

### nats

**Коли піднімати.** Працюєте із сервером NATS або JetStream.

**Порт** 8894, сервер `nats-docs`. Підняти: `./df nats serve`. Адреса: `http://127.0.0.1:8894/mcp`.

**Обсяг.** Документів: 3 449, фрагментів: 7 433.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `nats-js-docs` (8895).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про NATS — систему обміну повідомленнями з відкритим кодом nats-server
з core NATS (публікація й підписка, request/reply, черги-групи) і JetStream (потоки, консумери, Key-Value, Object
Store) — за документацією сайту docs.nats.io всіх версій, які він тримає, старою документацією GitBook, архітектурними
рішеннями команди й нотатками кожного стабільного релізу сервера. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the NATS documentation -- the open source messaging system nats-server with core NATS and JetStream (site
docs.nats.io, repositories nats.docs.v2, nats.docs, nats-architecture-and-design and nats-server): the reference of
the server 2.11, 2.12, 2.14 and 2.15 (every configuration key, JetStream streams and consumers, system subjects,
monitoring, protocols, services); the Learn section, the concepts, the upgrade notes and the tutorials; the old
GitBook documentation of docs.nats.io; the architecture decision records; and the release notes of every stable
nats-server release from 0.5.6 to 2.15.1. The documentation of the client libraries as their own projects (nats.js and
the packages nats and @nats-io/*, nats.go, the NestJS NATS transport), of Kubernetes and Go is not here; if something
about NATS is not found in these documents, it is unlikely to be anywhere in its official documentation. This set is
part of the NATS family: nats-docs (this one: the NATS server itself: core NATS, JetStream, Key-Value and Object
Store, clustering, security, the configuration file, release notes) and nats-js-docs (the nats.js client for Node.js:
the package nats 2.x and the packages @nats-io/* 3.x) are meant to be connected together -- when a question belongs to
the other member, name its server.

**Далі в [README](../instances/nats/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Родина NATS: піднімати разом; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### nats-js

**Коли піднімати.** Звертаєтеся до NATS із JavaScript через `nats` або `@nats-io/*`.

**Порт** 8895, сервер `nats-js-docs`. Підняти: `./df nats-js serve`. Адреса: `http://127.0.0.1:8895/mcp`.

**Обсяг.** Документів: 585, фрагментів: 3 114.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `nats-docs` (8894).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про nats.js — офіційний клієнт NATS для JavaScript і TypeScript
(Node.js, Deno, Bun, браузери) в обох його лініях: пакет `nats` 2.x і модульні пакети `@nats-io/*` 3.x (репозиторії
nats-io/nats.js і nats-io/nats.deno, реєстр npm, довідник TypeDoc). Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the nats.js documentation -- the official NATS client for JavaScript and TypeScript, the package nats 2.x
and the packages @nats-io/* 3.x (repositories nats.js and nats.deno, the npm registry, the TypeDoc reference): the
README of every nats version 0.2 to 2.29; the README, jetstream.md and services.md of nats-base-client for 2.0 to
2.29; the README of every @nats-io/* package with migration.md for 3.0 to 3.4; the API reference of core, jetstream,
kv, obj and services 3.4; the examples of docs.nats.io; the npm registry; the release notes of nats.js 3.x and
nats.deno 1.x. The documentation of the NATS server itself and of the NestJS NATS transport is not here; if something
about nats.js is not found in these documents, it is unlikely to be anywhere in its official documentation. This set
is part of the NATS family: nats-docs (the NATS server itself: core NATS, JetStream, Key-Value and Object Store,
clustering, security, the configuration file, release notes) and nats-js-docs (this one: the nats.js client for
Node.js: the package nats 2.x and the packages @nats-io/* 3.x) are meant to be connected together -- when a question
belongs to the other member, name its server.

**Далі в [README](../instances/nats-js/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Родина NATS: піднімати разом; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

<!-- тема: Мова Go й її бібліотеки -->

### go

**Коли піднімати.** Пишете на Go: мова, стандартна бібліотека, інструменти, зміни між версіями.

**Порт** 8913, сервер `go-docs`. Підняти: `./df go serve`. Адреса: `http://127.0.0.1:8913/mcp`.

**Обсяг.** Документів: 3 901, фрагментів: 37 123.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про мову Go: специфікація, модель пам'яті, стандартна бібліотека й
команди інструментарію в кожній мінорній версії, сайт go.dev (документація, довідники, блог, «A Tour of Go»), доповіді
команди Go, вікі, проєктні документи пропозицій, gopls, а поруч — «Go by Example», «Learn Go with Tests», настанови зі
стилю Google і Uber, запитання до співбесіди й окремо виділена підготовка до сертифікації Ardan Labs. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Go documentation: the language specification, the memory model, the Go 1 compatibility promise, the
assembler guide and GODEBUG at the last patch of every minor release 1.0 to 1.27; the standard library from pkg.go.dev
in each of those releases and the commands of the toolchain 1.4 to 1.27; the site go.dev (Effective Go, the FAQ,
tutorials, the modules reference, database/sql, security, diagnostics, the GC guide, PGO, release notes 1.0 to 1.27),
the go.dev blog, A Tour of Go, the talks, the Go wiki, the proposal design documents and the gopls documentation; Go
by Example, Learn Go with Tests, the Google and Uber Go style guides and the Go Interview Guide; set apart as
certification preparation (ids `cert-`), the Ardan Labs "Ultimate Go" class material and "Ultimate Service".
Third-party Go libraries, golang.org/x packages and the book "Learning Go" are not here; if something about Go itself
is not found in these documents, it is unlikely to be in its official documentation.

**Далі в [README](../instances/go/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Підготовка до сертифікації; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### learning-go

**Коли піднімати.** Вчите Go за книжками: Learning Go, Go by Example, 100 Go Mistakes, Go 101.

**Порт** 8914, сервер `learning-go-book`. Підняти: `./df learning-go serve`. Адреса: `http://127.0.0.1:8914/mcp`.

**Обсяг.** Документів: 549, фрагментів: 3 656.

**Опис.**

Захищений MCP-сервер для читання книжки «Learning Go: An Idiomatic Approach to Real-World Go Programming», 2nd Edition
— Jon Bodner; O'Reilly Media, 2024 — разом з офіційним кодом книжки й двома вільними для читання книжками про Go: «100
Go Mistakes and How to Avoid Them» (Teiva Harsanyi; Manning, 2022) у викладі автора на 100go.co і «Go 101» (Tapir Liu,
go101.org), а також другий підручник — «Go by Example: Programmer's guide to idiomatic and testable code» (Inanc
Gumus; Manning Publications, 2025). Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

This is a book, not library documentation. co, and "Go 101" (Tapir Liu, go101.org). The Go specification, the standard
library reference and the release notes are on the Go documentation server, not here; if something about the book is
not found in these documents, it is not in the book.

**Далі в [README](../instances/learning-go/README.md):** Навіщо; Корпус лише локально; Скільки цього; Що в цій теці;
Звідки документація; Версії; Установка venv; Збирання корпусу; Сервер під Claude Code.

### sqlc

**Коли піднімати.** Генеруєте код Go із запитів SQL через sqlc.

**Порт** 8916, сервер `sqlc-docs`. Підняти: `./df sqlc serve`. Адреса: `http://127.0.0.1:8916/mcp`.

**Обсяг.** Документів: 367, фрагментів: 1 064.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про sqlc (sqlc-dev/sqlc) — генератор типізованого коду Go із запитів
SQL: ви пишете схему й запити, sqlc перевіряє їх і генерує функції та структури Go. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the sqlc documentation: the site docs.sqlc.dev (tutorials, how-to guides, the configuration, CLI, query
annotation, macro and data type reference, the guide on Go and pgx) at every minor release 0.1 to 1.31, the README,
the changelog and the example projects' schemas, queries and configuration. PostgreSQL, MySQL and SQLite themselves,
pgx, goose and other Go libraries are not here; if something about sqlc is not found in these documents, it is
unlikely to be in its documentation.

**Далі в [README](../instances/sqlc/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### pgx

**Коли піднімати.** Звертаєтеся до PostgreSQL із Go через pgx.

**Порт** 8915, сервер `pgx-docs`. Підняти: `./df pgx serve`. Адреса: `http://127.0.0.1:8915/mcp`.

**Обсяг.** Документів: 229, фрагментів: 2 658.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про pgx (github.com/jackc/pgx) — драйвер і набір інструментів
PostgreSQL для Go: з'єднання й пул `pgxpool`, запити й розбір рядків у структури, типи PostgreSQL у Go (`pgtype`),
транзакції, пакети запитів, `COPY`, `LISTEN/NOTIFY`, трасування й драйвер для `database/sql`. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the pgx documentation: the package reference from pkg.go.dev (pgx, pgxpool, pgconn, pgtype, pgproto3,
stdlib, tracelog, multitracer) for every minor release of v5 and v4, the README of pgx, pgconn and pgproto3 at every
minor release 2.0 to 5.11, the changelog of releases 4.0.0 to 5.11.0 and the code of the example programs. PostgreSQL
itself, database/sql in general, sqlc, goose and other Go libraries are not here; if something about pgx is not found
in these documents, it is unlikely to be in its documentation.

**Далі в [README](../instances/pgx/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### goose

**Коли піднімати.** Виконуєте міграції бази в Go через goose.

**Порт** 8917, сервер `goose-docs`. Підняти: `./df goose serve`. Адреса: `http://127.0.0.1:8917/mcp`.

**Обсяг.** Документів: 119, фрагментів: 551.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про goose (pressly/goose) — інструмент і бібліотеку міграцій бази для
Go: файли SQL з анотаціями `-- +goose Up` і `-- +goose Down`, міграції на Go, команди CLI, міграції, вбудовані в
бінарник, і API `Provider`. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека
тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the goose documentation: the site pressly.github.io/goose with its blog, the README and examples at every
minor release 2.0 to 3.29, the changelog of 3.x and the package reference from pkg.go.dev for every minor release 3.0
to 3.29. SQL, the database servers, golang-migrate, sqlc and pgx are not here; if something about goose is not found
in these documents, it is unlikely to be in its documentation.

**Далі в [README](../instances/goose/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### golang-migrate

**Коли піднімати.** Виконуєте міграції бази в Go через golang-migrate.

**Порт** 8918, сервер `golang-migrate-docs`. Підняти: `./df golang-migrate serve`. Адреса: `http://127.0.0.1:8918/mcp`.

**Обсяг.** Документів: 232, фрагментів: 604.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про golang-migrate (github.com/golang-migrate/migrate) — інструмент і
бібліотеку міграцій бази для Go: пари файлів `N_name.up.sql` і `N_name.down.sql`, команди CLI, адреси баз кожного
драйвера, таблиця версій і позначка `dirty` після невдалої міграції. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the golang-migrate documentation: the README, GETTING_STARTED, MIGRATIONS, FAQ, the CLI and every
database driver and migration source at every minor release 1.2 to 4.20, the release notes, and the package reference
from pkg.go.dev (migrate, database, source, postgres, pgx/v5, file, iofs) for every minor release 4.0 to 4.20. SQL,
the database servers, goose, sqlc and pgx are not here; if something about golang-migrate is not found in these
documents, it is unlikely to be in its documentation.

**Далі в [README](../instances/golang-migrate/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### oapi-codegen

**Коли піднімати.** Генеруєте код Go з OpenAPI через oapi-codegen.

**Порт** 8919, сервер `oapi-codegen-docs`. Підняти: `./df oapi-codegen serve`. Адреса: `http://127.0.0.1:8919/mcp`.

**Обсяг.** Документів: 473, фрагментів: 2 452.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про oapi-codegen (github.com/oapi-codegen/oapi-codegen) — генератор
коду Go з документів OpenAPI 3 — і про бібліотеки, на яких стоїть згенерований код: `github.com/oapi-codegen/runtime`,
middleware перевірки запитів `nethttp-middleware` і kin-openapi (github.com/getkin/kin-openapi), що завантажує й
перевіряє документ. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі
дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents : the oapi-codegen README, docs and example READMEs at every minor release 1.0 to 2.8, its release notes and
example code; github.com/oapi-codegen/runtime and nethttp-middleware on pkg.go.dev; the kin-openapi README at every
minor release and its pkg.go.dev reference (openapi3, openapi3filter, routers) for the latest releases. The OpenAPI
specification, JSON Schema, other generators and TypeScript clients are not here; if something about oapi-codegen or
kin-openapi is not found in these documents, it is unlikely to be in their documentation.

**Далі в [README](../instances/oapi-codegen/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### golang-x

**Коли піднімати.** Використовуєте пакети `golang.org/x`: argon2, bcrypt, errgroup, rate.

**Порт** 8920, сервер `golang-x-docs`. Підняти: `./df golang-x serve`. Адреса: `http://127.0.0.1:8920/mcp`.

**Обсяг.** Документів: 27, фрагментів: 120.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про три модулі golang.org/x — пакети проєкту Go поза стандартною
бібліотекою: `golang.org/x/crypto` (лише `argon2` і `bcrypt`), `golang.org/x/sync` (`errgroup`, `semaphore`,
`singleflight`, `syncmap`) і `golang.org/x/time` (`rate`). Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the golang.org/x documentation on pkg.go.dev: x/crypto argon2 and bcrypt (0.1 to 0.58), x/sync errgroup,
semaphore, singleflight and syncmap (0.1 to 0.24), x/time rate (0.1 to 0.16). The standard library and the other
golang.org/x packages are not here; if something about these packages is not found in these documents, it is unlikely
to be in their documentation.

**Далі в [README](../instances/golang-x/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### golang-jwt

**Коли піднімати.** Працюєте з JWT у Go через golang-jwt.

**Порт** 8921, сервер `golang-jwt-docs`. Підняти: `./df golang-jwt serve`. Адреса: `http://127.0.0.1:8921/mcp`.

**Обсяг.** Документів: 63, фрагментів: 510.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про golang-jwt (github.com/golang-jwt/jwt) — реалізацію JSON Web Token
для Go: створення й підпис токена, розбір і перевірка, методи підпису й типи ключів, опції перевірки
(`WithValidMethods`, `WithLeeway`, `WithExpirationRequired`), помилки й перехід з v4 на v5. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the golang-jwt documentation: the site golang-jwt.github.io/jwt, the README, migration guide, version
history and security policy at every minor release 3.0 to 5.3, the release notes, and the pkg.go.dev reference of v5
(5.0 to 5.3) and v4 (4.0 to 4.5). The JWT specifications, OAuth 2.0 and other JWT libraries are not here; if something
about golang-jwt is not found in these documents, it is unlikely to be in its documentation.

**Далі в [README](../instances/golang-jwt/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### coder-websocket

**Коли піднімати.** Робите WebSocket у Go через coder/websocket.

**Порт** 8922, сервер `coder-websocket-docs`. Підняти: `./df coder-websocket serve`. Адреса: `http://127.0.0.1:8922/mcp`.

**Обсяг.** Документів: 78, фрагментів: 280.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про coder/websocket (github.com/coder/websocket, раніше
nhooyr.io/websocket) — мінімальну бібліотеку WebSocket для Go поверх `net/http` і `context`: `Accept` у звичайному
обробнику, перевірка `Origin`, читання й запис з контекстом, JSON через `wsjson`, ping, коди закриття. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the coder/websocket documentation: the README and example READMEs at every minor release 0.1 to 1.8, the
pkg.go.dev reference (github.com/coder/websocket 1.8 and nhooyr.io/websocket 1.0 to 1.8), the example code and the
release notes. The WebSocket RFC, the browser API, gorilla/websocket and socket.io are not here; if something about
coder/websocket is not found in these documents, it is unlikely to be in its documentation.

**Далі в [README](../instances/coder-websocket/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### river

**Коли піднімати.** Робите черги завдань у Go через River.

**Порт** 8924, сервер `river-docs`. Підняти: `./df river serve`. Адреса: `http://127.0.0.1:8924/mcp`.

**Обсяг.** Документів: 201, фрагментів: 1 279.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про River (github.com/riverqueue/river) — чергу задач для Go на
PostgreSQL: задачі й обробники, вставка в тій самій транзакції, що й дані (`InsertTx`), повтори, унікальні,
заплановані й періодичні задачі, черги, чемна зупинка, міграції, тестування й River UI. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the River documentation: the site riverqueue.com/docs (including River Pro), the README and docs/ at
every minor release 0.0 to 0.50, the changelog and the pkg.go.dev reference of river, rivermigrate, rivertest and
riverlog for the latest releases. PostgreSQL, pgx, other job queues and River's clients in other languages are not
here; if something about River is not found in these documents, it is unlikely to be in its documentation.

**Далі в [README](../instances/river/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### testcontainers-go

**Коли піднімати.** Запускаєте контейнери в тестах Go через Testcontainers.

**Порт** 8923, сервер `testcontainers-go-docs`. Підняти: `./df testcontainers-go serve`. Адреса: `http://127.0.0.1:8923/mcp`.

**Обсяг.** Документів: 451, фрагментів: 1 914.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про testcontainers-go (github.com/testcontainers/testcontainers-go) —
бібліотеку Go, що запускає з тестів тимчасові контейнери Docker: PostgreSQL для інтеграційних тестів, очікування
готовності, рядок з'єднання, скрипти ініціалізації, знімки бази між тестами, прибирання контейнерів, CI. Код спільний
і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the testcontainers-go documentation: the site golang.testcontainers.org at every minor release 0.0 to
0.44 (quickstart, features, the postgres, redis and compose modules), the pkg.go.dev reference of the core package,
wait and network and of the postgres module, and the release notes. Docker, PostgreSQL, Go testing in general and
testcontainers for other languages are not here; if something about testcontainers-go is not found in these documents,
it is unlikely to be in its documentation.

**Далі в [README](../instances/testcontainers-go/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### golangci-lint

**Коли піднімати.** Налаштовуєте перевірку коду Go через golangci-lint.

**Порт** 8925, сервер `golangci-lint-docs`. Підняти: `./df golangci-lint serve`. Адреса: `http://127.0.0.1:8925/mcp`.

**Обсяг.** Документів: 156, фрагментів: 387.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про golangci-lint (golangci/golangci-lint) — швидкий запускач лінтерів
і форматерів Go: встановлення закріпленої версії локально й у CI, файл `.golangci.yml` версії 2, лінтери й форматери
та їхні налаштування, хибні спрацювання й `nolint`, винятки, лише нові проблеми для великих проєктів, плагіни, перехід
з v1. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену.
Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the golangci-lint documentation: the site golangci-lint.run at every minor release 2.0 to 2.15
(installation, configuration, linters and formatters, false positives, plugins, integrations, migration guide, FAQ),
the site's data (linters and formatters list, exclusion presets, CLI help, configuration description) and the
changelog of v2 and v1. The linters' own projects, go vet and gopls are not here; if something about golangci-lint is
not found in these documents, it is unlikely to be in its documentation.

**Далі в [README](../instances/golangci-lint/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

<!-- тема: .NET -->

### dotnet

**Коли піднімати.** Пишете на .NET: бібліотека класів, середовище, інструмент `dotnet`.

**Порт** 8866, сервер `dotnet-docs`. Підняти: `./df dotnet serve`. Адреса: `http://127.0.0.1:8866/mcp`.

**Обсяг.** Документів: 253 774, фрагментів: 503 464.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `aspnetcore-docs` (8862),
`csharp-docs` (8878), `dotnet-testing-docs` (8870), `entityframework-docs` (8865), `nuget-docs` (8869),
`sqlserver-docs` (8864), `testcontainers-dotnet-docs` (8867).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про .NET 1.0–10.0 (колишній .NET Core) — від нового в кожному випуску,
CLI `dotnet`, критичних змін, діагностики й вбудованих метрик, розгортання й контейнерів до основ (DI, конфігурація,
журналювання, хостинг, HttpClient, System.Text.Json), F#, Visual Basic, .NET Framework, довідника API базової
бібліотеки й Microsoft.Extensions.*, підтримки й CVE кожного випуску. Документація англійською, усі стабільні мажорні
й мінорні версії: сайт learn.microsoft.com/dotnet кожної версії (без теки `docs/csharp/`: мова C# — у примірнику
`csharp`); критичні зміни компіляторів Visual Basic і Razor; довідник API з dotnet/dotnet-api-docs і з
XML-документації пакетів NuGet; метадані й нотатки випусків dotnet/core; документація dotnet/runtime і dotnet/sdk. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md). **Документації мови C# тут немає.** Довідник і посібник мови
(learn.microsoft.com/dotnet/csharp), стандарт ECMA-334, специфікації можливостей і документація компілятора Roslyn — у
примірнику `csharp` (сервер `csharp-docs`, порт 8878); до 22.10.2026 вони були тут, а відтоді знімки сайту виключають
теку `docs/csharp/` правилом `exclude`, і ці тексти видалено з корпусу разом із джерелами. Так сказано й в описі
інструмента пошуку, який бачить модель. Тут C# є лише як мова прикладів довідника API.

**Склад (так його описано моделі, англійською).**

Documents of the .NET documentation -- the pages of learn.microsoft.com/dotnet for every .NET version 1.0-10.0 (as the
site shows them now and as the repository held them after each release; the C# pages of the site are on the server
csharp-docs); the breaking changes of the Visual Basic and Razor compilers and the Visual Basic specification; the API
reference of learn.microsoft.com/dotnet/api with C# examples and the XML documentation of Microsoft.NETCore.App
2.0-10.0 and of every Microsoft.Extensions.* package line; the release metadata and release notes of .NET 1.0-10.0;
the docs of dotnet/runtime and dotnet/sdk. NET lines are plain numbers (10.0, 9.0 ...), Microsoft.Extensions packages
with their own numbering carry their name (azure-1.14, ml-5.0). The C# language itself (keywords, the standard, the
feature specifications, the Roslyn compiler) is on csharp-docs. If something about .NET is not found in these
documents, it is unlikely to be in its official documentation. This set is part of the .NET family: dotnet-docs (the
.NET platform: runtime, base class library, CLI, F#, Visual Basic), csharp-docs (the C# language, its standard and
compiler), aspnetcore-docs (ASP.NET Core and classic ASP.NET), entityframework-docs (EF Core and EF6), sqlserver-docs
(SQL Server and Azure SQL), dotnet-testing-docs (xUnit, NUnit, bUnit, Moq, NSubstitute, FluentAssertions, Shouldly,
AngleSharp, Respawn), testcontainers-dotnet-docs (Testcontainers for .NET) and nuget-docs (NuGet) are meant to be
connected together -- when a question belongs to another member, name its server. Playwright for .NET is outside the
family, on playwright-docs.

**Межі.**

- Усе англійською. Переклади сайту не взято.
- Лише стабільні випуски: .NET 11 (прев'ю і RC), preview і rc ліній 1.0–10.0 не взято.
- Не взято код і тести dotnet/runtime, docs-desktop (WinForms, WPF), docs-maui, Aspire; ASP.NET Core і Entity
  Framework — у своїх примірниках.
- Довідник API з XML пакетів не перелічує успадкованих членів; прикладів у ньому немає — вони в dotnet-api-docs.
- «Applies to» dotnet-api-docs — те, що несе `xml/FrameworksIndex` сьогодні: .NET 8–10, .NET Framework 4.6.2–4.8.1 і
  .NET Standard 2.0–2.1 лише для пакетів, Windows Desktop 3.0–10.0. Старші лінії .NET дає довідник із пакетів.

**Далі в [README](../instances/dotnet/README.md):** Навіщо одна одиниця; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина .NET: піднімати разом; Корпус лише локально; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### csharp

**Коли піднімати.** Питання про мову C#: синтаксис, можливості за версіями.

**Порт** 8878, сервер `csharp-docs`. Підняти: `./df csharp serve`. Адреса: `http://127.0.0.1:8878/mcp`.

**Обсяг.** Документів: 18 933, фрагментів: 43 165.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `aspnetcore-docs` (8862),
`dotnet-docs` (8866), `dotnet-testing-docs` (8870), `entityframework-docs` (8865), `nuget-docs` (8869),
`sqlserver-docs` (8864), `testcontainers-dotnet-docs` (8867).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про мову C# — і лише про мову: ключові слова, оператори, інструкції,
шаблони, типи, перетворення, правила розв'язання перевантажень, повідомлення компілятора, що нового в кожній версії,
що каже стандарт і специфікація можливості, що зламав компілятор чергового випуску. Документація англійською, усі
стабільні версії мови: сторінки learn.microsoft.com/dotnet/csharp на день виходу кожної версії C# 7.0–14 і чинний
сайт; стандарт ECMA-334 усіх видань — 1–4 (PDF Ecma, C# 1.0 і 2.0), 5–7 (dotnet/csharpstandard, C# 5, 6, 7.0–7.3) і
чернетки комітету для C# 8–14; специфікація C# 6 від Microsoft; специфікації можливостей C# 6.0–14.0
(dotnet/csharplang); документація компілятора Roslyn і критичні зміни компілятора C# у .NET 5–10. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md). **Документація мови C# є лише в цьому примірнику.** Примірник `dotnet`
тримає платформу: .NET, бібліотеку базових класів, довідник API, CLI `dotnet`, випуски; примірники `aspnetcore`,
`entityframework`, `testcontainers-dotnet` — свої фреймворки. Так сказано й в описі інструмента пошуку, який бачить
модель: питання про `HttpClient` чи `dotnet publish` сюди не йдуть.

**Склад (так його описано моделі, англійською).**

Documents of the C# documentation -- the only C# documentation server: the pages of learn.microsoft.com/dotnet/csharp
as the site shows them now and as the repository held them on the release day of C# 7.0 to 14 (tour, fundamentals,
language reference with keywords, operators and compiler messages, programming guide, LINQ, async, what's new); the C#
standard ECMA-334, editions 1 to 7 (C# 1.0, 2.0, 5, 6, 7.3) and the drafts for C# 8 to 14; the Microsoft C# 6
specification; the feature specifications of C# 6.0 to 14.0; the Roslyn compiler docs and the breaking changes of the
C# compiler per .NET release. 0, 12.0, 7.3, 2.0, 1.0); the compiler breaking changes carry the C# version that shipped
with the .NET release. The base class library, the API reference, the dotnet CLI and ASP.NET Core are not here; if
something about the C# language is not found in these documents, it is unlikely to be in its official documentation.
This set is part of the .NET family: dotnet-docs (the .NET platform: runtime, base class library, CLI, F#, Visual
Basic), csharp-docs (the C# language, its standard and compiler), aspnetcore-docs (ASP.NET Core and classic ASP.NET),
entityframework-docs (EF Core and EF6), sqlserver-docs (SQL Server and Azure SQL), dotnet-testing-docs (xUnit, NUnit,
bUnit, Moq, NSubstitute, FluentAssertions, Shouldly, AngleSharp, Respawn), testcontainers-dotnet-docs (Testcontainers
for .NET) and nuget-docs (NuGet) are meant to be connected together -- when a question belongs to another member, name
its server. Playwright for .NET is outside the family, on playwright-docs.

**Далі в [README](../instances/csharp/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Родина .NET: піднімати разом; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code; Ліцензії.

### aspnetcore

**Коли піднімати.** Пишете вебзастосунок на ASP.NET Core.

**Порт** 8862, сервер `aspnetcore-docs`. Підняти: `./df aspnetcore serve`. Адреса: `http://127.0.0.1:8862/mcp`.

**Обсяг.** Документів: 56 153, фрагментів: 126 194.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `csharp-docs` (8878), `dotnet-docs`
(8866), `dotnet-testing-docs` (8870), `entityframework-docs` (8865), `nuget-docs` (8869), `sqlserver-docs` (8864),
`testcontainers-dotnet-docs` (8867).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про ASP.NET Core і класичний ASP.NET — від хоста, middleware,
маршрутизації й Kestrel до Blazor, SignalR, автентифікації, тестування, розгортання й переходу з ASP.NET 4.x.
Документація англійською, усі стабільні мажорні й мінорні версії: сайт learn.microsoft.com/aspnet/core кожної редакції
1.0–10.0 і сайт класичного ASP.NET; довідник API кожної лінії ASP.NET Core 1.0–10.0, класичних MVC, Web API, Web
Pages, SignalR, Identity, Katana і System.Web; версії, залежності й README пакетів NuGet і npm; markdown репозиторію
dotnet/aspnetcore, різниці API між версіями й нотатки релізів. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the ASP.NET documentation -- the pages of learn.microsoft.com/aspnet/core for every ASP.NET Core version
1.0-10.0 (3.1-10.0 as the site shows them, 1.0-3.0 from the repository of 2019-2020); the pages of
learn.microsoft.com/aspnet for classic ASP.NET 4.x; the API reference of ASP.NET Core 1.0-10.0, classic MVC, Web API,
Web Pages, Razor, SignalR, Identity, Katana and System.Web from the XML documentation of the NuGet packages; the
api-diff of Microsoft.AspNetCore.App and the ASP.NET Core release notes of 9.0 and 10.0 from dotnet/core; the NuGet
packages of ASP.NET Core and classic ASP.NET; the npm packages of the SignalR JavaScript client and the Blazor JS
interop; the markdown of the dotnet/aspnetcore repository at the last tag of each line 2.1-10.0; the GitHub release
notes of dotnet/aspnetcore, AspNetWebStack, AspNetKatana and SignalR. NET Core lines are plain numbers (10.0, 9.0
...), classic ASP.NET lines carry the product prefix (mvc-5.2, webapi-5.3, signalr-2.4, katana-4.2, netfx-4.8 ...). If
something about ASP.NET is not found in these documents, it is unlikely to be in its official documentation. This set
is part of the .NET family: dotnet-docs (the .NET platform: runtime, base class library, CLI, F#, Visual Basic),
csharp-docs (the C# language, its standard and compiler), aspnetcore-docs (ASP.NET Core and classic ASP.NET),
entityframework-docs (EF Core and EF6), sqlserver-docs (SQL Server and Azure SQL), dotnet-testing-docs (xUnit, NUnit,
bUnit, Moq, NSubstitute, FluentAssertions, Shouldly, AngleSharp, Respawn), testcontainers-dotnet-docs (Testcontainers
for .NET) and nuget-docs (NuGet) are meant to be connected together -- when a question belongs to another member, name
its server. Playwright for .NET is outside the family, on playwright-docs.

**Межі.**

- Усе англійською. Переклади сайту не взято.
- Лише стабільні випуски: preview і rc не взято. Винятки: нотатки релізів .NET 9 і 10 — з усіма preview і rc, бо
  саме в них описано нове кожного випуску; таблиці версій npm перелічують і передрелізи.
- Microsoft.Extensions.*, Entity Framework Core, Azure і IIS як окремі довідники не взято — лише те, що про них
  каже сайт ASP.NET Core.
- Приклади коду — ті, що сторінки вставляють; повні проєкти прикладів не взято.
- Довідник API з XML не перелічує успадкованих членів і не має прикладів, яких немає в самому XML.
- Сторінка класичного Identity «two-factor authentication using SMS and email» у джерелі порожня (один байт).

**Далі в [README](../instances/aspnetcore/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина .NET: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### entityframework

**Коли піднімати.** Працюєте з базою через Entity Framework.

**Порт** 8865, сервер `entityframework-docs`. Підняти: `./df entityframework serve`. Адреса: `http://127.0.0.1:8865/mcp`.

**Обсяг.** Документів: 66 635, фрагментів: 346 092.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `aspnetcore-docs` (8862),
`csharp-docs` (8878), `dotnet-docs` (8866), `dotnet-testing-docs` (8870), `nuget-docs` (8869), `sqlserver-docs`
(8864), `testcontainers-dotnet-docs` (8867).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Entity Framework Core, Entity Framework 6 і класичний Entity
Framework 4.1–5.0 та провайдери баз даних для них — від DbContext, моделювання, зв'язків, запитів LINQ і збереження до
міграцій, інструментів `dotnet ef` і Package Manager Console, продуктивності, тестування й несумісних змін кожного
випуску. Документація англійською, усі стабільні мажорні й мінорні версії: сайт learn.microsoft.com/ef кожної редакції
EF Core 1.0–10.0 і EF6; довідник API кожної лінії EF Core 1.0–10.0 і Entity Framework 4.2–6.5; пакети NuGet EF Core,
`dotnet-ef`, EF6 і всіх провайдерів з офіційних переліків; код і тести dotnet/efcore та dotnet/ef6; документація,
нотатки релізів і довідник API провайдерів. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Entity Framework documentation -- the pages of learn.microsoft.com/ef for every EF Core version
1.0-10.0 (as the site shows them now and as the repository held them after each release) and for EF6; the API
reference of EF Core 1.0-10.0 and of Entity Framework 4.2-6.5 from the XML documentation of the NuGet packages; the
NuGet packages of EF Core, dotnet-ef, EF6 and every provider on the official lists; the source code and tests of
dotnet/efcore (1.0-10.0) and dotnet/ef6 (6.0-6.5); the GitHub release notes of EF Core and EF6; the documentation,
release notes and API reference of the third-party providers (Npgsql, MongoDB, Pomelo, MySQL, Oracle, Couchbase,
KEFCore, Firebird, Jet, Spanner, YDB, DuckDB, Devart and others). 0, 9.0 ...), classic Entity Framework lines carry
"ef-" (ef-6.5, ef-4.3), providers carry their name (npgsql-10.0, pomelo-9.0, mongodb-9.1 ...). If something about
Entity Framework is not found in these documents, it is unlikely to be in its official documentation. This set is part
of the .NET family: dotnet-docs (the .NET platform: runtime, base class library, CLI, F#, Visual Basic), csharp-docs
(the C# language, its standard and compiler), aspnetcore-docs (ASP.NET Core and classic ASP.NET), entityframework-docs
(EF Core and EF6), sqlserver-docs (SQL Server and Azure SQL), dotnet-testing-docs (xUnit, NUnit, bUnit, Moq,
NSubstitute, FluentAssertions, Shouldly, AngleSharp, Respawn), testcontainers-dotnet-docs (Testcontainers for .NET)
and nuget-docs (NuGet) are meant to be connected together -- when a question belongs to another member, name its
server. Playwright for .NET is outside the family, on playwright-docs.

**Межі.**

- Усе англійською. Переклади сайту не взято.
- Лише стабільні випуски: preview, rc, EF Core 11 і теги смуг SDK (`v10.0.104`) не взято.
- Документація закритих провайдерів (Devart, Oracle, IBM, InterBase, Teradata) і сайт MySQL Connector/NET
  (dev.mysql.com) — поза корпусом: лише NuGet і README репозиторію там, де він є.
- Microsoft.Data.Sqlite як окремий пакет NuGet не взято — його код є в `src/` efcore.
- Приклади коду — ті, що сторінки вставляють; повні проєкти прикладів (`samples/`) не взято.
- Довідник API з XML не перелічує успадкованих членів і не має прикладів, яких немає в самому XML.

**Далі в [README](../instances/entityframework/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Межі, про які треба пам'ятати; Родина .NET: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### nuget

**Коли піднімати.** Створюєте або підключаєте пакети NuGet.

**Порт** 8869, сервер `nuget-docs`. Підняти: `./df nuget serve`. Адреса: `http://127.0.0.1:8869/mcp`.

**Обсяг.** Документів: 30 366, фрагментів: 61 656.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `aspnetcore-docs` (8862),
`csharp-docs` (8878), `dotnet-docs` (8866), `dotnet-testing-docs` (8870), `entityframework-docs` (8865),
`sqlserver-docs` (8864), `testcontainers-dotnet-docs` (8867).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про NuGet, менеджер пакетів .NET: клієнтські інструменти (`nuget.exe`,
`dotnet nuget`, відновлення й пакування через `dotnet`, вікна пакетів у Visual Studio), `PackageReference` і
`packages.config`, `nuget.config` і джерела пакетів (зіставлення джерел, облікові дані, підпис і довірені
підписувачі), централізоване керування версіями, блокування версій і аудит, діапазони версій і цільові платформи,
створення й публікацію пакетів (`.nuspec`, властивості пакування MSBuild, nuget.org), помилки й попередження `NU…`,
протокол сервера V3 (Server API) і клієнтські бібліотеки `NuGet.*`. Документація англійською: сторінки
learn.microsoft.com/nuget з репозиторію документації, README і `docs/` репозиторію NuGet.Client на кожному стабільному
випуску 4.0.0–7.9.0, його код і тести на останньому випуску кожної мажорної лінії, специфікації дизайну NuGet/Home,
документація й релізи NuGetGallery, 52 пакети власника `nuget` на nuget.org з кожною стабільною версією та довідник
API з XML-документації цих пакетів для кожної мінорної лінії. Код спільний і лежить у `../../engine/`, `../../server/`
та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the documentation of NuGet -- the pages of learn.microsoft.com/nuget (guides, reference, concepts, the
Server API of the V3 protocol, nuget.org, the FAQ and the release notes 1.1-7.10), the README and docs/ of
NuGet.Client at every stable release and its source code and tests at the last release of every major line, the design
specifications of NuGet/Home, the README, docs/ and release notes of NuGetGallery, the NuGet packages owned by the
NuGet team with every stable version, and the API reference from the XML documentation of those packages. 4,
server-3.4, vs-17.14, build-2.12, gallery-2024.12). If something about NuGet is not found in these documents, it is
unlikely to be in its official documentation. This set is part of the .NET family: dotnet-docs (the .NET platform:
runtime, base class library, CLI, F#, Visual Basic), csharp-docs (the C# language, its standard and compiler),
aspnetcore-docs (ASP.NET Core and classic ASP.NET), entityframework-docs (EF Core and EF6), sqlserver-docs (SQL Server
and Azure SQL), dotnet-testing-docs (xUnit, NUnit, bUnit, Moq, NSubstitute, FluentAssertions, Shouldly, AngleSharp,
Respawn), testcontainers-dotnet-docs (Testcontainers for .NET) and nuget-docs (NuGet) are meant to be connected
together -- when a question belongs to another member, name its server. Playwright for .NET is outside the family, on
playwright-docs.

**Межі.**

- Усе англійською.
- Лише стабільні випуски: передрелізи NuGet, нотатки передрелізів і NuGet.Client до 4.0 (теги 3.x, `-VSIX`,
  `3.5.0-rtm`) не взято. Документація learn.microsoft.com — у стані на 15.10.2026 (нотатки 7.10 вже є, а 7.10 на
  nuget.org ще немає).
- Не взято нічого поза трьома групами: блог NuGet, документацію Visual Studio про NuGet, інші репозиторії NuGet
  (NuGet.Jobs, NuGet.Services.*, NuGet.Insights тощо), політики nuget.org поза тими, що лежать у репозиторії
  документації (`docs/nuget-org/policies/`, `docs/policies/` — їх узято), `CONTRIBUTING.md`, `SECURITY.md` і
  `.agents/skills` NuGet.Client, `meta/` і політики NuGet/Home (Privacy-Policy, Terms-Of-Use, Issue-Triage-Policy).
- Із пакетів власника `nuget` не взято `PoliteCaptcha` (бібліотека CAPTCHA, не NuGet) і `NuGet.Services.Build` (збірка
  внутрішніх сервісів nuget.org); взято всі п'ять `NuGet.Mcp.Server.<rid>`.
- Сім записів релізів GitHub (NuGet.Client — 2, NuGet/Home — 5, 2015–2016 роки, VS 2013/2015) майже порожні: тег, дата
  й посилання на нотатки. Їх лишено, бо релізи входять до обсягу.
- Документацію NuGetGallery (8 файлів про Azure Search, листи, фронтенд, розгортання) і 41 реліз розгортань nuget.org
  взято, хоч вони про сервіс, а не про клієнт NuGet.
- Довідник API з XML не перелічує успадкованих членів і не має прикладів, яких немає в самому XML; для 6.5–6.11 його
  немає зовсім.

**Далі в [README](../instances/nuget/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Родина .NET: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### dotnet-testing

**Коли піднімати.** Пишете тести .NET: бібліотеки тестування й підміни.

**Порт** 8870, сервер `dotnet-testing-docs`. Підняти: `./df dotnet-testing serve`. Адреса: `http://127.0.0.1:8870/mcp`.

**Обсяг.** Документів: 81 241, фрагментів: 149 944.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `aspnetcore-docs` (8862),
`csharp-docs` (8878), `dotnet-docs` (8866), `entityframework-docs` (8865), `nuget-docs` (8869), `sqlserver-docs`
(8864), `testcontainers-dotnet-docs` (8867).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про тестування застосунків .NET бібліотеками xUnit.net (v2 і v3, з
аналізаторами й адаптером Visual Studio), NUnit (3–5 і NUnit 2, з адаптером, аналізаторами, консоллю й рушієм), bUnit
(компоненти Blazor), FluentAssertions і Shouldly (твердження), Moq і NSubstitute з NSubstitute.Analyzers (моки й
замінники), AngleSharp з усіма офіційними пакетами (Css, Js, Xml, XPath, Io, Wasm, Renderer, Wrappers, Diffing —
розбір і порівняння HTML, на Diffing стоїть `MarkupMatches` bUnit), FluentAssertions.Json та Respawn (очищення бази
між інтеграційними тестами). Документація англійською, усі стабільні мажорні й мінорні версії: сайти бібліотек (де
сайт має теги — на кожному випуску), README з кожного стабільного тегу, журнали змін і нотатки релізів; довідник API
кожної мінорної лінії з XML-документації пакетів NuGet; пакети NuGet з версіями, залежностями й README; код і тести на
останньому тезі кожної мажорної лінії. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the documentation of the .NET testing libraries -- xunit.net (v2 and v3 guides, analyzer rules, release
notes), docs.nunit.org and the legacy NUnit 2 documentation, bunit.dev at every minor line, fluentassertions.com,
docs.shouldly.org and nsubstitute.github.io at every stable release, the Moq wiki and changelog, the AngleSharp and
AngleSharp.Diffing docs and changelogs, the Respawn README; the API reference of every stable minor line from the XML
documentation of the NuGet packages; the NuGet packages with every stable version; the source code and tests at the
last release of every major line; GitHub release notes. 9, xunit-v3-3.2, nunit-4.3, bunit-1.40, fluentassertions-6.12,
moq-4.20, nsubstitute-5.3 ...). If something about these libraries is not found in these documents, it is unlikely to
be in their official documentation. This set is part of the .NET family: dotnet-docs (the .NET platform: runtime, base
class library, CLI, F#, Visual Basic), csharp-docs (the C# language, its standard and compiler), aspnetcore-docs
(ASP.NET Core and classic ASP.NET), entityframework-docs (EF Core and EF6), sqlserver-docs (SQL Server and Azure SQL),
dotnet-testing-docs (xUnit, NUnit, bUnit, Moq, NSubstitute, FluentAssertions, Shouldly, AngleSharp, Respawn),
testcontainers-dotnet-docs (Testcontainers for .NET) and nuget-docs (NuGet) are meant to be connected together -- when
a question belongs to another member, name its server. Playwright for .NET is outside the family, on playwright-docs.

**Межі.**

- Усе англійською.
- Лише стабільні випуски: передрелізи NuGet і нотатки передрелізів не взято; xunit.net і docs.nunit.org — у стані на
  день збирання.
- Не взято: MSTest, Playwright, Testcontainers, Coverlet, AutoFixture, пакети розширень NUnit (`NUnit.Extension.*`),
  NUnitLite 0.x–1.x як окремий фреймворк, платформні пакети `xunit-console-tool.<rid>` і `xunit.v3.*.aot.*`, крім
  мета-пакетів, пакети AngleSharp.* інших авторів (Verify.AngleSharp тощо), код доповнень AngleSharp,
  FluentAssertions.Json, аналізаторів, адаптерів і консолей.
- bUnit доведено до 2.12.5 (19.10.2026, того самого дня, що й перша збірка): лінія 2.12 є на сайті, в довіднику API,
  README, журналі змін, пакетах NuGet і в коді з тестами. Випуски bUnit після 2.12.5 потраплять у корпус лише
  оновленням за схемою нижче.
- Довідник API з XML не перелічує успадкованих членів і не має прикладів, яких немає в самому XML.

**Далі в [README](../instances/dotnet-testing/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Межі, про які треба пам'ятати; Родина .NET: піднімати разом; Архівний режим: сервер без корпусу;
Установка venv; Збирання корпусу; Сервер під Claude Code.

### testcontainers-dotnet

**Коли піднімати.** Запускаєте контейнери в тестах .NET через Testcontainers.

**Порт** 8867, сервер `testcontainers-dotnet-docs`. Підняти: `./df testcontainers-dotnet serve`. Адреса: `http://127.0.0.1:8867/mcp`.

**Обсяг.** Документів: 17 270, фрагментів: 26 851.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `aspnetcore-docs` (8862),
`csharp-docs` (8878), `dotnet-docs` (8866), `dotnet-testing-docs` (8870), `entityframework-docs` (8865), `nuget-docs`
(8869), `sqlserver-docs` (8864).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Testcontainers for .NET — бібліотеку для тестів з одноразовими
контейнерами Docker: будівники контейнерів, образів, мереж і томів, стратегії очікування, Resource Reaper, повторне
використання, Docker Compose, налаштування й автентифікацію Docker, віддалений Docker і Docker у Docker, CI/CD,
інтеграцію з xUnit.net і всі модулі (PostgreSQL, MS SQL, MySQL, MongoDB, Redis, Kafka, RabbitMQ, LocalStack, Azurite,
Cosmos DB, Elasticsearch і ще п'ятдесят), — а також про Docker.DotNet.Enhanced, клієнт Docker Engine API, на якому
стоїть бібліотека. Документація англійською, усі стабільні версії 0.0.4–4.16.0: сайт dotnet.testcontainers.org на
кожному тезі і README, яким документація була до сайту; довідник API кожної мінорної лінії з XML-документації пакетів
NuGet; пакети NuGet з версіями й залежностями; код, тести й приклади репозиторію; релізи GitHub. Код спільний і лежить
у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Testcontainers for .NET documentation -- the pages of dotnet.testcontainers.org at every stable
release 2.2.0-4.16.0 (with the code samples the site inserts from the tests) and the README that was the documentation
of 0.0.4-2.1.0; the API reference of the core package and of every module for each minor line 2.2-4.16 and of
Docker.DotNet.Enhanced 4.2-4.3 from the XML documentation of the NuGet packages; the NuGet packages of Testcontainers,
its 66 modules, the xUnit.net packages, DotNet.Testcontainers and Docker.DotNet.Enhanced; the source code, tests and
examples of testcontainers/testcontainers-dotnet at the last release of each minor line 0.0-4.16 and of
testcontainers/Docker.DotNet 3.125-4.3; the GitHub release notes of both and the CHANGELOG.md of 2.1-2.3. 16, 3.10
...), Docker.DotNet.Enhanced lines carry "docker-dotnet-" (docker-dotnet-4.3). If something about Testcontainers for
.NET is not found in these documents, it is unlikely to be in its official documentation. This set is part of the .NET
family: dotnet-docs (the .NET platform: runtime, base class library, CLI, F#, Visual Basic), csharp-docs (the C#
language, its standard and compiler), aspnetcore-docs (ASP.NET Core and classic ASP.NET), entityframework-docs (EF
Core and EF6), sqlserver-docs (SQL Server and Azure SQL), dotnet-testing-docs (xUnit, NUnit, bUnit, Moq, NSubstitute,
FluentAssertions, Shouldly, AngleSharp, Respawn), testcontainers-dotnet-docs (Testcontainers for .NET) and nuget-docs
(NuGet) are meant to be connected together -- when a question belongs to another member, name its server. Playwright
for .NET is outside the family, on playwright-docs.

**Межі.**

- Усе англійською.
- Лише стабільні випуски: beta- і preview-збірки NuGet, гілка `develop` (живий сайт може бути на крок попереду 4.16.0)
  не взято.
- Пакети інших авторів з «Testcontainers» в імені (WireMock.Net.Testcontainers, Dapr.Testcontainers,
  Microcks.Testcontainers, TestContainers.Container.* та інші) — поза корпусом.
- Testcontainers для Java, Go, Node.js, Python і сайт testcontainers.com — поза корпусом.
- Docker, Docker Compose, бази й сервіси, які піднімають модулі, і xUnit.net самі по собі — їхня власна документація.
- Довідник API з XML не перелічує успадкованих членів і не має прикладів, яких немає в самому XML.

**Далі в [README](../instances/testcontainers-dotnet/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Родина .NET: піднімати разом; Архівний режим: сервер без
корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

<!-- тема: Python і обробка даних -->

### python

**Коли піднімати.** Пишете на Python: мова, стандартна бібліотека, PEP, pip, uv, Poetry.

**Порт** 8944, сервер `python-docs`. Підняти: `./df python serve`. Адреса: `http://127.0.0.1:8944/mcp`.

**Обсяг.** Документів: 16 852, фрагментів: 117 603.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про мову Python за її документацією. Він знає документацію CPython на
кожну мінорну лінію 2.6–3.15, старий сайт docs.python.org для ліній 1.4–2.5, журнали змін, документи PEP, а ще
менеджери пакетів pip, uv і Poetry, посібник із пакування та документацію PyPI. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`, а тут лежать лише дані домену. Загальний устрій фабрики описано в
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Python documentation -- the CPython documentation at the last patch of every minor line 2.6–3.15, the
old docs.python.org pages of 1.4–2.5, the CPython change logs, every PEP, and pip, uv and Poetry at every minor line
with their change logs and PyPI records, the Python Packaging User Guide and the PyPI documentation. Prereleases are
not here.

**Далі в [README](../instances/python/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### data-cleaning

**Коли піднімати.** Чистите або об'єднуєте таблиці через pandas, openpyxl чи RapidFuzz.

**Порт** 8949, сервер `data-cleaning-docs`. Підняти: `./df data-cleaning serve`. Адреса: `http://127.0.0.1:8949/mcp`.

**Обсяг.** Документів: 18 093, фрагментів: 31 198.

**Опис.**

Цей примірник зібрав документацію трьох бібліотек Python і віддає її через сервер MCP, щоб модель відповідала з їхніх
текстів, а не з пам'яті. Бібліотека pandas читає й об'єднує таблиці. Бібліотека openpyxl читає й пише файли Excel.
Бібліотека RapidFuzz порівнює рядки, які схожі, але не однакові, і так допомагає знаходити дублікати записів. Разом
вони потрібні для однієї задачі: прочитати кілька файлів Excel, очистити дані й знайти людей, записаних двічі.

**Склад (так його описано моделі, англійською).**

Documents of pandas, openpyxl and RapidFuzz: guides and what's new of pandas 0.4-3.1, its API reference 1.5-3.1,
openpyxl 2.4-3.1, RapidFuzz 0.12-3.14 and the PyPI records of all three. Other Python libraries and the Python
language are not here.

**Далі в [README](../instances/data-cleaning/README.md):** Скільки цього; Що в цій теці; Звідки документація; Як
підняти сервер; Архівний режим: сервер без корпусу.

### xgboost

**Коли піднімати.** Навчаєте дерева рішень, градієнтний бустинг чи випадковий ліс через XGBoost: параметри, GPU, формат моделі, прогноз.

**Порт** 8954, сервер `xgboost-docs`. Підняти: `./df xgboost serve`. Адреса: `http://127.0.0.1:8954/mcp`.

**Обсяг.** Документів: 774, фрагментів: 4 631.

**Опис.**

Цей примірник зібрав документацію бібліотеки XGBoost і віддає її через сервер MCP, щоб модель відповідала з текстів
бібліотеки, а не з пам'яті. XGBoost навчає ансамблі дерев рішень. Ансамбль — це багато дерев, чиї відповіді
складаються в одну. Найчастіше XGBoost будує дерева по черзі, і кожне наступне виправляє помилки попередніх; цей
спосіб називають градієнтним бустингом. Той самий XGBoost уміє будувати й випадковий ліс: тоді за один раунд росте
кілька незалежних дерев, і їхні відповіді усереднюються (параметр `num_parallel_tree`).

**Склад (так його описано моделі, англійською).**

Documents of XGBoost: the doc/ folder of the last patch of every minor line 0.40-3.4, the Python API reference and
Python examples of the site for the lines 0.72-3.4, the PyPI records, the GitHub release notes and the NEWS.md change
log. LightGBM, NumPy, scikit-learn and the Python language are not here.

**Далі в [README](../instances/xgboost/README.md):** Скільки цього; Що в цій теці; Звідки документація; Як підняти
сервер; Архівний режим: сервер без корпусу.

### lightgbm

**Коли піднімати.** Навчаєте градієнтний бустинг чи випадковий ліс через LightGBM: параметри та їхні псевдоніми, GPU, прогноз, зміни між версіями.

**Порт** 8955, сервер `lightgbm-docs`. Підняти: `./df lightgbm serve`. Адреса: `http://127.0.0.1:8955/mcp`.

**Обсяг.** Документів: 447, фрагментів: 2 592.

**Опис.**

Цей примірник зібрав документацію бібліотеки LightGBM і віддає її через сервер MCP, щоб модель відповідала з текстів
бібліотеки, а не з пам'яті. LightGBM, як і XGBoost, навчає ансамблі дерев рішень градієнтним бустингом: дерева
будуються по черзі, і кожне наступне виправляє помилки попередніх. Особливість LightGBM у тому, як росте одне дерево.
Бібліотека щоразу ділить той лист, поділ якого найбільше зменшує помилку, а не весь рівень дерева одразу, і шукає
поділи за гістограмами ознак. З параметром `boosting="rf"` LightGBM будує випадковий ліс: незалежні дерева на
випадкових підвибірках, чиї відповіді усереднюються.

**Склад (так його описано моделі, англійською).**

Documents of LightGBM: the docs/ folder and the example READMEs of the last patch of every minor line 1-4.7, the
Python API reference of the site for the lines 3.2-4.7, the PyPI records and the GitHub release notes. XGBoost, NumPy,
scikit-learn and the Python language are not here.

**Далі в [README](../instances/lightgbm/README.md):** Скільки цього; Що в цій теці; Звідки документація; Як підняти
сервер; Архівний режим: сервер без корпусу.

### numpy

**Коли піднімати.** Працюєте з масивами NumPy: сигнатури функцій, dtype і правила приведення типів, broadcasting, що змінилося між версіями 1.3–2.5.

**Порт** 8956, сервер `numpy-docs`. Підняти: `./df numpy serve`. Адреса: `http://127.0.0.1:8956/mcp`.

**Обсяг.** Документів: 31 404, фрагментів: 46 713.

**Опис.**

Цей примірник зібрав документацію бібліотеки NumPy і віддає її через сервер MCP, щоб модель відповідала з текстів
бібліотеки, а не з пам'яті. NumPy зберігає числа в багатовимірних масивах однакового типу і рахує над цілими масивами
одразу, без циклу Python. На NumPy стоять pandas, XGBoost, LightGBM і більшість інших бібліотек Python для обчислень.

**Склад (так його описано моделі, англійською).**

Documents of NumPy: the documentation site of every minor line 1.13-2.5 (user guide, API reference, C API, F2PY,
release notes, developer guide) and the PyPI records. CuPy, pandas, SciPy, XGBoost, LightGBM and the Python language
are not here.

**Далі в [README](../instances/numpy/README.md):** Скільки цього; Що в цій теці; Звідки документація; Як підняти
сервер; Архівний режим: сервер без корпусу.

<!-- тема: PHP -->

### php

**Коли піднімати.** Пишете на PHP або ставите пакети через Composer: мова, функції, перехід між версіями, RFC, `composer.json`.

**Порт** 8951, сервер `php-docs`. Підняти: `./df php serve`. Адреса: `http://127.0.0.1:8951/mcp`.

**Обсяг.** Документів: 13 184, фрагментів: 85 309.

**Опис.**

Цей примірник зібрав документацію мови PHP і її менеджера пакетів Composer та віддає її через сервер MCP, щоб модель
відповідала з її тексту, а не з пам'яті.

**Склад (так його описано моделі, англійською).**

Documents of the PHP documentation: the PHP Manual of php.net, the UPGRADING and NEWS files of php-src, the RFCs of
wiki.php.net, the Composer documentation and the Packagist pages. The manual has one current edition and carries no
version.

**Далі в [README](../instances/php/README.md):** Скільки цього; Що в цій теці; Звідки документація; Як підняти сервер;
Архівний режим: сервер без корпусу.

<!-- тема: Сервери, контейнери, розгортання -->

### linux

**Коли піднімати.** Адмініструєте Linux: команди, сторінки man, налаштування Ubuntu.

**Порт** 8782, сервер `linux-docs`. Підняти: `./df linux serve`. Адреса: `http://127.0.0.1:8782/mcp`.

**Обсяг.** Документів: 31 534, фрагментів: 134 661.

**Опис.**

Двадцять другий примірник фабрики: захищений MCP-сервер, що відповідає на питання про адміністрування Linux за
документацією, з якої працює адміністратор, — man-сторінки Ubuntu 22.04, 24.04 і 26.04, проєкт man-pages (системні
виклики, файли, огляди ядра), admin-guide ядра, systemd, посібники GNU (bash, coreutils, grep, sed, findutils, tar),
довідка vim, Debian Administrator's Handbook, документація Ubuntu Server і Rocky Linux, і сторінка іспиту LFCS. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the documentation of the Linux system -- the man pages of Ubuntu 22.04, 24.04 and 26.04 (several hundred
administration commands and configuration files, with their packages), the Linux man-pages project (sections 2, 4, 5
and 7, releases 2.00 to 6.19), the kernel admin-guide (5.10 to 7.2), systemd (docs and man pages, 183 to 262), the GNU
manuals of bash, coreutils, grep, sed, findutils and tar (every release), vim help (7.0 to 9.2), the Debian
Administrator's Handbook (Debian 6 to 13), the Ubuntu Server and Rocky Linux documentation and the LFCS exam page.
Each project numbers its own versions; titles name the project. Docker, Kubernetes, Ansible and cloud consoles are not
here.

**Межі.**

- **Дистрибутив іспиту LFCS не названо.** Відповіді — для поточних випусків; де Ubuntu й родина RHEL розходяться
  (apt/dnf, ufw/firewalld, AppArmor/SELinux, netplan/NetworkManager), промпт велить назвати обидва варіанти.
- **Man-сторінки Ubuntu — лише явний перелік** (`pages` у `sources.json`). Команди поза ним шукаються в man-pages,
  посібниках GNU чи systemd або не знаходяться зовсім; нова потрібна сторінка дописується в перелік.
- **Сторінки RHEL-родини** — лише з документації Rocky Linux; man-сторінок dnf, firewalld, SELinux тут немає.
- **Ліцензії** сторінки LFCS і документації Ubuntu Server не підтверджено; узято за рішенням власника 03.10.2026.
- Docker, Kubernetes, Ansible і хмарні консолі — в інших примірниках або ніде.

**Далі в [README](../instances/linux/README.md):** Навіщо; Скільки цього; Мітки версій; Нові читачі; Межі, про які
треба пам'ятати; Архівний режим: сервер без корпусу; Збирання корпусу; Сервер під Claude Code.

### docker

**Коли піднімати.** Працюєте з Docker: Dockerfile, Compose, рушій, збирання образів.

**Порт** 8780, сервер `docker-docs`. Підняти: `./df docker serve`. Адреса: `http://127.0.0.1:8780/mcp`.

**Обсяг.** Документів: 1 264, фрагментів: 10 111.

**Опис.**

Двадцятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Docker — Engine, Dockerfile, збирання
образів (BuildKit, buildx, bake), Compose, Docker Hub і CLI — за офіційною документацією docs.docker.com і нотатками
релізів Engine, Compose і Buildx. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека
тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Docker documentation at docs.docker.com -- Get started, Docker Engine (install, containers,
networking, storage, daemon, security, swarm), Docker Build (BuildKit, buildx, cache, multi-platform, bake, CI),
Docker Compose, Docker Hub, account security, the Dockerfile reference, the Compose file reference, build checks, the
CLI reference of docker, docker buildx, docker compose and dockerd, and the language and task guides; the Docker
Engine release notes for 27.x, 28.x and 29.x; and the GitHub release notes of Docker Engine (moby/moby, docker-v
tags), Docker Compose and Docker Buildx. The documentation itself is the current edition and carries no version;
release notes carry the version of their own product -- Engine 27 to 29, Compose 0.3 to 5, Buildx 0.x. Docker Desktop,
Docker AI, Docker Hardened Images, Scout, Extensions, Kubernetes and Podman are not here.

**Межі.**

Тут немає Docker Desktop, Docker AI (Model Runner, Gordon, MCP Toolkit, sandboxes), Docker Hardened Images, Scout,
Extensions, Build Cloud, Testcontainers, керування підпискою й обліковими записами, а також команд CLI цих
продуктів (`docker mcp`, `docker model`, `docker scout`, `docker dhi`, `docker desktop`, `docker pass`,
`docker offload`). Немає й специфікації Engine API за версіями (OpenAPI v1.40…v1.56): її YAML потребує PyYAML,
якого в цьому примірнику немає, а сторінки Engine API про SDK і історію версій API є. Нотатки релізів Engine
старіших за 27 не взято. Kubernetes, containerd і runc окремо — поза примірником.

**Далі в [README](../instances/docker/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Межі,
про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code;
На іншій машині.

### kubernetes

**Коли піднімати.** Працюєте з Kubernetes: об'єкти, `kubectl`, адміністрування, підготовка до CKAD чи CKA.

**Порт** 8781, сервер `kubernetes-docs`. Підняти: `./df kubernetes serve`. Адреса: `http://127.0.0.1:8781/mcp`.

**Обсяг.** Документів: 45 270, фрагментів: 144 282.

**Опис.**

Двадцять перший примірник фабрики: захищений MCP-сервер, що відповідає на питання про Kubernetes і інструменти навколо
кластера за офіційною документацією всіх версій — kubernetes.io від 1.0 до 1.37 з прикладами й згенерованими
довідниками, журнал змін кожного патча, розклад релізів, а поруч — Gateway API, k3s, k3d, Traefik, cert-manager, Helm,
Kustomize і книга kubectl, SOPS, age, metrics-server і документація Let's Encrypt, кожен із нотатками релізів, і
програми сертифікаційних іспитів CNCF (CKA, CKAD, CKS, KCNA та інші). Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official documentation of Kubernetes and of the tools around the cluster -- kubernetes.io/docs of
every release from 1.0 to 1.37 (each page once per release line, with its examples, feature states and generated
references: API, kubectl, kubeadm, component flags, feature gates), the changelog of every patch, alpha, beta and rc
from 1.2 on, and the release schedule with end of life dates; Gateway API (docs and GEPs, 0.1 to 1.7), k3s (docs and
every release), k3d (3.0 to 5.9), Traefik (1.0 to 3.7), cert-manager (1.0 to 1.21), Helm (2, 3 and 4), Kustomize (1.0
to 5.8) and the kubectl book, SOPS, age (1.0.0 to 1.3.2), metrics-server (0.1 to 0.9) and the Let's Encrypt
documentation, with the GitHub release notes of each tool. Each tool numbers its own versions; titles name the tool.
Prometheus, Grafana, Argo CD, Flux, Sealed Secrets, Docker and cloud providers are not here.

**Межі.**

Тут немає Docker, buildx і реєстрів образів (окремий примірник `docker`), Prometheus, Grafana, Loki, Argo CD, Flux,
Sealed Secrets, сервісних мереж і консолей хмарних провайдерів — план навчання лише згадує їх. Блог kubernetes.io
(71 МБ) не взято: анонси версій дублюють журнал змін і сторінки документації. Старий посібник SOPS (README.rst)
узято лише з останнього патча кожної лінії, 1.13–3.13.0; з 3.13.1 README лише відсилає на getsops.io.

Сторінки `contribute/` сайту Kubernetes (як писати документацію) лишаються з шорткодами в тексті там, де самі їх
показують як приклад розмітки.

**Далі в [README](../instances/kubernetes/README.md):** Навіщо; Скільки цього; Мітки версій; Що в цій теці; Звідки
документація; Програми іспитів CNCF; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка
venv; Збирання корпусу; Сервер під Claude Code; На іншій машині.

### gvisor

**Коли піднімати.** Ізолюєте контейнери через gVisor і `runsc`.

**Порт** 8859, сервер `gvisor-docs`. Підняти: `./df gvisor serve`. Адреса: `http://127.0.0.1:8859/mcp`.

**Обсяг.** Документів: 1 219, фрагментів: 5 792.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про gVisor — «ядро застосунку» для контейнерів: воно перехоплює
системні виклики програми й виконує їх саме, у просторі користувача, ядром, написаним на Go (Sentry), тож програма
майже не торкається ядра господаря. Запускає gVisor `runsc` — середовище виконання OCI, яке Docker, containerd, CRI-O
і Kubernetes викликають замість звичного `runc`. Документація — сторінки gvisor.dev/docs із теки `g3doc` репозиторію
google/gvisor і кореневі файли репозиторію для кожного випуску 20190304.1–20261012.0; прапорці й підкоманди `runsc` з
коду тих самих випусків; сторінки gvisor.dev поза документацією (таблиці системних викликів, сумісність застосунків,
історія вразливостей, блог); архівний сайт 2019–2020 і архівний gvisor-containerd-shim; нотатки релізів; пакет `runsc`
в APT і довідник netstack — мережевого стека gVisor як бібліотеки Go — на pkg.go.dev. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md). Слова, що трапляються нижче: - **Sentry** — ядро gVisor на Go, що виконує системні
виклики програми; **Gofer** — окремий процес, через який Sentry дістає файли господаря, а **directfs** — режим, де
Sentry відкриває їх сам, без Gofer; - **платформа** — спосіб, яким gVisor перехоплює системні виклики: `systrap` (на
seccomp, типова), `kvm` (апаратна віртуалізація), `ptrace` (стара); - **shim containerd** — посередник між containerd
і `runsc` (`containerd-shim-runsc-v1`); - **RuntimeClass** — об'єкт Kubernetes, що вибирає для пода середовище
виконання (так GKE Sandbox і вмикає gVisor); - **`g3doc`** — тека документації в репозиторії, з якої Jekyll збирає
gvisor.dev/docs; - **псевдоверсія** — версія модуля Go без тегу: `0.0.0-<час>-<коміт>`.

**Склад (так його описано моделі, англійською).**

Documents of the gVisor documentation -- the docs of gvisor.dev from the g3doc folder of google/gvisor for every
release 20190304.1-20261012.0 (installation, quick starts, containerd and CRI-O, platforms, networking, filesystem,
GPU, checkpoint/restore, observability, Runtime Monitoring, debugging, production, SDKs, tutorials, FAQ, the
architecture guide) with the repository README, SECURITY and other root files; the runsc flags and subcommands from
runsc/config and runsc/cmd of every release; the pages of gvisor.dev outside the docs (users, application
compatibility, security track record, syscall tables for linux/amd64 and arm64, the blog 2019-2026); the archived site
of 2019-2020 and the archived gvisor-containerd-shim 0.0.1-0.0.4; the GitHub release notes 20260817.0-20261012.0; the
runsc package of the APT repository; the pkg.go.dev reference of netstack (pkg/tcpip and its subpackages, pkg/buffer).
0 and any 20261012.N), containerd-shim-0 is the archived shim, 0.0 is the Go pseudo-version of the netstack reference.
If something about gVisor or runsc is not found in these documents, it is unlikely to be in its official
documentation.

**Межі.**

- Структура `Config` (`config.go`) і функція `RegisterFlags` (`flags.go`) — оголошення по 16–20 КБ, поділені за
  довжиною, тож питання про один прапорець зазвичай приходить на сторінку посібника, де його вживають, а не на рядок
  коду. Типове значення варто дочитати через `read_section` цілим фрагментом.
- Таблиці системних викликів amd64 і arm64 — кожна одним довгим розділом, поділеним за довжиною: фрагмент про виклик
  несе й сусідні рядки таблиці.
- `--nvproxy` у `flags.go` позначено LEGACY: підтримка GPU вмикається сама, коли в специфікації OCI є пристрої NVIDIA.
  Сторінка посібника про GPU досі каже, що прапорець потрібен.
- Тексти pkg.go.dev зберігають анотації gVisor `+stateify savable` у коментарях типів.
- Нотатки релізів GitHub є лише з 20260817.0; раніші зміни видно тільки з порівняння редакцій сторінок і коду.
- Netstack — лише чинна псевдоверсія, без історії; APT — лише останній випуск.
- У тегах 2019 року `g3doc` тримає лише `checkpoint_restore.md` (з 20190722.1 ще README); повна документація — з
  20200518.0, а до того її дає архівний сайт.
- Документації Docker, containerd, Kubernetes і самого ядра Linux (man системних викликів, seccomp, KVM, cgroups) тут
  немає: Docker — у примірнику `docker`, Kubernetes і containerd у кластері — у `kubernetes`, ядро — у `linux`.

**Далі в [README](../instances/gvisor/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### nvidia-container-toolkit

**Коли піднімати.** Даєте контейнерам доступ до відеокарти NVIDIA.

**Порт** 8861, сервер `nvidia-container-toolkit-docs`. Підняти: `./df nvidia-container-toolkit serve`. Адреса: `http://127.0.0.1:8861/mcp`.

**Обсяг.** Документів: 1 092, фрагментів: 4 439.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про NVIDIA Container Toolkit — набір, який дає контейнерам доступ до
GPU NVIDIA: середовище виконання `nvidia-container-runtime` (обгортка над `runc`, що дописує в специфікацію OCI
пристрої, бібліотеки драйвера й хуки), хук `nvidia-container-runtime-hook`, CLI `nvidia-ctk` (налаштування Docker,
containerd, CRI-O і Podman, генерація специфікацій CDI), хуки `nvidia-cdi-hook`, встановлювач `nvidia-ctk-installer`
(образ, яким користується GPU Operator) і під ними бібліотека libnvidia-container з CLI `nvidia-container-cli`.
Документація — сайт docs.nvidia.com кожної опублікованої версії 1.6.0–1.20.1; документи, журнал змін і нотатки релізів
репозиторію NVIDIA/nvidia-container-toolkit; код команд із прапорцями кожного сталого тегу v1.0.5–v1.20.1; код і тести
v1.20.1; README, журнал і релізи libnvidia-container; архівні nvidia-docker і nvidia-container-runtime; специфікація
Container Device Interface; пакети офіційного репозиторію APT і довідник публічних пакетів Go на pkg.go.dev. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md). Слова, що трапляються нижче: - **середовище виконання** (runtime)
— програма, яку Docker чи containerd викликають, щоб створити контейнер за специфікацією OCI; звичайне — `runc`, тут —
`nvidia-container-runtime` поверх нього; - **хук** — програма, яку середовище виконання запускає на певному кроці
створення контейнера (`createContainer`, `prestart`): так у контейнер потрапляють пристрої й бібліотеки драйвера; -
**CDI** (Container Device Interface) — відкрита специфікація CNCF: файл YAML чи JSON у `/etc/cdi` або `/var/run/cdi`
описує пристрій (`nvidia.com/gpu=0`) і зміни, які треба внести в контейнер (`containerEdits`: змінні, вузли пристроїв,
монтування, хуки), а рушій (containerd, CRI-O, Docker, Podman) вносить їх сам; - **режими**
`nvidia-container-runtime`: `legacy` (усе робить хук через `nvidia-container-cli`), `cdi` (зміни зі специфікації CDI),
`csv` (Jetson, перелік файлів у CSV), `auto` (вибирає сам); - **unified release** — з 1.13 libnvidia-container і
nvidia-container-toolkit випускаються разом під одним номером.

**Склад (так його описано моделі, англійською).**

Documents of the NVIDIA Container Toolkit documentation -- the docs.nvidia.com site of every published version
1.6.0-1.20.1 (installation, configuring Docker, containerd, CRI-O and Podman, specialized Docker configurations and
environment variables, CDI support, architecture, supported platforms, sample workload, troubleshooting, release
notes); the repository documents, CHANGELOG and GitHub release notes of NVIDIA/nvidia-container-toolkit; the command
code with the flags of nvidia-ctk, nvidia-cdi-hook, nvidia-ctk-installer, nvidia-container-runtime and
nvidia-container-runtime-hook of every stable tag v1.0.5-v1.20.1; the Go code and tests of v1.20.1; the README,
CHANGELOG and release notes of libnvidia-container (nvidia-container-cli); the archived nvidia-docker and
nvidia-container-runtime READMEs; the CDI specification (cncf-tags/container-device-interface); the packages of the
APT repository; the pkg.go.dev reference of the public Go packages. 20" is a toolkit and libnvidia-container line,
"nvidia-docker-2.14", "nvidia-container-runtime-3.14" and "cdi-1.1" are the lines of those products. If something
about the NVIDIA Container Toolkit is not found in these documents, it is unlikely to be in its official
documentation.

**Межі.**

- Старі теки сайту — не точні знімки своїх версій: 1.6.0, 1.7.0, 1.8.0 і 1.8.1 тримають ту саму документацію з
  нотатками випусків аж до 1.8.1, так само 1.10.0 з 1.11.0, 1.12.0 з 1.12.1, 1.13.1 з 1.13.5 — їх викладено пізніше
  одним станом. Номер теки — це те, що каже сайт.
- `command.build()` з довгим переліком прапорців поділено за довжиною, а типове значення часто — константа з розділу
  `const` того самого файла: перш ніж називати значення, варто дочитати обидва розділи через `read_section`.
- CHANGELOG libnvidia-container у репозиторії ведуть лише для 1.14 (1.14.0 і 1.14.1); решта історії бібліотеки — у
  нотатках релізів, а з 1.13 вони здебільшого відсилають до спільного релізу toolkit.
- APT — лише amd64 і лише версії 1.14.0–1.20.1, які репозиторій ще тримає; pkg.go.dev — лише версія модуля 1.20.1;
  повний код і тести — лише 1.20.1 (для старших тегів — тільки код команд).
- Вікі архівного nvidia-docker на GitHub (стара документація встановлення й FAQ) у корпус не входить: джерела — сайт і
  файли репозиторіїв.
- Документації Docker, containerd, Kubernetes, NVIDIA GPU Operator, device plugin і самого драйвера тут немає: Docker —
  у примірнику `docker`, Kubernetes і containerd у кластері — у `kubernetes`, GPU у пісочниці gVisor (nvproxy) — у
  `gvisor`.

**Далі в [README](../instances/nvidia-container-toolkit/README.md):** Навіщо окремий примірник; Скільки цього; Що в
цій теці; Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### nginx

**Коли піднімати.** Налаштовуєте nginx як вебсервер або зворотний проксі.

**Порт** 8798, сервер `nginx-docs`. Підняти: `./df nginx serve`. Адреса: `http://127.0.0.1:8798/mcp`.

**Обсяг.** Документів: 2 181, фрагментів: 11 390.

**Опис.**

Тридцять восьмий примірник фабрики: захищений MCP-сервер, що відповідає на питання про nginx. Тут документація
nginx.org — поточна (мітка «1.31») і знімки на мить випуску кожної стабільної гілки від 1.0 до 1.30, — журнали змін
кожного випуску від 0.1.0 до 1.31, NGINX Admin Guide, NGINX Ingress Controller (поточний і LTS) і NGINX Gateway Fabric
з docs.nginx.com та контролер ingress-nginx спільноти Kubernetes кожної мінорної версії від 0.34 до 1.15. Код спільний
і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents about nginx in English -- the nginx.org documentation (every module and directive, njs, guides, FAQ) as it
is now and at the release of every stable branch 1.0 to 1.30, the change log of every release from 0.1.0 to 1.31, the
NGINX Admin Guide, NGINX Ingress Controller and NGINX Gateway Fabric of docs.nginx.com, and the ingress-nginx
controller 0.34 to 1.15. Other web servers and proxies are not here.

**Межі.**

Тут немає документації nginx російською, njs поза nginx.org, сторонніх модулів (Lua, OpenResty, ModSecurity поза
сторінками docs.nginx.com), NGINX Unit, NGINX One, NGINX Instance Manager, F5 WAF як окремого продукту, старих версій
docs.nginx.com (сайт публікує лише поточну), історії NIC і NGF до поточного випуску, а також інших серверів і проксі
(Apache, Caddy, HAProxy, Traefik, Envoy). Сам Kubernetes — у примірнику `kubernetes`, Docker — у `docker`, тексти RFC
про TLS і HTTP — у `webstandards`.

**Далі в [README](../instances/nginx/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Версії у
відповіді; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер
під Claude Code.

### certbot

**Коли піднімати.** Отримуєте й поновлюєте сертифікати TLS через Certbot.

**Порт** 8811, сервер `certbot-docs`. Підняти: `./df certbot serve`. Адреса: `http://127.0.0.1:8811/mcp`.

**Обсяг.** Документів: 740, фрагментів: 3 337.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Certbot — клієнт ACME від EFF, який отримує й поновлює безкоштовні
сертифікати Let's Encrypt і сам налаштовує Apache та nginx, — за документацією всіх його стабільних версій: сайтом
eff-certbot.readthedocs.io у стані на кожен реліз, сторінками плагінів DNS, журналом змін і реєстром PyPI certbot,
acme та всіх офіційних плагінів. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека
тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Certbot documentation -- the eff-certbot.readthedocs.io site as it stood at every stable release of
Certbot (introduction, Get Certbot, the User Guide with commands, plugins, renewal, hooks and the configuration file,
what a certificate is, challenges, ciphers, compatibility, contributing, packaging, resources, the man page and the
full `certbot --help all` reference); the pages of every certbot-dns-* plugin (parameters, credentials file, examples)
at every release; the changelog; and the PyPI history of certbot, acme, certbot-apache, certbot-nginx and every
certbot-dns-* plugin, including the required Python version, the dependencies and the date of every release. The Let's
Encrypt site (letsencrypt.org: rate limits, chain of trust, ACME protocol), the ACME RFC 8555, the API reference of
the Python modules, the documentation of Apache, nginx and the DNS providers, and third-party plugins are not here; if
something about Certbot is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Межі.**

Сайту Let's Encrypt (letsencrypt.org: ліміти, ланцюжки довіри, протокол) тут немає — він є в примірнику
`kubernetes` (джерело `letsencrypt-docs`). Немає й RFC 8555 (ACME), документації Apache, nginx (є примірник `nginx`)
і провайдерів DNS, сторонніх плагінів, сайту certbot.eff.org з інструкціями під кожну систему (його сторінки
складає застосунок, а не текст у репозиторії) і коду самого Certbot.

**Далі в [README](../instances/certbot/README.md):** Скільки цього; Що в цій теці; Звідки документація; Межі, про які
треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### cloudflare

**Коли піднімати.** Працюєте з Cloudflare: Workers, Pages, DNS, wrangler.

**Порт** 8937, сервер `cloudflare-docs`. Підняти: `./df cloudflare serve`. Адреса: `http://127.0.0.1:8937/mcp`.

**Обсяг.** Документів: 10 198, фрагментів: 65 309.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Cloudflare за його документацією: увесь сайт
developers.cloudflare.com — платформа розробника (Workers і їхні API, прив'язки, Wrangler, Pages, R2, D1, KV, Durable
Objects, Queues, Workflows, Workers AI, Vectorize, Hyperdrive, AI Gateway, Agents, Containers), DNS, кеш і CDN,
правила, SSL/TLS, WAF, захист від DDoS, боти, Zero Trust і Cloudflare One, Tunnel, мережеві сервіси, аналітика, дописи
журналу змін; README кожної стабільної версії шести пакетів і журнали змін workers-sdk. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Cloudflare documentation -- every page of developers.cloudflare.com (all products: the developer
platform, DNS, CDN and cache, security, Zero Trust, network services, the changelog posts) as a current snapshot, the
README of every stable version of wrangler, @cloudflare/workers-types, miniflare, create-cloudflare,
@cloudflare/vitest-pool-workers and its successor @cloudflare/vitest-plugin, and the changelogs of wrangler,
miniflare, create-cloudflare and @cloudflare/vitest-pool-workers from the workers-sdk repository. The site itself
carries no version. Prereleases are not here.

**Далі в [README](../instances/cloudflare/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### oracle-cloud

**Коли піднімати.** Розгортаєте на Oracle Cloud: безплатний рівень, обчислення, мережа, OKE.

**Порт** 8825, сервер `oracle-cloud-docs`. Підняти: `./df oracle-cloud serve`. Адреса: `http://127.0.0.1:8825/mcp`.

**Обсяг.** Документів: 4 318, фрагментів: 23 351.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Oracle Cloud Infrastructure (OCI) — як завести обліковий запис і що
дає безкоштовний рівень, як створити машину Ampere A1 і під'єднатися до неї по ssh, як відкрити порт у мережі, як
налаштувати політики IAM, бюджет і сповіщення, як підняти кластер Kubernetes (OKE) і балансувальник, як працювати з
CLI, SDK і REST API. Джерело — офіційна документація docs.oracle.com/iaas, лише англійською, плюс сторінка запитань
Free Tier з www.oracle.com і SDK для TypeScript `oci-sdk`. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents in English -- the Oracle Cloud Infrastructure documentation (docs.oracle.com/iaas): Getting Started, Free
Tier, Service Essentials, Compute, Networking, Block Volume, Billing and Cost Management, IAM with Identity Domains,
Kubernetes Engine (OKE), Load Balancer, Network Load Balancer, Object Storage, Bastion, Monitoring, Notifications,
Certificates, DNS, Email Delivery, the Developer Guide and Developer Tutorials, the release notes of these services,
and the TypeScript SDK oci-sdk (npm registry versions, README, changelog). Databases, AI, analytics and the other OCI
services are not here.

**Межі.**

Тут немає баз даних (Autonomous Database, MySQL HeatWave), AI й аналітики, Functions, API Gateway, Vault, Logging,
Resource Manager як розділу (лише згадки в Developer Guide), SDK для інших мов, окрім опису в Developer Guide.
Kubernetes як такий — у примірнику `kubernetes`, Docker — у `docker`, Linux — у `linux`.

**Далі в [README](../instances/oracle-cloud/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація;
Версії у відповіді; Межі, про які треба пам'ятати; Сховище сирого; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### github-actions

**Коли піднімати.** Пишете процеси CI в GitHub Actions.

**Порт** 8794, сервер `github-actions-docs`. Підняти: `./df github-actions serve`. Адреса: `http://127.0.0.1:8794/mcp`.

**Обсяг.** Документів: 1 538, фрагментів: 8 362.

**Опис.**

Тридцять четвертий примірник фабрики: захищений MCP-сервер, що відповідає на питання про GitHub Actions — CI/CD на
GitHub: синтаксис workflow, події, контексти й вирази, змінні й секрети, раннери, кеш і артефакти, environments і
деплой, OIDC, перевикористовувані workflow, власні дії, безпека. Поруч — GitHub Pages, GitHub Packages з Container
registry (ghcr.io), Dependabot для оновлення дій і ціни хвилин, а також README кожного мажору й нотатки релізів
офіційних дій і раннера. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents about GitHub Actions in English -- the Actions section of GitHub Docs (get started, concepts, how-tos,
tutorials and reference: the workflow syntax, events, contexts and expressions, variables and secrets, runners,
caching, artifacts, environments, OIDC, reusable workflows, creating actions, security), the GitHub Pages and GitHub
Packages sections (with the Container registry), the Dependabot pages on version updates and on actions, the billing
pages for Actions, the README of every major version and the release notes of the official actions (checkout,
setup-node, setup-python, setup-go, setup-java, cache, upload-artifact, download-artifact, github-script, the Pages
actions, attest-build-provenance, pnpm/action-setup and the Docker actions) and of the runner. GitHub Enterprise
Server, the REST and GraphQL APIs and third-party actions are not here.

**Межі.**

Тут немає GitHub Enterprise Server, REST і GraphQL API GitHub, самого Git, сторонніх дій поза списком, інших CI (GitLab
CI, Jenkins), а також Docker і Kubernetes як таких (окремі примірники `docker` і `kubernetes`). Розділи GitHub Docs
поза Actions, Pages, Packages і Dependabot (Codespaces, Copilot, організації) не взято.

**Далі в [README](../instances/github-actions/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація;
Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### argocd

**Коли піднімати.** Розгортаєте в Kubernetes за підходом GitOps через Argo CD.

**Порт** 8907, сервер `argocd-docs`. Підняти: `./df argocd serve`. Адреса: `http://127.0.0.1:8907/mcp`.

**Обсяг.** Документів: 4 588, фрагментів: 14 908.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Argo CD — декларативний інструмент безперервної доставки GitOps для
Kubernetes (сайт argo-cd.readthedocs.io, репозиторій argoproj/argo-cd), а також про те, що ставлять поруч із ним:
офіційний Helm-чарт `argo-cd` (argoproj/argo-helm, Artifact Hub), Argo CD Image Updater і argocd-vault-plugin. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Argo CD documentation -- the declarative GitOps continuous delivery tool for Kubernetes (site
argo-cd.readthedocs.io, repository argoproj/argo-cd): the pages of the site at the last tag of every minor of Argo CD
0.1 to 3.5 (getting started, core concepts, the user guide, the `argocd` CLI, the operator manual with installation,
high availability, SSO, RBAC, ApplicationSet, Notifications and the upgrading guides), the README, the CHANGELOG and
the GitHub releases; the README and values of the Helm chart `argo-cd` at every chart minor; the documentation and
releases of Argo CD Image Updater and of argocd-vault-plugin. The documentation of Kubernetes, Helm, Kustomize, Vault
and the other Argo projects as their own projects is not here; if something about Argo CD is not found in these
documents, it is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/argocd/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### flux

**Коли піднімати.** Розгортаєте в Kubernetes за підходом GitOps через Flux.

**Порт** 8908, сервер `flux-docs`. Підняти: `./df flux serve`. Адреса: `http://127.0.0.1:8908/mcp`.

**Обсяг.** Документів: 3 565, фрагментів: 14 715.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Flux — набір інструментів GitOps для Kubernetes від CNCF (сайт
fluxcd.io, репозиторії fluxcd/flux2, fluxcd/website і контролерів), а також про те, що ставлять поруч із ним: Flagger
(прогресивна доставка), Flux Operator з його Helm-чартами і Terraform-провайдер для Flux. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Flux documentation -- the GitOps toolkit for Kubernetes (site fluxcd.io, repositories fluxcd/flux2,
fluxcd/website and the controllers): the pages of the site in the branch of every minor of Flux 2.0 to 2.10 and the
blog, the CRD specifications, API references, README and CHANGELOG of source-controller, kustomize-controller,
helm-controller, notification-controller, image-reflector-controller, image-automation-controller and source-watcher
at every minor, the documentation of Flux 0.x from the flux2 repository, the GitHub releases of Flux; the
documentation and releases of Flagger, Flux Operator (with its Helm charts) and terraform-provider-flux. The
documentation of Kubernetes, Helm, Kustomize, SOPS and Terraform as their own projects is not here, nor Flux v1; if
something about Flux is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/flux/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### sealed-secrets

**Коли піднімати.** Зберігаєте секрети Kubernetes у git через Sealed Secrets.

**Порт** 8909, сервер `sealed-secrets-docs`. Підняти: `./df sealed-secrets serve`. Адреса: `http://127.0.0.1:8909/mcp`.

**Обсяг.** Документів: 314, фрагментів: 1 061.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Sealed Secrets: контролер Kubernetes і утиліту `kubeseal` від
Bitnami (репозиторій bitnami/sealed-secrets, раніше bitnami-labs/sealed-secrets). Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Sealed Secrets documentation -- the Kubernetes controller and the `kubeseal` tool from Bitnami
(repository bitnami/sealed-secrets): the README and the docs/ folder at the last tag of every minor 0.1 to 0.41, the
pages of the site sealed-secrets.netlify.app at every minor 0.18 to 0.41, the README of the official Helm chart at
every minor of the chart 1.13 to 2.22, the release notes and the stable GitHub releases. The documentation of
Kubernetes, Helm, Kustomize, Argo CD, Flux and SOPS as their own projects is not here; if something about Sealed
Secrets is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/sealed-secrets/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

<!-- тема: Спостереження за застосунком -->

### prometheus

**Коли піднімати.** Збираєте метрики через Prometheus, Alertmanager або prom-client.

**Порт** 8910, сервер `prometheus-docs`. Підняти: `./df prometheus serve`. Адреса: `http://127.0.0.1:8910/mcp`.

**Обсяг.** Документів: 1 390, фрагментів: 5 410.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Prometheus — систему моніторингу й базу часових рядів CNCF
(репозиторій prometheus/prometheus) — і про Alertmanager, що групує, приглушує й розсилає сповіщення
(prometheus/alertmanager). Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Prometheus documentation -- the monitoring system (repository prometheus/prometheus) and Alertmanager
(prometheus/alertmanager): the docs/ folder of the Prometheus server at the last tag of every minor 1.8 to 3.15, the
docs/ folder of Alertmanager at every minor 0.21 to 0.34, the pages of the site prometheus.io and its blog as of 24
October 2026, the stable GitHub releases of both; the exporters node_exporter, blackbox_exporter and pushgateway at
every minor; the README of the Helm charts kube-prometheus-stack and prometheus at every major; the Node.js client
prom-client and its successor @prometheus-io/client. The documentation of Grafana, Kubernetes, the Prometheus
Operator, the client libraries for other languages and other exporters as their own projects is not here; if something
about Prometheus or Alertmanager is not found in these documents, it is unlikely to be anywhere in their official
documentation.

**Далі в [README](../instances/prometheus/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### grafana

**Коли піднімати.** Будуєте панелі й сповіщення в Grafana.

**Порт** 8902, сервер `grafana-docs`. Підняти: `./df grafana serve`. Адреса: `http://127.0.0.1:8902/mcp`.

**Обсяг.** Документів: 15 441, фрагментів: 60 435.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Grafana — відкриту платформу дашбордів, візуалізації, сповіщень і
дослідження метрик, логів і трас (сайт grafana.com/docs/grafana, репозиторій grafana/grafana, реєстр npm). Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Grafana documentation -- the open-source platform for dashboards, visualization, alerting and
exploration of metrics, logs and traces (site grafana.com/docs/grafana, repository grafana/grafana, the npm registry):
the pages of docs/sources at the last tag of every minor of Grafana 2.0 to 13.2 (installation and configuration,
authentication, administration and permissions, provisioning, dashboards, variables, visualizations, transformations,
every bundled data source, alerting, Explore, the HTTP API, plugin development, the upgrade guides and "What's new"),
the README of the @grafana/* packages, the release notes of every stable release, the npm registry entries of the
@grafana/* packages, the plugin development site plugin-tools with create-plugin and plugin-e2e, the documentation of
the Scenes library 0.0 to 9.0 and the README of the grafana Helm chart 5.6.0 to 14.0.1. The documentation of
Prometheus, Loki, Tempo, Mimir, Alloy, k6 and Grafana Cloud as their own projects is not here; if something about
Grafana is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/grafana/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### loki

**Коли піднімати.** Збираєте журнали через Loki.

**Порт** 8911, сервер `loki-docs`. Підняти: `./df loki serve`. Адреса: `http://127.0.0.1:8911/mcp`.

**Обсяг.** Документів: 2 320, фрагментів: 10 756.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Grafana Loki — систему збирання логів, що індексує лише мітки
потоку, а не сам текст (репозиторій grafana/loki), — а також про те, що ставлять поруч із ним: чарт Helm `loki` для
OSS (grafana-community/helm-charts), Loki Operator і транспорти логів Node.js `pino-loki` і `winston-loki`. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Grafana Loki documentation (repository grafana/loki): the docs/sources folder of the site
grafana.com/docs/loki at the last tag of every minor 1.6 to 3.7, the plain docs/ folder of 0.1 to 1.5, the repository
README at every minor, the stable GitHub releases and the changelog of the Helm chart loki 3.0 to 7.5; the README of
the community chart loki (grafana-community/helm-charts) at every minor 7.0 to 20.0; the Loki Operator docs at every
minor 0.4 to 0.12 and its changelog; the Node.js transports pino-loki and winston-loki. The documentation of Grafana,
Grafana Alloy, Prometheus, Tempo, Mimir and Kubernetes as their own projects is not here; if something about Loki is
not found in these documents, it is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/loki/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### opentelemetry

**Коли піднімати.** Додаєте трасування й метрики через OpenTelemetry.

**Порт** 8853, сервер `opentelemetry-docs`. Підняти: `./df opentelemetry serve`. Адреса: `http://127.0.0.1:8853/mcp`.

**Обсяг.** Документів: 38 119, фрагментів: 128 459.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про OpenTelemetry — відкритий стандарт і набір інструментів для трас,
метрик, журналів подій і профілів: API і SDK мов (насамперед JavaScript для Node.js і браузера), поширення контексту й
baggage, ресурси, вибірка, експортери, протокол OTLP, семантичні домовленості, автоматична інструментація й
OpenTelemetry Collector. Документація — увесь англійський сайт opentelemetry.io з блогом і реєстром екосистеми,
специфікація кожного тегу 0.1–1.61, семантичні домовленості 1.21–1.44, файли `.proto` OTLP 0.3–1.11, opentelemetry-js
кожного випуску (README пакетів, посібники, код із TSDoc, тести, приклади, журнали змін), архівний
opentelemetry-js-api, 78 пакетів opentelemetry-js-contrib на кожному своєму випуску, Collector і contrib Collector
кожного випуску, декларативна конфігурація, OpAMP, `@vercel/otel` і реєстр npm ключових пакетів. Код спільний і лежить
у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the OpenTelemetry documentation -- the whole English site opentelemetry.io with its blog and ecosystem
registry, the specification at every tag 0.1-1.61 with the OTEPs, the semantic conventions 1.21-1.44, the OTLP .proto
files 0.3-1.11, opentelemetry-js at every release (package READMEs, guides, source with TSDoc, tests, examples,
CHANGELOGs), the archived opentelemetry-js-api, opentelemetry-js-contrib with each of its 78 packages at each of its
releases, the Collector core and contrib at every release (component READMEs, docs, CHANGELOGs), the declarative
configuration schema, OpAMP, @vercel/otel and the npm registry of key packages. Jaeger, Prometheus, Grafana and vendor
backends are not here; if something about OpenTelemetry is not found in these documents, it is unlikely to be in its
official documentation.

**Межі.**

- Сайт — знімок поточного стану, версій не має; переклади (uk, ja, zh…) не взято.
- Репозиторії SDK інших мов (Java, Python, Go, .NET…) не взято: їхні сторінки на сайті — є, коду й журналів — немає.
- Код Collector (Go) не взято: лише README компонентів, `docs/` і журнали змін.
- GitHub Releases не взято: у всіх репозиторіях вони дослівно повторюють журнали змін.
- Jaeger, Prometheus, Grafana й бекенди постачальників — поза примірником.
- Файли коду понад 150 КБ не беруться (згенеровані константи `@opentelemetry/semantic-conventions` — їх зміст є в
  самих домовленостях).
- 35 «збоїв» `build` — порожні в самому журналі записи версій (наприклад, Collector 0.146.1).

**Далі в [README](../instances/opentelemetry/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### sentry

**Коли піднімати.** Відстежуєте помилки JavaScript через Sentry.

**Порт** 8802, сервер `sentry-docs`. Підняти: `./df sentry serve`. Адреса: `http://127.0.0.1:8802/mcp`.

**Обсяг.** Документів: 7 958, фрагментів: 67 112.

**Опис.**

Сорок другий примірник фабрики: захищений MCP-сервер, що відповідає на питання про Sentry у проєктах на JavaScript і
TypeScript — підключення SDK до фреймворку, опції `Sentry.init`, помилки, трасування й вибірка, Session Replay,
профілювання, логи, cron-моніторинг, карти коду та їх завантаження, релізи, продукт sentry.io, токени, інтеграції й
REST API. Поруч — журнали змін і посібники міграції SDK, плагінів збирачів і sentry-cli та версії пакетів `@sentry/*`
з реєстру npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents about Sentry for JavaScript in English -- the JavaScript section of docs.sentry.io (the browser SDK and the
guides of every JavaScript framework and runtime: setup, options, errors, tracing, Session Replay, profiling, logs,
metrics, crons, user feedback, enriching events, source maps, migration guides, pages for older SDK lines), the
product, concepts, sentry-cli, settings, security and PII pages, the integrations and the REST API; the README,
migration guides and changelogs of the JavaScript SDK (lines 4 to 11), of the bundler plugins and of sentry-cli; the
README with every option of the Vite, webpack, Rollup and esbuild plugins; the npm registry records of the @sentry/*
packages. SDKs of other platforms and self-hosting the Sentry server are not here.

**Межі.**

Тут немає SDK інших платформ (Python, Go, Java, .NET, PHP, Ruby, Rust, Android, Apple, Flutter, React Native, Unity),
самохостингу сервера Sentry, внутрішніх пакетів (`browser-utils`, `server-utils`, `server-runtime-injection`,
`bundler-plugins`) і конфігів розробки (`eslint-config-sdk`, `eslint-plugin-sdk`, `typescript`), а також розділів сайту
про ціни, внесок у документацію й Sentry для AI-асистентів. README окремих пакетів монорепозиторію не взято: це
однакові заглушки на кілька рядків із посиланням на сайт. Нотаток релізів GitHub теж немає — вони повторюють
`CHANGELOG.md`. Самі React, Next.js, NestJS, Node.js, Vite й Express — окремі примірники.

**Далі в [README](../instances/sentry/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Межі,
про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

<!-- тема: Сайти, контент, сервіси для бізнесу -->

### wordpress

**Коли піднімати.** Будуєте або підтримуєте сайт на WordPress: хуки, Gutenberg, WP-CLI, плагіни форм.

**Порт** 8946, сервер `wordpress-docs`. Підняти: `./df wordpress serve`. Адреса: `http://127.0.0.1:8946/mcp`.

**Обсяг.** Документів: 31 404, фрагментів: 204 522.

**Опис.**

Цей примірник зібрав документацію WordPress і віддає її через сервер MCP, щоб модель відповідала за текстом
документації, а не з пам'яті. WordPress — це система керування вмістом сайту, написана мовою PHP. До неї належать REST
API (запити HTTP, якими програма читає й змінює вміст сайту), редактор блоків Gutenberg і WP-CLI (керування сайтом із
командного рядка).

**Склад (так його описано моделі, англійською).**

Documents of the WordPress documentation: the whole Code Reference (functions, classes, methods, hooks), the developer
handbooks (plugins, themes, blocks, REST API, Common APIs, coding standards, administration, Playground), the user
documentation with the page of every version, the developer notes, Learn WordPress, Gutenberg docs of every minor, the
@wordpress/* packages, WP-CLI, the Packagist and Docker entries, readme.html and the requirements of every line 1.5 to
7.1, the WordPress Importer, and the form plugins WPForms, Gravity Forms, Ninja Forms, Fluent Forms, Formidable Forms,
Forminator, SureForms, Kali Forms, JetFormBuilder, Elementor Forms and Contact Form 7. A plain number is WordPress
itself; a prefix (gutenberg-, npm-, cli-, composer-, wpcs-) marks another project. The documentation of PHP, MySQL,
React and Composer as their own projects is not here; if something about WordPress is not found in these documents, it
is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/wordpress/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### civicrm

**Коли піднімати.** Ведете контакти, внески чи членство організації через CiviCRM.

**Порт** 8950, сервер `civicrm-docs`. Підняти: `./df civicrm serve`. Адреса: `http://127.0.0.1:8950/mcp`.

**Обсяг.** Документів: 1 439, фрагментів: 12 843.

**Опис.**

Цей примірник зібрав документацію CiviCRM і віддає її через сервер MCP, щоб модель відповідала з її текстів, а не з
пам'яті. CiviCRM — це відкрита система для неприбуткових організацій: контакти, членство, внески, події й розсилки. Її
порівнюють із власною розробкою, коли вирішують, чи писати систему для асоціації самому.

**Склад (так його описано моделі, англійською).**

Documents of the CiviCRM documentation: the user, developer, system administrator and installation guides of
docs.civicrm.org, the documentation of its extensions, the release notes of every version and the Packagist record.
The guides describe the current release and carry no version.

**Далі в [README](../instances/civicrm/README.md):** Скільки цього; Що в цій теці; Звідки документація; Як підняти
сервер; Архівний режим: сервер без корпусу.

### payload

**Коли піднімати.** Будуєте сайт на CMS Payload.

**Порт** 8901, сервер `payload-docs`. Підняти: `./df payload serve`. Адреса: `http://127.0.0.1:8901/mcp`.

**Обсяг.** Документів: 3 850, фрагментів: 16 774.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Payload — відкриту headless CMS і фреймворк застосунків на
TypeScript, що встановлюється просто в застосунок Next.js (сайт payloadcms.com/docs, репозиторій payloadcms/payload,
реєстр npm). Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Payload documentation -- the open-source headless CMS and application framework for TypeScript (site
payloadcms.com/docs, repository payloadcms/payload, the npm registry): the pages of docs/ at the last tag of every
minor of payload 0.0 to 3.92 (config, collections and globals, every field type, access control, hooks,
authentication, the Local API, REST and GraphQL, queries, uploads, versions and drafts, localization, database
adapters and migrations, the admin panel and custom components, Lexical, live preview, the jobs queue, email, plugins,
TypeScript, deployment, the migration guides), the README of 44 packages, the release notes of every stable release,
the examples and templates of the repository, the npm registry, the blog of payloadcms.com and its Community Help
archive of Discord and GitHub Discussions threads. The documentation of Payload 4.0 beta, Next.js, React, MongoDB,
PostgreSQL and Lexical as their own projects is not here; if something about Payload is not found in these documents,
it is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/payload/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### sanity

**Коли піднімати.** Будуєте сайт на CMS Sanity.

**Порт** 8899, сервер `sanity-docs`. Підняти: `./df sanity serve`. Адреса: `http://127.0.0.1:8899/mcp`.

**Обсяг.** Документів: 7 888, фрагментів: 49 042.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Sanity — платформу вмісту: Sanity Studio (редактор, пакет npm
`sanity`), Content Lake (сховище документів у хмарі Sanity), мову запитів GROQ і бібліотеки JavaScript навколо них
(сайти www.sanity.io/docs і reference.sanity.io, репозиторії sanity-io/* на GitHub, реєстр npm). Код спільний і лежить
у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Sanity documentation -- Sanity Studio, the Content Lake, GROQ and the JavaScript libraries (sites
www.sanity.io/docs and reference.sanity.io, repositories sanity-io/* on GitHub, the npm registry): every page of the
docs site (Studio, schema types, Content Lake, GROQ, the HTTP API and CLI references, Visual Editing, Functions,
Blueprints, framework guides, help articles), the TypeDoc API reference, the README of every stable version of sanity,
groq, @sanity/vision, @sanity/cli, @sanity/client, next-sanity, @sanity/image-url, @sanity/visual-editing and
@portabletext/react, their npm registry entries and the GitHub release notes. The documentation of Next.js, React,
Astro and Vercel as their own projects is not here; if something about Sanity is not found in these documents, it is
unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/sanity/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### contentful

**Коли піднімати.** Будуєте сайт на CMS Contentful.

**Порт** 8904, сервер `contentful-docs`. Підняти: `./df contentful serve`. Адреса: `http://127.0.0.1:8904/mcp`.

**Обсяг.** Документів: 5 170, фрагментів: 15 194.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Contentful — headless-платформу вмісту з API (документація для
розробників contentful.com/developers/docs, репозиторії офіційних SDK та інструментів на GitHub, реєстр npm). Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Contentful documentation -- the API-first headless content platform (contentful.com/developers/docs,
the repositories of the official SDKs and tools, the npm registry): the pages of the developer documentation as they
stand now (the concepts and the data model; the reference of the Content Delivery, Content Preview, Content
Management, GraphQL, Images, User Management and SCIM APIs; the App Framework, the App SDK, webhooks; the SDK pages,
the tutorials, Compose, Experiences and Personalization), the README and documentation files of contentful.js,
contentful-management.js, contentful-cli, contentful-migration, contentful-import, contentful-export, rich-text, the
App SDK, live-preview, the Experiences SDK, create-contentful-app and the MCP server at the last tag of every minor,
their GitHub releases and the npm registry of twenty packages. The documentation of Next.js, React, Gatsby and GraphQL
as their own projects, the Help Center for editors and Forma 36 are not here; if something about Contentful is not
found in these documents, it is unlikely to be anywhere in its official developer documentation.

**Далі в [README](../instances/contentful/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### sender

**Коли піднімати.** Надсилаєте розсилки через Sender.net.

**Порт** 8945, сервер `sender-docs`. Підняти: `./df sender serve`. Адреса: `http://127.0.0.1:8945/mcp`.

**Обсяг.** Документів: 1 464, фрагментів: 21 478.

**Опис.**

Цей примірник зібрав документацію Sender.net і віддає її через сервер MCP, щоб модель відповідала за текстом
документації, а не з пам'яті. Sender.net — це сервіс email- і SMS-розсилок. Програми працюють із ним через REST API:
це звичайні запити HTTP на адресу `https://api.sender.net/v2/`.

**Склад (так його описано моделі, англійською).**

Documents of the Sender.net documentation -- the email and SMS marketing service and its REST API v2: the whole API
reference (api.sender.net), the help center, the product pages, blog and template gallery of sender.net, the npm
package @sender-net/sender-transactional-nodejs, the Packagist package sendernet/sender-transactional-php, and the
code of the official PrestaShop module and WordPress plugin. The site pages carry no version: the API is one live
service. The documentation of Mailchimp, Shopify, WooCommerce, WordPress and other tools as their own projects is not
here; if something about Sender.net is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Далі в [README](../instances/sender/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### resend

**Коли піднімати.** Надсилаєте пошту через сервіс Resend.

**Порт** 8896, сервер `resend-docs`. Підняти: `./df resend serve`. Адреса: `http://127.0.0.1:8896/mcp`.

**Обсяг.** Документів: 559, фрагментів: 3 045.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `react-email-docs` (8897).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Resend — API надсилання листів для розробників — і його SDK для
Node.js, пакет npm `resend` (сайт resend.com/docs, репозиторій resend/resend-node, реєстр npm). Код спільний і лежить
у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Resend documentation -- the email API for developers and its Node.js SDK, the npm package resend
(site resend.com/docs, repository resend-node, the npm registry): every page of the site (sending with Node.js and
other runtimes, the REST API reference with the Node.js, cURL and CLI examples, webhooks, the dashboard, domains and
DNS, deliverability, guides), the README of every resend version 0.1 to 6.34, the npm registry and the release notes
of resend-node. The documentation of React Email, Next.js, Node.js and nodemailer as their own projects is not here;
if something about Resend is not found in these documents, it is unlikely to be anywhere in its official
documentation. This set is part of the Resend family: resend-docs (this one: the Resend API, dashboard, webhooks,
deliverability and the Node.js SDK) and react-email-docs (React Email: the components, render() and the CLI for
building the emails) are meant to be connected together -- when a question belongs to the other member, name its
server.

**Далі в [README](../instances/resend/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Версії; Родина Resend: піднімати разом; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### react-email

**Коли піднімати.** Верстаєте листи через React Email.

**Порт** 8897, сервер `react-email-docs`. Підняти: `./df react-email serve`. Адреса: `http://127.0.0.1:8897/mcp`.

**Обсяг.** Документів: 654, фрагментів: 1 517.

**Родина.** Цей примірник відповідає не на все сам, тому разом із ним піднімають: `resend-docs` (8896).

**Опис.**

Захищений MCP-сервер, що відповідає на питання про React Email — бібліотеку для верстки HTML-листів на React і
TypeScript від команди Resend (сайт react.email/docs, репозиторій resend/react-email, реєстр npm) — за документацією
кожної мінорної версії, пакетами й журналами змін. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the React Email documentation -- the library for building HTML emails with React and TypeScript (site
react.email/docs, repository resend/react-email, the npm registry): the site at the last release of every react-email
minor 2.1 to 6.11 (setup, components and their props, render(), the CLI and the preview server, integrations with
email providers, internationalization, the visual editor), the README of every @react-email/components and
@react-email/render version, the npm registry of five packages and the changelogs of seven. The documentation of
Resend itself, React, Tailwind CSS and the email providers as their own projects is not here; if something about React
Email is not found in these documents, it is unlikely to be anywhere in its official documentation. This set is part
of the Resend family: resend-docs (the Resend API, dashboard, webhooks, deliverability and the Node.js SDK) and
react-email-docs (this one: React Email: the components, render() and the CLI for building the emails) are meant to be
connected together -- when a question belongs to the other member, name its server.

**Далі в [README](../instances/react-email/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Родина Resend: піднімати разом; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### uploadthing

**Коли піднімати.** Приймаєте файли від користувачів через UploadThing.

**Порт** 8900, сервер `uploadthing-docs`. Підняти: `./df uploadthing serve`. Адреса: `http://127.0.0.1:8900/mcp`.

**Обсяг.** Документів: 1 137, фрагментів: 1 790.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про UploadThing — сервіс і бібліотеку завантаження файлів для
фулстек-застосунків на TypeScript (сайт docs.uploadthing.com, репозиторій pingdotgg/uploadthing, реєстр npm). Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the UploadThing documentation -- the file upload service and library for full-stack TypeScript apps (site
docs.uploadthing.com, repository pingdotgg/uploadthing, the npm registry): the pages of the site at the last tag of
every minor of uploadthing 3.0 to 7.7 (getting started with every framework, file routes, uploading and working with
files, backend adapters, auth and security, error handling, regions and ACL, theming, the API reference of the server,
the client, UTApi and the React, Solid, Svelte, Vue and Expo packages, the OpenAPI spec, the v7 migration guide, the
FAQ and the blog), the changelogs of ten packages, the npm registry and the examples of the repository. The
documentation of Next.js, React, Nuxt, Express and S3 as their own projects is not here; if something about
UploadThing is not found in these documents, it is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/uploadthing/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### stripe

**Коли піднімати.** Приймаєте платежі через Stripe.

**Порт** 8863, сервер `stripe-docs`. Підняти: `./df stripe serve`. Адреса: `http://127.0.0.1:8863/mcp`.

**Обсяг.** Документів: 14 499, фрагментів: 113 886.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Stripe — прийом платежів, підписки, рахунки, податки, Connect,
виплати й гроші в коді. Документація — сайт docs.stripe.com цілком англійською: посібники з усіма варіантами
інтеграцій (Checkout, Elements, мобільні iOS і Android, Direct API) і прикладами сервера сімома мовами, довідник API,
журнал змін API, довідник Stripe.js; повна специфікація OpenAPI (v1 і v2) — кожен ресурс і кожен об'єкт з типами
полів; для кожного стабільного випуску SDK Node.js, Stripe.js, React Stripe.js, React Native і Connect.js — README і
MIGRATING з репозиторію, для SDK Python, Go, Ruby, Java, .NET, PHP, CLI, iOS і Android — те саме з останнього тегу
кожної мінорної лінії; нотатки релізів усіх п'ятнадцяти репозиторіїв; код найновіших JS-SDK; таблиці версій з npm,
PyPI, RubyGems, Packagist, NuGet, Maven і CocoaPods. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Stripe documentation -- the whole English site docs.stripe.com (guides with server code in Node.js,
Python, Go, Ruby, Java, .NET and the Stripe CLI, every integration variant, the API reference, the API changelog of
every dated API version, the Stripe.js reference), the OpenAPI specification, the README and release notes of every
stable release of the JavaScript, React, React Native, Python, Go, Ruby, Java, .NET, PHP, CLI, iOS and Android SDKs,
the code and types of the newest JavaScript SDKs, and version tables from npm, PyPI, RubyGems, Packagist, NuGet, Maven
Central and CocoaPods. 0, python-16.0), API versions the date (api-2025-03-31.basil). If something about Stripe is not
found in these documents, it is unlikely to be in its official documentation.

**Межі.**

- Сайт — англійською. Переклади сайту не взято.
- Код на сторінках сайту — сімома мовами: Node.js, Python, Go, Ruby, Java, .NET і Stripe CLI. PHP і curl не взято:
  PHP дають README, релізи й Packagist, curl — довідник API. Нативний код iOS і Android приходить варіантами
  сторінок («Mobile: iOS»), а не параметром мови.
- Код — лише JS-SDK найновіших тегів, без тестів. Код SDK інших мов не взято: методи дають довідник API й OpenAPI.
- Лише стабільні випуски: альфи, беты, rc і передрелізи з дефісом у номері не взято, у таблицях реєстрів їх лише
  пораховано.
- Не взято: документацію Dokka stripe-android, довідники stripe.dev, pkg.go.dev (теги й релізи stripe-go дають те
  саме), блог stripe.com. У Maven дат випуску немає — лише перелік версій.
- Варіант Checkout «Stripe-hosted page» сторінки build-subscriptions майже порожній на боці Stripe: вступ і заголовок.

**Далі в [README](../instances/stripe/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### payments-pt

**Коли піднімати.** Приймаєте платежі в Португалії через ifthenpay, Easypay, Eupago чи SIBS: MB WAY, Multibanco, дебет.

**Порт** 8948, сервер `payments-pt-docs`. Підняти: `./df payments-pt serve`. Адреса: `http://127.0.0.1:8948/mcp`.

**Обсяг.** Документів: 1 330, фрагментів: 11 182.

**Опис.**

Цей примірник зібрав документацію чотирьох португальських постачальників онлайн-платежів і віддає її через сервер MCP,
щоб модель відповідала з їхніх текстів, а не з пам'яті. Постачальник платежів — це компанія, яка приймає гроші від
покупця через MB WAY, Multibanco, картку чи дебет і перераховує їх продавцеві. Тут є ifthenpay, Easypay, Eupago і
SIBS.

**Склад (так його описано моделі, англійською).**

Documents of four Portuguese payment providers: ifthenpay, Easypay, Eupago and SIBS: API references, guides, help
center, site pages with prices, blogs, press news, plugin READMEs and SDK packages. Prices are as shown on the fetch
date. Stripe is not here.

**Далі в [README](../instances/payments-pt/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Як підняти сервер; Архівний режим: сервер без корпусу.

### rgpd

**Коли піднімати.** Обробляєте персональні дані в Португалії: RGPD, закони, рішення CNPD, настанови EDPB.

**Порт** 8947, сервер `rgpd-docs`. Підняти: `./df rgpd serve`. Адреса: `http://127.0.0.1:8947/mcp`.

**Обсяг.** Документів: 126, фрагментів: 3 257.

**Опис.**

Цей примірник зібрав закони про захист персональних даних, що діють у Португалії, і віддає їх через сервер MCP, щоб
модель відповідала з текстів законів, а не з пам'яті. Головне питання, заради якого він існує: кому можна писати листи
й на якій підставі. Тексти не є юридичною консультацією: там, де відповідь залежить від фактів, рішення лишається за
юристом або за CNPD. Одна й та сама постанова ЄС має дві абревіатури. Англійською вона називається GDPR (General Data
Protection Regulation), португальською RGPD (Regulamento Geral sobre a Proteção de Dados). Обидві назви означають
Регламент (ЄС) 2016/679, тому в корпусі лежать обидві мовні версії, і запит можна писати будь-якою з двох мов.

**Склад (так його описано моделі, англійською).**

Documents of data protection law for Portugal: the RGPD/GDPR in Portuguese and English, Lei 58/2019, Lei 41/2004,
Decreto-Lei 7/2004, Directive 2002/58/EC, the directives, regulations, deliberations since 2018, older guidance and
pages of the CNPD, and three EDPB guidelines. Document versions are not tracked: each law is in one wording, stated in
the title of its document. Tax law, payments and the law of other countries are not here; if something is not found in
these documents, it does not follow that the law is silent on it.

**Далі в [README](../instances/rgpd/README.md):** Що тут є; Що треба знати про тексти; Що не взято; Що в цій теці;
Звідки документація; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Як підняти сервер.

<!-- тема: Штучний інтелект -->

### anthropic-api

**Коли піднімати.** Викликаєте Claude через API: моделі, ціни, інструменти, кеш запитів.

**Порт** 8860, сервер `anthropic-api-docs`. Підняти: `./df anthropic-api serve`. Адреса: `http://127.0.0.1:8860/mcp`.

**Обсяг.** Документів: 6 316, фрагментів: 92 404.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про API Anthropic — виклик моделей Claude (Haiku, Sonnet, Opus, Fable)
через Messages API та офіційні SDK. Документація — сайт platform.claude.com/docs цілком англійською (моделі й ціни,
ліміти, помилки, Messages API, потокова видача, thinking і effort, виклик інструментів, кешування промпту, пакетна
обробка, файли, структуровані відповіді, Managed Agents, Admin API, хмарні платформи, журнали змін і системні промпти,
HTTP-довідник API) разом із довідником API в редакціях Python і TypeScript; для кожного стабільного випуску SDK
TypeScript, Python, Go, Ruby, C# і CLI `ant` — README, `api.md`, helpers і MIGRATION з репозиторію та нотатки релізів;
код і приклади найновіших SDK TypeScript і Python; таблиці версій і README з npm і PyPI; рецепти claude-cookbooks. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Anthropic API documentation -- the whole English site platform.claude.com/docs (models and pricing,
Messages API, tool use, prompt caching, batches, thinking, structured outputs, rate limits, errors, Managed Agents,
Admin API, cloud platforms, release notes, the API reference as HTTP, Python and TypeScript), the README, api.md and
helper pages of the TypeScript, Python, Go, Ruby and C# SDKs and of the ant CLI for every stable release with their
release notes, the source code and examples of the newest TypeScript and Python SDK, the npm and PyPI version tables
and READMEs, and the claude-cookbooks notebooks. 135, python-1.15, go-1.82). If something about the Anthropic API is
not found in these documents, it is unlikely to be in its official documentation.

**Межі.**

- Сайт — англійською. Переклади (11 мов по 288 сторінок, серед них російська) коротші за англійську версію (783
  сторінки), їх не взято.
- Довідник API в редакціях Go, Ruby, C#, Java, PHP і CLI не взято. Методи цих SDK дає HTTP-довідник з тими самими
  описами, `api.md` (Go) і README з тегів.
- Код — лише найновіших TypeScript і Python SDK, без тестів. Старі версії видно з `api.md`, README й релізів кожного
  тегу.
- Лише стабільні випуски: альфи й беты Go, Ruby і `0.34.0-alpha.0` TypeScript не взято.
- Не взято: Claude Code (code.claude.com), Claude Agent SDK (`@anthropic-ai/claude-agent-sdk`, `claude-agent-sdk`),
  репозиторії `skills`, `claude-quickstarts`, а також власний MCP-сервер документації platform.claude.com/docs/mcp.
- claude-cookbooks не має тегів: це знімок гілки main на 17.10.2026. Частина зошитів написана під старі моделі й
  ціни: число з рецепта звіряти зі сторінками сайту.

**Далі в [README](../instances/anthropic-api/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### claude-code

**Коли піднімати.** Налаштовуєте Claude Code, Agent SDK, навички чи плагіни.

**Порт** 8926, сервер `claude-code-docs`. Підняти: `./df claude-code serve`. Адреса: `http://127.0.0.1:8926/mcp`.

**Обсяг.** Документів: 1 795, фрагментів: 17 824.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Claude Code — агента Anthropic для програмування в терміналі, IDE,
застосунку для комп'ютера й браузері: налаштування й дозволи, `CLAUDE.md` і пам'ять, скіли, субагенти, хуки, MCP,
плагіни й маркетплейси, моди, довідник CLI, команд і змінних оточення, Agent SDK, GitHub Actions. Документація — сайт
code.claude.com/docs англійською цілком, журнал змін Claude Code за версіями, Agent SDK для TypeScript і Python,
claude-code-action, Claude Tag (Claude у Slack), офіційні скіли й плагіни Anthropic і довідник спільноти Claude Code
Handbook російською. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі
дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Claude Code documentation -- the whole English site code.claude.com/docs (surfaces, memory and
context, skills, subagents, hooks, MCP, plugins, mods, settings and permissions, administration, CLI reference, Agent
SDK, What's New, changelog), the Claude Code CHANGELOG by version with the npm version table, the Agent SDK for
TypeScript and Python (changelogs, READMEs, examples, npm and PyPI tables), claude-code-action v1.0 and v0.0, the
anthropics/claude-code repository examples and mods, Claude Tag (Claude in Slack), Anthropic's official skills, the
claude-plugins-official marketplace and the community Claude Code Handbook in Russian. 1), the rest carry their
package name (agent-sdk-ts-0.3, agent-sdk-py-0.2, action-1.0). If something about Claude Code is not found in these
documents, it is unlikely to be in its official documentation.

**Далі в [README](../instances/claude-code/README.md):** Навіщо окремий примірник; Скільки цього; Довідник російською:
кирилиця в пошуку; Що в цій теці; Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### vercel-ai-sdk

**Коли піднімати.** Будуєте застосунок із моделями через AI SDK від Vercel.

**Порт** 8898, сервер `vercel-ai-sdk-docs`. Підняти: `./df vercel-ai-sdk serve`. Адреса: `http://127.0.0.1:8898/mcp`.

**Обсяг.** Документів: 25 369, фрагментів: 47 870.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про AI SDK від Vercel — набір TypeScript для застосунків і агентів на
мовних моделях (сайт ai-sdk.dev, репозиторій vercel/ai, реєстр npm) — за документацією кожної мінорної версії,
пакетами й журналами змін. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає
самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the AI SDK documentation -- the TypeScript toolkit by Vercel for applications and agents on language
models (site ai-sdk.dev, repository vercel/ai, the npm registry): the site at the last release of every `ai` minor 2.1
to 7.0 (AI SDK Core, AI SDK UI, RSC, agents, the API reference, migration guides, troubleshooting, the cookbook and
the providers), the README of the last release of every minor of `ai` and of 88 `@ai-sdk/*` packages, the changelogs
of all 89 packages and their npm registry. The model providers' own APIs, React, Next.js, Vue, Svelte, Zod and the
Vercel platform as their own projects are not here; if something about the AI SDK is not found in these documents, it
is unlikely to be anywhere in its official documentation.

**Далі в [README](../instances/vercel-ai-sdk/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Версії; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude
Code.

### ollama

**Коли піднімати.** Запускаєте локальні моделі через Ollama.

**Порт** 8854, сервер `ollama-docs`. Підняти: `./df ollama serve`. Адреса: `http://127.0.0.1:8854/mcp`.

**Обсяг.** Документів: 1 710, фрагментів: 5 693.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Ollama — локальний запуск великих мовних моделей (і хмару Ollama) з
HTTP API на порту 11434, CLI, форматом Modelfile та офіційними клієнтами для JavaScript і Python. Документація — сайт
docs.ollama.com цілком (можливості, CLI, Modelfile, довжина контексту, Linux/macOS/Windows/Docker, підтримка GPU, FAQ
зі змінними сервера, інтеграції, довідник API з полями кожного ендпоінта, сумісність з OpenAI й Anthropic), а для
кожного стабільного випуску ollama/ollama v0.0.1–v0.40.6 — тека `docs/`, README, код Go `api/` і `envconfig/` з
тестами і нотатки релізів; для кожного стабільного випуску клієнтів ollama-js і ollama-python — код, тести, приклади,
релізи, README з npm і PyPI. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека
тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Ollama documentation -- the site docs.ollama.com (capabilities, CLI, Modelfile, context length,
Linux, macOS, Windows, Docker, GPU support, FAQ, troubleshooting, integrations, the API reference and OpenAI and
Anthropic compatibility), and for every stable release of ollama/ollama the docs/ folder, the README, the Go code of
api/ and envconfig/ with tests and the GitHub release notes; for every stable release of the client libraries
ollama-js and ollama-python the README, source code, tests, examples and release notes, plus their version tables on
npm and PyPI. 40), client lines carry the package name (ollama-js-0.6, ollama-python-0.6). If something about Ollama
is not found in these documents, it is unlikely to be in its official documentation.

**Межі.**

- Лише стабільні випуски: 439 передрелізних і службових тегів ollama/ollama (432 rc, 7 ci) не взято.
- Сторінки моделей на ollama.com/library (що вміє модель, її шаблон, ліцензія) — не документація Ollama, сюди не
  взято. Так само llama.cpp, на якому Ollama стоїть.
- Код Go — лише `api/` і `envconfig/`: сервер (`server/`, `llm/`, `ml/`) не взято. Тека `envconfig/` з'явилася в
  0.1.39; для старіших версій змінні середовища дає лише FAQ.
- `docs/openapi.yaml` окремо не взято: чинну специфікацію сайт розгортає в сторінки ендпоінтів, а для старих версій
  довідник — `api.md`.

**Далі в [README](../instances/ollama/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

<!-- тема: Обробка файлів -->

### ffmpeg

**Коли піднімати.** Обробляєте відео чи аудіо через FFmpeg.

**Порт** 8813, сервер `ffmpeg-docs`. Підняти: `./df ffmpeg serve`. Адреса: `http://127.0.0.1:8813/mcp`.

**Обсяг.** Документів: 1 291, фрагментів: 11 668.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про FFmpeg — набір програм командного рядка `ffmpeg`, `ffprobe` і
`ffplay` та бібліотек libav* для читання, перетворення, перепакування й аналізу відео та аудіо — за документацією всіх
гілок випусків від 0.6 до 9.0: посібниками з репозиторію на тегах випусків, журналом змін, сторінками ffmpeg.org і
обгортками npm. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані
домену. Загальний устрій фабрики — у [../../README.md](../README.md). Що таке ffprobe, коротко: програма з набору
FFmpeg, що відкриває медіафайл, нічого в ньому не змінюючи, і друкує, як він улаштований — контейнер (MP4, MKV…),
доріжки, кодеки, роздільність, тривалість, бітрейт, а на вимогу й пакети та кадри — текстом, JSON, XML чи CSV. Її
«брат» `ffmpeg` перетворює й перепаковує файли: наприклад, `ffmpeg -i in.mp4 -c copy -movflags +faststart out.mp4`
переносить службовий блок `moov` на початок файла, щоб браузер міг почати відтворення й перемотування, не тягнучи
спершу кінець файла.

**Склад (так його описано моделі, англійською).**

Documents of the FFmpeg documentation -- every manual in the doc/ folder of the FFmpeg repository at the newest stable
tag of each release branch from 0.6 to 9.0 (ffmpeg, ffprobe, ffplay, ffserver, the utilities, codecs, bitstream
filters, formats with every muxer and demuxer, protocols, devices, filters, scaler and resampler manuals, the libav*
library pages, the general documentation of supported formats and codecs, the FAQ and the developer guides), the XML
schema of the ffprobe output; the Changelog entry of every stable release found in the branch changelogs; the
ffmpeg.org news, download, security, legal and about pages; and the README and npm registry history of the npm
wrappers ffprobe-static, @ffprobe-installer/ffprobe, fluent-ffmpeg, ffmpeg-static and @ffmpeg-installer/ffmpeg. The C
API reference (Doxygen), the community wiki (trac.ffmpeg.org), the documentation of the codecs' own libraries (x264,
x265, libvpx) and of the operating system packages are not here; if something about FFmpeg is not found in these
documents, it is unlikely to be anywhere in its official manuals.

**Межі.**

Довідника C API (Doxygen, ffmpeg.org/doxygen), вікі спільноти (trac.ffmpeg.org), документації зовнішніх бібліотек
кодеків (x264, x265, libvpx, libaom) і пакетів операційних систем тут немає. Пакет Debian `ffmpeg` несе ті самі
man-сторінки, зібрані з тих самих `.texi`, тож окремо не береться: Debian 12 bookworm дає FFmpeg 5.1, Debian 13 trixie
— 7.1, Ubuntu 24.04 — 6.1, і ці гілки в корпусі є. Код бібліотек не входить — лише документація.

**Далі в [README](../instances/ffmpeg/README.md):** Скільки цього; Що в цій теці; Звідки документація; Межі, про які
треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу; Сервер під Claude Code.

### tesseract

**Коли піднімати.** Розпізнаєте текст на зображеннях через Tesseract.

**Порт** 8858, сервер `tesseract-docs`. Підняти: `./df tesseract serve`. Адреса: `http://127.0.0.1:8858/mcp`.

**Обсяг.** Документів: 1 662, фрагментів: 5 704.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Tesseract OCR — рушій розпізнавання тексту на зображеннях
(командний рядок `tesseract`, C++ API `TessBaseAPI` і C API, мовні моделі tessdata, навчання й донавчання LSTM) — і
про обгортки над ним: OCRmyPDF (текстовий шар для сканів PDF через Tesseract, Ghostscript і pikepdf), tesseract.js
(Tesseract у WebAssembly для браузера й Node), pytesseract і tesserocr (Python), node-tesseract-ocr (Node).
Документація — сайт tesseract-ocr.github.io/tessdoc цілком, а для кожного стабільного випуску tesseract 1.03–5.5.3 —
сторінки man, README, публічні заголовки API, файли конфігурацій, ChangeLog і релізи; tesstrain і README репозиторіїв
tessdata; для кожного стабільного випуску обгорток — документація, код API, нотатки випусків, README з npm і PyPI. Код
спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний
устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the Tesseract OCR documentation -- the site tesseract-ocr.github.io/tessdoc (installation, command-line
usage, improving quality, input formats, language data, training for 3.x, 4.x and 5.x, VGSL, C++ API examples, FAQ),
and for every stable release of tesseract-ocr/tesseract the man pages (tesseract, lstmtraining, combine_tessdata,
text2image, unicharset and the other tools), the README, the public C and C++ API headers, the ChangeLog and the
GitHub release notes; the tesstrain README, Makefile and scripts; the READMEs and config files of tessdata,
tessdata_best and tessdata_fast; for every stable release of OCRmyPDF, tesseract.js, pytesseract, tesserocr and
node-tesseract-ocr their documentation, API code, release notes and README, plus their version tables on npm and PyPI.
5), the wrappers carry the package name (ocrmypdf-17, tesseract.js-6, pytesseract-0.3, tesserocr-2.11). If something
about Tesseract or these wrappers is not found in these documents, it is unlikely to be in their official
documentation.

**Межі.**

- Лише стабільні випуски: 34 передрелізні й службові теги tesseract (rc, alpha, beta, dev, `1.04b`) не взято.
- Самі моделі `.traineddata` (гігабайти) і словники `langdata_lstm` не взято: є README репозиторіїв і перелік мов і
  скриптів на сайті й у man.
- Довідник tessapi (Doxygen) окремо не взято: він генерується з тих самих заголовків, що лежать тут з коментарями.
- Leptonica, Ghostscript, pikepdf, unpaper і jbig2 — лише в межах того, що про них каже документація OCRmyPDF і
  Tesseract; Ghostscript, qpdf і pikepdf мають власну документацію в примірнику doc-tools.
- README tesseract.js 1.0.0 (лише заголовок) і 1.0.9 (tarball реєстр не віддає) пропущено.

**Далі в [README](../instances/tesseract/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

### libreoffice

**Коли піднімати.** Перетворюєте документи через LibreOffice без вікна або працюєте з UNO API.

**Порт** 8856, сервер `libreoffice-docs`. Підняти: `./df libreoffice serve`. Адреса: `http://127.0.0.1:8856/mcp`.

**Обсяг.** Документів: 61 986, фрагментів: 81 180.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про LibreOffice — офісний пакет (Writer, Calc, Impress, Draw, Math,
Base) і конвертер документів без вікна (`soffice --headless --convert-to`). Документація — уся англійська довідка
help.libreoffice.org для кінцевого випуску кожної лінії 3.3–26.8, текст `soffice --help` кожної лінії, оголошення
кожного фільтра імпорту й експорту та кожного типу файла, довідник UNO API (те, з чого генерується
api.libreoffice.org), посібник розробника (Developer's Guide), release notes, бюлетені безпеки, а також обгортки для
конвертації: libreoffice-convert і libreoffice-file-converter (npm), unoserver і unoconv (PyPI) — README кожної
версії, код, тести й журнали змін. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the LibreOffice documentation -- the LibreOffice Help (help.libreoffice.org) of every line 3.3-26.8, the
text of soffice --help, the declarations of every import and export filter and file type, the UNO API reference
(api.libreoffice.org: offapi and udkapi IDL), the Developer's Guide, the release notes, the security advisories, and
the conversion wrappers libreoffice-convert and libreoffice-file-converter (npm), unoserver and unoconv (PyPI). 8,
7.6), the wrappers carry their name (unoserver-3.7). If something about LibreOffice is not found in these documents,
it is unlikely to be in its official documentation.

**Межі.**

- Довідка — англійська; переклади живуть в іншому репозиторії й не взяті.
- Посібники Getting Started, Writer, Calc… (books.libreoffice.org) не взято: вони про роботу в редакторах.
- UNO API — файли IDL, з яких генерується api.libreoffice.org; самі сторінки Doxygen і довідник C++
  (docs.libreoffice.org) не взято. Посилання IDL ведуть на GitHub.
- Сім файлів IDL без жодного тексту (лише `#include` чи порожній модуль) документами не стали.
- Docker-образи й Gotenberg — не тут.

**Далі в [README](../instances/libreoffice/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці;
Звідки документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### doc-tools

**Коли піднімати.** Обробляєте файли через poppler та інші інструменти для PDF і документів.

**Порт** 8857, сервер `doc-tools-docs`. Підняти: `./df doc-tools serve`. Адреса: `http://127.0.0.1:8857/mcp`.

**Обсяг.** Документів: 17 963, фрагментів: 63 582.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про файлові інструменти командного рядка й бібліотеки, якими
перевіряють, перетворюють і рендерять документи й зображення: poppler (`pdfinfo`, `pdftotext`, `pdftoppm`,
`pdftocairo`, `pdfimages` і решта poppler-utils), librsvg з `rsvg-convert`, `file` і libmagic, ImageMagick 6 і 7,
img2pdf, Ghostscript, qpdf і pikepdf, ExifTool, resvg і CairoSVG. До кожного — їхні обгортки для Node.js (npm) і
Python (PyPI) та сторінки man так, як їх ставить apt в Ubuntu 22.04, 24.04 і 26.04. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the file tools documentation -- poppler (the man pages of pdfinfo, pdftotext, pdftoppm, pdftocairo,
pdfimages, pdffonts, pdfseparate, pdfunite, pdfsig, pdftohtml, pdftops, pdfdetach and pdfattach for every stable
release, NEWS, the API reference for GLib, Qt5, Qt6 and C++), librsvg (the rsvg-convert man page, docs and developer
docs, the C and Rust API, NEWS), file and libmagic (file(1), magic(5), libmagic(3) for every release, the ChangeLog,
the Magdir rules, the Python bindings), ImageMagick 6 and 7 (the imagemagick.org site of every release line with the
MagickCore and MagickWand API, the current site, man pages, policy.xml and delegates.xml, the ChangeLog), img2pdf,
Ghostscript (the docs of every release 6.0-10.x, News, man pages), qpdf (the manual of every release, ChangeLog, the C
and C++ headers) and pikepdf, ExifTool (exiftool.org with the tag tables of every production release, Changes), resvg
and CairoSVG; their Node.js wrappers (node-poppler, pdf2pic, gm, magick-wasm, file-type, mmmagic, wasmagic, resvg-js,
exiftool-vendored, node-qpdf2 …) and Python wrappers (pdf2image, python-poppler, pdftotext, Wand, python-magic,
file-magic, pikepdf, PyExifTool, CairoSVG, ghostscript) with READMEs, code and npm/PyPI version tables, and the Ubuntu
22.04, 24.04 and 26.04 man pages of all these tools. 10, imagemagick-7.1, ghostscript-10.08, ubuntu-24.04). If
something about these tools is not found in these documents, it is unlikely to be in their official documentation.

**Межі.**

- API poppler (glib, Qt5, Qt6, C++) — лише чинний стан сайту, без версій: сайт будується з master.
- README pdf-poppler не взято: tarball пакета з вкладеними бінарниками poppler більший за 50 МБ; таблиця версій є.
- Код ядер на C і C++ (poppler, ImageMagick, Ghostscript) не взято — лише документацію, заголовки qpdf і librsvg.
- `magick-wasm` — код лише найновішого випуску: `magick-image.ts` — 190 КБ на кожен із 44 випусків.
- exiftool-vendored — код останнього випуску кожної мажорної лінії, без згенерованого `Tags.ts` (532 КБ).
- darwinsys.com (сайт file) на час збирання не відповідав; змісту там — одна сторінка посилань.

**Далі в [README](../instances/doc-tools/README.md):** Навіщо окремий примірник; Скільки цього; Що в цій теці; Звідки
документація; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання корпусу;
Сервер під Claude Code.

<!-- тема: Блокчейн і біржі -->

### wagmi

**Коли піднімати.** Підключаєте гаманець у застосунку React через Wagmi.

**Порт** 8827, сервер `wagmi-docs`. Підняти: `./df wagmi serve`. Адреса: `http://127.0.0.1:8827/mcp`.

**Обсяг.** Документів: 4 965, фрагментів: 16 981.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Wagmi — бібліотеку від wevm для фронтенду застосунків на Ethereum:
як підключити гаманець, перемкнути мережу, прочитати баланс, блок чи транзакцію, прочитати смартконтракт і записати в
нього, надіслати транзакцію й дочекатися її квитанції, підписати повідомлення, налаштувати кеш TanStack Query і
рендеринг на сервері, згенерувати типізовані хуки з ABI контрактів. Джерела — репозиторій wevm/wagmi на GitHub (з
нього збирається сайт wagmi.sh) і реєстр npm, лише англійською. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Wagmi documentation -- the site of every stable release (3.x on wagmi.sh, 2.x on
2.x.wagmi.sh, 1.x on 1.x.wagmi.sh, 0.x from the repository) with the React hooks, Vue composables, Solid primitives,
@wagmi/core actions, connectors, transports, the CLI and the Tempo hooks and actions, the changelog of every package
(wagmi, @wagmi/core, @wagmi/connectors, @wagmi/vue, @wagmi/solid, @wagmi/cli, create-wagmi) and their npm version
tables. Only stable releases are here. If something about Wagmi is not found in these documents, it is unlikely to be
anywhere in its official documentation.

**Межі.**

Тут немає viem (низькорівнева бібліотека, на якій стоїть Wagmi; сторінки Wagmi лише посилаються на її дії), ethers.js,
RainbowKit, ConnectKit, Reown AppKit, SDK MetaMask і WalletConnect, Solidity, Foundry і Hardhat як таких, документації
мережі Tempo поза хуками Wagmi, передрелізів (canary). TanStack Query як такий — у примірнику `tanstack-query`, React —
у `react`.

**Далі в [README](../instances/wagmi/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Версії у
відповіді; Межі, про які треба пам'ятати; Сховище сирого; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### viem

**Коли піднімати.** Звертаєтеся до Ethereum із TypeScript через Viem.

**Порт** 8828, сервер `viem-docs`. Підняти: `./df viem serve`. Адреса: `http://127.0.0.1:8828/mcp`.

**Обсяг.** Документів: 4 057, фрагментів: 11 096.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Viem — бібліотеку TypeScript від wevm для роботи з Ethereum: як
створити клієнт і транспорт, прочитати баланс, блок, транзакцію чи журнали подій, прочитати смартконтракт, перевірити
виклик симуляцією й записати в нього, надіслати транзакцію й дочекатися її квитанції, підписати повідомлення чи
типізовані дані, перевести одиниці (ether, gwei, wei), закодувати й розкодувати ABI, знайти адресу за іменем ENS,
працювати з L2 (OP Stack, ZKsync), смарт-акаунтами й EIP-7702. Джерела — репозиторій wevm/viem на GitHub (з нього
збирається сайт viem.sh) і реєстр npm, лише англійською. Код спільний і лежить у `../../engine/`, `../../server/` та
`../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Viem documentation -- the site of every stable release (2.x on viem.sh, 1.x on v1.viem.sh,
0.x from the repository) with clients, transports, actions, contracts, accounts, chains, ABI, utilities, ENS, SIWE,
EIP-7702 and the OP Stack, ZKsync, Account Abstraction, Experimental, Circle USDC, Tempo and Tokens sections, the
repository examples of each major line, the changelog of every version and the npm version table. Only stable releases
are here. If something about Viem is not found in these documents, it is unlikely to be anywhere in its official
documentation.

**Межі.**

Тут немає Wagmi (хуки React поверх Viem — примірник `wagmi`), ethers.js і web3.js як таких (є лише сторінка про перехід
з ethers.js), бібліотек Ox і ABIType як таких, Solidity, Foundry й Anvil, Hardhat, SDK гаманців, документації мереж
Tempo, OP Stack і ZKsync поза діями Viem для них, передрелізів (canary, 3.0.0-next).

**Далі в [README](../instances/viem/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Версії у
відповіді; Межі, про які треба пам'ятати; Сховище сирого; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### foundry

**Коли піднімати.** Пишете й тестуєте смартконтракти через Foundry.

**Порт** 8829, сервер `foundry-docs`. Підняти: `./df foundry serve`. Адреса: `http://127.0.0.1:8829/mcp`.

**Обсяг.** Документів: 4 424, фрагментів: 13 822.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про Foundry — набір інструментів на Rust від foundry-rs для
смартконтрактів Ethereum: forge (збирання, тести, фазинг- та інваріантні тести, форки, покриття, газ, скрипти
Solidity, розгортання й верифікація, лінтер, форматер), cast (виклики, транзакції, гаманці, ABI з командного рядка),
anvil (локальний вузол) і chisel (REPL Solidity), а ще читкоди, стандартна бібліотека forge-std і налаштування
`foundry.toml`. Джерела — сайт getfoundry.sh (Foundry Book, репозиторій foundry-rs/book), репозиторії
foundry-rs/foundry і foundry-rs/forge-std на GitHub і реєстр npm, лише англійською. Код спільний і лежить у
`../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of the official Foundry documentation -- the Foundry Book (getfoundry.sh) on the release day of every stable
release with forge, cast, anvil, chisel, configuration, the cheatcode, forge-std and CLI references; the markdown of
the foundry-rs/foundry repository at every stable tag; the release notes; forge-std's README, Solidity source and
release notes for every version; and the npm version table of @foundry-rs/forge, cast, anvil and chisel. Only stable
releases are here, no nightly builds. If something about Foundry is not found in these documents, it is unlikely to be
anywhere in its official documentation.

**Межі.**

Тут немає Hardhat, Truffle й Remix, мови Solidity як такої, бібліотек OpenZeppelin і Solmate, Viem і Wagmi (окремі
примірники `viem` і `wagmi`), ethers.js, специфікацій EIP, документації мереж і RPC-провайдерів, нічних збірок і
машинного переліку читкодів `cheatcodes.json` (читкоди описують сторінки сайту й `Vm.sol`).

**Далі в [README](../instances/foundry/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація; Версії
у відповіді; Межі, про які треба пам'ятати; Сховище сирого; Архівний режим: сервер без корпусу; Установка venv;
Збирання корпусу; Сервер під Claude Code.

### binance-spot

**Коли піднімати.** Працюєте з API спотової торгівлі Binance.

**Порт** 8801, сервер `binance-spot-docs`. Підняти: `./df binance-spot serve`. Адреса: `http://127.0.0.1:8801/mcp`.

**Обсяг.** Документів: 24, фрагментів: 1 042.

**Опис.**

Сорок перший примірник фабрики: захищений MCP-сервер, що відповідає на питання про API споту біржі Binance — як
отримати ринкові дані (ціни, свічки, книгу заявок), як працюють потоки WebSocket і їхні ліміти, як підписати запит,
які є ордери й правила біржі, що означає код помилки і що в API змінилося. Джерело — офіційний репозиторій
документації `binance/binance-spot-api-docs`, лише англійські файли. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents in English -- the Binance Spot API documentation (binance/binance-spot-api-docs): the REST API, the
WebSocket API, the market data streams, the user data stream, error codes, filters, enums, the short SBE references,
the FAQ pages and the changelogs of the Spot API and of the SPOT Testnet. Futures, margin, wallet and the other
Binance products, the full FIX API reference and the SBE schemas are not here.

**Межі.**

Тут немає ф'ючерсів, маржі, гаманця, суб-акаунтів та інших продуктів Binance (вони — лише на
developers.binance.com), повного довідника FIX API, схем SBE, бібліотек-конекторів, китайських перекладів і
демо-режиму. Сам протокол WebSocket і браузерний `WebSocket` — у примірниках `webstandards` і `mdn`.

**Далі в [README](../instances/binance-spot/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація;
Версії у відповіді; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

### kraken-spot

**Коли піднімати.** Працюєте з API спотової торгівлі Kraken.

**Порт** 8824, сервер `kraken-spot-docs`. Підняти: `./df kraken-spot serve`. Адреса: `http://127.0.0.1:8824/mcp`.

**Обсяг.** Документів: 153, фрагментів: 981.

**Опис.**

Захищений MCP-сервер, що відповідає на питання про API споту біржі Kraken — як отримати ринкові дані (тікер, свічки,
книгу заявок, угоди), як під'єднатися до WebSocket v2 і підписатися на канал, як підписати запит REST, які є ордери,
ліміти й помилки, як працює протокол FIX 4.4 і що в API змінилося. Джерело — офіційний сайт документації
docs.kraken.com, лише англійською. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`; ця
тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents in English -- the Kraken Spot API documentation (docs.kraken.com): every Spot REST endpoint, the Spot
WebSocket API v2 channels and methods, the exchange guides (overview, quickstart, authentication, API keys, rate
limits, errors, client order ids, amends, L3 data, book checksums, reconnection), the Unified FIX 4.4 reference and
FIX guides, the exchange changelog and the short pages on the official SDKs, kraken-cli and its MCP server.
Derivatives (futures) beyond the shared FIX reference, Spot WebSocket v1 reference, institutional and Embed APIs and
the SDK code reference are not here.

**Межі.**

Тут немає деривативів (ф'ючерсів) — окрім того, що каже спільний довідник FIX, — довідника WebSocket v1, інституційних
API (custody, OTC, prime), Embed і Pay, affiliate, документації коду SDK і README їхніх репозиторіїв. Сам протокол
WebSocket і браузерний `WebSocket` — у примірниках `webstandards` і `mdn`; Binance — у `binance-spot`.

**Далі в [README](../instances/kraken-spot/README.md):** Навіщо; Скільки цього; Що в цій теці; Звідки документація;
Версії у відповіді; Межі, про які треба пам'ятати; Архівний режим: сервер без корпусу; Установка venv; Збирання
корпусу; Сервер під Claude Code.

<!-- тема: Навчальні матеріали й архітектура -->

### patterns

**Коли піднімати.** Обираєте шаблон проєктування або рефакторинг за refactoring.guru.

**Порт** 8777, сервер `patterns-docs`. Підняти: `./df patterns serve`. Адреса: `http://127.0.0.1:8777/mcp`.

**Обсяг.** Документів: 463, фрагментів: 3 931.

**Опис.**

Сімнадцятий примірник фабрики: захищений MCP-сервер, що відповідає на питання про патерни проєктування, рефакторинг і
принципи SOLID та GRASP: сайт [refactoring.guru](https://refactoring.guru/) (англійська версія),
[patterns.dev](https://www.patterns.dev/) (патерни JavaScript, React і Vue), оригінальні статті й блог Роберта
Мартіна, стаття Лісков і Вінг, статті Вікіпедії і глави чотирьох книг про GRASP і SOLID (див. «Книги»). Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents of refactoring.guru, in English -- the 22 classic design patterns (intent, problem, solution, structure,
pseudocode, applicability, how to implement, pros and cons, relations with other patterns) with the introduction,
classification, criticism and the factory comparison; the refactoring section (what refactoring is, technical debt,
when and how to refactor), the 23 code smells and the 66 refactoring techniques with before/after code in Java, C#,
PHP, Python and TypeScript; and the code examples of every pattern in TypeScript, C++, C#, Go, Java, PHP, Python,
Ruby, Rust and Swift. Next to it: patterns.dev (JavaScript, performance, rendering, React and Vue patterns); SOLID
from Robert C. Martin's original articles and blog, Liskov and Wing's 1994 paper and Wikipedia; GRASP and coupling,
cohesion, the Law of Demeter and composition over inheritance from Wikipedia; and the GRASP and SOLID chapters of
Larman's "Applying UML and Patterns" (2004), Martin and Martin's "Agile Principles, Patterns, and Practices in C#"
(2006) and Martin's "Clean Architecture" (2017). Architecture patterns, other frameworks' patterns and the rest of
those books are not here.

**Межі.**

Тут 22 класичні патерни (GoF), запахи коду й техніки за Фаулером, патерни JS/React/Vue з patterns.dev, SOLID і
GRASP, з главами книг Ларманa й Мартіна. Немає архітектурних патернів (MVC, мікросервіси, CQRS), патернів інших
фреймворків (NestJS, Angular, Redux), книг Gang of Four і Фаулера, а з книг Ларманa й Мартіна — решти глав (зокрема
архітектурних частин «Clean Architecture»).

**Далі в [README](../instances/patterns/README.md):** Навіщо; Корпус лише локально; Скільки цього; Книги; Що в цій
теці; Звідки документація; Межі, про які треба пам'ятати; Установка venv; Збирання корпусу; Сервер під Claude Code; На
іншій машині.

### frontend-architecture

**Коли піднімати.** Обираєте будову фронтенду: Feature-Sliced Design та інші підходи.

**Порт** 8790, сервер `frontend-architecture-docs`. Підняти: `./df frontend-architecture serve`. Адреса: `http://127.0.0.1:8790/mcp`.

**Обсяг.** Документів: 223, фрагментів: 4 687.

**Опис.**

Тридцятий примірник фабрики: захищений MCP-сервер, що допомагає обрати й застосувати архітектуру фронтенд-проєкту. Тут
методологія Feature-Sliced Design (документація, блог її авторів, лінтер Steiger), Bulletproof React, Flux, книга
Atomic Design, мікрофронтенди і першоджерела архітектурних стилів: шарова архітектура, MVC і MVP, порти й адаптери
(гексагональна), цибулева, чиста, вертикальні зрізи, острови, DDD. Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

Documents on frontend architecture, in English -- the Feature-Sliced Design documentation (overview, tutorial, layers,
slices, segments, public API, slice groups, guides, migration, framework guides, the About section) with its
changelog, the feature-sliced.design blog, the Steiger linter and its FSD rules, Bulletproof React, the Flux docs,
Brad Frost's Atomic Design book, micro-frontends.org; and the primary sources of architectural styles: Martin Fowler's
GUI Architectures, Presentation Domain Data Layering, Modularizing React Applications, Micro Frontends, Domain Driven
Design and Bounded Context; Alistair Cockburn's Hexagonal Architecture; Robert C. Martin's The Clean Architecture and
Screaming Architecture; Jeffrey Palermo's Onion Architecture; Alexander Bespoyasov's Clean Architecture on Frontend;
Jimmy Bogard's Vertical Slice Architecture; Jason Miller's Islands Architecture; and Herberto Graça's The Software
Architecture Chronicles. Design patterns of code (refactoring.guru, patterns.dev) are in the patterns instance, not
here.

**Межі.**

Тут немає патернів коду (примірник `patterns`), документації фреймворків і бібліотек (React, Next.js, Astro, Redux
та інші — власні примірники) і бекенд-архітектури поза тим, що пояснюють самі статті. Книг «Clean Architecture» і
«Domain-Driven Design» тут немає: є статті їхніх авторів і пояснення інших.

**Далі в [README](../instances/frontend-architecture/README.md):** Навіщо; Корпус лише локально; Скільки цього; Що в
цій теці; Звідки документація; Межі, про які треба пам'ятати; Установка venv; Збирання корпусу; Сервер під Claude
Code; На іншій машині.

### htdp

**Коли піднімати.** Читаєте книжку How to Design Programs або виконуєте її вправи в Racket.

**Порт** 8912, сервер `htdp-book`. Підняти: `./df htdp serve`. Адреса: `http://127.0.0.1:8912/mcp`.

**Обсяг.** Документів: 29, фрагментів: 3 196.

**Опис.**

Захищений MCP-сервер для читання книжки «How to Design Programs, Second Edition» — Matthias Felleisen, Robert Bruce
Findler, Matthew Flatt, Shriram Krishnamurthi; MIT Press, 2018 — за онлайн-виданням авторів на htdp.org, разом із
довідником мов і бібліотек, якими книжка пише (docs.racket-lang.org). Код спільний і лежить у `../../engine/`,
`../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій фабрики — у
[../../README.md](../README.md).

**Склад (так його описано моделі, англійською).**

This is a book, not library documentation. org dated 28 May 2026 -- the Preface, the Prologue, six parts, five
intermezzos and the Epilogue, with every exercise -- and the docs.racket-lang.org reference (Racket 9.3) of its
teaching languages BSL, BSL+, ISL, ISL+, ASL and of its teachpacks 2htdp/image, 2htdp/universe, 2htdp/batch-io,
2htdp/abstraction, 2htdp/web-io, 2htdp/itunes, Planet Cute and htdp/dir. Racket in general, DrRacket beyond the book
and the first edition are not here; if something about the book is not found in these documents, it is not in the
book.

**Далі в [README](../instances/htdp/README.md):** Навіщо; Корпус лише локально; Скільки цього; Що в цій теці; Звідки
документація; Версії; Установка venv; Збирання корпусу; Сервер під Claude Code.

### agent-harness-course

**Коли піднімати.** Вчитеся будувати оболонку для агентів за курсом Agent Harness Course.

**Порт** 8942, сервер `agent-harness-course-docs`. Підняти: `./df agent-harness-course serve`. Адреса: `http://127.0.0.1:8942/mcp`.

**Обсяг.** Документів: 252, фрагментів: 2 250.

**Опис.**

Захищений MCP-сервер для вивчення відкритого курсу Agent Harness Course
([justxor/agent-harness-course](https://github.com/justxor/agent-harness-course)): як побудувати **харнес**, тобто код
навколо моделі, що робить її агентом, — цикл, інструменти, контекст, пам'ять, субагенти, безпеку, evals (замір якості
агента). Поруч лежить проєкт, який курс розбирає в модулі 8, і сім статей, які курс радить прочитати. Код спільний і
лежить у `../../engine/`, `../../server/` та `../../common/`; ця тека тримає самі дані домену. Загальний устрій
фабрики — у [../../README.md](../README.md). План вивчення з практикою за модулями — у
[LEARNING.md](../instances/agent-harness-course/LEARNING.md).

**Склад (так його описано моделі, англійською).**

This is a course and its reading, not library documentation. 4.1 in English (documentation, system prompts, release
notes, code of the agent, the core, the server and the stores); seven articles: four from Anthropic, HumanLayer
12-Factor Agents, Simon Willison on the lethal trifecta, Hamel Husain on evals. Other harnesses, frameworks, model API
references and the Model Context Protocol are not here; if something about the course is not found in these documents,
it is not in the course.

**Далі в [README](../instances/agent-harness-course/README.md):** Навіщо; Скільки цього; Який запит писати; Що не
входить; Ліцензії: що можна брати у свій код; Корпус лише локально; Як запустити.

### devops-core-course

**Коли піднімати.** Виконуєте лабораторні курсу DevOps Core Course.

**Порт** 8943, сервер `devops-core-course-docs`. Підняти: `./df devops-core-course serve`. Адреса: `http://127.0.0.1:8943/mcp`.

**Обсяг.** Документів: 82, фрагментів: 2 339.

**Опис.**

Захищений MCP-сервер для вивчення курсу DevOps Engineering: Core Practices
([inno-devops-labs/DevOps-Core-Course](https://github.com/inno-devops-labs/DevOps-Core-Course)): один власний
вебсервіс за шістнадцять тижнів проходить шлях від контейнера й CI через Terraform, Ansible і спостережуваність до
Kubernetes, GitOps і поступової доставки. Код спільний і лежить у `../../engine/`, `../../server/` та `../../common/`;
ця тека тримає самі дані домену. Загальний устрій фабрики — у [../../README.md](../README.md). План вивчення — у
[LEARNING.md](../instances/devops-core-course/LEARNING.md). Він є четвертим етапом лінії Linux → Docker → Kubernetes.

**Склад (так його описано моделі, англійською).**

This is a course, not the documentation of a tool. The reference of those tools is not here; if something about the
course is not found in these documents, it is not in the course. Reminder: before Lab 4 (Terraform, OpenTofu, Pulumi),
Labs 5-6 (Ansible), Lab 7 (Grafana Alloy), Lab 11 (OpenBao, External Secrets Operator), Lab 14 (Argo Rollouts) and Lab
18 (Nix) the instance of that tool still has to be built: tell the user.

**Далі в [README](../instances/devops-core-course/README.md):** Навіщо; Нагадування: що зібрати перед лабораторними;
Скільки цього; Версії; Що не входить; Корпус лише локально; Лекції й розбір читання; Як запустити.
