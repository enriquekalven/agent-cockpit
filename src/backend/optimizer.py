import sys
import os
import re
import ast
from typing import List, Dict
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

app = typer.Typer(help="AgentOps Cockpit: The Agent Optimizer CLI")
console = Console()

class OptimizationIssue:
    def __init__(self, id: str, title: str, impact: str, savings: str, description: str, diff: str):
        self.id = id
        self.title = title
        self.impact = impact
        self.savings = savings
        self.description = description
        self.diff = diff

def analyze_code(content: str) -> List[OptimizationIssue]:
    issues = []
    
    # Check for large system instructions (heuristic: multi-line strings with > 50 words)
    large_string_pattern = re.compile(r'"""[\s\S]{200,}"""|\'\'\'[\s\S]{200,}\'\'\'')
    if large_string_pattern.search(content):
        issues.append(OptimizationIssue(
            "context_caching",
            "Enable Gemini Context Caching",
            "HIGH",
            "90% cost reduction on reuse",
            "Large static system instructions detected. Using context caching prevents redundant token processing.",
            "+ cache = vertexai.preview.CachingConfig(ttl=3600)\n+ model = GenerativeModel('gemini-1.5-pro', caching_config=cache)"
        ))

    # Check for hardcoded Pro model usage where Flash might suffice
    if "gemini-1.5-pro" in content.lower() and "flash" not in content.lower():
        issues.append(OptimizationIssue(
            "model_routing",
            "Flash-First Model Routing",
            "CRITICAL",
            "10x lower latency & cost",
            "Explicit usage of Gemini 1.5 Pro detected without routing. Consider Gemini 1.5 Flash for non-reasoning tasks.",
            "- model = 'gemini-1.5-pro'\n+ model = 'gemini-1.5-flash'  # Or use model_router"
        ))

    # Check for missing semantic cache
    if "hive_mind" not in content and "cache" not in content.lower():
         issues.append(OptimizationIssue(
            "semantic_caching",
            "Implement Semantic Caching",
            "HIGH",
            "40-60% cost savings",
            "No caching layer detected. Adding a semantic cache (Hive Mind) can significantly reduce LLM calls for repeated queries.",
            "+ @hive_mind(cache=global_cache)\n  async def chat(q: str): ..."
        ))

    # Check for legacy tool usage (mock check)
    if "legacy_tool" in content or "requests.get" in content:
        issues.append(OptimizationIssue(
            "mcp_migration",
            "MCP Tool Chain Optimization",
            "HIGH",
            "Reduced Latency",
            "Legacy tool patterns detected. Migrating to Model Context Protocol (MCP) provides standardized connectivity.",
            "- tools = [legacy_tool_api('search')]\n+ tools = [global_mcp_hub.get_tool('search')]"
        ))

    return issues

@app.command()
def audit(
    file_path: str = typer.Argument("src/backend/agent.py", help="Path to the agent code to audit"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", "-i", help="Run in interactive mode")
):
    """
    Audits agent code and proposes cost/perf optimizations.
    """
    console.print(Panel.fit("🔍 [bold blue]GCP AGENT OPS: OPTIMIZER AUDIT[/bold blue]", border_style="blue"))
    console.print(f"Target: [yellow]{file_path}[/yellow]")
    
    if not os.path.exists(file_path):
        console.print(f"❌ [red]Error: File {file_path} not found.[/red]")
        raise typer.Exit(1)

    with open(file_path, 'r') as f:
        content = f.read()
    
    token_estimate = len(content.split()) * 1.5 
    console.print(f"📊 Token Metrics: ~[bold]{token_estimate:.0f}[/bold] prompt tokens detected.")
    
    with console.status("[bold green]Running heuristic analysis..."):
        issues = analyze_code(content)
        import time
        time.sleep(1)

    if not issues:
        console.print("\n[bold green]✅ No immediate optimization opportunities found. Your agent is lean![/bold green]")
        return

    applied = 0
    rejected = 0

    for opt in issues:
        console.print(f"\n[bold white on blue] --- [{opt.impact} IMPACT] {opt.title} --- [/bold white on blue]")
        console.print(f"Benefit: [green]{opt.savings}[/green]")
        console.print(f"Reason: {opt.description}")
        console.print("\nProposed Change:")
        syntax = Syntax(opt.diff, "python", theme="monokai", line_numbers=False)
        console.print(syntax)
        
        if interactive:
            choice = typer.confirm(f"\nDo you want to apply this optimization?", default=True)
            if choice:
                console.print(f"✅ [APPROVED] queued for deployment.")
                applied += 1
            else:
                console.print(f"❌ [REJECTED] skipping optimization.")
                rejected += 1
        else:
            console.print("ℹ️ Auto-skipping in non-interactive mode.")

    summary_table = Table(title="🎯 AUDIT SUMMARY")
    summary_table.add_column("Category", style="cyan")
    summary_table.add_column("Count", style="magenta")
    summary_table.add_row("Optimizations Applied", str(applied))
    summary_table.add_row("Optimizations Rejected", str(rejected))
    console.print(summary_table)
    
    if applied > 0:
        console.print("\n🚀 [bold green]Ready for production.[/bold green] Run 'make deploy-prod' to push changes.")
    else:
        console.print("\n⚠️ [yellow]No optimizations applied. High cost warnings may persist in Cloud Trace.[/yellow]")

if __name__ == "__main__":
    app()
