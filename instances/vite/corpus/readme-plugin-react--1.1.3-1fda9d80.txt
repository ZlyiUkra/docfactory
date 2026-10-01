# @vitejs/plugin-react README 1.0.0-beta.0 … 1.1.3: @vitejs/plugin-react [![npm](https://img.shields.io/npm/v/@vitejs/plugin-react.svg)](https://npmjs.com/package/@vitejs/plugin-react)
# джерело: https://raw.githubusercontent.com/vitejs/vite/plugin-react@1.1.3/packages/plugin-react/README.md
# отримано: 2026-10-01
# версія: 1.1.3, 1.1.2, 1.1.1, 1.1.0, 1.1.0-beta.1, 1.0.9, 1.0.8, 1.1.0-beta.0, 1.0.7, 1.0.6, 1.0.5, 1.0.4, 1.0.3, 1.0.2, 1.0.1, 1.0.0, 1.0.0-beta.0

The all-in-one Vite plugin for React projects.

- enable Fast Refresh in development
- use the automatic JSX runtime
- avoid manual `import React` in `.jsx` and `.tsx` modules
- dedupe the `react` and `react-dom` packages
- use custom Babel plugins/presets

```js
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()]
})
```

## Filter which files use Fast Refresh

By default, Fast Refresh is used by files ending with `.js`, `.jsx`, `.ts`, and `.tsx`, except for files with a `node_modules` parent directory.

In some situations, you may not want a file to act as a HMR boundary, instead preferring that the changes propagate higher in the stack before being handled. In these cases, you can provide an `include` and/or `exclude` option, which can be a regex, a picomatch pattern, or an array of either. Files matching `include` and not `exclude` will use Fast Refresh. The defaults are always applied.

```js
react({
  // Exclude storybook stories
  exclude: /\.stories\.(t|j)sx?$/,
  // Only .tsx files
  include: '**/*.tsx'
})
```

## Babel configuration

The `babel` option lets you add plugins, presets, and other configuration to the Babel transformation performed on each JSX/TSX file.

```js
react({
  babel: {
    presets: [...],
    // Your plugins run before any built-in transform (eg: Fast Refresh)
    plugins: [...],
    // Use .babelrc files
    babelrc: true,
    // Use babel.config.js files
    configFile: true,
  }
})
```

### Proposed syntax

If you are using ES syntax that are still in proposal status (e.g. class properties), you can selectively enable them with the `babel.parserOpts.plugins` option:

```js
react({
  babel: {
    parserOpts: {
      plugins: ['decorators-legacy']
    }
  }
})
```

This option does not enable _code transformation_. That is handled by ESBuild.

**Note:** TypeScript syntax is handled automatically.

Here's the complete list of Babel parser plugins.

## Middleware mode

In middleware mode, you should make sure your entry `index.html` file is transformed by Vite. Here's an example for an Express server:

```js
app.get('/', async (req, res, next) => {
  try {
    let html = fs.readFileSync(path.resolve(root, 'index.html'), 'utf-8')

    // Transform HTML using Vite plugins.
    html = await viteServer.transformIndexHtml(req.url, html)

    res.send(html)
  } catch (e) {
    return next(e)
  }
})
```

Otherwise, you'll probably get this error:

```
Uncaught Error: @vitejs/plugin-react can't detect preamble. Something is wrong.
```
