import os
import re
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

app = typer.Typer(help="Face Auditor: Scan frontend code for A2UI alignment.")
console = Console()

def audit(path: str = "src"):
    """
    Step 4: Frontend / A2UI Auditing.
    Ensures frontend components are properly mapping surfaceId and detecting triggers.
    """
    console.print(Panel.fit("🎭 [bold blue]FACE AUDITOR: A2UI COMPONENT SCAN[/bold blue]", border_style="blue"))
    console.print(f"Scanning directory: [yellow]{path}[/yellow]")

    files_scanned = 0
    issues = []

    # Heuristic Patterns
    surface_id_pattern = re.compile(r"surfaceId|['\"]surface-id['\"]")
    registry_pattern = re.compile(r"A2UIRegistry|registerComponent")
    trigger_pattern = re.compile(r"onTrigger|handleTrigger|agentAction")

    for root, dirs, files in os.walk(path):
        if any(d in root for d in [".venv", "node_modules", ".git", "dist"]):
            continue
            
        for file in files:
            if file.endswith((".tsx", ".ts", ".js", ".jsx")):
                files_scanned += 1
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                    findings = []
                    if not surface_id_pattern.search(content):
                        findings.append("Missing 'surfaceId' mapping")
                    if not registry_pattern.search(content) and "Registry" in file:
                        findings.append("Registry component without A2UIRegistry registration")
                    if "Button" in file and not trigger_pattern.search(content):
                        findings.append("Interactive component without Tool/Agent triggers")
                        
                    if findings:
                        issues.append({"file": file, "findings": findings})
                except Exception:
                    pass

    console.print(f"📝 Scanned [bold]{files_scanned}[/bold] frontend files.")

    table = Table(title="🔍 A2UI Audit Findings")
    table.add_column("File", style="cyan")
    table.add_column("Issue", style="red")

    if not issues:
        table.add_row("All Files", "[green]A2UI Ready[/green]")
    else:
        for issue in issues:
            for finding in issue["findings"]:
                table.add_row(issue["file"], finding)

    console.print(table)
    
    if len(issues) > 5:
        console.print("\n⚠️  [yellow]Recommendation:[/yellow] Your 'Face' layer has fragmented A2UI surface mappings.")
        console.print("💡 Use the A2UI Registry to unify how your agent logic triggers visual surfaces.")
    else:
        console.print("\n✅ [bold green]Frontend is Well-Architected for GenUI interactions.[/bold green]")

if __name__ == "__main__":
    app()
