# tailwind-merge README 3.3.0
# джерело: https://raw.githubusercontent.com/dcastil/tailwind-merge/ceb3b4aea113281e75b39f20e40fd1d16e0727be/README.md
# отримано: 2026-09-30
# версія: 3.3.0

## tailwind-merge

Utility function to efficiently merge Tailwind CSS classes in JS without style conflicts.

```ts
import { twMerge } from 'tailwind-merge'

twMerge('px-2 py-1 bg-red hover:bg-dark-red', 'p-3 bg-[#B91C1C]')
// → 'hover:bg-dark-red p-3 bg-[#B91C1C]'
```

- Supports Tailwind v4.0 up to v4.1 (if you use Tailwind v3, use tailwind-merge v2.6.0)
- Works in all modern browsers and maintained Node versions
- Fully typed
- Check bundle size on Bundlephobia

## Get started

- What is it for
- When and how to use it
- Features
- Limitations
- Configuration
- Recipes
- API reference
- Writing plugins
- Versioning
- Contributing
- Similar packages
