# redux-persist README 5.6.1 … 5.6.5: Redux Persist
# джерело: https://raw.githubusercontent.com/rt2zz/redux-persist/d768b1639341e4c451b96c258e2df77a07cea4ea/README.md
# отримано: 2026-10-01
# версія: 5.6.5, 5.6.4, 5.6.3, 5.6.2, 5.6.1

Persist and rehydrate a redux store.

build status npm version npm downloads

Redux Persist takes your redux state object and saves it to persisted storage. On app launch, it retrieves this persisted state and saves it back to redux.

**Note:** These instructions are for redux-persist v5. For a list of breaking changes between v4 and v5, see our migration guide.
v4 will be supported for the forseeable future, and if it works well for your use case you are encouraged to stay on v4.

## Quickstart

`npm install redux-persist`

#### Usage

Basic implementation involves adding `persistReducer` and `persistStore` to your setup. **IMPORTANT** Every app needs to decide how many levels of state they want to "merge". The default is 1 level. Please read through the state reconciler docs for more information.

```js
// configureStore.js

import { createStore } from 'redux'
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'

import rootReducer from './reducers'

const persistConfig = {
  key: 'root',
  storage: storage,
}

const persistedReducer = persistReducer(persistConfig, rootReducer)

export default () => {
  let store = createStore(persistedReducer)
  let persistor = persistStore(store)
  return { store, persistor }
}
```

If you are using react, wrap your root component with PersistGate. This delays the rendering of your app's UI until your persisted state has been retrieved and saved to redux. **NOTE** the `PersistGate` loading prop can be null, or any react instance, e.g. `loading={<Loading />}`

```js
import React from 'react'
import { Provider } from 'react-redux'
import { PersistGate } from 'redux-persist/lib/integration/react'

import configureStore from './store/configureStore'
let { store, persistor } = configureStore()

// import your necessary custom components.
import { RootComponent } from './components'

const App = () => {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <RootComponent />
      </PersistGate>
    </Provider>
  );
};

export default App
```

## API

Full API

#### `persistReducer(config, reducer)`

  - arguments
    - **config** *object*
      - required config: `key, storage`
      - notable other config: `whitelist, blacklist, version, stateReconciler, debug`
    - **reducer** *function*
      - any reducer will work, typically this would be the top level reducer returned by `combineReducers`
  - returns an enhanced reducer

#### `persistStore(store, [config, callback])`

  - arguments
    - **config** *persist config* The store to be persisted.
    - **config** *object* (typically null)
    - **callback** *function* will be called after rehydration is finished.
  - returns **persistor** object

#### `persistor object`

  - the persistor object is returned by persistStore with the following methods:
    - `.purge(keys)`
      - purges state from disk and returns a promise
    - `flush()`
      - immediately writes all pending state to disk and returns a promise
    - `pause()`
      - pauses persistence
    - `persist()`
      - resumes persistence

## State Reconciler

State reconcilers define how incoming persisted state is merged in with existing default state. It is critical to choose the right state reconciler for your state shape. There are three options that ship out of the box, lets look at how each operates:

1. hardSet (`import hardSet from 'redux-persist/lib/stateReconciler/hardSet'`)
This will hard set incoming state. This can be desirable in some cases where persistReducer is nested deeper in your reducer tree, or if you do not rely on initialState in your reducer.
   - **INCOMING STATE**: `{ foo: incomingFoo }`
   - **INITIAL STATE**: `{ foo: initialFoo, bar: initialBar }`
   - **RECONCILED STATE**: `{ foo: incomingFoo }` // note bar has been dropped
2. autoMergeLevel1 (default)
This will auto merge one level deep. Auto merge means if the some piece of substate was modified by your reducer during the REHYDRATE action, it will skip this piece of state. Level 1 means it will shallow merge 1 level deep.
   - **INCOMING STATE**: `{ foo: incomingFoo }`
   - **INITIAL STATE**: `{ foo: initialFoo, bar: initialBar }`
   - **RECONCILED STATE**: `{ foo: incomingFoo, bar: initialBar }`
3. autoMergeLevel2
This acts just like autoMergeLevel1, except it shallow merges two levels
   - **INCOMING STATE**: `{ foo: incomingFoo }`
   - **INITIAL STATE**: `{ foo: initialFoo, bar: initialBar }`
   - **RECONCILED STATE**: `{ foo: mergedFoo, bar: initialBar }`

