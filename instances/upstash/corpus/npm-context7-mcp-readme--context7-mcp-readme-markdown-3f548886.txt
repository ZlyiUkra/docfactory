# @upstash/context7-mcp README 4.1.3
# джерело: https://registry.npmjs.org/@upstash/context7-mcp/-/context7-mcp-4.1.3.tgz
# отримано: 2026-10-16
# версія: context7-mcp-4.1.3

Cover

Install MCP Server

## Context7 MCP - Up-to-date Code Docs For Any Prompt

Website NPM Version MIT licensed

繁體中文 简体中文 日本語 한국어 문서 Documentación en Español Documentation en Français Documentação em Português (Brasil) Documentazione in italiano Dokumentasi Bahasa Indonesia Dokumentation auf Deutsch Документация на русском языке Українська документація Türkçe Doküman Arabic Documentation Tiếng Việt

## ❌ Without Context7

LLMs rely on outdated or generic information about the libraries you use. You get:

- ❌ Code examples are outdated and based on year-old training data
- ❌ Hallucinated APIs that don't even exist
- ❌ Generic answers for old package versions

## ✅ With Context7

Context7 MCP pulls up-to-date, version-specific documentation and code examples straight from the source — and places them directly into your prompt.

Add `use context7` to your prompt (or set up a rule to auto-invoke):

```txt
Create a Next.js middleware that checks for a valid JWT in cookies
and redirects unauthenticated users to `/login`. use context7
```

```txt
Configure a Cloudflare Worker script to cache
JSON API responses for five minutes. use context7
```

Context7 fetches up-to-date code examples and documentation right into your LLM's context.

- 1️⃣ Write your prompt naturally
- 2️⃣ Tell the LLM to `use context7` (or set up a rule once)
- 3️⃣ Get working code answers

No tab-switching, no hallucinated APIs that don't exist, no outdated code generation.

> [!NOTE]
> This repository hosts the source code of Context7 MCP server. The supporting components — API backend, parsing engine, and crawling engine — are private and not part of this release.

## 📚 Adding Projects

Check out our project addition guide to learn how to add (or update) your favorite libraries to Context7.

## 🛠️ Installation

### Requirements

- Node.js >= v20.18.1
- Cursor, Claude Code, VSCode, Devin Desktop or another MCP Client
- Context7 API Key (Optional) for higher rate limits and private repositories (Get yours by creating an account at context7.com/dashboard)

> [!TIP]
> **Recommended Post-Setup: Add a Rule to Auto-Invoke Context7**
>
> After installing Context7 (see instructions below), enhance your workflow by adding a rule so you don't have to type `use context7` in every prompt. Define a simple rule in your MCP client's rule section to automatically invoke Context7 on any code question:
>
> - For Devin Desktop, in `.devin/rules/` directory
> - For Cursor, from `Cursor Settings > Rules` section
> - For Claude Code, in `CLAUDE.md` file
> - Or the equivalent in your MCP client
>
> **Example Rule:**
>
> ```txt
> Always use context7 when I need code generation, setup or configuration steps, or
> library/API documentation. This means you should automatically use the Context7 MCP
> tools to resolve library id and get library docs without me having to explicitly ask.
> ```
>
> From then on, you'll get Context7's docs in any related conversation without typing anything extra. You can alter the rule to match your use cases.

Installing via Smithery

To install Context7 MCP Server for any client automatically via Smithery:

```bash
npx -y @smithery/cli@latest install @upstash/context7-mcp --client <CLIENT_NAME> --key <YOUR_SMITHERY_KEY>
```

You can find your Smithery key in the Smithery.ai webpage.

Install in Cursor

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See Cursor MCP docs for more info.

> Since Cursor 1.0, you can click the install button below for instant one-click installation.

#### Cursor Remote Server Connection

Install MCP Server

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

#### Cursor Local Server Connection

Install MCP Server

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Install in Claude Code

Run this command. See Claude Code MCP docs for more info.

#### Claude Code Local Server Connection

