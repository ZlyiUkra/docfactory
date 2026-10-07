# redux README 3.1.0 … 3.2.1: [Redux](http://rackt.github.io/redux)
# джерело: https://raw.githubusercontent.com/reduxjs/redux/0ea221f1f218228bb307194b5e1d57c52ee641ce/README.md
# отримано: 2026-10-01
# версія: 3.2.1, 3.2.0, 3.1.7, 3.1.6, 3.1.5, 3.1.4, 3.1.3, 3.1.2, 3.1.1, 3.1.0

Redux is a predictable state container for JavaScript apps.

It helps you write applications that behave consistently, run in different environments (client, server, and native), and are easy to test. On top of that, it provides a great developer experience, such as live code editing combined with a time traveling debugger.

You can use Redux together with React, or with any other view library.
It is tiny (2kB) and has no dependencies.

build status
npm version
npm downloads
redux channel on discord
#rackt on freenode
Changelog #187

>**New! Learn Redux from its creator:
>Getting Started with Redux (30 free videos)**

### Testimonials

>“Love what you’re doing with Redux”
>Jing Chen, creator of Flux

>“I asked for comments on Redux in FB's internal JS discussion group, and it was universally praised. Really awesome work.”
>Bill Fisher, author of Flux documentation

>“It's cool that you are inventing a better Flux by not doing Flux at all.”
>André Staltz, creator of Cycle

### Developer Experience

I wrote Redux while working on my React Europe talk called “Hot Reloading with Time Travel”. My goal was to create a state management library with minimal API but completely predictable behavior, so it is possible to implement logging, hot reloading, time travel, universal apps, record and replay, without any buy-in from the developer.

### Influences

Redux evolves the ideas of Flux, but avoids its complexity by taking cues from Elm.
Whether you have used them or not, Redux only takes a few minutes to get started with.

### Installation

To install the stable version:

```
npm install --save redux
```

Most likely, you’ll also need the React bindings and the developer tools.

```
npm install --save react-redux
npm install --save-dev redux-devtools
```

This assumes that you’re using npm package manager with a module bundler like Webpack or Browserify to consume CommonJS modules.

If you don’t yet use npm or a modern module bundler, and would rather prefer a single-file UMD build that makes `Redux` available as a global object, you can grab a pre-built version from cdnjs. We *don’t* recommend this approach for any serious application, as most of the libraries complementary to Redux are only available on npm.

### The Gist

The whole state of your app is stored in an object tree inside a single *store*.
The only way to change the state tree is to emit an *action*, an object describing what happened.
To specify how the actions transform the state tree, you write pure *reducers*.

That’s it!

```js
import { createStore } from 'redux'

/**
 * This is a reducer, a pure function with (state, action) => state signature.
 * It describes how an action transforms the state into the next state.
 *
 * The shape of the state is up to you: it can be a primitive, an array, an object,
 * or even an Immutable.js data structure. The only important part is that you should
 * not mutate the state object, but return a new object if the state changes.
 *
 * In this example, we use a `switch` statement and strings, but you can use a helper that
 * follows a different convention (such as function maps) if it makes sense for your project.
 */
function counter(state = 0, action) {
  switch (action.type) {
  case 'INCREMENT':
    return state + 1
  case 'DECREMENT':
    return state - 1
  default:
    return state
  }
}

// Create a Redux store holding the state of your app.
// Its API is { subscribe, dispatch, getState }.
let store = createStore(counter)

// You can subscribe to the updates manually, or use bindings to your view layer.
store.subscribe(() =>
  console.log(store.getState())
)

// The only way to mutate the internal state is to dispatch an action.
// The actions can be serialized, logged or stored and later replayed.
store.dispatch({ type: 'INCREMENT' })
// 1
store.dispatch({ type: 'INCREMENT' })
// 2
store.dispatch({ type: 'DECREMENT' })
// 1
```

Instead of mutating the state directly, you specify the mutations you want to happen with plain objects called *actions*. Then you write a special function called a *reducer* to decide how every action transforms the entire application’s state.

If you’re coming from Flux, there is a single important difference you need to understand. Redux doesn’t have a Dispatcher or support many stores. Instead, there is just a single store with a single root reducing function. As your app grows, instead of adding stores, you split the root reducer into smaller reducers independently operating on the different parts of the state tree. This is exactly like there is just one root component in a React app, but it is composed out of many small components.

This architecture might seem like an overkill for a counter app, but the beauty of this pattern is how well it scales to large and complex apps. It also enables very powerful developer tools, because it is possible to trace every mutation to the action that caused it. You can record user sessions and reproduce them just by replaying every action.

### Learn Redux from Its Creator

Getting Started with Redux is a video course consisting of 30 videos narrated by Dan Abramov, author of Redux. It is designed to complement the “Basics” part of the docs while bringing additional insights about immutability, testing, Redux best practices, and using Redux with React. **This course is free and will always be.**

>“Great course on egghead.io by @dan_abramov - instead of just showing you how to use #redux, it also shows how and why redux was built!”
>Sandrino Di Mattia

>“Plowing through @dan_abramov 'Getting Started with Redux' - its amazing how much simpler concepts get with video.”
>Chris Dhanaraj

>“This video series on Redux by @dan_abramov on @eggheadio is spectacular!”
>Eddie Zaneski

>“Come for the name hype. Stay for the rock solid fundamentals. (Thanks, and great job @dan_abramov and @eggheadio!)”
>Dan

>“This series of videos on Redux by @dan_abramov is repeatedly blowing my mind - gunna do some serious refactoring”
>Laurence Roberts

So, what are you waiting for?

#### Watch the 30 Free Videos!

If you enjoyed my course, consider supporting Egghead by buying a subscription. Subscribers have access to the source code for the example in every one of my videos, as well as to tons of advanced lessons on other topics, including JavaScript in depth, React, Angular, and more. Many Egghead instructors are also open source library authors, so buying a subscription is a nice way to thank them for the work that they’ve done.

### Documentation

* Introduction
* Basics
* Advanced
* Recipes
* Troubleshooting
* Glossary
* API Reference

For PDF, ePub, and MOBI exports for offline reading, and instructions on how to create them, please see: paulkogel/redux-offline-docs.

### Examples

* Counter (source)
* TodoMVC (source)
* Todos with Undo (source)
* Async (source)
* Universal (source)
* Real World (source)
* Shopping Cart (source)
* Tree View (source)

If you’re new to the NPM ecosystem and have troubles getting a project up and running, or aren’t sure where to paste the gist above, check out simplest-redux-example that uses Redux together with React and Browserify.

### Discussion

Join the #redux channel of the Reactiflux Discord community.

### Thanks

* The Elm Architecture for a great intro to modeling state updates with reducers;
* Turning the database inside-out for blowing my mind;
* Developing ClojureScript with Figwheel for convincing me that re-evaluation should “just work”;
* Webpack for Hot Module Replacement;
* Flummox for teaching me to approach Flux without boilerplate or singletons;
* disto for a proof of concept of hot reloadable Stores;
* NuclearJS for proving this architecture can be performant;
* Om for popularizing the idea of a single state atom;
* Cycle for showing how often a function is the best tool;
* React for the pragmatic innovation.

Special thanks to Jamie Paton for handing over the `redux` NPM package name.

### Change Log

This project adheres to Semantic Versioning.
Every release, along with the migration instructions, is documented on the Github Releases page.

### Patrons

The work on Redux was funded by the community.
Meet some of the outstanding companies that made it possible:

* Webflow
* Chess iX

See the full list of Redux patrons.

### License

MIT
