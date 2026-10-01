# @reduxjs/toolkit README 1.6.0: Redux Toolkit
# джерело: https://raw.githubusercontent.com/reduxjs/redux-toolkit/8910a6153df6e7aeaccf533b87924e2307a8fd71/README.md
# отримано: 2026-10-01
# версія: 1.6.0

GitHub Workflow Status
npm version
npm downloads

**The official, opinionated, batteries-included toolset for efficient Redux development**

(Formerly known as "Redux Starter Kit")

## Installation

### Using Create React App

The recommended way to start new apps with React and Redux Toolkit is by using the official Redux+JS template for Create React App, which takes advantage of React Redux's integration with React components.

```sh
npx create-react-app my-app --template redux
```

Or if you are a TypeScript user, use cra-template-redux-typescript, which is based on that template

```sh
npx create-react-app my-app --template redux-typescript
```

### An Existing App

Redux Toolkit is available as a package on NPM for use with a module bundler or in a Node application:

```bash
# NPM
npm install @reduxjs/toolkit

# Yarn
yarn add @reduxjs/toolkit
```

It is also available as a precompiled UMD package that defines a `window.RTK` global variable.
The UMD package can be used as a `<script>` tag directly.

## Purpose

The **Redux Toolkit** package is intended to be the standard way to write Redux logic. It was originally created to help address three common concerns about Redux:

- "Configuring a Redux store is too complicated"
- "I have to add a lot of packages to get Redux to do anything useful"
- "Redux requires too much boilerplate code"

We can't solve every use case, but in the spirit of `create-react-app` and `apollo-boost`, we can try to provide some tools that abstract over the setup process and handle the most common use cases, as well as include some useful utilities that will let the user simplify their application code.

Because of that, this package is deliberately limited in scope. It does _not_ address concepts like "reusable encapsulated Redux modules", data caching, folder or file structures, managing entity relationships in the store, and so on.

## What's Included

Redux Toolkit includes these APIs:

- `configureStore()`: wraps `createStore` to provide simplified configuration options and good defaults. It can automatically combine your slice reducers, adds whatever Redux middleware you supply, includes `redux-thunk` by default, and enables use of the Redux DevTools Extension.
- `createReducer()`: that lets you supply a lookup table of action types to case reducer functions, rather than writing switch statements. In addition, it automatically uses the `immer` library to let you write simpler immutable updates with normal mutative code, like `state.todos[3].completed = true`.
- `createAction()`: generates an action creator function for the given action type string. The function itself has `toString()` defined, so that it can be used in place of the type constant.
- `createSlice()`: accepts an object of reducer functions, a slice name, and an initial state value, and automatically generates a slice reducer with corresponding action creators and action types.
- `createAsyncThunk`: accepts an action type string and a function that returns a promise, and generates a thunk that dispatches `pending/resolved/rejected` action types based on that promise
- `createEntityAdapter`: generates a set of reusable reducers and selectors to manage normalized data in the store
- The `createSelector` utility from the Reselect library, re-exported for ease of use.

## Documentation

The Redux Toolkit docs are available at **https://redux-toolkit.js.org**.
