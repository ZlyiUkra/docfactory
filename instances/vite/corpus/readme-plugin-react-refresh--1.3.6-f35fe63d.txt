# @vitejs/plugin-react-refresh README 1.3.4 … 1.3.6: @vitejs/plugin-react-refresh [![npm](https://img.shields.io/npm/v/@vitejs/plugin-react-refresh.svg)](https://npmjs.com/package/@vitejs/plugin-react-refresh)
# джерело: https://raw.githubusercontent.com/vitejs/vite/plugin-react-refresh@1.3.6/packages/plugin-react-refresh/README.md
# отримано: 2026-10-01
# версія: 1.3.6, 1.3.5, 1.3.4

Provides React Refresh support for Vite.

```js
// vite.config.js
import reactRefresh from '@vitejs/plugin-react-refresh'

export default {
  plugins: [reactRefresh()]
}
```

## Specifying Additional Parser Plugins

If you are using ES syntax that are still in proposal status (e.g. class properties), you can selectively enable them via the `parserPlugins` option:

```js
export default {
  plugins: [
    reactRefresh({
      parserPlugins: ['classProperties', 'classPrivateProperties']
    })
  ]
}
```

Full list of Babel parser plugins.

## Specifying files to include or exclude from refreshing

By default, @vite/plugin-react-refresh will process files ending with `.js`, `.jsx`, `.ts`, and `.tsx`, and excludes all files in `node_modules`.

In some situations you may not want a file to act as an HMR boundary, instead preferring that the changes propagate higher in the stack before being handled. In these cases, you can provide an `include` and/or `exclude` option, which can be regex or a picomatch pattern, or array of either. Files must match include and not exclude to be processed. Note, when using either `include`, or `exclude`, the defaults will not be merged in, so re-apply them if necessary.

```js
export default {
  plugins: [
    reactRefresh({
      // Exclude storybook stories and node_modules
      exclude: [/\.stories\.(t|j)sx?$/, /node_modules/],
      // Only .tsx files
      include: '**/*.tsx'
    })
  ]
}
```

### Notes

- If using TSX, any TS-supported syntax will already be transpiled away so you won't need to specify them here.

- This option only enables the plugin to parse these syntax - it does not perform any transpilation since this plugin is dev-only.

- If you wish to transpile the syntax for production, you will need to configure the transform separately using @rollup/plugin-babel as a build-only plugin.

## Middleware Mode Notes

When Vite is launched in **Middleware Mode**, you need to make sure your entry `index.html` file is transformed with `ViteDevServer.transformIndexHtml`. Otherwise, you may get an error prompting `Uncaught Error: @vitejs/plugin-react-refresh can't detect preamble. Something is wrong.`

To mitigate this issue, you can explicitly transform your `index.html` like this when configuring your express server:

```js
app.get('/', async (req, res, next) => {
  try {
    let html = fs.readFileSync(path.resolve(root, 'index.html'), 'utf-8')
    html = await viteServer.transformIndexHtml(req.url, html)
    res.send(html)
  } catch (e) {
    return next(e)
  }
})
```
