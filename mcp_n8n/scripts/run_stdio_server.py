"""Convenience wrapper to run the n8n MCP server over stdio."""

from __future__ import annotations

import anyio
from mcp.server.stdio import stdio_server

from mcp_n8n.server import build_server


def main() -> None:
    async def _run() -> None:
        server = build_server()
        init_options = server.create_initialization_options()
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, init_options)

    anyio.run(_run)


if __name__ == "__main__":
    main()
