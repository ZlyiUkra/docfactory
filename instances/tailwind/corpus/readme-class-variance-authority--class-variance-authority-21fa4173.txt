# class-variance-authority README 0.0.0
# джерело: https://raw.githubusercontent.com/joe-bell/cva/3707b816c0bac8a9421e5961181152b9bee4bf58/README.md
# отримано: 2026-09-30
# версія: 0.0.0

cva

    Class Variance Authority 🧬

## Introduction

Coming from BEM…

```ts
import { cva } from "@joebell/cva";

const button = cva("button", {
  variants: {
    intent: {
      primary: "button--primary",
      secondary: "button--secondary",
      warning: "button--warning",
      danger: "button--danger",
    },
    size: {
      small: "button--small",
      medium: "button--medium",
      large: "button--large",
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

Tailwind

```ts
import { cva } from "@joebell/cva";

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
      warning: [
        "bg-yellow-500",
        "text-black",
        "border-transparent",
        "hover:bg-yellow-600",
      ],
      danger: [
        "bg-red-500",
        "text-white",
        "border-transparent",
        "hover:bg-red-600",
      ],
    },
    size: {
      small: ["text-sm", "py-1", "px-2"],
      medium: ["text-base", "py-2", "px-4"],
      large: ["text-lg", "py-2.5", "px-4"],
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

### Problem?

### Prior Art

- clb
- Stitches
- Vanilla Extract

## Installation

```sh
npm i @joebell/cva
```

## Getting Started

### Composing Classes

Whilst `cva` doesn't yet offer a built-in method for composing classes, it does offer the tools to extend components on your own terms…

For example; two `cva` styles, concatenated together with `cx`:

```ts
// styles/components.ts
import type * as CVA from "cva";
import { cva, cx } from "@joebell/cva";

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

- `cva` – build a class variance authority
- `cx` – concatenate class names

### `cva`

```ts
const component = cva("base", options);
```

#### Parameters

1. `base` – the base class name
1. `options` _(optional)_
   1. `variants`
   1. `compoundVariants`
   1. `defaultVariants`

### `cx`

## Examples

    React (with Tailwind)

```tsx
// button.tsx
import React from "react";
import { cva } from "@joebell/cva";
import * as CVA from "@joebell/cva";

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

> ⚠️ Warning: The examples below are purely demonstrative and haven't been tested thoroughly (yet)

    11ty (with Tailwind)

```js
// button.11ty.js
const { cva } = require("@joebell/cva");

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

    Svelte

```svelte
<!-- button.svelte -->
<script lang="ts">
  import { cva } from "@joebell/cva";
  import type * as CVA from "@joebell/cva";

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

import { cva } from "@joebell/cva";
import type * as CVA from "@joebell/cva";

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
