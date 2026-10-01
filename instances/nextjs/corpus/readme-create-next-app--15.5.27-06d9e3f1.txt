# create-next-app README 15.1.0 … 15.5.27: Create Next App
# джерело: https://raw.githubusercontent.com/vercel/next.js/v15.5.27/packages/create-next-app/README.md
# отримано: 2026-10-01
# версія: 15.5.27, 15.5.26, 15.5.25, 15.5.24, 15.5.23, 15.5.22, 15.5.21, 15.5.20, 15.5.19, 15.5.18, 15.5.16, 15.5.15, 15.5.14, 15.5.13, 16.1.7, 15.5.12, 15.5.11, 16.1.6, 15.1.12, 15.2.9, 15.3.9, 15.4.11, 16.0.11, 15.5.10, 16.1.5, 16.1.4, 16.1.3, 16.1.2, 16.1.1, 16.1.0, 15.1.11, 15.2.8, 15.3.8, 15.4.10, 16.0.10, 15.5.9, 15.1.10, 15.2.7, 15.3.7, 15.4.9, 16.0.9, 15.5.8, 16.0.8, 15.2.6, 15.3.6, 15.1.9, 15.4.8, 15.5.7, 16.0.7, 16.0.6, 16.0.5, 16.0.4, 16.0.3, 16.0.2, 16.0.1, 16.0.0, 15.5.6, 15.5.5, 16.0.0-beta.0, 15.5.4, 15.5.3, 15.5.2, 15.5.1, 15.5.0, 15.4.7, 15.4.6, 15.4.5, 15.4.4, 15.4.3, 15.4.2, 15.4.1, 15.4.0, 15.3.5, 15.3.4, 15.3.3, 15.1.8, 15.3.2, 15.3.1, 15.3.0, 15.2.5, 15.2.4, 15.2.3, 15.2.2, 15.2.1, 15.2.0, 15.1.7, 15.1.6, 15.1.5, 15.1.4, 15.1.3, 15.1.2, 15.1.1, 15.1.0

The easiest way to get started with Next.js is by using `create-next-app`. This CLI tool enables you to quickly start building a new Next.js application, with everything set up for you. You can create a new app using the default Next.js template, or by using one of the official Next.js examples. To get started, use the following command:

### Interactive

You can create a new project interactively by running:

```bash
npx create-next-app@latest
# or
yarn create next-app
# or
pnpm create next-app
# or
bunx create-next-app
```

You will be asked for the name of your project, and then whether you want to
create a TypeScript project:

```bash
✔ Would you like to use TypeScript? … No / Yes
```

Select **Yes** to install the necessary types/dependencies and create a new TS project.

### Non-interactive

You can also pass command line arguments to set up a new project
non-interactively. See `create-next-app --help`:

```bash
Usage: create-next-app [project-directory] [options]

Options:
  -V, --version                        output the version number
  --ts, --typescript

    Initialize as a TypeScript project. (default)

  --js, --javascript

    Initialize as a JavaScript project.

  --tailwind

    Initialize with Tailwind CSS config. (default)

  --eslint

    Initialize with ESLint config.

  --app

    Initialize as an App Router project.

  --src-dir

    Initialize inside a `src/` directory.

  --turbopack

    Enable Turbopack by default for development.

  --import-alias <alias-to-configure>

    Specify import alias to use (default "@/*").

  --empty

    Initialize an empty project.

  --use-npm

    Explicitly tell the CLI to bootstrap the application using npm

  --use-pnpm

    Explicitly tell the CLI to bootstrap the application using pnpm

  --use-yarn

    Explicitly tell the CLI to bootstrap the application using Yarn

  --use-bun

    Explicitly tell the CLI to bootstrap the application using Bun

  -e, --example [name]|[github-url]

    An example to bootstrap the app with. You can use an example name
    from the official Next.js repo or a GitHub URL. The URL can use
    any branch and/or subdirectory

  --example-path <path-to-example>

    In a rare case, your GitHub URL might contain a branch name with
    a slash (e.g. bug/fix-1) and the path to the example (e.g. foo/bar).
    In this case, you must specify the path to the example separately:
    --example-path foo/bar

  --reset-preferences

    Explicitly tell the CLI to reset any stored preferences

  --skip-install

    Explicitly tell the CLI to skip installing packages

  --disable-git

    Explicitly tell the CLI to skip initializing a git repository.

  --yes

    Use previous preferences or defaults for all options that were not
    explicitly specified, without prompting.

  -h, --help                           display help for command
```

### Why use Create Next App?

`create-next-app` allows you to create a new Next.js app within seconds. It is officially maintained by the creators of Next.js, and includes a number of benefits:

- **Interactive Experience**: Running `npx create-next-app@latest` (with no arguments) launches an interactive experience that guides you through setting up a project.
- **Zero Dependencies**: Initializing a project is as quick as one second. Create Next App has zero dependencies.
- **Offline Support**: Create Next App will automatically detect if you're offline and bootstrap your project using your local package cache.
- **Support for Examples**: Create Next App can bootstrap your application using an example from the Next.js examples collection (e.g. `npx create-next-app --example route-handlers`).
- **Tested**: The package is part of the Next.js monorepo and tested using the same integration test suite as Next.js itself, ensuring it works as expected with every release.
