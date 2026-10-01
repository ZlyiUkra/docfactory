# @next/mdx README 13.2.0 … 13.4.5: Next.js + MDX
# джерело: https://raw.githubusercontent.com/vercel/next.js/db10dd674088fb04cadee2b6830bec55b70fe1ad/packages/next-mdx/readme.md
# отримано: 2026-10-01
# версія: 13.4.5, 13.4.4, 13.4.3, 13.4.2, 13.4.1, 13.4.0, 13.3.4, 13.3.3, 13.3.2, 13.3.1, 13.3.0, 13.2.4, 13.2.3, 13.2.2, 13.2.1, 13.2.0

Use MDX with Next.js

## Installation

For usage with the `app` directory see the section below.

```
npm install @next/mdx @mdx-js/loader @mdx-js/react
```

or

```
yarn add @next/mdx @mdx-js/loader @mdx-js/react
```

## Usage

Create a `next.config.js` in your project

```js
// next.config.js
const withMDX = require('@next/mdx')()
module.exports = withMDX()
```

Optionally you can provide MDX plugins:

```js
// next.config.js
const withMDX = require('@next/mdx')({
  options: {
    remarkPlugins: [],
    rehypePlugins: [],
  },
})
module.exports = withMDX()
```

Optionally you can add your custom Next.js configuration as parameter

```js
// next.config.js
const withMDX = require('@next/mdx')()
module.exports = withMDX({
  webpack(config, options) {
    return config
  },
})
```

Optionally you can match other file extensions for MDX compilation, by default only `.mdx` is supported

```js
// next.config.js
const withMDX = require('@next/mdx')({
  extension: /\.(md|mdx)$/,
})
module.exports = withMDX()
```

## Top level .mdx pages

Define the `pageExtensions` option to have Next.js handle `.md` and `.mdx` files in the `pages` directory as pages:

```js
// next.config.js
const withMDX = require('@next/mdx')({
  extension: /\.mdx?$/,
})
module.exports = withMDX({
  pageExtensions: ['js', 'jsx', 'ts', 'tsx', 'md', 'mdx'],
})
```

## TypeScript

Follow this guide from the MDX docs.

---

## App directory

## Installation

For usage with the `app` directory see below.

```
npm install @next/mdx
```

or

```
yarn add @next/mdx
```

## Usage

Create a `mdx-components.js` file at the root of your project with the following contents:

```js
// This file is required to use @next/mdx in the `app` directory.
export function useMDXComponents(components) {
  return components
  // Allows customizing built-in components, e.g. to add styling.
  // return {
  //   h1: ({ children }) => <h1 style={{ fontSize: "100px" }}>{children}</h1>,
  //   ...components,
  // }
}
```

Create a `next.config.js` in your project

```js
// next.config.js
const withMDX = require('@next/mdx')({
  // Optionally provide remark and rehype plugins
  options: {
    // If you use remark-gfm, you'll need to use next.config.mjs
    // as the package is ESM only
    // https://github.com/remarkjs/remark-gfm#install
    remarkPlugins: [],
    rehypePlugins: [],
    // If you use `MDXProvider`, uncomment the following line.
    // providerImportSource: "@mdx-js/react",
  },
})

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configure pageExtensions to include md and mdx
  pageExtensions: ['ts', 'tsx', 'js', 'jsx', 'md', 'mdx'],
  experimental: {
    appDir: true,
  }
  // Optionally, add any other Next.js config below
  reactStrictMode: true,
}

// Merge MDX config with Next.js config
module.exports = withMDX(nextConfig)
```

## TypeScript

Follow this guide from the MDX docs.
