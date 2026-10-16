# @upstash/react-cli README 0.6.0
# джерело: https://registry.npmjs.org/@upstash/react-cli/-/react-cli-0.6.0.tgz
# отримано: 2026-10-16
# версія: react-cli-0.6.0

    @upstash/react-cli
    CLI for Upstash Redis

  upstash-react-cli.vercel.app

Upstash Redis CLI

## 1. Install

```sh-session
$ npm install @upstash/react-cli
```

## 2. Add a client component in your app:

```tsx
// /app/components/cli.tsx

"use client"
import { RedisCli } from "@upstash/react-cli";
import "@upstash/react-cli/dist/index.css";


<div
        style={{
          width: "100%",
          height: "100%",
          maxWidth: "48rem",
          maxHeight: "32rem",
        }}
      >
  <RedisCli url="UPSTASH_REDIS_REST_URL" token="UPSTASH_REDIS_REST_TOKEN" />;
</div>

```
