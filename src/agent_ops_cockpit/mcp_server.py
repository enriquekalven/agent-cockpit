try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.8.4 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
from tenacity import retry, wait_exponential, stop_after_attempt
import asyncio
import io
import contextlib
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server.stdio import stdio_server
from rich.console import Console
from agent_ops_cockpit.ops import arch_review as arch_mod
from agent_ops_cockpit.ops import policy_engine as policy_mod
from agent_ops_cockpit.eval import red_team as red_mod
from agent_ops_cockpit import optimizer as opt_mod
from agent_ops_cockpit.telemetry import telemetry
server = Server('agent-ops-cockpit')

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available AgentOps tools.
    """
    return [types.Tool(name='optimize_code', description='Audit agent code for optimizations (cost, performance, FinOps).', inputSchema={'type': 'object', 'properties': {'file_path': {'type': 'string', 'description': 'Path to the agent file'}, 'quick': {'type': 'boolean', 'description': 'Run in fast mode (skip live fetches)'}}, 'required': ['file_path']}), types.Tool(name='policy_audit', description='Validate input against declarative guardrail policies (forbidden topics, costs).', inputSchema={'type': 'object', 'properties': {'text': {'type': 'string', 'description': 'Agent input or output to validate'}}, 'required': ['text']}), types.Tool(name='architecture_review', description='Run a Google Well-Architected design review on a path.', inputSchema={'type': 'object', 'properties': {'path': {'type': 'string', 'description': 'Directory path to audit'}}, 'required': ['path']}), types.Tool(name='red_team_attack', description='Perform an adversarial security audit on agent logic.', inputSchema={'type': 'object', 'properties': {'agent_path': {'type': 'string', 'description': 'Path to the agent file'}}, 'required': ['agent_path']})]

@server.call_tool()
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """
    Execute AgentOps tools natively via MCP.
    """
    telemetry.track_event_sync("mcp_tool_call", {"tool_name": name})
    if not arguments:
        raise ValueError('Missing arguments')
    output_buffer = io.StringIO()
    capture_console = Console(file=output_buffer, force_terminal=False, width=100)
    with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
        if name == 'optimize_code':
            file_path = arguments.get('file_path')
            quick = arguments.get('quick', True)
            opt_mod.audit(file_path, interactive=False, quick=quick)
        elif name == 'policy_audit':
            text = arguments.get('text')
            engine = policy_mod.GuardrailPolicyEngine()
            try:
                engine.validate_input(text)
                capture_console.print(f"✅ Input passed policy validation: [bold]'{text[:50]}...'[/bold]")
            except policy_mod.PolicyViolation as e:
                capture_console.print(f'❌ [bold red]Policy Violation:[/bold red] {e.category} - {e.message}')
        elif name == 'architecture_review':
            path = arguments.get('path', '.')
            arch_mod.audit(path)
        elif name == 'red_team_attack':
            agent_path = arguments.get('agent_path')
            red_mod.audit(agent_path)
        else:
            raise ValueError(f'Unknown tool: {name}')
    return [types.TextContent(type='text', text=output_buffer.getvalue())]

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
async def main():
    telemetry.track_event_sync("mcp_server_start")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(server_name='agent-ops-cockpit', server_version='0.7.0', capabilities=server.get_capabilities(notification_options=NotificationOptions(), experimental_capabilities={})))
if __name__ == '__main__':
    asyncio.run(main())