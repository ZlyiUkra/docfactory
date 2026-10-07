# flowbite-react README 0.4.1 … 0.4.4
# джерело: https://raw.githubusercontent.com/themesberg/flowbite-react/57cf6e84abe88f67947725c15e26fe3f36204f71/README.md
# отримано: 2026-09-30
# версія: 0.4.4, 0.4.3, 0.4.2, 0.4.1

  :construction: flowbite-react (unreleased) :construction:

    Build websites even faster with components on top of React and Tailwind CSS

---

Screenshot of flowbite-react.com

---

### `flowbite-react` is an open source collection of UI components, built in React, with utility classes from Tailwind CSS that you can use as a starting point for user interfaces and websites.

## Table of Contents

- Table of Contents
- Documentation
- Getting started
- Customize components
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

Make sure you have Node.js installed.

To use `flowbite-react`, you need to setup `flowbite` and also install `flowbite-react` from `npm` or `yarn`.

`flowbite` can be included as a plugin into an existing Tailwind CSS project.

1. Install `flowbite` as a dependency using `npm` by running the following command:

```bash
npm i flowbite flowbite-react # or yarn add flowbite flowbite-react
```

2. Require `flowbite` as a plugin inside the `tailwind.config.js` file, and include content from `flowbite-react`:

```javascript
module.exports = {
  content: [
    ...,
    'node_modules/flowbite-react/**/*.{js,jsx,ts,tsx}'
  ],
  plugins: [..., require('flowbite/plugin')],
  ...
};
```

## Customize components

You can customize every component in `flowbite-react`. We've provided a few different methods so just about any use case you have should be covered for now.

See https://flowbite-react.com/theme

## Components

    Alerts
    Badge
    Breadcrumbs

    Buttons
    Button group
    Cards

    Dropdown
    Forms
    List group

    :construction: Typography
    Modal
    Tabs

    Navbar
    Pagination
    Timeline

    Progress bar
    Tables
    Toast

    Tooltips
    :construction: Datepicker
    Spinner

    Footer
    Accordion
    Sidebar

    Carousel
    Avatar
    Rating

    Input Field
    File Input
    :construction: Search Input

    Select
    Textarea
    Checkbox

    Radio
    Toggle
    Range Slider

    :construction: Floating Label

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

The Flowbite name and logos are trademarks of Crafty Dwarf Inc.

📝 Read about the licensing terms
📀 Brand guideline and trademark usage agreement
