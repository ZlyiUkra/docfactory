# MEMORY.md, a Redis-backed agent memory you can watch live
# джерело: https://github.com/upstash/agent-memory/blob/3cb7927f7e1f6dac0a171aeb0a465369297ab9ca/README.md
# отримано: 2026-10-16

An AI SDK agent whose entire long-term memory is **one
Markdown file, `MEMORY.md`**. The agent reads it, greps it, and writes to it with
ordinary file-style tools. The "file" is virtual and lives in
Upstash Redis.

Memory model inspired by <https://docs.openclaw.ai/concepts/memory>.

## How it works

```
┌──────────────┐   tools     ┌──────────────┐   string key   ┌─────────────┐
│  Claude      │ ──────────▶ │ lib/memory.ts│ ─────────────▶ │   Upstash   │
│ (AI SDK)     │  read/grep  │  read/write  │  memory:MEMORY │    Redis    │
│              │  write/edit │  edit/grep   │  memory:oplog  │             │
└──────────────┘             └──────────────┘                └─────────────┘
```

## Run it

1. Add your Anthropic key and Upstash Redis credentials to `.env`:

```
   UPSTASH_REDIS_REST_URL=
   UPSTASH_REDIS_REST_TOKEN=
   ANTHROPIC_API_KEY=sk-ant-...
```

2. Start it:

```bash
   bun dev
```

   Open <http://localhost:3000>.

3. Tell the agent something about yourself ("I'm Josh, I prefer TypeScript") and
   watch it write to `MEMORY.md` on the right. Ask "what do you remember?" in a
   fresh message and it reads the file back. **Reset demo** wipes it between takes.
