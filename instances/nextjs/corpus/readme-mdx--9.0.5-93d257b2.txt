# @next/mdx README 9.0.0 … 9.0.5: Next.js + MDX
# джерело: https://raw.githubusercontent.com/vercel/next.js/2c7b4d8aaac475f81de21c0e9cb40fdea1a7a178/packages/next-mdx/readme.md
# отримано: 2026-10-01
# версія: 9.0.5, 9.0.4, 9.0.3, 9.0.2, 9.0.1, 9.0.0

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

Define the `pagesExtensions` option to have Next.js handle `.mdx` files in the `pages` directory as pages:

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
