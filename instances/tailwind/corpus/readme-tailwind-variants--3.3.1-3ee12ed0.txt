# tailwind-variants README 3.3.0 … 3.3.1
# джерело: https://raw.githubusercontent.com/heroui-inc/tailwind-variants/v3.3.1/README.md
# отримано: 2026-09-30
# версія: 3.3.1, 3.3.0

    tailwind-variants

  The power of Tailwind combined with a first-class variant API.

## Features

- First-class variant API
- Slots support
- Composition support
- Fully typed
- Framework agnostic
- Built-in conflict resolution
- Tailwind CSS v4 support

## Installation

```bash
npm i tailwind-variants
# or
yarn add tailwind-variants
# or
pnpm add tailwind-variants
```

**Lite mode:** import from `tailwind-variants/lite` for a smaller bundle without conflict resolution.

**Upgrading?**

- v2 → v3: migration guide
- v1 → v2: migration guide

## Quick Start

```js
import { tv } from "tailwind-variants";

const button = tv({
  base: "font-medium bg-blue-500 text-white rounded-full active:opacity-80",
  variants: {
    color: {
      primary: "bg-blue-500 text-white",
      secondary: "bg-purple-500 text-white",
    },
    size: {
      sm: "text-sm",
      md: "text-base",
      lg: "px-4 py-3 text-lg",
    },
  },
  compoundVariants: [
    {
      size: ["sm", "md"],
      class: "px-3 py-1",
    },
  ],
  defaultVariants: {
    size: "md",
    color: "primary",
  },
});

button({ size: "sm", color: "secondary" });
// => "font-medium rounded-full active:opacity-80 bg-purple-500 text-white text-sm px-3 py-1"
```

> **Note:** Tailwind CSS v4 no longer supports `config.content.transform`, so responsive variants
> were removed. Add responsive classes to your class names manually if needed.

## Conflict Resolution

Conflict resolution is built into the default entry — no extra package is required. It is available
on `tv`, `createTV`, `cn`, and `cnMerge` (`cx` and `/lite` do not merge).

```js
import { tv, cn } from "tailwind-variants";

cn("px-2", "px-4"); // => "px-4"

tv({ base: "px-2", variants: { size: { lg: "px-4" } } })({ size: "lg" }); // => "px-4"
```

### Custom configuration

Pass `twMergeConfig` to teach the resolver about custom utilities. Prefer `{ extend, override }` —
`extend` appends to the defaults, `override` replaces them:

```ts
import { cnMerge, createTV, tv, type TWMergeConfig } from "tailwind-variants";

const twMergeConfig = {
  extend: {
    classGroups: {
      elevation: ["elevation-low", "elevation-high"],
    },
  },
} satisfies TWMergeConfig;

tv({ base: "elevation-low", variants: { raised: { true: "elevation-high" } } }, { twMergeConfig });
createTV({ twMergeConfig });
cnMerge("elevation-low", "elevation-high")({ twMergeConfig }); // => "elevation-high"
```

Disable merging with `{ twMerge: false }` on `tv`, `createTV`, or `cnMerge`.

### Reusing a `tailwind-merge` config

If you already configure `extendTailwindMerge`, reuse the same config object as `twMergeConfig`
(pass the object — not the returned merge function):

```ts
import { extendTailwindMerge } from "tailwind-merge";
import { createTV, type TWMergeConfig } from "tailwind-variants";

const mergeConfig = {
  extend: {
    classGroups: {
      elevation: ["elevation-low", "elevation-high"],
    },
  },
} satisfies TWMergeConfig;

extendTailwindMerge(mergeConfig);
createTV({ twMergeConfig: mergeConfig });
```

For `createTailwindMerge`, move the custom parts of the factory into `{ extend, override }` and pass
that object. Merge functions and full default configs cannot be passed directly.

## Utility Functions

| Function  | Behavior                                             |
| --------- | ---------------------------------------------------- |
| `cx`      | Concatenate class names (no merging)                 |
| `cn`      | Concatenate and merge with the default config        |
| `cnMerge` | Concatenate and merge, with optional per-call config |

```js
import { cx, cn, cnMerge } from "tailwind-variants";

cx("px-2", "px-4"); // => "px-2 px-4"
cn("px-2", "px-4"); // => "px-4"
cnMerge("px-2", "px-4")({ twMerge: false }); // => "px-2 px-4"
```

## Documentation

For full documentation, visit tailwind-variants.org.

## Acknowledgements

- **cva** (Joe Bell)
  This project started as an extension of Joe's work on `cva` — a great tool for generating variants
  for a single element with Tailwind CSS. Big shoutout to Joe Bell and
  contributors! If you don't need the
  **Tailwind Variants** features listed
  here, we recommend `cva`.

- **Stitches** (Modulz)
  The pioneers of the `variants` API movement. Immense thanks to Modulz for
  their work on Stitches and the community around it.

- **tailwind-merge**, **clsx**, and **cnfast**
  Conflict resolution draws on ideas and MIT-licensed work from these projects.

## Community

We're excited to see the community adopt HeroUI, raise issues, and provide feedback. Whether it's a
feature request, bug report, or a project to showcase, please get involved!

- Discord
- Twitter
- GitHub Discussions

## Contributing

Contributions are always welcome!

- Contributing guidelines
- Code of conduct
- Security policy

## Authors

- Junior Garcia (@jrgarciadev)
- Tianen Pang (@tianenpang)

## License

Licensed under the MIT License. See LICENSE for more information.
