# @next/bundle-analyzer README 9.0.0 … 9.2.1: Next.js + Webpack Bundle Analyzer
# джерело: https://raw.githubusercontent.com/vercel/next.js/45d5535b36e1c6794dce6bfafdda2d008771b6d1/packages/next-bundle-analyzer/readme.md
# отримано: 2026-10-01
# версія: 9.2.1, 9.2.0, 9.1.7, 9.1.6, 9.1.5, 9.1.4, 9.1.3, 9.1.2, 9.1.1, 9.1.0, 9.0.8, 9.0.7, 9.0.6, 9.0.5, 9.0.4, 9.0.3, 9.0.2, 9.0.1, 9.0.0

Use `webpack-bundle-analyzer` in your Next.js project

## Installation

```
npm install --save @next/bundle-analyzer
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
