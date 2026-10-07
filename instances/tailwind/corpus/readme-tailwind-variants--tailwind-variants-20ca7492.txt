# tailwind-variants README 0.2.1
# джерело: https://raw.githubusercontent.com/heroui-inc/tailwind-variants/9d7abb0a026e3e49c2e950102211e8d6e1a9948e/README.md
# отримано: 2026-09-30
# версія: 0.2.1

    tailwind-variants

  The power of Tailwind combined with a first-class variant API.

## Features

- First-class variant API
- Responsive variants
- Slots support
- Composition support
- Fully typed
- Framework agnostic
- Automatic conflict resolution

## Documentation

For full documentation, visit tailwind-variants.org

## Quick Start

1. Installation:
To use Tailwind Variants in your project, you can install it as a dependency:

```bash
yarn add tailwind-variants
# or
npm i tailwind-variants
```

2. Usage:

```js
import { tv } from 'tailwind-variants';

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
  }
});

return (
  <button className={button({ size: 'sm', color: 'secondary' })}>Click me</button>
)
```

3. Responsive variants configuration (optional): If you want to use responsive variants
you need to add the Tailwind Variants `wrapper` to your TailwindCSS config file `tailwind.config.js`.

```js
// tailwind.config.js

const { withTV } = require('tailwind-variants/transformer')

/** @type {import('tailwindcss').Config} */
module.exports = withTV({
  content:  ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
})
```

If you're using a custom path to import Tailwind variants, such as creating a custom tv instance with `createTV`, it's recommended to include this path in the transformer configuration:

```js
// tailwind.config.js

const { withTV } = require('tailwind-variants/transformer')

/** @type {import('tailwindcss').Config} */
module.exports = withTV({
  content:  ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}, {
  aliases: ["@/lib/tv"]
})
```

## Acknowledgements

- **cva** (Joe Bell)
  This project as started as an extension of Joe's work on `cva` – a great tool for generating variants for a single element with Tailwind CSS. Big shoutout to Joe Bell and contributors you guys rock! 🤘 - we recommend to use `cva` if don't need any of the **Tailwind Variants** features listed here.

- **Stitches** (Modulz)
  The pioneers of the `variants` API movement. Inmense thanks to Modulz for their work on Stitches and the community around it. 🙏

## Community

We're excited to see the community adopt NextUI, raise issues, and provide feedback. Whether it's a feature request, bug report, or a project to showcase, please get involved!

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
