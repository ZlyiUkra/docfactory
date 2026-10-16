# Workflow Examples
# джерело: https://github.com/upstash/qstash-js/blob/v2.7.22/examples/workflow/README.md
# отримано: 2026-10-16
# версія: qstash-2.7.22, qstash-2.7.21, qstash-2.7.20, qstash-2.7.19, qstash-2.7.18, qstash-2.7.17, qstash-2.7.16, qstash-2.7.15, qstash-2.7.14, qstash-2.7.13, qstash-2.7.12, qstash-2.7.11

This directory has example projects for Upstash Workflows with different frameworks.

Each project has an interface where you can enter the deployment URL, pick a workflow endpoint, enter a payload and finally call the picked workflow endpoint.

## How to Run

There are three alternatives:
1. Deploy the app and use the interface to call it
2. Run the app locally and create a local tunnel with Ngrok so that QStash can call it. Doing this is simplified through the `bootstrap.sh` script.
3. If you have access to the QStash development server, run both the development server and the example workflow project locally. Unfortunetly, local QStash development server is not public.

### `bootstrap.sh` Script

First, set the environment variables `QSTASH_TOKEN`, `QSTASH_URL`, `QSTASH_CURRENT_SIGNING_KEY` and `QSTASH_NEXT_SIGNING_KEY`.

The `bootstrap.sh` script makes it possible to start an examplew workflow project and create a Ngrok tunnel in one script. To run it, simply choose the framework and the endpoint you would like to choose as default:

```
bash bootstrap.sh <example-framework>
```

Here is an example call:

```
bash bootstrap.sh nextjs
```

Here is what the script does in a nutshell:
- create a Ngrok tunnel from `localhost:3001`
- Public URL of the tunnel is inferred from Ngrok logs. This URL is set to the `UPSTASH_WORKFLOW_URL` environment variable.
- `npm install` and `npm run dev` are executed in the example directory
- a web browser is opened with the picked endpoint

To use the app, simply send a request through the opened interface.

You will be able to see the workflow executing in the console logs. You can also monitor the events in the QStash tab of Upstash Console.
