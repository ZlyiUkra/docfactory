# eve-demo
# джерело: https://github.com/upstash/agentkit/blob/@upstash%2Fagentkit-sdk@0.6.0/examples/eve-demo/README.md
# отримано: 2026-10-16
# версія: agentkit-sdk-0.6.0, agentkit-sdk-0.2.0, agentkit-eve-extension-0.8.0, agentkit-eve-extension-0.7.0, agentkit-eve-extension-0.6.0, agentkit-eve-extension-0.5.0, agentkit-eve-extension-0.4.0, agentkit-eve-extension-0.3.1, agentkit-eve-extension-0.3.0, agentkit-eve-0.8.0, agentkit-eve-0.7.0, agentkit-eve-0.6.0, agentkit-eve-0.5.0, agentkit-eve-0.3.0, agentkit-eve-0.2.2, agentkit-eve-0.2.1, agentkit-eve-0.2.0, agentkit-ai-sdk-0.6.0, agentkit-ai-sdk-0.2.0

An eve agent app built on `@upstash/agentkit-eve`, backed by a
real Upstash Redis. It's a real `eve` CLI scaffold (a workspace member) — see
`AGENTS.md`, and read `node_modules/eve/docs/` before editing agent code.

## What it shows (under `agent/`)

- **Memory tools** — `recall_memory` / `save_memory` (`defineMemoryRecallTool` / `defineMemorySaveTool`).
- **Search tools** — `search_books` / `aggregate_books` / `count_books` over a seeded **books** index
  (`defineSearchTools`). The books are seeded once into Redis when the page loads.
- **Cached tool** — `get_weather`, memoized in Redis (`defineCachedTool`).
- **Rate limiting** — `createRateLimitAuth` first in the channel's `auth` walk (`agent/channels/eve.ts`).
- **Sandbox** — an Upstash Box code-execution backend (`agent/sandbox/`).

The chat UI (`app/`) mirrors the ai-sdk-demo's minimal look and renders tool calls inline.

> **Agent files must be self-contained.** eve's dev-runtime snapshots each tool/channel/hook file and
> resolves only **package** imports — it does not include shared `agent/`-source modules. So every
> `agent/` file imports only packages and omits `redis` (it defaults to `Redis.fromEnv()`). App-only
> shared code (e.g. the books seeder) lives in the project `lib/`.

## Setup

```bash
cp .env.example .env   # then fill in the values
pnpm install           # from the repo root
```

`.env.example` lists the vars: `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`, `OPENAI_API_KEY`,
and `UPSTASH_BOX_API_KEY` (only needed for the sandbox).

## Run

```bash
pnpm --filter eve-demo dev   # or: cd examples/eve-demo && pnpm dev
```

Open <http://localhost:3000>. The agent model is `gpt-5.4-mini`. Requires Node 24 (`engines.node`); on
Node 20 it warns but still runs.
