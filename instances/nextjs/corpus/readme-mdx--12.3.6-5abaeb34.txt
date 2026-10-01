# @next/mdx README 12.3.1 … 12.3.6: Next.js + MDX
# джерело: https://raw.githubusercontent.com/vercel/next.js/a4e7a948b1a997e087df5d1bdd38d3cb57f5e968/packages/next-mdx/readme.md
# отримано: 2026-10-01
# версія: 12.3.6, 12.3.5, 13.1.5, 13.1.4, 13.1.3, 13.1.2, 13.1.1, 13.1.0, 13.0.7, 13.0.6, 13.0.5, 12.3.4, 13.0.4, 13.0.3, 12.3.3, 13.0.2, 13.0.1, 12.3.2, 13.0.0, 12.3.1

Use MDX with Next.js

## Installation

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
