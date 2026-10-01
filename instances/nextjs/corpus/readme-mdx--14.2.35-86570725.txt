# @next/mdx README 14.2.0 … 14.2.35: Next.js + MDX
# джерело: https://raw.githubusercontent.com/vercel/next.js/7b940d9ce96faddb9f92ff40f5e35c34ace04eb2/packages/next-mdx/readme.md
# отримано: 2026-10-01
# версія: 14.2.35, 14.2.34, 14.2.33, 14.2.32, 14.2.31, 14.2.30, 14.2.29, 14.2.28, 14.2.27, 14.2.26, 14.2.25, 14.2.24, 14.2.23, 14.2.22, 14.2.21, 14.2.20, 14.2.19, 14.2.18, 14.2.17, 14.2.16, 14.2.15, 14.2.14, 14.2.13, 14.2.12, 14.2.11, 14.2.10, 14.2.9, 14.2.8, 14.2.7, 14.2.6, 14.2.5, 14.2.4, 15.0.0-rc.0, 14.2.3, 14.2.2, 14.2.1, 14.2.0

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
  // Optionally, add any other Next.js config below
  reactStrictMode: true,
}

// Merge MDX config with Next.js config
module.exports = withMDX(nextConfig)
```

## TypeScript

Follow this guide from the MDX docs.
