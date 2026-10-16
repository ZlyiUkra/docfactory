# README
# джерело: https://github.com/upstash/workflow-js/blob/v1.4.0/examples/nextjs/README.md
# отримано: 2026-10-16
# версія: workflow-1.4.0, workflow-1.3.3, workflow-1.3.2, workflow-1.3.1, workflow-1.3.0, workflow-1.2.1, workflow-1.2.0, workflow-1.1.1, workflow-1.1.0, workflow-1.0.0, workflow-0.2.23, workflow-0.2.22, workflow-0.2.21, workflow-0.2.20, workflow-0.2.19, workflow-0.2.18, workflow-0.2.17, workflow-0.2.16, workflow-0.2.15, workflow-0.2.14

Deploy with Vercel

## Upstash Workflow Nextjs Example

This project has some routes showcasing how Upstash Workflow can be used in a nextjs project. You can learn more in Workflow documentation for Nextjs.

Under the app directory, you will find 7 folders, each corresponding to a workflow API except the `-call-qstash`. In each of these folders, you will find the `route.ts` file which defines the endpoint.

The user calls `-call-qstash` with information about which endpoint is to be called in the body. `-call-qstash` publishes a message to QStash. QStash then calls the specified endpoint.

## Deploying the Project at Vercel

To deploy the project, you can simply use the `Deploy with Vercel` button at the top of this README. If you want to edit the project and deploy it, you can read the rest of this section.

To deploy the project at vercel and try the endpoints, you should start with setting up the project by running:

```
vercel
```

Next, you shoud go to vercel.com, find your project and add `QSTASH_TOKEN`, to the project as environment variables. You can find this env variables from the Upstash Console. To learn more about other env variables and their use in the context of Upstash Workflow, you can read the Secure your Endpoint in our documentation.

Once you add the env variables, you can deploy the project with:

```
vercel --prod
```

Note that the project won't work in preview. It should be deployed to production like above. This is because preview requires authentication.

Once you have the app deployed, you can go to the deployment and call the endpoints using the form on the page.

You can observe the logs at Upstash console under the Worfklow tab or vercel.com to see your workflow operate.

## Local Development

For local development setup, refer to the Local Development section in our documentation.
