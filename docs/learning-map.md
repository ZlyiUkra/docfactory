# Карта навчання: примірники по фазах і чого ще бракує

Три незалежні лінії навчання й примірники фабрики, на які вони спираються. **Примірник** — сервер документації
однієї бібліотеки чи інструмента (тека `instances/<ім'я>`). Файл оновлюється після кожного нового примірника, разом
із підрозділами «Документація у фабриці» самих планів.

Стан на 29.10.2026. Примірники: alpine, amqp-connection-manager, amqplib, angular, anthropic-api, argocd, argon2,
aspnetcore, astro, astro-markdown-pipeline, auth, bcrypt, binance-spot, biome, bullmq, cares, casl, certbot,
class-transformer, class-validator, claude-code, clerk, coder-websocket, confluent-kafka-javascript, contentful,
csharp, csrf-csrf, d3, doc-tools, docker, dotnet, dotnet-testing, drizzle, ecmascript, entityframework, eslint, expo,
express, express-rate-limit, fastify, ffmpeg, flux, foundry, frontend-architecture, github-actions, go, golang-jwt,
golang-migrate, golang-x, golangci-lint, golevelup-nestjs-rabbitmq, goose, grafana, gvisor, helmet, htdp, i18next,
icu, ioredis, iron-session, jose, jsonschema, kafka, kafkajs, kraken-spot, kubernetes, learning-go, libreoffice,
libuv, lightweight-charts, linux, llhttp, loki, mdn, mikro-orm, mongodb, mongoose, motion, msw, nats, nats-js, nestjs,
nestjs-cls, nestjs-pino, next-intl, next-safe-action, next-themes, nextjs, nghttp2, nginx, node-mongodb,
node-postgres, node-redis, nodejs, nodemailer, nuget, nuqs, nvidia-container-toolkit, oapi-codegen, ollama,
openapi-typescript, openssl, opentelemetry, oracle-cloud, orval, owasp, partysocket, passport, patterns, payload, pgx,
platformatic-kafka, playwright, postgrator, postgres-image, postgresql, prisma, prometheus, rabbitmq, react,
react-email, react-hook-form, react-native, react-router, react-window, redis, redux, resend, river, rxjs, sanity,
sealed-secrets, sentry, shadcn, socketio, solidjs, sqlc, sqlserver, storybook, stripe, supabase, supertest, svelte,
sveltekit, swr, tailwind, tanstack-query, tanstack-router, tanstack-virtual, tesseract, testcontainers-dotnet,
testcontainers-go, testing-library, trpc, turborepo, typeorm, typescript, uploadthing, upstash, v8, vercel-ai-sdk,
viem, vite, vitest, vue, vueuse, wagmi, wasm, webdev, webstandards, ws, zod, zustand.

## Як читати таблиці

Власний примірник плану (`react` для плану React, `nestjs` для NestJS і так далі) потрібен на всіх його фазах,
тому в таблицях не повторюється. Номер у дужках — день фази, «вступ» — текст фази поза днями. Прочерк — фаза
спирається лише на власний примірник або на джерела поза фабрикою. У самих планах ті самі примірники стоять іменами
серверів документації: рядок «Сервери MCP» під кожним днем і під заголовком кожної фази (`mdn` — `mdn-docs`,
`webstandards` — `webstandards-docs`).

## Лінія 1. React → NestJS → Next.js

Після плану React можна піти не в NestJS і Next.js, а в окрему лінійку Go з власним проєктом — її план стоїть нижче,
поруч із планом NestJS.

### План React — [instances/react/LEARNING.md](../instances/react/LEARNING.md)

| Фаза | Примірники (дні) |
|------|------------------|
| 0. База, якої React не дає | `mdn` (вступ, 1–8), `webstandards` (1, 5–8), `typescript` (вступ, 9–10), `vite` (11–12), `eslint` (11), `tailwind` (11), `nodejs` (4), `webdev` (8) |
| 1. Ядро React | `vite` (20), `eslint` (19) |
| 2. Як React працює зсередини | `eslint` (4), `webdev` (5, 7), `tanstack-virtual` і `react-window` (7), `sentry` (8) |
| 3. Екосистема | `react-router` (1–2, 13), `tanstack-query` (3–5, 8, 13), `react-hook-form` і `zod` (10), `zustand` і `redux` (11), `vitest` і `testing-library` (12–13), `msw` (13), `playwright` (14), `mdn` (6–8, 15), `webstandards` (6, 15), `shadcn` (15), `webdev` (8, 10, 15), `binance-spot` (вступ, 6–8), `kraken-spot` (вступ, 6–7), `partysocket` (7) |
| 4. Сервер: SSR, стрімінг, серверні компоненти | — |
| 5. Продакшн і викот у кластер | `vite` (1–2, 5–7, 9), `react-router` (1), `docker` (вступ, 7), `kubernetes` (вступ, 7–9), `oracle-cloud` (вступ, 8), `mdn` (4), `webstandards` (6), `playwright` (5), `github-actions` (5), `owasp` (2), `nginx` (7), `webdev` (3–4, 6) |
| Факультатив «крипта» | `binance-spot` (К1–К3), `tanstack-query` (К1, К4), `lightweight-charts` (К2), `mdn` (К3), `zod` (К5), `wagmi` (К4–К5), `viem` (К4–К5), `foundry` (К4–К5) |

