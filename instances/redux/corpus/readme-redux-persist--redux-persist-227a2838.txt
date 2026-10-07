# redux-persist README 5.0.0-beta.2: Redux Persist
# джерело: https://raw.githubusercontent.com/rt2zz/redux-persist/1510601a1fbaa487c6966e34dfc1baad3a79ca53/README.md
# отримано: 2026-10-01
# версія: 5.0.0-beta.2

Persist and rehydrate a redux store.

Redux Persist is performant, easy to implement, and easy to extend.

`npm i redux-persist`

build status
npm version
npm downloads

**Note:** These docs apply to redux-persist v5. v4 will be supported for the forseeable future, and if it works well for your use case you are encouraged to stay on v4.

## Migration from v4 to v5

Standard Usage:
- remove `autoRehydrate`
- changes to `persistStore`:
  - 1. remove config (or replace with an empty object)
  - 2. remove all arguments from the callback. If you need state you can call `store.getState()`
- add `persistReducer` to your reducer
  - e.g. `let persistedReducer = persistReducer(config, reducer)`
- changes to `config`:
  - `key` is now required. Can be set to anything, e.g. 'primary'
  - `storage` is now required. For default web storage: `import storage from 'redux-persist/lib/storage'`

Recommended Additions
- use new PersistGate to delay rendering until rehydration is complete
  - `import { PersistGate } from 'redux-persist/lib/integration/react`
- set `config.debug = true` to get useful logging

If your implementatation uses getStoredState + createPersistor see alternate migration

## Usage

API Docs
```js
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/es/storage'
import rootReducer from './rootReducer'

const config = {
  key: 'root', // key is required
  storage, // storage is now required
}

const reducer = persistReducer(config, rootReducer)

function configureStore () {
  // ...
  let store = createStore(reducer)
  let persistor = persistStore(store)

  return { persistor, store }
}
```

## Breaking Changes

There are two important breaking changes.
1. api has changed as described in the above migration section
2. state with cycles is no longer serialized using json-stringify-safe, and will instead noop.
3. state methods can no longer be overridden which means all top level state needs to be plain objects. `redux-persist-transform-immutable` will continue to operate as before as it works on substate, not top level state.

## Why v5

Long story short, the changes are required in order to support new use cases
- code splitting reducers
- easier to ship persist support inside of other libs (e.g. redux-offline)
- ability to colocate persistence rules with the reducer it pertains to
- first class migration support
- enable PersistGate react component which blocks rendering until persistence is complete (and enables similar patterns for integration)
- possible to nest persistence
- gaurantee consistent state atoms
- better debugability and extensibility

## Migrations

`persistReducer` has a general purpose "migrate" config which will be called after getting stored state but before actually reconciling with the reducer. It can be any function which takes state as an argument and returns a promise to return a new state object.

Redux Persist ships with `createMigrate`, which helps create a synchronous migration for moving from any version of stored state to the current state version.

## Storage Engines

- **localStorage** (default) web
- **sessionStorage**
- **localForage** (recommended) web, see usage below
- **AsyncStorage** for react-native
- **redux-persist-filesystem-storage** for use in react-native Android to mitigate storage size limitations (#199, 284)
- **redux-persist-node-storage** for use in nodejs environments.
- **custom** any conforming storage api implementing the following methods: `setItem` `getItem` `removeItem` `getAllKeys`. (**NB**: These methods must support callbacks, not promises.) [example]

## Transforms

Transforms allow for arbitrary state transforms before saving and during rehydration.
- immutable - support immutable reducers
- compress - compress your serialized state with lz-string
- encrypt - encrypt your serialized state with AES
- filter - store or load a subset of your state
- filter-immutable - store or load a subset of your state with support for immutablejs
- expire - expire a specific subset of your state based on a property
- custom transforms:
```js
import { createTransform, persistReducer } from 'redux-persist'

let myTransform = createTransform(
  // transform state coming from redux on its way to being serialized and stored
  (inboundState, key) => specialSerialize(inboundState, key),
  // transform state coming from storage, on its way to be rehydrated into redux
  (outboundState, key) => specialDeserialize(outboundState, key),
  // configuration options
  {whitelist: ['specialKey']}
)

const reducer = persistReducer({transforms: [myTransform]}, baseReducer)
```
