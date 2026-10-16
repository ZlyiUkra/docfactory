# @upstash/react-databrowser README 0.0.4 … 0.3.20: @upstash/react-databrowser
# джерело: https://registry.npmjs.org/@upstash/react-databrowser/-/react-databrowser-0.3.20.tgz
# отримано: 2026-10-16
# версія: react-databrowser-0.3.20, react-databrowser-0.3.19, react-databrowser-0.3.18, react-databrowser-0.3.17, react-databrowser-0.3.16, react-databrowser-0.3.15, react-databrowser-0.3.14, react-databrowser-0.3.13, react-databrowser-0.3.12, react-databrowser-0.3.11, react-databrowser-0.3.10, react-databrowser-0.3.9, react-databrowser-0.3.8, react-databrowser-0.3.7, react-databrowser-0.3.6, react-databrowser-0.3.5, react-databrowser-0.3.4, react-databrowser-0.3.3, react-databrowser-0.3.2, react-databrowser-0.3.1, react-databrowser-0.3.0, react-databrowser-0.2.10, react-databrowser-0.2.9, react-databrowser-0.2.8, react-databrowser-0.2.7, react-databrowser-0.2.6, react-databrowser-0.2.5, react-databrowser-0.2.4, react-databrowser-0.2.3, react-databrowser-0.2.2, react-databrowser-0.2.1, react-databrowser-0.2.0, react-databrowser-0.1.1, react-databrowser-0.1.0, react-databrowser-0.0.7, react-databrowser-0.0.6, react-databrowser-0.0.5, react-databrowser-0.0.4

    Databrowser for Upstash Redis

    Explore the demo application

---

## Introduction

`@upstash/react-databrowser` is a React component that provides a UI for browsing data in your Upstash Redis instances. It’s easy to set up and integrate into your React applications. This guide will help you get started with the installation and basic usage.

## Table of Contents

- Install
- Configuration
- Usage

## 1. Install

Install the databrowser component via npm:

```sh-session
$ npm install @upstash/react-databrowser
```

## 2. Configuration

### Environment Variables

Configure your Upstash Redis REST URL and token as environment variables:

```sh-session
NEXT_PUBLIC_UPSTASH_REDIS_REST_URL=YOUR_REDIS_REST_URL
NEXT_PUBLIC_UPSTASH_REDIS_REST_TOKEN=YOUR_REDIS_REST_TOKEN
```

## 3. Usage

### Creating the Data Browser Component

In your React application, create a new component that will utilize @upstash/react-databrowser.

Here's a basic example of how to use the component:

```tsx
// /app/components/DatabrowserDemo.tsx

import { Databrowser } from "@upstash/react-databrowser";
import "@upstash/react-databrowser/dist/index.css";

export default function DatabrowserDemo() {
  const redisUrl = process.env.NEXT_PUBLIC_UPSTASH_REDIS_REST_URL;
  const redisToken = process.env.NEXT_PUBLIC_UPSTASH_REDIS_REST_TOKEN;

  return (
    <main style={mainStyle}>
      <div style={divStyle}>
        <Databrowser token={redisToken} url={redisUrl}/>
      </div>
    </main>
  );
}

const mainStyle = {
  height: "100vh",
  width: "100vw",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  flexDirection: "column",
  background: "rgb(250,250,250)",
};

const divStyle = {
  height: "100%",
  width: "100%",
  maxHeight: "45rem",
  maxWidth: "64rem",
  borderRadius: "0.5rem",
  overflow: "hidden",
};

```
