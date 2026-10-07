# flowbite-vue README 0.1.1 … 0.1.2
# джерело: https://raw.githubusercontent.com/themesberg/flowbite-vue/77d73abe340df85423adb729344b41287ff651c6/README.md
# отримано: 2026-09-30
# версія: 0.1.2, 0.1.1

  flowbite-vue

    Build websites even faster with components on top of Vue and Tailwind CSS

---

### `flowbite-vue` is an open source collection of UI components, built in Vue, with utility classes from Tailwind CSS that you can use as a starting point for user interfaces and websites.

## Table of Contents

- Documentation
- Getting started
    - Require via `npm`
    - Include via CDN
- Components
- Community
- Contributing
- Figma
- Copyright and license

## Documentation

Documentation for `flowbite-vue` is not yet finished.

If you want to browse the components, visit flowbite.com.

If you want to learn more about Flowbite, visit Flowbite docs.

## Getting started

To use `flowbite-vue`, you just need to setup `flowbite` normally and install `flowbite-vue` from `npm`.

`flowbite` can be included as a plugin into an existing Tailwind CSS project.

### Require via `npm`

Make sure that you have Node.js and Tailwind CSS installed.

1. Install `flowbite` as a dependency using `npm` by running the following command:

```bash
npm i flowbite flowbite-vue
```

2. Require `flowbite` as a plugin inside the `tailwind.config.js` file:

```javascript
module.exports = {
  content: [
    ...,
    'node_modules/flowbite-vue/**/*.{js,jsx,ts,tsx}'
  ],
  plugins: [..., require('flowbite/plugin')],
};
```

## Components

    Alerts
    Badge
    Breadcrumbs

    Buttons
    Button group
    Cards

    Dropdown
    :construction: Forms
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
    :construction: Sidebar

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
