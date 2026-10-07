# tailwind-merge README 1.6.0
# джерело: https://raw.githubusercontent.com/dcastil/tailwind-merge/b32c973d9808f5d22fb8580ed008d81786627c78/README.md
# отримано: 2026-09-30
# версія: 1.6.0

## tailwind-merge

Utility function to efficiently merge Tailwind CSS classes in JS without style conflicts.

```ts
import { twMerge } from 'tailwind-merge'

twMerge('px-2 py-1 bg-red hover:bg-dark-red', 'p-3 bg-[#B91C1C]')
// → 'hover:bg-dark-red p-3 bg-[#B91C1C]'
```

-   Supports Tailwind v3.0 up to v3.1 (if you use Tailwind v2, use tailwind-merge v0.9.0)
-   Works in Node >=12 and all modern browsers
-   Fully typed
-   Check bundle size on Bundlephobia

## Get started

-   What is it for
-   Features
-   Configuring tailwind-merge
-   Recipes
-   API reference
-   Writing plugins
-   Versioning
-   Contributing
-   Similar packages
