# Local Development
# джерело: https://github.com/upstash/ratelimit-js/blob/v2.2.0/examples/cloudflare-workers/README.md
# отримано: 2026-10-16
# версія: ratelimit-2.2.0, ratelimit-2.1.0, ratelimit-2.0.8, ratelimit-2.0.7, ratelimit-2.0.6, ratelimit-2.0.5, ratelimit-2.0.4, ratelimit-2.0.3, ratelimit-2.0.2, ratelimit-2.0.1, ratelimit-2.0.0, ratelimit-1.2.1

For testing the app locally, start by creating an Upstash Redis. Next, create the `.dev.vars` file under `cloudflare-workers` directory and set the `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` environment variables:

```
// .dev.vars
UPSTASH_REDIS_REST_URL="****"
UPSTASH_REDIS_REST_TOKEN="****"
```

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
