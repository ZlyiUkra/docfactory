# @tailwindcss/vite README 4.2.0 … 4.3.3
# джерело: https://raw.githubusercontent.com/tailwindlabs/tailwindcss/v4.3.3/packages/@tailwindcss-vite/README.md
# отримано: 2026-09-30
# версія: 4.3.3, 4.3.2, 4.3.1, 4.3.0, 4.2.4, 4.2.3, 4.2.2, 4.2.1, 4.2.0

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
