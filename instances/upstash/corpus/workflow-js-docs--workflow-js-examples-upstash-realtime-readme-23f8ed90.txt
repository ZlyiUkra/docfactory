# Upstash Workflow + Realtime Demo
# джерело: https://github.com/upstash/workflow-js/blob/v1.4.0/examples/upstash-realtime/README.md
# отримано: 2026-10-16
# версія: workflow-1.4.0, workflow-1.3.3, workflow-1.3.2, workflow-1.3.1, workflow-1.3.0, workflow-1.2.1, workflow-1.2.0, workflow-1.1.1, workflow-1.1.0, workflow-1.0.0, workflow-0.2.23, workflow-0.2.22

This demo showcases the integration of **Upstash Workflow** and **Upstash Realtime** to build real-time workflow visualizations. Watch your workflow steps execute and update live in the browser.

The demo includes two examples:
- **Basic Workflow:** A simple multi-step workflow that runs automatically
- **Human-in-the-Loop:** Uses `waitForEvent` to pause execution and wait for user input before continuing

## Setup

1. **Start QStash dev server:**
```bash
   npx @upstash/qstash-cli@latest dev
```

2. **Get a Redis database:**
   - Go to Upstash Console
   - Create a new Redis database

3. **Configure environment variables:**
```bash
   cp .env.example .env
```

   Fill in your `.env` file with:
   - `QSTASH_URL` and `QSTASH_TOKEN` from the QStash dev server output
   - Redis credentials (`UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`) from the Upstash Console

4. **Start the app:**
```bash
   npm run dev
   # or
   pnpm dev
   # or
   bun dev
```

5. **Try it out:**
   - Open http://localhost:3000
   - Click the workflow buttons and watch real-time updates!