### План NestJS — [instances/nestjs/LEARNING.md](../instances/nestjs/LEARNING.md)

| Фаза | Примірники (дні) |
|------|------------------|
| 0. База, якої Nest не дає | `typescript` (вступ, 1–4), `mdn` (вступ, 6–7, 10–11), `webstandards` (6–7, 10–11), `express` (9–10), `vite` (11), `postgresql` (вступ, 13–18), `owasp` (вступ, 10), `nodejs` (5, 8, 12), `csrf-csrf` (10) |
| 1. Ядро Nest | `rxjs` (7) |
| 2. Робочий API | `zod` (1, 3, 8), `class-validator` (2, 8), `class-transformer` (2), `webstandards` (4, 6), `tanstack-query` (7), `react-hook-form` (8), `jsonschema` (6), `nestjs-cls` (5), `orval` і `openapi-typescript` (7) |
| 3. Дані: TypeORM, Prisma | `typeorm` (вступ, 1–6, 11–12), `prisma` (вступ, 3, 7–12), `postgresql` (12), `owasp` (5) |
| 4. Автентифікація й авторизація | `webstandards` (1–2, 6–8, 12), `express` (8, 12), `react-router` (9), `owasp` (1, 6, 8, 12), `argon2` (1), `bcrypt` (1), `class-transformer` (1), `passport` (5), `helmet` (12), `express-rate-limit` (12), `csrf-csrf` (8), `casl` (11) |
| 5. Якість: тести й DI | `vitest` (1), `supertest` (3–4), `prisma` (2), `nestjs-cls` (6) |
| 6. Продакшн | `docker` (вступ, 2, 7), `upstash` (6), `kubernetes` (вступ, 8–9), `oracle-cloud` (вступ, 8), `express` (9), `postgresql` (9), `github-actions` (вступ, 7), `nginx` (вступ, 2, 5), `node-postgres` (5), `argon2` (8), `bcrypt` (8), `prisma` (2, 8), `redis` (8), `nestjs-pino` (3) |
| 7. Живі дані: WebSockets | `socketio` (вступ, 2–4, 6–7), `mdn` (вступ, 1), `webstandards` (вступ, 1, 3, 6), `ws` (1–2, 5), `vite` (2), `kubernetes` (3, 6, 8), `owasp` (3), `nginx` (6), `binance-spot` (вступ, 5), `redis` (5), `kraken-spot` (вступ, 1, 5), `rxjs` (6) |
| Факультатив «крипта» | `binance-spot` (К1), `webstandards` (К3), `node-postgres` (К1), `viem` (К3–К4), `foundry` (К4) |

### План Go — [instances/go/LEARNING.md](../instances/go/LEARNING.md)

Окрема лінійка фулстек-розробника з бекендом на Go і власним проєктом — читачем документів `reader` (прототип ради
17.10.2026, реалізований на Go і React, у фазі 8 — з інтерфейсом на Next.js; код — у репозиторії навчання
`goal2learn`, тека `reader/`). Мову фаза 0 вчить за книжкою «Learning Go» (примірник `learning-go`); лінія
сертифікації Ardan Labs спирається на документи `cert-…` власного примірника `go`.

