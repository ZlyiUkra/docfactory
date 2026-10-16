# README
# джерело: https://github.com/upstash/edge-flags/blob/@upstash%2Fedge-flags@0.1.3/README.md
# отримано: 2026-10-16
# версія: edge-flags-0.1.3, edge-flags-0.1.2

    Edge Flags
    Feature Flags for the Edge

  edge-flags.vercel.app

> [!NOTE]
> **This project is a Community Project.**
>
> The project is maintained and supported by the community. Upstash may contribute but does not officially support or assume responsibility for it.

Edge Flags is a low latency feature flagging solution running at the edge and storing data in a global Redis database. It is designed to be used with Next.js and Vercel but we will soon roll out support for other popular frameworks and platforms. Let us know what you are looking for!

## Features

- **Global Low latency:** Flags are stored in a global Redis database and are evaluated at the edge.
- **Environments:** Flags have different environments to support your deployment process: `production`, `preview` and `development`
- **Flexible:** Flags support geo targeting, percentage based rollouts and custom attributes
- **Manage:** Flags can be created and managed using the SDK or the self-hosted dashboard in this repo.
- **Free:** Edge Flags is free to use. You only pay for the Redis database.
- **Cache:** Flags can be cached for a short period of time to reduce the required requests to redis, making it cheaper to use.

## Docs

This readme provides a quickstart guide. For more information, see our docs.

## Architecture

## Quickstart

1. Create a redis database

Go to console.upstash.com/redis and create
a new global database.

After creating the db, copy the `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` to your `.env` file.

2.  Run `npx @upstash/edge-flags-dashboard` in your project to open the self-hosted dashboard.

```bash
npx @upstash/edge-flags-dashboard
```

You can also use the hosted version at https://edge-flags-dashboard.vercel.app.

3.  Create a flag from the dashboard. See our docs for more information.

4.  Install `@upstash/edge-flags` in your project

```bash
npm install @upstash/edge-flags
```

4. Create an edge function in your project

```ts
// /app/api/edge-flags/route.ts
import { createEdgeHandler } from "@upstash/edge-flags";

export const GET = createEdgeHandler({
  cacheMaxAge: 0, // cache time in seconds, 0 disables the cache
  redisUrl: process.env.UPSTASH_REDIS_REST_URL!, // omit to load from env automatically
  redisToken: process.env.UPSTASH_REDIS_REST_TOKEN!, // omit to load from env automatically
});

export const runtime = "edge";
```

5. Query the flag in your frontend

```tsx
// /app/page.tsx
import { useFlag } from "@upstash/edge-flags";

export default function Example() {
  const { isEnabled, isLoading, error } = useFlag("flag-name");

  if (error) return <div>Error: {error}</div>;
  if (isLoading) return <div>Loading...</div>;

  return <div>Is my feature enabled: {isEnabled}</div>;
}
```

## Custom attributes

`useFlag` accepts an optional object that can be used to pass custom attributes
to be evaluated in the flag rules.

```tsx
const attributes = {
  userId: "chronark",
  role: "admin",
};

useFlag("flag-name", attributes);
```

## Development

This monorepo is managed by turborepo and uses `pnpm` for dependency management.

#### Install dependencies

```bash
pnpm install
```

#### Build

```bash
pnpm build
```

## Database Schema

All configuration is stored in Redis `String` data types. Each flag is
accessible through a key like

```
STRING
edge-flags:{TENANT}:flags:{FLAG_NAME}:{ENVIRONMENT}
```

In addition to the flags, there will be a single set that contains all the flag IDs. We can not guarantee the database is only used for edge-flags so we need to keep track of the flags we have created instead of using a potentially expensive
`SCAN` operation.

```
SET
edge-flags:{TENANT}:flags
```

- `TENANT` is currently unused (set as `default`) but reserved for future use.
  ie for managing multiple projects int a single database
- `FLAG_NAME` is the unique identifier for the flag
- `ENVIRONMENT` is the environment the flag is targeting. ie `production`,
  `preview`, `development`

### Packages

- **/packages/sdk:** The SDK to be imported into your project
- **/packages/dashboard:** A dashboard for creating and updating your flags
- **/examples/nextjs:** An example Next.js app using the SDK

## Authors

This project was originally created by

- @ademilter
- @chronark\_
- @enesakar
