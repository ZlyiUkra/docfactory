# redis-analytics
# джерело: https://github.com/upstash/redis-analytics/blob/a7e0afc8a694dad44777c4172e14d955d5e8f640/README.md
# отримано: 2026-10-16

A lightweight, typed analytics SDK backed by Upstash Redis.
Capture pageviews, clicks, and custom events; manage sessions; resolve feature
flags server-side; and query everything through Redis Search.

It's designed for serverless / edge runtimes (Next.js App Router, etc.): a single
HTTP endpoint on the backend, a typed client on the frontend, and an optional React
hook.

> **Status:** early (`0.x`). APIs may change.

## Packages

This is a pnpm + Turborepo monorepo.

| Package        | Description                                    |
| -------------- | ---------------------------------------------- |
| `packages/sdk` | The published SDK — `@upstash/redis-analytics` |
| `packages/app` | Example Next.js app wiring the SDK end-to-end  |
| `packages/ui`  | Dashboard UI for exploring captured analytics  |

## Installation

```bash
npm install @upstash/redis-analytics @upstash/redis
```

## Concepts

- **Session** — created on the backend, identified by a `sessionId`. Carries the
  resolved feature flags and optional server-set metadata. Sessions expire after
  `session.expirationMs`.
- **Event** — a named occurrence tied to a session. Standard events (`pageview`,
  `click`, `error`, `warning`, `info`) are built in; custom events are fully typed.
- **Feature flag** — resolved server-side (typically in middleware) and frozen onto
  the session at creation time.
- **Schema registry** — infers property types from captured events and powers the
  Redis Search index.
- **Single endpoint** — the frontend client and backend talk over one route
  (`/api/analytics` by default) using a typed request/response protocol.

## Quick start (Next.js App Router)

### 1. Configure the backend client

```ts
// lib/analytics.ts
import { AnalyticsBackendClient } from "@upstash/redis-analytics";

export const analytics = new AnalyticsBackendClient({
  redis: {
    url: process.env.UPSTASH_REDIS_REST_URL!,
    token: process.env.UPSTASH_REDIS_REST_TOKEN!,
  },
  // optional
  config: {
    session: { expirationMs: 3_600_000 }, // 1 hour
    featureFlags: {
      theme: {
        possibleValues: ["light", "dark"],
        defaultValue: "light",
      },
    },
    events: { customEventRetentionDays: 7, maxBatchSize: 20 },
    schemaValidation: { checkFrequency: 1 },
    logging: {
      retentionDays: 30,
      enabledTypes: ["schema_update", "feature_flag_update", "index_update"],
    },
    search: { indexName: "events-idx" },
  },
});
```

### 2. Expose the single endpoint

```ts
// app/api/analytics/route.ts
import { analytics } from "@/lib/analytics";

const handler = analytics.getHandler({
  // Middleware runs before every request. Resolve feature flags here.
  middleware: ({ analyticsRequest }) => {
    if (analyticsRequest.requestType !== "createSession") return;

    return {
      featureFlags: { theme: Math.random() < 0.5 ? "light" : "dark" },
      // sessionMetadata: { ... } // attach server-side metadata if needed
    };
  },
});

export const POST = handler;
export const GET = handler;
```

Middleware can also return a `Response` to short-circuit (e.g. `401`), and you can
pass an array of middlewares that run in order.

### 3. Use the React hook on the frontend

```ts
// lib/use-analytics.ts
import { createAnalyticsHook } from "@upstash/redis-analytics/react";

type Events = {
  "custom:purchase": { productId: string; amount: number; currency: string };
};
type Flags = { theme: "light" | "dark" };

export const useAnalytics = createAnalyticsHook<Events, Flags>({
  endpoint: "/api/analytics",
  flushInterval: 2000, // debounce + batch event sends
});
```

```tsx
"use client";
import { useAnalytics } from "@/lib/use-analytics";

export function BuyButton() {
  const { captureEvent, featureFlags, sessionId } = useAnalytics();

  return (
    <button
      onClick={() =>
        captureEvent({
          sessionId: sessionId!,
          eventName: "custom:purchase",
          properties: { productId: "sku-1", amount: 42, currency: "USD" },
        })
      }
    >
      Buy ({featureFlags.theme})
    </button>
  );
}
```

The hook auto-creates a session, auto-captures a `pageview` on path change, and
exposes the resolved feature flags. No provider needed — call `createAnalyticsHook`
once at module level.

### Using the client directly (no React)

```ts
import { AnalyticsClient } from "@upstash/redis-analytics";

const client = new AnalyticsClient({ endpoint: "/api/analytics" });

const session = await client.createSession();
await client.capturePageView(session.id, "/products");
const theme = await client.getFeatureFlag(session.id, "theme");
```

## Configuration reference

`AnalyticsConfig` passed to `AnalyticsBackendClient` (config is optional; defaults
shown):

| Field                             | Default      | Description                                              |
| --------------------------------- | ------------ | -------------------------------------------------------- |
| `session.expirationMs`            | `3_600_000`  | Session TTL in ms.                                       |
| `featureFlags`                    | `{}`         | Flag definitions (`possibleValues`, `defaultValue`).     |
| `events.customEventRetentionDays` | `7`          | Retention window for custom events.                      |
| `events.maxBatchSize`             | `20`         | Max events per batch request.                            |
| `schemaValidation.checkFrequency` | `1`          | Probability (0–1) of running schema inference per event. |
| `logging.retentionDays`           | `30`         | System-log retention.                                    |
| `logging.enabledTypes`            | see source   | Which `LogType`s to persist.                             |
| `search.indexName`                | `events-idx` | Redis Search index name.                                 |

`ClientConfig` passed to `AnalyticsClient` / `createAnalyticsHook`:

| Field           | Default          | Description                                            |
| --------------- | ---------------- | ------------------------------------------------------ |
| `endpoint`      | `/api/analytics` | Backend endpoint URL.                                  |
| `flushInterval` | `0`              | Debounce window (ms) for batching captures. `0` = off. |
| `maxBatchSize`  | `20`             | Max events per batch request from the client.          |

## Development

```bash
pnpm install
pnpm dev     # turbo dev across packages
pnpm build   # turbo build
pnpm lint    # turbo lint
```

The example app and dashboard need Upstash Redis credentials:

```bash
UPSTASH_REDIS_REST_URL=...
UPSTASH_REDIS_REST_TOKEN=...
```

## License

See LICENSE.
