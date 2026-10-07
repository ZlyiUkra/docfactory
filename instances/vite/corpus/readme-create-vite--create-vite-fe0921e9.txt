# create-vite README 3.0.1 … 4.0.0-beta.0: create-vite
# джерело: https://raw.githubusercontent.com/vitejs/vite/4efb188c7c0dec58d6560090ab7ad2ac6363b3f3/packages/create-vite/README.md
# отримано: 2026-10-01
# версія: 4.0.0-beta.0, 3.2.1, 3.2.0, 3.1.0, 3.0.2, 3.0.1

## Scaffolding Your First Vite Project

> **Compatibility Note:**
> Vite requires Node.js version 14.18+, 16+. However, some templates require a higher Node.js version to work, please upgrade if your package manager warns about it.

With NPM:

```bash
$ npm create vite@latest
```

With Yarn:

```bash
$ yarn create vite
```

With PNPM:

```bash
$ pnpm create vite
```

Then follow the prompts!

You can also directly specify the project name and the template you want to use via additional command line options. For example, to scaffold a Vite + Vue project, run:

```bash
# npm 6.x
npm create vite@latest my-vue-app --template vue

# npm 7+, extra double-dash is needed:
npm create vite@latest my-vue-app -- --template vue

# yarn
yarn create vite my-vue-app --template vue

# pnpm
pnpm create vite my-vue-app --template vue
```

Currently supported template presets include:

- `vanilla`
- `vanilla-ts`
- `vue`
- `vue-ts`
- `react`
- `react-ts`
- `preact`
- `preact-ts`
- `lit`
- `lit-ts`
- `svelte`
- `svelte-ts`

You can use `.` for the project name to scaffold in the current directory.

## Community Templates

create-vite is a tool to quickly start a project from a basic template for popular frameworks. Check out Awesome Vite for community maintained templates that include other tools or target different frameworks. You can use a tool like degit to scaffold your project with one of the templates.

```bash
npx degit user/project my-project
cd my-project

npm install
npm run dev
```

If the project uses `main` as the default branch, suffix the project repo with `#main`

```bash
npx degit user/project#main my-project
```
