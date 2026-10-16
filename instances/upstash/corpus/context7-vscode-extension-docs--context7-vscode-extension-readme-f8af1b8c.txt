# Context7 MCP Server for VS Code
# джерело: https://github.com/upstash/context7-vscode-extension/blob/v1.1.0/README.md
# отримано: 2026-10-16
# версія: context7-vscode-1.1.0

This VS Code extension registers the Context7 MCP (Model Context Protocol) server with VS Code's built-in MCP support, giving AI assistants real-time access to up-to-date documentation for thousands of libraries and frameworks.

The extension connects to the hosted Context7 server at `https://mcp.context7.com/mcp`, so it is always running the latest version — no local server process, no manual updates.

## Features

- **Up-to-date Documentation**: Pulls version-specific documentation and code examples straight from the source into your AI assistant's context
- **Automatic Library Resolution**: Finds the right library documentation based on your query
- **Zero Configuration**: The server is registered automatically when the extension activates
- **Optional API Key**: Add a Context7 API key for higher rate limits and access to private repositories

## Installation

Install **Context7 MCP Server** from the Visual Studio Marketplace, or from the Extensions view in VS Code (`Upstash.context7-mcp`).

Requires VS Code 1.101 or later.

## Usage

Once installed, the Context7 MCP server is available to VS Code's AI features (e.g. Copilot Chat in agent mode). Ask questions like:

- "Show me how to use React hooks. use context7"
- "What are the best practices for Next.js routing? use context7"
- "How do I implement authentication with Supabase? use context7"

You can also reference a library directly by its Context7 ID:

```text
Implement basic authentication with Supabase. Use the API and documentation from the /supabase/supabase library.
```

> **Tip:** Add a rule to your AI assistant's instructions (e.g. `.github/copilot-instructions.md`) telling it to use Context7 for code generation and library questions, so you don't have to type `use context7` every time.

### Available Tools

1. **`resolve-library-id`** — Resolves a package/product name to a Context7-compatible library ID
2. **`get-library-docs`** — Fetches up-to-date documentation for a library

## Configuration

| Setting | Description |
|---------|-------------|
| `context7.apiKey` | Optional Context7 API key for higher rate limits and private repositories. Get one at context7.com/dashboard. |

Changing the API key stops the running server so the new key can be picked up. Restart it via **MCP: List Servers** → **Context7** → **Start Server** (or just send a new chat request, which prompts to start it) — no window reload required.

## Development

### Project Structure

```text
├── src/
│   └── extension.ts          # Main extension code
├── package.json              # Extension manifest
├── tsconfig.json             # TypeScript configuration
├── CHANGELOG.md              # Release notes
├── DEPLOYMENT.md             # Publishing guide
└── README.md                 # This file
```

### Building

```bash
npm install     # Install dependencies
npm run compile # Build the extension
```

### Testing

1. Open this repository in VS Code
2. Press F5 to launch the extension in a new Extension Development Host window
3. Run the **MCP: List Servers** command and confirm "Context7" is listed
4. Open Copilot Chat in agent mode and ask a library question with "use context7"

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Context7 for providing the MCP server for real-time documentation access
