# daisyui README 0.1.19 … 0.1.21: DaisyUI 🌼
# джерело: https://raw.githubusercontent.com/saadeghi/daisyui/0ca658b07053b3c0b720bc72bb1ea6aa8f1326ea/README.md
# отримано: 2026-09-30
# версія: 0.1.21, 0.1.20, 0.1.19

logo

See components in action 👉 https://daisyui.netlify.app/

Unstyled *(and styled)* UI component library for Tailwind CSS users

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

## 1. Install

```
npm i daisyui
```

#### then add plugin and preset to `tailwind.config.js`

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

### 2. Set up the colors for your design system (optional)

If you want to use your custom colors, you need to define the color values in your css. Colors must be themeable so we're using CSS Variables.
↗︎ Theming guide

## Components

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

## Todo

- [ ] Add all components
- [ ] Complete documents
- [ ] Add demo for components
