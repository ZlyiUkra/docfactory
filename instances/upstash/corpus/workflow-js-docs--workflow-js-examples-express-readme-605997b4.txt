# Upstash Workflow Express Example
# джерело: https://github.com/upstash/workflow-js/blob/v0.2.13/examples/express/README.md
# отримано: 2026-10-16
# версія: workflow-0.2.13, workflow-0.2.12, workflow-0.2.11, workflow-0.2.10, workflow-0.2.9, workflow-0.2.8, workflow-0.2.7, workflow-0.2.6, workflow-0.2.5, workflow-0.2.4, workflow-0.2.3, workflow-0.2.2, workflow-0.2.1, workflow-0.2.0, workflow-0.1.5, workflow-0.1.4, workflow-0.1.3

This is an example of how to use Upstash Workflow in a Express.js project. You can learn more in Getting Started with Upstash Workflow.

## Development

> [!TIP]
> You can use the `bootstrap.sh` script to run this example with a local tunnel.
>
> Simply set the environment variables as explained below and run the following command in the `qstash-js/examples/workflow` directory:
>
> ```
> bash bootstrap.sh express
> ```

1. Install the dependencies

```bash
npm install
```

2. Get the credentials from the Upstash Console and add them to the `.env` file.

```bash
QSTASH_TOKEN=

UPSTASH_WORKFLOW_URL=
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

**NOTE**: Workflow on Express.js only works with `Content-Type: application/json` header.

```bash
curl -X POST http://localhost:3001/workflow \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello from the workflow!"}'
```
