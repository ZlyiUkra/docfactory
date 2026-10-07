# redux-saga README 1.2.0 … 1.2.2
# джерело: https://raw.githubusercontent.com/redux-saga/redux-saga/4ebb5930303b0a27b8ce91241afa6972dadad018/README.md
# отримано: 2026-10-01
# версія: 1.2.2, 1.2.1, 1.2.0

## redux-saga

npm version
CDNJS
npm
Build Status
Join the chat at https://gitter.im/yelouafi/redux-saga
OpenCollective
OpenCollective

`redux-saga` is a library that aims to make application side effects (i.e. asynchronous things like data fetching and impure things like accessing the browser cache) easier to manage, more efficient to execute, easy to test, and better at handling failures.

The mental model is that a saga is like a separate thread in your application that's solely responsible for side effects. `redux-saga` is a redux middleware, which means this thread can be started, paused and cancelled from the main application with normal redux actions, it has access to the full redux application state and it can dispatch redux actions as well.

It uses an ES6 feature called Generators to make those asynchronous flows easy to read, write and test. _(if you're not familiar with them here are some introductory links)_ By doing so, these asynchronous flows look like your standard synchronous JavaScript code. (kind of like `async`/`await`, but generators have a few more awesome features we need)

You might've used `redux-thunk` before to handle your data fetching. Contrary to redux thunk, you don't end up in callback hell, you can test your asynchronous flows easily and your actions stay pure.

## Getting started

## Install

```sh
$ npm install redux-saga
```

or

```sh
$ yarn add redux-saga
```

Alternatively, you may use the provided UMD builds directly in the `<script>` tag of an HTML page. See this section.

## Usage Example

Suppose we have a UI to fetch some user data from a remote server when a button is clicked. (For brevity, we'll just show the action triggering code.)

```javascript
class UserComponent extends React.Component {
  ...
  onSomeButtonClicked() {
    const { userId, dispatch } = this.props
    dispatch({type: 'USER_FETCH_REQUESTED', payload: {userId}})
  }
  ...
}
```

The Component dispatches a plain Object action to the Store. We'll create a Saga that watches for all `USER_FETCH_REQUESTED` actions and triggers an API call to fetch the user data.

#### `sagas.js`

```javascript
import { call, put, takeEvery, takeLatest } from 'redux-saga/effects'
import Api from '...'

// worker Saga: will be fired on USER_FETCH_REQUESTED actions
function* fetchUser(action) {
  try {
    const user = yield call(Api.fetchUser, action.payload.userId)
    yield put({ type: 'USER_FETCH_SUCCEEDED', user: user })
  } catch (e) {
    yield put({ type: 'USER_FETCH_FAILED', message: e.message })
  }
}

/*
  Starts fetchUser on each dispatched `USER_FETCH_REQUESTED` action.
  Allows concurrent fetches of user.
*/
function* mySaga() {
  yield takeEvery('USER_FETCH_REQUESTED', fetchUser)
}

/*
  Alternatively you may use takeLatest.

  Does not allow concurrent fetches of user. If "USER_FETCH_REQUESTED" gets
  dispatched while a fetch is already pending, that pending fetch is cancelled
  and only the latest one will be run.
*/
function* mySaga() {
  yield takeLatest('USER_FETCH_REQUESTED', fetchUser)
}

export default mySaga
```

To run our Saga, we'll have to connect it to the Redux Store using the `redux-saga` middleware.

#### `main.js`

```javascript
import { createStore, applyMiddleware } from 'redux'
import createSagaMiddleware from 'redux-saga'

import reducer from './reducers'
import mySaga from './sagas'

// create the saga middleware
const sagaMiddleware = createSagaMiddleware()
// mount it on the Store
const store = createStore(reducer, applyMiddleware(sagaMiddleware))

// then run the saga
sagaMiddleware.run(mySaga)

// render the application
```

## Documentation

- Introduction
- Basic Concepts
- Advanced Concepts
- Recipes
- External Resources
- Troubleshooting
- Glossary
- API Reference

## Translation

- Chinese
- Traditional Chinese
- Japanese
- Korean
- Portuguese
- Russian

## Using umd build in the browser

There is also a **umd** build of `redux-saga` available in the `dist/` folder. When using the umd build `redux-saga` is available as `ReduxSaga` in the window object. This enables you to create Saga middleware without using ES6 `import` syntax like this:

```javascript
var sagaMiddleware = ReduxSaga.default()
```

The umd version is useful if you don't use Webpack or Browserify. You can access it directly from unpkg.

The following builds are available:

- https://unpkg.com/redux-saga/dist/redux-saga.umd.js
- https://unpkg.com/redux-saga/dist/redux-saga.umd.min.js

**Important!** If the browser you are targeting doesn't support _ES2015 generators_, you must transpile them (i.e. with babel plugin) and provide a valid runtime, such as the one here. The runtime must be imported before **redux-saga**:

```javascript
import 'regenerator-runtime/runtime'
// then
import sagaMiddleware from 'redux-saga'
```

## Building examples from sources

```sh
$ git clone https://github.com/redux-saga/redux-saga.git
$ cd redux-saga
$ yarn
$ npm test
```

Below are the examples ported (so far) from the Redux repos.

### Counter examples

There are three counter examples.

#### counter-vanilla

Demo using vanilla JavaScript and UMD builds. All source is inlined in `index.html`.

To launch the example, open `index.html` in your browser.

> Important: your browser must support Generators. Latest versions of Chrome/Firefox/Edge are suitable.

#### counter

Demo using `webpack` and high-level API `takeEvery`.

```sh
$ npm run counter

# test sample for the generator
$ npm run test-counter
```

#### cancellable-counter

Demo using low-level API to demonstrate task cancellation.

```sh
$ npm run cancellable-counter
```

### Shopping Cart example

```sh
$ npm run shop

# test sample for the generator
$ npm run test-shop
```

### async example

```sh
$ npm run async

# test sample for the generators
$ npm run test-async
```

### real-world example (with webpack hot reloading)

```sh
$ npm run real-world

# sorry, no tests yet
```

### TypeScript

Redux-Saga with TypeScript requires `DOM.Iterable` or `ES2015.Iterable`. If your `target` is `ES6`, you are likely already set, however, for `ES5`, you will need to add it yourself.
Check your `tsconfig.json` file, and the official compiler options documentation.

### Logo

You can find the official Redux-Saga logo with different flavors in the logo directory.

## Redux Saga chooses generators over `async/await`

A few issues have been raised asking whether Redux saga plans to use `async/await` syntax instead of generators.

We will continue to use generators. The primary mechanism of `async/await` is Promises and it is very difficult to retain the scheduling simplicity and semantics of existing Saga concepts using Promises. `async/await` simply don't allow for certain things - like i.e. cancellation. With generators we have full power over how & when effects are executed.

## Backers

Support us with a monthly donation and help us continue our activities. \[Become a backer\]

### Sponsors

Become a sponsor and get your logo on our README on Github with a link to your site. \[Become a sponsor\]

## License

Copyright (c) 2015 Yassine Elouafi.

Licensed under The MIT License (MIT).
