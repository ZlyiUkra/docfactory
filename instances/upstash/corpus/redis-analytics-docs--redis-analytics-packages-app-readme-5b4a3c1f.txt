# @analytics/app
# джерело: https://github.com/upstash/redis-analytics/blob/a7e0afc8a694dad44777c4172e14d955d5e8f640/packages/app/README.md
# отримано: 2026-10-16

Demo and test application showcasing the analytics platform integration. Built with Next.js and React Query.

## Purpose

The app package serves as:

- **Demo Application**: Showcases how to integrate `@upstash/redis-analytics` into a Next.js application
- **Testing Environment**: Provides a controlled environment for testing the analytics package
- **Integration Example**: Demonstrates best practices for implementation

## Key Features

### Frontend Integration Examples

- Client-side event tracking with `AnalyticsClient`
- Auto-capture page views on route change
- Manual event tracking (clicks, custom events)
- Feature flag usage in UI
- Session management with backend-assigned feature flags

### Backend Integration Examples

- Server-side analytics with `AnalyticsBackendClient`
- Single API route handler via `getHandler()`
- Feature flag management
- Admin operations

### Demo Pages

- **Home**: Overview and getting started
- **Products**: Example e-commerce flow with tracking
- **Checkout**: Purchase flow with analytics
- **Docs**: Interactive documentation with code examples

## Technology Stack

- **Framework**: Next.js (App Router)
- **Styling**: Tailwind CSS
- **Data Fetching**: React Query (TanStack Query)
- **State Management**: React Context + React Query
- **Analytics**: `@upstash/redis-analytics`

## Installation

```bash
pnpm install
```

## Development

```bash
pnpm dev
```

## Environment Variables

```env
UPSTASH_REDIS_REST_URL=https://your-redis-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token
```

## Usage Examples

### Backend Setup

```typescript
// lib/analytics.ts
import { AnalyticsBackendClient } from "@upstash/redis-analytics";

const client = new AnalyticsBackendClient<CustomEvents>({
  redis: {
    url: process.env.UPSTASH_REDIS_REST_URL!,
    token: process.env.UPSTASH_REDIS_REST_TOKEN!,
  },
  config: CONFIG,
});

// app/api/analytics/route.ts
const handler = client.getHandler({
  middleware: ({ analyticsRequest }) => {
    if (analyticsRequest.requestType !== "createSession") return;
    return {
      featureFlags: { theme: "dark", newCheckout: "enabled" },
    };
  },
});
export const POST = handler;
export const GET = handler;
```

### Frontend Setup

```typescript
// lib/analytics-provider.tsx
import { AnalyticsClient } from "@upstash/redis-analytics";

const client = new AnalyticsClient<CustomEvents, FeatureFlags>({
  endpoint: "/api/analytics",
  flushInterval: 2000,
});

// Flags are assigned by backend middleware
const session = await client.createSession();
```

### Feature Flag Usage

```typescript
const { data: theme } = useFeatureFlag("theme");

return (
  <header className={theme === "dark" ? "dark" : "light"}>
    <h1>My App</h1>
  </header>
);
```

## Development

This package is part of a monorepo using pnpm workspaces.
