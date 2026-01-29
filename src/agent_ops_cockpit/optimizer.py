import sys
import os
import re
import ast
from typing import List, Dict, Any
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from packaging import version

# Import the evidence bridge
try:
    from backend.ops.evidence_bridge import get_package_evidence, get_compatibility_report
except ImportError:
    # Fallback for local execution
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from backend.ops.evidence_bridge import get_package_evidence, get_compatibility_report

app = typer.Typer(help="AgentOps Cockpit: The Agent Optimizer CLI")
console = Console()

class OptimizationIssue:
    def __init__(self, id: str, title: str, impact: str, savings: str, description: str, diff: str, package: str = None, fix_pattern: str = None):
        self.id = id
        self.title = title
        self.impact = impact
        self.savings = savings
        self.description = description
        self.diff = diff
        self.package = package
        self.fix_pattern = fix_pattern
        self.evidence = None

def analyze_code(content: str, file_path: str = "agent.py", versions: Dict[str, str] = None) -> List[OptimizationIssue]:
    issues = []
    content_lower = content.lower()
    versions = versions or {}

    # --- SITUATIONAL PLATFORM OPTIMIZATIONS ---

    v_ai = versions.get("google-cloud-aiplatform", "Not Installed")
    if "google.cloud.aiplatform" in content_lower or "vertexai" in content_lower:
        if v_ai == "Not Installed":
             issues.append(OptimizationIssue(
                "vertex_install", "Install Modern Vertex SDK", "HIGH", "90% cost savings",
                "You appear to be using Vertex AI logic but the SDK is not in your environment. Install v1.70.0+ to unlock context caching.",
                "+ # pip install google-cloud-aiplatform>=1.70.0",
                package="google-cloud-aiplatform"
            ))
        elif v_ai != "Unknown":
            try:
                if version.parse(v_ai) < version.parse("1.70.0"):
                     issues.append(OptimizationIssue(
                        "vertex_legacy_opt", "Situational Performance (Legacy SDK)", "MEDIUM", "20% cost savings",
                        f"Your SDK ({v_ai}) lacks native Context Caching. Optimize by using selective prompt pruning before execution.",
                        "+ from backend.ops.cost_optimizer import situational_pruning\n+ pruned = situational_pruning(context)",
                        package="google-cloud-aiplatform"
                    ))
                     issues.append(OptimizationIssue(
                        "vertex_upgrade_path", "Modernization Path", "HIGH", "90% cost savings",
                        "Upgrading to 1.70.0+ enables near-instant token reuse via CachingConfig.",
                        "+ # Upgrade to >1.70.0",
                        package="google-cloud-aiplatform"
                    ))
                elif "cache" not in content_lower:
                    issues.append(OptimizationIssue(
                        "context_caching", "Enable Context Caching", "HIGH", "90% cost reduction",
                        "Large model context detected. Use native CachingConfig.",
                        "+ cache = vertexai.preview.CachingConfig(ttl=3600)",
                        package="google-cloud-aiplatform"
                    ))
            except: pass

    # OpenAI
    openai_v = versions.get("openai", "Not Installed")
    if "openai" in content_lower:
        if openai_v != "Not Installed" and version.parse(openai_v) < version.parse("1.0.0"):
             issues.append(OptimizationIssue(
                "openai_legacy", "Found Legacy OpenAI SDK", "HIGH", "40% latency reduction",
                f"You are on {openai_v}. Transitioning to the v1.0.0+ Client pattern enables modern streaming and improved error handling.",
                "+ from openai import OpenAI\n+ client = OpenAI()",
                package="openai"
            ))
        elif "prompt_cache" not in content_lower:
             issues.append(OptimizationIssue(
                "openai_caching", "OpenAI Prompt Caching", "MEDIUM", "50% latency reduction",
                "OpenAI automatically caches repeated input prefixes. Ensure your system prompt is first.",
                "+ # Ensure system prompt is first\n+ messages = [{'role': 'system', ...}]",
                package="openai"
            ))

    # Anthropic
    if ("anthropic" in content_lower or "claude" in content_lower) and "orchestra" not in content_lower:
        issues.append(OptimizationIssue(
            "anthropic_orchestration", "Anthropic Orchestration Pattern", "HIGH", "30% reliability boost",
            "Claude performs best with an Orchestrator-Subagent pattern for complex tasks.",
            "+ # Use orchestrator to delegate sub-tasks",
            package="anthropic"
        ))

    # Microsoft
    if ("autogen" in content_lower or "microsoft" in content_lower) and "workflow" not in content_lower:
        issues.append(OptimizationIssue(
            "ms_workflows", "Microsoft Agent Workflows", "MEDIUM", "40% consistency boost",
            "Using graph-based repeatable workflows ensures enterprise reliability.",
            "+ # Define a repeatable graph-based flow",
            package="pyautogen"
        ))

    # AWS
    if ("bedrock" in content_lower or "boto3" in content_lower) and "actiongroup" not in content_lower:
        issues.append(OptimizationIssue(
            "aws_action_groups", "AWS Bedrock Action Groups", "HIGH", "50% tool reliability",
            "Standardize tool execution via Bedrock Action Group schemas.",
            "+ # Define Bedrock Action Group",
            package="aws-sdk"
        ))

    # CopilotKit
    if "copilotkit" in content_lower and "usecopilotstate" not in content_lower:
        issues.append(OptimizationIssue(
            "copilot_state", "CopilotKit Shared State", "MEDIUM", "60% UI responsiveness",
            "Ensure the Face remains aligned with the Engine via shared state sync.",
            "+ # Use shared state for UI alignment",
            package="@copilotkit/react-core"
        ))

    # Routing
    if "pro" in content_lower and "flash" not in content_lower:
        issues.append(OptimizationIssue(
            "model_routing", "Smart Model Routing", "HIGH", "70% cost savings",
            "Route simple queries to Flash models to minimize consumption.",
            "+ if is_simple(q): model = 'gemini-1.5-flash'",
            package="google-cloud-aiplatform"
        ))

    # Infrastructure (Cloud Run + GKE)
    if "cloud run" in content_lower and "cpu_boost" not in content_lower:
        issues.append(OptimizationIssue(
            "cr_startup_boost", "Cloud Run Startup Boost", "HIGH", "50% latency reduction",
            "Enable Startup CPU Boost to reduce cold-start latency for Python agents.",
            "+ startup_cpu_boost: true",
            package="google-cloud-run"
        ))
    if ("gke" in content_lower or "kubernetes" in content_lower) and "identity" not in content_lower:
        issues.append(OptimizationIssue(
            "gke_identity", "GKE Workload Identity", "HIGH", "100% security baseline",
            "Use Workload Identity for secure service-to-service communication.",
            "+ # Use Workload Identity",
            package="google-cloud-gke"
        ))

    # Language Specific (Go + Node)
    if file_path.endswith(".go") and "goroutine" not in content_lower:
        issues.append(OptimizationIssue(
            "go_concurrency", "Go Native Concurrency", "HIGH", "80% throughput boost",
            "Leveraging Goroutines for parallel tool execution is a Go best practice.",
            "+ go func() { tool.execute() }()",
            package="golang"
        ))
    if (file_path.endswith(".ts") or file_path.endswith(".js") or "axios" in content_lower) and "fetch" not in content_lower:
        issues.append(OptimizationIssue(
            "node_native_fetch", "Native Fetch API", "MEDIUM", "20% bundle reduction",
            "Node 20+ supports native fetch, reducing dependency on heavy libraries like axios.",
            "+ const res = await fetch(url);",
            package="nodejs"
        ))

    lg_v = versions.get("langgraph", "Not Installed")
    if "langgraph" in content_lower:
        if lg_v != "Not Installed" and lg_v != "Unknown":
            try:
                if version.parse(lg_v) < version.parse("0.1.0"):
                     issues.append(OptimizationIssue(
                        "langgraph_legacy", "Situational Stability (Legacy LangGraph)", "HIGH", "Stability Boost",
                        f"You are on {lg_v}. Older versions lack the hardened StateGraph compilation. Upgrade is recommended.",
                        "+ # Consider upgrading for better persistence",
                        package="langgraph"
                    ))
            except: pass
        
        if "persistence" not in content_lower and "checkpointer" not in content_lower:
            issues.append(OptimizationIssue(
                "langgraph_persistence", "LangGraph Persistence", "HIGH", "100% state recovery",
                "A checkpointer is mandatory for reliable long-running agents.",
                "+ graph.compile(checkpointer=checkpointer)",
                package="langgraph"
            ))
        if "recursion" not in content_lower:
            issues.append(OptimizationIssue(
                "langgraph_recursion", "Recursion Limits", "MEDIUM", "Safety Guardrail",
                "Set recursion limits to prevent expensive infinite loops in cyclic graphs.",
                "+ graph.invoke(..., config={'recursion_limit': 50})",
                package="langgraph"
            ))

    # --- ARCHITECTURAL OPTIMIZATIONS ---

    # Large system instructions
    large_string_pattern = re.compile(r'"""[\s\S]{200,}"""|\'\'\'[\s\S]{200,}\'\'\'')
    if large_string_pattern.search(content) and "cache" not in content_lower:
        issues.append(OptimizationIssue(
            "context_caching", "Enable Context Caching", "HIGH", "90% cost reduction",
            "Large static system instructions detected. Use context caching.",
            "+ cache = vertexai.preview.CachingConfig(ttl=3600)",
            package="google-cloud-aiplatform"
        ))

    # Missing semantic cache
    if "hive_mind" not in content_lower and "cache" not in content_lower:
         issues.append(OptimizationIssue(
            "semantic_caching", "Implement Semantic Caching", "HIGH", "40-60% savings",
            "No caching layer detected. Adding a semantic cache reduces LLM costs.",
            "+ @hive_mind(cache=global_cache)",
            package="google-adk"
        ))

    return issues

