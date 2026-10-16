# Google Cloud Functions Example
# джерело: https://github.com/upstash/redis-js/blob/v1.36.4/examples/google-cloud-functions/README.md
# отримано: 2026-10-16
# версія: redis-1.36.4, redis-1.36.3, redis-1.36.2, redis-1.36.1, redis-1.36.0, redis-1.35.8, redis-1.35.7, redis-1.35.6, redis-1.35.5, redis-1.35.4, redis-1.35.3, redis-1.35.2, redis-1.35.1, redis-1.35.0, redis-1.34.9, redis-1.34.8, redis-1.34.7, redis-1.34.6, redis-1.34.5, redis-1.34.4, redis-1.34.3, redis-1.34.2, redis-1.34.1

### Prerequisites

1. Create a Google Cloud Project.
2. Enable billing for your project.
3. Enable Cloud Functions, Cloud Build, Artifact Registry, Cloud Run, Logging, and Pub/Sub APIs.
4. Install and initialize the Google Cloud CLI.

### Project Setup

Clone the example

```shell
git clone https://github.com/upstash/redis-js.git
cd redis-js/examples/google-cloud-functions
```

### Database Setup

Create a Redis database using Upstash Console or Upstash CLI. Copy `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` for the next steps.

### Deploy

```shell
gcloud functions deploy counter-function \
--gen2 \
--runtime=nodejs20 \
--region=<YOUR_REGION> \
--source=. \
--entry-point=counter \
--set-env-vars UPSTASH_REDIS_REST_URL=<YOUR_URL>,UPSTASH_REDIS_REST_TOKEN=<YOUR_TOKEN> \
--trigger-http \
--allow-unauthenticated
```

Visit the URL provided by the deployment to see the counter in action.
