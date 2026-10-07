# create-vite README 2.8.0 … 2.9.5: create-vite
# джерело: https://raw.githubusercontent.com/vitejs/vite/4f00f5835618a772a7ba599ba5e5f2a1fc10ef11/packages/create-vite/README.md
# отримано: 2026-10-01
# версія: 2.9.5, 2.9.4, 2.9.3, 2.9.2, 2.9.1, 2.9.0, 2.8.0

## Scaffolding Your First Vite Project

> **Compatibility Note:**
> Vite requires Node.js version >=12.2.0. However, some templates require a higher Node.js version to work, please upgrade if your package manager warns about it.

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
pnpm create vite my-vue-app -- --template vue
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
