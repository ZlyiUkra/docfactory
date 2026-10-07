# @redux-devtools/extension README 3.3.0 … 4.0.0: Redux DevTools Extension's helper
# джерело: https://raw.githubusercontent.com/reduxjs/redux-devtools/@redux-devtools/extension@4.0.0/packages/redux-devtools-extension/README.md
# отримано: 2026-10-01
# версія: 4.0.0, 3.3.0

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
    applyMiddleware(...middleware),
    // other store enhancers if any
  ),
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
    applyMiddleware(...middleware),
    // other store enhancers if any
  ),
);
```

There are just a few lines of code. If you don’t want to allow the extension in production, just use `composeWithDevToolsDevelopmentOnly` instead of `composeWithDevTools`.

## License

MIT
