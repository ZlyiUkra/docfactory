# @upstash/redis README 1.38.3 … 1.39.0: Upstash Redis
# джерело: https://registry.npmjs.org/@upstash/redis/-/redis-1.39.0.tgz
# отримано: 2026-10-16
# версія: redis-1.39.0, redis-1.38.4, redis-1.38.3

`@upstash/redis` is an HTTP/REST based Redis client for typescript, built on top
of Upstash REST API.

Tests
npm (scoped)
npm bundle size

> [!NOTE]
> **This project is in GA Stage.**
>
> The Upstash Professional Support fully covers this project. It receives regular updates, and bug fixes. The Upstash team is committed to maintaining and improving its functionality.

It is the only connectionless (HTTP based) Redis client and designed for:

- Serverless functions (AWS Lambda ...)
- Cloudflare Workers (see
  the example)
- Fastly Compute@Edge (see
  the example)
- Next.js, Jamstack ...
- Client side web/mobile applications
- WebAssembly
- and other environments where HTTP is preferred over TCP.

See
the list of APIs
supported.

## Quick Start

### Install

#### Node.js

```bash
npm install @upstash/redis
```

#### Deno

```ts
import { Redis } from "https://esm.sh/@upstash/redis";
```

### Create database

Create a new redis database on upstash

## Basic Usage:

```ts
import { Redis } from "@upstash/redis"

const redis = new Redis({
  url: <UPSTASH_REDIS_REST_URL>,
  token: <UPSTASH_REDIS_REST_TOKEN>,
})

// string
await redis.set('key', 'value');
let data = await redis.get('key');
console.log(data)

await redis.set('key3', 'value3', {ex: 1});

// sorted set
await redis.zadd('scores', { score: 1, member: 'team1' })
data = await redis.zrange('scores', 0, 100 )
console.log(data)

// list
await redis.lpush('elements', 'magnesium')
data = await redis.lrange('elements', 0, 100 )
console.log(data)

// hash
await redis.hset('people', {name: 'joe'})
data = await redis.hget('people', 'name' )
console.log(data)

// sets
await redis.sadd('animals', 'cat')
data  = await redis.spop('animals', 1)
console.log(data)
```

## Troubleshooting

We have a
dedicated page
for common problems. If you can't find a solution, please
open an issue.

## Docs

See the documentation for
details.

## Contributing

### Install Bun

### Database

Create a new redis database on upstash and copy
the url and token

### Running tests

```sh
bun run test
```

### Building

```sh
bun run build
```

### Telemetry

This library sends anonymous telemetry data to help us improve your experience.
We collect the following:

- SDK version
- Platform (Deno, Cloudflare, Vercel)
- Runtime version (node@18.x)
- Retry count of retried requests (to measure retry rates)

You can opt out by setting the `UPSTASH_DISABLE_TELEMETRY` environment variable
to any truthy value.

```sh
UPSTASH_DISABLE_TELEMETRY=1
```

Alternatively, you can pass `enableTelemetry: false` when initializing the Redis client:

```ts
const redis = new Redis({
  // ...,
  enableTelemetry: false,
});
```
