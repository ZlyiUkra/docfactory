# README
# джерело: https://github.com/upstash/workflow-js/blob/v1.4.0/examples/nextjs-pages/README.md
# отримано: 2026-10-16
# версія: workflow-1.4.0, workflow-1.3.3, workflow-1.3.2, workflow-1.3.1, workflow-1.3.0, workflow-1.2.1, workflow-1.2.0, workflow-1.1.1, workflow-1.1.0, workflow-1.0.0, workflow-0.2.23, workflow-0.2.22, workflow-0.2.21, workflow-0.2.20, workflow-0.2.19, workflow-0.2.18, workflow-0.2.17, workflow-0.2.16, workflow-0.2.15, workflow-0.2.14

Deploy with Vercel

## Upstash Workflow Nextjs (Pages Router) Example

This is an example of how to use Upstash Workflow with Nextjs (using Pages Router). You can learn more in Workflow documentation for Nextjs.

In the `src/pages/api/path.sh` file, you can find out how one can define endpoints serving Upstash Workflow.

## Development

1. Install the dependencies

```bash
npm install
```

2. Start the QStash development server:

```bash
npx @upstash/qstash-cli dev
```

3. Once you run the development server, you will see `QSTASH_URL` and `QSTASH_TOKEN` environment variables for the local development server. Add these to the `.env.local` file:

```bash
QSTASH_URL="***"
QSTASH_TOKEN="***"
```

When you are deploying your app to production, you don't need to set `QSTASH_URL`. You should only set the `QSTASH_TOKEN` environment variable to the token you get from Upstash Console.

4. Run your app:

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
