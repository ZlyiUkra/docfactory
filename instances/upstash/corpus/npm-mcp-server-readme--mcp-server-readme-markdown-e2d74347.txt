# @upstash/mcp-server README 0.2.0 … 0.2.1: Upstash MCP Server
# джерело: https://registry.npmjs.org/@upstash/mcp-server/-/mcp-server-0.2.1.tgz
# отримано: 2026-10-16
# версія: mcp-server-0.2.1, mcp-server-0.2.0

Install MCP Server

Install MCP Server

smithery badge

Model Context Protocol (MCP) is a new, standardized protocol for managing context between large language models (LLMs) and external systems. In this repository, we provide an installer as well as an MCP Server for Upstash Developer API's.

This allows you to use any MCP Client to interact with your Upstash account using natural language, e.g.:

- "Create a new Redis database in us-east-1"
- "List my databases"
- "List keys starting with "user:" in users-db"
- "Create a backup"
- "Give me the spikes in throughput during the last 7 days"

## Usage

## Quick Setup

First, get your Upstash credentials:

- **Email**: Your Upstash account email
- **API Key**: Get it from Upstash Console → Account → API Keys

Add this to your MCP client configuration:

```json
{
  "mcpServers": {
    "upstash": {
      "command": "npx",
      "args": [
        "-y",
        "@upstash/mcp-server@latest",
        "--email",
        "YOUR_EMAIL",
        "--api-key",
        "YOUR_API_KEY"
      ]
    }
  }
}
```

**Streamable HTTP Transport (for web applications):**

Start your MCP server with the `http` transport:

```bash
npx @upstash/mcp-server@latest --transport http --port 3000 --email YOUR_EMAIL --api-key YOUR_API_KEY
```

And configure your MCP client to use the HTTP transport:

```json
{
  "mcpServers": {
    "upstash": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

Docker Setup

1. **Create a Dockerfile:**

   Click to see Dockerfile content

```Dockerfile
   FROM node:18-alpine

   WORKDIR /app

   # Install the latest version globally
   RUN npm install -g @upstash/mcp-server

   # Expose default port if needed (optional, depends on MCP client interaction)
   # EXPOSE 3000

   # Default command to run the server
   CMD ["upstash-mcp-server"]
```

   Then, build the image using a tag (e.g., `upstash-mcp`). **Make sure Docker Desktop (or the Docker daemon) is running.** Run the following command in the same directory where you saved the `Dockerfile`:

```bash
   docker build -t upstash-mcp .
```

2. **Configure Your MCP Client:**

   Update your MCP client's configuration to use the Docker command.

   _Example for a claude_desktop_config.json:_

```json
   {
     "mcpServers": {
       "upstash": {
         "command": "docker",
         "args": [
           "run",
           "-i",
           "--rm",
           "-e",
           "UPSTASH_EMAIL=YOUR_EMAIL",
           "-e",
           "UPSTASH_API_KEY=YOUR_API_KEY",
           "upstash-mcp"
         ]
       }
     }
   }
```

   _Note: This is an example configuration. Please refer to the specific examples for your MCP client (like Cursor, VS Code, etc.) earlier in this README to adapt the structure (e.g., `mcpServers` vs `servers`). Also, ensure the image name in `args` matches the tag used during the `docker build` command._

## Requirements

- Node.js >= v18.0.0
- Upstash API key - You can create one from here.

### Troubleshooting

#### Common Issues

Your mcp client might have trouble finding the right binaries because of the differences between your shell and system `PATH`.

To fix this, you can get the full path of the binaries by running `which npx` or `which docker` in your shell, and replace the `npx` or `docker` command in the MCP config with the full binary path.

#### Node Version Manager

If you are using a node version manager like nvm or fnm, please check this issue. You should change the `node` command in the MCP config to the absolute path of the node binary.

#### Additional Troubleshooting

See the troubleshooting guide in the MCP documentation. You can also reach out to us at Discord.

## Tools

### Redis

- `redis_database_create_backup`
- `redis_database_create_new`
- `redis_database_delete`
- `redis_database_delete_backup`
- `redis_database_get_details`
- `redis_database_list_backups`
- `redis_database_list_databases`
- `redis_database_reset_password`
- `redis_database_restore_backup`
- `redis_database_run_multiple_redis_commands`
- `redis_database_run_single_redis_command`
- `redis_database_set_daily_backup`
- `redis_database_update_regions`
- `redis_database_get_usage_last_5_days`
- `redis_database_get_stats`

## Development

Clone the project and run:

```bash
pnpm install
pnpm run watch
```

This will continuously build the project and watch for changes.

For testing, you can create a `.env` file in the same directory as the project with the following content:

```bash
UPSTASH_EMAIL=<UPSTASH_EMAIL>
UPSTASH_API_KEY=<UPSTASH_API_KEY>
```

This will be used for setting the Claude config.

### Testing with Claude Desktop

To install the Claude Desktop config for local development, add the following to your Claude Desktop MCP config:

```json
{
  "mcpServers": {
    "upstash": {
      "command": "node",
      "args": [
        "<path-to-repo>/dist/index.js",
        "run",
        "--email",
        "<UPSTASH_EMAIL>",
        "--api-key",
        "<UPSTASH_API_KEY>"
      ]
    }
  }
}
```

> NOTE: The same issue with node version manager applies here. Please look at the note in the usage section if you are using a node version manager.

You can now use Claude Desktop to run Upstash commands.

To view the logs from the MCP Server in real time, run the following command:

```bash
pnpm run logs
```
