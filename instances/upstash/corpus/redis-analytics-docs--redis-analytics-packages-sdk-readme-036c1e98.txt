# @upstash/redis-analytics
# джерело: https://github.com/upstash/redis-analytics/blob/a7e0afc8a694dad44777c4172e14d955d5e8f640/packages/sdk/README.md
# отримано: 2026-10-16

Unified analytics package for Upstash Redis. Provides both server-side (`AnalyticsBackendClient`) and browser-side (`AnalyticsClient`) functionality in a single package.

## Purpose

This package is the complete analytics solution. It provides:

- Session management (creation, retrieval, validation)
- Event tracking and capture (standard + custom events)
- Feature flag management with A/B testing
- Redis Search index management (blue-green deployment)
- Custom event schema registry
- System logging
- Rate limiting
- Browser-side client with event batching

## Architecture

```
┌─────────────────────────────────────┐
│           Applications              │
│         (ui, app, user apps)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     @upstash/redis-analytics        │
│  AnalyticsBackendClient (server)    │
│  AnalyticsClient (browser)          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Upstash Redis + Redis Search    │
└─────────────────────────────────────┘
```

## Package Structure

```
src/
  index.ts                 # barrel exports
  backend-client.ts        # AnalyticsBackendClient (server-side)
  client.ts                # AnalyticsClient (browser-side)
  types.ts                 # all shared types
  protocol.ts              # request/response contract
  utils.ts                 # helpers
  services/
    events.ts              # EventService
    sessions.ts            # SessionService
    feature-flags.ts       # FeatureFlagService
    schema-registry.ts     # SchemaRegistry
    search-index.ts        # SearchIndexService
    logging.ts             # LoggingService
```

## Usage

### Server-side (Next.js API route)

```typescript
import { AnalyticsBackendClient } from "@upstash/redis-analytics";

const client = new AnalyticsBackendClient({
  redis: {
    url: process.env.UPSTASH_REDIS_REST_URL!,
    token: process.env.UPSTASH_REDIS_REST_TOKEN!,
  },
  config: {
    // All config is optional — only override what you need
    session: { expirationMs: 7200000 },
    schemaValidation: { checkFrequency: 0.01 }, // validate ~1% of events to reduce costs
  },
});

// Single endpoint handler for Next.js
const handler = client.getHandler();
export const POST = handler;
export const GET = handler;

// Or use namespaced services directly
const session = await client.sessions.createSession();
await client.events.capturePageView(session.id, "/home");
const flags = await client.featureFlags.getDefinitions();
const logs = await client.logs.getLogs({ limit: 50 });
const info = await client.searchIndex.getInfo();
const schemas = await client.schemas.getAllSchemas();
```

### Browser-side (React/Next.js)

```typescript
import { AnalyticsClient } from "@upstash/redis-analytics";

const analytics = new AnalyticsClient({
  endpoint: "/api/analytics",
  flushInterval: 2000, // batch events, flush every 2s
});

const session = await analytics.createSession();
await analytics.capturePageView(session.id, "/home");
await analytics.captureClick(session.id, "signup-button");
```

### Middleware & Session Metadata

Add middleware to `getHandler()` for authentication and to attach metadata to sessions.
The 3rd generic parameter provides type safety for session metadata.

```typescript
import { AnalyticsBackendClient } from "@upstash/redis-analytics";

type MyEvents = { "custom:purchase": { productId: string; amount: number } };
type MyFlags = { theme: "light" | "dark" };
type MySessionMetadata = { userId: string; plan: string };

const client = new AnalyticsBackendClient<MyEvents, MyFlags, MySessionMetadata>({
  redis: { url: "...", token: "..." },
});

const handler = client.getHandler({
  middleware: async ({ request, analyticsRequest }) => {
    const token = request.headers.get("authorization");
    if (!token) {
      return new Response(JSON.stringify({ success: false, error: "Unauthorized" }), { status: 401 });
    }
    const user = await verifyToken(token);
    // Attach metadata to the session — stored in Redis, included in every event
    return { sessionMetadata: { userId: user.id, plan: user.plan } };
  },
});

export const POST = handler;
export const GET = handler;
```

Session metadata is automatically:
- Stored with the session in Redis
- Included in every captured event under `sessionMetadata`
- Registered in the schema registry for search index queryability

### Type Safety

```typescript
import { AnalyticsBackendClient, AnalyticsClient } from "@upstash/redis-analytics";

type MyEvents = {
  "custom:purchase": { productId: string; amount: number };
};

type MyFlags = {
  theme: "light" | "dark";
};

type MySessionMetadata = {
  userId: string;
  plan: string;
};

// Backend accepts 3 generic parameters: events, flags, session metadata
const backend = new AnalyticsBackendClient<MyEvents, MyFlags, MySessionMetadata>({ ... });

// Frontend client accepts events and flags
const frontend = new AnalyticsClient<MyEvents, MyFlags>({ ... });
```

## Dependencies

- `@upstash/redis` - Redis client with Redis Search support
- `@upstash/ratelimit` - Distributed rate limiting

## Development

This package is part of a monorepo using pnpm workspaces.
