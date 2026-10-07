# react-redux README 4.3.0 … 4.4.0: React Redux
# джерело: https://raw.githubusercontent.com/reduxjs/react-redux/9c50ae13b84a9fe1702190a94bf900e4ffa32a26/README.md
# отримано: 2026-10-01
# версія: 4.4.0, 4.3.0

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

Until React Native works on top of React instead of shipping a fork of React, you’ll need to keep using React Redux 3.x branch and documentation.

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
