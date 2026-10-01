# @next/bundle-analyzer README 9.2.2 … 9.4.4: Next.js + Webpack Bundle Analyzer
# джерело: https://raw.githubusercontent.com/vercel/next.js/e6eb32f67639d6306b885573c37f9a906dcc03e0/packages/next-bundle-analyzer/readme.md
# отримано: 2026-10-01
# версія: 9.4.4, 9.4.3, 9.4.2, 9.4.1, 9.4.0, 9.3.6, 9.3.5, 9.3.4, 9.3.3, 9.3.2, 9.3.1, 9.3.0, 9.2.2

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

Then you can run the command below:

```bash
# Analyze is done on build when env var is set
ANALYZE=true yarn build
```

When enabled two HTML files (client.html and server.html) will be outputted to `<distDir>/analyze/`. One will be for the server bundle, one for the browser bundle.
