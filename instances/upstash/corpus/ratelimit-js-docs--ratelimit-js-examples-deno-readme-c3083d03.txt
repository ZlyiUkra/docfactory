# Deno Examples
# джерело: https://github.com/upstash/ratelimit-js/blob/v2.2.0/examples/deno/README.md
# отримано: 2026-10-16
# версія: ratelimit-2.2.0, ratelimit-2.1.0, ratelimit-2.0.8, ratelimit-2.0.7, ratelimit-2.0.6, ratelimit-2.0.5, ratelimit-2.0.4, ratelimit-2.0.3, ratelimit-2.0.2, ratelimit-2.0.1, ratelimit-2.0.0, ratelimit-1.2.1, ratelimit-1.2.0

This directory has two deno examples.

| File            | Description |
| --------------- | ----------- |
| `deprecated.ts` | Deno app with the `serve` method which was deprecated with Deno version `0.107.0`. |
| `main.ts`       | Up-to-date Deno app with the `Deno.serve` method |

To run the apps locally, simply set the environment variables `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` and run:

```
deno run --allow-net --allow-env main.ts
```
