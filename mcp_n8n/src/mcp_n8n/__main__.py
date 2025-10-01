"""Entry point so the server can run via `python -m mcp_n8n`."""

from __future__ import annotations

import anyio
from mcp.server.stdio import stdio_server

from .server import build_server


async def _run() -> None:
    server = build_server()
    initialization_options = server.create_initialization_options()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, initialization_options)


def main() -> None:
    """Launch the MCP server over stdio."""

    anyio.run(_run)


if __name__ == "__main__":
    main()
