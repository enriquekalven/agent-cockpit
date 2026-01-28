import os
import re
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

app = typer.Typer(help="UI/UX Auditor: Governance and optimization for the Agent Face.")
console = Console()

class UIFinding:
    def __init__(self, id: str, category: str, severity: str, message: str, file: str, suggestion: str):
        self.id = id
        self.category = category
        self.severity = severity
        self.message = message
        self.file = file
        self.suggestion = suggestion

def audit_ui_best_practices(src_path: str):
    findings = []
    
    for root, dirs, files in os.walk(src_path):
        if "node_modules" in root or ".venv" in root: continue
        
        for file in files:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, src_path)
            
            if file.endswith((".tsx", ".jsx", ".ts", ".js")):
                try:
                    with open(path, "r", errors="ignore") as f:
                        content = f.read()
                        
                        # 1. A2UI Compliance: Missing surface IDs
                        if "a2-surface" in content and "surfaceId" not in content:
                            findings.append(UIFinding(
                                "a2ui_surface_id", "A2UI Protocol", "HIGH",
                                "Detected A2UI surface without unique surfaceId.",
                                rel_path, "Add `surfaceId` for automated browser testing."
                            ))
                            
                        # 2. Accessibility: Missing ARIA
                        if "<button" in content.lower() and "aria-label" not in content.lower() and "children" not in content.lower():
                            findings.append(UIFinding(
                                "aria_label", "Accessibility", "MEDIUM",
                                "Interactive button lacks description.",
                                rel_path, "Add `aria-label` for screen readers."
                            ))

                        # 3. Optimization: Large Component Detection
                        if len(content.splitlines()) > 300:
                            findings.append(UIFinding(
                                "large_component", "Refactor", "MEDIUM",
                                f"Component file is very large ({len(content.splitlines())} lines).",
                                rel_path, "Split into smaller sub-components for better performance."
                            ))

                        # 4. Streamlit: Hardcoded Secrets
                        if "st.secrets" not in content and (".env" in content or "API_KEY" in content):
                            findings.append(UIFinding(
                                "st_secrets", "Streamlit Security", "HIGH",
                                "Detected likely hardcoded keys instead of st.secrets.",
                                rel_path, "Move tokens to .streamlit/secrets.toml."
                            ))

                        # 5. Angular: Reactive Pattern
                        if "@Component" in content and "signal" not in content.lower() and "Observable" not in content:
                             findings.append(UIFinding(
                                "angular_reactivity", "Angular Performance", "MEDIUM",
                                "Component lacks reactive patterns (Signals/Observables).",
                                rel_path, "Use Signals for low-latency Agent output sync."
                            ))

                except: continue

            if file.endswith(".css"):
                try:
                    with open(path, "r", errors="ignore") as f:
                        content = f.read()
                        
                        # 4. Responsive: Missing Media Queries
                        if "@media" not in content:
                            findings.append(UIFinding(
                                "missing_media_queries", "UX / Responsive", "HIGH",
                                "No media queries detected in CSS file.",
                                rel_path, "Implement mobile-first responsive design."
                            ))
                except: continue
                
    return findings

@app.command()
def audit(path: str = typer.Argument("src", help="Path to the frontend source code")):
    """
    Runs a comprehensive UI/UX best practice audit on the codebase.
    """
    console.print(Panel.fit("🎨 [bold magenta]FACE AUDITOR: UI/UX GOVERNANCE[/bold magenta]", border_style="magenta"))
    
    findings = audit_ui_best_practices(path)
    
    table = Table(title="🎨 UI/UX Audit Results")
    table.add_column("Category", style="cyan")
    table.add_column("Severity", style="bold")
    table.add_column("Message", style="white")
    table.add_column("File", style="dim")
    table.add_column("Suggestion", style="green")

    if findings:
        for f in findings:
            severity_style = "red" if f.severity == "HIGH" else "yellow"
            table.add_row(f.category, f"[{severity_style}]{f.severity}[/{severity_style}]", f.message, f.file, f.suggestion)
        
        console.print(table)
        console.print(f"\n⚠️ Found {len(findings)} UI/UX improvement opportunities.")
    else:
        console.print("✅ [bold green]PASS:[/bold green] UI/UX architecture aligns with Agent Ops standards.")

if __name__ == "__main__":
    app()
