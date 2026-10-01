# @vitejs/plugin-legacy README 1.0.0: @vitejs/plugin-legacy
# джерело: https://raw.githubusercontent.com/vitejs/vite/plugin-legacy@1.0.0/packages/plugin-legacy/README.md
# отримано: 2026-10-01
# версія: 1.0.0

Vite's default browser support baseline is Native ESM. This plugin provides support for legacy browsers that do not support native ESM.

By default, this plugin will:

- Generate a corresponding legacy chunk for every chunk in the final bundle, transformed with @babel/preset-env and emitted as SystemJS modules (code splitting is still supported!).

- Generate a polyfill chunk including SystemJS runtime, and any necessary polyfills determined by specified browser targets and **acutal usage** in the bundle.

- Inject `<script nomdule>` tags into generated HTML to conditionally load the polyfills and legacy bundle only in browsers without native ESM support.

## Usage

```js
// vite.config.js
import legacy from '@vitejs/plugin-legacy'

export default {
  plugins: [
    legacy({
      targets: [
        'defaults',
        'not IE 11'
      ]
    })
  ]
}
```

## Options

### `targets`

- **Type:** `string | string[] | { [key: string]: string }`
- **Default:** `'defaults'`

  If explicitly set, it's passed on to `@babel/preset-env`.

  The query is also Browserslist compatible. The default value, `'defaults'`, is what is recommended by Browserslist. See Browserslist Best Practices for more details.

### `polyfills`

- **Type:** `boolean | string[]`
- **Default:** `true`

  By default, a polyfills chunks is generated based on the target browser ranges and actual usage in the final bundle (detected via `@babel/preset-env`'s `useBuiltIns: 'usage'`).

  Set to a list of strings to explicitly control which polyfills to include. See Polyfill Specifiers for details.

  Set to `false` to avoid generating polyfills and handle it yourself (will still generate legacy chunks with syntax transformations).

### `ignoreBrowserslistConfig`

- **Type:** `boolean`
- **Default:** `false`

  `@babel/preset-env` automatically detects `browserslist` config sources:

  - `browserslist` field in `package.json`
  - `.browserslistrc` file in cwd.

  Set to `false` to ignore these sources.

### `modernPolyfills`

- **Type:** `boolean | string[]`
- **Default:** `false`

  Defaults to `false`. Enabling this option will generate a separate polyfills chunk for the modern build (targeting browsers with native ESM support).

  Set to a list of strings to explicitly control which polyfills to include. See Polyfill Specifiers for details.

  Note it is **not recommended** to use the `true` value (which uses auto detection) because `core-js@3` is very aggressive in polyfill inclusions due to all the bleeding edge features it supports. Even when targeting native ESM support, it injects 15kb of polyfills!

  If you don't have hard reliance on bleeding edge runtime features, it is not that hard to avoid having to use polyfills in the modern build altogether. Alternatively, consider using an on-demand service like Polyfill.io to only inject necessary polyfills based on actual browser useragents (most modern brwosers will need nothing!).

### `renderLegacyChunks`

- **Type:** `boolean`
- **Default:** `true`

  Set to `false` to disable legacy chunks. This is only useful if you are using `modernPolyfills`, which essentially allows you to use this plugin for injecting polyfills to the modern build only:

```js
  import legacy from '@vitejs/plugin-legacy'

  export default {
    plugins: [
      legacy({
        modernPolyfills: [
          /* ... */
        ],
        renderLegacyChunks: false
      })
    ]
  }
```

## Polyfill Sepcifiers

Polyfill specifier strings for `polyfills` and `modernPolyfills` can be either of the following:

- Any `core-js` 3 sub import paths - e.g. `es/map` will import `core-js/es/map`

- Any individual `core-js` 3 modules - e.g. `es.array.iterator` will import `core-js/modules/es.array.iterator.js`

**Example**

```js
import legacy from '@vitejs/plugin-legacy'

export default {
  plugins: [
    legacy({
      polyfills: [
        'es.promise.finally',
        'es/map',
        'es/set'
      ],
      modernPolyfills: [
        'es.promise.finally'
      ]
    })
  ]
}
```

## References

- Vue CLI modern mode
- Using Native JavaScript Modules in Production Today
- rollup-native-modules-boilerplate
