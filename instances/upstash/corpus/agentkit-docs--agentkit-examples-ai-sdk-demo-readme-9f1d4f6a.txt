# ai-sdk-demo
# джерело: https://github.com/upstash/agentkit/blob/@upstash%2Fagentkit-tanstack-ai@0.1.1/examples/ai-sdk-demo/README.md
# отримано: 2026-10-16
# версія: agentkit-tanstack-ai-0.1.1, agentkit-sdk-0.9.0, agentkit-sdk-0.6.0, agentkit-sdk-0.2.0, agentkit-eve-extension-0.16.0, agentkit-eve-extension-0.15.0, agentkit-eve-extension-0.14.0, agentkit-eve-extension-0.13.0, agentkit-eve-extension-0.12.0, agentkit-eve-extension-0.11.0, agentkit-eve-extension-0.10.0, agentkit-eve-extension-0.9.0, agentkit-eve-extension-0.8.0, agentkit-eve-extension-0.7.0, agentkit-eve-extension-0.6.0, agentkit-eve-extension-0.5.0, agentkit-eve-extension-0.4.0, agentkit-eve-extension-0.3.1, agentkit-eve-extension-0.3.0, agentkit-eve-0.15.1, agentkit-eve-0.14.1, agentkit-eve-0.13.0, agentkit-eve-0.12.0, agentkit-eve-0.9.0, agentkit-eve-0.8.0, agentkit-eve-0.7.0, agentkit-eve-0.6.0, agentkit-eve-0.5.0, agentkit-eve-0.3.0, agentkit-eve-0.2.2, agentkit-eve-0.2.1, agentkit-eve-0.2.0, agentkit-ai-sdk-0.15.1, agentkit-ai-sdk-0.9.0, agentkit-ai-sdk-0.6.0, agentkit-ai-sdk-0.2.0

A persistent, streaming chat app built on `@upstash/agentkit-ai-sdk` and the
Vercel AI SDK (`useChat`), backed entirely by a real Upstash Redis.

## What it shows

- **Chat history** — every turn is persisted with `createChatHistory`. The sidebar lists your chats and
  fuzzy-searches them (`listChats` / `searchChats`); reloading or revisiting a chat resumes it
  (`getChat` → `useChat({ messages })`). The route persists the whole conversation in `onFinish`.
- **Agent memory** — `recall_memory` / `save_memory` tools (`createMemoryTools`).
- **Search tools** — schema-driven `search` / `aggregate` / `count` over a seeded **books** index
  (`createSearchTools`). The books are seeded once into Redis on first load.
- **Tool cache** — a memoized `convert_price` tool (`cachedTools`).
- **Rate limiting** — `createRateLimit` checked (by user) before each model call.

Tool calls are rendered inline in the chat so you can see what the agent did.

## Setup

```bash
cp .env.example .env   # then fill in the values (or put them in the repo-root .env)
pnpm install           # from the repo root
```

`.env.example` lists the required vars: `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`, and
`OPENAI_API_KEY`. The app reads a local `.env` first, then falls back to the repo-root `.env`.

## Run

```bash
pnpm --filter ai-sdk-demo dev   # or: cd examples/ai-sdk-demo && pnpm dev
```

Open <http://localhost:3000>. The demo uses the `gpt-5.4-mini` model.