| Фаза | Примірники (дні) |
|------|------------------|
| 0. Мова Go за книжкою «Learning Go» | `learning-go` (1–20), `golangci-lint` (13), `golang-x` (15) |
| 1. Каркас: сервер, Docker, база | `mdn` (1, 3), `webstandards` (1, 3), `learning-go` (1–5, 9), `docker` (6–7), `owasp` (6), `postgresql` (8), `goose` (8), `pgx` (8), `golang-migrate` (8) |
| 2. Модель і контракт, реєстр схем і причин | `ollama` (1–3), `docker` (1), `learning-go` (2, 4, 6–9), `jsonschema` (3, 5–6), `owasp` (9) |
| 3. Документи на вході: синтетичний набір і пісочниця | `docker` (1, 4), `libreoffice` (1–2), `doc-tools` (3, 7), `owasp` (4, 9), `learning-go` (5, 8, 10), `tesseract` (7), `jsonschema` (8) |
| 4. Черга в PostgreSQL: надходження, стани, воркери | `postgresql` (1–3, 5–6), `goose` (1), `pgx` (3, 5–6), `owasp` (3, 9), `sqlc` (4–5), `river` (6), `golang-x` (7), `learning-go` (7–8, 10), `mdn` (9), `testcontainers-go` (10) |
| 5. Розпізнавання, перевірки й інтерфейс | `ollama` (1–3), `jsonschema` (1), `owasp` (1, 10–11), `learning-go` (4), `postgresql` (5–6), `sqlc` (5–6), `mdn` (6, 8, 10–11), `vite` (7), `tanstack-query` (8–9), `react` (8, 10) |
| 6. Замір і якість | `learning-go` (2, 4, 7), `ollama` (3), `testcontainers-go` (4), `golangci-lint` (5), `github-actions` (5) |
| 7. Після прототипу: людина, видача, хмара, агент, кластер | `golang-x` (1, 6), `owasp` (1–3, 5–6, 8), `golang-jwt` (2), `webstandards` (2, 5), `mdn` (2, 6), `learning-go` (3), `react-hook-form` (4), `jsonschema` (4), `postgresql` (4–5, 12), `oapi-codegen` (5), `anthropic-api` (7–9), `docker` (7), `gvisor` (10), `tesseract` (10), `doc-tools` (10), `kubernetes` (11–12), `goose` (12), `ollama` (12) |
| 8. Інтерфейс на Next.js | `nextjs` (1–8), `docker` (1), `react` (2, 5), `mdn` (3, 6), `owasp` (3, 7), `webstandards` (4), `playwright` (8), `kubernetes` (8) |
| С. Лінія сертифікації Ardan Labs | `learning-go` (С4) |

### План Next.js — [instances/nextjs/LEARNING.md](../instances/nextjs/LEARNING.md)

| Фаза | Примірники (дні) |
|------|------------------|
| 0. База, якої Next.js не дає | `mdn` (вступ, 1–3, 6), `webstandards` (1–3, 6), `react` (вступ, 4–5), `owasp` (3), `nodejs` (6) |
| 1. Ядро App Router | `eslint` і `biome` (1), `tailwind` (10), `webdev` (11, 14) |
| 2. Як Next.js працює зсередини | — |
| 3. Кешування | `redis` і `upstash` (9) |
| 4. Фулстек: дані, автентифікація, дії, тести | `webstandards` (2–3, 5, 9–10, 12), `zod` (5), `react-hook-form` і `shadcn` (6), `postgresql` (1), `drizzle` (1, 4), `prisma` (1, 4), `auth`, `clerk` і `supabase` (9), `tanstack-query` і `swr` (11), `vitest` і `testing-library` (13), `playwright` (14), `owasp` (12), `webdev` (6), `argon2` (2), `bcrypt` (2), `iron-session` і `jose` (3) |
| 5. Інтерфейс із характером | `mdn` (4), `motion` (3–4), `zustand` (5), `webstandards` (5, 7), `shadcn`, `next-themes` і `nuqs` (5), `webdev` (4, 7), `i18next` і `next-intl` (8) |
| 6. Чужий код | — |
| 7. DevOps: від збірки до продакшну | `docker` (вступ, 2, 4), `upstash` (6), `drizzle` (4), `prisma` (4), `webstandards` (6), `kubernetes` (вступ, 12), `playwright` (7), `github-actions` (вступ, 7), `nginx` (вступ, 6), `webdev` (9–10), `sentry` (9), `opentelemetry` (9) |
| 8. Next.js поруч з окремим бекендом | `upstash` (1), `webstandards` (2, 6–7), `mdn` (7), `socketio` (6), `nginx` (6), `iron-session` і `jose` (3), `orval` і `openapi-typescript` (2); за змістом — `nestjs` |
| 9. Kubernetes глибше і демо | `kubernetes` (вступ, 1–8), `oracle-cloud` (вступ, 2, 7), `linux` (5), `mdn` (8), `webstandards` (8), `github-actions` (вступ, 5), `sealed-secrets` (6) |
| Факультатив «крипта» | `webstandards` (К1–К3), `wagmi` (К3), `viem` (К1, К3), `foundry` (К2) |

## Лінія 2. Linux → Docker → Kubernetes

