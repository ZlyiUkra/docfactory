# Local Development
# джерело: https://github.com/upstash/ratelimit-js/blob/v1.2.0/examples/cloudflare-workers/README.md
# отримано: 2026-10-16
# версія: ratelimit-1.2.0, ratelimit-1.1.3, ratelimit-1.1.2, ratelimit-1.1.1, ratelimit-1.1.0

For testing the app locally, set the `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` environment variables after creating an Upstash Redis.

Then, simply run:

```
npx wrangler dev
```

## Deploy on Cloudflare

To deploy the app, set the environment variables with the following lines. In both cases, you will be prompted to enter the secret value:

```
npx wrangler secret put UPSTASH_REDIS_REST_URL
npx wrangler secret put UPSTASH_REDIS_REST_TOKEN
```

Then, deploy the project with:

```
npx wrangler deploy
```
