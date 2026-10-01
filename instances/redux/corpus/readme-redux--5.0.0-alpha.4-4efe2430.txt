# redux README 4.2.0-alpha.0 … 5.0.0-alpha.4: <a href='https://redux.js.org'><img src='https://camo.githubusercontent.com/f28b5bc7822f1b7bb28a96d8d09e7d79169248fc/687474703a2f2f692e696d6775722e636f6d2f4a65567164514d2e706e67' height='60' alt='Redux Logo' aria-label='redux.js.org' /></a>
# джерело: https://raw.githubusercontent.com/reduxjs/redux/ad5942c033a6614b3831bdeddd1c4e780e49414a/README.md
# отримано: 2026-10-01
# версія: 5.0.0-alpha.4, 5.0.0-alpha.3, 5.0.0-alpha.2, 5.0.0-alpha.1, 5.0.0-alpha.0, 4.2.0-alpha.0

Redux is a predictable state container for JavaScript apps.
(Not to be confused with a WordPress framework – Redux Framework)

It helps you write applications that behave consistently, run in different environments (client, server, and native), and are easy to test. On top of that, it provides a great developer experience, such as live code editing combined with a time traveling debugger.

You can use Redux together with React, or with any other view library.
It is tiny (2kB, including dependencies), and has a rich ecosystem of addons.

GitHub Workflow Status
npm version
npm downloads
redux channel on discord
Changelog #187

## Installation

**Redux Toolkit** is our official recommended approach for writing Redux logic. It wraps around the Redux core, and contains packages and functions that we think are essential for building a Redux app. Redux Toolkit builds in our suggested best practices, simplifies most Redux tasks, prevents common mistakes, and makes it easier to write Redux applications.

```
npm install @reduxjs/toolkit react-redux
```

For the Redux core library by itself:

```
npm install redux
```

For more details, see the Installation docs page.

## Documentation

The Redux docs are located at **https://redux.js.org**:

- Introduction
- Tutorials
- Usage Guides
- FAQ
- API Reference

## Learn Redux

### Redux Essentials Tutorial

The **Redux Essentials tutorial** is a "top-down" tutorial that teaches "how to use Redux the right way", using our latest recommended APIs and best practices. We recommend starting there.

### Redux Fundamentals Tutorial

The **Redux Fundamentals tutorial** is a "bottom-up" tutorial that teaches "how Redux works" from first principles and without any abstractions, and why standard Redux usage patterns exist.

### Additional Tutorials

- The Redux repository contains several example projects demonstrating various aspects of how to use Redux. Almost all examples have a corresponding CodeSandbox sandbox. This is an interactive version of the code that you can play with online. See the complete list of examples in the **Examples page**.
- Redux creator Dan Abramov's **free "Getting Started with Redux" video series** and **Building React Applications with Idiomatic Redux** video courses on Egghead.io
- Redux maintainer Mark Erikson's **"Redux Fundamentals" conference talk** and **"Redux Fundamentals" workshop slides**
- Dave Ceddia's post **A Complete React Redux Tutorial for Beginners**

### Other Resources

- The **Redux FAQ** answers many common questions about how to use Redux, and the **"Using Redux" docs section** has information on handling derived data, testing, structuring reducer logic, and reducing boilerplate.
- Redux maintainer Mark Erikson's **"Practical Redux" tutorial series** demonstrates real-world intermediate and advanced techniques for working with React and Redux (also available as **an interactive course on Educative.io**).
- The **React/Redux links list** has categorized articles on working with reducers and selectors, managing side effects, Redux architecture and best practices, and more.
- Our community has created thousands of Redux-related libraries, addons, and tools. The **"Ecosystem" docs page** lists our recommendations, and also there's a complete listing available in the **Redux addons catalog**.

### Help and Discussion

The **#redux channel** of the **Reactiflux Discord community** is our official resource for all questions related to learning and using Redux. Reactiflux is a great place to hang out, ask questions, and learn - please come and join us there!

## Before Proceeding Further

Redux is a valuable tool for organizing your state, but you should also consider whether it's appropriate for your situation. Please don't use Redux just because someone said you should - instead, please take some time to understand the potential benefits and tradeoffs of using it.

Here are some suggestions on when it makes sense to use Redux:

- You have reasonable amounts of data changing over time
- You need a single source of truth for your state
- You find that keeping all your state in a top-level component is no longer sufficient

Yes, these guidelines are subjective and vague, but this is for a good reason. The point at which you should integrate Redux into your application is different for every user and different for every application.

> **For more thoughts on how Redux is meant to be used, please see:**
>
> - **When (and when not) to reach for Redux**
> - **You Might Not Need Redux**
> - **The Tao of Redux, Part 1 - Implementation and Intent**
> - **The Tao of Redux, Part 2 - Practice and Philosophy**
> - **Redux FAQ**

## Developer Experience

Dan Abramov (author of Redux) wrote Redux while working on his React Europe talk called “Hot Reloading with Time Travel”. His goal was to create a state management library with a minimal API but completely predictable behavior. Redux makes it possible to implement logging, hot reloading, time travel, universal apps, record and replay, without any buy-in from the developer.

## Influences

Redux evolves the ideas of Flux, but avoids its complexity by taking cues from Elm.
Even if you haven't used Flux or Elm, Redux only takes a few minutes to get started with.

## Basic Example

