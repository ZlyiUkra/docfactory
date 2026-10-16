# @upstash/strapi-plugin-upstash-ratelimit README 0.0.0
# джерело: https://registry.npmjs.org/@upstash/strapi-plugin-upstash-ratelimit/-/strapi-plugin-upstash-ratelimit-0.0.0.tgz
# отримано: 2026-10-16
# версія: strapi-plugin-upstash-ratelimit-0.0.0

Strapi Upstash Ratelimit Plugin
Ratelimit your Strapi endpoints using globally distributed redis.

npm package version
npm package daily downloads
github stars
github issues

> [!NOTE]
> **This project is in the Experimental Stage.**
> We declare this project experimental to set clear expectations for your usage. There could be known or unknown bugs, the API could evolve, or the project could be discontinued if it does not find community adoption. While we cannot provide professional support for experimental projects, we’d be happy to hear from you if you see value in this project!

## Quickstart

### Install

#### npm

```bash
npm install --save strapi-plugin-strapi-algolia
```

#### yarn

```bash
yarn add strapi-plugin-strapi-algolia
```

### Create database

Create a new redis database on Upstash Console. See docs for further info related to creating a database.

### Set up environment variables

Get the environment variables from Upstash Console, and set it to `.env` file as below:

```shell
UPSTASH_REDIS_REST_TOKEN="<YOUR_TOKEN>"
UPSTASH_REDIS_REST_URL="<YOUR_URL>"
```

### Configure the Strapi plugin

In the `./config/plugins.ts` file, set the configurations for ratelimiter.

```typescript
export default () => ({
  "strapi-plugin-upstash-ratelimit": {
    enabled: true,
    resolve: "./src/plugins/strapi-plugin-upstash-ratelimit",
    config: {
      enabled: true,
      token: process.env.UPSTASH_REDIS_REST_TOKEN,
      url: process.env.UPSTASH_REDIS_REST_URL,
      strategy: [
        {
          methods: ["GET", "POST"],
          path: "*",
          limiter: {
            algorithm: "fixed-window",
            tokens: 10,
            window: "20s",
          },
        },
      ],
      prefix: "@strapi",
    },
  },
});
```

## Documentation

See the documentation for more information details about this package.
