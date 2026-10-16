# QStash With Next.js
# джерело: https://github.com/upstash/qstash-js/blob/v2.12.0/examples/nextjs/README.md
# отримано: 2026-10-16
# версія: qstash-2.12.0, qstash-2.11.3, qstash-2.11.2, qstash-2.11.1, qstash-2.11.0, qstash-2.10.1, qstash-2.10.0, qstash-2.9.1, qstash-2.9.0, qstash-2.8.4, qstash-2.8.3, qstash-2.8.2, qstash-2.8.1, qstash-2.8.0, qstash-2.7.23, qstash-2.7.22, qstash-2.7.21, qstash-2.7.20, qstash-2.7.19, qstash-2.7.18, qstash-2.7.17, qstash-2.7.16, qstash-2.7.15, qstash-2.7.14, qstash-2.7.13

This project is a simple example of how to use QStash with Next.js.

Routes in the project:

- `/api/edge` (pages router)
- `/api/receiver` (pages router)
- `/api/serverless` (pages router)

- `/edge` (app router)
- `/serverless` (app router)
- '/publish' (app router)

On the landing page of the project, you will find an introduction to QStash. You can click a button to call the `/publish` endpoint and observe the requests delivered by QStash.

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
