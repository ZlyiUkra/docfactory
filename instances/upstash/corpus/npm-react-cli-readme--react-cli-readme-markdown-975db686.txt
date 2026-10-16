# @upstash/react-cli README 0.2.0
# джерело: https://registry.npmjs.org/@upstash/react-cli/-/react-cli-0.2.0.tgz
# отримано: 2026-10-16
# версія: react-cli-0.2.0

    @upstash/react-cli
    CLI for Upstash Redis

  console.upstash.com/redis

## Install

```sh-session
$ npm install @upstash/react-cli
```

Add the package in your `next.config.js` file:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  transpilePackages: ["@upstash/react-cli"],
};

module.exports = nextConfig;
```

```tsx
import "@upstash/react-cli/dist/index.css";
import { RedisCli } from "@upstash/react-cli";

<RedisCli url="UPSTASH_REDIS_REST_URL" token="UPSTASH_REDIS_REST_TOKEN"/>

```
