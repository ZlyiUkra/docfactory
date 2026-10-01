# react-redux README 5.1.0 … 5.1.2: React Redux
# джерело: https://raw.githubusercontent.com/reduxjs/react-redux/4be2626f288d36ed1b781bc8844a1355044a8f21/README.md
# отримано: 2026-10-01
# версія: 5.1.2, 6.0.0, 6.0.0-beta.3, 5.1.1, 6.0.0-beta.2, 6.0.0-beta.1, 5.1.0

Official React bindings for Redux.
Performant and flexible.

build status npm version
npm downloads
redux channel on discord

## Installation

React Redux requires **React 0.14 or later.**

```
npm install --save react-redux
```

This assumes that you’re using npm package manager with a module bundler like Webpack or Browserify to consume CommonJS modules.

If you don’t yet use npm or a modern module bundler, and would rather prefer a single-file UMD build that makes `ReactRedux` available as a global object, you can grab a pre-built version from cdnjs. We *don’t* recommend this approach for any serious application, as most of the libraries complementary to Redux are only available on npm.

## React Native

As of React Native 0.18, React Redux 5.x should work with React Native. If you have any issues with React Redux 5.x on React Native, run `npm ls react` and make sure you don’t have a duplicate React installation in your `node_modules`. We recommend that you use `npm@3.x` which is better at avoiding these kinds of issues.

If you are on an older version of React Native, you’ll need to keep using React Redux 3.x branch and documentation because of this problem.

## Documentation

The React-Redux docs are now published at **https://react-redux.js.org** .

We're currently expanding and rewriting our docs content - check back soon for more updates!

## How Does It Work?

We do a deep dive on how React Redux works in this readthesource episode.
Enjoy!

## License

MIT
