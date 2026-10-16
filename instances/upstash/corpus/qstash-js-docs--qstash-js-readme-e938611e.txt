# Upstash qStash SDK
# джерело: https://github.com/upstash/qstash-js/blob/v0.0.11/README.md
# отримано: 2026-10-16
# версія: qstash-0.0.11, qstash-0.0.10, qstash-0.0.9, qstash-0.0.8, qstash-0.0.7, qstash-0.0.6, qstash-0.0.5, qstash-0.0.4

Tests

**qStash** is a serverless queueing / messaging system, designed to be used with
serverless functions to consume from the queue.

It is the only connectionless (HTTP based) Redis client and designed for:

- Serverless functions (AWS Lambda ...)
- Cloudflare Workers (see
  the example)
- Fastly Compute@Edge (see
  the example)
- Next.js, Jamstack ...
- Client side web/mobile applications
- WebAssembly
- and other environments where HTTP is preferred over TCP.

See
the list of APIs
supported.

## How does qStash work?

qStash is the message broker between your serverless apps. You send a HTTP
request to qStash, that includes a destination, a payload and optional settings.
We store your message durable and will deliver it to the destination server via
HTTP. In case the destination is not ready to receive the message, we will retry
the message later, to guarentee at-least-once delivery.

## Quick Start

### Install

#### npm

```bash
npm install @upstash/qstash
```

#### Deno

```ts
import { Redis } from "https://deno.land/x/upstash_qstash/mod.ts";
```

### Activate qStash

Go to upstash and activate qStash.

## Basic Usage:

### Publishing a message

```ts
import { Client } from "@upstash/qstash"

const q = new Client({
  token: <QSTASH_TOKEN>,
})

const res = await q.publishJSON({
    body: { hello: "world" },
})

console.log(res.messageID)
```

### Consuming a message

How to consume a message depends on your http server. QStash does not receive
the http request directly, but should be called by you as the first step in your
handler function.

```ts
import { Consumer } from "@upstash/qstash";

const c = new Consumer({
  currentSigningKey: "..",
  nextSigningKey: "..",
});

const isValid = await c.verify({
  /**
   * The signature from the `upstash-signature` header.
   */
  signature: "string";

  /**
   * The raw request body.
   */
  body: "string";

  /**
   * URL of the endpoint where the request was sent to.
   */
  url: "string";
})
```

## Docs

See the documentation for details.

## Contributing

### Install Deno

### Running tests

```sh
QSTASH_TOKEN=".." deno test -A
```

```
```
