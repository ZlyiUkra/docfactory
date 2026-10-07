# @vitejs/plugin-react-swc README 3.6.0 … 3.7.0: @vitejs/plugin-react-swc [![npm](https://img.shields.io/npm/v/@vitejs/plugin-react-swc)](https://www.npmjs.com/package/@vitejs/plugin-react-swc)
# джерело: https://raw.githubusercontent.com/vitejs/vite-plugin-react-swc/b829b03f6476bed60ff5535fe883abc1b0b4e095/README.md
# отримано: 2026-10-01
# версія: 3.7.0, 3.6.0

Speed up your Vite dev server with SWC

- ✅ A fast Fast Refresh (~20x faster than Babel)
- ✅ Enable automatic JSX runtime

## Installation

```sh
npm i -D @vitejs/plugin-react-swc
```

## Usage

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
});
```

## Caveats

This plugin has limited options to enable good performances and be transpiler agnostic. Here is the list of non-configurable options that impact runtime behaviour:

- useDefineForClassFields is always activated, as this matches the current ECMAScript spec
- `jsx runtime` is always `automatic`
- In development:
  - esbuild is disabled, so the esbuild configuration has no effect
  - `target` is `es2020`
  - JS files are not transformed
  - tsconfig is not resolved, so properties other than the ones listed above behaves like TS defaults

## Options

### jsxImportSource

Control where the JSX factory is imported from.

`@default` "react"

```ts
react({ jsxImportSource: "@emotion/react" });
```

### tsDecorators

Enable TypeScript decorators. Requires `experimentalDecorators` in tsconfig.

`@default` false

```ts
react({ tsDecorators: true });
```

### plugins

Use SWC plugins. Enable SWC at build time.

```ts
react({ plugins: [["@swc/plugin-styled-components", {}]] });
```

### devTarget

Set the target for SWC in dev. This can avoid to down-transpile private class method for example.

For production target, see https://vitejs.dev/config/build-options.html#build-target.

`@default` "es2020"

```ts
react({ devTarget: "es2022" });
```

### parserConfig

Override the default include list (.ts, .tsx, .mts, .jsx, .mdx).

This requires to redefine the config for any file you want to be included (ts, mdx, ...).

If you want to trigger fast refresh on compiled JS, use `jsx: true`. Exclusion of node_modules should be handled by the function if needed. Using this option to use JSX inside `.js` files is highly discouraged and can be removed in any future version.

```ts
react({
  parserConfig(id) {
    if (id.endsWith(".res")) return { syntax: "ecmascript", jsx: true };
    if (id.endsWith(".ts")) return { syntax: "typescript", tsx: false };
  },
});
```

## Consistent components exports

For React refresh to work correctly, your file should only export React components. The best explanation I've read is the one from the Gatsby docs.

If an incompatible change in exports is found, the module will be invalidated and HMR will propagate. To make it easier to export simple constants alongside your component, the module is only invalidated when their value changes.

You can catch mistakes and get more detailed warning with this eslint rule.

## Migrating from `vite-plugin-swc-react-refresh`

The documentation for the previous version of the plugin is available in the v2 branch

To migrate, see this changelog
