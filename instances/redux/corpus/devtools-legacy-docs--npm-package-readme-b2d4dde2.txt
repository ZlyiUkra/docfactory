# Redux DevTools Extension's helper
# джерело: https://github.com/zalmoxisus/redux-devtools-extension/blob/master/npm-package/README.md
# отримано: 2026-10-01
# версія: 2.13

Join the chat at https://gitter.im/zalmoxisus/redux-devtools-extension

## Usage

  Install:
```
  npm install --save redux-devtools-extension
```
  and use like that:
```js
  import { createStore, applyMiddleware } from 'redux';
  import { composeWithDevTools } from 'redux-devtools-extension';

  const store = createStore(reducer, composeWithDevTools(
    applyMiddleware(...middleware),
    // other store enhancers if any
  ));
```
  or if needed to apply extension’s options:
```js
  import { createStore, applyMiddleware } from 'redux';
  import { composeWithDevTools } from 'redux-devtools-extension';

  const composeEnhancers = composeWithDevTools({
    // Specify here name, actionsBlacklist, actionsCreators and other options
  });
  const store = createStore(reducer, composeEnhancers(
    applyMiddleware(...middleware),
    // other store enhancers if any
  ));
```
  There’re just few lines of code. If you don’t want to allow the extension in production, just use ‘redux-devtools-extension/developmentOnly’ instead of ‘redux-devtools-extension’.

## License

MIT
