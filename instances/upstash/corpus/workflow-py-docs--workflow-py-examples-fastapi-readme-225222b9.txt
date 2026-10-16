# Upstash Workflow FastAPI Example
# джерело: https://github.com/upstash/workflow-py/blob/v2.0.0/examples/fastapi/README.md
# отримано: 2026-10-16
# версія: upstash-workflow-2.0.0, upstash-workflow-0.1.2, upstash-workflow-0.1.1, upstash-workflow-0.1.0

This is an example of how to use Upstash Workflow in a FastAPI project. You can learn more in Workflow documentation for FastAPI.

## Development

> \[!TIP]
> You can use the `bootstrap.sh` script to run this example with a local tunnel.
>
> Simply set the environment variables as explained below and run the following command in the `workflow-py/examples` directory:
>
> ```
> bash bootstrap.sh fastapi
> ```

1. Create a virtual environment

```sh
python -m venv venv
source venv/bin/activate
```

2. Install the dependencies

```bash
pip install fastapi uvicorn upstash-workflow
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
uvicorn main:app --reload
```

7. Send a `POST` request to the `/sleep` endpoint.

```bash
curl -X POST "http://localhost:8000/sleep" -d '{"text": "hello world!"}'
```
