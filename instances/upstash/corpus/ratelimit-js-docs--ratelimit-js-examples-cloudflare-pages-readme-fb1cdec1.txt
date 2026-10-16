# README
# джерело: https://github.com/upstash/ratelimit-js/blob/v2.2.0/examples/cloudflare-pages/README.md
# отримано: 2026-10-16
# версія: ratelimit-2.2.0, ratelimit-2.1.0, ratelimit-2.0.8, ratelimit-2.0.7, ratelimit-2.0.6, ratelimit-2.0.5, ratelimit-2.0.4, ratelimit-2.0.3, ratelimit-2.0.2, ratelimit-2.0.1, ratelimit-2.0.0, ratelimit-1.2.1, ratelimit-1.2.0

This is a Next.js project bootstrapped with `c3` which examplifies how one can use Upstash Ratelimit with Cloudflare Pages.

The project was initialized with (see CF guide):

```bash
npm create cloudflare@latest cloudflare-pages -- --framework=next
```

Then, the page.tsx file was updated with a simple page to test ratelimiting. An api endpoint was added in route.tsx. This is where we define the rate limit like the following:

```tsx
export const runtime = 'edge';

export const dynamic = 'force-dynamic';

import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

// Create a new ratelimiter
const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, "10 s"),
  prefix: "@upstash/ratelimit",
});

export async function GET(request: Request) {

  const identifier = "api";
  const { success, limit, remaining } = await ratelimit.limit(identifier);
  const response = {
    success: success,
    limit: limit,
    remaining: remaining
  }

  if (!success) {
    return new Response(JSON.stringify(response), { status: 429 });
  }
  return new Response(JSON.stringify(response));
}
```

## Getting Started

First, create an Upstash Redis through the Upstash console and set the environment variables `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`.

Then, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open http://localhost:3000 with your browser to see the result.

## Deployment

To deploy the project, simply set the environment variables `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` through the Environment Variables section under the Settings tab on the Cloudflare Dashboard. Then, run:

```bash
npm run deploy
```

Note: if you don't set the environment variables, you may get an error when deploying the project.
