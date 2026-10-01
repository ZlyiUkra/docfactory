# create-next-app README 11.0.1 … 11.1.4: Create Next App
# джерело: https://raw.githubusercontent.com/vercel/next.js/75b7a57e0f0044d9315eb6adbd4231b67799d0b1/packages/create-next-app/README.md
# отримано: 2026-10-01
# версія: 11.1.4, 12.0.7, 11.1.3, 12.0.6, 12.0.5, 12.0.4, 12.0.3, 12.0.2, 12.0.1, 12.0.0, 11.1.2, 11.1.1, 11.1.0, 11.0.1

The easiest way to get started with Next.js is by using `create-next-app`. This CLI tool enables you to quickly start building a new Next.js application, with everything set up for you. You can create a new app using the default Next.js template, or by using one of the official Next.js examples. To get started, use the following command:

```bash
npx create-next-app
```

Or, for a TypeScript project:

```bash
npx create-next-app --typescript
```

To create a new app in a specific folder, you can send a name as an argument. For example, the following command will create a new Next.js app called `blog-app` in a folder with the same name:

```bash
npx create-next-app blog-app
```

## Options

`create-next-app` comes with the following options:

- **--ts, --typescript** - Initialize as a TypeScript project.
- **-e, --example [name]|[github-url]** - An example to bootstrap the app with. You can use an example name from the Next.js repo or a GitHub URL. The URL can use any branch and/or subdirectory.
- **--example-path <path-to-example>** - In a rare case, your GitHub URL might contain a branch name with a slash (e.g. bug/fix-1) and the path to the example (e.g. foo/bar). In this case, you must specify the path to the example separately: `--example-path foo/bar`
- **--use-npm** - Explicitly tell the CLI to bootstrap the app using npm. To bootstrap using yarn we recommend to run `yarn create next-app`

## Why use Create Next App?

`create-next-app` allows you to create a new Next.js app within seconds. It is officially maintained by the creators of Next.js, and includes a number of benefits:

- **Interactive Experience**: Running `npx create-next-app` (with no arguments) launches an interactive experience that guides you through setting up a project.
- **Zero Dependencies**: Initializing a project is as quick as one second. Create Next App has zero dependencies.
- **Offline Support**: Create Next App will automatically detect if you're offline and bootstrap your project using your local package cache.
- **Support for Examples**: Create Next App can bootstrap your application using an example from the Next.js examples collection (e.g. `npx create-next-app --example api-routes`).
- **Tested**: The package is part of the Next.js monorepo and tested using the same integration test suite as Next.js itself, ensuring it works as expected with every release.
