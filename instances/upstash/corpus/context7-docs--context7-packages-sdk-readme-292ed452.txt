# Upstash Context7 SDK
# джерело: https://github.com/upstash/context7/blob/ctx7@0.5.10/packages/sdk/README.md
# отримано: 2026-10-16
# версія: ctx7-0.5.10, ctx7-0.5.9, ctx7-0.5.8, ctx7-0.5.7, ctx7-0.5.6, ctx7-0.5.5, ctx7-0.5.4, ctx7-0.5.3, ctx7-0.5.2, ctx7-0.5.1, ctx7-0.5.0, ctx7-0.4.5, ctx7-0.4.4, ctx7-0.4.3, ctx7-0.4.2, ctx7-0.4.1, ctx7-0.4.0, ctx7-0.3.13, ctx7-0.3.12, ctx7-0.3.11, ctx7-0.3.10, ctx7-0.3.9, ctx7-0.3.8, ctx7-0.3.6, ctx7-0.3.5, ctx7-0.3.4, ctx7-0.3.3, ctx7-0.3.2, ctx7-0.3.1, ctx7-0.3.0, ctx7-0.2.4, ctx7-0.2.3, ctx7-0.2.2, ctx7-0.2.1, ctx7-0.2.0, context7-tools-ai-sdk-0.2.5, context7-tools-ai-sdk-0.2.4, context7-tools-ai-sdk-0.2.3, context7-tools-ai-sdk-0.2.2, context7-tools-ai-sdk-0.2.1, context7-tools-ai-sdk-0.2.0, context7-sdk-0.3.1, context7-sdk-0.3.0, context7-pi-0.1.2, context7-pi-0.1.1, context7-pi-0.1.0, context7-opencode-0.1.0, context7-mcp-4.0.5, context7-mcp-4.0.4, context7-mcp-4.0.3, context7-mcp-4.0.2, context7-mcp-4.0.1, context7-mcp-4.0.0, context7-mcp-3.2.5, context7-mcp-3.2.4, context7-mcp-3.2.3, context7-mcp-3.2.2, context7-mcp-3.2.1, context7-mcp-3.2.0, context7-mcp-3.1.0, context7-mcp-3.0.0, context7-mcp-2.3.0, context7-mcp-2.2.5, context7-mcp-2.2.4, context7-mcp-2.2.3, context7-mcp-2.2.2, context7-mcp-2.2.1, context7-mcp-2.2.0, context7-mcp-2.1.8, context7-mcp-2.1.7, context7-mcp-2.1.6, context7-mcp-2.1.4, context7-mcp-2.1.3, context7-mcp-2.1.2, context7-mcp-2.1.1, context7-mcp-2.1.0

> ⚠️ **Work in Progress**: This SDK is currently under active development. The API is subject to change and may introduce breaking changes in future releases.

`@upstash/context7-sdk` is an HTTP/REST based client for TypeScript, built on top of the Context7 API.

## Why Context7?

LLMs rely on outdated or generic training data about the libraries you use. This leads to:

- Code examples based on year-old training data
- Hallucinated APIs that don't exist
- Generic answers for old package versions

Context7 solves this by providing up-to-date, version-specific documentation and code examples directly from the source. Use this SDK to:

- Build AI agents with accurate, current documentation context
- Create RAG pipelines with reliable library documentation
- Power code generation tools with real API references

## Quick Start

### Install

```bash
npm install @upstash/context7-sdk
```

### Get API Key

Get your API key from Context7

## Basic Usage

```ts
import { Context7 } from "@upstash/context7-sdk";

const client = new Context7({
  apiKey: "<CONTEXT7_API_KEY>",
});

// Search for libraries
const libraries = await client.searchLibrary(
  "I need to build a UI with components",
  "react"
);
console.log(libraries[0].id); // "/facebook/react"

// Get documentation as JSON array (default)
const docs = await client.getContext("How do I use hooks?", "/facebook/react");
console.log(docs[0].title, docs[0].content);

// Get documentation context as plain text
const context = await client.getContext(
  "How do I use hooks?",
  "/facebook/react",
  { type: "txt" }
);
console.log(context);
```

## Configuration

### Environment Variables

You can set your API key via environment variable:

```sh
CONTEXT7_API_KEY=ctx7sk-...
```

Then initialize without options:

```ts
const client = new Context7();
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
