# class-variance-authority README 0.0.1
# джерело: https://raw.githubusercontent.com/joe-bell/cva/def9f182998c49dafa92ddf8c595e69de14b7d03/README.md
# отримано: 2026-09-30
# версія: 0.0.1

CVA

cva

    Class Variance Authority

## Introduction

CSS-in-TS libraries such as Stitches and Vanilla Extract are **fantastic** options for building type-safe UI components; taking away all the worries of class names and StyleSheet composition.

…but CSS-in-TS (or CSS-in-JS) isn't for everyone.

You may need full control over your StyleSheet output. Your job might require you to use a framework such as Tailwind CSS. You might just prefer writing your own CSS.

Creating variants with the "traditional" CSS approach can become an arduous task; manually matching classes to props and manually adding types.

CVA aims to take those pain points away, allowing you to focus on the more fun aspects of UI development.

## Acknowledgements

- **Stitches** (Modulz)
  Huge thanks to the Modulz team for pioneering the `variants` API movement – your open-source contributions are immensely appreciated
- **clb** (Bill Criswell)
  This project originally started out with the intention of merging into the wonderful `clb` library, but after some discussion with Bill, we felt it was best to go down the route of a separate project.
  I'm so grateful to Bill for sharing his work publicly and for getting me excited about building a type-safe variants API for classes. If you have a moment, please go and star the project on GitHub. Thank you Bill!

## Installation

```sh
npm i class-variance-authority
```

"Do I really have to write such a long package name for every import?"

Unfortunately, yes. Originally, the plan was the publish the package as `cva`, but this name has been taken and marked as a "placeholder". I've reached out to the author and NPM support, but have yet to hear back.

In the meantime, you can always alias the package for your convenience…

### Aliasing in TypeScript

1. Add the alias to your `tsconfig.json` `paths`:

```json
   {
     "compilerOptions": {
       "baseUrl": ".",
       "paths": {
         "cva": ["node_modules/class-variance-authority"]
       }
     }
   }
```

2. Then import like so:

```ts
   import { cva } from "cva";

   // …
```

## Getting Started

> **Disclaimer**: Although `cva` is a **tiny** library, it's best to use in a SSR/SSG environment – your user probably doesn't need this JavaScript, especially for static components.

### Your First Component

To kick things off, let's build a "basic" `button` component, using `cva` to handle our variant's classes

> **Note:** Use of Tailwind CSS is optional

```ts
import { cva } from "class-variance-authority";

const button = cva(["font-semibold", "border", "rounded"], {
  variants: {
    intent: {
      primary: [
        "bg-blue-500",
        "text-white",
        "border-transparent",
        "hover:bg-blue-600",
      ],
      // **or**
      // primary: "bg-blue-500 text-white border-transparent hover:bg-blue-600",
      secondary: [
        "bg-white",
        "text-gray-800",
        "border-gray-400",
        "hover:bg-gray-100",
      ],
    },
    size: {
      small: ["text-sm", "py-1", "px-2"],
      medium: ["text-base", "py-2", "px-4"],
    },
  },
  compoundVariants: [{ intent: "primary", size: "medium", class: "uppercase" }],
  defaultVariants: {
    intent: "primary",
    size: "medium",
  },
});

button();
// => "font-semibold border rounded bg-blue-500 text-white border-transparent hover:bg-blue-600 text-base py-2 px-4 uppercase"

button({ intent: "secondary", size: "small" });
// => "font-semibold border rounded bg-white text-gray-800 border-gray-400 hover:bg-gray-100 text-sm py-1 px-2"
```

### TypeScript Helpers

`cva` offers the `VariantProps` helper to extract variant types

```ts
// styles/components.ts
import type * as CVA from "class-variance-authority";
import { cva, cx } from "class-variance-authority";

/**
 * YourComponent
 */
export type YourComponentProps = CVA.VariantProps<typeof yourComponent>;
export const yourComponent = cva(/* ... */);
```

### Composing Classes

Whilst `cva` doesn't yet offer a built-in method for composing classes, it does offer the tools to extend components on your own terms…

For example; two `cva` styles, concatenated together with `cx`:

