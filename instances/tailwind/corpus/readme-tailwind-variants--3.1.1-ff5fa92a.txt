# tailwind-variants README 3.0.0 … 3.1.1
# джерело: https://raw.githubusercontent.com/heroui-inc/tailwind-variants/1b67c1a28380b48798bfdfea15832b166155bf68/README.md
# отримано: 2026-09-30
# версія: 3.1.1, 3.1.0, 3.0.0

    tailwind-variants

  The power of Tailwind combined with a first-class variant API.

## Features

- First-class variant API
- Slots support
- Composition support
- Fully typed
- Framework agnostic
- Automatic conflict resolution
- Tailwindcss V4 support

## Documentation

For full documentation, visit tailwind-variants.org

> ❕ Note: `Tailwindcss V4` no longer supports the `config.content.transform` so we remove the `responsive variants` feature
>
> If you want to use `responsive variants`, you need to add it manually to your classname.

## Quick Start

1. Installation:
   To use Tailwind Variants in your project, you can install it as a dependency:

```bash
yarn add tailwind-variants
# or
npm i tailwind-variants
# or
pnpm add tailwind-variants
```

**Optional:** If you want automatic conflict resolution, also install `tailwind-merge`:

```bash
yarn add tailwind-merge
# or
npm i tailwind-merge
# or
pnpm add tailwind-merge
```

> **💡 Lite mode (v3):** For smaller bundle size and faster runtime without conflict resolution, use the `/lite` import:
> ```js
> import {tv} from "tailwind-variants/lite";
> ```

> **⚠️ Upgrading?**
> - From v2 to v3: See the v3 migration guide
> - From v1 to v2: See the v2 migration guide

2. Usage:

```js
import {tv} from "tailwind-variants";

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

return <button className={button({size: "sm", color: "secondary"})}>Click me</button>;
```

## Acknowledgements

- **cva** (Joe Bell)
  This project as started as an extension of Joe's work on `cva` – a great tool for generating variants for a single element with Tailwind CSS. Big shoutout to Joe Bell and contributors you guys rock! 🤘 - we recommend to use `cva` if don't need any of the **Tailwind Variants** features listed here.

- **Stitches** (Modulz)
  The pioneers of the `variants` API movement. Inmense thanks to Modulz for their work on Stitches and the community around it. 🙏

## Community

We're excited to see the community adopt HeroUI, raise issues, and provide feedback. Whether it's a feature request, bug report, or a project to showcase, please get involved!

- Discord
- Twitter
- GitHub Discussions

## Contributing

Contributions are always welcome!

Please follow our contributing guidelines.

Please adhere to this project's CODE_OF_CONDUCT.

## Authors

- Junior garcia (@jrgarciadev)
- Tianen Pang (@tianenpang)

## License

Licensed under the MIT License.

See LICENSE for more information.
