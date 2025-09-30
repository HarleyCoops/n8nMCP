# n8n MCP Server

This package contains a standalone [Model Context Protocol](https://modelcontextprotocol.io/) (MCP)
server that exposes tools for managing [n8n](https://n8n.io/) workflows. Once installed, the server
can be registered with Claude Code (or any other MCP-compatible client) so that you can list,
inspect, create, update, and activate n8n workflows directly from your IDE.

The layout is intentionally verbose and self-contained so you can understand each piece without
needing an existing Python project.

```
mcp_n8n/
├── README.md              # High-level explanation and setup instructions (this file)
├── pyproject.toml         # Python packaging metadata and dependency list
├── .env.example           # Sample environment variables used by the server
├── scripts/
│   └── run_stdio_server.py# Convenience wrapper to launch the server over stdio
└── src/
    └── mcp_n8n/
        ├── __init__.py    # Package marker + exports
        ├── __main__.py    # Entry point executed by `python -m mcp_n8n`
        ├── client.py      # Thin async wrapper around the n8n REST API
        ├── config.py      # Pydantic settings that load configuration from env or .env files
        ├── schemas.py     # Pydantic request/response models shared by the MCP tools
        └── server.py      # MCP server definition (tool metadata + tool execution handlers)
```

The following sections walk through installation, configuration, and testing.

## 1. Prerequisites

1. Python 3.10 or newer installed locally.
2. Access to an n8n instance (local Docker container or remote server).
3. Claude Code desktop app or VS Code extension already running with MCP support enabled.

## 2. Installation

```bash
cd mcp_n8n
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e .
```

The editable install (`-e .`) makes it easy to tweak the code while Claude Code is running.

## 3. Configure Environment Variables

Copy the sample environment file and adjust the values so the server can talk to your n8n instance.

```bash
cp .env.example .env
```

| Variable | Description |
| --- | --- |
| `N8N_MCP_BASE_URL` | Base URL of the n8n REST API (usually `http://localhost:5678`). |
| `N8N_MCP_API_KEY` | Optional n8n API key. Provide this if API key auth is enabled. |
| `N8N_MCP_USERNAME`/`N8N_MCP_PASSWORD` | Optional basic-auth credentials. These are only used if both are provided. |
| `N8N_MCP_VERIFY_SSL` | Set to `false` when connecting to self-signed HTTPS endpoints. |
| `N8N_MCP_TIMEOUT` | Request timeout in seconds (default `30`). |

> The settings loader also understands the legacy n8n environment variables `N8N_API_KEY`,
> `N8N_BASIC_AUTH_USER`, and `N8N_BASIC_AUTH_PASSWORD` so the server can reuse existing `.env`
> files from your Docker setup.

## 4. Register the server with Claude Code

Add the following block to your Claude Code configuration file. On macOS this typically lives at
`~/Library/Application Support/Claude/claude_desktop_config.json`. Replace the `command` path with
the location of your virtual environment.

```json
{
  "mcpServers": {
    "n8n": {
      "command": "/absolute/path/to/mcp_n8n/.venv/bin/python",
      "args": ["-m", "mcp_n8n"],
      "env": {
        "N8N_MCP_BASE_URL": "http://localhost:5678",
        "N8N_MCP_API_KEY": "your-api-key"
      }
    }
  }
}
```

On Windows, the `command` would look like
`"C:/path/to/mcp_n8n/.venv/Scripts/python.exe"`.

Whenever Claude Code starts it will launch the MCP server using stdio and automatically detect the
available tools.

## 5. Usage Overview

Once connected, Claude Code will surface the following tools:

| Tool name | Description |
| --- | --- |
| `n8n_list_workflows` | Returns the workflows visible to the authenticated user. |
| `n8n_get_workflow` | Fetches the full JSON definition for a workflow ID. |
| `n8n_create_workflow` | Creates a new workflow from a JSON definition (optional activation). |
| `n8n_update_workflow` | Updates an existing workflow with new JSON data (optional activation). |
| `n8n_toggle_workflow` | Activates or deactivates a workflow. |
| `n8n_delete_workflow` | Removes a workflow by ID. |

Each tool returns both a human-readable message and machine-readable JSON so agents can chain calls
reliably.

## 6. Local smoke test

You can verify the server independently of Claude Code by running it in one terminal and connecting
with the reference MCP client in another.

```bash
# Terminal 1
python -m mcp_n8n

# Terminal 2 (separate shell)
mcp-client --stdio --command "python" -- "-m" "mcp_n8n"
```

The `mcp-client` command ships with the `mcp` Python package. Use Ctrl+C to exit.

## 7. Next steps

* Edit `src/mcp_n8n/schemas.py` to add more structured tooling (for example workflow templates).
* Extend `src/mcp_n8n/client.py` with credential helpers, execution logs, etc.
* Wire this server into n8n itself by creating workflows that call the MCP tools.

