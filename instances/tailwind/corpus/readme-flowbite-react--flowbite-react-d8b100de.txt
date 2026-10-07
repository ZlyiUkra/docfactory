# flowbite-react README 0.7.3 … 0.7.5
# джерело: https://raw.githubusercontent.com/themesberg/flowbite-react/7f9ef9f44e6ff60c6ea4daa302d0d174f143a4ad/README.md
# отримано: 2026-09-30
# версія: 0.7.5, 0.7.4, 0.7.3

  :construction: flowbite-react (unreleased) :construction:

    Build websites even faster with components on top of React and Tailwind CSS

---

---

### `flowbite-react` is an open source collection of UI components, built in React, with utility classes from Tailwind CSS that you can use as a starting point for user interfaces and websites.

## Table of Contents

- Table of Contents
- Documentation
- Getting started
  - Setup Tailwind CSS
  - Install Flowbite React
  - Try it out
  - Next steps
    - Next.js
    - Dark mode
    - Customization
    - Contributing
- Components
- Community
- Contributing
- Figma
- Copyright and license

## Documentation

Documentation for `flowbite-react` is not yet finished.

If you want to browse the components, visit flowbite-react.com.

If you want to learn more about Flowbite, visit Flowbite docs.

## Getting started

Learn how to get started with Flowbite React and start leveraging the interactive React components coupled with Flowbite and Tailwind CSS.

You'll need to be familiar with Node.js and `npm`, and have `npm` installed. You should be comfortable installing packages with `npm`, and experience creating web apps with React and Tailwind CSS will be very helpful.

### Setup Tailwind CSS

Install Tailwind CSS:

```bash
npm i autoprefixer postcss tailwindcss
npx tailwindcss init -p
```

Point Tailwind CSS to files you have `className=".."` in:

```javascript
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}' /* src folder, for example */],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

Add Tailwind CSS to a CSS file:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Install Flowbite React

1. Run the following command to install `flowbite-react`:

```bash
npm i flowbite-react
```

2. Add the Flowbite plugin to `tailwind.config.js`, and include content from `flowbite-react`:

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    // ...
    'node_modules/flowbite-react/lib/esm/**/*.js',
  ],
  plugins: [
    // ...
    require('flowbite/plugin'),
  ],
};
```

### Try it out

How you use Flowbite React depends on your project setup. In general, you can just import the components you want to use from `flowbite-react` and use them in a React `.jsx` file:

```tsx
import { Button } from 'flowbite-react';

export default function MyPage() {
  return (
    <div>
      <Button>Click me</Button>
    </div>
  );
}
```

### Next steps

#### Next.js

If you're using Next.js, you can follow the Next.js install guide, which includes a Next.js starter project with Flowbite React already set up.

#### Dark mode

If you want to add a dark mode switcher to your app, you can follow the dark mode guide.

#### Customization

If you want to customize Flowbite React component, you can follow the theme guide.

#### Contributing

If you want to contribute to Flowbite React, you can follow the contributing guide.

## Components

**Please note that some components in the vanilla Flowbite library are not yet available in Flowbite React.**

    Accordion
    Alert
    Avatar

    Banner
    Badge
    Breadcrumb

    Button
    Button group
    Card

    Carousel
    Datepicker
    Dropdown

    Footer
    Forms
    List group

    Modal
    Navbar
    Pagination

    Progress bar
    Rating
    Sidebar

    Spinner
    Table
    Tabs

    Tooltip
    Timeline
    Toast

    Sticky Banner

## Community

If you need help or just want to discuss about the library join the community on Github:

⌨️ Discuss about Flowbite on GitHub

For casual chatting with others using the library:

💬 Join the Flowbite Discord Server

## Contributing

Thank you for your interest in helping! Visit our guide on contributing to get started.

## Figma

If you need the Figma files for the components you can check out our website for more information:

🎨 Get access to the Figma design files

## Copyright and license

The Flowbite name and logos are trademarks of Bergside Srl.

📝 Read about the licensing terms
📀 Brand guideline and trademark usage agreement
