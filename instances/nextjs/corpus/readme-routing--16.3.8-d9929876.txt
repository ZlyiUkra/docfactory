# @next/routing README 16.3.0-preview.7 … 16.3.8: @next/routing
# джерело: https://raw.githubusercontent.com/vercel/next.js/v16.3.8/packages/next-routing/README.md
# отримано: 2026-10-01
# версія: 16.3.8, 16.3.7, 16.3.6, 16.3.5, 16.3.4, 16.3.3, 16.3.2, 16.3.1, 16.3.0, 16.3.0-preview.10, 16.2.12, 16.3.0-preview.9, 16.3.0-preview.8, 16.3.0-preview.7

Shared route resolving package for Next.js.

## Overview

This package provides a comprehensive route resolution system that handles rewrites, redirects, middleware invocation, and dynamic route matching with support for conditional routing based on headers, cookies, queries, and host.

## Installation

```bash
npm install @next/routing
```

## Usage

```typescript
import { resolveRoutes } from '@next/routing'

const result = await resolveRoutes({
  url: new URL('https://example.com/api/users'),
  basePath: '',
  requestBody: readableStream,
  headers: new Headers(),
  pathnames: ['/api/users', '/api/posts'],
  routes: {
    beforeMiddleware: [],
    beforeFiles: [],
    afterFiles: [],
    dynamicRoutes: [],
    onMatch: [],
    fallback: [],
  },
  invokeMiddleware: async (ctx) => {
    // Your middleware logic
    return {}
  },
})

if (result.resolvedPathname) {
  console.log('Resolved pathname:', result.resolvedPathname)
  console.log('Resolved query:', result.resolvedQuery)
  console.log('Invocation target:', result.invocationTarget)
}
```

## Route Resolution Flow

1. **beforeMiddleware routes** - Applied before middleware execution
2. **invokeMiddleware** - Custom middleware logic
3. **beforeFiles routes** - Applied before checking filesystem
4. **Static pathname matching** - Check against provided pathnames
5. **afterFiles routes** - Applied after filesystem checks
6. **dynamicRoutes** - Dynamic route matching with parameter extraction
7. **fallback routes** - Final fallback routes

## Route Configuration

Each route can have:

- `sourceRegex` - Regular expression to match against pathname
- `destination` - Destination path with support for replacements ($1, $name)
- `headers` - Headers to apply on match
- `has` - Conditions that must match
- `missing` - Conditions that must not match
- `status` - HTTP status code (3xx for redirects)

### Redirects

When a route has:
- A redirect status code (300-399)
- Headers containing `Location` or `Refresh`

The routing will end immediately and return a `redirect` result with the destination URL and status code.

### Has/Missing Conditions

Conditions support:

- `header` - Match HTTP headers
- `cookie` - Match cookies
- `query` - Match query parameters
- `host` - Match hostname

Values can be:

- `undefined` - Match if key exists
- String - Direct string match
- Regex string - Match against regex pattern
