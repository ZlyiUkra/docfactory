# SST v2 Example
# джерело: https://github.com/upstash/redis-js/blob/v1.36.4/examples/sst-v2/README.md
# отримано: 2026-10-16
# версія: redis-1.36.4, redis-1.36.3, redis-1.36.2, redis-1.36.1, redis-1.36.0, redis-1.35.8, redis-1.35.7, redis-1.35.6, redis-1.35.5, redis-1.35.4, redis-1.35.3, redis-1.35.2, redis-1.35.1, redis-1.35.0, redis-1.34.9, redis-1.34.8, redis-1.34.7, redis-1.34.6, redis-1.34.5, redis-1.34.4, redis-1.34.3, redis-1.34.2, redis-1.34.1

### Prerequisites

You need to have AWS credentials configured locally.

1. Create an AWS account
2. Create an IAM user
3. Configure the AWS CLI

### Project Setup

Clone the example and install dependencies

```shell
git clone https://github.com/upstash/redis-js.git
cd redis-js/examples/sst-v2
npm install
```

### Database Setup

Create a Redis database using Upstash Console or Upstash CLI and copy the `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` into your `.env` file.

```shell
npx sst secrets set UPSTASH_REDIS_REST_URL <YOUR_URL>
npx sst secrets set UPSTASH_REDIS_REST_TOKEN <YOUR_TOKEN>
```

### Run

Run the SST app.

```shell
npm run dev
```

After prompted, run the Next.js app.

```shell
cd packages/web
npm run dev
```

Check `http://localhost:3000/api/hello`

### Deploy

Set the secrets for the prod stage.

```shell
npx sst secrets set --stage prod UPSTASH_REDIS_REST_URL <YOUR_URL>
npx sst secrets set --stage prod UPSTASH_REDIS_REST_TOKEN <YOUR_TOKEN>
```

Deploy with SST.

```shell
npx sst deploy --stage prod
```

Check `<SiteUrl>/api/hello` with the given SiteUrl.
