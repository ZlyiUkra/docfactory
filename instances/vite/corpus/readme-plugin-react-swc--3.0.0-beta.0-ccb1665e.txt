# @vitejs/plugin-react-swc README 3.0.0-beta.0: @vitejs/plugin-react-swc [![npm](https://img.shields.io/npm/v/@vitejs/plugin-react-swc)](https://www.npmjs.com/package/@vitejs/plugin-react-swc)
# джерело: https://raw.githubusercontent.com/vitejs/vite-plugin-react-swc/b78abc5e026bd9bf78c7f22096ca812d5dc46d9c/README.md
# отримано: 2026-10-01
# версія: 3.0.0-beta.0

Use the versatility of SWC for development and the maturity of esbuild for production.

- ✅ A fast Fast Refresh (~20x faster than Babel)
- ✅ Enable automatic JSX runtime

> ⚠️ This is an alpha release for Vite 4, for the v2 named `vite-plugin-swc-react-refresh`, see the v2 branch.

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

## Consistent components exports

For React refresh to work, your file should only export React components. The best explanation I've read is the one from the Gatsby docs.

You can catch mistakes and get more detailed warning with this eslint rule.
