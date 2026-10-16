# @upstash/redis README 0.1.7 … 0.2.1: Upstash Redis
# джерело: https://registry.npmjs.org/@upstash/redis/-/redis-0.2.1.tgz
# отримано: 2026-10-16
# версія: redis-0.2.1, redis-0.2.0, redis-0.1.9, redis-0.1.8, redis-0.1.7

An HTTP/REST based Redis client built on top of Upstash REST API.

Tests
npm (scoped)
npm bundle size

It is the only connectionless (HTTP based) Redis client and designed for:

- Serverless functions (AWS Lambda ...)
- Cloudflare Workers (see the example)
- Fastly Compute@Edge
- Next.js, Jamstack ...
- Client side web/mobile applications
- WebAssembly
- and other environments where HTTP is preferred over TCP.

See the list of APIs supported.

## Quick Start

### Install

```bash
npm install @upstash/redis
```

### Usage with Promise

```typescript
import { auth, set } from '@upstash/redis';

auth('UPSTASH_REDIS_REST_URL', 'UPSTASH_REDIS_REST_TOKEN');

set('key', 'value').then(({ data }) => {
  console.log(data);
  // -> "OK"
});
```

### Usage with async/await

```typescript
import { set } from '@upstash/redis';

(async () => {
  try {
    const { data, error } = await set('key', 'value');
    if (error) throw error;
    console.log(data);
    // -> "OK"
  } catch (error) {
    console.error(error);
  }
})();
```

> If you define `UPSTASH_REDIS_REST_URL` and` UPSTASH_REDIS_REST_TOKEN` environment variables, you can skip the auth().

## Docs

See the documentation for details.
