# Upstash Rate Limit
# джерело: https://github.com/upstash/ratelimit-js/blob/v2.0.8/README.md
# отримано: 2026-10-16
# версія: ratelimit-2.0.8, ratelimit-2.0.7, ratelimit-2.0.6, ratelimit-2.0.5, ratelimit-2.0.4, ratelimit-2.0.3, ratelimit-2.0.2

npm (scoped)
Tests

> [!NOTE]
>  **This project is in GA Stage.**
> The Upstash Professional Support fully covers this project. It receives regular updates, and bug fixes. The Upstash team is committed to maintaining and improving its functionality.

It is the only connectionless (HTTP based) rate limiting library and designed
for:

- Serverless functions (AWS Lambda, Vercel ....)
- Cloudflare Workers & Pages
- Vercel Edge
- Fastly Compute@Edge
- Next.js, Jamstack ...
- Client side web/mobile applications
- WebAssembly
- and other environments where HTTP is preferred over TCP.

## Quick Start

### Install

#### npm

```bash
npm install @upstash/ratelimit
```

#### Deno

```ts
import { Ratelimit } from "https://cdn.skypack.dev/@upstash/ratelimit@latest";
```

### Create database

Create a new redis database on upstash. See here for documentation on how to create a redis instance.

### Basic Usage

```ts
import { Ratelimit } from "@upstash/ratelimit"; // for deno: see above
import { Redis } from "@upstash/redis"; // see below for cloudflare and fastly adapters

// Create a new ratelimiter, that allows 10 requests per 10 seconds
const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, "10 s"),
  analytics: true,
  /**
   * Optional prefix for the keys used in redis. This is useful if you want to share a redis
   * instance with other applications and want to avoid key collisions. The default prefix is
   * "@upstash/ratelimit"
   */
  prefix: "@upstash/ratelimit",
});

// Use a constant string to limit all requests with a single ratelimit
// Or use a userID, apiKey or ip address for individual limits.
const identifier = "api";
const { success } = await ratelimit.limit(identifier);

if (!success) {
  return "Unable to process at this time";
}
doExpensiveCalculation();
return "Here you go!";
```

For more information on getting started, you can refer to our documentation.

Here's a complete nextjs example

## Documentation

See the documentation for more information details about this package.

## Contributing

### Database

Create a new redis database on upstash and copy
the url and token.

### Running tests

To run the tests, you will need to set some environment variables. Here is a list of
variables to set:
- `UPSTASH_REDIS_REST_URL`
- `UPSTASH_REDIS_REST_TOKEN`
- `US1_UPSTASH_REDIS_REST_URL`
- `US1_UPSTASH_REDIS_REST_TOKEN`
- `APN_UPSTASH_REDIS_REST_URL`
- `APN_UPSTASH_REDIS_REST_TOKEN`
- `EU2_UPSTASH_REDIS_REST_URL`
- `EU2_UPSTASH_REDIS_REST_TOKEN`

You can create a single Upstash Redis and use its URL and token for all four above.

Once you set the environment variables, simply run:
```sh
pnpm test
```
