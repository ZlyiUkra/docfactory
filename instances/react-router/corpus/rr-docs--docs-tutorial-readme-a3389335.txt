# React Router Tutorial
# джерело: https://github.com/remix-run/react-router/blob/v6.0.0-alpha.2/docs/tutorial/README.md
# отримано: 2026-09-25
# версія: 6.0.0-alpha.2

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
- Redirects (main uses are for preserving old URLs and doing auth)
- Descendant `<Routes>` (rendered somewhere further down the component tree)
