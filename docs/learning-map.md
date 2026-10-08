# Карта навчання: примірники по фазах і чого ще бракує

Дві незалежні лінії навчання й примірники фабрики, на які вони спираються. **Примірник** — сервер документації
однієї бібліотеки чи інструмента (тека `instances/<ім'я>`). Файл оновлюється після кожного нового примірника, разом
із підрозділами «Документація у фабриці» самих планів.

Стан на 08.10.2026. Примірники: astro, auth, clerk, docker, ecmascript, eslint, express, frontend-architecture,
github-actions, kubernetes, linux, mdn, msw, nestjs, nextjs, nginx, nodejs, owasp, patterns, playwright, postgresql,
react, react-hook-form, react-router, redux, shadcn, socketio, supabase, tailwind, tanstack-query, testing-library,
typescript, v8, vite, vitest, wasm, webdev, webstandards, zod, zustand.

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
| 2. Як React працює зсередини | `eslint` (4), `webdev` (5, 7) |
| 3. Екосистема | `react-router` (1–2, 13), `tanstack-query` (3–5, 8, 13), `react-hook-form` і `zod` (10), `zustand` і `redux` (11), `vitest` і `testing-library` (12–13), `msw` (13), `playwright` (14), `mdn` (6–8, 15), `webstandards` (6, 15), `shadcn` (15), `webdev` (8, 10, 15) |
| 4. Сервер: SSR, стрімінг, серверні компоненти | — |
| 5. Продакшн і викот у кластер | `vite` (1–2, 5–7, 9), `react-router` (1), `docker` (6–7), `kubernetes` (6–9), `mdn` (4), `webstandards` (6), `playwright` (5), `github-actions` (5), `owasp` (2), `nginx` (7), `webdev` (3–4, 6) |
| Факультатив «крипта» | `tanstack-query`, `zod`, `vite`, `docker` |

### План NestJS — [instances/nestjs/LEARNING.md](../instances/nestjs/LEARNING.md)

| Фаза | Примірники (дні) |
|------|------------------|
| 0. База, якої Nest не дає | `typescript` (вступ, 1–4), `mdn` (вступ, 6–7, 10–11), `webstandards` (6–7, 10–11), `express` (9–10), `vite` (11), `postgresql` (вступ, 13–18), `owasp` (вступ, 10), `nodejs` (5, 8, 12) |
| 1. Ядро Nest | — |
| 2. Робочий API | `zod` (1, 3, 8), `webstandards` (4, 6), `tanstack-query` (7), `react-hook-form` (8) |
| 3. Дані: TypeORM, Prisma | `postgresql` (12), `owasp` (5); TypeORM і Prisma — у документації Nest лише інтеграція |
| 4. Автентифікація й авторизація | `webstandards` (1–2, 6–8, 12), `express` (8, 12), `react-router` (9), `owasp` (1, 6, 8, 12) |
| 5. Якість: тести й DI | `vitest` (1) |
| 6. Продакшн | `docker` (вступ, 2), `kubernetes` (8–9), `express` (9), `postgresql` (9), `github-actions` (вступ, 7), `nginx` (вступ, 2, 5) |
| 7. Живі дані: WebSockets | `socketio` (вступ, 2–4, 6–7), `mdn` (вступ, 1), `webstandards` (вступ, 1, 3, 6), `vite` (2), `kubernetes` (3, 6, 8), `owasp` (3), `nginx` (6) |
| Факультатив «крипта» | `docker`, `kubernetes`, `webstandards` |

### План Next.js — [instances/nextjs/LEARNING.md](../instances/nextjs/LEARNING.md)

