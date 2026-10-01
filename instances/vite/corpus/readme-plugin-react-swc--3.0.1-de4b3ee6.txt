# @vitejs/plugin-react-swc README 3.0.1: @vitejs/plugin-react-swc [![npm](https://img.shields.io/npm/v/@vitejs/plugin-react-swc)](https://www.npmjs.com/package/@vitejs/plugin-react-swc)
# джерело: https://raw.githubusercontent.com/vitejs/vite-plugin-react-swc/63dbd6985f3aa93ff1c1e96ec3c899fa2f5bfdca/README.md
# отримано: 2026-10-01
# версія: 3.0.1

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

This plugin is only used in development and aims to be kept simple to enable good performances and be transpiler agnostic. Here is the list of non-configurable options that impact runtime behaviour:

- useDefineForClassFields is always activated, as this matches the current ECMAScript spec
- `jsx runtime` is always `automatic`
- In development:
  - esbuild is disabled, so the esbuild configuration has no effect
  - `target` is `es2020`
  - JS files are not transformed
  - tsconfig is not resolved, so properties other than the ones listed above behaves like TS defaults

## Changing the JSX import source

You can use the jsxImportSource option like this:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react({ jsxImportSource: "@emotion/react" })],
});
```

## Consistent components exports

For React refresh to work correctly, your file should only export React components. The best explanation I've read is the one from the Gatsby docs.

If an incompatible change in exports is found, the module will be invalidated and HMR will propagate. To make it easier to export simple constants alongside your component, the module is only invalidated when their value changes.

You can catch mistakes and get more detailed warning with this eslint rule.

## Migrating from `vite-plugin-swc-react-refresh`

The documentation for the previous version of the plugin is available in the v2 branch

To migrate, see this changelog
