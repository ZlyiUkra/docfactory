# flowbite README 1.4.1
# джерело: https://raw.githubusercontent.com/themesberg/flowbite/d5a516c1b3ecf17db2bd0756e0f2302f354c6f17/README.md
# отримано: 2026-09-30
# версія: 1.4.1

    Build websites even faster with components on top of Tailwind CSS

------

## Documentation

For full documentation, visit flowbite.com.

## Components

Flowbite is an open source collection of UI components built with the utility classes from Tailwind CSS that you can use as a starting point when coding user interfaces and websites.

    Alerts
    Badge
    Breadcrumbs

    Buttons
    Button group
    Cards

    Dropdown
    Forms
    List group

    Typography
    Modal
    Tabs

    Navbar
    Pagination
    Timeline

    Progress bar
    Tables
    Toast

    Tooltips
    Datepicker
    Spinner

    Footer
    Accordion
    Sidebar

    Carousel

## Getting started

Flowbite can be included as a plugin into an existing Tailwind CSS project and it is supposed to help you build websites faster by having a set of web components to work with built with the utility classes from Tailwind CSS.

### Require via NPM

Make sure that you have Node.js and Tailwind CSS installed.

1. Install Flowbite as a dependency using NPM by running the following command:

```bash
npm i flowbite
```

2. Require Flowbite as a plugin inside the `tailwind.config.js` file:

```javascript
module.exports = {

    plugins: [
        require('flowbite/plugin')
    ]

}
```

3. Include the main JavaScript file to make interactive elements work:

```html
<script src="../path/to/flowbite/dist/flowbite.js"></script>
```

If you use Webpack or other bundlers you can also import it like this:

```javascript
import 'flowbite';
```

### Include via CDN

The quickest way to get started working with FlowBite is to simply include the CSS and JavaScript into your project via CDN.

Require the following minified stylesheet inside the `head` tag:

```html
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />
```

And include the following javascript file before the end of the `body` element:

```html
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
```

## Community

If you need help or just want to discuss about the library join the community on Github:

⌨️ Discuss about Flowbite on GitHub

For casual chatting with others using the library:

💬 Join the Flowbite Discord Server

## Figma

If you need the Figma files for the components you can check out our website for more information:

🎨 Get access to the Figma design files

## Copyright and license

The Flowbite name and logos are trademarks of Crafty Dwarf Inc.

📝 Read about the licensing terms
