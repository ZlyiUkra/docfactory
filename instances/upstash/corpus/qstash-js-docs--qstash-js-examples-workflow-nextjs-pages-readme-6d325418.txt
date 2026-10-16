# README
# джерело: https://github.com/upstash/qstash-js/blob/v2.7.10/examples/workflow/nextjs-pages/README.md
# отримано: 2026-10-16
# версія: qstash-2.7.10, qstash-2.7.9

Deploy with Vercel

## QStash Workflow Nextjs (Pages Router) Example

This is an example of how to use QStash Workflow with Nextjs (using Pages Router). You can learn more in Workflow documentation for Nextjs.

In the `src/pages/api/path.sh` file, you can find out how one can define endpoints serving Upstash Workflow.

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
