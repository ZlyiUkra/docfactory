# @redux-devtools/extension README 3.0.0-rc.1 … 3.2.1: Redux DevTools Extension's helper
# джерело: https://raw.githubusercontent.com/reduxjs/redux-devtools/b725a3af51cd9862b4d3c921ae342801705809a0/packages/redux-devtools-extension/README.md
# отримано: 2026-10-01
# версія: 3.2.1, 3.2.0, 3.1.0, 3.0.0, 3.0.0-rc.1

Join the chat at https://gitter.im/zalmoxisus/redux-devtools-extension

## Usage

Install:

```
yarn add @redux-devtools/extension
```

and use like that:

```js
import { createStore, applyMiddleware } from 'redux';
import { composeWithDevTools } from '@redux-devtools/extension';

const store = createStore(
  reducer,
  composeWithDevTools(
    applyMiddleware(...middleware)
    // other store enhancers if any
  )
);
```

or if needed to apply extension’s options:

```js
import { createStore, applyMiddleware } from 'redux';
import { composeWithDevTools } from '@redux-devtools/extension';

const composeEnhancers = composeWithDevTools({
  // Specify here name, actionsDenylist, actionsCreators and other options
});
const store = createStore(
  reducer,
  composeEnhancers(
    applyMiddleware(...middleware)
    // other store enhancers if any
  )
);
```

There’re just few lines of code. If you don’t want to allow the extension in production, just use ‘@redux-devtools/extension/lib/developmentOnly’ instead of ‘@redux-devtools/extension’.

## License

MIT