| Фаза | Примірники (дні) |
|------|------------------|
| 0. База, якої Next.js не дає | `mdn` (вступ, 1–3, 6), `webstandards` (1–3, 6), `react` (вступ, 4–5), `owasp` (3), `nodejs` (6) |
| 1. Ядро App Router | `eslint` (1), `tailwind` (10), `webdev` (11, 14) |
| 2. Як Next.js працює зсередини | — |
| 3. Кешування | — |
| 4. Фулстек: дані, автентифікація, дії, тести | `webstandards` (2–3, 5, 9–10, 12), `zod` (5), `react-hook-form` і `shadcn` (6), `postgresql` (1), `auth`, `clerk` і `supabase` (9), `tanstack-query` (11), `vitest` і `testing-library` (13), `playwright` (14), `owasp` (12), `webdev` (6) |
| 5. Інтерфейс із характером | `mdn` (4), `zustand` (5), `webstandards` (5, 7), `shadcn` (5), `webdev` (4, 7) |
| 6. Чужий код | — |
| 7. DevOps: від збірки до продакшну | `docker` (вступ, 2, 4), `webstandards` (6), `kubernetes` (вступ, 12), `playwright` (7), `github-actions` (вступ, 7), `nginx` (вступ, 6), `webdev` (9–10) |
| 8. Next.js поруч з окремим бекендом | `webstandards` (2, 6–7), `mdn` (7), `socketio` (6), `nginx` (6); за змістом — `nestjs` |
| 9. Kubernetes глибше і демо | `kubernetes` (вступ, 1–8), `linux` (5), `mdn` (8), `webstandards` (8), `github-actions` (вступ, 5) |
| Факультатив «крипта» | `docker`, `linux`, `webstandards` |

## Лінія 2. Linux → Docker → Kubernetes

| План | Фаза | Примірники (дні) |
|------|------|------------------|
| [Linux](../instances/linux/LEARNING.md) | 3. Процеси, служби, пакети, ядро, відновлення | `nginx` (6) |
| Linux | 5. Мережа | `webstandards` (10), `nginx` (10) |
| Linux | 6. Безпека й віртуалізація | `docker` (4) |
| Linux | 7. Міст до контейнерів | `docker` (4) |
| [Docker](../instances/docker/LEARNING.md) | 1. Образи й Dockerfile | `nginx` (4) |
| Docker | 2. Дані й мережа | `nginx` (2) |
| Docker | 4. Кілька архітектур, реєстри, CI, ланцюг постачання | `github-actions` (3–4) |
| Docker | 6. Міст до Kubernetes | `kubernetes` (1) |
| [Kubernetes](../instances/kubernetes/LEARNING.md) | 2. Конфігурація, ресурси й безпека застосунку | `webstandards` (6) |
| Kubernetes | 11. Мережа кластера | `nginx` (3) |
| Kubernetes | 13. Іспит CKA | `docker`, `linux` (4) |

Решта фаз — лише власний примірник плану.

## Чого бракує

Документація, яку ще треба зробити, щоб навчання не виходило за межі фабрики. У кожному списку порядок — за
кількістю згадок у плані: що вище, то більше днів спирається на джерело поза фабрикою.

### React

1. react-window або TanStack Virtual, Sentry.
2. Факультатив: wagmi, viem, lightweight-charts, decimal.js, Foundry.

### NestJS

1. Prisma (40) і TypeORM (29): у документації Nest — лише інтеграційний шар.
2. Redis (29) і BullMQ (8).
3. Passport (13), class-validator і class-transformer (7), RxJS (4).
4. Факультатив: viem, decimal.js, Foundry.

### Next.js

1. Redis (14).
2. Drizzle або Prisma.
3. nuqs, next-themes, next-intl, Motion, iron-session, jose.
4. Sentry, OpenTelemetry, Prometheus і Grafana.
5. Факультатив: viem, wagmi, OpenZeppelin, Foundry.

### Спільне для лінії 1

Redis потрібен двом-трьом планам одразу: такий примірник закриває найбільше.

### Лінія 2

Прогалин, для яких варто збирати примірник, не лишилося: nginx (30 згадок у Linux, 7 у Docker, 3 у Kubernetes) має
примірник `nginx` з 07.10.2026.

Свідомо без примірника — план їх лише згадує або ставить однією командою: CNI (Calico, Cilium, Flannel), HAProxy,
Podman, libvirt і QEMU, MetalLB, CloudNativePG, Trivy, Prometheus. etcd і containerd з `crictl` окремого примірника
не потребують: їх покриває примірник `kubernetes` — `Operating etcd clusters for Kubernetes`, `Debugging Kubernetes
nodes with crictl`, `Container Runtimes`.
