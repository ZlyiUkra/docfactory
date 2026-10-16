# @upstash/search-redis README 0.1.0 … 3.0.0: @upstash/search-redis
# джерело: https://registry.npmjs.org/@upstash/search-redis/-/search-redis-3.0.0.tgz
# отримано: 2026-10-16
# версія: search-redis-3.0.0, search-redis-2.0.4, search-redis-2.0.3, search-redis-2.0.2, search-redis-2.0.1, search-redis-2.0.0, search-redis-1.0.0, search-redis-0.1.0

Use node-redis with @upstash/redis for Redis Search operations.

## Installation

```bash
npm install @upstash/search-redis redis
```

## Usage

```typescript
import { createClient } from "redis";
import { createSearch, s } from "@upstash/search-redis";

// Create node-redis client
const client = createClient({
  url: process.env.REDIS_URL,
});
await client.connect();

// Create search client
const search = createSearch(client);

const schema = s.object({
  title: s.string(),
  price: s.number(),
});

// Use all Redis search commands
await search.createIndex({
  name: "products",
  prefix: "product:",
  dataType: "string",
  schema,
});

const index = search.index({ name: "products", schema });
await index.query();
```

## Testing

To run the tests, you need an Upstash Redis server. Set the `REDIS_URL` environment variable:

```bash
export REDIS_URL=rediss://default:<PASSWORD>@<YOUR-DATABASE>.upstash.io:6379

# Run tests
npm test
```

## License

MIT
