# React Router API
# джерело: https://github.com/remix-run/react-router/blob/v0.11.6/docs/api/README.md
# отримано: 2026-09-25
# версія: 0.11.6, 0.11.5, 0.11.4, 0.11.3, 0.11.2

- `Router`

- `Router.run`

- `Router.create`

- Components
  - `DefaultRoute`
  - `Link`
  - `NotFoundRoute`
  - `Redirect`
  - `Route`
  - `RouteHandler`

- Mixins
  - `State`
  - `Navigation`

- Misc
  - `Location`
  - `transition`

## Public Modules

While there are many modules in this repository, only those found on the
default export are considered public.

```js
var Router = require('react-router');
var Link = Router.Link // yes
var Link = require('react-router/modules/components/Link') // no
```
