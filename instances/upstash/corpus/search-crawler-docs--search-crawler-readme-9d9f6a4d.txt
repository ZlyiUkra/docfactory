# @upstash/search-crawler
# джерело: https://github.com/upstash/search-crawler/blob/0.1.3/README.md
# отримано: 2026-10-16
# версія: search-crawler-0.1.3, search-crawler-0.1.2

A CLI tool to crawl documentation sites and create a search index for Upstash Search.

## Getting Started

You can run the CLI directly using `npx` (no installation required):

```sh
npx @upstash/search-crawler
```

## Features

- Crawls documentation websites and extracts content
- Creates a search index in Upstash Search
- Fast crawling for static content docs

You will be prompted for:
- Your Upstash Search URL
- Your Upstash Search token
- (Optional) Custom index name
- The documentation URL to crawl

The tool will:
1. Discover all internal documentation links
2. Crawl each page and extract content
3. Keep track of the new or obsolete data
4. Upsert the new records into your Upstash Search index

## Obtaining Upstash Credentials

1. Go to your Upstash Console.
2. Select your Search index.
3. Under the **Details** section, copy your `UPSTASH_SEARCH_REST_URL` and `UPSTASH_SEARCH_REST_TOKEN`.
