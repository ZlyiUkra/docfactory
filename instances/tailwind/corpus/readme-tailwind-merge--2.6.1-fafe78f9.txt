# tailwind-merge README 2.6.1
# джерело: https://raw.githubusercontent.com/dcastil/tailwind-merge/03778635bfd7c73f0181e9aefbc5b01a0f804961/README.md
# отримано: 2026-09-30
# версія: 2.6.1

## tailwind-merge

Utility function to efficiently merge Tailwind CSS classes in JS without style conflicts.

```ts
import { twMerge } from 'tailwind-merge'

twMerge('px-2 py-1 bg-red hover:bg-dark-red', 'p-3 bg-[#B91C1C]')
// → 'hover:bg-dark-red p-3 bg-[#B91C1C]'
```

-   Supports Tailwind v3.0 up to v3.4 (if you use Tailwind v2, use tailwind-merge v0.9.0)
-   Works in all modern browsers and maintained Node versions
-   Fully typed
-   Check bundle size on Bundlephobia

## Get started

-   What is it for
-   When and how to use it
-   Features
-   Limitations
-   Configuration
-   Recipes
-   API reference
-   Writing plugins
-   Versioning
-   Contributing
-   Similar packages
