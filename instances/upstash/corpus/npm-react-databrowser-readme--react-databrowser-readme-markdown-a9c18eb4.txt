# @upstash/react-databrowser README 0.0.2
# джерело: https://registry.npmjs.org/@upstash/react-databrowser/-/react-databrowser-0.0.2.tgz
# отримано: 2026-10-16
# версія: react-databrowser-0.0.2

    @upstash/react-databrowser
    Databrowser for Upstash Redis

  upstash-react-cli.vercel.app

## 1. Install

```sh-session
$ npm install @upstash/react-databrowser
```

## 2. Add env keys

```sh-session
NEXT_PUBLIC_UPSTASH_REDIS_REST_URL=XXX
NEXT_PUBLIC_UPSTASH_REDIS_REST_TOKEN=XXX
```

## 3. Add a client component in your app:

```tsx
// /app/components/databrowser.tsx

"use client";
import { Databrowser } from "@upstash/react-databrowser";
import "@upstash/react-databrowser/dist/index.css";

export default function DatabrowserDemo() {
  return (
    <main
      style={{
        height: "100vh",
        width: "100vw",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        background: "rgb(250,250,250)",
      }}
    >
      <div
        style={{
          height: "100%",
          width: "100%",
          maxHeight: "45rem",
          maxWidth: "64rem",
          borderRadius: "0.5rem",
          overflow: "hidden",
        }}
      >
        <Databrowser />
      </div>
    </main>
  );
}

```