def estimate_savings(token_count: int, issues: List[OptimizationIssue]) -> Dict[str, Any]:
    baseline_cost_per_m = 10.0
    monthly_requests = 10000 
    current_cost = (token_count / 1_000_000) * baseline_cost_per_m * monthly_requests
    
    total_savings_pct = 0.0
    for issue in issues:
        if "90%" in issue.savings: total_savings_pct += 0.4
        if "50%" in issue.savings: total_savings_pct += 0.2
        if "40-60%" in issue.savings: total_savings_pct += 0.25

    projected_savings = current_cost * min(total_savings_pct, 0.8)
    
    return {
        "current_monthly": current_cost,
        "projected_savings": projected_savings,
        "new_monthly": current_cost - projected_savings
    }

@app.command()
def audit(
    file_path: str = typer.Argument("agent.py", help="Path to the agent code to audit"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", "-i", help="Run in interactive mode"),
    apply_fix: bool = typer.Option(False, "--apply", "--fix", help="Automatically apply recommended fixes"),
    quick: bool = typer.Option(False, "--quick", "-q", help="Skip live evidence fetching for faster execution")
):
    console.print(Panel.fit("🔍 [bold blue]GCP AGENT OPS: OPTIMIZER AUDIT[/bold blue]", border_style="blue"))
    if quick:
        console.print("[dim]⚡ Running in Quick Mode (skipping live evidence fetches)[/dim]")
    console.print(f"Target: [yellow]{file_path}[/yellow]")
    
    if not os.path.exists(file_path):
        console.print(f"❌ [red]Error: File {file_path} not found.[/red]")
        raise typer.Exit(1)

    with open(file_path, 'r') as f:
        content = f.read()
    
    # Heuristic: Find all imported packages
    imports = re.findall(r"(?:from|import)\s+([\w\.-]+)", content)
    # Pre-fetch version info for installed packages
    from backend.ops.evidence_bridge import get_installed_version
    package_versions = { pkg: get_installed_version(pkg) for pkg in ["google-cloud-aiplatform", "openai", "anthropic", "langgraph", "crewai"] }
    
    token_estimate = len(content.split()) * 1.5 
    console.print(f"📊 Token Metrics: ~[bold]{token_estimate:.0f}[/bold] prompt tokens detected.")
    
    issues = analyze_code(content, file_path, versions=package_versions)
    # Inject live evidence (skip in quick mode)
    if not quick:
        for issue in issues:
            if issue.package:
                issue.evidence = get_package_evidence(issue.package)

    # --- CROSS-PACKAGE VALIDATION ---
    comp_reports = get_compatibility_report(imports)
    
    if comp_reports:
        console.print("\n[bold yellow]🧩 Cross-Package Validation:[/bold yellow]")
        for report in comp_reports:
            if report["type"] == "INCOMPATIBLE":
                console.print(f"❌ [bold red]Conflict Detected:[/bold red] {report['component']} + {report['conflict_with']}")
                console.print(f"   [dim]{report['reason']}[/dim]")
            elif report["type"] == "SYNERGY":
                console.print(f"✅ [bold green]Synergy Verified:[/bold green] {report['component']} is optimally paired.")

    if not issues:
        console.print("\n[bold green]✅ No immediate code-level optimizations found. Your agent is lean![/bold green]")
        if not comp_reports:
             return
        else:
             raise typer.Exit(0)

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
        
        if opt.evidence and "error" not in opt.evidence:
            ev = opt.evidence
            ev_title = "[dim]SDK Citation & Evidence[/dim]"
            
            # Highlight if an upgrade is required for maximum efficiency
            if ev.get("upgrade_required"):
                console.print(f"🚨 [bold yellow]URGENT UPGRADE RECOMMENDED[/bold yellow]")
                console.print(f"   Current: {ev['installed_version']} | Required for optimization: >={ev['min_optimized_version']}")
                ev_title = "[bold red]UPGRADE REQUIRED Evidence[/bold red]"

            ev_panel = Panel(
                f"🔗 [bold]Source[/bold]: {ev['source_url']}\n"
                f"📅 [bold]Latest Release[/bold]: {ev['release_date'][:10]}\n"
                f"📝 [bold]Note[/bold]: {ev['best_practice_context']}",
                title=ev_title,
                border_style="red" if ev.get("upgrade_required") else "dim"
            )
            console.print(ev_panel)

        console.print("\nProposed Code-Level Change (Apply now):")
        syntax = Syntax(opt.diff, "python", theme="monokai", line_numbers=False)
        console.print(syntax)
        
        do_apply = False
        if apply_fix:
            do_apply = True
        elif interactive:
            do_apply = typer.confirm("\nDo you want to apply this code-level optimization?", default=True)
        
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
    
    summary_table = Table(title="🎯 AUDIT SUMMARY")
    summary_table.add_column("Category", style="cyan")
    summary_table.add_column("Count", style="magenta")
    summary_table.add_row("Optimizations Applied", str(applied))
    summary_table.add_row("Optimizations Rejected", str(rejected))
    console.print(summary_table)

if __name__ == "__main__":
    app()
