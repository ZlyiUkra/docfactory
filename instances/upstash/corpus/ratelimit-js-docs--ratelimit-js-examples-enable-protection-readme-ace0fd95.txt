# Using deny list by enabling protection
# джерело: https://github.com/upstash/ratelimit-js/blob/v2.2.0/examples/enable-protection/README.md
# отримано: 2026-10-16
# версія: ratelimit-2.2.0, ratelimit-2.1.0, ratelimit-2.0.8, ratelimit-2.0.7, ratelimit-2.0.6, ratelimit-2.0.5, ratelimit-2.0.4, ratelimit-2.0.3, ratelimit-2.0.2, ratelimit-2.0.1, ratelimit-2.0.0, ratelimit-1.2.1

To use enable list, simply set the `enableProtection` parameter to true when
initializing the Upstash Redis client.

```tsx
const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, "10 s"),
  prefix: "@upstash/ratelimit",
  analytics: true,
  enableProtection: true
});
```

When this parameter is enabled, redis client will check the identifier and
other parameters against a dent list managed through Ratelimit Dashboard.

When analytics is set to true, requests blocked with the deny list are
logged under Denied and shown in the dashboard.

In addition to passing an identifier, you can pass IP address, user agent
and country in the `limit` method. If any of these values is in the deny
list, the request will be denied.

```tsx
const { success, limit, remaining, pending, reason } = await ratelimit.limit(
  identifier, {
    ip: ipAddress,
    userAgent: userAgent,
    country: country
  }
);
```

With this change, we also introduce the reason parameter, which denotes
whether a request passed with timeout or rejected with caching or deny list.

## Running the example locally

To run the example, simply create a Redis instance from Upstash
console and save the URL and the token to this directory under a
`.env` file.

Then run `npm run dev`.
