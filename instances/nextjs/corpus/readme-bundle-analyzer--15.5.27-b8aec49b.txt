# @next/bundle-analyzer README 14.2.0 … 15.5.27: Next.js + Webpack Bundle Analyzer
# джерело: https://raw.githubusercontent.com/vercel/next.js/v15.5.27/packages/next-bundle-analyzer/readme.md
# отримано: 2026-10-01
# версія: 15.5.27, 16.3.8, 16.3.7, 15.5.26, 16.3.6, 16.3.5, 15.5.25, 16.3.4, 15.5.24, 16.3.3, 16.3.2, 16.3.1, 15.5.23, 16.3.0, 16.3.0-preview.10, 16.2.12, 15.5.22, 16.3.0-preview.9, 16.3.0-preview.8, 16.3.0-preview.7, 16.2.11, 15.5.21, 16.3.0-preview.6, 15.5.20, 16.2.10, 16.3.0-preview.5, 16.3.0-preview.4, 16.3.0-preview.3, 16.2.9, 16.2.8, 16.3.0-preview.2, 16.3.0-preview.0, 15.5.19, 16.2.7, 15.5.18, 16.2.6, 15.5.16, 16.2.5, 16.2.4, 15.5.15, 16.2.3, 16.2.2, 16.2.1, 15.5.14, 16.2.0, 15.5.13, 16.1.7, 15.5.12, 15.5.11, 16.1.6, 15.0.8, 15.1.12, 15.2.9, 15.3.9, 15.4.11, 16.0.11, 15.5.10, 16.1.5, 16.1.4, 16.1.3, 16.1.2, 16.1.1, 16.1.0, 14.2.35, 15.0.7, 15.1.11, 15.2.8, 15.3.8, 15.4.10, 16.0.10, 15.5.9, 15.0.6, 15.1.10, 15.2.7, 14.2.34, 15.3.7, 15.4.9, 16.0.9, 15.5.8, 16.0.8, 15.2.6, 15.3.6, 15.0.5, 15.1.9, 15.4.8, 15.5.7, 16.0.7, 16.0.6, 16.0.5, 16.0.4, 16.0.3, 16.0.2, 16.0.1, 16.0.0, 15.5.6, 15.5.5, 16.0.0-beta.0, 14.2.33, 15.5.4, 15.5.3, 15.5.2, 15.5.1, 15.5.0, 14.2.32, 15.4.7, 15.4.6, 14.2.31, 15.4.5, 15.4.4, 15.4.3, 15.4.2, 15.4.1, 15.4.0, 15.3.5, 15.3.4, 14.2.30, 15.3.3, 15.1.8, 14.2.29, 15.3.2, 15.3.1, 15.3.0, 15.2.5, 14.2.28, 14.2.27, 14.2.26, 15.2.4, 15.2.3, 14.2.25, 15.2.2, 15.2.1, 15.2.0, 15.1.7, 14.2.24, 15.1.6, 15.1.5, 15.1.4, 14.2.23, 15.1.3, 14.2.22, 14.2.21, 15.1.2, 15.1.1, 15.1.0, 15.0.4, 14.2.20, 14.2.19, 14.2.18, 15.0.3, 14.2.17, 15.0.2, 14.2.16, 15.0.1, 15.0.0, 15.0.0-rc.1, 14.2.15, 14.2.14, 14.2.13, 14.2.12, 14.2.11, 14.2.10, 14.2.9, 14.2.8, 14.2.7, 14.2.6, 14.2.5, 14.2.4, 15.0.0-rc.0, 14.2.3, 14.2.2, 14.2.1, 14.2.0

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

When enabled three HTML files (client.html, edge.html and nodejs.html) will be outputted to `<distDir>/analyze/`. One will be for the nodejs server bundle, one for the edge server bundle, and one for the browser bundle.

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
