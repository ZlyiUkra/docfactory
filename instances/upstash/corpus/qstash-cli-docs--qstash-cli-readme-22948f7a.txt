# Upstash QStash CLI
# джерело: https://github.com/upstash/qstash-cli/blob/v2.40.12/README.md
# отримано: 2026-10-16
# версія: qstash-cli-2.40.12, qstash-cli-2.37.18, qstash-cli-2.32.32, qstash-cli-2.30.4, qstash-cli-2.28.3, qstash-cli-2.27.9, qstash-cli-2.22.3, qstash-cli-2.21.1, qstash-cli-2.20.10

> [!NOTE]
> **This project is in GA Stage.**
> The Upstash Professional Support fully covers this project. It receives regular updates, and bug fixes.
> The Upstash team is committed to maintaining and improving its functionality.

QStash CLI is a command-line tool that helps developers work with QStash locally. The only command currently available is `dev`, which runs a local QStash server for development and testing purposes.

**QStash** is an HTTP based messaging and scheduling solution for serverless and
edge runtimes.

It is 100% built on stateless HTTP requests and designed for:

- Serverless functions (AWS Lambda ...)
- Cloudflare Workers (see
  the example)
- Fastly Compute@Edge
- Next.js, including edge
- Deno
- Client side web/mobile applications
- WebAssembly
- and other environments where HTTP is preferred over TCP.

## Quick Start

### Install

```bash
npm install @upstash/qstash-cli
```

## Basic Usage:

```bash
npx @upstash/qstash-cli dev
```

### Available Commands

```bash
Usage:
        qstash-cli [command] [options]
Commands:
        dev     Start a local dev server
Options:
        -port  The port number to start server on (default: 8080)
```

## Docs

See the local development guide for details.
