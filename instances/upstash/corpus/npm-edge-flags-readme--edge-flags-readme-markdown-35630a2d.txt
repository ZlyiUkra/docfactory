# @upstash/edge-flags README 0.0.12 … 0.0.15
# джерело: https://registry.npmjs.org/@upstash/edge-flags/-/edge-flags-0.0.15.tgz
# отримано: 2026-10-16
# версія: edge-flags-0.0.15, edge-flags-0.0.14, edge-flags-0.0.13, edge-flags-0.0.12

    Edge Flags
    Low latency feature flags at the edge

  edge-flags.vercel.app

TODO: Add description

## Powered by

- Upstash Global Redis Database
- Next.js
- Vercel

Arch

## Quickstart

1. Install `@upstash/edge-flags` in your project

```bash
npm install @upstash/edge-flags
```

2. Create an edge function in your project

```ts
// /api/edge-flags.ts
import { createHandler } from "@upstash/edge-flags";

export default createHandler({
	redisUrl: process.env.UPSTASH_REDIS_REST_URL!,
	redisToken: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

/**
 * Edge flags only works on edge functions, it will break if you do not set the runtime
 */
export const config = {
	runtime: "experimental-edge",
};
```

3. Query the flag in your frontend

```ts
// /app/index.tsx
import { useFlag } from "@upstash/edge-flags";

const { isLoading, value, error } = useFlag("my-flag");

if (error) return <div>Error: {error}</div>;
if (isLoading) return <div>Loading...</div>;

return <div>Is my feature enabled: {value}</div>;
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

All configuration is stored in Redis `String` data types. Each flag is accessible through a key like

```
STRING
edge-flags:{TENANT}:flags:{FLAG_ID}:{ENVIRONMENT}
```
In addition to the flags, there will be a single set that contains all the flag IDs.
We can not guarantee the database is only used for edge-flags so we need to keep track of the flags we have created instead of using a potentially expensive `SCAN` operation.
```
SET
edge-flags:{TENANT}:flags
```

- `TENANT` is currently unused (set as `default`) but reserved for future use. ie for managing multiple projects int a single database
- `FLAG_ID` is the unique identifier for the flag
- `ENVIRONMENT` is the environment the flag is targeting. ie `production`, `preview`, `development`

### Packages

- **/packages/sdk:** The SDK to be imported into your project
- **/packages/web:** The management interface you can selfhost Link
- **/examples/nextjs:** TODO: An example Next.js app using the SDK
- **/examples/nextjs12:** TODO: Using the SDK with Next.js 12

## Authors

This project was originally created by
- @ademilter
- @chronarkdotdev
- @enesakar