```sh
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

#### Claude Code Remote Server Connection

```sh
claude mcp add --scope user --header "Authorization: Bearer YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp
```

> Remove `--scope user` to install for the current project only.

Install in Amp

Run this command in your terminal. See Amp MCP docs for more info.

#### Without API Key (Basic Usage)

```sh
amp mcp add context7 https://mcp.context7.com/mcp
```

#### With API Key (Higher Rate Limits & Private Repos)

```sh
amp mcp add context7 --header "Authorization=Bearer YOUR_API_KEY" https://mcp.context7.com/mcp
```

Install in Devin Desktop

Add this to your Devin Desktop MCP config file. See Devin Desktop MCP docs for more info.

#### Devin Desktop Remote Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "serverUrl": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

#### Devin Desktop Local Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Install in VS Code

Add this to your VS Code MCP config file. See VS Code MCP docs for more info.

#### VS Code Remote Server Connection

```json
"mcp": {
  "servers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

#### VS Code Local Server Connection

```json
"mcp": {
  "servers": {
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Install in Cline

You can easily install Context7 through the Cline MCP Server Marketplace by following these instructions:

1. Open **Cline**.
2. Click the hamburger menu icon (☰) to enter the **MCP Servers** section.
3. Use the search bar within the **Marketplace** tab to find _Context7_.
4. Click the **Install** button.

Or you can directly edit MCP servers configuration:

1. Open **Cline**.
2. Click the hamburger menu icon (☰) to enter the **MCP Servers** section.
3. Choose **Remote Servers** tab.
4. Click the **Edit Configuration** button.
5. Add context7 to `mcpServers`:

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "type": "streamableHttp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

Install in Zed

It can be installed via Zed Extensions or you can add this to your Zed `settings.json`. See Zed Context Server docs for more info.

```json
{
  "context_servers": {
    "Context7": {
      "source": "custom",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Install in Augment Code

To configure Context7 MCP in Augment Code, you can use either the graphical interface or manual configuration.

### **A. Using the Augment Code UI**

1. Click the hamburger menu.
2. Select **Settings**.
3. Navigate to the **Tools** section.
4. Click the **+ Add MCP** button.
5. Enter the following command:

```
   npx -y @upstash/context7-mcp@latest
```

6. Name the MCP: **Context7**.
7. Click the **Add** button.

Once the MCP server is added, you can start using Context7's up-to-date code documentation features directly within Augment Code.

---

### **B. Manual Configuration**

1. Press Cmd/Ctrl Shift P or go to the hamburger menu in the Augment panel
2. Select Edit Settings
3. Under Advanced, click Edit in settings.json
4. Add the server configuration to the `mcpServers` array in the `augment.advanced` object

```json
"augment.advanced": {
  "mcpServers": [
    {
      "name": "context7",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  ]
}
```

Once the MCP server is added, restart your editor. If you receive any errors, check the syntax to make sure closing brackets or commas are not missing.

Install in Kilo Code

You can configure the Context7 MCP server in **Kilo Code** using either the UI or by editing your project's MCP configuration file.

Kilo Code supports two configuration levels:

- **Global MCP Configuration** — stored in `mcp_settings.json`
- **Project-level MCP Configuration** — stored in `.kilocode/mcp.json` (recommended)

If a server is defined in both places, the **project-level configuration overrides the global one**.

---

## Configure via Kilo Code UI

1. Open **Kilo Code**.
2. Click the **Settings** icon in the top-right corner.
3. Navigate to **Settings → MCP Servers**.
4. Click **Add Server**.
5. Choose **HTTP Server** (Streamable HTTP Transport).
6. Enter the details:

**URL**
`https://mcp.context7.com/mcp`

**Headers → Add Header**

- **Key:** `Authorization`
- **Value:** `Bearer YOUR_API_KEY`

7. Click **Save**.
8. Ensure the server toggle is **enabled**.
9. If needed, click **Refresh MCP Servers** to reload the configuration.

---

## Manual Configuration (`.kilocode/mcp.json`)

To configure the server at the project level (recommended for team environments), create the following file:

**`.kilocode/mcp.json`:**

```json
{
  "mcpServers": {
    "context7": {
      "type": "streamable-http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      },
      "alwaysAllow": [],
      "disabled": false
    }
  }
}
```

Replace YOUR_API_KEY with your actual Context7 API key.

After saving the file:

- Open Settings → MCP Servers

- Click Refresh MCP Servers

Kilo Code will automatically detect and load the configuration.

Install in Google Antigravity

Add this to your Antigravity MCP config file. See Antigravity MCP docs for more info.

#### Google Antigravity Remote Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "serverUrl": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

#### Google Antigravity Local Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Install in Roo Code

Add this to your Roo Code MCP configuration file. See Roo Code MCP docs for more info.

#### Roo Code Remote Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "type": "streamable-http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

#### Roo Code Local Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Install in Gemini CLI

See Gemini CLI Configuration for details.

1.  Open the Gemini CLI settings file. The location is `~/.gemini/settings.json` (where `~` is your home directory).
2.  Add the following to the `mcpServers` object in your `settings.json` file:

```json
{
  "mcpServers": {
    "context7": {
      "httpUrl": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY",
        "Accept": "application/json, text/event-stream"
      }
    }
  }
}
```

Or, for a local server:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

If the `mcpServers` object does not exist, create it.

Install in Qwen Coder

See Qwen Coder MCP Configuration for details.

1.  Open the Qwen Coder settings file. The location is `~/.qwen/settings.json` (where `~` is your home directory).
2.  Add the following to the `mcpServers` object in your `settings.json` file:

```json
{
  "mcpServers": {
    "context7": {
      "httpUrl": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY",
        "Accept": "application/json, text/event-stream"
      }
    }
  }
}
```

Or, for a local server:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

If the `mcpServers` object does not exist, create it.

Install in Claude Desktop

#### Remote Server Connection

Open Claude Desktop and navigate to Settings > Connectors > Add Custom Connector. Enter the name as `Context7` and the remote MCP server URL as `https://mcp.context7.com/mcp`.

#### Local Server Connection

Open Claude Desktop developer settings and edit your `claude_desktop_config.json` file to add the following configuration. See Claude Desktop MCP docs for more info.

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Install in Opencode

Add this to your Opencode configuration file. See Opencode MCP docs for more info.

#### Opencode Remote Server Connection

```json
"mcp": {
  "context7": {
    "type": "remote",
    "url": "https://mcp.context7.com/mcp",
    "headers": {
      "Authorization": "Bearer YOUR_API_KEY"
    },
    "enabled": true
  }
}
```

#### Opencode Local Server Connection

```json
{
  "mcp": {
    "context7": {
      "type": "local",
      "command": ["npx", "-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"],
      "enabled": true
    }
  }
}
```

Install in OpenAI Codex

See OpenAI Codex for more information.

Add the following configuration to your OpenAI Codex MCP server settings:

#### Local Server Connection

```toml
[mcp_servers.context7]
args = ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
command = "npx"
startup_timeout_ms = 20_000
```

#### Remote Server Connection

```toml
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"
http_headers = { "Authorization" = "Bearer YOUR_API_KEY" }
```

> Optional troubleshooting — only if you see startup "request timed out" or "not found program". Most users can ignore this.
>
> - First try: increase `startup_timeout_ms` to `40_000` and retry.
> - Windows quick fix (absolute `npx` path + explicit env):
>
> ```toml
> [mcp_servers.context7]
> command = "C:\\Users\\yourname\\AppData\\Roaming\\npm\\npx.cmd"
> args = [
>   "-y",
>   "@upstash/context7-mcp",
>   "--api-key",
>   "YOUR_API_KEY"
> ]
> env = { SystemRoot="C:\\Windows", APPDATA="C:\\Users\\yourname\\AppData\\Roaming" }
> startup_timeout_ms = 40_000
> ```
>
> - macOS quick fix (use Node + installed package entry point):
>
> ```toml
> [mcp_servers.context7]
> command = "/Users/yourname/.nvm/versions/node/v22.14.0/bin/node"
> args = ["/Users/yourname/.nvm/versions/node/v22.14.0/lib/node_modules/@upstash/context7-mcp/dist/index.js",
>   "--transport",
>   "stdio",
>   "--api-key",
>   "YOUR_API_KEY"
> ]
> ```
>
> Notes: Replace `yourname` with your OS username. Explicitly setting `APPDATA` and `SystemRoot` is essential because these are required by `npx` on Windows but not set by certain versions of OpenAI Codex mcp clients by default.

Install in JetBrains AI Assistant

See JetBrains AI Assistant Documentation for more details.

1. In JetBrains IDEs, go to `Settings` -> `Tools` -> `AI Assistant` -> `Model Context Protocol (MCP)`
2. Click `+ Add`.
3. Click on `Command` in the top-left corner of the dialog and select the As JSON option from the list
4. Add this configuration and click `OK`

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

5. Click `Apply` to save changes.
6. The same way context7 could be added for JetBrains Junie in `Settings` -> `Tools` -> `Junie` -> `MCP Settings`

Install in Kiro

See Kiro Model Context Protocol Documentation for details.

Add to Kiro

1. Navigate `Kiro` > `MCP Servers`
2. Add a new MCP server by clicking the `+ Add` button.
3. Paste one of the configurations below:

#### Kiro Remote Server Connection

```json
{
  "mcpServers": {
    "Context7": {
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

To use an API key in Kiro, add:

```json
"headers": {
  "Authorization": "Bearer YOUR_API_KEY"
}
```

You can create an API key at context7.com/dashboard for authenticated usage and higher rate limits.

#### Kiro Local Server Connection

```json
{
  "mcpServers": {
    "Context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

4. Click `Save` to apply the changes.

Install in Trae

Use the Add manually feature and fill in the JSON configuration information for that MCP server.
For more details, visit the Trae documentation.

#### Trae Remote Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

#### Trae Local Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Using Bun or Deno

Use these alternatives to run the local Context7 MCP server with other runtimes. These examples work for any client that supports launching a local MCP server via command + args.

#### Bun

```json
{
  "mcpServers": {
    "context7": {
      "command": "bunx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

#### Deno

```json
{
  "mcpServers": {
    "context7": {
      "command": "deno",
      "args": [
        "run",
        "--allow-env=NO_DEPRECATION,TRACE_DEPRECATION",
        "--allow-net",
        "npm:@upstash/context7-mcp"
      ]
    }
  }
}
```

Using Docker

If you prefer to run the MCP server in a Docker container:

1. **Build the Docker Image:**

   First, create a `Dockerfile` in the project root (or anywhere you prefer):

   Click to see Dockerfile content

```Dockerfile
   FROM node:20-alpine

   WORKDIR /app

   # Install the latest version globally
   RUN npm install -g @upstash/context7-mcp

   # Expose default port if needed (optional, depends on MCP client interaction)
   # EXPOSE 3000

   # Default command to run the server
   CMD ["context7-mcp", "--transport", "stdio"]
```

   Then, build the image using a tag (e.g., `context7-mcp`). **Make sure Docker Desktop (or the Docker daemon) is running.** Run the following command in the same directory where you saved the `Dockerfile`:

```bash
   docker build -t context7-mcp .
```

2. **Configure Your MCP Client:**

   Update your MCP client's configuration to use the Docker command.

   _Example for a cline_mcp_settings.json:_

```json
   {
     "mcpServers": {
       "Сontext7": {
         "autoApprove": [],
         "disabled": false,
         "timeout": 60,
         "command": "docker",
         "args": ["run", "-i", "--rm", "context7-mcp"],
         "transportType": "stdio"
       }
     }
   }
```

   _Note: This is an example configuration. Please refer to the specific examples for your MCP client (like Cursor, VS Code, etc.) earlier in this README to adapt the structure (e.g., `mcpServers` vs `servers`). Also, ensure the image name in `args` matches the tag used during the `docker build` command._

   If you use the Docker MCP Toolkit image (`mcp/context7`) with a stdio-based client,
   set `MCP_TRANSPORT=stdio` so the container starts with stdio transport instead of its
   HTTP default. For Cline, Roo Code, and Claude Desktop, use:

```json
   {
     "mcpServers": {
       "context7": {
         "command": "docker",
         "args": ["run", "-i", "--rm", "-e", "MCP_TRANSPORT=stdio", "mcp/context7"]
       }
     }
   }
```

   For VS Code, use the same Docker command in the `servers` format:

```json
   {
     "servers": {
       "context7": {
         "type": "stdio",
         "command": "docker",
         "args": ["run", "-i", "--rm", "-e", "MCP_TRANSPORT=stdio", "mcp/context7"]
       }
     }
   }
```

   Keep using the remote server URL for HTTP-based clients.

Install Using the Desktop Extension

Install the context7.mcpb file under the mcpb folder and add it to your client. For more information, please check out MCP bundles docs.

Install in Windows

The configuration on Windows is slightly different compared to Linux or macOS (_`Cline` is used in the example_). The same principle applies to other editors; refer to the configuration of `command` and `args`.

```json
{
  "mcpServers": {
    "github.com/upstash/context7-mcp": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Install in Amazon Q Developer CLI

Add this to your Amazon Q Developer CLI configuration file. See Amazon Q Developer CLI docs for more details.

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Install in Warp

See Warp Model Context Protocol Documentation for details.

1. Navigate `Settings` > `AI` > `Manage MCP servers`.
2. Add a new MCP server by clicking the `+ Add` button.
3. Paste the configuration given below:

```json
{
  "Context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"],
    "env": {},
    "working_directory": null,
    "start_on_launch": true
  }
}
```

4. Click `Save` to apply the changes.

Install in Copilot Coding Agent

## Using Context7 with Copilot Coding Agent

Add the following configuration to the `mcp` section of your Copilot Coding Agent configuration file Repository->Settings->Copilot->Coding agent->MCP configuration:

```json
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      },
      "tools": ["query-docs", "resolve-library-id"]
    }
  }
}
```

For more information, see the official GitHub documentation.

Install in Copilot CLI

1.  Open the Copilot CLI MCP config file. The location is `~/.copilot/mcp-config.json` (where `~` is your home directory).
2.  Add the following to the `mcpServers` object in your `mcp-config.json` file:

```json
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      },
      "tools": ["query-docs", "resolve-library-id"]
    }
  }
}
```

Or, for a local server:

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "tools": ["query-docs", "resolve-library-id"],
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

If the `mcp-config.json` file does not exist, create it.

Install in LM Studio

See LM Studio MCP Support for more information.

#### One-click install:

Add MCP Server context7 to LM Studio

#### Manual set-up:

1. Navigate to `Program` (right side) > `Install` > `Edit mcp.json`.
2. Paste the configuration given below:

```json
{
  "mcpServers": {
    "Context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

3. Click `Save` to apply the changes.
4. Toggle the MCP server on/off from the right hand side, under `Program`, or by clicking the plug icon at the bottom of the chat box.

Install in Visual Studio 2022

You can configure Context7 MCP in Visual Studio 2022 by following the Visual Studio MCP Servers documentation.

Add this to your Visual Studio MCP config file (see the Visual Studio docs for details):

```json
{
  "inputs": [],
  "servers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

Or, for a local server:

```json
{
  "mcp": {
    "servers": {
      "context7": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
      }
    }
  }
}
```

For more information and troubleshooting, refer to the Visual Studio MCP Servers documentation.

Install in Crush

Add this to your Crush configuration file. See Crush MCP docs for more info.

#### Crush Remote Server Connection (HTTP)

```json
{
  "$schema": "https://charm.land/crush.json",
  "mcp": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

#### Crush Local Server Connection

```json
{
  "$schema": "https://charm.land/crush.json",
  "mcp": {
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Install in BoltAI

Open the "Settings" page of the app, navigate to "Plugins," and enter the following JSON:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Once saved, enter in the chat `query-docs` followed by your Context7 documentation ID (e.g., `query-docs /nuxt/ui how to set up a theme`). More information is available on BoltAI's Documentation site. For BoltAI on iOS, see this guide.

Install in Rovo Dev CLI

Edit your Rovo Dev CLI MCP config by running the command below -

```bash
acli rovodev mcp
```

Example config -

#### Remote Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

#### Local Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

Install in Zencoder

To configure Context7 MCP in Zencoder, follow these steps:

1. Go to the Zencoder menu (...)
2. From the dropdown menu, select Agent tools
3. Click on the Add custom MCP
4. Add the name and server configuration from below, and make sure to hit the Install button

```json
{
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
}
```

Once the MCP server is added, you can easily continue using it.

Install in Qodo Gen

See Qodo Gen docs for more details.

1. Open Qodo Gen chat panel in VSCode or IntelliJ.
2. Click Connect more tools.
3. Click + Add new MCP.
4. Add the following configuration:

#### Qodo Gen Local Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

#### Qodo Gen Remote Server Connection

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

Install in Perplexity Desktop

See Local and Remote MCPs for Perplexity for more information.

1. Navigate `Perplexity` > `Settings`
2. Select `Connectors`.
3. Click `Add Connector`.
4. Select `Advanced`.
5. Enter Server Name: `Context7`
6. Paste the following JSON in the text area:

```json
{
  "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"],
  "command": "npx",
  "env": {}
}
```

7. Click `Save`.

Install in Factory

Factory's droid supports MCP servers through its CLI. See Factory MCP docs for more info.

#### Factory Remote Server Connection (HTTP)

Run this command in your terminal:

```sh
droid mcp add context7 https://mcp.context7.com/mcp --type http --header "Authorization: Bearer YOUR_API_KEY"
```

Or without an API key (basic usage with rate limits):

```sh
droid mcp add context7 https://mcp.context7.com/mcp --type http
```

#### Factory Local Server Connection (Stdio)

Run this command in your terminal:

```sh
droid mcp add context7 "npx -y @upstash/context7-mcp" --env CONTEXT7_API_KEY=YOUR_API_KEY
```

Once configured, Context7 tools will be available in your droid sessions. Type `/mcp` within droid to manage servers, authenticate, and view available tools.

Install in Emdash

Emdash is an orchestration layer for running multiple coding agents in parallel. Provider-agnostic, worktree-isolated, and local-first. Emdash supports Context7 MCP to enable Context7 for your agents.

**What Emdash provides:**

- Global toggle: Settings → MCP → "Enable Context7 MCP"
- Per-workspace enable: The Context7 button in the ProviderBar (off by default). First click enables it for that workspace. Clicking again disables it.
- ProviderBar: The Context7 button shows status, a short explanation, and a link to docs

**What you still need to do:**
Configure your coding agent (Codex, Claude Code, Cursor, etc.) to connect to Context7 MCP. Emdash does not modify your agent's config. See the respective MCP configuration sections above for your agent (e.g., OpenAI Codex, Claude Code, Cursor).

See the Emdash repository for more information.

Install in Autohand Code

Use the Autohand Code CLI to add the local Context7 server:

```sh
autohand mcp add context7 npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

Add `--scope project` before `context7` to save the server in the current project's `.autohand` configuration instead of your user configuration.

For basic usage without an API key, you can connect to the remote server instead:

```sh
autohand mcp add --transport http context7 https://mcp.context7.com/mcp
```

## 🔨 Available Tools

Context7 MCP provides the following tools that LLMs can use:

- `resolve-library-id`: Resolves a general library name into a Context7-compatible library ID.
  - `libraryName` (required): The name of the library to search for
  - `query` (required): What you need the docs for, used to rank matches

- `query-docs`: Queries up-to-date documentation and code examples for a Context7-compatible library ID.
  - `libraryId` (required): Exact Context7-compatible library ID (e.g., `/mongodb/docs`, `/vercel/next.js`)
  - `query` (required): The concept to look up, scoped to a single topic

`get-library-docs` was renamed to `query-docs`. Update client tool allowlists to use `query-docs`.

## 🛟 Tips

### Add a Rule

To avoid typing `use context7` in every prompt, you can add a rule to your MCP client that automatically invokes Context7 for code-related questions. See the recommended setup in the Installation section for detailed instructions and example rules.

### Use Library Id

If you already know exactly which library you want to use, add its Context7 ID to your prompt. That way, Context7 MCP server can skip the library-matching step and directly continue with retrieving docs.

```txt
Implement basic authentication with Supabase. use library /supabase/supabase for API and docs.
```

The slash syntax tells the MCP tool exactly which library to load docs for.

### HTTPS Proxy

If you are behind an HTTP proxy, Context7 uses the standard `https_proxy` / `HTTPS_PROXY` environment variables.

## 💻 Development

Clone the project and install dependencies:

```bash
bun i
```

Build:

```bash
bun run build
```

Run the server:

```bash
bun run dist/index.js
```

### CLI Arguments

`context7-mcp` accepts the following CLI flags:

- `--transport <stdio|http>` – Transport to use (`stdio` by default). Use `http` for remote HTTP server or `stdio` for local integration.
- `--port <number>` – Port to listen on when using `http` transport (default `3000`).
- `--api-key <key>` – API key for authentication (or set `CONTEXT7_API_KEY` env var). You can get your API key by creating an account at context7.com/dashboard.

Example with HTTP transport and port 8080:

```bash
bun run dist/index.js --transport http --port 8080
```

Another example with stdio transport:

```bash
bun run dist/index.js --transport stdio --api-key YOUR_API_KEY
```

### Environment Variables

You can use the `CONTEXT7_API_KEY` environment variable instead of passing the `--api-key` flag. This is useful for:

- Storing API keys securely in `.env` files
- Integration with MCP server setups that use dotenv
- Tools that prefer environment variable configuration

**Note:** The `--api-key` CLI flag takes precedence over the environment variable when both are provided.

**Example with .env file:**

```bash
# .env
CONTEXT7_API_KEY=your_api_key_here
```

**Example MCP configuration using environment variable:**

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### OpenTelemetry observability

Context7 instruments individual MCP requests and notifications at the SDK transport boundary,
including messages inside a valid batch and MCP v2 `subscriptions/listen` operations handled by the
SDK entry layer. Requests rejected by the SDK's HTTP envelope and protocol-version validation before
dispatch remain visible in normal HTTP/gateway telemetry, but are not reported as MCP operations.
Observed operations follow the
development-status OpenTelemetry MCP semantic conventions
for server metrics and spans. Trace context is extracted from the `traceparent`, `tracestate`, and
`baggage` fields in MCP `params._meta` as defined by
SEP-414.

The HTTP transport exposes metrics in Prometheus format on a dedicated listener at
`127.0.0.1:9464/metrics` by default. The production Docker image explicitly binds that listener to
`0.0.0.0` so an internal Prometheus pod scraper or `PodMonitor` can reach it. The stdio transport
does not open a telemetry port. Keeping this listener separate from the public MCP port prevents
the metrics endpoint from being routed through a catch-all gateway rule. On SIGTERM, SIGINT, or
SIGHUP, both transports use a bounded shutdown path that stops serving, closes active MCP
connections and subscriptions, and best-effort flushes externally installed SDK metric and trace
providers before exit. Stdio EOF triggers the same path.

The exporter uses the standard OpenTelemetry Prometheus settings:

- `OTEL_EXPORTER_PROMETHEUS_HOST` changes the bind address (default `127.0.0.1`; the Docker image
  sets `0.0.0.0`).
- `OTEL_EXPORTER_PROMETHEUS_PORT` changes the port (default `9464`).
- `OTEL_METRICS_EXPORTER=none` or `OTEL_SDK_DISABLED=true` disables the embedded exporter.

`OTEL_SDK_DISABLED=true` is the hard-off switch: provider modules are not loaded and MCP
transports and handlers are not wrapped, preserving the baseline request path. In contrast,
`OTEL_METRICS_EXPORTER=none` disables only the embedded Prometheus bootstrap, so a provider
installed by a Node preload can still receive the MCP signals.

Exporter bind or configuration failures are logged but do not prevent the MCP endpoint from
starting. If a Node preload has already registered global OpenTelemetry providers, they take
precedence. The embedded Prometheus listener is not started when a global `MeterProvider` exists,
and MCP spans are exported through the preload's `TracerProvider`. This supports an OpenTelemetry
Node SDK or Kubernetes auto-instrumentation without creating a second provider in the application.
When an external SDK owns the provider, configure its Node runtime instrumentation there as well;
the application does not register a duplicate collector.

It reports bounded-cardinality counters, histograms, and in-flight gauges for MCP methods,
subscriptions, tool outcomes, authentication outcomes, Context7 upstream requests, and Node runtime
saturation.
Prometheus receives these metric families:

- `mcp_server_operation_duration` (its `_count` series is the MCP operation count, and tool-call
  series include the `context7_mcp_tool_outcome` label)
- `mcp_server_session_duration` for real stateful stdio sessions (stateless HTTP request transports
  are intentionally excluded)
- `context7_mcp_operations_active`
- `context7_mcp_subscriptions_active` and `context7_mcp_subscription_duration`
- `context7_mcp_upstream_requests_total` and `context7_mcp_upstream_request_duration`
- `context7_mcp_authentication_attempts_total` and `context7_mcp_authentication_duration`
- `context7_mcp_upstream_requests_active` and `context7_mcp_authentication_active`
- `nodejs_eventloop_*`, `v8js_gc_duration`, `v8js_memory_heap_*`, and
  `v8js_resource_active` from the official OpenTelemetry Node runtime instrumentation

Tool outcomes on the standard MCP operation metric distinguish `success`, `not_found`, and
`error`. An acknowledged `subscriptions/listen` operation is timed through its acknowledgement;
the separate subscription metrics track the active stream and its bounded terminal outcome.
Upstream outcomes distinguish
HTTP, response-decoding, network, timeout, and cancellation failures and include both the bounded
status-code class and the exact numeric HTTP status. Authentication reports accepted, missing,
invalid, and unexpected-error outcomes. The OAuth authorization-server metadata proxy caps its
upstream fetch at 10 seconds and returns `502` if that dependency times out.

The labels intentionally exclude API keys, client IPs, queries, library IDs, session IDs, and raw
error text. Expose port `9464` only to your Prometheus scraper or `ServiceMonitor`, not through the
public MCP ingress.

#### Signal ownership with an Envoy gateway

Do not treat `mcp_server_operation_duration_count` as another HTTP request counter. An Envoy
Gateway observes HTTP envelopes, while this metric observes JSON-RPC requests and notifications
after SDK dispatch. A valid batch is one HTTP request but several MCP operations, and HTTP requests
rejected before MCP dispatch never increment the MCP metric.

Context7 deliberately does **not** register generic inbound HTTP server metrics. Keep the following
signals in the existing Envoy scrape instead of collecting them again from the application:

- downstream HTTP request/response totals, status classes, duration, active requests, connections,
  resets, and gateway timeouts (`envoy_http_*_downstream_*`)
- Envoy-to-MCP backend request totals, status codes, duration, active/pending requests, connection
  failures, retries, resets, timeouts, and circuit-breaker overflows (`envoy_cluster_upstream_*`)
- Envoy process health and resource metrics

The application exporter owns only signals the ingress gateway cannot provide: MCP method and
protocol semantics (including batches, notifications, and active MCP v2 subscriptions), tool and
authentication outcomes, MCP-to-Context7 API calls, and Node event-loop/V8 health. In the
Kubernetes deployment Envoy is a
Gateway API proxy rather than a sidecar in the MCP pod, so `context7_mcp_upstream_*` describes the
MCP server's outbound Context7 API dependency, not Envoy's inbound MCP backend cluster. Pod and
container CPU, memory, network, and restart metrics should continue to come from the Kubernetes
monitoring stack.

See the Envoy HTTP connection manager statistics
and upstream cluster statistics
for the proxy-owned metric families.

For a replicated Kubernetes deployment, discover and scrape every MCP pod directly. Do not use one
static, load-balanced Service target: successive scrapes can reach different replicas and produce
incomplete per-process counters and runtime series. For an annotation-based `kubernetes-pods`
scrape job, add the following fields to the MCP workload's pod template:

```yaml
spec:
  template:
    metadata:
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9464"
        prometheus.io/path: /metrics
    spec:
      containers:
        - name: mcp
          ports:
            - name: metrics
              containerPort: 9464
              protocol: TCP
```

Prometheus will then scrape `http://<mcp-pod-ip>:9464/metrics` for each replica. Declaring
`EXPOSE 9464` in the image does not add the Kubernetes `containerPort` metadata. The scrape interval
is controlled by Prometheus; the exporter does not impose one. If the monitoring stack uses the
Prometheus Operator instead, configure the equivalent per-pod endpoint with a `PodMonitor`.

Local Configuration Example

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["tsx", "/path/to/folder/context7/src/index.ts", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

### OAuth Authentication

Context7 MCP server supports OAuth 2.0 authentication for MCP clients that implement the MCP OAuth specification.

To use OAuth, change the endpoint from `/mcp` to `/mcp/oauth` in your client configuration:

```diff
- "url": "https://mcp.context7.com/mcp"
+ "url": "https://mcp.context7.com/mcp/oauth"
```

> **Note:** OAuth is not supported with stdio transport. For local MCP connections, use API key authentication instead.

Testing with MCP Inspector

```bash
npx -y @modelcontextprotocol/inspector npx @upstash/context7-mcp
```

## 🚨 Troubleshooting

Module Not Found Errors

If you encounter `ERR_MODULE_NOT_FOUND`, try using `bunx` instead of `npx`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "bunx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

This often resolves module resolution issues in environments where `npx` doesn't properly install or resolve packages.

ESM Resolution Issues

For errors like `Error: Cannot find module 'uriTemplate.js'`, try the `--experimental-vm-modules` flag:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "--node-options=--experimental-vm-modules", "@upstash/context7-mcp@1.0.6"]
    }
  }
}
```

TLS/Certificate Issues

Use the `--experimental-fetch` flag to bypass TLS-related problems:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "--node-options=--experimental-fetch", "@upstash/context7-mcp"]
    }
  }
}
```

General MCP Client Errors

1. Try adding `@latest` to the package name
2. Use `bunx` as an alternative to `npx`
3. Consider using `deno` as another alternative
4. Ensure you're using Node.js v20 or higher for native fetch support

## ⚠️ Disclaimer

1- Context7 projects are community-contributed and while we strive to maintain high quality, we cannot guarantee the accuracy, completeness, or security of all library documentation. Projects listed in Context7 are developed and maintained by their respective owners, not by Context7. If you encounter any suspicious, inappropriate, or potentially harmful content, please use the "Report" button on the project page to notify us immediately. We take all reports seriously and will review flagged content promptly to maintain the integrity and safety of our platform. By using Context7, you acknowledge that you do so at your own discretion and risk.

2- This repository hosts the MCP server’s source code. The supporting components — API backend, parsing engine, and crawling engine — are private and not part of this release.

## 🤝 Connect with Us

Stay updated and join our community:

- 📢 Follow us on X for the latest news and updates
- 🌐 Visit our Website
- 💬 Join our Discord Community

## 📺 Context7 In Media

- Better Stack: "Free Tool Makes Cursor 10x Smarter"
- Cole Medin: "This is Hands Down the BEST MCP Server for AI Coding Assistants"
- Income Stream Surfers: "Context7 + SequentialThinking MCPs: Is This AGI?"
- Julian Goldie SEO: "Context7: New MCP AI Agent Update"
- JeredBlu: "Context 7 MCP: Get Documentation Instantly + VS Code Setup"
- Income Stream Surfers: "Context7: The New MCP Server That Will CHANGE AI Coding"
- AICodeKing: "Context7 + Cline & RooCode: This MCP Server Makes CLINE 100X MORE EFFECTIVE!"
- Sean Kochel: "5 MCP Servers For Vibe Coding Glory (Just Plug-In & Go)"

## Vercel Marketplace OIDC

Vercel Marketplace resources can call the remote MCP server without a
long-lived Context7 API key. Obtain a fresh per-resource access token from
Vercel's Marketplace integration runtime and send it as the bearer credential:

```ts
import { getIntegrationToken } from "@vercel/integrations";

const authorization = `Bearer ${await getIntegrationToken("context7")}`;
```

The `getIntegrationToken` signature is based on Vercel's current provider
specification and may change before Marketplace OIDC is generally available.

Use `authorization` as the `Authorization` header when creating the MCP HTTP
transport. Create the transport inside the request that uses it so a short-lived
token is not retained across function invocations. Its `resource` claim must
match the Context7 resource created during Marketplace provisioning.

The hosted MCP service must be configured with the exact issuer and audience
assigned by Vercel when the Context7 Marketplace product is created:

```sh
VERCEL_MARKETPLACE_OIDC_ISSUER=https://integrations.vercel.com/oac_...
VERCEL_MARKETPLACE_OIDC_AUDIENCE=https://integrations.vercel.com/context7/icfg_...
```

## 📄 License

MIT
