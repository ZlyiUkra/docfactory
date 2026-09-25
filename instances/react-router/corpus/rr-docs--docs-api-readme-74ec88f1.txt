# React Router API
# джерело: https://github.com/remix-run/react-router/blob/v0.9.4/docs/api/README.md
# отримано: 2026-09-25
# версія: 0.9.4, 0.9.3, 0.9.2, 0.9.1, 0.9.0

- `Router`

- Components
  - `DefaultRoute`
  - `Link`
  - `NotFoundRoute`
  - `Redirect`
  - `Route`
  - `RouteHandler`
  - `Routes`

- Mixins
  - `ActiveState`
  - `AsyncState`
  - `CurrentPath`
  - `Navigation`

- Misc
  - `transition`

## Public Modules

While there are many modules in this repository, only those found on the
default export are considered public.

```js
var Router = require('react-router');
var Link = Router.Link // yes
var Link = require('react-router/modules/components/Link') // no
```
