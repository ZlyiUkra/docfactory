# @tailwindcss/postcss README 4.2.3
# джерело: https://raw.githubusercontent.com/tailwindlabs/tailwindcss/v4.2.3/packages/@tailwindcss-postcss/README.md
# отримано: 2026-09-30
# версія: 4.2.3

  A utility-first CSS framework for rapidly building custom user interfaces.

---

## Documentation

For full documentation, visit tailwindcss.com.

## Community

For help, discussion about best practices, or feature ideas:

Discuss Tailwind CSS on GitHub

## Contributing

If you're interested in contributing to Tailwind CSS, please read our contributing docs **before submitting a pull request**.

---

## `@tailwindcss/postcss` plugin API

### Changing where the plugin searches for source files

You can use the `base` option (defaults to the current working directory) to change the directory in which the plugin searches for source files:

```js
import tailwindcss from '@tailwindcss/postcss'

export default {
  plugins: [
    tailwindcss({
      base: path.resolve(__dirname, './path'),
    }),
  ],
}
```

### Enabling or disabling Lightning CSS

By default, this plugin detects whether or not the CSS is being built for production by checking the `NODE_ENV` environment variable. When building for production Lightning CSS will be enabled otherwise it is disabled.

If you want to always enable or disable Lightning CSS the `optimize` option may be used:

```js
import tailwindcss from '@tailwindcss/postcss'

export default {
  plugins: [
    tailwindcss({
      // Enable or disable Lightning CSS
      optimize: false,
    }),
  ],
}
```

It's also possible to keep Lightning CSS enabled but disable minification:

```js
import tailwindcss from '@tailwindcss/postcss'

export default {
  plugins: [
    tailwindcss({
      optimize: { minify: false },
    }),
  ],
}
```

### Enabling or disabling `url(…)` rewriting

Our PostCSS plugin can rewrite `url(…)`s for you since it also handles `@import` (no `postcss-import` is needed). This feature is enabled by default.

In some situations the bundler or framework you're using may provide this feature itself. In this case you can set `transformAssetUrls` to `false` to disable this feature:

```js
import tailwindcss from '@tailwindcss/postcss'

export default {
  plugins: [
    tailwindcss({
      // Disable `url(…)` rewriting
      transformAssetUrls: false,

      // Enable `url(…)` rewriting (the default)
      transformAssetUrls: true,
    }),
  ],
}
```
