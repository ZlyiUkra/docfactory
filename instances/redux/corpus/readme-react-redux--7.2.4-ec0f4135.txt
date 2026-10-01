# react-redux README 7.2.1 … 7.2.4: React Redux
# джерело: https://raw.githubusercontent.com/reduxjs/react-redux/86e962edf8ed077cf720e8e089876227d943dfe8/README.md
# отримано: 2026-10-01
# версія: 7.2.4, 7.2.3, 7.2.2, 7.2.1

Official React bindings for Redux.
Performant and flexible.

build status npm version
npm downloads
redux channel on discord

## Installation

### Using Create React App

The recommended way to start new apps with React Redux is by using the official Redux+JS template for Create React App, which takes advantage of Redux Toolkit.

```sh
npx create-react-app my-app --template redux
```

### An Existing React App

React Redux 7.1 requires **React 16.8.3 or later.**

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

If you don’t yet use npm or a modern module bundler, and would rather prefer a single-file UMD build that makes `ReactRedux` available as a global object, you can grab a pre-built version from cdnjs. We *don’t* recommend this approach for any serious application, as most of the libraries complementary to Redux are only available on npm.

## React Native

As of React Native 0.18, React Redux 5.x should work with React Native. If you have any issues with React Redux 5.x on React Native, run `npm ls react` and make sure you don’t have a duplicate React installation in your `node_modules`. We recommend that you use `npm@3.x` which is better at avoiding these kinds of issues.

## Documentation

The React Redux docs are now published at **https://react-redux.js.org** .

We're currently expanding and rewriting our docs content - check back soon for more updates!

## How Does It Work?

We do a deep dive on how React Redux works in this readthesource episode.

Also, the post The History and Implementation of React-Redux
explains what it does, how it works, and how the API and implementation have evolved over time.

Enjoy!

## License

MIT
