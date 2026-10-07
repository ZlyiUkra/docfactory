# daisyui README 2.6.2
# джерело: https://raw.githubusercontent.com/saadeghi/daisyui/310eab6e73addccb50a7e6582254f7c7d45746ec/README.md
# отримано: 2026-09-30
# версія: 2.6.2

![][docs-url]

**Tailwind CSS Components**
Adds component classes like `btn`, `card` and more to Tailwind CSS

 [See all components ]

![][tweet-url]

![][docs-url]

## daisyUI 2.0

![][build-url] ![][npm-url] ![][docs-url] ![][license-url]
![][npm-url] ![][gh-url] ![][gh-url]

- 👉  [See all components ]
- 📘 Documents: daisyui.com
- 🎲 Try it online: Tailwind Play | Codepen
- 📦 Source: GitHub | NPM | Unpkg | JSdeliver | cdnjs

---

## 🌼 Features

  show / hide

- **Tailwind CSS plugin**
  daisyUI is a Tailwind CSS plugin. Install it and add it to your `tailwind.config.js` file.
- **Component classes**
  Adds component classes to Tailwind. Classes like `btn`, `card`,… So you will end up with a cleaner HTML.
- **Semantic color names**
  Adds color names like `primary`, `secondary`, `accent`,….
- **Customizable**
  You can customize the design of components with Tailwind utility classes and CSS variables.
- **Themeable**
  Add multiple themes and customize colors. You can even set a theme for a specific section of your page.
- **RTL supported**
  Enable `rtl` config for right to left layouts.
- **Pure CSS**
  No script file. Pure CSS. Works on all frameworks!

---

## 📀 Install now!

```bash
npm i daisyui
```

Then add daisyUI to your `tailwind.config.js`
 [Read more ]

```js
module.exports = {
  plugins: [require("daisyui")],
};
```

  Or use a CDN

Loading CSS files from CDN is not recommended for production. It's better to install Tailwind and daisyUI as Nodejs dependencies so you can config/customize everything, and purge unused styles.

```html
<link href="https://cdn.jsdelivr.net/npm/daisyui@2.6.1/dist/full.css" rel="stylesheet" type="text/css" />
<script src="https://cdn.tailwindcss.com"></script>
```

---

## 🚀 Use

Use component classes to build your UI.

```html
<a class="btn">Hello!</a>
```

```html
<input type="checkbox" class="checkbox" />
```

```html
<input type="checkbox" class="toggle" />
```

```html
<div class="alert alert-success">Message sent successfully</div>
```

👉 See all components
🎲 Try it online

---

## 📘 Documents + Examples

See the official site:
 [daisyui.com ↗︎ ]

---

## 🤝 Contributing

Read the documents for more info:
 [Read contribution guide ]

---

## List of Components

  show / hide

- Actions
  - [x] Button
  - [x] Dropdown
  - [x] Modal
  - [x] Swap

- Data display
  - [x] Alert
  - [x] Avatar
  - [x] Badge
  - [ ] Banner
  - [ ] Calendar
  - [x] Card
  - [x] Carousel
  - [ ] Chat bubble
  - [x] Collapse
  - [ ] Comment
  - [x] Countdown
  - [ ] Empty placeholder
  - [x] Kbd
  - [ ] Loading
  - [x] Progress
  - [x] Radial progress
  - [x] Stat
  - [x] Table
  - [ ] Tag
  - [ ] Timeline
  - [ ] Toast
  - [x] Tooltip
  - [ ] Treeview

- Data input
  - [x] Checkbox
  - [x] Text input
  - [x] Radio
  - [x] Range
  - [x] Rating
  - [x] Select
  - [x] Textarea
  - [x] Toggle
  - [ ] Upload

- Layout
  - [x] Artboard
  - [x] Button group
  - [x] Divider
  - [x] Drawer
  - [x] Footer
  - [x] Hero
  - [x] Indicator
  - [x] Input group
  - [x] Mask
  - [x] Stack

- Navigation
  - [ ] App bar
  - [x] Breadcrumbs
  - [x] Link
  - [x] Menu
  - [x] Navbar
  - [x] Pagination
  - [x] Steps
  - [x] Tab

