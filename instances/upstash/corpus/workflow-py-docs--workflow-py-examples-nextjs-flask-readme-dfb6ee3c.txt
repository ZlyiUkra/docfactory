# README
# джерело: https://github.com/upstash/workflow-py/blob/v2.0.0/examples/nextjs-flask/README.md
# отримано: 2026-10-16
# версія: upstash-workflow-2.0.0, upstash-workflow-0.1.2, upstash-workflow-0.1.1, upstash-workflow-0.1.0

Deploy with Vercel

## Upstash Workflow Next.js & Flask Example

This project has some routes showcasing how Upstash Workflow can be used in a Next.js & Flask project. You can learn more in Workflow documentation for Next.js & Flask.

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

> \[!TIP]
> You can use the `bootstrap.sh` script to run this example with a local tunnel.
>
> Simply set the environment variables as explained below and run the following command in the `workflow-py/examples` directory:
>
> ```
> bash bootstrap.sh nextjs-flask
> ```

1. Create a virtual environment

```sh
python -m venv venv
source venv/bin/activate
```

2. Install the dependencies

```bash
npm install
```

3. Get the credentials from the Upstash Console and add them to the `.env` file.

```bash
export QSTASH_TOKEN=
```

4. Open a local tunnel to port of the development server. Check out our Local Development guide to learn how to set up a local tunnel.

```bash
ngrok http 8000
```

Also, set the `UPSTASH_WORKLFOW_URL` environment variable to the public url provided by ngrok.

```bash
export UPSTASH_WORKFLOW_URL=
```

5. Set the environment variables

```bash
source .env
```

6. Run the development server

```bash
npm run dev
```

Flask server will be running at `localhost:8000` and Next.js server will be running at `localhost:3000`. Visit `http://localhost:3000` to see the app.
