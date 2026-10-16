# @upstash/context7-pi
# джерело: https://github.com/upstash/context7/blob/ctx7@0.6.1/packages/pi/README.md
# отримано: 2026-10-16
# версія: ctx7-0.6.1, ctx7-0.6.0, ctx7-0.5.16, ctx7-0.5.15, ctx7-0.5.14, ctx7-0.5.13, ctx7-0.5.12, ctx7-0.5.11, ctx7-0.5.10, ctx7-0.5.9, ctx7-0.5.8, ctx7-0.5.7, ctx7-0.5.6, ctx7-0.5.5, ctx7-0.5.4, ctx7-0.5.3, ctx7-0.5.2, ctx7-0.5.1, ctx7-0.5.0, ctx7-0.4.5, context7-tools-ai-sdk-1.0.3, context7-tools-ai-sdk-1.0.2, context7-tools-ai-sdk-1.0.1, context7-tools-ai-sdk-0.2.5, context7-tools-ai-sdk-0.2.4, context7-sdk-0.5.1, context7-sdk-0.5.0, context7-sdk-0.4.1, context7-sdk-0.4.0, context7-sdk-0.3.1, context7-pi-0.1.3, context7-pi-0.1.2, context7-pi-0.1.1, context7-pi-0.1.0, context7-opencode-0.2.1, context7-opencode-0.2.0, context7-opencode-0.1.0, context7-mcp-4.4.2, context7-mcp-4.4.1, context7-mcp-4.4.0, context7-mcp-4.3.0, context7-mcp-4.2.1, context7-mcp-4.2.0, context7-mcp-4.1.3, context7-mcp-4.1.2, context7-mcp-4.1.1, context7-mcp-4.1.0, context7-mcp-4.0.7, context7-mcp-4.0.6, context7-mcp-4.0.5, context7-mcp-4.0.4, context7-mcp-4.0.3, context7-mcp-4.0.2, context7-mcp-4.0.1, context7-mcp-4.0.0, context7-mcp-3.2.5, context7-mcp-3.2.4, context7-mcp-3.2.3, context7-mcp-3.2.2, context7-mcp-3.2.1, context7-mcp-3.2.0, context7-mcp-3.1.0

Official Context7 extension for the pi coding agent.

Adds up-to-date library documentation to pi via two LLM-callable tools — `resolve-library-id` and `query-docs` — plus a skill that teaches the agent when to use them and a `/c7-docs` slash command for manual lookups.

## Install

```bash
pi install npm:@upstash/context7-pi
```

## Authenticate

The extension works without any setup at IP-based rate limits — useful for trying it out. For higher quotas, generate a free key at context7.com/dashboard and export it:

```bash
export CONTEXT7_API_KEY=ctx7sk_...
```

Set it in your shell profile so pi picks it up on launch.

## What it adds

- **`resolve-library-id`** — converts a package or product name to a Context7 library ID (e.g. `Next.js` → `/vercel/next.js`). The agent should call this first.
- **`query-docs`** — fetches documentation and code examples for a resolved library ID.
- **`context7-docs` skill** — instructs the agent to reach for these tools whenever the user asks about a library, framework, SDK, API, CLI tool, or cloud service.
- **`/c7-docs <library> <question>`** — slash command that runs the resolve + query flow in one shot.

## Usage

Once installed, just ask the agent a docs question and the tools are invoked automatically:

```
how do I configure caching in Next.js 16?
```

For a manual lookup:

```
/c7-docs next.js Cache Components
```

## License

MIT
