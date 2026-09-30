# daisyui README 0.1.22
# джерело: https://raw.githubusercontent.com/saadeghi/daisyui/dd4423fca19656e6200c6cb98b257f9ed0de37af/README.md
# отримано: 2026-09-30
# версія: 0.1.22

[](#)

Unstyled (and styled) UI component library based on Tailwind CSS

![][tweet-url]

## DaisyUI 🌼

![][install-size-url]
![][base-css-url]
![][styled-css-url]

![][build-url]
![][npm-url]
![][npm-url]
![][gh-url]
![][license-url]

[install-size]: https://badgen.net/packagephobia/publish/daisyui?label=package%20install%20size&icon=npm&color=purple
[base-css]: https://badgen.net/badgesize/normal/https/unpkg.com/daisyui/dist/base.min.css?label=base.css%20size&color=purple
[styled-css]: https://badgen.net/badgesize/normal/https/unpkg.com/daisyui/dist/styled.min.css?label=styled.css%20size&color=purple
[build]: https://badgen.net/github/checks/saadeghi/daisyui?label=build
[npm]: https://badgen.net/npm/v/daisyui?label=version&icon=npm&color=purple
[dl]: https://badgen.net/npm/dt/daisyui?icon=npm&color=purple
[commit]: https://badgen.net/github/last-commit/saadeghi/daisyui?icon=github&color=purple
[license]: https://badgen.net/github/license/saadeghi/daisyui?color=purple
[tweet]: https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fsaadeghi%2Fdaisyui

[install-size-url]: https://packagephobia.com/result?p=daisyui
[base-css-url]: https://unpkg.com/daisyui@latest/dist/base.min.css
[styled-css-url]: https://unpkg.com/daisyui@latest/dist/styled.min.css
[license-url]: https://github.com/saadeghi/daisyui/blob/master/LICENSE
[npm-url]: https://www.npmjs.com/package/daisyui
[gh-url]: https://github.com/saadeghi/daisyui
[build-url]: https://github.com/saadeghi/daisyui/actions
[tweet-url]: https://twitter.com/intent/tweet?text=Checkout%20DaisyUI%20on%20github%20https://github.com/saadeghi/daisyui

## Demo

↗︎ See all components

## Get Started

## 1. Install

You need TailwindCSS 2.0+ of course.

```
npm i daisyui
```

Then add plugin and preset to `tailwind.config.js`
```
module.exports = {
  plugins: [
    require('daisyui/styled'), // 🌼 for styled UI
    // require('daisyui'), // for base UI only
  ],
  presets: [
    require('daisyui/preset')
  ],
}

```

  Or use a CDN

- 🌼 styled version
```
<link rel="stylesheet" href="https://unpkg.com/daisyui@latest/dist/styled.min.css" />
```
- unstyled version
```
<link rel="stylesheet" href="https://unpkg.com/daisyui@latest/dist/base.min.css" />
```

---

## 2. Set up the colors for your design system (optional)

If you want to use your custom colors , you need to define the color values in your css. Colors must be themeable so we're using CSS Variables.
↗︎ Theming guide and examples

## FAQ

  Why do I need it?

> ↗︎ Utility first is fast and scalable but developing a scalable design system with utility first is messy, time consuming hard to manage. So why not put all basic skeleton of your UI components in one place and use it on all your design systems then use the power of utility first everywhere?

  How does it work?

> **DaisyUI** provides basic and unstyled component classes that you can use for almost all design systems. It also has an optional style that you can use if you don't want to fully design your components.
> It's all based on tailwind so you can customize everything with utility classes and ↗︎ purge all unused class names.

  What's included?

> When you add **DaisyUI** as a Tailwind CSS plugin, it gives you ready-to-use UI component classes to use. Like `btn`, `card`, `alert`, etc...
> If you use the unstyled version, it has no color or visual style so you can fully style the components with Tailwind utility classes. If you use styled version, you get something pre-designed (like Bootstrap) but you can still customize it with Tailwind classes.

  Concepts

> - **Typography, spacing, layout** You will handle these with tailwind classes. We suggest using the official ↗︎ Tailwind Typography plugin
> - **Colors and theming** You should ditch Tailwind's default and multi-purpose color set and set your custom set of colors for a DaisyUI project. (↗︎ Theming guide)
> - **Components** (like button, card, etc...) DaisyUI will handle this

  What is "preset"

```
module.exports = {
  // ...
  presets: [
    require('daisyui/preset')
  ],
}

```
> When you add DaisyUI preset it will replaces default tailwind colors with a set of semantic color set that is themeable and can be configed with CSS variables.
> `daisyui/preset` also adds a few `borderRadius` that is used in components. They are also configurable with CSS variables.

---

## Components

  Show

- [x] Accordion
- [x] Alert
- [ ] Artboard
- [ ] App bar
- [x] Avatar
- [ ] Avatar group
- [x] Badge
- [ ] Banner
- [ ] Breadcrumb
- [x] Button
- [x] Button group
- [x] Card
- [ ] Chat bubble
- [ ] Comment
- [ ] Divider
- [ ] Empty placeholder
- [ ] Form
  - [ ] Dropdown
  - [ ] Select
  - [x] Text input
  - [ ] Text area
  - [ ] Checkbox
  - [ ] Radio
  - [ ] Range slider
  - [ ] Switch
  - [ ] Upload
- [ ] Loading
- [x] Menu
- [ ] Navbar
- [ ] Modal
- [x] Pagination
- [ ] Progress
- [ ] Progress indicator
- [ ] Skeleton placeholder
- [ ] Statistic
- [ ] Steps
- [ ] Tag
- [ ] Tabs
- [ ] Timeline
- [ ] Toast
- [ ] Tooltip

---

Please share
![][tweet-url]
