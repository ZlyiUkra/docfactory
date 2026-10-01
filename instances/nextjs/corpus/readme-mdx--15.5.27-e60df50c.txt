# @next/mdx README 15.5.0 … 15.5.27: Next.js + MDX
# джерело: https://raw.githubusercontent.com/vercel/next.js/v15.5.27/packages/next-mdx/readme.md
# отримано: 2026-10-01
# версія: 15.5.27, 16.3.8, 16.3.7, 15.5.26, 16.3.6, 16.3.5, 15.5.25, 16.3.4, 15.5.24, 16.3.3, 16.3.2, 16.3.1, 15.5.23, 16.3.0, 16.3.0-preview.10, 16.2.12, 15.5.22, 16.3.0-preview.9, 16.3.0-preview.8, 16.3.0-preview.7, 16.2.11, 15.5.21, 16.3.0-preview.6, 15.5.20, 16.2.10, 16.3.0-preview.5, 16.3.0-preview.4, 16.3.0-preview.3, 16.2.9, 16.2.8, 16.3.0-preview.2, 16.3.0-preview.0, 15.5.19, 16.2.7, 15.5.18, 16.2.6, 15.5.16, 16.2.5, 16.2.4, 15.5.15, 16.2.3, 16.2.2, 16.2.1, 15.5.14, 16.2.0, 15.5.13, 16.1.7, 15.5.12, 15.5.11, 16.1.6, 16.0.11, 15.5.10, 16.1.5, 16.1.4, 16.1.3, 16.1.2, 16.1.1, 16.1.0, 16.0.10, 15.5.9, 16.0.9, 15.5.8, 16.0.8, 15.5.7, 16.0.7, 16.0.6, 16.0.5, 16.0.4, 16.0.3, 16.0.2, 16.0.1, 16.0.0, 15.5.6, 15.5.5, 16.0.0-beta.0, 15.5.4, 15.5.3, 15.5.2, 15.5.1, 15.5.0

Use MDX with Next.js

## Installation

For usage with the `app` directory see the section below.

```
npm install @next/mdx @mdx-js/loader
```

or

```
yarn add @next/mdx @mdx-js/loader
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
// Allows customizing built-in components, e.g. to add styling.
const components = {
  // h1: ({ children }) => <h1 style={{ fontSize: "100px" }}>{children}</h1>,
}

export function useMDXComponents() {
  return components
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
