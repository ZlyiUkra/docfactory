# README
# джерело: https://github.com/upstash/workflow-js/blob/v0.2.13/examples/nextjs-pages/README.md
# отримано: 2026-10-16
# версія: workflow-0.2.13, workflow-0.2.12, workflow-0.2.11, workflow-0.2.10, workflow-0.2.9, workflow-0.2.8, workflow-0.2.7, workflow-0.2.6, workflow-0.2.5, workflow-0.2.4, workflow-0.2.3, workflow-0.2.2, workflow-0.2.1, workflow-0.2.0, workflow-0.1.5, workflow-0.1.4, workflow-0.1.3

Deploy with Vercel

## Upstash Workflow Nextjs (Pages Router) Example

This is an example of how to use Upstash Workflow with Nextjs (using Pages Router). You can learn more in Workflow documentation for Nextjs.

In the `src/pages/api/path.sh` file, you can find out how one can define endpoints serving Upstash Workflow.

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

5. Send a `POST` request to the `/api/path` endpoint.

```bash
curl -X POST "http://localhost:3001/api/path" -d 'my-payload'
```

## Deploying the Project at Vercel

To deploy the project, you can simply use the `Deploy with Vercel` button at the top of this README. If you want to edit the project and deploy it, you can read the rest of this section.

To deploy the project at vercel and try the endpoints, you should start with setting up the project by running:

```
vercel
```
