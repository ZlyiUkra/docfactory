# Upstash Workflow & Fastify Example
# джерело: https://github.com/upstash/workflow-js/blob/v1.4.0/examples/fastify/README.md
# отримано: 2026-10-16
# версія: workflow-1.4.0, workflow-1.3.3, workflow-1.3.2, workflow-1.3.1, workflow-1.3.0, workflow-1.2.1, workflow-1.2.0, workflow-1.1.1, workflow-1.1.0, workflow-1.0.0, workflow-0.2.23, workflow-0.2.22, workflow-0.2.21, workflow-0.2.20, workflow-0.2.19, workflow-0.2.18, workflow-0.2.17, workflow-0.2.16, workflow-0.2.15, workflow-0.2.14

This is an example of how to use Upstash Workflow with a Fastify server using TypeScript and ES modules.

## Getting Started

### 1. Install the dependencies

```bash
bun install
```

### 2. Start the QStash development server:

```bash
npx @upstash/qstash-cli dev
```

### 3. Once you run the development server, you will see `QSTASH_URL` and `QSTASH_TOKEN` environment variables for the local development server. Add these to the `.env` file:

```bash
QSTASH_URL="***"
QSTASH_TOKEN="***"
```

When you are deploying your app to production, you don't need to set `QSTASH_URL`. You should only set the `QSTASH_TOKEN` environment variable to the token you get from Upstash Console.

### 4. Run your app:

```bash
bun start
```

For production builds:

```bash
bun run build
bun run start:prod
```

### 5. Send a `POST` request to the workflow endpoint.

```bash
curl -X POST http://localhost:3001/workflow -d '{"hello": "world"}' -H "content-type:application/json"
```

## Project Structure

- `src/index.ts`: Entry point for the application
- `src/server.ts`: Fastify server configuration and workflow implementation
- `tsconfig.json`: TypeScript configuration
- `package.json`: Project dependencies and scripts

## Scripts

- `bun start`: Start the development server using Bun
- `bun run build`: Build the TypeScript files
