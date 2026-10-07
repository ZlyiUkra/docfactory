# react-redux README 7.1.1 … 7.2.0: React Redux
# джерело: https://raw.githubusercontent.com/reduxjs/react-redux/ec38c1bd0026bedca3fd7a8db063f242b0378694/README.md
# отримано: 2026-10-01
# версія: 7.2.0, 7.1.3, 7.1.2, 7.1.2-alpha.0, 7.1.1

Official React bindings for Redux.
Performant and flexible.

build status npm version
npm downloads
redux channel on discord

## Installation

React Redux requires **React 16.8.3 or later.**

```
npm install --save react-redux
```

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