```ts
// styles/components.ts
import type * as CVA from "class-variance-authority";
import { cva, cx } from "class-variance-authority";

/**
 * Box
 */
export type BoxProps = CVA.VariantProps<typeof box>;
export const box = cva(["box", "box-border"], {
  variants: {
    margin: { 0: "m-0", 2: "m-2", 4: "m-4", 8: "m-8" },
    padding: { 0: "p-0", 2: "p-2", 4: "p-4", 8: "p-8" },
  },
  defaultVariants: {
    margin: 0,
    padding: 0,
  },
});

/**
 * Card
 */
type CardBaseProps = CVA.VariantProps<typeof cardBase>;
const cardBase = cva(["card", "border-solid", "border-slate-300", "rounded"], {
  variants: {
    shadow: {
      md: "drop-shadow-md",
      lg: "drop-shadow-lg",
      xl: "drop-shadow-xl",
    },
  },
});

export interface CardProps extends BoxProps, CardBaseProps {}
export const card = ({ margin, padding, shadow }: CardProps = {}) =>
  cx(box({ margin, padding }), cardBase({ shadow }));
```

## API Reference

### `cva`

Builds a class variance authority

```ts
const component = cva("base", options);
```

1. `base`: the base class name (`string`, `string[]` or `null`)
1. `options` _(optional)_
   - `variants`: your variants schema
   - `compoundVariants`: variants based on a combination of previously defined variants
   - `defaultVariants`: set default values for previously defined variants

### `cx`

Concatenates class names

```ts
const className = cx(classes);
```

- `classes`: array of classes to be concatenated

## Examples

> ⚠️ Warning: The examples below are purely demonstrative and haven't been tested thoroughly (yet)

  BEM

```css
/* styles.css */
.button {
  /* */
}

.button--primary {
  /* */
}
.button--secondary {
  /* */
}

.button--small {
  /* */
}
.button--medium {
  /* */
}

.button--primary-small {
  /* */
}
```

```ts
import { cva } from "class-variance-authority";

const button = cva("button", {
  variants: {
    intent: {
      primary: "button--primary",
      secondary: "button--secondary",
    },
    size: {
      small: "button--small",
      medium: "button--medium",
    },
  },
  compoundVariants: [
    { intent: "primary", size: "medium", class: "button--primary-small" },
  ],
  defaultVariants: {
    intent: "primary",
    size: "medium",
  },
});

button();
// => "button button--primary button--medium"

button({ intent: "secondary", size: "small" });
// => "button button--secondary button--small"
```

    11ty (with Tailwind)

```js
// button.11ty.js
const { cva } = require("class-variance-authority");

// ⚠️ Disclaimer: Use of Tailwind CSS is optional
const button = cva("button", {
  variants: {
    intent: {
      primary: [
        "bg-blue-500",
        "text-white",
        "border-transparent",
        "hover:bg-blue-600",
      ],
      secondary: [
        "bg-white",
        "text-gray-800",
        "border-gray-400",
        "hover:bg-gray-100",
      ],
    },
    size: {
      small: ["text-sm", "py-1", "px-2"],
      medium: ["text-base", "py-2", "px-4"],
    },
  },
  compoundVariants: [{ intent: "primary", size: "medium", class: "uppercase" }],
  defaultVariants: {
    intent: "primary",
    size: "medium",
  },
});

module.exports = function ({ label, intent, size }) {
  return `<button class="${button({ intent, size })}">${label}</button>`;
};
```

    React (with CSS Modules)

```css
/* button.css */
.base {
  /* */
}

.primary {
  /* */
}
.secondary {
  /* */
}

.small {
  /* */
}
.medium {
  /* */
}

.primaryMedium {
  /* */
}
```

```tsx
// button.tsx
import React from "react";
import { cva } from "class-variance-authority";
import * as CVA from "class-variance-authority";

import {
  base,
  primary,
  secondary,
  small,
  medium,
  primaryMedium,
} from "./button.css";

// ⚠️ Disclaimer: Use of Tailwind CSS is optional
const button = cva(base, {
  variants: {
    intent: {
      primary,
      secondary,
    },
    size: {
      small,
      medium,
    },
  },
  compoundVariants: [
    { intent: "primary", size: "medium", class: primaryMedium },
  ],
  defaultVariants: {
    intent: "primary",
    size: "medium",
  },
});

export type ButtonProps = CVA.VariantProps<typeof button>;

export const Button: React.FC<ButtonProps> = ({ intent, size, ...props }) => (
  <button className={button({ intent, size })} {...props} />
);
```

    React (with Tailwind)

