# tailwind-merge README 1.9.0
# джерело: https://raw.githubusercontent.com/dcastil/tailwind-merge/170e2ceefcffe3181e2bd30dfb74d41a5a0f353e/README.md
# отримано: 2026-09-30
# версія: 1.9.0

## tailwind-merge

Utility function to efficiently merge Tailwind CSS classes in JS without style conflicts.

```ts
import { twMerge } from 'tailwind-merge'

twMerge('px-2 py-1 bg-red hover:bg-dark-red', 'p-3 bg-[#B91C1C]')
// → 'hover:bg-dark-red p-3 bg-[#B91C1C]'
```

-   Supports Tailwind v3.0 up to v3.2 (if you use Tailwind v2, use tailwind-merge v0.9.0)
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
