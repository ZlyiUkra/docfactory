# ʕ •́؈•̀) `worker-typescript-template`
# джерело: https://github.com/upstash/redis-js/blob/v1.3.5/examples/cloudflare-service-worker/README.md
# отримано: 2026-10-16
# версія: redis-1.3.5, redis-1.3.4, redis-1.3.3, redis-1.3.2

A batteries included template for kick starting a TypeScript Cloudflare worker
project.

## Note: You must use wrangler 1.17 or newer to use this template.

## 🔋 Getting Started

This template is meant to be used with
Wrangler. If you are not already
familiar with the tool, we recommend that you install the tool and configure it
to work with your Cloudflare account.
Documentation can be found
here.

To generate using Wrangler, run this command:

```bash
wrangler generate my-ts-project https://github.com/cloudflare/worker-typescript-template
```

### 👩 💻 Developing

`src/index.ts` calls the request handler in
`src/handler.ts`, and will return the
request method
for the given request.

### 🧪 Testing

This template comes with jest tests which simply test that the request handler
can handle each request method. `npm test` will run your tests.

### ✏️ Formatting

This template uses `prettier` to format the project. To
invoke, run `npm run format`.

### 👀 Previewing and Publishing

For information on how to preview and publish your worker, please see the
Wrangler docs.

## 🤢 Issues

If you run into issues with this specific project, please feel free to file an
issue here.
If the problem is with Wrangler, please file an issue
here.

## ⚠️ Caveats

The `service-worker-mock` used by the tests is not a perfect representation of
the Cloudflare Workers runtime. It is a general approximation. We recommend that
you test end to end with `wrangler dev` in addition to a
staging environment
to test things before deploying.
