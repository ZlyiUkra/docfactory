# redux README 1.0.1: [Redux](http://rackt.github.io/redux)
# джерело: https://raw.githubusercontent.com/reduxjs/redux/7cf753f428ad70c04acd2648e7f329ee578f4fdd/README.md
# отримано: 2026-10-01
# версія: 1.0.1

Redux is a predictable state container for JavaScript apps.

It helps you write applications that behave consistently, run in different environments (client, server, and native), and are easy to test. On top of that, it provides a great developer experience, such as live code editing combined with a time traveling debugger.

You can use Redux together with React, or with any other view library.
It is tiny (2kB) and has no dependencies.

build status
npm version
npm downloads
redux channel on slack

### Testimonials

>“Love what you’re doing with Redux”
>Jing Chen, creator of Flux

>“I asked for comments on Redux in FB's internal JS discussion group, and it was universally praised. Really awesome work.”
>Bill Fisher, creator of Flux

>“It's cool that you are inventing a better Flux by not doing Flux at all.”
>André Staltz, creator of Cycle

### Developer Experience

I wrote Redux while working on my React Europe talk called “Hot Reloading with Time Travel”. My goal was to create a state management library with minimal API but completely predictable behavior, so it is possible to implement logging, hot reloading, time travel, universal apps, record and replay, without any buy-in from the developer.

### Influences

Redux evolves the ideas of Flux, but avoids its complexity by taking cues from Elm.
Whether you used them or not, Redux takes a few minutes to get started with.

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

### The Gist

The whole state of your app is stored in an object tree inside a single *store*.
The only way to change the state tree is to emit an *action*, an object describing what happened.
To specify how the actions transform the state tree, you write pure *reducers*.

That’s it!

```js
import { createStore } from 'redux';

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
    return state + 1;
  case 'DECREMENT':
    return state - 1;
  default:
    return state;
  }
}

// Create a Redux store holding the state of your app.
// Its API is { subscribe, dispatch, getState }.
let store = createStore(counter);

// You can subscribe to the updates manually, or use bindings to your view layer.
store.subscribe(() =>
  console.log(store.getState())
);

// The only way to mutate the internal state is to dispatch an action.
// The actions can be serialized, logged or stored and later replayed.
store.dispatch({ type: 'INCREMENT' });
// 1
store.dispatch({ type: 'INCREMENT' });
// 2
store.dispatch({ type: 'DECREMENT' });
// 1
```

Instead of mutating the state directly, you specify the mutations you want to happen with plain objects called *actions*. Then you write a special function called a *reducer* to decide how every action transforms the entire application’s state.

If you’re coming from Flux, there is a single important difference you need to understand. Redux doesn’t have a Dispatcher or support many stores. Instead, there is just a single store with a single root reducing function. As your app grows, instead of adding stores, you split the root reducer into smaller reducers independently operating on the different parts of the state tree. This is exactly like there is just one root component in a React app, but it is composed out of many small components.

This architecture might seem like an overkill for a counter app, but the beauty of this pattern is how well it scales to large and complex apps. It also enables very powerful developer tools, because it is possible to trace every mutation to the action that caused it. You can record user sessions and reproduce them just by replaying every action.

### Documentation

* Introduction
* Basics
* Advanced
* Recipes
* Troubleshooting
* Glossary
* API Reference

### Examples

* Counter (source)
* TodoMVC (source)
* Async (source)
* Real World (source)

### Discussion

Join the **#redux** channel of the Reactiflux Slack community.

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

### Patrons

The work on Redux was funded by the community.
Meet some of the outstanding companies that made it possible:

* Webflow
* Chess iX

See the full list of Redux patrons.

### License

MIT
