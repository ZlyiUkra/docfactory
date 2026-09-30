# @spartan-ng/cli README 0.0.1-alpha.705 … 0.0.1-alpha.720: @spartan-ng/cli
# джерело: https://raw.githubusercontent.com/spartan-ng/spartan/31ef93424f583464d00c6fa8fe4e96617797027c/libs/cli/README.md
# отримано: 2026-09-30
# версія: 0.0.1-alpha.720, 0.0.1-alpha.719, 0.0.1-alpha.718, 0.0.1-alpha.717, 0.0.1-alpha.716, 0.0.1-alpha.715, 0.0.1-alpha.714, 0.0.1-alpha.713, 0.0.1-alpha.712, 0.0.1-alpha.711, 0.0.1-alpha.710, 0.0.1-alpha.709, 0.0.1-alpha.708, 0.0.1-alpha.707, 0.0.1-alpha.706, 0.0.1-alpha.705

npm version
npm downloads
License: MIT
Discord

Website • Documentation • Components • GitHub

> The official CLI for spartan/ui. Add accessible, beautifully styled Angular components to any project with one command.

`@spartan-ng/cli` is an Nx plugin and Angular schematic that wires up the spartan/ui two-layer architecture for you: the **brain** primitives are installed from npm and the **helm** styles are copied into your codebase where you own them. Works with both Angular CLI projects and Nx workspaces - no extra configuration required.

## Installation

```bash
npm install -D @spartan-ng/cli
# or
pnpm add -D @spartan-ng/cli
# or
yarn add -D @spartan-ng/cli
```

> **Prerequisite:** spartan/ui requires Tailwind CSS. If you haven't set it up yet, follow the official Angular installation guide first.

## Quick Start

```bash
# 1. Initialize spartan in your project (theme, dependencies, Tailwind preset)
ng g @spartan-ng/cli:init
# Nx: npx nx g @spartan-ng/cli:init

# 2. Add the components you need (interactive picker)
ng g @spartan-ng/cli:ui
# Nx: npx nx g @spartan-ng/cli:ui

# 3. Add a single component by name
ng g @spartan-ng/cli:ui button
```

The CLI installs the relevant `@spartan-ng/brain` entry points as npm dependencies and copies the helm component code straight into your project so you can edit every style.

## Generators

### Setup

| Generator     | Description                                                                                |
| ------------- | ------------------------------------------------------------------------------------------ |
| `init`        | Initialize a spartan/ui project - adds dependencies, the Tailwind preset, and the theme.   |
| `ui`          | Add one, many, or all spartan/ui primitives to your project.                               |
| `ui-theme`    | Generate the theme CSS variables and Tailwind setup interactively.                         |
| `healthcheck` | Scan your workspace for outdated patterns and (optionally) auto-fix them with `--autoFix`. |

### Migrations

The CLI ships with a suite of generators that automate breaking changes between spartan releases. They keep upgrades to a single command.

View all migration generators

| Generator                            | Description                                                                                  |
| ------------------------------------ | -------------------------------------------------------------------------------------------- |
| `migrate-brain-accordion-trigger`    | Wrap brain accordion triggers in a heading element.                                          |
| `migrate-brain-imports`              | Move brain imports to their secondary entry points.                                          |
| `migrate-brn-checkbox-changed-event` | Rename `changed` to `checkedChange` on `brn-checkbox`.                                       |
| `migrate-brn-switch-changed-event`   | Rename `changed` to `checkedChange` on `brn-switch`.                                         |
| `migrate-core`                       | Migrate the legacy `core` library to the `@spartan-ng/brain/core` entry point.               |
| `migrate-date-picker`                | Rename `changed` to `dateChange` on `hlm-date-picker`.                                       |
| `migrate-helm-imports`               | Move helm imports to the new entry-point structure.                                          |
| `migrate-helm-libraries`             | Update helm libraries to their latest versions.                                              |
| `migrate-hlm`                        | Move `hlm` from `@spartan-ng/brain` to `@spartan-ng/helm/utils`.                             |
| `migrate-input-id`                   | Rename the `id` input on helm inputs to `inputId`.                                           |
| `migrate-icon`                       | Migrate `hlm-icon` to `ng-icon`.                                                             |
| `migrate-module-imports`             | Replace `NgModule`-style imports with `const` array imports.                                 |
| `migrate-naming-conventions`         | Update legacy naming conventions to the latest standards.                                    |
| `migrate-progress`                   | Migrate `brn-progress` to `hlm-progress`.                                                    |
| `migrate-radio`                      | Migrate `brn-radio` to `hlm-radio`.                                                          |
| `migrate-scroll-area`                | Migrate `hlm-scroll-area` to `ngx-scrollbar`.                                                |
| `migrate-select`                     | Migrate `brn-select` / `hlm-select` to `openChange` and active descendants.                  |
| `migrate-separator`                  | Migrate `brn-separator` to `hlm-separator`.                                                  |
| `migrate-toggle-group`               | Move `brn-toggle-group` from `@spartan-ng/brain/toggle` to `@spartan-ng/brain/toggle-group`. |

Run any migration with:

```bash
ng g @spartan-ng/cli:<migration-name>
# Nx: npx nx g @spartan-ng/cli:<migration-name>
```

## What the CLI does

When you add a component, the CLI:

- **Installs the brain primitive** - adds the right `@spartan-ng/brain` secondary entry point to your `package.json`.
- **Copies the helm styles** - drops the styled component into your project so you can edit it freely.
- **Wires up imports** - updates your workspace configuration so the new components resolve out of the box.
- **Creates libraries (Nx)** - optionally generates buildable Nx libraries for clean code organization.

## Supported Components

The `ui` generator can scaffold any of the spartan/ui primitives, including accordion, alert, alert-dialog, aspect-ratio, autocomplete, avatar, badge, breadcrumb, button, button-group, calendar, card, carousel, checkbox, collapsible, combobox, command, context-menu, date-picker, dialog, dropdown-menu, empty, field, hover-card, icon, input, input-group, input-otp, item, kbd, label, menubar, native-select, navigation-menu, pagination, popover, progress, radio-group, resizable, scroll-area, select, separator, sheet, sidebar, skeleton, slider, sonner, spinner, switch, table, tabs, textarea, toggle, toggle-group, tooltip, typography, and utils.

See the components gallery for live examples.

## Documentation

- CLI documentation
- Installation guide
- Theming
- Components

## Community

- Discord
- GitHub
- Twitter / X
- Sponsor the project

## License

MIT © goetzrobin and the spartan contributors
