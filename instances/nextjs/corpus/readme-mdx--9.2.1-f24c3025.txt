# @next/mdx README 9.0.6 … 9.2.1: Next.js + MDX
# джерело: https://raw.githubusercontent.com/vercel/next.js/45d5535b36e1c6794dce6bfafdda2d008771b6d1/packages/next-mdx/readme.md
# отримано: 2026-10-01
# версія: 9.2.1, 9.2.0, 9.1.7, 9.1.6, 9.1.5, 9.1.4, 9.1.3, 9.1.2, 9.1.1, 9.1.0, 9.0.8, 9.0.7, 9.0.6

Use MDX with Next.js

## Installation

```
npm install --save @next/mdx @mdx-js/loader
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

Optionally you can provide MDX options:

```js
// next.config.js
const withMDX = require('@next/mdx')({
  options: {
    mdPlugins: [],
    hastPlugins: [],
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
