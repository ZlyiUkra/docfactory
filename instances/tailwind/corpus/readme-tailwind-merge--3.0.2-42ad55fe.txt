# tailwind-merge README 3.0.2
# джерело: https://raw.githubusercontent.com/dcastil/tailwind-merge/b5423b8174eea318d36577080388945b4b74999a/README.md
# отримано: 2026-09-30
# версія: 3.0.2

## tailwind-merge

Utility function to efficiently merge Tailwind CSS classes in JS without style conflicts.

```ts
import { twMerge } from 'tailwind-merge'

twMerge('px-2 py-1 bg-red hover:bg-dark-red', 'p-3 bg-[#B91C1C]')
// → 'hover:bg-dark-red p-3 bg-[#B91C1C]'
```

- Supports Tailwind v4.0 (if you use Tailwind v3, use tailwind-merge v2.6.0)
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
