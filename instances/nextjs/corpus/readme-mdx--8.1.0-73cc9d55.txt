# @next/mdx README 8.0.4 … 8.1.0: Next.js + MDX
# джерело: https://raw.githubusercontent.com/vercel/next.js/0dbd3b98eca0bee01a05b8414a60c48abba76abd/packages/next-mdx/readme.md
# отримано: 2026-10-01
# версія: 8.1.0, 8.0.4

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
    mdPlugins: [

    ],
    hastPlugins: [

    ]
  }
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
  }
})
```

Optionally you can match other file extensions for MDX compilation, by default only `.mdx` is supported

```js
// next.config.js
const withMDX = require('@next/mdx')({
  extension: /\.(md|mdx)$/
})
module.exports = withMDX()
```

## Top level .mdx pages

Define the `pagesExtensions` option to have Next.js handle `.mdx` files in the `pages` directory as pages:

```js
// next.config.js
const withMDX = require('@next/mdx')({
  extension: /\.mdx?$/
})
module.exports = withMDX({
  pageExtensions: ['js', 'jsx', 'mdx']
})
```
