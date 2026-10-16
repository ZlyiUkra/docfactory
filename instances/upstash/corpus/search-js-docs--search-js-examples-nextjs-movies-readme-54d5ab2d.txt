# README
# джерело: https://github.com/upstash/search-js/blob/0.1.7/examples/nextjs-movies/README.md
# отримано: 2026-10-16
# версія: search-0.1.7, search-0.1.6, search-0.1.5, search-0.1.4, search-0.1.3

Deploy with Vercel

## Upstash Search - Movies Example

This is a Next.js application demonstrating the semantic search capabilities of Upstash Search. It allows you to search for movies using natural language queries and find semantically similar content from a movie dataset.

## Features

- **Semantic Search:** Utilizes Upstash Search's AI-powered semantic search to find movies based on meaning and context, not just keywords.
- **Movie Details:** View detailed information about specific movies by clicking on search results.
- **Smart Filtering:** Advanced search capabilities that understand the intent behind your queries.
- **Command-line Data Import:** Easy setup with a dedicated script to populate your database.

## Setup

Follow these steps to get the application running:

1.  **Install Dependencies:**
```bash
    npm install
```

2.  **Create Upstash Search Database:**
    - Go to the Upstash Console and create a new Search database.
    - Once created, copy your `UPSTASH_SEARCH_REST_URL` and `UPSTASH_SEARCH_REST_TOKEN`.

3.  **Set Environment Variables:**
    Create a `.env` file in the project root and add your credentials:
```env
    UPSTASH_SEARCH_REST_URL="YOUR_UPSTASH_SEARCH_REST_URL"
    UPSTASH_SEARCH_REST_TOKEN="YOUR_UPSTASH_SEARCH_REST_TOKEN"
```
    Replace the placeholder values with your actual Upstash Search credentials.

    You can also control reranking through env variables. If you want to enable reranking, set env variable `RERANKING_ENABLED` to `true`. Reranking is disabled by default.

4.  **Populate the Database:**
    Run the data upsert script to populate your Upstash Search database with the movie dataset:
```bash
    npm run upsert-data
```
    This script will process and upload all movie data to your database. You'll see progress logs as batches are uploaded.

5.  **Start the Development Server:**
```bash
    npm run dev
```
    Open http://localhost:3000 with your browser to see the application.

6.  **Search for Movies:**
    Try semantic search queries like:
    - "space adventure with robots"
    - "romantic comedy in Paris"
    - "thriller about artificial intelligence"
    - "superhero movie with humor"

## Learn More About Upstash Search

- Upstash Search Documentation
- Upstash Search GitHub Repository
