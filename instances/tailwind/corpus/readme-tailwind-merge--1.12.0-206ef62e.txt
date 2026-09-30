# tailwind-merge README 1.12.0
# джерело: https://raw.githubusercontent.com/dcastil/tailwind-merge/2fd82afaa3e9704236a3c7cd0e985511b16b0ef2/README.md
# отримано: 2026-09-30
# версія: 1.12.0

## tailwind-merge

Utility function to efficiently merge Tailwind CSS classes in JS without style conflicts.

```ts
import { twMerge } from 'tailwind-merge'

twMerge('px-2 py-1 bg-red hover:bg-dark-red', 'p-3 bg-[#B91C1C]')
// → 'hover:bg-dark-red p-3 bg-[#B91C1C]'
```

-   Supports Tailwind v3.0 up to v3.3 (if you use Tailwind v2, use tailwind-merge v0.9.0)
-   Works in all modern browsers and Node >=12
-   Fully typed
-   Check bundle size on Bundlephobia

## Get started

-   What is it for
-   Features
-   Configuration
-   Recipes
-   API reference
-   Writing plugins
-   Versioning
-   Contributing
-   Similar packages
