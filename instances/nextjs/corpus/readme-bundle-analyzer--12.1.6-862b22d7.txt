# @next/bundle-analyzer README 11.1.0 … 12.1.6: Next.js + Webpack Bundle Analyzer
# джерело: https://raw.githubusercontent.com/vercel/next.js/b188fab3360855c28fd9407bd07c4ee9f5de16a6/packages/next-bundle-analyzer/readme.md
# отримано: 2026-10-01
# версія: 12.1.6, 12.1.5, 12.1.4, 12.1.3, 12.1.2, 12.1.1, 12.1.0, 12.0.10, 11.1.4, 12.0.9, 12.0.8, 12.0.7, 11.1.3, 12.0.6, 12.0.5, 12.0.4, 12.0.3, 12.0.2, 12.0.1, 12.0.0, 11.1.2, 11.1.1, 11.1.0

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
