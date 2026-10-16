# @upstash/redis README 0.1.22: Upstash Redis
# джерело: https://registry.npmjs.org/@upstash/redis/-/redis-0.1.22.tgz
# отримано: 2026-10-16
# версія: redis-0.1.22

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

### Usage with Callback Style

```typescript
import upstash from '@upstash/redis';

const redis = upstash('UPSTASH_REDIS_REST_URL', 'UPSTASH_REDIS_REST_TOKEN');

redis.get('key', function ({ data, error }) {
  if (error) {
    return console.error(error);
  }
  console.log(data);
});
```

### Usage with async/await (Promise)

```typescript
import upstash from '@upstash/redis';

const redis = upstash('UPSTASH_REDIS_REST_URL', 'UPSTASH_REDIS_REST_TOKEN');

(async () => {
  try {
    const { data, error } = await redis.get('key');
    if (error) throw error;
    console.log(data);
  } catch (error) {
    console.error(error);
  }
})();
```

If you define `UPSTASH_REDIS_REST_URL` and` UPSTASH_REDIS_REST_TOKEN` environment variables, you can run the Redis commands directly.

```typescript
import { get } from '@upstash/redis';

(async () => {
  try {
    const { data, error } = await get('key');
    if (error) throw error;
    console.log(data);
  } catch (error) {
    console.error(error);
  }
})();
```

### Edge Support

> Only GET requests are supported in Edge Caching. As a result, write/update commands are not supported.

```typescript
import upstash from '@upstash/redis';

const redis = upstash({
  url: 'UPSTASH_REDIS_REST_URL',
  token: 'UPSTASH_REDIS_REST_TOKEN',
  edgeUrl: 'UPSTASH_REDIS_EDGE_URL',
});

(async () => {
  try {
    const { data, error, metadata } = await redis.get('key');
    if (error) throw error;
    console.log(data);
    // -> null | string
    console.log(metadata);
    // -> { edge: boolean, cache: null | 'miss' | 'hit' }
  } catch (error) {
    console.error(error);
  }
})();
```
