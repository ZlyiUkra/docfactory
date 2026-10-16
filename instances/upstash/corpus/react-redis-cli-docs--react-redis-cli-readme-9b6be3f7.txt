# React Redis CLI for Upstash Redis
# джерело: https://github.com/upstash/react-redis-cli/blob/v0.1.2/README.md
# отримано: 2026-10-16
# версія: react-redis-cli-0.1.2, react-redis-cli-0.1.1, react-redis-cli-0.1.0

`@upstash/react-redis-cli` is a React component that provides a CLI interface to interact with Upstash Redis.

### Install

Install the component via npm:

```bash
$ npm install @upstash/react-redis-cli
```

### Usage

Here's a basic example of how to use the component:

```tsx
import { RedisCli } from "@upstash/react-redis-cli"

import "@upstash/react-redis-cli/dist/index.css"

export default function Page() {
  return (
    <main style={mainStyle}>
      <RedisCli url={UPSTASH_REDIS_REST_URL} token={UPSTASH_REDIS_REST_TOKEN} />
    </main>
  )
}

const mainStyle = {
  width: "100vw",
  maxWidth: "900px",
  height: "500px",
  margin: "0 auto",
}
```
