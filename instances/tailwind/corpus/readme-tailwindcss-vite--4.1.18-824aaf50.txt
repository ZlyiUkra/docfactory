# @tailwindcss/vite README 4.1.15 … 4.1.18
# джерело: https://raw.githubusercontent.com/tailwindlabs/tailwindcss/v4.1.18/packages/@tailwindcss-vite/README.md
# отримано: 2026-09-30
# версія: 4.1.18, 4.1.17, 4.1.16, 4.1.15

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

## `@tailwindcss/vite` plugin API

### Enabling or disabling Lightning CSS

By default, this plugin detects whether or not the CSS is being built for production by checking the `NODE_ENV` environment variable. When building for production Lightning CSS will be enabled otherwise it is disabled.

If you want to always enable or disable Lightning CSS the `optimize` option may be used:

```js
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    tailwindcss({
      // Disable Lightning CSS optimization
      optimize: false,
    }),
  ],
})
```

It's also possible to keep Lightning CSS enabled but disable minification:

```js
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    tailwindcss({
      // Enable Lightning CSS but disable minification
      optimize: { minify: false },
    }),
  ],
})
```