The whole global state of your app is stored in an object tree inside a single _store_.
The only way to change the state tree is to create an _action_, an object describing what happened, and _dispatch_ it to the store.
To specify how state gets updated in response to an action, you write pure _reducer_ functions that calculate a new state based on the old state and the action.

```js
import { createStore } from 'redux'

/**
 * This is a reducer - a function that takes a current state value and an
 * action object describing "what happened", and returns a new state value.
 * A reducer's function signature is: (state, action) => newState
 *
 * The Redux state should contain only plain JS objects, arrays, and primitives.
 * The root state value is usually an object.  It's important that you should
 * not mutate the state object, but return a new object if the state changes.
 *
 * You can use any conditional logic you want in a reducer. In this example,
 * we use a switch statement, but it's not required.
 */
function counterReducer(state = { value: 0 }, action) {
  switch (action.type) {
    case 'counter/incremented':
      return { value: state.value + 1 }
    case 'counter/decremented':
      return { value: state.value - 1 }
    default:
      return state
  }
}

// Create a Redux store holding the state of your app.
// Its API is { subscribe, dispatch, getState }.
let store = createStore(counterReducer)

// You can use subscribe() to update the UI in response to state changes.
// Normally you'd use a view binding library (e.g. React Redux) rather than subscribe() directly.
// There may be additional use cases where it's helpful to subscribe as well.

store.subscribe(() => console.log(store.getState()))

// The only way to mutate the internal state is to dispatch an action.
// The actions can be serialized, logged or stored and later replayed.
store.dispatch({ type: 'counter/incremented' })
// {value: 1}
store.dispatch({ type: 'counter/incremented' })
// {value: 2}
store.dispatch({ type: 'counter/decremented' })
// {value: 1}
```

Instead of mutating the state directly, you specify the mutations you want to happen with plain objects called _actions_. Then you write a special function called a _reducer_ to decide how every action transforms the entire application's state.

In a typical Redux app, there is just a single store with a single root reducing function. As your app grows, you split the root reducer into smaller reducers independently operating on the different parts of the state tree. This is exactly like how there is just one root component in a React app, but it is composed out of many small components.

This architecture might seem like a lot for a counter app, but the beauty of this pattern is how well it scales to large and complex apps. It also enables very powerful developer tools, because it is possible to trace every mutation to the action that caused it. You can record user sessions and reproduce them just by replaying every action.

### Redux Toolkit Example

Redux Toolkit simplifies the process of writing Redux logic and setting up the store. With Redux Toolkit, that same logic looks like:

```js
import { createSlice, configureStore } from '@reduxjs/toolkit'

const counterSlice = createSlice({
  name: 'counter',
  initialState: {
    value: 0
  },
  reducers: {
    incremented: state => {
      // Redux Toolkit allows us to write "mutating" logic in reducers. It
      // doesn't actually mutate the state because it uses the Immer library,
      // which detects changes to a "draft state" and produces a brand new
      // immutable state based off those changes
      state.value += 1
    },
    decremented: state => {
      state.value -= 1
    }
  }
})

export const { incremented, decremented } = counterSlice.actions

const store = configureStore({
  reducer: counterSlice.reducer
})

// Can still subscribe to the store
store.subscribe(() => console.log(store.getState()))

// Still pass action objects to `dispatch`, but they're created for us
store.dispatch(incremented())
// {value: 1}
store.dispatch(incremented())
// {value: 2}
store.dispatch(decremented())
// {value: 1}
```

Redux Toolkit allows us to write shorter logic that's easier to read, while still following the same Redux behavior and data flow.

## Examples

Almost all examples have a corresponding CodeSandbox sandbox. This is an interactive version of the code that you can play with online.

- **Counter Vanilla**: Source
- **Counter**: Source | Sandbox
- **Todos**: Source | Sandbox
- **Todos with Undo**: Source | Sandbox
- **TodoMVC**: Source | Sandbox
- **Shopping Cart**: Source | Sandbox
- **Tree View**: Source | Sandbox
- **Async**: Source | Sandbox
- **Universal**: Source
- **Real World**: Source | Sandbox

## Testimonials

> “Love what you're doing with Redux”
> Jing Chen, creator of Flux

> “I asked for comments on Redux in FB's internal JS discussion group, and it was universally praised. Really awesome work.”
> Bill Fisher, author of Flux documentation

> “It's cool that you are inventing a better Flux by not doing Flux at all.”
> André Staltz, creator of Cycle

## Thanks

- The Elm Architecture for a great intro to modeling state updates with reducers;
- Turning the database inside-out for blowing my mind;
- Developing ClojureScript with Figwheel for convincing me that re-evaluation should “just work”;
- Webpack for Hot Module Replacement;
- Flummox for teaching me to approach Flux without boilerplate or singletons;
- disto for a proof of concept of hot reloadable Stores;
- NuclearJS for proving this architecture can be performant;
- Om for popularizing the idea of a single state atom;
- Cycle for showing how often a function is the best tool;
- React for the pragmatic innovation.

Special thanks to Jamie Paton for handing over the `redux` NPM package name.

## Logo

You can find the official logo on GitHub.

## Change Log

This project adheres to Semantic Versioning.
Every release, along with the migration instructions, is documented on the GitHub Releases page.

## Patrons

The work on Redux was funded by the community.
Meet some of the outstanding companies that made it possible:

- Webflow
- Ximedes

See the full list of Redux patrons, as well as the always-growing list of people and companies that use Redux.

## License

MIT
