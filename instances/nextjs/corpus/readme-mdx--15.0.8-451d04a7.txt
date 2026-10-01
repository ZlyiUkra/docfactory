# @next/mdx README 15.0.0-rc.1 … 15.0.8: Next.js + MDX
# джерело: https://raw.githubusercontent.com/vercel/next.js/16eb2af3da89b036fd4783f77631cb6bf5c1fe9f/packages/next-mdx/readme.md
# отримано: 2026-10-01
# версія: 15.0.8, 15.1.12, 15.2.9, 15.3.9, 15.0.7, 15.1.11, 15.2.8, 15.3.8, 15.0.6, 15.1.10, 15.2.7, 15.3.7, 15.2.6, 15.3.6, 15.0.5, 15.1.9, 15.3.5, 15.3.4, 15.3.3, 15.1.8, 15.3.2, 15.3.1, 15.3.0, 15.2.5, 15.2.4, 15.2.3, 15.2.2, 15.2.1, 15.2.0, 15.1.7, 15.1.6, 15.1.5, 15.1.4, 15.1.3, 15.1.2, 15.1.1, 15.1.0, 15.0.4, 15.0.3, 15.0.2, 15.0.1, 15.0.0, 15.0.0-rc.1

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

By default MDX will only match and compile MDX files with the `.mdx` extension.
However, it can also be optionally configured to handle markdown files with the `.md` extension, as shown below:

```js
// next.config.js
const withMDX = require('@next/mdx')({
  extension: /\.(md|mdx)$/,
})
module.exports = withMDX()
```

In addition, MDX can be customized with compiler options, see the mdx documentation for details on supported options.

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

Create an `mdx-components.js` file at the root of your project with the following contents:

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
  },
})

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configure pageExtensions to include md and mdx
  pageExtensions: ['ts', 'tsx', 'js', 'jsx', 'md', 'mdx'],
  // Optionally, add any other Next.js config below
  reactStrictMode: true,
}

// Merge MDX config with Next.js config
module.exports = withMDX(nextConfig)
```

## TypeScript

Follow this guide from the MDX docs.
