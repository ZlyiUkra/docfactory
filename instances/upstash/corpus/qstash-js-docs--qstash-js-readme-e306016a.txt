# Upstash qStash SDK
# джерело: https://github.com/upstash/qstash-js/blob/v0.0.16/README.md
# отримано: 2026-10-16
# версія: qstash-0.0.16

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

## Status of the SDK

It is currently in beta and we are actively collecting feedback from the community.
Please report any issues you encounter or feature requests in the GitHub issues or talk to us on Discord. Thank you!

## How does qStash work?

qStash is the message broker between your serverless apps. You send aa HTTP
request to qStash, that includes a destination, a payload and optional settings.
We store your message durable and will deliver it to the destination API via
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

### Get your authorization token

Go to upstash and copy the token.

## Basic Usage:

### Publishing a message

```ts
import { Client } from "@upstash/qstash";
/**
 * Import a fetch polyfill only if you are using node prior to v18.
 * This is not necessary for nextjs, deno or cloudflare workers.
 */
import "isomorphic-fetch";

const c = new Client({
  token: "<QSTASH_TOKEN>",
});

const res = await c.publishJSON({
  destination: "https://my-api...",
  body: {
    hello: "world",
  },
});
console.log(res);
// { messageId: "msg_xxxxxxxxxxxxxxxx" }
```

### Receiving a message

How to consume a message depends on your http server. QStash does not receive
the http request directly, but should be called by you as the first step in your
handler function.

```ts
import { Receiver } from "@upstash/qstash";

const r = new Receiver({
  currentSigningKey: "..",
  nextSigningKey: "..",
});

const isValid = await r.verify({
  /**
   * The signature from the `Upstash-Signature` header.
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
