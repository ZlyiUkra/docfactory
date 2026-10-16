# Upstash Workflow with Nextjs 12 Example
# джерело: https://github.com/upstash/workflow-js/blob/v0.2.13/examples/nextjs-12/README.md
# отримано: 2026-10-16
# версія: workflow-0.2.13, workflow-0.2.12, workflow-0.2.11, workflow-0.2.10, workflow-0.2.9, workflow-0.2.8, workflow-0.2.7, workflow-0.2.6, workflow-0.2.5, workflow-0.2.4, workflow-0.2.3, workflow-0.2.2, workflow-0.2.1, workflow-0.2.0, workflow-0.1.5, workflow-0.1.4, workflow-0.1.3

This example is for testing the compatibility of Upstash Workflow with older versions of Nextjs and also older Node versions. Our CI will use this example for testing Workflow with Node 18.

## Development

> [!TIP]
> You can use the `bootstrap.sh` script to run this example with a local tunnel.
>
> Simply set the environment variables as explained below and run the following command in the `workflow-js/examples` directory:
>
> ```
> bash bootstrap.sh cloudflare-workers-hono
> ```

1. Install the dependencies

```bash
npm install
```

2. Get the credentials from the Upstash Console and add them to the `.env.local` file.

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

5. Send a `POST` request to the `/api/path` endpoint. In your requesets, you should use `text/plain` header:

```bash
curl -X POST "http://localhost:3001/api/workflow" \
     -H "Content-type: text/plain" \
     -d "my-payload"
```

## Deploying the Project at Vercel

To deploy the project, you can simply use the `Deploy with Vercel` button at the top of this README. If you want to edit the project and deploy it, you can read the rest of this section.

To deploy the project at vercel and try the endpoints, you should start with setting up the project by running:

```
vercel
```
