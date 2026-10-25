# Карта навчання: примірники по фазах і чого ще бракує

Три незалежні лінії навчання й примірники фабрики, на які вони спираються. **Примірник** — сервер документації
однієї бібліотеки чи інструмента (тека `instances/<ім'я>`). Файл оновлюється після кожного нового примірника, разом
із підрозділами «Документація у фабриці» самих планів.

Стан на 25.10.2026. Примірники: alpine, amqp-connection-manager, amqplib, anthropic-api, argon2, aspnetcore, astro,
astro-markdown-pipeline, auth, bcrypt, binance-spot, biome, bullmq, cares, casl, certbot, class-transformer,
class-validator, clerk, confluent-kafka-javascript, csharp, csrf-csrf, doc-tools, docker, dotnet, dotnet-testing,
drizzle, ecmascript, entityframework, eslint, expo, express, express-rate-limit, fastify, ffmpeg, foundry,
frontend-architecture, github-actions, gvisor, helmet, i18next, icu, ioredis, iron-session, jose, jsonschema, kafka,
kafkajs, kraken-spot, kubernetes, libreoffice, libuv, lightweight-charts, linux, llhttp, mdn, mikro-orm, mongodb,
mongoose, motion, msw, nestjs, nestjs-cls, nestjs-pino, next-intl, next-themes, nextjs, nghttp2, nginx, node-mongodb,
node-postgres, node-redis, nodejs, nodemailer, nuget, nuqs, nvidia-container-toolkit, ollama, openapi-typescript,
openssl, opentelemetry, oracle-cloud, orval, owasp, partysocket, passport, patterns, platformatic-kafka, playwright,
postgrator, postgres-image, postgresql, prisma, rabbitmq, react, react-hook-form, react-native, react-router,
react-window, redis, redux, rxjs, sentry, shadcn, socketio, sqlserver, storybook, stripe, supabase, supertest, swr,
tailwind, tanstack-query, tanstack-router, tanstack-virtual, tesseract, testcontainers-dotnet, testing-library,
typeorm, typescript, upstash, v8, viem, vite, vitest, wagmi, wasm, webdev, webstandards, ws, zod, zustand.

## Як читати таблиці

Власний примірник плану (`react` для плану React, `nestjs` для NestJS і так далі) потрібен на всіх його фазах,
тому в таблицях не повторюється. Номер у дужках — день фази, «вступ» — текст фази поза днями. Прочерк — фаза
спирається лише на власний примірник або на джерела поза фабрикою. У самих планах ті самі примірники стоять іменами
серверів документації: рядок «Сервери MCP» під кожним днем і під заголовком кожної фази (`mdn` — `mdn-docs`,
`webstandards` — `webstandards-docs`).

## Лінія 1. React → NestJS → Next.js

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
| 9. Kubernetes глибше і демо | `kubernetes` (вступ, 1–8), `oracle-cloud` (вступ, 2, 7), `linux` (5), `mdn` (8), `webstandards` (8), `github-actions` (вступ, 5) |
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
| Docker | 4. Кілька архітектур, реєстри, CI, ланцюг постачання | `github-actions` (1, 4) |
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
| 2. Контент | `zod` (2), `webdev` (6–7), `mdn` (7) |
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

### Next.js

1. Prometheus і Grafana.
2. Факультатив: OpenZeppelin.

### Лінія 2

Прогалин, для яких варто збирати примірник, не лишилося.

Свідомо без примірника — план їх лише згадує або ставить однією командою: CNI (Calico, Cilium, Flannel), HAProxy,
Podman, libvirt і QEMU, MetalLB, CloudNativePG, Trivy, Prometheus.

### Astro

1. Платформи розгортання: Cloudflare (3), Vercel і Netlify (по 1) — документація Astro описує лише адаптери до них.
2. Контент поза документацією Astro: remark і rehype (3), CMS (2), Shiki (1).
3. Lighthouse (1).
4. Лише в переліку плану, без днів: Vue, Svelte, Solid, Preact (острови не на React).
