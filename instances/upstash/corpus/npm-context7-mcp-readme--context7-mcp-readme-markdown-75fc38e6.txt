# @upstash/context7-mcp README 0.0.1: Context7 MCP Server
# джерело: https://registry.npmjs.org/@upstash/context7-mcp/-/context7-mcp-0.0.1.tgz
# отримано: 2026-10-16
# версія: context7-mcp-0.0.1

In this repository, we provide an MCP Server for Context7, which offers access to high-quality documentation for popular libraries.

This lets you use Cursor, Windsurf, Claude Desktop, or any MCP Client, to use natural language to search and access documentation for libraries, e.g.:

- "What are the main features of React hooks?"
- "How do I implement authentication with Next.js?"
- "Rate limiting with Redis"
- "Get examples of using React Query"

## Usage

### Requirements

- Node.js >= v18.0.0
- Cursor, Windsurf, Claude Desktop or another MCP Client

### How to use locally

#### Installing for Cursor

Add this command to the MCP list in Cursor. For more info, check the Cursor MCP docs.

```bash
npx -y @upstash/context7-mcp
```

#### Installing for Windsurf

Add this to your Windsurf MCP config file. For more info, check the Windsurf MCP docs.

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### Tools

- `list-available-docs`: Lists all available documentation libraries from Context7
- `get-library-documentation`: Retrieves documentation for a specific library with options for:
  - `libraryName`: Name of the library to retrieve docs for
  - `topic`: Specific topic within the library
  - `tokens`: Maximum tokens to retrieve (default: 5000)

## Development

Clone the project and run:

```bash
npm install
```

You can use the following commands to format and lint the code:

```bash
npm run format
npm run lint
```

### Building

```bash
npm run build
```

### Testing with MCP Inspector

You can also use the MCP Inspector to test the tools by following the MCP documentation for setting up the inspector.

```bash
npx -y @modelcontextprotocol/inspector npx @upstash/context7-mcp
```

## License

MIT
