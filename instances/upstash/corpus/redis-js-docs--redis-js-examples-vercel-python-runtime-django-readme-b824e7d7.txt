# Vercel Python Runtime - Django Example
# джерело: https://github.com/upstash/redis-js/blob/v1.36.4/examples/vercel-python-runtime-django/README.md
# отримано: 2026-10-16
# версія: redis-1.36.4, redis-1.36.3, redis-1.36.2, redis-1.36.1, redis-1.36.0, redis-1.35.8, redis-1.35.7, redis-1.35.6, redis-1.35.5, redis-1.35.4, redis-1.35.3, redis-1.35.2, redis-1.35.1, redis-1.35.0, redis-1.34.9, redis-1.34.8, redis-1.34.7, redis-1.34.6, redis-1.34.5, redis-1.34.4, redis-1.34.3, redis-1.34.2, redis-1.34.1

### Project Setup

Let's create a new django application from Vercel's template.

```shell
git clone https://github.com/upstash/redis-js.git
cd redis-js/examples/vercel-python-runtime-django
```

We will create a Conda environment with python version `3.12` to match Vercel Python Runtime and avoid conflicts on deployment, you can use any other environment management system.

```shell
conda create --name vercel-django python=3.12
conda activate vercel-django
pip install -r requirements.txt
```

### Database Setup

Create a Redis database using Upstash Console or Upstash CLI and export `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` to your environment.

```shell
export UPSTASH_REDIS_REST_URL=<YOUR_URL>
export UPSTASH_REDIS_REST_TOKEN=<YOUR_TOKEN>
```

### Run & Deploy

Run the app locally with `python manage.py runserver`, check `http://localhost:8000/`

Deploy your app with `vercel`

Set `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` in your project's Settings -> Environment Variables. Redeploy from Deployments tab.
