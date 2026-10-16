# Upstash Redis
# джерело: https://github.com/upstash/redis-js/blob/v1.16.0/README.md
# отримано: 2026-10-16
# версія: redis-1.16.0, redis-1.15.1, redis-1.15.0, redis-1.14.0, redis-1.13.1, redis-1.13.0, redis-1.12.0, redis-1.11.0, redis-1.10.2, redis-1.10.1, redis-1.10.0, redis-1.9.0, redis-1.8.0, redis-1.7.0, redis-1.6.1

`@upstash/redis` is an HTTP/REST based Redis client for typescript, built on top
of Upstash REST API.

Tests

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

#### npm

```bash
npm install @upstash/redis
```

#### Deno

```ts
import { Redis } from "https://deno.land/x/upstash_redis/mod.ts";
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

await redis.set('key2', 'value2', {ex: 1});

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

### Upgrading to v1.4.0 **(ReferenceError: fetch is not defined)**

If you are running on nodejs v17 and earlier, `fetch` will not be natively
supported. Platforms like Vercel, Netlify, Deno, Fastly etc. provide a polyfill
for you. But if you are running on bare node, you need to either specify a
polyfill yourself or change the import path to:

```typescript
import { Redis } from "@upstash/redis/with-fetch";
```

### Upgrading from v0.2.0?

Please read the
migration guide.
For further explanation we wrote a
blog post.

## Docs

See the documentation for
details.

## Contributing

### Install Deno

### Database

Create a new redis database on upstash and copy
the url and token

### Running tests

```sh
UPSTASH_REDIS_REST_URL=".." UPSTASH_REDIS_REST_TOKEN=".." deno test -A
```

```
```
