# RedisBrowser for Upstash Redis
# джерело: https://github.com/upstash/react-redis-browser/blob/v0.1.11/README.md
# отримано: 2026-10-16
# версія: react-redis-browser-0.1.11, react-redis-browser-0.1.10, react-redis-browser-0.1.9, react-redis-browser-0.1.8, react-redis-browser-0.1.7, react-redis-browser-0.1.6, react-redis-browser-0.1.5, react-redis-browser-0.1.4, react-redis-browser-0.1.3, react-redis-browser-0.1.2

`@upstash/react-redis-browser` is a React component that provides a UI for browsing and editing data in your Upstash Redis instances.

### Install

Install the databrowser component via npm:

```bash
$ npm install @upstash/react-redis-browser
```

### Usage

Here's a basic example of how to use the component:

```tsx
import { RedisBrowser } from "@upstash/react-redis-browser"
import "@upstash/react-redis-browser/dist/index.css"

export default function RedisBrowserDemo() {
  return (
    <main style={mainStyle}>
      <RedisBrowser
        url={UPSTASH_REDIS_REST_URL}
        token={UPSTASH_REDIS_REST_TOKEN} />
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
