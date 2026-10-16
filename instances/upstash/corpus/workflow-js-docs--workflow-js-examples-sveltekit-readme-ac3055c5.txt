# README
# джерело: https://github.com/upstash/workflow-js/blob/v1.4.0/examples/sveltekit/README.md
# отримано: 2026-10-16
# версія: workflow-1.4.0, workflow-1.3.3, workflow-1.3.2, workflow-1.3.1, workflow-1.3.0, workflow-1.2.1, workflow-1.2.0, workflow-1.1.1, workflow-1.1.0, workflow-1.0.0, workflow-0.2.23, workflow-0.2.22, workflow-0.2.21, workflow-0.2.20, workflow-0.2.19, workflow-0.2.18, workflow-0.2.17, workflow-0.2.16, workflow-0.2.15, workflow-0.2.14, workflow-0.2.13, workflow-0.2.12, workflow-0.2.11, workflow-0.2.10, workflow-0.2.9, workflow-0.2.8, workflow-0.2.7, workflow-0.2.6, workflow-0.2.5, workflow-0.2.4, workflow-0.2.3, workflow-0.2.2, workflow-0.2.1, workflow-0.2.0, workflow-0.1.5, workflow-0.1.4, workflow-0.1.3

Deploy with Vercel

## Upstash Workflow Sveltekit Example

This project has some routes showcasing how Upstash Workflow can be used in a sveltekit project. You can learn more in Workflow documentation for Svelte.

Under the `src/routes` directory, you will find 6 folders, each corresponding to a workflow API except the `-call-qstash`. In each of these folders, you will find the `+server.ts` file which defines the workflow.

Here is what these `-call-qstash` endpoint does: The user calls `-call-qstash` with information about which endpoint is to be called in the body. `-call-qstash` publishes a message to QStash. QStash then calls the specified endpoint.

To run the app locally, first set the environment variables `QSTASH_URL`, `QSTASH_TOKEN`, `QSTASH_CURRENT_SIGNING_KEY` and `QSTASH_NEXT_SIGNING_KEY`. You can find the values of the env variables from the Upstash Console. `QSTASH_URL` should be `https://qstash.upstash.io`.

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
