# react-redux README 4.4.2 … 4.4.5: React Redux
# джерело: https://raw.githubusercontent.com/reduxjs/react-redux/e06a0a730490dddc669157bff2d751bce987681b/README.md
# отримано: 2026-10-01
# версія: 4.4.5, 4.4.4, 4.4.3, 4.4.2

Official React bindings for Redux.
Performant and flexible.

build status npm version
npm downloads
redux channel on slack

## Installation

React Redux requires **React 0.14 or later.**

```
npm install --save react-redux
```

This assumes that you’re using npm package manager with a module bundler like Webpack or Browserify to consume CommonJS modules.

If you don’t yet use npm or a modern module bundler, and would rather prefer a single-file UMD build that makes `ReactRedux` available as a global object, you can grab a pre-built version from cdnjs. We *don’t* recommend this approach for any serious application, as most of the libraries complementary to Redux are only available on npm.

## React Native

As of React Native 0.18, React Redux 4.x should work with React Native. If you have any issues with React Redux 4.x on React Native, run `npm ls react` and make sure you don’t have a duplicate React installation in your `node_modules`. We recommend that you use `npm@3.x` which is better at avoiding this sort of issues.

If you are on an older version of React Native, you’ll need to keep using React Redux 3.x branch and documentation because of this problem.

## Documentation

- Redux: Usage with React
- API
  - `<Provider store>`
  - [`connect([mapStateToProps], [mapDispatchToProps], [mergeProps], [options])`](docs/api.md#connectmapstatetoprops-mapdispatchtoprops-mergeprops-options)
- Troubleshooting

## How Does It Work?

We do a deep dive on how React Redux works in this readthesource episode.
Enjoy!

## License

MIT
