# @next/playwright README 16.2.0 … 16.3.8: @next/playwright
# джерело: https://raw.githubusercontent.com/vercel/next.js/v16.3.8/packages/next-playwright/README.md
# отримано: 2026-10-01
# версія: 16.3.8, 16.3.7, 16.3.6, 16.3.5, 16.3.4, 16.3.3, 16.3.2, 16.3.1, 16.3.0, 16.3.0-preview.10, 16.2.12, 16.3.0-preview.9, 16.3.0-preview.8, 16.3.0-preview.7, 16.2.11, 16.3.0-preview.6, 16.2.10, 16.3.0-preview.5, 16.3.0-preview.4, 16.3.0-preview.3, 16.2.9, 16.2.8, 16.3.0-preview.2, 16.3.0-preview.0, 16.2.7, 16.2.6, 16.2.5, 16.2.4, 16.2.3, 16.2.2, 16.2.1, 16.2.0

> - **Status:** Experimental. This API is not yet stable.
> - **Requires:** Cache Components to be enabled.

Playwright helpers for testing Next.js applications.

## Instant Navigation Testing

An **instant navigation** commits immediately without waiting for data fetching.
The cached shell — including any Suspense loading boundaries — renders right
away, and dynamic data streams in afterward. The shell is the instant part, not
the full page.

`instant()` lets you test whether a route achieves this. While the callback is
active, navigations render only cached and prefetched content. Dynamic data is
deferred until the callback returns. This lets you make deterministic assertions
against the shell without race conditions.

The tool assumes a warm cache: all prefetches have completed and all cacheable
data is available. This way you're testing whether the route is *structured
correctly* for instant navigation, independent of network timing. If content you
expected to be cached is missing inside the callback, it points to a problem — a
missing `use cache` directive, a misplaced Suspense boundary, or a similar gap.

### Examples

**Loading shell appears instantly** (dynamic content behind a Suspense boundary):

```ts
import { instant } from '@next/playwright'

test('shows loading shell during navigation', async ({ page }) => {
  await page.goto('/')

  await instant(page, async () => {
    await page.click('a[href="/dashboard"]')

    // The loading shell is visible — dynamic data is deferred
    await expect(page.locator('[data-testid="loading"]')).toBeVisible()
  })

  // After instant() returns, dynamic data streams in normally
  await expect(page.locator('[data-testid="content"]')).toBeVisible()
})
```

**Fully instant navigation** (all content is cached):

```ts
test('navigates to profile instantly', async ({ page }) => {
  await page.goto('/')

  await instant(page, async () => {
    await page.click('a[href="/profile"]')

    // All content renders immediately
    await expect(page.locator('[data-testid="profile-name"]')).toBeVisible()
    await expect(page.locator('[data-testid="profile-bio"]')).toBeVisible()
  })
})
```

### Enabling in production builds

In development (`next dev`), the testing API is available by default. In
production builds, it is disabled unless you explicitly opt in:

```js
// next.config.js
module.exports = {
  experimental: {
    exposeTestingApiInProductionBuild: true,
  },
}
```

This is not meant to be deployed to live production sites. Only enable it in
controlled testing environments like preview deployments or CI.

## How it works

`instant()` sets a cookie that tells Next.js to serve only cached data during
navigations. While the cookie is active:

- **Client-side navigations**: The router renders only what is available in the
  prefetch cache. Dynamic data is deferred until the cookie is cleared.
- **Server renders (initial load, reload, MPA navigation)**: The server responds
  with only the static shell, without any per-request dynamic data.

When the callback completes, the cookie is cleared and normal behavior resumes.

## Design

The layering between this package and Next.js is intentionally very thin. This
serves as a reference implementation that other testing frameworks and dev tools
can replicate with minimal effort. The entire mechanism is a single cookie:

```ts
// Set the cookie to enter instant mode
document.cookie = 'next-instant-navigation-testing=1; path=/'

// ... run assertions ...

// Clear the cookie to resume normal behavior
document.cookie = 'next-instant-navigation-testing=; path=/; max-age=0'
```
