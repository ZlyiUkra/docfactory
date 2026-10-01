# @reduxjs/toolkit README 2.2.0 … 2.11.2: Redux Toolkit
# джерело: https://raw.githubusercontent.com/reduxjs/redux-toolkit/646d54c1f7040342cdaf109ca81a344c88cda9ba/packages/toolkit/README.md
# отримано: 2026-10-01
# версія: 2.11.2, 2.11.1, 2.11.0, 2.10.1, 2.10.0, 2.9.2, 2.9.1, 2.9.0, 2.8.2, 2.8.1, 2.8.0, 2.7.0, 2.6.1, 2.6.0, 2.5.1, 2.5.0, 2.4.0, 2.3.0, 2.2.8, 2.2.7, 2.2.6, 2.2.5, 2.2.4, 2.2.3, 2.2.2, 2.2.1, 2.2.0

GitHub Workflow Status
npm version
npm downloads

**The official, opinionated, batteries-included toolset for efficient Redux development**

## Installation

### Create a React Redux App

The recommended way to start new apps with React and Redux Toolkit is by using our official Redux Toolkit + TS template for Vite, or by creating a new Next.js project using Next's `with-redux` template.

Both of these already have Redux Toolkit and React-Redux configured appropriately for that build tool, and come with a small example app that demonstrates how to use several of Redux Toolkit's features.

```bash
# Vite with our Redux+TS template
# (using the `degit` tool to clone and extract the template)
npx degit reduxjs/redux-templates/packages/vite-template-redux my-app

# Next.js using the `with-redux` template
npx create-next-app --example with-redux my-app
```

We do not currently have official React Native templates, but recommend these templates for standard React Native and for Expo:

- https://github.com/rahsheen/react-native-template-redux-typescript
- https://github.com/rahsheen/expo-template-redux-typescript

### An Existing App

Redux Toolkit is available as a package on NPM for use with a module bundler or in a Node application:

```bash
# NPM
npm install @reduxjs/toolkit

# Yarn
yarn add @reduxjs/toolkit
```

The package includes a precompiled ESM build that can be used as a `<script type="module">` tag directly in the browser.

## Documentation

The Redux Toolkit docs are available at **https://redux-toolkit.js.org**, including API references and usage guides for all of the APIs included in Redux Toolkit.

The Redux core docs at https://redux.js.org includes the full Redux tutorials, as well usage guides on general Redux patterns.

## Purpose

The **Redux Toolkit** package is intended to be the standard way to write Redux logic. It was originally created to help address three common concerns about Redux:

- "Configuring a Redux store is too complicated"
- "I have to add a lot of packages to get Redux to do anything useful"
- "Redux requires too much boilerplate code"

We can't solve every use case, but in the spirit of `create-react-app`, we can try to provide some tools that abstract over the setup process and handle the most common use cases, as well as include some useful utilities that will let the user simplify their application code.

Because of that, this package is deliberately limited in scope. It does _not_ address concepts like "reusable encapsulated Redux modules", folder or file structures, managing entity relationships in the store, and so on.

Redux Toolkit also includes a powerful data fetching and caching capability that we've dubbed "RTK Query". It's included in the package as a separate set of entry points. It's optional, but can eliminate the need to hand-write data fetching logic yourself.

## What's Included

Redux Toolkit includes these APIs:

- `configureStore()`: wraps `createStore` to provide simplified configuration options and good defaults. It can automatically combine your slice reducers, add whatever Redux middleware you supply, includes `redux-thunk` by default, and enables use of the Redux DevTools Extension.
- `createReducer()`: lets you supply a lookup table of action types to case reducer functions, rather than writing switch statements. In addition, it automatically uses the `immer` library to let you write simpler immutable updates with normal mutative code, like `state.todos[3].completed = true`.
- `createAction()`: generates an action creator function for the given action type string. The function itself has `toString()` defined, so that it can be used in place of the type constant.
- `createSlice()`: combines `createReducer()` + `createAction()`. Accepts an object of reducer functions, a slice name, and an initial state value, and automatically generates a slice reducer with corresponding action creators and action types.
- `combineSlices()`: combines multiple slices into a single reducer, and allows "lazy loading" of slices after initialisation.
- `createListenerMiddleware()`: lets you define "listener" entries that contain an "effect" callback with additional logic, and a way to specify when that callback should run based on dispatched actions or state changes. A lightweight alternative to Redux async middleware like sagas and observables.
- `createAsyncThunk()`: accepts an action type string and a function that returns a promise, and generates a thunk that dispatches `pending/resolved/rejected` action types based on that promise
- `createEntityAdapter()`: generates a set of reusable reducers and selectors to manage normalized data in the store
- The `createSelector()` utility from the Reselect library, re-exported for ease of use.

For details, see the Redux Toolkit API Reference section in the docs.

## RTK Query

**RTK Query** is provided as an optional addon within the `@reduxjs/toolkit` package. It is purpose-built to solve the use case of data fetching and caching, supplying a compact, but powerful toolset to define an API interface layer for your app. It is intended to simplify common cases for loading data in a web application, eliminating the need to hand-write data fetching & caching logic yourself.

RTK Query is built on top of the Redux Toolkit core for its implementation, using Redux internally for its architecture. Although knowledge of Redux and RTK are not required to use RTK Query, you should explore all of the additional global store management capabilities they provide, as well as installing the Redux DevTools browser extension, which works flawlessly with RTK Query to traverse and replay a timeline of your request & cache behavior.

RTK Query is included within the installation of the core Redux Toolkit package. It is available via either of the two entry points below:

```ts
import { createApi } from '@reduxjs/toolkit/query'

/* React-specific entry point that automatically generates
   hooks corresponding to the defined endpoints */
import { createApi } from '@reduxjs/toolkit/query/react'
```

### What's included

RTK Query includes these APIs:

- `createApi()`: The core of RTK Query's functionality. It allows you to define a set of endpoints describe how to retrieve data from a series of endpoints, including configuration of how to fetch and transform that data. In most cases, you should use this once per app, with "one API slice per base URL" as a rule of thumb.
- `fetchBaseQuery()`: A small wrapper around fetch that aims to simplify requests. Intended as the recommended baseQuery to be used in createApi for the majority of users.
- `<ApiProvider />`: Can be used as a Provider if you do not already have a Redux store.
- `setupListeners()`: A utility used to enable refetchOnMount and refetchOnReconnect behaviors.

See the **RTK Query Overview** page for more details on what RTK Query is, what problems it solves, and how to use it.

## Contributing

Please refer to our contributing guide to learn about our development process, how to propose bugfixes and improvements, and how to build and test your changes to Redux Toolkit.
