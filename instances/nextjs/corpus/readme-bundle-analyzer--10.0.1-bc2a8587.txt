# @next/bundle-analyzer README 9.5.3 … 10.0.1: Next.js + Webpack Bundle Analyzer
# джерело: https://raw.githubusercontent.com/vercel/next.js/3c3379412eeb0f877cef54bd6fe7afa9512c8ee5/packages/next-bundle-analyzer/readme.md
# отримано: 2026-10-01
# версія: 10.0.1, 10.0.0, 9.5.5, 9.5.4, 9.5.3

Use `webpack-bundle-analyzer` in your Next.js project

## Installation

```
npm install @next/bundle-analyzer
```

or

```
yarn add @next/bundle-analyzer
```

### Usage with environment variables

Create a next.config.js (and make sure you have next-bundle-analyzer set up)

```js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})
module.exports = withBundleAnalyzer({})
```

Or configuration as a function:

```js
module.exports = (phase, defaultConfig) => {
  return withBundleAnalyzer(defaultConfig)
}
```

Then you can run the command below:

```bash
# Analyze is done on build when env var is set
ANALYZE=true yarn build
```

When enabled two HTML files (client.html and server.html) will be outputted to `<distDir>/analyze/`. One will be for the server bundle, one for the browser bundle.

### Usage with next-compose-plugins

From version 2.0.0 of next-compose-plugins you need to call bundle-analyzer in this way to work

```js
const withPlugins = require('next-compose-plugins')
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})
module.exports = withPlugins([
  [withBundleAnalyzer({})],
  // your other plugins here
])
```