| План | Фаза | Примірники (дні) |
|------|------|------------------|
| [Linux](../instances/linux/LEARNING.md) | 1. Основні команди | `certbot` (9) |
| Linux | 3. Процеси, служби, пакети, ядро, відновлення | `nginx` (6) |
| Linux | 5. Мережа | `webstandards` (10), `nginx` (10), `certbot` (10) |
| Linux | 6. Безпека й віртуалізація | `docker` (4) |
| Linux | 7. Міст до контейнерів | `docker` (4) |
| [Docker](../instances/docker/LEARNING.md) | 1. Образи й Dockerfile | `nginx` (4) |
| Docker | 2. Дані й мережа | `nginx` (2) |
| Docker | 4. Кілька архітектур, реєстри, CI, ланцюг постачання | `github-actions` (1, 4), `go` (2) |
| Docker | 5. Експлуатація й безпека рушія | `nvidia-container-toolkit` (1), `gvisor` (4) |
| Docker | 6. Міст до Kubernetes | `kubernetes` (1) |
| [Kubernetes](../instances/kubernetes/LEARNING.md) | 2. Конфігурація, ресурси й безпека застосунку | `webstandards` (6) |
| Kubernetes | 11. Мережа кластера | `nginx` (3) |

Решта фаз — лише власний примірник плану.

## Лінія 3. Astro

### План Astro — [instances/astro/LEARNING.md](../instances/astro/LEARNING.md)

Окремий план: фулстек з боку фронтенду, з Astro за головний інструмент. Дні в ньому — пункти списку, а не
підзаголовки, але рядок «Сервери MCP» той самий.

| Фаза | Примірники (дні) |
|------|------------------|
| 0. База, якої Astro не дає | `mdn` (1–4), `webstandards` (1, 4), `webdev` (3–4), `typescript` (5), `nodejs` (6), `vite` (6) |
| 1. Ядро Astro | `tailwind` (6), `react` (10), `vite` (14) |
| 2. Контент | `zod` (2), `webdev` (6–7), `mdn` (7), `sanity` (10) |
| 3. Сервер | `mdn` (3–4, 12), `zod` (7), `webstandards` (12) |
| 4. Дані й авторизація | `postgresql` (2–3), `clerk` (6), `supabase` (6), `mdn` (7, 9), `webstandards` (7, 9), `argon2` (7), `upstash` (9) |
| 5. Продуктивність і якість | `mdn` (3–4, 8), `webdev` (4, 8), `vitest` (6), `playwright` (7), `webstandards` (8) |
| 6. Продакшн | `docker` (3–4), `playwright` (5) |
| 7. Межі інструмента | `nextjs` (2), `nestjs` (3–4), `webstandards` (4) |

## Чого бракує

Документація, яку ще треба зробити, щоб навчання не виходило за межі фабрики. У кожному списку порядок — за
кількістю згадок у плані: що вище, то більше днів спирається на джерело поза фабрикою.

### React

1. Факультатив: decimal.js.

### NestJS

1. Факультатив: decimal.js.

### Go

План Go з 28.10.2026 вчить на власному проєкті — читачі документів `reader` (прототип ради 17.10.2026; рішення,
файл передачі й конституція — у репозиторії `reader`, код лінійки — у `goal2learn`, тека `reader/`). Фази 1–6
відповідають фазам 0–8 прототипу, фаза 7 — його таблиці відкладеного, фаза 8 переносить інтерфейс на Next.js.

Що треба, крім документації:

1. Формат розгорнутого дня для Go: перевірки у файлах `_test.go` замість `assert`, «Неправильні варіанти» з точними
   повідомленнями компілятора, теорія «від загадки до розбору».
2. Середовище: у WSL стоїть Go 1.24.1 (план і документація — 1.27.3); Ollama на GPU в Docker — не перевірено.
3. Тренажер пробного іспиту Ardan Labs: банку запитань немає (Ardan прикладів не публікує), складати з матеріалу
   `cert-` примірника `go`.

Документація, якої немає:

1. Бібліотека перевірки JSON Schema для Go `santhosh-tekuri/jsonschema` (фаза 2, дні 5–6; фаза 5, день 3);
   специфікація є в примірнику `jsonschema`.
2. Налагоджувач delve — тема іспиту Ardan.
3. pgvector і `pgvector-go` — лише якщо дійде до пошуку за змістом (у плані — «Що далі»).

### Next.js

1. Факультатив: OpenZeppelin.

### Лінія 2

Прогалин, для яких варто збирати примірник, не лишилося.

Свідомо без примірника — план їх лише згадує або ставить однією командою: CNI (Calico, Cilium, Flannel), HAProxy,
Podman, libvirt і QEMU, MetalLB, CloudNativePG, Trivy.

### Astro

1. Платформи розгортання: Cloudflare (3), Vercel і Netlify (по 1) — документація Astro описує лише адаптери до них.
2. Контент поза документацією Astro: remark і rehype (3), Shiki (1).
3. Lighthouse (1).
4. Лише в переліку плану, без днів: Preact (острови не на React).
