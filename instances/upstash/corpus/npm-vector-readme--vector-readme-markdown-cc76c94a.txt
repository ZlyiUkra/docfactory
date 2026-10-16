# @upstash/vector README 1.0.2 … 1.0.3: Upstash Vector Node.js Client &middot; ![license](https://img.shields.io/npm/l/%40upstash%2Fvector) [![Tests](https://github.com/upstash/vector-js/actions/workflows/tests.yaml/badge.svg)](https://github.com/upstash/vector-js/actions/workflows/tests.yaml) ![npm (scoped)](https://img.shields.io/npm/v/@upstash/vector) ![npm bundle size](https://img.shields.io/bundlephobia/minzip/@upstash/vector) ![npm weekly download](https://img.shields.io/npm/dw/%40upstash%2Fvector)
# джерело: https://registry.npmjs.org/@upstash/vector/-/vector-1.0.3.tgz
# отримано: 2026-10-16
# версія: vector-1.0.3, vector-1.0.2

`@upstash/vector` is an HTTP/REST based client for Typescript, built on top of Upstash REST API.

It is the only connectionless (HTTP based) Vector client and designed for:

- Serverless functions (AWS Lambda ...)
- Cloudflare Workers
- Next.js, Jamstack ...
- Client side web/mobile applications
- WebAssembly
- and other environments where HTTP is preferred over TCP.

See the list of APIs supported.

## Quick Start

### Install

#### Node.js

```bash
npm install @upstash/vector
```

### Create Index

Create a new index on Upstash

## Basic Usage:

```ts
import { Index } from "@upstash/vector";

type Metadata = {
  title: string,
  genre: 'sci-fi' | 'fantasy' | 'horror' | 'action'
  category: "classic" | "modern"
}

const index = new Index<Metadata>({
  url: "<UPSTASH_VECTOR_REST_URL>",
  token: "<UPSTASH_VECTOR_REST_TOKEN>",
});

//Upsert Data
await index.upsert([{
  id: 'upstash-rocks',
  vector: [
    .... // embedding values
  ],
  metadata: {
    title: 'Lord of The Rings',
    genre: 'fantasy',
    category: 'classic'
  }
}])

//Query Data
const results = await index.query<Metadata>({
  vector: [
    ... // query embedding
  ],
  includeVectors: true,
  includeMetadata: true
  topK: 1,
})

//Update Data
await index.upsert({
  id: "upstash-rocks",
  metadata: {
    title: 'Star Wars',
    genre: 'sci-fi',
    category: 'classic'
  }
});

//Delete record
await index.delete("upstash-rocks");

//Delete many by id
await index.delete(["id-1", "id-2", "id-3"]);

//Fetch records by their IDs
await index.fetch(["id-1", "id-2"]);

//Fetch records with range
await index.range({
      cursor: 0,
      limit: 5,
      includeVectors: true,
});

//Reset index
await index.reset();

//Info about index
await index.info();

//Random vector based on stored vectors
await index.random();
```

## Troubleshooting

We have a Discord for common problems. If you can't find a solution, please open an issue.

## Docs

See the documentation for details.

## Contributing

### Install Bun

### Vector Database

Create a new index on Upstash and copy the url and token.

### Running tests

```sh
bun run test
```

### Building

```sh
bun run build
```
