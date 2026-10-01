# @next/mdx README 9.4.3 … 11.0.1: Next.js + MDX
# джерело: https://raw.githubusercontent.com/vercel/next.js/e969d226999bb0fcb52ecc203b359f3715ff69bf/packages/next-mdx/readme.md
# отримано: 2026-10-01
# версія: 11.0.1, 11.0.0, 10.2.3, 10.2.2, 10.2.1, 10.2.0, 10.1.3, 10.1.2, 10.1.1, 10.1.0, 10.0.9, 10.0.8, 10.0.7, 10.0.6, 10.0.5, 10.0.4, 10.0.3, 10.0.2, 10.0.1, 10.0.0, 9.5.5, 9.5.4, 9.5.3, 9.5.2, 9.5.1, 9.5.0, 9.4.4, 9.4.3

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

Define the `pageExtensions` option to have Next.js handle `.mdx` files in the `pages` directory as pages:

```js
// next.config.js
const withMDX = require('@next/mdx')({
  extension: /\.mdx?$/,
})
module.exports = withMDX({
  pageExtensions: ['js', 'jsx', 'mdx'],
})
```

## Typescript

Follow this guide from the MDX docs.
