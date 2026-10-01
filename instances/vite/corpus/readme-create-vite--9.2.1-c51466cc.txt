# create-vite README 9.0.7 … 9.2.1: create-vite <a href="https://npmjs.com/package/create-vite"><img src="https://img.shields.io/npm/v/create-vite" alt="npm package"></a>
# джерело: https://raw.githubusercontent.com/vitejs/vite/create-vite@9.2.1/packages/create-vite/README.md
# отримано: 2026-10-01
# версія: 9.2.1, 9.2.0, 9.1.2, 9.1.1, 9.1.0, 9.0.7

## Scaffolding Your First Vite Project

> **Compatibility Note:**
> Vite requires Node.js version 20.19+, 22.12+. However, some templates require a higher Node.js version to work, please upgrade if your package manager warns about it.

With NPM:

```bash
npm create vite@latest
```

With Yarn:

```bash
yarn create vite
```

With PNPM:

```bash
pnpm create vite
```

With Bun:

```bash
bun create vite
```

With Deno:

```bash
deno init --npm vite
```

Then follow the prompts!

You can also directly specify the project name and the template you want to use via additional command line options. For example, to scaffold a Vite + Vue project, run:

```bash
# npm 7+, extra double-dash is needed:
npm create vite@latest my-vue-app -- --template vue

# yarn
yarn create vite my-vue-app --template vue

# pnpm
pnpm create vite my-vue-app --template vue

# Bun
bun create vite my-vue-app --template vue

# Deno
deno init --npm vite my-vue-app --template vue
```

Currently supported template presets include:

- `vanilla`
- `vanilla-ts`
- `vue`
- `vue-ts`
- `react`
- `react-compiler`
- `react-ts`
- `react-compiler-ts`
- `preact`
- `preact-ts`
- `lit`
- `lit-ts`
- `svelte`
- `svelte-ts`
- `solid`
- `solid-ts`
- `qwik`
- `qwik-ts`

You can use `.` for the project name to scaffold in the current directory.

## Community Templates

create-vite is a tool to quickly start a project from a basic template for popular frameworks. Check out Awesome Vite for community maintained templates that include other tools or target different frameworks. You can use a tool like tiged to scaffold your project with one of the templates.

```bash
npx tiged user/project my-project
cd my-project

npm install
npm run dev
```
