from typing import List, Dict, Any
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPHub:
    """
    Model Context Protocol (MCP) Hub.
    Provides a unified interface for tool discovery and execution across
    multiple MCP servers (Google Search, SQL, internal tools).
    """

    def __init__(self):
        self.servers: Dict[str, StdioServerParameters] = {}
        self.registry = {
            "search": {"type": "mcp", "provider": "google-search", "server": "google-search-mcp"},
            "db": {"type": "mcp", "provider": "alloydb", "server": "postgres-mcp"},
            "legacy_crm": {"type": "rest", "provider": "internal", "status": "deprecated"}
        }

    def register_server(self, name: str, command: str, args: List[str] = None):
        """Registers a local MCP server."""
        self.servers[name] = StdioServerParameters(
            command=command,
            args=args or [],
            env=os.environ.copy()
        )

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]):
        """
        Executes a tool call using the Model Context Protocol.
        """
        if tool_name not in self.registry:
            raise ValueError(f"Tool {tool_name} not found in MCP registry.")

        config = self.registry[tool_name]
        
        # If it's a legacy tool, handle it separately
        if config["type"] == "rest":
            print(f"⚠️  Executing legacy REST tool: {tool_name}")
            return await self._mock_legacy_exec(tool_name, arguments)

        server_name = config.get("server")
        if not server_name or server_name not in self.servers:
            # Fallback to mock for demo/unconfigured environments
            print(f"ℹ️  MCP Server '{server_name}' not configured. Running in simulated mode.")
            return await self._mock_mcp_exec(tool_name, arguments)

        # Real MCP Protocol Execution
        async with stdio_client(self.servers[server_name]) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return {
                    "result": result.content,
                    "protocol": "mcp-v1",
                    "server": server_name
                }

    async def _mock_mcp_exec(self, tool_name: str, args: Dict[str, Any]):
        await asyncio.sleep(0.2)
        return {
            "result": f"Simulated MCP response for {tool_name}",
            "protocol": "mcp-virtual",
            "assurance": 0.95
        }

    async def _mock_legacy_exec(self, tool_name: str, args: Dict[str, Any]):
        await asyncio.sleep(0.5)
        return {
            "result": f"Legacy response for {tool_name}",
            "protocol": "rest-legacy",
            "warning": "MIGRATE_TO_MCP"
        }

global_mcp_hub = MCPHub()
# Example registration (commented out as it requires local binaries)
# global_mcp_hub.register_server("google-search-mcp", "npx", ["-y", "@modelcontextprotocol/server-google-search"])
