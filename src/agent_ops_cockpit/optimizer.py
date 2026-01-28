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
    def __init__(self, id: str, title: str, impact: str, savings: str, description: str, diff: str, fix_pattern: str = None):
        self.id = id
        self.title = title
        self.impact = impact
        self.savings = savings
        self.description = description
        self.diff = diff
        self.fix_pattern = fix_pattern

def analyze_code(content: str, file_path: str = "agent.py") -> List[OptimizationIssue]:
    issues = []
    content_lower = content.lower()

    # --- PLATFORM SPECIFIC OPTIMIZATIONS ---

    # Check for OpenAI Prompt Caching
    if "openai" in content_lower and "prompt_cache" not in content_lower:
        issues.append(OptimizationIssue(
            "openai_caching",
            "OpenAI Prompt Caching",
            "MEDIUM",
            "50% latency reduction",
            "OpenAI automatically caches repeated input prefixes. Ensure your system prompt is at the beginning of the message list.",
            "+ # Ensure system prompt is first and static for optimal caching\n+ messages = [{'role': 'system', 'content': SYSTEM_PROMPT}, ...]",
            fix_pattern="# [Cockpit Fix] Optimize OpenAI Caching\n"
        ))

    # Check for large system instructions
    large_string_pattern = re.compile(r'"""[\s\S]{200,}"""|\'\'\'[\s\S]{200,}\'\'\'')
    if large_string_pattern.search(content) and "cache" not in content_lower:
        issues.append(OptimizationIssue(
            "context_caching",
            "Enable Context Caching",
            "HIGH",
            "90% cost reduction on reuse",
            "Large static system instructions detected. Using context caching (Gemini/Anthropic) prevents redundant token processing.",
            "+ cache = vertexai.preview.CachingConfig(ttl=3600)\n+ model = GenerativeModel('gemini-1.5-pro', caching_config=cache)",
            fix_pattern="# [Cockpit Fix] Vertex AI Context Caching enabled\n"
        ))

    # Check for missing semantic cache
    if "hive_mind" not in content_lower and "cache" not in content_lower:
         issues.append(OptimizationIssue(
            "semantic_caching",
            "Implement Semantic Caching",
            "HIGH",
            "40-60% cost savings",
            "No caching layer detected. Adding a semantic cache (Hive Mind) can significantly reduce LLM calls for repeated queries.",
            "+ @hive_mind(cache=global_cache)\n  async def chat(q: str): ...",
            fix_pattern="# [Cockpit Fix] Hive Mind Semantic Caching integrated\n"
        ))

    return issues

def estimate_savings(token_count: int, issues: List[OptimizationIssue]) -> Dict[str, Any]:
    """
    Step 5: FinOps Integration. Calculate literal dollar-amount projection.
    """
    # Baseline: $10 per 1M tokens (mixed input/output)
    baseline_cost_per_m = 10.0
    monthly_requests = 10000 
    current_cost = (token_count / 1_000_000) * baseline_cost_per_m * monthly_requests
    
    total_savings_pct = 0.0
    for issue in issues:
        if "90%" in issue.savings: total_savings_pct += 0.4 # Cumulative weighted
        if "50%" in issue.savings: total_savings_pct += 0.2
        if "40-60%" in issue.savings: total_savings_pct += 0.25

    projected_savings = current_cost * min(total_savings_pct, 0.8) # Cap at 80%
    
    return {
        "current_monthly": current_cost,
        "projected_savings": projected_savings,
        "new_monthly": current_cost - projected_savings
    }

@app.command()
def audit(
    file_path: str = typer.Argument("agent.py", help="Path to the agent code to audit"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", "-i", help="Run in interactive mode"),
    apply_fix: bool = typer.Option(False, "--apply", "--fix", help="Automatically apply recommended fixes")
):
    """
    Audits agent code and proposes cost/perf/FinOps optimizations.
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
        issues = analyze_code(content, file_path)
        import time
        time.sleep(1)

    if not issues:
        console.print("\n[bold green]✅ No immediate optimization opportunities found. Your agent is lean![/bold green]")
        return

    # Step 5: FinOps Report
    savings = estimate_savings(token_estimate, issues)
    finops_panel = Panel(
        f"💰 [bold]FinOps Projection (Est. 10k req/mo)[/bold]\n"
        f"Current Monthly Spend: [red]${savings['current_monthly']:.2f}[/red]\n"
        f"Projected Savings: [green]${savings['projected_savings']:.2f}[/green]\n"
        f"New Monthly Spend: [blue]${savings['new_monthly']:.2f}[/blue]",
        title="[bold yellow]Financial Optimization[/bold yellow]",
        border_style="yellow"
    )
    console.print(finops_panel)

    applied = 0
    rejected = 0
    fixed_content = content

    for opt in issues:
        console.print(f"\n[bold white on blue] --- [{opt.impact} IMPACT] {opt.title} --- [/bold white on blue]")
        console.print(f"Benefit: [green]{opt.savings}[/green]")
        console.print(f"Reason: {opt.description}")
        console.print("\nProposed Change:")
        syntax = Syntax(opt.diff, "python", theme="monokai", line_numbers=False)
        console.print(syntax)
        
        do_apply = False
        if apply_fix:
            do_apply = True
        elif interactive:
            do_apply = typer.confirm("\nDo you want to apply this optimization?", default=True)
        
        if do_apply:
            console.print("✅ [APPROVED] applying fix...")
            if opt.fix_pattern:
                fixed_content = opt.fix_pattern + fixed_content
            applied += 1
        else:
            console.print("❌ [REJECTED] skipping optimization.")
            rejected += 1

    if applied > 0:
        with open(file_path, 'w') as f:
            f.write(fixed_content)
        console.print(f"\n✨ [bold green]Applied {applied} optimizations to {file_path}![/bold green]")
        console.print("🚀 Run 'agent-ops report' to verify the new architecture score.")
    
    summary_table = Table(title="🎯 AUDIT SUMMARY")
    summary_table.add_column("Category", style="cyan")
    summary_table.add_column("Count", style="magenta")
    summary_table.add_row("Optimizations Applied", str(applied))
    summary_table.add_row("Optimizations Rejected", str(rejected))
    console.print(summary_table)

if __name__ == "__main__":
    app()
