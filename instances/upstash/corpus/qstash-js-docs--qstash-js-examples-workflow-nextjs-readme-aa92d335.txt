# README
# джерело: https://github.com/upstash/qstash-js/blob/v2.7.10/examples/workflow/nextjs/README.md
# отримано: 2026-10-16
# версія: qstash-2.7.10, qstash-2.7.9

Deploy with Vercel

## QStash Workflow Nextjs Example

This project has some routes showcasing how QStash Workflow can be used in a nextjs project. You can learn more in Workflow documentation for Nextjs.

Under the app directory, you will find 8 folders, each corresponding to a workflow API except the `-call-qstash`. In each of these folders, you will find the `route.ts` file which defines the workflow.

The user calls `-call-qstash` with information about which endpoint is to be called in the body. `-call-qstash` publishes a message to QStash. QStash then calls the specified endpoint.

## Deploying the Project at Vercel

To deploy the project, you can simply use the `Deploy with Vercel` button at the top of this README. If you want to edit the project and deploy it, you can read the rest of this section.

To deploy the project at vercel and try the endpoints, you should start with setting up the project by running:

```
vercel
```

Next, you shoud go to vercel.com, find your project and add `QSTASH_URL`, `QSTASH_TOKEN`, `QSTASH_CURRENT_SIGNING_KEY` and `QSTASH_NEXT_SIGNING_KEY` to the project as environment variables. You can find these env variables from the Upstash Console. `QSTASH_URL` should be `https://qstash.upstash.io`

At this point, if you are using a released `@upstash/qstash` version, you can deploy the project with `vercel --prod`. If you are going to deploy the project with an `@upstash/qstash` version which is not released yet, you can go to the branch and run:

```
cd ../../..

bun install
npm run build

cd examples/workflow/nextjs

npm install @upstash/qstash@file:../../../dist

vercel build --prod
vercel --prebuilt --prod
```

This will go to the parent directory, build `@upstash/qstash`, install it in the workflow example project and deploy to Vercel.

Once you have the app deployed, you can go to the deployment and call the endpoints using the form on the page. Simply enter the deployment URL and pick an endpoint.

Here is an example payload you can use for invoice:

```json
{"date":123,"email":"my@mail.com","amount":10}
```

You can observe the logs at Upstash console or vercel.com to see your workflow operate.
