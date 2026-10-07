# prettier-plugin-tailwindcss README 0.1.1: prettier-plugin-tailwindcss
# джерело: https://raw.githubusercontent.com/tailwindlabs/prettier-plugin-tailwindcss/4a4d036554601bb853b792f89c78700006edbfd2/README.md
# отримано: 2026-09-30
# версія: 0.1.1

A Prettier plugin for Tailwind CSS that automatically sorts classes based on Tailwind's internal class sorting algorithm.

> Note, this plugin is only compatible with Tailwind CSS v3.

## Installation

Install `prettier-plugin-tailwindcss` via npm as a dev-dependency.

```sh
npm install --save-dev prettier prettier-plugin-tailwindcss
```

This plugin follows the Prettier autoloading convention, so once it's installed it should automatically start working.

## Resolving your Tailwind configuration

By default this plugin will look for a Tailwind configuration file (`tailwind.config.js`) in the same directory as your Prettier configuration file.

If your Tailwind configuration file is somewhere else, you can specify this using the `tailwindConfig` option in your Prettier configuration. Note that paths are resolved relative to the Prettier configuration file.

```js
// prettier.config.js
module.exports = {
  tailwindConfig: './styles/tailwind.config.js',
}
```

If a Tailwind configuration file cannot be found then the default Tailwind configuration will be used.

## Compatibility with other Prettier plugins

To make this plugin work, we had to build it in a way that the Prettier plugin system was not designed for. We had to extend the core parsers in Prettier with our own custom parsers. And while this works, it makes this plugin incompatible with other Prettier plugins that are build the same way. This is a known limitation of Prettier.

One example of this incompatibility is with the prettier-plugin-svelte plugin. It's not possible to use the Svelte plugin at the same time as the Tailwind CSS plugin. However, as a workaround, we bundled the Svelte plugin into this plugin. Simply remove `prettier-plugin-svelte` from your Svelte project when installing the `prettier-plugin-tailwindcss` plugin, and everything should work fine.
