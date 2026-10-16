# RAGChat with Nuxt.js Example
# джерело: https://github.com/upstash/rag-chat/blob/v1.6.4/examples/nextjs/server-actions/README.md
# отримано: 2026-10-16
# версія: rag-chat-1.6.4, rag-chat-1.6.1, rag-chat-1.6.0, rag-chat-1.5.0, rag-chat-1.4.0, rag-chat-1.3.2, rag-chat-1.3.1, rag-chat-1.3.0, rag-chat-1.2.1, rag-chat-1.1.1, rag-chat-1.1.0, rag-chat-1.0.7, rag-chat-1.0.6, rag-chat-1.0.5, rag-chat-1.0.4

This project demonstrates how to implement RAGChat (Retrieval-Augmented Generation Chat) using Next.js server actions.

## Getting started

### 1. Install packages

```bash
npm install
```

### 2. Start the app

```bash
npm run dev
```

The app will start running on `http://localhost:3000`.

### How It Works

1. Server actions: The server actions for adding data as well as chatting are located in `actions.ts`:

   - `server_chat`: Handles chat requests, retrieves relevant information using RAG, and streams responses back to the client.
   - `server_add_data`: Adds new data to the knowledge base for future retrieval.

2. RAG Implementation: The RAGChat class from @upstash/rag-chat is used to integrate the vector database and language model.
3. Vector Database: Upstash Vector is used to store and retrieve context-relevant information.
4. Language Model: The example uses Meta's Llama 3 8B Instruct model via QStash, but can be easily switched to OpenAI's GPT models.

### Customization

Upstash RAGChat is highly customizable to suit your needs. For all available options, please refer to our RAGChat documentation.
