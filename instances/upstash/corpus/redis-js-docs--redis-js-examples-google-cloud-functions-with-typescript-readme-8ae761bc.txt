# Google Cloud Functions Example with Typescript
# джерело: https://github.com/upstash/redis-js/blob/v1.34.0/examples/google-cloud-functions-with-typescript/README.md
# отримано: 2026-10-16
# версія: redis-1.34.0, redis-1.33.0, redis-1.32.0, redis-1.31.6, redis-1.31.5, redis-1.31.4, redis-1.31.3, redis-1.31.2, redis-1.31.1, redis-1.31.0, redis-1.30.1, redis-1.30.0, redis-1.29.0, redis-1.28.4, redis-1.28.3, redis-1.28.2, redis-1.28.1, redis-1.28.0, redis-1.27.1, redis-1.27.0, redis-1.26.0, redis-1.25.2, redis-1.25.1, redis-1.25.0, redis-1.24.3, redis-1.24.2, redis-1.24.1, redis-1.24.0, redis-1.23.4

## How to use

1. Clone and install the example

```bash
git clone https://github.com/upstash/upstash-redis.git
cd upstash-redis/examples/google-cloud-functions
npm install
```

2. Create a free Database on upstash.com
3. Copy the `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` to
   `Runtime, build, connections and security settings > Runtime environment variables`
   in GCP website when creating a new function or pass those keys when you are
   deploying from the CLI.

## Work locally

Simply run `npm run start`
