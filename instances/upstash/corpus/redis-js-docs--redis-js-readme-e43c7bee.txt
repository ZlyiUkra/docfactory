# Upstash Redis
# джерело: https://github.com/upstash/redis-js/blob/v1.16.1/README.md
# отримано: 2026-10-16
# версія: redis-1.16.1

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
