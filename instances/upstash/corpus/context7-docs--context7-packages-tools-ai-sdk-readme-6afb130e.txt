# Upstash Context7 AI SDK
# джерело: https://github.com/upstash/context7/blob/ctx7@0.6.0/packages/tools-ai-sdk/README.md
# отримано: 2026-10-16
# версія: ctx7-0.6.0, ctx7-0.5.16, ctx7-0.5.15, ctx7-0.5.14, ctx7-0.5.13, ctx7-0.5.12, ctx7-0.5.11, ctx7-0.5.10, ctx7-0.5.9, ctx7-0.5.8, ctx7-0.5.7, ctx7-0.5.6, ctx7-0.5.5, ctx7-0.5.4, ctx7-0.5.3, ctx7-0.5.2, ctx7-0.5.1, ctx7-0.5.0, ctx7-0.4.5, ctx7-0.4.4, ctx7-0.4.3, ctx7-0.4.2, ctx7-0.4.1, ctx7-0.4.0, ctx7-0.3.13, ctx7-0.3.12, ctx7-0.3.11, ctx7-0.3.10, ctx7-0.3.9, ctx7-0.3.8, ctx7-0.3.6, ctx7-0.3.5, ctx7-0.3.4, ctx7-0.3.3, ctx7-0.3.2, ctx7-0.3.1, ctx7-0.3.0, ctx7-0.2.4, ctx7-0.2.3, ctx7-0.2.2, ctx7-0.2.1, ctx7-0.2.0, context7-tools-ai-sdk-1.0.2, context7-tools-ai-sdk-1.0.1, context7-tools-ai-sdk-1.0.0, context7-tools-ai-sdk-0.2.5, context7-tools-ai-sdk-0.2.4, context7-tools-ai-sdk-0.2.3, context7-tools-ai-sdk-0.2.2, context7-tools-ai-sdk-0.2.1, context7-tools-ai-sdk-0.2.0, context7-tools-ai-sdk-0.1.0, context7-sdk-0.5.1, context7-sdk-0.5.0, context7-sdk-0.4.1, context7-sdk-0.4.0, context7-sdk-0.3.1, context7-sdk-0.3.0, context7-sdk-0.2.0, context7-pi-0.1.2, context7-pi-0.1.1, context7-pi-0.1.0, context7-opencode-0.2.0, context7-opencode-0.1.0, context7-mcp-4.3.0, context7-mcp-4.2.1, context7-mcp-4.2.0, context7-mcp-4.1.3, context7-mcp-4.1.2, context7-mcp-4.1.1, context7-mcp-4.1.0, context7-mcp-4.0.7, context7-mcp-4.0.6, context7-mcp-4.0.5, context7-mcp-4.0.4, context7-mcp-4.0.3, context7-mcp-4.0.2, context7-mcp-4.0.1, context7-mcp-4.0.0, context7-mcp-3.2.5, context7-mcp-3.2.4, context7-mcp-3.2.3, context7-mcp-3.2.2, context7-mcp-3.2.1, context7-mcp-3.2.0, context7-mcp-3.1.0, context7-mcp-3.0.0, context7-mcp-2.3.0, context7-mcp-2.2.5, context7-mcp-2.2.4, context7-mcp-2.2.3, context7-mcp-2.2.2, context7-mcp-2.2.1, context7-mcp-2.2.0, context7-mcp-2.1.8, context7-mcp-2.1.7, context7-mcp-2.1.6, context7-mcp-2.1.4, context7-mcp-2.1.3, context7-mcp-2.1.2, context7-mcp-2.1.1, context7-mcp-2.1.0, context7-mcp-2.0.2, context7-mcp-2.0.1, context7-mcp-2.0.0, context7-mcp-1.0.33, context7-mcp-1.0.32

`@upstash/context7-tools-ai-sdk` provides Vercel AI SDK compatible tools and agents that give your AI applications access to up to date library documentation through Context7.

Use this package to:

- Add documentation lookup tools to your AI SDK workflows with `generateText` or `streamText`
- Create documentation aware agents using the pre-configured `Context7Agent`
- Build RAG pipelines that retrieve accurate, version specific code examples

The package provides two main tools:

- `resolveLibrary` - Searches Context7's database to find the correct library ID
- `getLibraryDocs` - Fetches documentation for a specific library with optional topic filtering

## Quick Start

### Install

```bash
npm install @upstash/context7-tools-ai-sdk @upstash/context7-sdk ai zod
```

### Get API Key

Get your API key from Context7

## Usage

### Using Tools with `generateText`

```typescript
import { resolveLibrary, getLibraryDocs } from "@upstash/context7-tools-ai-sdk";
import { generateText, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";

const { text } = await generateText({
  model: openai("gpt-4o"),
  prompt: "How do I use React Server Components?",
  tools: {
    resolveLibrary: resolveLibrary(),
    getLibraryDocs: getLibraryDocs(),
  },
  stopWhen: stepCountIs(5),
});

console.log(text);
```

### Using the Context7 Agent

The package provides a pre-configured agent that handles the multi-step workflow automatically:

```typescript
import { Context7Agent } from "@upstash/context7-tools-ai-sdk";
import { anthropic } from "@ai-sdk/anthropic";

const agent = new Context7Agent({
  model: anthropic("claude-sonnet-4-20250514"),
});

const { text } = await agent.generate({
  prompt: "How do I set up routing in Next.js?",
});

console.log(text);
```

## Configuration

### Environment Variables

Set your API key via environment variable:

```sh
CONTEXT7_API_KEY=ctx7sk-...
```

Then use tools and agents without explicit configuration:

```typescript
const tool = resolveLibrary(); // Uses CONTEXT7_API_KEY automatically
```

## Docs

See the documentation for details.

## Contributing

### Running tests

```sh
pnpm test
```

### Building

```sh
pnpm build
```
