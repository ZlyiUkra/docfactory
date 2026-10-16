# Upstash Workflow Cloudflare Workers Example
# джерело: https://github.com/upstash/workflow-js/blob/v1.4.0/examples/cloudflare-workers/README.md
# отримано: 2026-10-16
# версія: workflow-1.4.0, workflow-1.3.3, workflow-1.3.2, workflow-1.3.1, workflow-1.3.0, workflow-1.2.1, workflow-1.2.0, workflow-1.1.1, workflow-1.1.0, workflow-1.0.0, workflow-0.2.23, workflow-0.2.22, workflow-0.2.21, workflow-0.2.20, workflow-0.2.19, workflow-0.2.18, workflow-0.2.17, workflow-0.2.16, workflow-0.2.15, workflow-0.2.14

This is an example of how to use Upstash Workflow with Cloudflare Workers. You can learn more in Workflow documentation for Cloudflare Workers.

Deploy to Cloudflare Workers
**Note:** After deploying with the button above, you need to set the environment variables `QSTASH_URL` and `QSTASH_TOKEN`.

## Development

1. Install the dependencies

```bash
npm install
```

2. Start the QStash development server:

```bash
npx @upstash/qstash-cli dev
```

3. Once you run the development server, you will see `QSTASH_URL` and `QSTASH_TOKEN` environment variables for the local development server. Add these to the `.dev.vars` file:

```bash
QSTASH_URL="***"
QSTASH_TOKEN="***"
```

When you are deploying your app to production, you don't need to set `QSTASH_URL`. You should only set the `QSTASH_TOKEN` environment variable to the token you get from Upstash Console.

4. Run your app:

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
