# React Router API
# джерело: https://github.com/remix-run/react-router/blob/v0.10.2/docs/api/README.md
# отримано: 2026-09-25
# версія: 0.10.2, 0.10.1, 0.10.0, 0.9.5

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
