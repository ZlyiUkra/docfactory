# React Router API
# джерело: https://github.com/remix-run/react-router/blob/v0.12.4/docs/api/README.md
# отримано: 2026-09-25
# версія: 0.12.4, 0.12.3, 0.12.2, 0.12.1

- `Router.run`
- `Router.create`
- `Location`
- `Transition`

- Renderable Components
  - `RouteHandler`
  - `Link`

- Configuration Components
  - `Route`
  - `DefaultRoute`
  - `NotFoundRoute`
  - `Redirect`

- Mixins
  - `State`
  - `Navigation`

## Public Modules

While there are many modules in this repository, only those found on the
default export are considered public.

```js
var Router = require('react-router');
var Link = Router.Link // yes
var Link = require('react-router/components/Link') // no
```
