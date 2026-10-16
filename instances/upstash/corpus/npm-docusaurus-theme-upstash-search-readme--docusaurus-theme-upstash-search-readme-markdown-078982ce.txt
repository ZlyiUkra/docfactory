# @upstash/docusaurus-theme-upstash-search README 1.0.0: `@upstash/docusaurus-theme-upstash-search`
# джерело: https://registry.npmjs.org/@upstash/docusaurus-theme-upstash-search/-/docusaurus-theme-upstash-search-1.0.0.tgz
# отримано: 2026-10-16
# версія: docusaurus-theme-upstash-search-1.0.0

AI-powered search component for Docusaurus using Upstash Search.

## Features

- 🤖 AI-powered search search results based on your documentation
- 🎨 Modern and responsive UI
- 🌜 Dark/Light mode support

## Installation

To install the package, run:

```bash
npm install @upstash/docusaurus-theme-upstash-search
```

### Enabling the Searchbar

To enable the searchbar, add the following to your docusaurus config file:

```js
export default {
  themes: ['@upstash/docusaurus-theme-upstash-search'],
  // ...
  themeConfig: {
    // ...
    upstash: {
      upstashSearchRestUrl: "UPSTASH_SEARCH_REST_URL",
      upstashSearchReadOnlyRestToken: "UPSTASH_SEARCH_READ_ONLY_REST_TOKEN",
      upstashSearchIndexName: "UPSTASH_SEARCH_INDEX_NAME",
    },
  },
};
```

The default index name is `docusaurus`. You can override it by setting the `upstashSearchIndexName` option.

You can fetch your URL and read only token from Upstash Console. **Make sure to use the read only token!**

If you do not have a search database yet, you can create one from Upstash Console. Make sure to use Upstash generated embedding model.

### Indexing Your Docs

To index your documentation, create a `.env` file with the following environment variables and run `npx index-docs-upstash`.

```bash
UPSTASH_SEARCH_REST_URL=
UPSTASH_SEARCH_REST_TOKEN=
UPSTASH_SEARCH_INDEX_NAME=
DOCS_PATH=
```

You can fetch your URL and token from Upstash Console. This time **do not use the read only token** since we are upserting data.

The indexing script looks for documentation in the `docs` directory by default. You can specify a different path using the `DOCS_PATH` option.

The default index name is `docusaurus`. You can override it by setting the `UPSTASH_SEARCH_INDEX_NAME` option. Make sure the name you set while indexing matches with your themeConfig `upstashSearchIndexName` option.
