# README
# джерело: https://github.com/upstash/workflow-js/blob/v0.2.23/examples/agents-researcher/README.md
# отримано: 2026-10-16
# версія: workflow-0.2.23, workflow-0.2.22, workflow-0.2.21, workflow-0.2.20, workflow-0.2.19, workflow-0.2.18, workflow-0.2.17, workflow-0.2.16, workflow-0.2.15, workflow-0.2.14, workflow-0.2.13, workflow-0.2.12

Deploy with Vercel

## Deploying the Project at Vercel

To deploy the project, you can simply use the `Deploy with Vercel` button at the top of this README. If you want to edit the project and deploy it, you can read the rest of this section.

To deploy the project at vercel and try the endpoints, you should start with setting up the project by running:

```
vercel
```

### Setting up the Environment Variables

1. `QSTASH_TOKEN`

Next, you shoud go to vercel.com, find your project and add `QSTASH_TOKEN`, to the project as environment variables. You can find this env variables from the Upstash Console. To learn more about other QStash env variables and their use in the context of Upstash Workflow, you can read the Secure your Endpoint in our documentation.

2. `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`

You can find these env variables from the Upstash Console.

3. `OPENAI_API_KEY`

You can get your API key from the OpenAI Platform.

4. `WOLFRAM_ALPHA_APP_ID`

You can get your App ID from the Wolfram Alpha Developer Portal.

5. `EXASEARCH_API_KEY`

You can get your API key from the Exa Dashboard.

### Deploying the Project

Once you add the env variables, you can deploy the project with:

```
vercel --prod
```

Note that the project won't work in preview. It should be deployed to production like above. This is because preview requires authentication.

Once you have the app deployed, you can go to the deployment and call the endpoints using the form on the page.

You can observe the logs at Upstash console under the Worfklow tab or vercel.com to see your workflow operate.

## Local Development

For local development setup, refer to the Local Development section in our documentation. Also set up the environment variables in a `.env` file as described in the previous section.
