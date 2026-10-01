# @next/bundle-analyzer README 12.2.0 … 13.5.11: Next.js + Webpack Bundle Analyzer
# джерело: https://raw.githubusercontent.com/vercel/next.js/492b7fb1e1b6026f5b2cc4caa5a5d739ef5039d1/packages/next-bundle-analyzer/readme.md
# отримано: 2026-10-01
# версія: 13.5.11, 12.3.6, 13.5.10, 12.3.5, 13.5.9, 13.5.8, 13.5.7, 14.1.4, 14.1.3, 14.1.2, 14.1.1, 14.1.0, 14.0.4, 14.0.3, 14.0.2, 14.0.1, 14.0.0, 13.5.6, 13.5.5, 13.5.4, 13.5.3, 13.5.2, 13.5.1, 13.5.0, 13.4.19, 13.4.18, 13.4.17, 13.4.16, 13.4.15, 13.4.13, 13.4.12, 13.4.11, 13.4.10, 13.4.9, 13.4.8, 13.4.7, 13.4.6, 13.4.5, 13.4.4, 13.4.3, 13.4.2, 13.4.1, 13.4.0, 13.3.4, 13.3.3, 13.3.2, 13.3.1, 13.3.0, 13.2.4, 13.2.3, 13.2.2, 13.2.1, 13.2.0, 13.1.6, 13.1.5, 13.1.4, 13.1.3, 13.1.2, 13.1.1, 13.1.0, 13.0.7, 13.0.6, 13.0.5, 12.3.4, 13.0.4, 13.0.3, 12.3.3, 13.0.2, 13.0.1, 12.3.2, 13.0.0, 12.2.6, 12.3.1, 12.3.0, 12.2.5, 12.2.4, 12.2.3, 12.2.2, 12.2.1, 12.2.0

Use `webpack-bundle-analyzer` in your Next.js project

## Installation

```
npm install @next/bundle-analyzer
```

or

```
yarn add @next/bundle-analyzer
```

Note: if installing as a `devDependency` make sure to wrap the require in a `process.env` check as `next.config.js` is loaded during `next start` as well.

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

#### Options

To disable automatically opening the report in your default browser, set `openAnalyzer` to false:

```js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
  openAnalyzer: false,
})
module.exports = withBundleAnalyzer({})
```

### Usage with next-compose-plugins

From version 2.0.0 of next-compose-plugins you need to call bundle-analyzer in this way to work

```js
const withPlugins = require('next-compose-plugins')
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withPlugins([
  [withBundleAnalyzer],
  // your other plugins here
])
```
