# prettier-plugin-tailwindcss README 0.1.0: prettier-plugin-tailwindcss
# джерело: https://raw.githubusercontent.com/tailwindlabs/prettier-plugin-tailwindcss/288f92c2eedee2ba0ca85bce641637339ebf621a/README.md
# отримано: 2026-09-30
# версія: 0.1.0

A Prettier plugin for Tailwind CSS that automatically sorts classes based on Tailwind's internal class sorting algorithm.

## Installation

> Note that `prettier-plugin-tailwindcss` is only compatible with Tailwind CSS v3

```sh
npm install --save-dev prettier prettier-plugin-tailwindcss
```

By default the plugin will look for a Tailwind config file (`tailwind.config.js`) in the same directory as your Prettier config file. If your Tailwind config file is somewhere else you can specify this using the `tailwindConfig` option (paths are resolved relative to the Prettier config file):

```js
// prettier.config.js
module.exports = {
  tailwindConfig: './styles/tailwind.config.js',
}
```

_If a Tailwind config file cannot be found then the default Tailwind configuration will be used._
