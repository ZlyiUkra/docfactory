# @reduxjs/toolkit README 1.1.0: Redux Toolkit
# джерело: https://raw.githubusercontent.com/reduxjs/redux-toolkit/1eed13a520410a3ede49eb62dcc234831a4e9f9b/README.md
# отримано: 2026-10-01
# версія: 1.1.0

build status
npm version
npm downloads
npm downloads

**The official, opinionated, batteries-included toolset for efficient Redux development**

`npm install @reduxjs/toolkit`

(Formerly known as "Redux Starter Kit")

### Purpose

The **Redux Toolkit** package is intended to be the standard way to write Redux logic. It was originally created to help address three common concerns about Redux:

- "Configuring a Redux store is too complicated"
- "I have to add a lot of packages to get Redux to do anything useful"
- "Redux requires too much boilerplate code"

We can't solve every use case, but in the spirit of `create-react-app` and `apollo-boost`, we can try to provide some tools that abstract over the setup process and handle the most common use cases, as well as include some useful utilities that will let the user simplify their application code.

This package is _not_ intended to solve every possible use case for Redux, and is deliberately limited in scope. It does _not_ address concepts like "reusable encapsulated Redux modules", data fetching, folder or file structures, managing entity relationships in the store, and so on.

### What's Included

Redux Toolkit includes:

- A `configureStore()` function with simplified configuration options. It can automatically combine your slice reducers, adds whatever Redux middleware you supply, includes `redux-thunk` by default, and enables use of the Redux DevTools Extension.
- A `createReducer()` utility that lets you supply a lookup table of action types to case reducer functions, rather than writing switch statements. In addition, it automatically uses the `immer` library to let you write simpler immutable updates with normal mutative code, like `state.todos[3].completed = true`.
- A `createAction()` utility that returns an action creator function for the given action type string. The function itself has `toString()` defined, so that it can be used in place of the type constant.
- A `createSlice()` function that accepts a set of reducer functions, a slice name, and an initial state value, and automatically generates corresponding action creators, types, and simple selector functions.
- The `createSelector` utility from the Reselect library, re-exported for ease of use.

## Documentation

The Redux Toolkit docs are available at **https://redux-toolkit.js.org**.
