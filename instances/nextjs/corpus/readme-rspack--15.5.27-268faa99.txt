# next-rspack README 15.3.0 … 15.5.27: next-rspack (EXPERIMENTAL)
# джерело: https://raw.githubusercontent.com/vercel/next.js/v15.5.27/packages/next-rspack/README.md
# отримано: 2026-10-01
# версія: 15.5.27, 16.3.8, 16.3.7, 15.5.26, 16.3.6, 16.3.5, 15.5.25, 16.3.4, 15.5.24, 16.3.3, 16.3.2, 16.3.1, 15.5.23, 16.3.0, 16.3.0-preview.10, 16.2.12, 15.5.22, 16.3.0-preview.9, 16.3.0-preview.8, 16.3.0-preview.7, 16.2.11, 15.5.21, 16.3.0-preview.6, 15.5.20, 16.2.10, 16.3.0-preview.5, 16.3.0-preview.4, 16.3.0-preview.3, 16.2.9, 16.2.8, 16.3.0-preview.2, 16.3.0-preview.0, 15.5.19, 16.2.7, 15.5.18, 16.2.6, 15.5.16, 16.2.5, 16.2.4, 15.5.15, 16.2.3, 16.2.2, 16.2.1, 15.5.14, 16.2.0, 15.5.13, 16.1.7, 15.5.12, 15.5.11, 16.1.6, 15.3.9, 15.4.11, 16.0.11, 15.5.10, 16.1.5, 16.1.4, 16.1.3, 16.1.2, 16.1.1, 16.1.0, 15.3.8, 15.4.10, 16.0.10, 15.5.9, 15.3.7, 15.4.9, 16.0.9, 15.5.8, 16.0.8, 15.3.6, 15.4.8, 15.5.7, 16.0.7, 16.0.6, 16.0.5, 16.0.4, 16.0.3, 16.0.2, 16.0.1, 16.0.0, 15.5.6, 15.5.5, 16.0.0-beta.0, 15.5.4, 15.5.3, 15.5.2, 15.5.1, 15.5.0, 15.4.7, 15.4.6, 15.4.5, 15.4.4, 15.4.3, 15.4.2, 15.4.1, 15.4.0, 15.3.5, 15.3.4, 15.3.3, 15.3.2, 15.3.1, 15.3.0

> [!WARNING]
> This package is currently experimental. It's not an official Next.js plugin, and is supported by the Rspack team in partnership with Next.js. Help improve Next.js and Rspack by providing feedback at https://github.com/vercel/next.js/discussions/77800

This plugin allows you to use Rspack in place of webpack with Next.js.

## Installation

```
npm install next-rspack
```

or

```
yarn add next-rspack
```

## Usage

Create or update a `next.config.js`/`next.config.ts` and wrap your existing configuration:

```js
const withRspack = require('next-rspack')

/** @type {import('next').NextConfig} */
const nextConfig = {
  /* config options here */
}

module.exports = withRspack(nextConfig)
```

## Usage with next-compose-plugins

Alternatively, you can use `next-compose-plugins` to quickly integrate `next-rspack` with other Next.js plugins:

```js
const withPlugins = require('next-compose-plugins')
const withRspack = require('next-rspack')

module.exports = withPlugins([
  [withRspack],
  // your other plugins here
])
```
