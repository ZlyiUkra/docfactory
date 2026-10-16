# README
# джерело: https://github.com/upstash/workflow-js/blob/v1.4.0/examples/image-gen-with-workflow/README.md
# отримано: 2026-10-16
# версія: workflow-1.4.0, workflow-1.3.3, workflow-1.3.2, workflow-1.3.1, workflow-1.3.0, workflow-1.2.1, workflow-1.2.0, workflow-1.1.1, workflow-1.1.0, workflow-1.0.0, workflow-0.2.23, workflow-0.2.22, workflow-0.2.21, workflow-0.2.20, workflow-0.2.19, workflow-0.2.18, workflow-0.2.17, workflow-0.2.16, workflow-0.2.15, workflow-0.2.14, workflow-0.2.13, workflow-0.2.12, workflow-0.2.11, workflow-0.2.10, workflow-0.2.9, workflow-0.2.8, workflow-0.2.7, workflow-0.2.6, workflow-0.2.5, workflow-0.2.4, workflow-0.2.3, workflow-0.2.2, workflow-0.2.1, workflow-0.2.0, workflow-0.1.5, workflow-0.1.4, workflow-0.1.3

Deploy with Vercel

## Upstash Workflow - Vercel Function Cost Comparison Example

This project showcases how Upstash Workflow can reduce Vercel Function runtime costs. This is achieved by letting Upstash Workflow call an external endpoint instead of calling it in a Vercel Function and waiting.

In this example, the external endpoint is Ideogram which takes around 20 seconds to return a response.

See the demo at https://image-gen-with-workflow.vercel.app for more information.

For more information about Upstash Workflow, you can refer to the Upstash Workflow documentation.

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

If you set `IDEOGRAM_API_KEY`, the app will call Ideogram. To make the app work with OpenAI "dall-e-2" model, set `OPENAI_API_KEY` env variable instead of `IDEOGRAM_API_KEY`. If you want to simply develop the app, you can leave both env variables empty; the app will return a mock url as image.
