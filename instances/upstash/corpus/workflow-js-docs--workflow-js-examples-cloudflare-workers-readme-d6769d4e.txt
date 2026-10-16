# Upstash Workflow Cloudflare Workers Example
# джерело: https://github.com/upstash/workflow-js/blob/v0.2.13/examples/cloudflare-workers/README.md
# отримано: 2026-10-16
# версія: workflow-0.2.13, workflow-0.2.12, workflow-0.2.11, workflow-0.2.10, workflow-0.2.9, workflow-0.2.8, workflow-0.2.7, workflow-0.2.6, workflow-0.2.5, workflow-0.2.4, workflow-0.2.3, workflow-0.2.2, workflow-0.2.1, workflow-0.2.0, workflow-0.1.5, workflow-0.1.4, workflow-0.1.3

This is an example of how to use Upstash Workflow with Cloudflare Workers. You can learn more in Workflow documentation for Cloudflare Workers.

Deploy to Cloudflare Workers
**Note:** After deploying with the button above, you need to set the environment variables `QSTASH_URL` and `QSTASH_TOKEN`.

## Development

> [!TIP]
> You can use the `bootstrap.sh` script to run this example with a local tunnel.
>
> Simply set the environment variables as explained below and run the following command in the `workflow-js/examples` directory:
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

Then, go to cloudflare dashboard and find your project. Add the
`QSTASH_TOKEN` environment variable and re-deploy the project.

Once the project is re-deployed, you can send a curl request
like the one above (after replacing the localhost with the
deployment URL).
