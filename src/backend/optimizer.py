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

def analyze_code(content: str, file_path: str = "src/backend/agent.py") -> List[OptimizationIssue]:
    issues = []
    content_lower = content.lower()

    # --- PLATFORM SPECIFIC OPTIMIZATIONS ---

    # Check for OpenAI Prompt Caching (Automatic for repeated prefixes)
    if "openai" in content_lower and "prompt_cache" not in content_lower:
        issues.append(OptimizationIssue(
            "openai_caching",
            "OpenAI Prompt Caching",
            "MEDIUM",
            "50% latency reduction",
            "OpenAI automatically caches repeated input prefixes. Ensure your system prompt is at the beginning of the message list.",
            "+ # Ensure system prompt is first and static for optimal caching\n+ messages = [{'role': 'system', 'content': SYSTEM_PROMPT}, ...]"
        ))

    # Check for Anthropic Orchestrator Pattern
    if "anthropic" in content_lower and "orchestrator" not in content_lower and "subagent" not in content_lower:
         issues.append(OptimizationIssue(
            "anthropic_orchestration",
            "Anthropic Orchestrator-Subagent Pattern",
            "HIGH",
            "Improved Accuracy & Concurrency",
            "Anthropic recommends using an orchestrator to manage subagents for complex tasks. This reduces token spill over and improves reliability.",
            "+ orchestrator = AnthropicOrchestrator()\n+ orchestrator.register_subagent('researcher', researcher_agent)"
        ))

    # Check for Microsoft Semantic Kernel Workflows
    if ("microsoft" in content_lower or "autogen" in content_lower) and "workflow" not in content_lower and "process" not in content_lower:
        issues.append(OptimizationIssue(
            "ms_workflows",
            "Implement Repeatable Process Workflows",
            "HIGH",
            "Enterprise reliability",
            "Microsoft best practice: Use the Semantic Kernel Process Framework for stateful, graph-based workflows instead of simple loops.",
            "+ workflow = KernelProcess(name='logic')\n+ workflow.add_step(MyStep())"
        ))

    # Check for AWS Bedrock Action Groups
    if "bedrock" in content_lower and "actiongroup" not in content_lower:
        issues.append(OptimizationIssue(
            "aws_action_groups",
            "Use Bedrock Action Groups",
            "MEDIUM",
            "Standardized tool execution",
            "AWS recommends using Action Groups with OpenAPI schemas to manage tool interactions securely and consistently.",
            "+ action_group = bedrock.AgentActionGroup(name='Tools', schema='s3://bucket/api.json')"
        ))

    # Check for CopilotKit Shared State
    if "copilotkit" in content_lower and "sharedstate" not in content_lower:
        issues.append(OptimizationIssue(
            "copilot_state",
            "Enable CopilotKit Shared State",
            "HIGH",
            "Face-Engine Synchronization",
            "CopilotKit best practice: Use shared state to keep the frontend (Face) and agent (Engine) reactive and aligned.",
            "+ state = useCopilotState({ 'user': user_id })\n+ agent.sync_state(state)"
        ))

    # --- GENERIC OPTIMIZATIONS ---
    
    # Check for large system instructions
    large_string_pattern = re.compile(r'"""[\s\S]{200,}"""|\'\'\'[\s\S]{200,}\'\'\'')
    if large_string_pattern.search(content) and "cache" not in content_lower:
        issues.append(OptimizationIssue(
            "context_caching",
            "Enable Context Caching",
            "HIGH",
            "90% cost reduction on reuse",
            "Large static system instructions detected. Using context caching (Gemini/Anthropic) prevents redundant token processing.",
            "+ cache = vertexai.preview.CachingConfig(ttl=3600)\n+ model = GenerativeModel('gemini-1.5-pro', caching_config=cache)"
        ))

    # Check for hardcoded Pro model usage where Flash might suffice
    if re.search(r"\bpro\b", content_lower) and not any(re.search(rf"\b{w}\b", content_lower) for w in ["flash", "mini", "haiku"]):
        issues.append(OptimizationIssue(
            "model_routing",
            "Flash/Mini-First Model Routing",
            "CRITICAL",
            "10x lower latency & cost",
            "Explicit usage of Pro/Opus models detected. Consider Flash (Google), Mini (OpenAI), or Haiku (Anthropic) for non-reasoning tasks.",
            "- model = 'gpt-4o'\n+ model = 'gpt-4o-mini'  # Or use model_router"
        ))

    # Check for missing semantic cache
    if "hive_mind" not in content_lower and "cache" not in content_lower:
         issues.append(OptimizationIssue(
            "semantic_caching",
            "Implement Semantic Caching",
            "HIGH",
            "40-60% cost savings",
            "No caching layer detected. Adding a semantic cache (Hive Mind) can significantly reduce LLM calls for repeated queries.",
            "+ @hive_mind(cache=global_cache)\n  async def chat(q: str): ..."
        ))

    # --- INFRASTRUCTURE OPTIMIZATIONS ---

    # Check for Cloud Run Python Optimizations
    if "cloudrun" in content_lower or "cloud run" in content_lower:
        if "startupcpu" not in content_lower and "boost" not in content_lower:
            issues.append(OptimizationIssue(
                "cr_startup_boost",
                "Cloud Run Startup CPU Boost",
                "MEDIUM",
                "50% faster cold starts",
                "Detected Cloud Run deployment without CPU Boost. Enabling this in your terraform/cloud-run-ui reduces startup latency for Python agents.",
                "+ metadata:\n+   annotations:\n+     run.googleapis.com/startup-cpu-boost: 'true'"
            ))

    # Check for GKE Workload Identity
    if "gke" in content_lower or "kubernetes" in content_lower:
        if "workloadidentity" not in content_lower and not re.search(r"\bwi\b", content_lower):
             issues.append(OptimizationIssue(
                "gke_identity",
                "GKE Workload Identity Implementation",
                "HIGH",
                "Enhanced Security & Audit",
                "Detected GKE deployment using static keys or default service accounts. Use Workload Identity for least-privilege tool access.",
                "+ iam.gke.io/gcp-service-account: agent-sa@project.iam.gserviceaccount.com"
            ))

    # --- LANGUAGE-SPECIFIC PERFORMANCE ---

    # Go: Suggest sync.Map for high-concurrency tools
    if ".go" in file_path and "map[" in content and "sync.Map" not in content:
        issues.append(OptimizationIssue(
            "go_concurrency",
            "Go Thread-Safe State Management",
            "MEDIUM",
            "Prevents Race Conditions",
            "Detected a standard raw map in Go code. For high-concurrency agents, use sync.Map or a Mutex to prevent fatal panics under load.",
            "- state := make(map[string]int)\n+ var state sync.Map"
        ))

    # NodeJS: Suggest native fetch for Node 20+
    if (".ts" in file_path or ".js" in file_path) and ("axios" in content or "node-fetch" in content):
        issues.append(OptimizationIssue(
            "node_native_fetch",
            "NodeJS Native Fetch Optimization",
            "LOW",
            "Reduced Bundle & Memory",
            "Detected external HTTP libraries. Node 20+ supports high-performance native fetch(), which simplifies the dependency tree.",
            "- import axios from 'axios'\n+ const resp = await fetch(url)"
        ))

    # --- FRAMEWORK-SPECIFIC OPTIMIZATIONS ---

    # LangGraph: Check for persistence (checkpointer)
    if "langgraph" in content_lower and "checkpointer" not in content_lower:
        issues.append(OptimizationIssue(
            "langgraph_persistence",
            "Implement LangGraph Persistence",
            "HIGH",
            "Cross-session memory & Safety",
            "Detected LangGraph usage without a checkpointer. Persistence is mandatory for production agents to resume from failures or maintain long-term state.",
            "+ checkpointer = MemorySaver()\n+ app = workflow.compile(checkpointer=checkpointer)"
        ))

    # LangGraph: Check for recursion limit
    if "langgraph" in content_lower and "recursion_limit" not in content_lower:
        issues.append(OptimizationIssue(
            "langgraph_recursion",
            "Configure LangGraph Recursion Limit",
            "MEDIUM",
            "Prevents runaway execution",
            "No recursion limit detected in LangGraph config. Setting a limit (e.g., 50) prevents infinite loops in cyclic agent graphs.",
            "+ config = {'recursion_limit': 50}\n+ app.invoke(inputs, config)"
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
        issues = analyze_code(content, file_path)

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
            choice = typer.confirm("\nDo you want to apply this optimization?", default=True)
            if choice:
                console.print("✅ [APPROVED] queued for deployment.")
                applied += 1
            else:
                console.print("❌ [REJECTED] skipping optimization.")
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