- Mockup
  - [ ] Browser
  - [x] Code
  - [x] Phone
  - [x] Window

---

## Featured on:

  show / hide

- Blogs
  - Logrocket
  - GraphCMS
  - wweb.dev
  - flaming.codes
  - rockyourcode
  - HackerNews
  - Product Hunt
  - Siecle Digital
  - speckyboy
  - dailydev
  - Future Tech Blog (Japanese)
- Youtube videos
  - Supabase & Sveltekit - Build Twitter in 75 minutes
  - Setup the Best Frontend JavaScript Stack - Svelte, Vite, TailwindCSS and DaisyUI
  - Jamstack powered Image gallery with Cloudinary, Tailwind and DaisyUI
  - SvelteKit Crash Course w/ Tailwind CSS and DaisyUI, GraphQL and dynamic routes
  - DaisyUI : Worth a try or skip on by?
  - How to use daisyUI in SvelteKit?
  - DaisyUI Untuk Yang Mau Pindah ke TailwindCSS dari Bootstrap (Indonesian)
  - Next.js - Tailwind - DeisyUI Setup
  - Svelte Setup with Vite, Tailwind, DaisyUI. Custom Themes!
  - Build a blog with Svelte
  - Building a product in less than 10 minutes: Laravel, InertiaJS, VueJS, TailwindCSS, DaisyUI
  - Infinite scrolling with MERN | ReactJS, TailwindCSS v3, DaisyUI | NodeJs, Express, MongoDB
  - How to install TailwindCSS v3 and DaisyUI to your React app
  - Laravel: DaisyUI Agiliza Tus Desarrollos Con TailwindCSS + Select2 Tailwind Style (Spanish)
- Courses
  - Building with SvelteKit and GraphCMS
  - Svelte for Beginners by Mike Karan
  - React Front To Back 2022 by Brad Traversy
  - Build Instagram profile page UI clone w/Next.js TailwindCSS
  - Instagram UI Clone Login Page w/ NextJS & TailwindCSS
  - Build your Developer Portfolio and Blog from Scratch with Svelte and GraphCMS

---

༼ つ ◕_◕ ༽つ  Please share

![][tweet-url]

[install-size]: https://badgen.net/bundlephobia/minzip/daisyui?label=bundle%20size&color=green
[build]: https://badgen.net/github/checks/saadeghi/daisyui?label=build
[npm]: https://badgen.net/github/tag/saadeghi/daisyui?label=version&color=green
[dl]: https://badgen.net/npm/dt/daisyui?label=installs&icon=npm&color=green
[commit]: https://badgen.net/github/last-commit/saadeghi/daisyui?icon=github&color=green
[license]: https://badgen.net/github/license/saadeghi/daisyui?color=green
[stars]: https://badgen.net/github/stars/saadeghi/daisyui?color=green
[tweet]: https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fsaadeghi%2Fdaisyui
[install-size-url]: https://bundlephobia.com/result?p=daisyui
[license-url]: https://github.com/saadeghi/daisyui/blob/master/LICENSE
[npm-url]: https://www.npmjs.com/package/daisyui
[cdnjs-url]: https://cdnjs.com/libraries/daisyui
[gh-url]: https://github.com/saadeghi/daisyui
[tw-play-url]: https://daisyui.com/tailwindplay
[codepen-url]: https://codepen.io/saadeghi/pen/gOwWKvv
[unpkg-url]: https://unpkg.com/browse/daisyui/
[jsdeliver-url]: https://www.jsdelivr.com/package/npm/daisyui
[build-url]: https://github.com/saadeghi/daisyui/actions
[tweet-url]: https://twitter.com/intent/tweet?text=daisyUI%20%0D%0AUI%20Components%20for%20Tailwind%20CSS%20%0D%0Ahttps://github.com/saadeghi/daisyui
[number-of-components]: https://badgen.net/badge/total%20components/45/green
[docs-url-install]: https://daisyui.com/docs/install
[docs-url]: https://daisyui.com/
[logo-url]: https://raw.githubusercontent.com/saadeghi/files/main/daisyui/logo-4.svg
[banner-url]: https://raw.githubusercontent.com/saadeghi/files/main/daisyui/card-3.png
