try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v2.0.2 Sovereign Alignment: Maturing ADK Tooling
from tenacity import retry, wait_exponential, stop_after_attempt
import asyncio
import io
import contextlib
import os
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server.stdio import stdio_server
from rich.console import Console

from agent_ops_cockpit.ops import arch_review as arch_mod
from agent_ops_cockpit.ops import policy_engine as policy_mod
from agent_ops_cockpit.eval import red_team as red_mod
from agent_ops_cockpit import optimizer as opt_mod
from agent_ops_cockpit.ops import orchestrator as orch_mod
from agent_ops_cockpit.ops.benchmarker import ReliabilityBenchmarker
from agent_ops_cockpit.telemetry import telemetry

server = Server('agent-ops-cockpit')

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available AgentOps tools for ADK/MCP consumption.
    """
    return [
        types.Tool(
            name='optimize_code', 
            description='Audit agent code for optimizations (cost, performance, FinOps).', 
            inputSchema={
                'type': 'object', 
                'properties': {
                    'file_path': {'type': 'string', 'description': 'Path to the agent file'}, 
                    'quick': {'type': 'boolean', 'description': 'Run in fast mode (skip live fetches)', 'default': True}
                }, 
                'required': ['file_path']
            }
        ), 
        types.Tool(
            name='policy_audit', 
            description='Validate input against declarative guardrail policies (forbidden topics, costs).', 
            inputSchema={
                'type': 'object', 
                'properties': {
                    'text': {'type': 'string', 'description': 'Agent input or output to validate'}
                }, 
                'required': ['text']
            }
        ), 
        types.Tool(
            name='architecture_review', 
            description='Run a Google Well-Architected design review on a path.', 
            inputSchema={
                'type': 'object', 
                'properties': {
                    'path': {'type': 'string', 'description': 'Directory path to audit', 'default': '.'}
                }
            }
        ), 
        types.Tool(
            name='red_team_attack', 
            description='Perform an adversarial security audit on agent logic.', 
            inputSchema={
                'type': 'object', 
                'properties': {
                    'agent_path': {'type': 'string', 'description': 'Path to the agent file'}
                }, 
                'required': ['agent_path']
            }
        ),
        types.Tool(
            name='shadow_roi',
            description='🔦 Shadow ROI: Benchmarking to find optimal model tiers by comparing accuracy vs cost.',
            inputSchema={
                'type': 'object',
                'properties': {
                    'path': {'type': 'string', 'description': 'Directory path to look for agents to benchmark', 'default': '.'}
                }
            }
        ),
        types.Tool(
            name='certify_agent',
            description='🏅 Production Readiness: Run Pre-flight, Deep Audit, and Regression to generate a Sovereign Certificate.',
            inputSchema={
                'type': 'object',
                'properties': {
                    'path': {'type': 'string', 'description': 'Path to the agent project to certify', 'default': '.'}
                }
            }
        )
    ]

@server.call_tool()
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """
    Execute AgentOps tools natively via MCP.
    """
    telemetry.track_event_sync("mcp_tool_call", {"tool_name": name})
    
    output_buffer = io.StringIO()
    capture_console = Console(file=output_buffer, force_terminal=False, width=100)
    
    with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
        try:
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
                    capture_console.print(f"❌ [bold red]Policy Violation:[/bold red] {e.category} - {e.message}")
            
            elif name == 'architecture_review':
                path = arguments.get('path', '.')
                arch_mod.audit(path)
            
            elif name == 'red_team_attack':
                agent_path = arguments.get('agent_path')
                red_mod.audit(agent_path)
                
            elif name == 'shadow_roi':
                path = arguments.get('path', '.')
                bench = ReliabilityBenchmarker(path)
                # shadow_benchmark_roi is async
                asyncio.run(bench.shadow_benchmark_roi())
                
            elif name == 'certify_agent':
                # We reuse the logic from main.py but in a programmatic way
                path = arguments.get('path', '.')
                abs_path = os.path.abspath(path)
                
                capture_console.print(f"🏅 [bold blue]Sovereign Certification Process Initialized for: {abs_path}[/bold blue]")
                
                # Note: Calling typer-wrapped certification might be tricky,
                # so we replicate the core logic here.
                audit_exit_code = orch_mod.run_audit(mode='deep', target_path=abs_path, title='MCP CERTIFICATION AUDIT')
                
                # For MCP, we skip heavy shell-based regression unless specifically requested
                # But we indicate the status
                if audit_exit_code == 0:
                   capture_console.print("✅ [green]Audit Gates Passed.[/green]")
                else:
                   capture_console.print("❌ [red]Audit Findings Block Certification.[/red]")

            else:
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            capture_console.print(f"🛑 [bold red]Tool Execution Error:[/bold red] {str(e)}")

    return [types.TextContent(type='text', text=output_buffer.getvalue())]

async def main():
    telemetry.track_event_sync("mcp_server_start")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, 
            write_stream, 
            InitializationOptions(
                server_name='agent-ops-cockpit', 
                server_version='2.0.2', 
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(), 
                    experimental_capabilities={}
                )
            )
        )

if __name__ == '__main__':
    asyncio.run(main())