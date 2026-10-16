# @upstash/text2emoji README 1.0.0: Text2Emoji
# джерело: https://registry.npmjs.org/@upstash/text2emoji/-/text2emoji-1.0.0.tgz
# отримано: 2026-10-16
# версія: text2emoji-1.0.0

## Overview

**Text2Emoji** is a Node.js SDK which maps input text to relevant emojis using a Vector-based similarity search powered by Upstash.

The key features include:
- Semantic rather than full text search. e.g. `delicious` matches food emojis
- A lightweight SDK for querying emoji data using an existing Upstash vector database.
- A utility script to seed the vector index with emoji data (`emoji_data.json`).
- Emoji data is enriched using OpenAI ChatGPT model.
---

## Installation and Usage

### Seed Vector Index

In this step, we will insert the Emoji data your Upstash Vector DB. So first you need to create an Index and select one of the available embedding models (do not choose custom).

Download or clone the repo.

Rename the .env.example file as .env and add your Upstash Vector DB URL and token.

Install dependencies then run the seed.js:
```bash
npm install
node scripts/seed.js
```
Check your Data Browser on Upstash console to ensure the emoji data inserted into the Upstash Vector index.

### Basic Usage

Install by:
```bash
npm install @upstash/text2emoji
```

```js
// examples/basic.js
import Text2Emoji from './src/sdk.js';
import dotenv from 'dotenv';

dotenv.config();

async function test() {
    const text2emoji = new Text2Emoji({
        vectorRestUrl: process.env.UPSTASH_VECTOR_REST_URL,
        vectorRestToken: process.env.UPSTASH_VECTOR_REST_TOKEN
    });

    console.log( await text2emoji.get("delicious", 5) );

    const testCases = [
        "love",
        "happy",
        "sad",
        "angry",
        "celebration",
        "food"
    ];


    for (const text of testCases) {
        const emojis = await text2emoji.get(text, 3);
        console.log(`Emojis for "${text}":`, emojis);
    }
}

test().catch(console.error);
```

## Contributing

Feel free to raise issues or submit pull requests to improve this package or add additional features.