#### Example

```js
import hardSet from 'redux-persist/lib/stateReconciler/hardSet'

const persistConfig = {
  key: 'root',
  storage,
  stateReconciler: hardSet,
}
```

## Blacklist & Whitelist

By Example:
```js
// BLACKLIST
const persistConfig = {
  key: 'root',
  storage: storage,
  blacklist: ['navigation'] // navigation will not be persisted
};

// WHITELIST
const persistConfig = {
  key: 'root',
  storage: storage,
  whitelist: ['navigation'] // only navigation will be persisted
};
```

#### Nested Blacklist / Whitelist

The blacklist and whitelist only work one level deep. However persisted reducers can be nested.For example, if you want to blacklist `state.auth.somethingTemporary`:
```js
import { combineReducers } from 'redux'
import { persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'

import { authReducer, otherReducer } from './reducers'

const rootPersistConfig = {
  key: 'root',
  storage: storage,
  blacklist: ['auth']
}

const authPersistConfig = {
  key: 'auth',
  storage: storage,
  blacklist: ['somethingTemporary']
}

const rootReducer = combineReducers({
  auth: persistReducer(authPersistConfig, authReducer),
  other: otherReducer,
})

export default persistReducer(rootPersistConfig, rootReducer)
```

## Migrations

`persistReducer` has a general purpose "migrate" config which will be called after getting stored state but before actually reconciling with the reducer. It can be any function which takes state as an argument and returns a promise to return a new state object.

Redux Persist ships with `createMigrate`, which helps create a synchronous migration for moving from any version of stored state to the current state version. [[Additional information]](./docs/migrations.md)

## Transforms

Transforms allow you to customize the state object that gets persisted and rehydrated.

There are several libraries that tackle some of the common implementations for transforms.
- immutable - support immutable reducers
- compress - compress your serialized state with lz-string
- encrypt - encrypt your serialized state with AES
- filter - store or load a subset of your state
- filter-immutable - store or load a subset of your state with support for immutablejs
- expire - expire a specific subset of your state based on a property

When the state object gets persisted, it first gets serialized with `JSON.stringify()`. If parts of your state object are not mappable to JSON objects, the serialization process may transform these parts of your state in unexpected ways. For example, the javascript Set type does not exist in JSON. When you try to serialize a Set via `JSON.stringify()`, it gets converted to an empty object. Probably not what you want.

Below is a Transform that successfully persists a Set property, which simply converts it to an array and back. In this way, the Set gets converted to an Array, which is a recognized data structure in JSON. When pulled out of the persisted store, the array gets converted back to a Set before being saved to the redux store.

```js
const myTransform = createTransform(
  // transform state on its way to being serialized and persisted.
  (inboundState, key) => {
    // convert mySet to an Array.
    return { ...inboundState, mySet: [...inboundState.mySet] };
  },
  // transform state being rehydrated
  (outboundState, key) => {
    // convert mySet back to a Set.
    return { ...outboundState, mySet: new Set(outboundState.mySet) };
  },
  // define which reducers this transform gets called for.
  { whitelist: ['someReducer'] }
);
```

The createTransform function takes three parameters.
1. A function that gets called right before state is persisted.
2. A function that gets called right before state is rehydrated.
3. A config object.

## Storage Engines

- **localStorage** `import storage from 'redux-persist/lib/storage'`
- **sessionStorage** `import sessionStorage from 'redux-persist/lib/storage/session'`
- **AsyncStorage** react-native `import storage from 'redux-persist/lib/storage'`
- **localForage** recommended for web
- **electron storage** Electron support via electron store
- **redux-persist-filesystem-storage** react-native, to mitigate storage size limitations in android (#199, #284)
- **redux-persist-node-storage** for use in nodejs environments.
- **redux-persist-sensitive-storage** react-native, for sensitive information (uses react-native-sensitive-storage).
- **redux-persist-expo-securestore** react-native, for sensitive information using Expo's SecureStore. Only available if using Expo SDK (Expo, create-react-native-app, standalone).
- **redux-persist-fs-storage** react-native-fs engine
- **redux-persist-cookie-storage** Cookie storage engine, works in browser and Node.js, for universal / isomorphic apps
- **custom** any conforming storage api implementing the following methods: `setItem` `getItem` `removeItem`. (**NB**: These methods must support promises)
