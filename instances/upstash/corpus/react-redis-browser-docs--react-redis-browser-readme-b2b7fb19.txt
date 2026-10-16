# Redis Browser for Upstash Redis - [Preview](https://react-redis-browser.vercel.app/)
# джерело: https://github.com/upstash/react-redis-browser/blob/v0.2.13/README.md
# отримано: 2026-10-16
# версія: react-redis-browser-0.2.13, react-redis-browser-0.2.12, react-redis-browser-0.2.11, react-redis-browser-0.2.10, react-redis-browser-0.2.9, react-redis-browser-0.2.8, react-redis-browser-0.2.7, react-redis-browser-0.2.6, react-redis-browser-0.2.5, react-redis-browser-0.2.4, react-redis-browser-0.2.3, react-redis-browser-0.2.2, react-redis-browser-0.2.1, react-redis-browser-0.2.0

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

export default function Page() {
  return (
    <RedisBrowser
      url={UPSTASH_REDIS_REST_URL}
      token={UPSTASH_REDIS_REST_TOKEN}
    />
  )
}
```

### Persistance

The state of the databrowser can be persisted using the `storage` property.

```tsx
import { RedisBrowser } from "@upstash/react-redis-browser"
import "@upstash/react-redis-browser/dist/index.css"

export default function Page() {
  return (
    <RedisBrowser
      url={UPSTASH_REDIS_REST_URL}
      token={UPSTASH_REDIS_REST_TOKEN}
      storage={{
        get: () => localStorage.getItem("databrowser") || "",
        set: (value) => localStorage.setItem("databrowser", value),
      }}
    />
  )
}
```
