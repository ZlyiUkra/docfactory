# redux-persist README 5.0.0-beta.15 … 5.0.0-rc.4: Redux Persist
# джерело: https://raw.githubusercontent.com/rt2zz/redux-persist/d9c096047b8c4064fb1d461cd1beaee51c7db44f/README.md
# отримано: 2026-10-01
# версія: 5.0.0-rc.4, 5.0.0-rc.3, 5.0.0-rc.2, 5.0.0-beta.16, 5.0.0-beta.15

Persist and rehydrate a redux store.

Redux Persist is performant, easy to implement, and easy to extend.

`npm i redux-persist`

build status
npm version
npm downloads

**Note:** These docs apply to redux-persist v5. v4 will be supported for the forseeable future, and if it works well for your use case you are encouraged to stay on v4.

## Migration from v4 to v5

Standard Usage:
- remove **autoRehydrate**
- changes to **persistStore**:
  - 1. remove config argument (or replace with an empty object)
  - 2. remove all arguments from the callback. If you need state you can call `store.getState()`
- add **persistReducer** to your reducer
  - e.g. `let persistedReducer = persistReducer(config, reducer)`
- changes to **config**:
  - `key` is now required. Can be set to anything, e.g. 'primary'
  - `storage` is now required. For default storage: `import storage from 'redux-persist/lib/storage'`

Recommended Additions
- use new **PersistGate** to delay rendering until rehydration is complete
  - `import { PersistGate } from 'redux-persist/lib/integration/react`
- set `config.debug = true` to get useful logging
- experimental v4 -> v5 state migration

If your implementatation uses getStoredState + createPersistor see alternate migration

## Usage

API Docs
```js
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/es/storage' // default: localStorage if web, AsyncStorage if react-native
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

Redux Persist ships with `createMigrate`, which helps create a synchronous migration for moving from any version of stored state to the current state version. [[Additional information]](./docs/migrations.md)

## Experimental v4 to v5 State Migration

- **warning: this method is completely untested**
- v5 getStoredState is not compatible with v4, so by default v5 will cause all of the persisted state from v4 to disappear on first run
- v5 ships with an experimental v4 -> v5 migration that works by overriding the default getStoredState implementation
**Warning** this is completely untested, please try and report back with any issues.
```js
import getStoredStateMigrateV4 from 'redux-persist/lib/integration/getStoredStateMigratev4'
// ...
persistReducer({
  // ...
  getStoredState: getStoredStateMigrateV4(yourOldV4Config)
}, baseReducer)
```

## Storage Engines

- **localStorage** `import storage from 'redux-persist/lib/storage'`
- **sessionStorage** `import sessionStorage from 'redux-persist/lib/storage/session'`
- **AsyncStorage** react-native `import storage from 'redux-persist/lib/storage'`
- **localForage** recommended for web
- **redux-persist-filesystem-storage** react-native, to mitigate storage size limitations in android (#199, #284)
- **redux-persist-node-storage** for use in nodejs environments.
- **redux-persist-sensitive-storage** react-native, for sensitive information (uses react-native-sensitive-storage).
- **custom** any conforming storage api implementing the following methods: `setItem` `getItem` `removeItem`. (**NB**: These methods must support promises)

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
  (state, key) => specialSerialize(state, key),
  // transform state coming from storage, on its way to be rehydrated into redux
  (state, key) => specialDeserialize(state, key),
  // configuration options
  {whitelist: ['specialKey']}
)

const reducer = persistReducer({transforms: [myTransform]}, baseReducer)
```
