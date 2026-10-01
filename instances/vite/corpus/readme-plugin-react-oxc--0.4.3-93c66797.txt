# @vitejs/plugin-react-oxc README 0.4.1 … 0.4.3
# джерело: https://raw.githubusercontent.com/vitejs/vite-plugin-react/a06940b10c3d7c19236f1f176fc0a1748b9f62e7/packages/plugin-react-oxc/README.md
# отримано: 2026-10-01
# версія: 0.4.3, 0.4.2, 0.4.1

> [!IMPORTANT]
> This package is deprecated. Please use @vitejs/plugin-react instead, which automatically enables Oxc-based Fast Refresh transform on `rolldown-vite`.

## @vitejs/plugin-react-oxc npm

The future default Vite plugin for React projects.

- enable Fast Refresh in development
- use the automatic JSX runtime
- small installation size

```js
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-oxc'

export default defineConfig({
  plugins: [react()],
})
```

## Caveats

- `jsx runtime` is always `automatic`
- this plugin only works with `rolldown-vite`

## Options

### include/exclude

Includes `.js`, `.jsx`, `.ts` & `.tsx` and excludes `/node_modules/` by default. This option can be used to add fast refresh to `.mdx` files:

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

### jsxImportSource

Control where the JSX factory is imported from. Default to `'react'`

```js
react({ jsxImportSource: '@emotion/react' })
```

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
Uncaught Error: @vitejs/plugin-react-oxc can't detect preamble. Something is wrong.
```

## Consistent components exports

For React refresh to work correctly, your file should only export React components. You can find a good explanation in the Gatsby docs.

If an incompatible change in exports is found, the module will be invalidated and HMR will propagate. To make it easier to export simple constants alongside your component, the module is only invalidated when their value changes.

You can catch mistakes and get more detailed warning with this eslint rule.
