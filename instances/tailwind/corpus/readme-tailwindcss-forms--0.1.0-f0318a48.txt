# @tailwindcss/forms README 0.1.0: @tailwindcss/forms
# джерело: https://raw.githubusercontent.com/tailwindlabs/tailwindcss-forms/9ac4ac3c94a5a45b1eea84efbc7ffd17af30593e/README.md
# отримано: 2026-09-30
# версія: 0.1.0

A plugin that provides basic default form styles that are easy to override with utilities. Hopefully the successor to `@tailwindcss/custom-forms`.

## Installation

Install the plugin from npm:

```sh
# Using npm
npm install @tailwindcss/forms

# Using Yarn
yarn add @tailwindcss/forms
```

Then add the plugin to your `tailwind.config.js` file:

```js
// tailwind.config.js
module.exports = {
  theme: {
    // ...
  },
  plugins: [
    require('@tailwindcss/forms'),
    // ...
  ],
}
```

## Usage

All of the basic form elements you use will now have some sensible default styles that are easy to override with utilities. Works basically like the `@tailwindcss/custom-forms` plugin in terms of how you modify things using utility classes. More details eventually.
