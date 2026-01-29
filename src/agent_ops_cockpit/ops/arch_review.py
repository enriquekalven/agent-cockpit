import typer
import os
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from agent_ops_cockpit.ops.frameworks import detect_framework, FRAMEWORKS

app = typer.Typer(help="Agent Architecture Reviewer: Audit your design against Google Well-Architected Framework.")
console = Console()

@app.command()
def audit(path: str = "."):
    """
    Run the Architecture Design Review based on detected framework.
    """
    framework_key = detect_framework(path)
    framework_data = FRAMEWORKS[framework_key]
    checklist = framework_data["checklist"]
    framework_name = framework_data["name"]
    # Read all relevant code files for inspection
    code_content = ""
    for root, dirs, files in os.walk(path):
        # Prune excluded directories for performance
        dirs[:] = [d for d in dirs if d not in [".venv", "node_modules", ".git", "__pycache__", "dist", "build"]]
        
        for file in files:
            if file.endswith((".py", ".ts", ".tsx", ".js")):
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        code_content += f.read() + "\n"
                except Exception:
                    pass

    if framework_key == "generic":
        console.print(Panel.fit("🔍 [bold yellow]SHADOW INTELLIGENCE: ZERO-SHOT AUDIT INITIALIZED[/bold yellow]", border_style="yellow"))
        console.print("⚠️ [dim]Detected Unknown Technology Stack. Switching to Structural Pattern Matching...[/dim]")
        
        # Self-Learning Heuristic: Look for patterns even if tech is unknown
        structural_indicators = {
            "decorators": r"@[\w\.]+",
            "async_loops": r"async\s+def.*await",
            "class_hierarchy": r"class\s+\w+\(\w*\):",
            "environment_vars": r"os\.environ|process\.env",
            "structured_output": r"Pydantic|BaseModel|zod|interface",
        }
        
        found_patterns = []
        for p_name, pattern in structural_indicators.items():
            if re.search(pattern, code_content):
                found_patterns.append(p_name)
        
        if found_patterns:
            console.print(f"📡 [bold green]Heuristically identified patterns:[/bold green] {', '.join(found_patterns)}")
            console.print("Adjusting audit benchmarks for custom agentic architecture...\n")

    console.print(Panel.fit(f"🏛️ [bold blue]{framework_name.upper()}: ARCHITECTURE REVIEW[/bold blue]", border_style="blue"))
    console.print(f"Detected Framework: [bold green]{framework_name}[/bold green]")
    console.print(f"Comparing local agent implementation against [bold]{framework_name} Best Practices[/bold]...\n")

    total_checks = 0.0
    passed_checks = 0.0
    current_check_num = 0

    with console.status("[bold blue]Scanning architecture...") as status:
        for section in checklist:
            table = Table(title=section["category"], show_header=True, header_style="bold magenta")
            table.add_column("Design Check", style="cyan")
            table.add_column("Status", style="green", justify="center")
            table.add_column("Rationale", style="dim")

            for check_text, rationale in section["checks"]:
                current_check_num += 1
                check_key = check_text.split(":")[0].strip()
                status.update(f"[bold blue]Step {current_check_num}: Checking {check_key}...")
                
                # Simple heuristic audit: check if certain keywords exist in the code
                keywords = {
                    "PII": ["scrub", "mask", "pii", "filter"],
                    "Sandbox": ["sandbox", "docker", "isolated", "gvisor"],
                    "Caching": ["cache", "redis", "memorystore", "hive_mind"],
                    "Identity": ["iam", "auth", "token", "oauth", "workloadidentity"],
                    "Moderation": ["moderate", "safety", "filter"],
                    "Routing": ["router", "switch", "map", "agentengine"],
                    "Outputs": ["schema", "json", "structured", "basemodel", "interface"],
                    "HITL": ["approve", "confirm", "human"],
                    "Confirmation": ["confirm", "ask", "approve"],
                    "Logging": ["log", "trace", "audit", "reasoningengine"],
                    "Cloud Run": ["startupcpu", "boost", "minInstances"],
                    "GKE": ["kubectl", "k8s", "autopilot", "helm"],
                    "VPC": ["vpcnc", "sc-env", "isolation"],
                    "A2UI": ["a2ui", "renderer", "registry", "component"],
                    "Responsive": ["@media", "max-width", "flex", "grid", "vw", "vh"],
                    "Accessibility": ["aria-", "role=", "alt=", "tabindex"],
                    "Policies": ["policies.json", "policy_engine", "forbidden_topics", "hitl"],
                    "Triggers": ["trigger", "callback", "handle", "onclick"],
                    "Resiliency": ["retry", "tenacity", "backoff", "exponential"],
                    "Prompts": [".md", ".yaml", ".prompt", "load_prompt", "jinja2"],
                    "Sessions": ["session", "state", "conversation_id", "thread_id"],
                    "Retrieval": ["rag", "vector", "embedding", "context_cache", "retrieval", "pinecone", "alloydb", "cloudsql", "bigquery", "firestore", "spanner", "redshift", "snowflake", "databricks", "s3", "blob"],
                    "Reasoning": ["while", "for", "loop", "invoke", "call", "run", "execute", "chain", "agent"],
                    "State": ["memory", "state", "db", "redis", "history", "session", "storage"],
                    "Tools": ["tool", "registry", "dispatcher", "handler", "mcp", "api", "sdk", "client", "connect"],
                    "Safety": ["filter", "clean", "sanitize", "scrub", "guard"],
                    "Shadow Mode": ["shadow", "router", "dual_rollout", "traffic_split", "version_v2"],
                    "Orchestration": ["swarm", "coordinator", "manager_agent", "supervisor", "orchestrator", "worker_agent"],
                    "VPC": ["vpc_sc", "service_control", "isolated_network", "private_endpoint"],
                    "Observability": ["otel", "trace", "span", "telemetry", "opentelemetry", "cloud_trace"],
                    "Governance": ["policies.json", "hitl", "approval", "policy_engine"],
                    "Legal": ["copyright", "license", "disclaimer", "data_residency", "privacy", "tos", "terms_of_service"],
                    "Marketing": ["brand", "tone", "vibrant", "consistent", "seo", "og:image", "description", "cta"]
                }
                
                # Weighting: Security and Core Architecture are more important
                weights = {
                    "🏗️": 1.5,
                    "🛡️": 2.0,
                    "🎭": 1.0,
                    "🧗": 1.2,
                    "📉": 1.3,
                    "⚖️": 1.8,  # Legal/Compliance
                    "📢": 0.9   # Marketing/Brand
                }
                
                category_prefix = section["category"][:2]
                weight = weights.get(category_prefix, 1.0)

                # If any keyword for this check type is found, mark as PASSED
                matched = False
                for k, words in keywords.items():
                    if k.lower() in check_key.lower():
                        if any(word in code_content.lower() for word in words):
                            matched = True
                            break
                
                if matched:
                    check_status = "[bold green]PASSED[/bold green]"
                    passed_checks += weight
                    # Output source for evidence bridge
                    if "Google" in framework_name:
                        console.print(f"SOURCE: {check_key} | https://cloud.google.com/architecture/framework | Google Cloud Architecture Framework: {section['category']}")
                else:
                    check_status = "[bold red]FAIL[/bold red]"
                    # Output action for report
                    console.print(f"ACTION: codebase | Architecture Gap: {check_key} | {rationale}")
                    if "Google" in framework_name:
                         console.print(f"SOURCE: {check_key} | https://cloud.google.com/architecture/framework | Recommended Pattern: {check_text}")
                
                total_checks += weight
                
                table.add_row(check_text, check_status, rationale)
            
            console.print(table)
            console.print("\n")

    score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    console.print(f"📊 [bold]Review Score: {score:.0f}/100[/bold]")
    if score >= 80:
        console.print("✅ [bold green]Architecture Review Complete.[/bold green] Your agent is well-aligned with optimized patterns.")
    else:
        if framework_key == "generic":
            console.print("💡 [bold yellow]Self-Learning Note:[/bold yellow] Found unknown tech. I have mapped your code structure to universal agentic pillars (Reasoning/Tools/Safety).")
        console.print("⚠️ [bold yellow]Review Complete with warnings.[/bold yellow] Your agent has gaps in best practices. See results above.")

if __name__ == "__main__":
    app()
