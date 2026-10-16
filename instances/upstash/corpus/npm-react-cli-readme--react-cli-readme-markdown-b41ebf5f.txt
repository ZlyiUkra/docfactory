# @upstash/react-cli README 0.7.0 … 1.0.13
# джерело: https://registry.npmjs.org/@upstash/react-cli/-/react-cli-1.0.13.tgz
# отримано: 2026-10-16
# версія: react-cli-1.0.13, react-cli-1.0.12, react-cli-1.0.11, react-cli-1.0.10, react-cli-1.0.7, react-cli-1.0.6, react-cli-1.0.5, react-cli-1.0.4, react-cli-1.0.3, react-cli-1.0.2, react-cli-1.0.1, react-cli-1.0.0, react-cli-0.8.0, react-cli-0.7.3, react-cli-0.7.2, react-cli-0.7.1, react-cli-0.7.0

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

## With Tailwind CSS

If you already have a tailwindcss toolchain, you can omit the css import and add the library to your tailwind config file:

```js
// tailwind.config.js

module.exports = {
  content: [
    // ...
    "./node_modules/@upstash/react-cli/**/*.js", // <--  add this line
  ],
  //...
}

```
