# Cloudflare Workers Example
# джерело: https://github.com/upstash/redis-js/blob/v1.13.0/examples/cloudflare-workers-with-wrangler-1/README.md
# отримано: 2026-10-16
# версія: redis-1.13.0, redis-1.12.0, redis-1.11.0, redis-1.10.2, redis-1.10.1, redis-1.10.0, redis-1.9.0, redis-1.8.0, redis-1.7.0, redis-1.6.1

This example uses
Wrangler 1 to create a
typescript worker.

## How to use

1. Clone and install the example

```bash
git clone https://github.com/upstash/upstash-redis.git
cd upstash-redis/examples/cloudflare-workers-with-wrangler-1
npm install
```

2. Create a free Database on upstash.com
3. Copy the `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` to
   `wrangler.toml`
4. Start the development server

```bash
npm run dev
```

5. Open your browser at localhost:8787
