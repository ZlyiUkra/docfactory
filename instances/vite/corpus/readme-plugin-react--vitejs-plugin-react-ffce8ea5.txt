# @vitejs/plugin-react README 4.3.0 … 4.3.4: @vitejs/plugin-react [![npm](https://img.shields.io/npm/v/@vitejs/plugin-react.svg)](https://npmjs.com/package/@vitejs/plugin-react)
# джерело: https://raw.githubusercontent.com/vitejs/vite-plugin-react/2e368a65aaf8314142538c369c296e277fdfb69b/packages/plugin-react/README.md
# отримано: 2026-10-01
# версія: 4.3.4, 4.3.3, 4.3.2, 4.3.1, 4.3.0

The default Vite plugin for React projects.

- enable Fast Refresh in development (requires react >= 16.9)
- use the automatic JSX runtime
- use custom Babel plugins/presets
- small installation size

```js
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

## Options

### include/exclude

Includes `.js`, `.jsx`, `.ts` & `.tsx` by default. This option can be used to add fast refresh to `.mdx` files:

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import mdx from '@mdx-js/rollup'

export default defineConfig({
  plugins: [
    { enforce: 'pre', ...mdx() },
    react({ include: /\.(mdx|js|jsx|ts|tsx)$/ }),
  ],
})
```

> `node_modules` are never processed by this plugin (but esbuild will)

### jsxImportSource

Control where the JSX factory is imported from. Default to `'react'`

```js
react({ jsxImportSource: '@emotion/react' })
```

### jsxRuntime

By default, the plugin uses the automatic JSX runtime. However, if you encounter any issues, you may opt out using the `jsxRuntime` option.

```js
react({ jsxRuntime: 'classic' })
```

### babel

The `babel` option lets you add plugins, presets, and other configuration to the Babel transformation performed on each included file.

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

Note: When not using plugins, only esbuild is used for production builds, resulting in faster builds.

#### Proposed syntax

If you are using ES syntax that are still in proposal status (e.g. class properties), you can selectively enable them with the `babel.parserOpts.plugins` option:

```js
react({
  babel: {
    parserOpts: {
      plugins: ['decorators-legacy'],
    },
  },
})
```

This option does not enable _code transformation_. That is handled by esbuild.

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

## Consistent components exports

For React refresh to work correctly, your file should only export React components. You can find a good explanation in the Gatsby docs.

If an incompatible change in exports is found, the module will be invalidated and HMR will propagate. To make it easier to export simple constants alongside your component, the module is only invalidated when their value changes.

You can catch mistakes and get more detailed warning with this eslint rule.
