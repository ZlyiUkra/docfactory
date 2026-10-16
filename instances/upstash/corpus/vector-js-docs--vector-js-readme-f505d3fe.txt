# Upstash Vector Node.js Client · [](https://github.com/upstash/vector-js/actions/workflows/tests.yaml)
# джерело: https://github.com/upstash/vector-js/blob/v1.0.7/README.md
# отримано: 2026-10-16
# версія: vector-1.0.7, vector-1.0.6, vector-1.0.5

> [!NOTE] > **This project is in GA Stage.**
>
> The Upstash Professional Support fully covers this project. It receives regular updates, and bug fixes. The Upstash team is committed to maintaining and improving its functionality.

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
  filter: "genre = 'fantasy' and title = 'Lord of the Rings'"
})

// If you wanna learn more about filtering check: [Metadata Filtering](https://upstash.com/docs/vector/features/filtering)

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

## Metadata Filtering

If you wanna learn more about filtering check: Metadata Filtering

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

### Contributing

Make sure you have Bun.js installed and have those relevant keys with specific vector dimensions:

```bash

## Vector dimension should be 2
UPSTASH_VECTOR_REST_URL="XXXXX"
UPSTASH_VECTOR_REST_TOKEN="XXXXX"

## Vector dimension should be 384
EMBEDDING_UPSTASH_VECTOR_REST_URL="XXXXX"
EMBEDDING_UPSTASH_VECTOR_REST_TOKEN="XXXXX"
```
