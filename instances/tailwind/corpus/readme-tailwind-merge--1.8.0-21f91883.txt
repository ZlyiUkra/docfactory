# tailwind-merge README 1.8.0
# джерело: https://raw.githubusercontent.com/dcastil/tailwind-merge/d1a7f273123ad2fcd8dea67f70a15d4986dd2a64/README.md
# отримано: 2026-09-30
# версія: 1.8.0

## tailwind-merge

Utility function to efficiently merge Tailwind CSS classes in JS without style conflicts.

```ts
import { twMerge } from 'tailwind-merge'

twMerge('px-2 py-1 bg-red hover:bg-dark-red', 'p-3 bg-[#B91C1C]')
// → 'hover:bg-dark-red p-3 bg-[#B91C1C]'
```

-   Supports Tailwind v3.0 up to v3.2 (if you use Tailwind v2, use tailwind-merge v0.9.0)
-   Works in Node >=12 and all modern browsers
-   Fully typed
-   Check bundle size on Bundlephobia

## Get started

-   What is it for
-   Features
-   Configruation
-   Recipes
-   API reference
-   Writing plugins
-   Versioning
-   Contributing
-   Similar packages
