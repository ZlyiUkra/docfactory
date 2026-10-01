# @next/bundle-analyzer README 8.0.4 … 8.1.0: Next.js + Webpack Bundle Analyzer
# джерело: https://raw.githubusercontent.com/vercel/next.js/0dbd3b98eca0bee01a05b8414a60c48abba76abd/packages/next-bundle-analyzer/readme.md
# отримано: 2026-10-01
# версія: 8.1.0, 8.0.4

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
const withBundleAnalyzer = require("@next/bundle-analyzer")({ enabled: process.env.ANALYZE === "true" });
module.exports = withBundleAnalyzer({});
```

Then you can run the command below:

```bash
# Analyze is done on build when env var is set
ANALYZE=true yarn build
```

When enabled two HTML files (client.html and server.html) will be outputted to `<distDir>/analyze/`. One will be for the server bundle, one for the browser bundle.
