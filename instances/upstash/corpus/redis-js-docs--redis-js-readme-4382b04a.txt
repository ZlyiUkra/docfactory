# Upstash Redis
# джерело: https://github.com/upstash/redis-js/blob/v0.1.0/README.md
# отримано: 2026-10-16
# версія: redis-0.1.0

An HTTP/REST based Redis client built on top of Upstash REST API.

Tests

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
