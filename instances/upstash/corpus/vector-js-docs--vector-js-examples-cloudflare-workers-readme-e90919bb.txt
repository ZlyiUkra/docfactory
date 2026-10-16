# Upstash Vector & Cloudflare Workers Example
# джерело: https://github.com/upstash/vector-js/blob/v1.2.3/examples/cloudflare-workers/README.md
# отримано: 2026-10-16
# версія: vector-1.2.3, vector-1.2.2, vector-1.2.1, vector-1.2.0

In this example, you can find how you can use Upstash Vector with Cloudflare Workers.

The client is initialized in `/src/index.ts` folder like:

```ts
export default {
  async fetch(request, env, ctx): Promise<Response> {

    const index = new Index({
      url: env.UPSTASH_VECTOR_REST_URL,
      token: env.UPSTASH_VECTOR_REST_TOKEN,
      cache: false,
    })

    // ...
  }
}
```

## Local Development

First, install the dependencies with:

```
npm install
```

Then, create a `.dev.vars` file and fill the environment variables:

```
UPSTASH_VECTOR_REST_URL="***"
UPSTASH_VECTOR_REST_TOKEN="***"
```

Finally, run:

```
npm run dev
```

## Deployment

You can deploy with:

```
npm run deploy
```

Then, set the environment variables in your project and start using the app on Cloudflare!
