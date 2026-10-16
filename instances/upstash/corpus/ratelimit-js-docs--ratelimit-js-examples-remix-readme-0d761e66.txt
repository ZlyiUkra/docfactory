# @upstash/ratelimit in Remix
# джерело: https://github.com/upstash/ratelimit-js/blob/v2.2.0/examples/remix/README.md
# отримано: 2026-10-16
# версія: ratelimit-2.2.0, ratelimit-2.1.0, ratelimit-2.0.8, ratelimit-2.0.7, ratelimit-2.0.6, ratelimit-2.0.5, ratelimit-2.0.4, ratelimit-2.0.3, ratelimit-2.0.2, ratelimit-2.0.1, ratelimit-2.0.0, ratelimit-1.2.1, ratelimit-1.2.0, ratelimit-1.1.3, ratelimit-1.1.2, ratelimit-1.1.1, ratelimit-1.1.0, ratelimit-1.0.3, ratelimit-1.0.1, ratelimit-1.0.0, ratelimit-0.4.4, ratelimit-0.4.3, ratelimit-0.4.2, ratelimit-0.4.1, ratelimit-0.4.0

This example shows how to use `@upstash/ratelimit` in a Remix app.

## Getting Started

Create a database on Upstash and copy the `Upstash_REDIS_REST_URL` and `Upstash_REDIS_REST_TOKEN` from the database settings to your `.env` file.

Then add a `loader` to your route like this:

```tsx
import { json } from "@remix-run/node";
import type { LoaderArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.fixedWindow(10, "60 s"),
  analytics: true,
});

export const loader = async (args: LoaderArgs) => {
  // getting the ip can be different depending on your hosting provider
  const ip = args.request.headers.get("X-Forwarded-For") ?? args.request.headers.get("x-real-ip");
  const identifier = ip ?? "global";
  const { success, limit, remaining, reset } = await ratelimit.limit(identifier);
  return json(
    {
      success,
      limit,
      remaining,
      reset,
      identifier,
    },
    {
      headers: {
        "X-RateLimit-Limit": limit.toString(),
        "X-RateLimit-Remaining": remaining.toString(),
        "X-RateLimit-Reset": reset.toString(),
      },
    },
  );
};

export default function Index() {
  const ratelimitResponse = useLoaderData<typeof loader>();

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", lineHeight: "1.4" }}>
      <h1>Welcome to @upstash/ratelimit in Remix app</h1>
      <code>
        <pre>{JSON.stringify(ratelimitResponse, null, 2)}</pre>
      </code>
    </div>
  );
}
```
