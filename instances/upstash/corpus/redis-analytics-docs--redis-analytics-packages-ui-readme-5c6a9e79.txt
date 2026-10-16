# @analytics/ui
# джерело: https://github.com/upstash/redis-analytics/blob/a7e0afc8a694dad44777c4172e14d955d5e8f640/packages/ui/README.md
# отримано: 2026-10-16

Analytics dashboard for viewing, analyzing, and managing analytics data. Built with Next.js, shadcn/ui, and React Query.

## Purpose

The UI package provides a comprehensive web-based dashboard for:

- Viewing and analyzing captured events
- Filtering events by various criteria
- Visualizing data with charts and graphs
- Managing feature flags
- Viewing system logs
- Monitoring search index health

Uses `@upstash/redis-analytics` for all backend operations via `AnalyticsBackendClient` with namespaced service access.

## Key Features

### Explore Tab

- **Table View**: Display events in a sortable, paginated table
- **Graph View**: Visualize event counts over time with charts (using Redis Search aggregations)
- **Advanced Filtering**: Filter by event name, properties, session ID, feature flags
- **Time Range Selection**: Quick filters (15 min, 1 hour, 6 hours, 24 hours, 7 days, 30 days) and custom ranges

### System Logs Tab

- View all system activity and changes
- Filter by log type (schema updates, feature flag changes, rate limits, errors, index updates)
- View before/after comparisons for updates

### Configuration Management

- **Feature Flags**: Create, edit feature flags with default values and distributions
- **Event Schemas**: View custom event schemas and first-seen timestamps
- **Search Index**: View index status, trigger rebuilds, check schema drift

## API Routes

All admin API routes use `AnalyticsBackendClient` with namespaced services:

```typescript
import { getAnalyticsBackendClient } from "@/lib/analytics";

const client = getAnalyticsBackendClient();

// Feature flags
await client.featureFlags.getDefinitions();
await client.featureFlags.defineFlag(config);
await client.featureFlags.updateFlag(name, update);

// Schemas
await client.schemas.getAllSchemas();
await client.schemas.getCustomEventFirstSeen();

// Logs
await client.logs.getLogs({ type, limit, offset });

// Search index
await client.searchIndex.getInfo();
await client.searchIndex.checkSchemaDrift();
await client.searchIndex.rebuild();
```

Events query and aggregation routes use `@upstash/redis` directly for complex Redis Search queries (filters, aggregation pipelines).

## Technology Stack

- **Framework**: Next.js (App Router)
- **UI Components**: shadcn/ui
- **Styling**: Tailwind CSS
- **Data Fetching**: React Query (TanStack Query)
- **Charts**: Recharts
- **Analytics Backend**: `@upstash/redis-analytics`

## Installation

```bash
pnpm install
```

## Development

```bash
pnpm dev
```

The dashboard will be available at `http://localhost:3001`.

## Environment Variables

```env
UPSTASH_REDIS_REST_URL=https://your-redis-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token
```

## Development

This package is part of a monorepo using pnpm workspaces.
