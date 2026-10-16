# Upstash Workflow SDK
# джерело: https://github.com/upstash/workflow-js/blob/v1.1.1/README.md
# отримано: 2026-10-16
# версія: workflow-1.1.1, workflow-1.1.0, workflow-1.0.0, workflow-0.2.23, workflow-0.2.22

> [!NOTE]
> **This project is in GA Stage.**
> The Upstash Professional Support fully covers this project. It receives regular updates, and bug fixes.
> The Upstash team is committed to maintaining and improving its functionality.

**Upstash Workflow** lets you write durable, reliable and performant serverless functions. Get delivery guarantees, automatic retries on failure, scheduling and more without managing any infrastructure.

See the documentation for more details

## Quick Start

Here, we will briefly showcase how you can get started with Upstash Workflow.

Alternatively, you can check our quickstarts for different frameworks, including Next.js and Cloudflare.

### Install

First, install the package with:

```
npm install @upstash/workflow
```

### Get QStash token

Go to Upstash Console and copy the QSTASH_TOKEN.

### Define a Workflow Endpoint

To declare workflow endpoints, use the `serve` method:

```ts
import { serve } from "@upstash/workflow/nextjs";

// mock function
const someWork = (input: string) => {
  return `processed '${JSON.stringify(input)}'`;
};

// serve endpoint which expects a string payload:
export const { POST } = serve<string>(async (context) => {
  // get request body:
  const input = context.requestPayload;

  // run the first step:
  const result1 = await context.run("step1", async () => {
    const output = someWork(input);
    console.log("step 1 input", input, "output", output);
    return output;
  });

  // run the second step:
  await context.run("step2", async () => {
    const output = someWork(result1);
    console.log("step 2 input", result1, "output", output);
  });
});
```

In the example, you can see that steps are declared through the `context` object.

The kinds of steps which are available are:

- `context.run`: execute a function
- `context.sleep`: sleep for some time
- `context.sleepUntil`: sleep until some timestamp
- `context.call`: make a third party call without consuming any runtime
- `context.waitForEvent`: wait for an event
- `context.notify`: notify an event to make workflows waiting for the event continue

You can learn more about these methods from our documentation.

### Workflow Client

You can use the Upstash Workflow client to cancel workflows, notify workflows
waiting for an event or get the workflows waiting for an event:

```ts
import { Client } from "@upstash/workflow";
const client = new Client({ token: "<QSTASH_TOKEN>" });

// trigger a workflow
const { workflowRunId } = await client.trigger({
  url: "https://workflow-endpoint.com",
  body: "hello there!",         // Optional body
  headers: { ... },             // Optional headers
  workflowRunId: "my-workflow", // Optional workflow run ID
  retries: 3                    // Optional retries for the initial request
});

// cancel workflow:
await client.cancel({ workflowRunId: "<WORKFLOW_RUN_ID>" });

// notify workflows:
await client.notify({
  eventId: "my-event-id",
  eventData: "my-data", // data passed to the workflow run
});

// get waiters:
const result = await client.getWaiters({
  eventId: "my-event-id",
});
```

## Telemetry

This sdk sends anonymous telemetry headers to help us improve your experience.
We collect the following:

- SDK version
- Platform (Cloudflare, AWS or Vercel)
- Runtime version (node@18.x)

You can opt out by setting `disableTelemetry: true` when triggering the workflow and in the serve options:

```ts
// client
const client = new Client(/***/);
await client.trigger({
  // ...
  disableTelemetry: true,
});

// workflow endpoint
export const { POST } = serve(
  async (context) => {
    // ...
  },
  {
    disableTelemetry: true,
  }
);
```

## Contributing

### Setup

This project requires Bun to be installed. Please see the Bun installation documentation for further instructions.

Once you have cloned the project, you will need to install the dependencies and then you can run the project.

```sh
bun install
bun run build
```

### Testing

To begin testing, environment variables will need to be setup. First, create a `.env` file in the root of the project. `.env.template` can be used as a template. Your values can be found in the Qstash Console.

```sh
bun run test
```
