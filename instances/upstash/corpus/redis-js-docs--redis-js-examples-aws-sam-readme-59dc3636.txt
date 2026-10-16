# AWS SAM Example
# джерело: https://github.com/upstash/redis-js/blob/v1.36.4/examples/aws-sam/README.md
# отримано: 2026-10-16
# версія: redis-1.36.4, redis-1.36.3, redis-1.36.2, redis-1.36.1, redis-1.36.0, redis-1.35.8, redis-1.35.7, redis-1.35.6, redis-1.35.5, redis-1.35.4, redis-1.35.3, redis-1.35.2, redis-1.35.1, redis-1.35.0, redis-1.34.9, redis-1.34.8, redis-1.34.7, redis-1.34.6, redis-1.34.5, redis-1.34.4, redis-1.34.3, redis-1.34.2, redis-1.34.1

### Prerequisites

1. Complete AWS SAM Prerequisites
2. Install the AWS SAM CLI

### Project Setup

Clone the example

```shell
git clone https://github.com/upstash/redis-js.git
cd redis-js/examples/aws-sam
```

### Database Setup

Create a Redis database using Upstash Console or Upstash CLI. Copy `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` for the next steps.

### Build

```shell
sam build
```

### Deploy

Enter your database related environment variables when prompted.
```shell
sam deploy --guided
```

Visit the HelloWorld API Gateway URL to see the response.
