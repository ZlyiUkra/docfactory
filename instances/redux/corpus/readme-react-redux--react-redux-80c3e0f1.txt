# react-redux README 8.0.6 … 9.0.1: React Redux
# джерело: https://raw.githubusercontent.com/reduxjs/react-redux/11060e51935d85fef9f99ac15da968dfed99aed4/README.md
# отримано: 2026-10-01
# версія: 9.0.1, 9.0.0, 9.0.0-rc.0, 9.0.0-beta.0, 8.1.3, 9.0.0-alpha.1, 9.0.0-alpha.0, 8.1.2, 8.1.1, 8.1.0, 8.0.7, 8.0.6

Official React bindings for Redux.
Performant and flexible.

GitHub Workflow Status npm version
npm downloads
#redux channel on Discord

## Installation

### Using Create React App

The recommended way to start new apps with React Redux is by using the official Redux+JS/TS templates for Create React App, which takes advantage of Redux Toolkit.

```sh
# JS
npx create-react-app my-app --template redux

# TS
npx create-react-app my-app --template redux-typescript
```

### An Existing React App

React Redux 8.0 requires **React 16.8.3 or later** (or React Native 0.59 or later).

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
