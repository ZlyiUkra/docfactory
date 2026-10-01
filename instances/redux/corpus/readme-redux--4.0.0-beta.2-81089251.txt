# redux README 4.0.0-beta.2: <a href='http://redux.js.org'><img src='https://camo.githubusercontent.com/f28b5bc7822f1b7bb28a96d8d09e7d79169248fc/687474703a2f2f692e696d6775722e636f6d2f4a65567164514d2e706e67' height='60' alt='Redux Logo' aria-label='Redux.js.org' /></a>
# джерело: https://raw.githubusercontent.com/reduxjs/redux/2112d4591809b3dba351389627f36e32694f3407/README.md
# отримано: 2026-10-01
# версія: 4.0.0-beta.2

Redux is a predictable state container for JavaScript apps.
(Not to be confused with a WordPress framework – Redux Framework.)

It helps you write applications that behave consistently, run in different environments (client, server, and native), and are easy to test. On top of that, it provides a great developer experience, such as live code editing combined with a time traveling debugger.

You can use Redux together with React, or with any other view library.
It is tiny (2kB, including dependencies).

build status
npm version
npm downloads
redux channel on discord
#rackt on freenode
Changelog #187

>**Learn Redux from its creator:**
>**Part 1: Getting Started with Redux (30 free videos)**
>**Part 2: Building React Applications with Idiomatic Redux (27 free videos)**

## Testimonials

>“Love what you're doing with Redux”
>Jing Chen, creator of Flux

>“I asked for comments on Redux in FB's internal JS discussion group, and it was universally praised. Really awesome work.”
>Bill Fisher, author of Flux documentation

>“It's cool that you are inventing a better Flux by not doing Flux at all.”
>André Staltz, creator of Cycle

## Before Proceeding Further

>**Also read:**
>**You Might Not Need Redux**

## Developer Experience

I wrote Redux while working on my React Europe talk called “Hot Reloading with Time Travel”. My goal was to create a state management library with minimal API but completely predictable behavior, so it is possible to implement logging, hot reloading, time travel, universal apps, record and replay, without any buy-in from the developer.

## Influences

Redux evolves the ideas of Flux, but avoids its complexity by taking cues from Elm.
Whether you have used them or not, Redux only takes a few minutes to get started with.

## Installation

To install the stable version:

```
npm install --save redux
```

This assumes you are using npm as your package manager.

If you're not, you can access these files on unpkg, download them, or point your package manager to them.

Most commonly people consume Redux as a collection of CommonJS modules. These modules are what you get when you import `redux` in a Webpack, Browserify, or a Node environment. If you like to live on the edge and use Rollup, we support that as well.

If you don't use a module bundler, it's also fine. The `redux` npm package includes precompiled production and development UMD builds in the `dist` folder. They can be used directly without a bundler and are thus compatible with many popular JavaScript module loaders and environments. For example, you can drop a UMD build as a `<script>` tag on the page, or tell Bower to install it. The UMD builds make Redux available as a `window.Redux` global variable.

The Redux source code is written in ES2015 but we precompile both CommonJS and UMD builds to ES5 so they work in any modern browser. You don't need to use Babel or a module bundler to get started with Redux.

### Complementary Packages

Most likely, you'll also need the React bindings and the developer tools.

```
npm install --save react-redux
npm install --save-dev redux-devtools
```

Note that unlike Redux itself, many packages in the Redux ecosystem don't provide UMD builds, so we recommend using CommonJS module bundlers like Webpack and Browserify for the most comfortable development experience.

## The Gist

The whole state of your app is stored in an object tree inside a single *store*.
The only way to change the state tree is to emit an *action*, an object describing what happened.
To specify how the actions transform the state tree, you write pure *reducers*.

That's it!

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
 * follows a different convention (such as function maps) if it makes sense for your
 * project.
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

// You can use subscribe() to update the UI in response to state changes.
// Normally you'd use a view binding library (e.g. React Redux) rather than subscribe() directly.
// However it can also be handy to persist the current state in the localStorage.

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

Instead of mutating the state directly, you specify the mutations you want to happen with plain objects called *actions*. Then you write a special function called a *reducer* to decide how every action transforms the entire application's state.

If you're coming from Flux, there is a single important difference you need to understand. Redux doesn't have a Dispatcher or support many stores. Instead, there is just a single store with a single root reducing function. As your app grows, instead of adding stores, you split the root reducer into smaller reducers independently operating on the different parts of the state tree. This is exactly like how there is just one root component in a React app, but it is composed out of many small components.

This architecture might seem like an overkill for a counter app, but the beauty of this pattern is how well it scales to large and complex apps. It also enables very powerful developer tools, because it is possible to trace every mutation to the action that caused it. You can record user sessions and reproduce them just by replaying every action.

## Learn Redux from Its Creator

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

### Watch the 30 Free Videos!

If you enjoyed my course, consider supporting Egghead by buying a subscription. Subscribers have access to the source code of every example in my videos and tons of advanced lessons on other topics, including JavaScript in depth, React, Angular, and more. Many Egghead instructors are also open source library authors, so buying a subscription is a nice way to thank them for the work that they've done.

## Documentation

* Introduction
* Basics
* Advanced
* Recipes
* FAQ
* Troubleshooting
* Glossary
* API Reference

For PDF, ePub, and MOBI exports for offline reading, and instructions on how to create them, please see: paulkogel/redux-offline-docs.

For Offline docs, please see: devdocs

## Examples

Almost all examples have a corresponding CodeSandbox sandbox. This is an interactive version of the code that you can play with online.

* Counter Vanilla (source)
* Counter (source, sandbox)
* Todos (source, sandbox)
* Todos with Undo (source, sandbox)
* TodoMVC (source, sandbox)
* Shopping Cart (source, sandbox)
* Tree View (source, sandbox)
* Async (source, sandbox)
* Universal (source)
* Real World (source, sandbox)

If you're new to the NPM ecosystem and have troubles getting a project up and running, or aren't sure where to paste the gist above, check out simplest-redux-example that uses Redux together with React and Browserify.

## Discussion

Join the #redux channel of the Reactiflux Discord community.

## Thanks

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

## Logo

You can find the official logo on GitHub.

## Change Log

This project adheres to Semantic Versioning.
Every release, along with the migration instructions, is documented on the Github Releases page.

## Patrons

The work on Redux was funded by the community.
Meet some of the outstanding companies that made it possible:

* Webflow
* Ximedes

See the full list of Redux patrons, as well as the always-growing list of people and companies that use Redux.

## License

MIT
