# README
# джерело: https://github.com/upstash/search-js/blob/0.1.7/examples/upstash-search-vercel-changelog/README.md
# отримано: 2026-10-16
# версія: search-0.1.7, search-0.1.6

Deploy with Vercel

## Vercel Changelog Search

A Next.js application that provides search functionality for Vercel's changelog using Upstash Search.

## Features

- **Full-text & Semantic Search**: Search through Vercel changelog entries with full text and semantic search capabilities
- **Input Enrichment & Reranking**: Enriches search queries and reranks search results
- **Date & Content Type Filtering**: Filter results by date range (From/Until dates) and content type (Blog/Changelog)
- **Search Scoring**: Display relevance scores for search results

## Setup

### 1. Install Dependencies

```bash
bun install
```

### 2. Environment Configuration

> [!TIP]
> If you created the project with the `Deploy with Vercel` button, you can skip this section.

Copy the example environment file and configure your Upstash Search credentials:

```bash
cp .env.example .env.local
```

To create an Upstash Search database:

1. Go to Upstash Console
2. Create a new Search index named `vercel-changelog`
3. Copy the REST URL and Token to your `.env.local` file

### 3. Load the Database

Upload the data from `https://vercel.com/atom` to Upstash Search:

```bash
bun upload-data
```

## Development

```bash
bun dev
```

Open http://localhost:3000 to view the application.

## Tech Stack

- **Next.js 15** - React framework with App Router
- **TypeScript** - Type safety
- **Ant Design** - UI component library
- **Tailwind CSS** - Utility-first CSS framework
- **Upstash Search** - Semantic and full-text search
