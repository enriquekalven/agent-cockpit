import os
import re
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

app = typer.Typer(help="Face Auditor: Scan frontend code for A2UI alignment.")
console = Console()

@app.command()
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
    ux_feedback_pattern = re.compile(r"Skeleton|Loading|Spinner|Progress")
    a11y_pattern = re.compile(r"aria-label|role=|tabIndex|alt=")
    legal_pattern = re.compile(r"Copyright|PrivacyPolicy|Disclaimer|TermsOfService|©")
    marketing_pattern = re.compile(r"og:image|meta\s+name=['\"]description['\"]|favicon|logo")

    for root, dirs, files in os.walk(path):
        if any(d in root for d in [".venv", "node_modules", ".git", "dist"]):
            continue
            
        for file in files:
            if file.endswith((".tsx", ".ts", ".js", ".jsx")):
                files_scanned += 1
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, ".")
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                        content = "".join(lines)
                        
                    findings = []
                    
                    # Heuristic with Line Numbers
                    if not surface_id_pattern.search(content):
                        findings.append({"line": 1, "issue": "Missing 'surfaceId' mapping", "fix": "Add 'surfaceId' prop to the root component or exported interface."})
                    
                    if not registry_pattern.search(content) and "Registry" in file:
                        findings.append({"line": 1, "issue": "Registry component without A2UIRegistry registration", "fix": "Wrap component in A2UIRegistry.registerComponent()."})
                    
                    if "Button" in file and not trigger_pattern.search(content):
                        # Try to find the button line
                        line_no = 1
                        for i, line in enumerate(lines):
                            if "<button" in line.lower() or "<Button" in line:
                                line_no = i + 1
                                break
                        findings.append({"line": line_no, "issue": "Interactive component without Tool/Agent triggers", "fix": "Ensure the button calls an agent tool trigger (onTrigger)."})

                    if not ux_feedback_pattern.search(content) and ("Page" in file or "View" in file):
                         findings.append({"line": 1, "issue": "Missing 'Thinking' feedback (Skeleton/Spinner)", "fix": "Implement a Loading state or Skeleton component for agent latency."})
                    
                    if not a11y_pattern.search(content) and ("Button" in file or "Input" in file):
                        line_no = 1
                        for i, line in enumerate(lines):
                            if "<button" in line.lower() or "<input" in line.lower():
                                line_no = i + 1
                                break
                        findings.append({"line": line_no, "issue": "Missing i18n/Accessibility labels (aria-label)", "fix": "Add aria-label or alt tags for screen readers and i18n."})

                    if not legal_pattern.search(content) and ("Page" in file or "Layout" in file or "Footer" in file):
                        findings.append({"line": 1, "issue": "Missing Legal Disclaimer or Privacy Policy link", "fix": "Add a footer link to the mandatory Privacy Policy / TOS."})
                    
                    if not marketing_pattern.search(content) and ("index" in file.lower() or "head" in file.lower() or "App" in file):
                        findings.append({"line": 1, "issue": "Missing Branding (Logo) or SEO Metadata (OG/Description)", "fix": "Add meta tags (og:image, description) and project logo."})

                    if findings:
                        issues.append({"file": rel_path, "findings": findings})

                except Exception:
                    pass

    console.print(f"📝 Scanned [bold]{files_scanned}[/bold] frontend files.")

    table = Table(title="🔍 A2UI Audit Findings")
    table.add_column("File:Line", style="cyan")
    table.add_column("Issue", style="red")
    table.add_column("Recommended Fix", style="green")

    if not issues:
        table.add_row("All Files", "[green]A2UI Ready[/green]", "No action needed.")
    else:
        # Structured output for Orchestrator parsing
        console.print("\n[bold]🛠️  DEVELOPER ACTIONS REQUIRED:[/bold]")
        for issue in issues:
            for finding in issue["findings"]:
                table.add_row(f"{issue['file']}:{finding['line']}", finding["issue"], finding["fix"])
                # This line is for the orchestrator to parse easily
                console.print(f"ACTION: {issue['file']}:{finding['line']} | {finding['issue']} | {finding['fix']}")

    console.print("\n", table)

    
    if len(issues) > 5:
        console.print("\n⚠️  [yellow]Recommendation:[/yellow] Your 'Face' layer has fragmented A2UI surface mappings.")
        console.print("💡 Use the A2UI Registry to unify how your agent logic triggers visual surfaces.")
    else:
        console.print("\n✅ [bold green]Frontend is Well-Architected for GenUI interactions.[/bold green]")

if __name__ == "__main__":
    app()
