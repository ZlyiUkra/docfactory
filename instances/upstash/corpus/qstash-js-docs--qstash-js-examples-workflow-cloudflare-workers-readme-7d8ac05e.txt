# QStash Workflow Cloudflare Workers Example
# джерело: https://github.com/upstash/qstash-js/blob/v2.7.10/examples/workflow/cloudflare-workers/README.md
# отримано: 2026-10-16
# версія: qstash-2.7.10, qstash-2.7.9, qstash-2.7.8, qstash-2.7.7, qstash-2.7.6, qstash-2.7.5, qstash-2.7.4, qstash-2.7.3, qstash-2.7.2, qstash-2.7.1, qstash-2.7.0

This is an example of how to use QStash Workflow with Cloudflare Workers. You can learn more in Workflow documentation for Cloudflare Workers.

Deploy to Cloudflare Workers
**Note:** After deploying with the button above, you need to set the environment variables `QSTASH_URL` and `QSTASH_TOKEN`.

## Development

> [!TIP]
> You can use the `bootstrap.sh` script to run this example with a local tunnel.
>
> Simply set the environment variables as explained below and run the following command in the `qstash-js/examples/workflow` directory:
>
> ```
> bash bootstrap.sh cloudflare-workers
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

5. Send a `POST` request to the endpoint.

```bash
curl -X POST "http://localhost:3001" -d '{"text": "hello world!"}'
```

## Deployment

You can use wrangler to deploy the project to Cloudflare Workers.

```bash
npm run deploy
```
