# @next/mdx README 11.1.0 … 11.1.4: Next.js + MDX
# джерело: https://raw.githubusercontent.com/vercel/next.js/75b7a57e0f0044d9315eb6adbd4231b67799d0b1/packages/next-mdx/readme.md
# отримано: 2026-10-01
# версія: 11.1.4, 12.0.7, 11.1.3, 12.0.6, 12.0.5, 12.0.4, 12.0.3, 12.0.2, 12.0.1, 12.0.0, 11.1.2, 11.1.1, 11.1.0

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
  pageExtensions: ['js', 'jsx', 'md', 'mdx'],
})
```

## TypeScript

Follow this guide from the MDX docs.
