# @upstash/mcp-server README 0.2.2: Upstash MCP
# джерело: https://registry.npmjs.org/@upstash/mcp-server/-/mcp-server-0.2.2.tgz
# отримано: 2026-10-16
# версія: mcp-server-0.2.2

Install MCP Server

smithery badge

The Upstash MCP gives your agent the ability to interact with your Upstash account, such as:

### Redis

- "Create a new Redis in us-east-1"
- "List my databases that have high memory usage"
- "Give me the schema of how users are stored in redis"
- "Create a backup and clear db"
- "Give me the spikes in throughput during the last 7 days"

### QStash & Workflow

- "Check the logs and figure out what is wrong"
- "Find me failed workflows of user @ysfk_0x"
- "Restart the failed workflow run started in last 2 hours"
- "Check DLQ and give me a summary"

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

### Claude Code

```bash
claude mcp add --transport stdio upstash -- npx -y @upstash/mcp-server@latest --email YOUR_EMAIL --api-key YOUR_API_KEY
```

### Streamable HTTP Transport (for web applications)

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

## Telemetry

The server sends anonymous runtime/platform info to Upstash with each request. To opt out, add `--disable-telemetry` to your args.

## Troubleshooting

See the troubleshooting guide in the official MCP documentation. You can also reach out to us at Discord for support.

## Development

Clone the project and run:

```bash
bun i
bun run watch
```

This will continuously build the project and watch for changes.

For testing, you can create a `.env` file in the same directory as the project with the following content:

```bash
UPSTASH_EMAIL=<UPSTASH_EMAIL>
UPSTASH_API_KEY=<UPSTASH_API_KEY>
```

To install the local MCP Server to Claude Code, run:

```bash
claude mcp add --transport stdio upstash -- bun --watch dist/index.js --debug
```

To view the logs from the MCP Server in real time, run:

```bash
bun run logs
```
