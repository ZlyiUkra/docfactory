# preline README 1.9.0
# джерело: https://raw.githubusercontent.com/htmlstreamofficial/preline/v1.9.0/README.md
# отримано: 2026-09-30
# версія: 1.9.0

Preline UI is an open-source set of prebuilt UI components based on the utility-first Tailwind CSS framework.

License: MIT

## Why use Preline UI?

Based on the Tailwind CSS utility classes, Preline UI's prebuilt components and UI elements help you quickly design and customize responsive mobile-first websites with the components a website needs, including buttons, dropdowns, navigation bars, modals, and more.

## What's in the box?

Components are grouped by visual usability criteria (components, navigation, forms, etc.) and styled directly on top of Tailwind CSS, making them easy to extend and customize. This is a lifesaver for developers looking to create a unique and eye-catching design system without the hassle of creating each component by hand.

## Getting Started

### Quick Setup

This guide will help you get started with Preline UI, including how to run, customize, update, and integrate your project!

First, you need to make sure that you have a working Tailwind CSS project installed and that you also have Node and NPM installed on your machine.

### Require via NPM

1. Install preline via npm

npm i preline

2. Include Preline UI as a plugin in the tailwind.config.js file

module.exports = {
  content: [
    'node_modules/preline/dist/*.js'
  ],
  plugins: [
    require('preline/plugin')
  ],
}

3. Include the JavaScript  that powers the interactive elements near the end of your <body> tag:

## Documentation

For full documentation of the Preline options, visit preline.co. The site also contains information on the wide variety of plugins that are available for TailwindCSS projects.

## Community

For help, discussion about best practices, or any other conversation that would benefit from being searchable use GitHub Discussions

## License

Preline UI is Open Source project and licensed under MIT.

Preline UI Figma is free for both commercial and personal projects, learn more here.

All brand icons are trademarks of their respective owners. The use of these trademarks does not indicate endorsement of the trademark holder by Preline UI, nor vice versa.

## A product of Htmlstream

Preline UI is built and maintend by Htmlstream team. Over the last decade at Htmlstream, our journey has involved crafting UI Components and Templates. This process has allowed us to understand and explore a range of strategies for developing versatile UI designs that can adapt to a variety of needs.

Share about Preline on Twitter and keep an eye on Dribbble for teasers of our upcoming UIs.
