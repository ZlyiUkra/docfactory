# QStash With Next.js
# джерело: https://github.com/upstash/qstash-js/blob/v2.7.12/examples/nextjs/README.md
# отримано: 2026-10-16
# версія: qstash-2.7.12, qstash-2.7.11

This project is a simple example of how to use QStash with Next.js.

Routes in the project:

- `/api/edge` (pages router)
- `/api/receiver` (pages router)
- `/api/serverless` (pages router)

- `/edge` (app router)
- `/serverless` (app router)

## Local Development

### 1. Install dependencies

```bash
npm install
```

### 2. Set environment variables

Create a `.env.local` file in the root of the project and add the following environment variables:

```bash
QSTASH_CURRENT_SIGNING_KEY=
QSTASH_CURRENT_SIGNING_KEY_ID=
```

You can get these values from the Upstash Console.

### 3. Start the development server

```bash
npm run dev
```

### 4. Start a local tunnel

To test the application, QStash needs to send requests to your local server. You can use a tool like ngrok to create a secure tunnel to your localhost.

```bash
ngrok http 3000
```

Copy the resulting url and. Go to the Upstash Console and send a simple request to `<ngrok-url>/api/receiver`
