# README
# джерело: https://github.com/upstash/workflow-js/blob/v0.1.2/examples/nuxt/README.md
# отримано: 2026-10-16
# версія: workflow-0.1.2, workflow-0.1.1, workflow-0.1.0

Deploy with Vercel

## Upstash Workflow Nuxt Example

This project has some routes showcasing how Upstash Workflow can be used in a nuxt project. You can learn more in Workflow documentation for Nuxt.

Under the `server/api` directory, you will find 6 files, each corresponding to a workflow API except the `callQstash`.

Here is what these `callQstash` endpoint does: The user calls `callQstash` with information about which endpoint is to be called in the body. `callQstash` publishes a message to QStash. QStash then calls the specified endpoint.

To run the app locally, first set the environment variables `QSTASH_URL`, `QSTASH_TOKEN`, `QSTASH_CURRENT_SIGNING_KEY` and `QSTASH_NEXT_SIGNING_KEY`. You can find the values of the env variables from the Upstash Console. `QSTASH_URL` should be `https://qstash.upstash.io`.

> [!WARNING]
> When adding workflow to your own app, don't forget to add `QSTASH_URL`, `QSTASH_TOKEN`, `QSTASH_CURRENT_SIGNING_KEY` and `QSTASH_NEXT_SIGNING_KEY` to `nuxt.config.ts`:
>
> ```diff
> // nuxt.config.ts
> export default defineNuxtConfig({
>   compatibilityDate: '2024-04-03',
>   devtools: { enabled: true },
> + runtimeConfig: {
> +   QSTASH_URL: process.env.QSTASH_URL,
> +   QSTASH_TOKEN: process.env.QSTASH_TOKEN,
> +   QSTASH_CURRENT_SIGNING_KEY: process.env.QSTASH_CURRENT_SIGNING_KEY,
> +   QSTASH_NEXT_SIGNING_KEY: process.env.QSTASH_NEXT_SIGNING_KEY,
> + },
>   css: ['~/assets/css/main.css'],
>   postcss: {
>     plugins: {
>       tailwindcss: {},
>       autoprefixer: {},
>     },
>   },
> })
> ```

Once you have the environment variables set, you can run the project with:

```
npm run dev
```

You can go to the deployment and call the endpoints using the form on the page. Simply enter the deployment URL and pick an endpoint.

Here is an example payload you can use for invoice:

```json
{"date":123,"email":"my@mail.com","amount":10}
```

You can observe the logs at Upstash console to see your workflow operate.
