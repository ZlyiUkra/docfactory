# README
# джерело: https://github.com/upstash/qstash-js/blob/v2.12.0/examples/workflow/nuxt/README.md
# отримано: 2026-10-16
# версія: qstash-2.12.0, qstash-2.11.3, qstash-2.11.2, qstash-2.11.1, qstash-2.11.0, qstash-2.10.1, qstash-2.10.0, qstash-2.9.1, qstash-2.9.0, qstash-2.8.4, qstash-2.8.3, qstash-2.8.2, qstash-2.8.1, qstash-2.8.0, qstash-2.7.23, qstash-2.7.22, qstash-2.7.21, qstash-2.7.20, qstash-2.7.19, qstash-2.7.18, qstash-2.7.17, qstash-2.7.16, qstash-2.7.15, qstash-2.7.14, qstash-2.7.13, qstash-2.7.12, qstash-2.7.11

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
