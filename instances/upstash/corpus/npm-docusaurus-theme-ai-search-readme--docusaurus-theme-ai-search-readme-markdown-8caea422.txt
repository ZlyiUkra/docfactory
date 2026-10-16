# @upstash/docusaurus-theme-ai-search README 1.0.0: `@upstash/docusaurus-theme-ai-search`
# джерело: https://registry.npmjs.org/@upstash/docusaurus-theme-ai-search/-/docusaurus-theme-ai-search-1.0.0.tgz
# отримано: 2026-10-16
# версія: docusaurus-theme-ai-search-1.0.0

AI Search and Chat Component for Docusaurus using Upstash Vector.

## Features

- 🔍 Hybrid search combining sparse and dense embeddings for better results
- 🤖 AI-powered chat responses based on your documentation
- 🎨 Modern and responsive UI
- 🌜 Dark/Light mode support
- 🔒 Secure AI chat communication with CORS protection

## Demo

See it in action with `Jest` documentation here or you can watch the demo video:

Demo Video - Click to Play

## Installation

To install the package, run:

```bash
npm install @upstash/docusaurus-theme-ai-search
```

### Enable Searchbar

To enable the searchbar, add the following to your docusaurus config:

```js
export default {
  themes: ['@upstash/docusaurus-theme-ai-search'],
  // ...
  themeConfig: {
    // ...
    upstash: {
      enableAiChat: false, // Set to true to enable AI chat
      upstashVectorRestUrl: "UPSTASH_VECTOR_REST_URL",
      upstashVectorReadOnlyRestToken: "UPSTASH_VECTOR_READ_ONLY_REST_TOKEN",
      upstashVectorIndexNamespace: "UPSTASH_VECTOR_INDEX_NAMESPACE",
    },
  },
};
```

The default index namespace is `@upstash/docusaurus-theme-ai-search`. You can override it by setting the `upstashVectorIndexNamespace` option.

You can fetch your URL and read only token from Upstash Console. Make sure to use the read only token!

If you do not have a vector index yet, you can create one from Upstash Console. Make sure to use Upstash generated embedding model.

### Index Documents

Set your env variables in a `.env` file and run `npx index-docs-upstash`.

```bash
UPSTASH_VECTOR_REST_URL=
UPSTASH_VECTOR_REST_TOKEN=
UPSTASH_VECTOR_INDEX_NAMESPACE=
DOCS_PATH=
```

You can fetch your URL and read only token from Upstash Console. This time do not use the read only token since we are indexing.

The default docs path is `docs`. You can override it by setting the `DOCS_PATH` option.

The default index namespace is `@upstash/docusaurus-theme-ai-search`. You can override it by setting the `UPSTASH_VECTOR_INDEX_NAMESPACE` option. Make sure this matches with your themeConfig `upstashVectorIndexNamespace` option.

### Enable AI Chat

To enable AI Chat, set the `enableAiChat` option to `true`.

```js
export default {
  // ...
  themeConfig: {
    // ...
    upstash: {
      enableAiChat: true,
      aiChatApiEndpoint: "https://your-function-deployment-url/api/ask-ai",
    },
  },
};
```

Deploy the ai chat endpoint with the following button:

Deploy with Vercel
