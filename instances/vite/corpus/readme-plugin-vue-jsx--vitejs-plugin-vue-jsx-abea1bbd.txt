# @vitejs/plugin-vue-jsx README 5.1.0 … 5.1.6: @vitejs/plugin-vue-jsx [![npm](https://img.shields.io/npm/v/@vitejs/plugin-vue-jsx.svg)](https://npmjs.com/package/@vitejs/plugin-vue-jsx)
# джерело: https://raw.githubusercontent.com/vitejs/vite-plugin-vue/plugin-vue-jsx@5.1.6/packages/plugin-vue-jsx/README.md
# отримано: 2026-10-01
# версія: 5.1.6, 5.1.5, 5.1.4, 5.1.3, 5.1.2, 5.1.1, 5.1.0

Provides Vue 3 JSX & TSX support with HMR.

```js
// vite.config.js
import vueJsx from '@vitejs/plugin-vue-jsx'

export default {
  plugins: [
    vueJsx({
      // options are passed on to @vue/babel-plugin-jsx
    }),
  ],
}
```

## Options

### include

Type: `(string | RegExp)[] | string | RegExp | null`

Default: `/\.[jt]sx$/`

A picomatch pattern, or array of patterns, which specifies the files the plugin should operate on.

### exclude

Type: `(string | RegExp)[] | string | RegExp | null`

Default: `undefined`

A picomatch pattern, or array of patterns, which specifies the files to be ignored by the plugin.

> See @vue/babel-plugin-jsx for other options.

### defineComponentName

Type: `string[]`

Default: `['defineComponent']`

The name of the function to be used for defining components. This is useful when you have a custom `defineComponent` function.

### tsTransform

Type: `'babel' | 'built-in'`

Default: `'babel'`

Defines how `typescript` transformation is handled for `.tsx` files.

`'babel'` - `typescript` transformation is handled by `@babel/plugin-transform-typescript` during `babel` invocation for JSX transformation.

`'built-in'` - `babel` is invoked only for JSX transformation and then `typescript` transformation is handled by the same toolchain used for `.ts` files (currently `esbuild`).

### babelPlugins

Type: `any[]`

Default: `undefined`

Provide additional plugins for `babel` invocation for JSX transformation.

### tsPluginOptions

Type: `any`

Default: `undefined`

Defines options for `@babel/plugin-transform-typescript` plugin.

## HMR Detection

This plugin supports HMR of Vue JSX components. The detection requirements are:

- The component must be exported.
- The component must be declared by calling `defineComponent` or the name specified in `defineComponentName` via a root-level statement, either variable declaration or export declaration.

### Supported patterns

```jsx
import { defineComponent } from 'vue'

// named exports w/ variable declaration: ok
export const Foo = defineComponent({})

// named exports referencing variable declaration: ok
const Bar = defineComponent({ render() { return <div>Test</div> }})
export { Bar }

// default export call: ok
export default defineComponent({ render() { return <div>Test</div> }})

// default export referencing variable declaration: ok
const Baz = defineComponent({ render() { return <div>Test</div> }})
export default Baz
```

### Non-supported patterns

```jsx
// not using `defineComponent` call
export const Bar = { ... }

// not exported
const Foo = defineComponent(...)
```
