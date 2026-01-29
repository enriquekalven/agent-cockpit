import typer
import os
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

    console.print(Panel.fit(f"🏛️ [bold blue]{framework_name.upper()}: ARCHITECTURE REVIEW[/bold blue]", border_style="blue"))
    console.print(f"Detected Framework: [bold green]{framework_name}[/bold green]")
    console.print(f"Comparing local agent implementation against [bold]{framework_name} Best Practices[/bold]...\n")

    # Read all relevant code files for inspection
    code_content = ""
    for root, dirs, files in os.walk(path):
        if any(d in root for d in [".venv", "node_modules", ".git"]):
            continue
        for file in files:
            if file.endswith((".py", ".ts", ".tsx", ".js")):
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        code_content += f.read() + "\n"
                except Exception:
                    pass

    total_checks = sum(len(section["checks"]) for section in checklist)
    passed_checks = 0
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
                status.update(f"[bold blue][{current_check_num}/{total_checks}] Checking {check_key}...")
                
                # Simple heuristic audit: check if certain keywords exist in the code
                keywords = {
                    "PII": ["scrub", "mask", "pii", "filter"],
                    "Sandbox": ["sandbox", "docker", "isolated", "gvisor"],
                    "Caching": ["cache", "redis", "memorystore", "hive_mind"],
                    "Identity": ["iam", "auth", "token", "oauth", "workloadidentity"],
                    "Moderation": ["moderate", "safety", "filter"],
                    "Routing": ["router", "switch", "map", "agentengine"],
                    "Outputs": ["schema", "json", "structured"],
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
                    "Triggers": ["trigger", "callback", "handle", "onclick"]
                }
                
                # If any keyword for this check type is found, mark as PASSED
                matched = False
                for k, words in keywords.items():
                    if k.lower() in check_key.lower():
                        if any(word in code_content.lower() for word in words):
                            matched = True
                            break
                
                if matched:
                    check_status = "[bold green]PASSED[/bold green]"
                    passed_checks += 1
                else:
                    check_status = "[bold red]FAIL[/bold red]"
                
                # time.sleep(0.1) # Simulate deep heuristic scan
                
                table.add_row(check_text, check_status, rationale)
            
            console.print(table)
            console.print("\n")

    score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    console.print(f"📊 [bold]Review Score: {score:.0f}/100[/bold]")
    if score >= 80:
        console.print(f"✅ [bold green]Architecture Review Complete.[/bold green] Your agent is well-aligned with {framework_name} patterns.")
    else:
        console.print("⚠️ [bold yellow]Review Complete with warnings.[/bold yellow] Your agent has gaps in best practices. See results above.")

if __name__ == "__main__":
    app()
