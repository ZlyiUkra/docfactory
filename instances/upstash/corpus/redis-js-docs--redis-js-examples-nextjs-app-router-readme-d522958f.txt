# Next.js 14 - App Router Example
# джерело: https://github.com/upstash/redis-js/blob/v1.36.4/examples/nextjs-app-router/README.md
# отримано: 2026-10-16
# версія: redis-1.36.4, redis-1.36.3, redis-1.36.2, redis-1.36.1, redis-1.36.0, redis-1.35.8, redis-1.35.7, redis-1.35.6, redis-1.35.5, redis-1.35.4, redis-1.35.3, redis-1.35.2, redis-1.35.1, redis-1.35.0, redis-1.34.9, redis-1.34.8, redis-1.34.7, redis-1.34.6, redis-1.34.5, redis-1.34.4, redis-1.34.3, redis-1.34.2, redis-1.34.1

### Project Setup

Clone the example and install dependencies

```shell
git clone https://github.com/upstash/redis-js.git
cd redis-js/examples/nextjs-app-router
npm install
```

### Database Setup

Create a Redis database using Upstash Console or Upstash CLI and copy the `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` into your `.env` file.

```shell
UPSTASH_REDIS_REST_URL=<YOUR_URL>
UPSTASH_REDIS_REST_TOKEN=<YOUR_TOKEN>
```

### Run & Deploy

Run the app locally with `npm run dev`, check `http://localhost:3000/`

Deploy your app with `vercel`
