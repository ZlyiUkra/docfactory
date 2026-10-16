# Upstash Workflow Cloudflare Workers Example (with Hono)
# джерело: https://github.com/upstash/qstash-js/blob/v2.12.0/examples/workflow/cloudflare-workers-hono/README.md
# отримано: 2026-10-16
# версія: qstash-2.12.0, qstash-2.11.3, qstash-2.11.2, qstash-2.11.1, qstash-2.11.0, qstash-2.10.1, qstash-2.10.0, qstash-2.9.1, qstash-2.9.0, qstash-2.8.4, qstash-2.8.3, qstash-2.8.2, qstash-2.8.1, qstash-2.8.0, qstash-2.7.23, qstash-2.7.22, qstash-2.7.21, qstash-2.7.20, qstash-2.7.19, qstash-2.7.18, qstash-2.7.17, qstash-2.7.16, qstash-2.7.15, qstash-2.7.14, qstash-2.7.13, qstash-2.7.12, qstash-2.7.11

This is an example of how to use Upstash Workflow with Cloudflare Workers with Hono router. You can learn more in Workflow documentation for Hono.

Deploy to Cloudflare Workers
**Note:** After deploying with the button above, you need to set the environment variables `QSTASH_URL` and `QSTASH_TOKEN`.

## Development

> [!TIP]
> You can use the `bootstrap.sh` script to run this example with a local tunnel.
>
> Simply set the environment variables as explained below and run the following command in the `qstash-js/examples/workflow` directory:
>
> ```
> bash bootstrap.sh cloudflare-workers-hono
> ```

1. Install the dependencies

```bash
npm install
```

2. Get the credentials from the Upstash Console and add them to the `.dev.vars` file.

```bash
QSTASH_URL=
QSTASH_TOKEN=
```

3. Open a local tunnel to port of the development server

```bash
ngrok http 3001
```

Also, set the `UPSTASH_WORKLFOW_URL` environment variable to the public url provided by ngrok.

4. Run the development server

```bash
npm run dev
```

5. Send a `POST` request to the `/workflow` endpoint.

```bash
curl -X POST "http://localhost:3001/workflow" -d '{"text": "hello world!"}'
```

## Deployment

You can use wrangler to deploy the project to Cloudflare Workers.

```bash
npm run deploy
```

Then, go to cloudflare dashboard and find your project. Add the
`QSTASH_TOKEN` environment variable and re-deploy the project.

Once the project is re-deployed, you can send a curl request
like the one above (after replacing the localhost with the
deployment URL).
