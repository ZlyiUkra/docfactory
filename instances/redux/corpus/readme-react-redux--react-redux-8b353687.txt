# react-redux README 9.4.0-alpha.0 … 9.4.0-alpha.2: React Redux
# джерело: https://raw.githubusercontent.com/reduxjs/react-redux/457f0b3689fd74f9c4dfb310f634207e9f078306/README.md
# отримано: 2026-10-01
# версія: 9.4.0-alpha.2, 9.4.0-alpha.1, 9.4.0-alpha.0

Official React bindings for Redux.
Performant and flexible.

GitHub Workflow Status npm version
npm downloads
#redux channel on Discord

## Installation

### Create a React Redux App

The recommended way to start new apps with React and Redux is by using our official Redux+TS template for Vite, or by creating a new Next.js project using Next's `with-redux` template.

Both of these already have Redux Toolkit and React-Redux configured appropriately for that build tool, and come with a small example app that demonstrates how to use several of Redux Toolkit's features.

```bash
# Vite with our Redux+TS template
# (using the `tiged` tool to clone and extract the template)
npx tiged reduxjs/redux-templates/packages/vite-template-redux my-app

# Next.js using the `with-redux` template
npx create-next-app --example with-redux my-app
```

### An Existing React App

React Redux 9.0 requires **React 18 or later**

To use React Redux with your React app, install it as a dependency:

```bash
# If you use npm:
npm install react-redux

# Or if you use Yarn:
yarn add react-redux
```

You'll also need to install Redux and set up a Redux store in your app.

This assumes that you’re using npm package manager
with a module bundler like Webpack or
Browserify to consume [CommonJS
modules](https://webpack.js.org/api/module-methods/#commonjs).

If you don’t yet use npm or a modern module bundler, and would rather prefer a single-file UMD build that makes `ReactRedux` available as a global object, you can grab a pre-built version from cdnjs. We _don’t_ recommend this approach for any serious application, as most of the libraries complementary to Redux are only available on npm.

## Documentation

The React Redux docs are published at **https://react-redux.js.org** .

## How Does It Work?

The post The History and Implementation of React-Redux
explains what it does, how it works, and how the API and implementation have evolved over time.

There's also a Deep Dive into React-Redux talk that covers some of the same material at a higher level.

## License

MIT
