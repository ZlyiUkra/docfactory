# @next/mdx README 12.0.8 … 12.2.6: Next.js + MDX
# джерело: https://raw.githubusercontent.com/vercel/next.js/63fe37140159f7bdc33e7eafbd66496faadddd87/packages/next-mdx/readme.md
# отримано: 2026-10-01
# версія: 12.2.6, 12.3.0, 12.2.5, 12.2.4, 12.2.3, 12.2.2, 12.2.1, 12.2.0, 12.1.6, 12.1.5, 12.1.4, 12.1.3, 12.1.2, 12.1.1, 12.1.0, 12.0.10, 12.0.9, 12.0.8

Use MDX with Next.js

## Installation

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