```tsx
// button.tsx
import React from "react";
import { cva } from "class-variance-authority";
import * as CVA from "class-variance-authority";

// ⚠️ Disclaimer: Use of Tailwind CSS is optional
const button = cva("button", {
  variants: {
    intent: {
      primary: [
        "bg-blue-500",
        "text-white",
        "border-transparent",
        "hover:bg-blue-600",
      ],
      secondary: [
        "bg-white",
        "text-gray-800",
        "border-gray-400",
        "hover:bg-gray-100",
      ],
    },
    size: {
      small: ["text-sm", "py-1", "px-2"],
      medium: ["text-base", "py-2", "px-4"],
    },
  },
  compoundVariants: [{ intent: "primary", size: "medium", class: "uppercase" }],
  defaultVariants: {
    intent: "primary",
    size: "medium",
  },
});

export type ButtonProps = CVA.VariantProps<typeof button>;

export const Button: React.FC<ButtonProps> = ({ intent, size, ...props }) => (
  <button className={button({ intent, size })} {...props} />
);
```

    Svelte

```svelte
<!-- button.svelte -->
<script lang="ts">
  import { cva } from "class-variance-authority";
  import type * as CVA from "class-variance-authority";

  const button = cva("button", {
    variants: {
      intent: {
        primary: "button--primary",
        secondary: "button--secondary",
      },
      size: {
        small: "button--small",
        medium: "button--medium",
      },
    },
    compoundVariants: [
      { intent: "primary", size: "medium", class: "button--primary-medium" },
    ],
    defaultVariants: {
      intent: "primary",
      size: "medium",
    },
  });

  type ButtonProps = CVA.VariantProps<typeof button>;

  export let intent: ButtonProps["intent"];
  export let size: ButtonProps["size"];
</script>

<button class={button({ intent, size })}><slot /></button>

<style>
  .button { /* … */ }

  .button--primary { /* … */ }
  .button--secondary { /* … */ }

  .button--small { /* … */ }
  .button--medium { /* … */ }

  .button--primary-medium { /* … */ }
</style>
```

    Vue 3

```vue
<!-- button.vue -->
<script lang="ts">
import { defineComponent } from "vue";

import { cva } from "class-variance-authority";
import type * as CVA from "class-variance-authority";

const button = cva("button", {
  variants: {
    intent: {
      primary: "button--primary",
      secondary: "button--secondary",
    },
    size: {
      small: "button--small",
      medium: "button--medium",
    },
  },
  compoundVariants: [
    { intent: "primary", size: "medium", class: "button--primary-medium" },
  ],
  defaultVariants: {
    intent: "primary",
    size: "medium",
  },
});

type ButtonProps = CVA.VariantProps<typeof button>;

export default defineComponent({
  props: ["intent" as ButtonProps["intent"], "size" as ButtonProps["size"]],
  methods: {
    button,
  },
});
</script>

<template>
  <button :class="button({ intent, size })">
    <slot></slot>
  </button>
</template>

<style>
.button {
  /* … */
}

.button--primary {
  /* … */
}
.button--secondary {
  /* … */
}

.button--small {
  /* … */
}
.button--medium {
  /* … */
}

.button--primary-medium {
  /* … */
}
</style>
```

### Other Use Cases

Although primarily designed for handling class names, at its core, `cva` is really just a fancy way of managing a string…

  Dynamic Text Content

```ts
const greeter = cva("Good morning!", {
  variants: {
    isLoggedIn: {
      true: "Here's a secret only logged in users can see",
      false: "Log in to find out more…",
    },
  },
  defaultVariants: {
    isLoggedIn: "false",
  },
});

greeter();
// => "Good morning! Log in to find out more…"

greeter({ isLoggedIn: "true" });
// => "Good morning! Here's a secret only logged in users can see"
```
