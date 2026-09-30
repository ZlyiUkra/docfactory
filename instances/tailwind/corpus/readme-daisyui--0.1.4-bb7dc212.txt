# daisyui README 0.1.4: DaisyUI 🌼
# джерело: https://raw.githubusercontent.com/saadeghi/daisyui/74dbd77e8197d98535bff2e0ae0ec26147a798a6/README.md
# отримано: 2026-09-30
# версія: 0.1.4

Styled (and unstyled) UI Components for Tailwind CSS users

## Install

```
npm i daisyui
```

## Add plugin and preset to `tailwind.config.js`

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

## Or use a CDN

🌼 styled version
```
<link rel="stylesheet" href="https://unpkg.com/daisyui@latest/dist/styled.min.css" />
```
unstyled version
```
<link rel="stylesheet" href="https://unpkg.com/daisyui@latest/dist/base.min.css" />
```
