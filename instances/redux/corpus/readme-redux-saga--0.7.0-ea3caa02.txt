# redux-saga README 0.7.0: redux-saga
# джерело: https://raw.githubusercontent.com/redux-saga/redux-saga/25a64f353229408edfc9dd35c5d695d37a77f5b7/README.md
# отримано: 2026-10-01
# версія: 0.7.0

npm version

An alternative Side Effect model for Redux applications. Instead of dispatching thunks
which get handled by the redux-thunk middleware, you create *Sagas* to gather all your
Side Effects logic in a central place.

This means the logic of the application lives in 2 places:

- Reducers are responsible for handling state transitions between actions

- Sagas are responsible for orchestrating complex/asynchronous operations.

Sagas are created using Generator functions.

> As you'll see in the docs, Generators, while seemingly more low-level than ES7 async
functions, allow some features like declarative effects and cancellation which are harder—if not
impossible—to implement with simple async functions.

What this middleware proposes is:

- A composable abstraction **Effect**: waiting for an action, triggering state updates (by dispatching
  actions to the store), and calling a remote service are all different forms of Effects. A Saga composes those
  Effects using familiar control flow constructs (if, while, for, try/catch).

- The Saga is itself an Effect. It can be combined with other Effects using combinators.
It can also be called from inside other Sagas, providing the full power of Subroutines and
Structured Programming

- Effects may be yielded declaratively. You yield a description of the Effect which will be
executed by the middleware. This makes your operational logic inside Generators fully testable.

- You can implement complex operations with logic that spans across multiple actions (e.g. User onboarding, wizard
dialogs, complex Game rules, etc.), which are non-trivial to express using other effects middlewares.

## Install

```
npm install redux-saga
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

## Using umd build in the browser

There's also an **umd** build of `redux-saga` available in the `dist/` folder. When using the umd build
`redux-saga` is available as `ReduxSaga` in the window object.

The umd version is useful if you don't use Webpack or Browserify. You can access it directly from npmcdn.

The following builds are available:

- https://npmcdn.com/redux-saga/dist/redux-saga.js
- https://npmcdn.com/redux-saga/dist/redux-saga.min.js

**Important!** If the browser you are targeting doesn't support _es2015 generators_ you must provide a valid polyfill,
for example the one provided by *babel*:
browser-polyfill.min.js.
The polyfill must be imported before **redux-saga**.

```javascript
import 'babel-polyfill'
// then
import sagaMiddleware from 'redux-saga'
```

## Building examples from sources

```
git clone https://github.com/yelouafi/redux-saga.git
cd redux-saga
npm install
npm test
```

Below are the examples ported (so far) from the Redux repos

### Counter example

```
npm run counter

// test sample for the generator
npm run test-counter
```

### Shopping Cart example

```
npm run shop

// test sample for the generator
npm run test-shop
```

### async example

```
npm run async

//sorry, no tests yet
```

### real-world example (with webpack hot reloading)

```
cd examples/real-world
npm install
npm start
```
