# Карта навчання: примірники по фазах і чого ще бракує

Дві незалежні лінії навчання й примірники фабрики, на які вони спираються. **Примірник** — сервер документації
однієї бібліотеки чи інструмента (тека `instances/<ім'я>`). Файл оновлюється після кожного нового примірника, разом
із підрозділами «Документація у фабриці» самих планів.

Стан на 05.10.2026. Примірники: astro, clerk, docker, ecmascript, kubernetes, linux, mdn, msw, nestjs, nextjs,
patterns, playwright, react, react-hook-form, react-router, redux, supabase, tailwind, tanstack-query,
testing-library, typescript, v8, vite, vitest, wasm, webstandards, zod, zustand.

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
| 0. База, якої React не дає | `mdn` (вступ, 1–8), `webstandards` (1, 5–8), `typescript` (вступ, 9–10), `vite` (11–12), `tailwind` (11) |
| 1. Ядро React | `vite` (20) |
| 2. Як React працює зсередини | — |
| 3. Екосистема | `react-router` (1–2, 13), `tanstack-query` (3–5, 8, 13), `react-hook-form` і `zod` (10), `zustand` і `redux` (11), `vitest` і `testing-library` (12–13), `msw` (13), `playwright` (14), `mdn` (6–8, 15), `webstandards` (6, 15) |
| 4. Сервер: SSR, стрімінг, серверні компоненти | — |
| 5. Продакшн і викот у кластер | `vite` (1–2, 5–7, 9), `react-router` (1), `docker` (6–7), `kubernetes` (6–9), `mdn` (4), `webstandards` (6), `playwright` (5) |
| Факультатив «крипта» | `tanstack-query`, `zod`, `vite`, `docker` |

### План NestJS — [instances/nestjs/LEARNING.md](../instances/nestjs/LEARNING.md)

| Фаза | Примірники (дні) |
|------|------------------|
| 0. База, якої Nest не дає | `typescript` (вступ, 1–4), `mdn` (вступ, 6–7, 10–11), `webstandards` (6–7, 10–11), `vite` (11) |
| 1. Ядро Nest | — |
| 2. Робочий API | `zod` (1, 3, 8), `webstandards` (4, 6), `tanstack-query` (7), `react-hook-form` (8) |
| 3. Дані: TypeORM, Prisma | — (у документації Nest лише інтеграція) |
| 4. Автентифікація й авторизація | `webstandards` (1–2, 6–8, 12), `react-router` (9) |
| 5. Якість: тести й DI | `vitest` (1) |
| 6. Продакшн | `docker` (вступ, 2), `kubernetes` (8–9) |
| 7. Живі дані: WebSockets | `mdn` (вступ, 1), `webstandards` (вступ, 1, 3, 6), `vite` (2), `kubernetes` (3, 6, 8) |
| Факультатив «крипта» | `docker`, `kubernetes`, `webstandards` |

### План Next.js — [instances/nextjs/LEARNING.md](../instances/nextjs/LEARNING.md)

| Фаза | Примірники (дні) |
|------|------------------|
| 0. База, якої Next.js не дає | `mdn` (вступ, 1–3, 6), `webstandards` (1–3, 6), `react` (вступ, 4–5) |
| 1. Ядро App Router | `tailwind` (10) |
| 2. Як Next.js працює зсередини | — |
| 3. Кешування | — |
| 4. Фулстек: дані, автентифікація, дії, тести | `webstandards` (2–3, 5, 9–10, 12), `zod` (5), `react-hook-form` (6), `clerk` і `supabase` (9), `tanstack-query` (11), `vitest` і `testing-library` (13), `playwright` (14) |
| 5. Інтерфейс із характером | `mdn` (4), `zustand` (5), `webstandards` (5, 7) |
| 6. Чужий код | — |
| 7. DevOps: від збірки до продакшну | `docker` (вступ, 2, 4), `webstandards` (6), `kubernetes` (вступ, 12), `playwright` (7) |
| 8. Next.js поруч з окремим бекендом | `webstandards` (2, 6–7), `mdn` (7); за змістом — `nestjs` |
| 9. Kubernetes глибше і демо | `kubernetes` (вступ, 1–8), `linux` (5), `mdn` (8), `webstandards` (8) |
| Факультатив «крипта» | `docker`, `linux`, `webstandards` |

## Лінія 2. Linux → Docker → Kubernetes

| План | Фаза | Примірники (дні) |
|------|------|------------------|
| [Linux](../instances/linux/LEARNING.md) | 5. Мережа | `webstandards` (10) |
| Linux | 6. Безпека й віртуалізація | `docker` (4) |
| Linux | 7. Міст до контейнерів | `docker` (4) |
| [Docker](../instances/docker/LEARNING.md) | 6. Міст до Kubernetes | `kubernetes` (1) |
| [Kubernetes](../instances/kubernetes/LEARNING.md) | 2. Конфігурація, ресурси й безпека застосунку | `webstandards` (6) |
| Kubernetes | 13. Іспит CKA | `docker`, `linux` (4) |

Решта фаз — лише власний примірник плану.

## Чого бракує

Документація, яку ще треба зробити, щоб навчання не виходило за межі фабрики. У кожному списку порядок — за
кількістю згадок у плані: що вище, то більше днів спирається на джерело поза фабрикою.

### React

1. npm — `package.json`, `npm ci` (фаза 0).
2. web.dev і web-vitals (фази 2 і 5).
3. react-window або TanStack Virtual, Sentry, ESLint з `eslint-plugin-react-hooks`.
4. Факультатив: wagmi, viem, lightweight-charts, decimal.js, Foundry.

### NestJS

1. socket.io, сервер і клієнт (42 згадки; уся фаза 7).
2. Prisma (40) і TypeORM (29): у документації Nest — лише інтеграційний шар.
3. Redis (29) і BullMQ (8).
4. PostgreSQL (20; фаза 0, дні 13–18, і фаза 3).
5. Express (15) і Node.js (14; фаза 0).
6. nginx (15; compose у фазі 6).
7. Passport (13), class-validator і class-transformer (7), RxJS (4).
8. GitHub Actions (7), OWASP Cheat Sheets (6).
9. Факультатив: viem, decimal.js, Foundry.

### Next.js

1. nginx (15), Redis (14), Node.js (13), PostgreSQL (12).
2. socket.io-client (11; фаза 8).
3. GitHub Actions (8).
4. shadcn/ui і Radix UI, Auth.js або Better Auth, Drizzle або Prisma.
5. nuqs, next-themes, next-intl, Motion, iron-session, jose.
6. Sentry, OpenTelemetry, Prometheus і Grafana.
7. Факультатив: viem, wagmi, OpenZeppelin, Foundry.

### Спільне для лінії 1

PostgreSQL, Node.js, nginx, Redis, socket.io і GitHub Actions потрібні двом-трьом планам
одразу: кожен такий примірник закриває найбільше.

### Лінія 2

1. nginx — 34 згадки в Linux, ще в Docker і Kubernetes; найбільша прогалина лінії.
2. etcd з etcdctl і etcdutl — 25 згадок у Kubernetes, частина CKA. Глави про резервні копії etcd є в документації
   Kubernetes, власної документації etcd немає.
3. containerd і crictl — 17 згадок у Docker і Kubernetes.
4. CNI: Calico, Cilium, Flannel — фаза 11, CKA.
5. HAProxy з keepalived — балансувальник для кластера з HA.
6. Podman — у Linux як альтернатива Docker.
7. Дрібне: MetalLB, CloudNativePG, Trivy, Prometheus.
