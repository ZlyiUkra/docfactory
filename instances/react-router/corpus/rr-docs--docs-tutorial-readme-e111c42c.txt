# React Router Tutorial
# джерело: https://github.com/remix-run/react-router/blob/v6.0.0-beta.6/docs/tutorial/README.md
# отримано: 2026-09-25
# версія: 6.0.0-beta.6, 6.0.0-beta.5, 6.0.0-beta.4, 6.0.0-beta.3, 6.0.0-beta.2, 6.0.0-beta.1, 6.0.0-beta.0, 6.0.0-alpha.5, 6.0.0-alpha.4, 6.0.0-alpha.3, experimental

Principles we should cover:

- Static paths like `<Route path="home">`
- Dynamic paths like `<Route path=":id">`
- Nested paths (and layouts with `<Outlet>`s) like:

```
function ProductLayout() {
  return (
    <div>
      <h1>Product Layout</h1>
      <Outlet />
    </div>
  )
}

<Route path="products" element={<ProductLayout />}>
  <Route path=":id" element={<ProductDetail />}>
<Route path=":id">
```

- Links
- Redirects (after auth)
- Descendant `<Routes>` (rendered somewhere further down the component tree)
