try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.8.4 Sovereign Alignment: Optimized for Google Cloud Run
import os
import re

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(help="Face Auditor: Scan frontend code for A2UI alignment.")
console = Console()

@app.command()
def audit(path: str = typer.Argument("src", help="Directory to scan")):
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
    trigger_pattern = re.compile(r"onTrigger|handleTrigger|agentAction|onClick|handleSubmit")
    ux_feedback_pattern = re.compile(r"Skeleton|Loading|Spinner|Progress|Thinking|Loader|lucide|animate-spin")
    a11y_pattern = re.compile(r"aria-label|role=|tabIndex|alt=")
    legal_pattern = re.compile(r"Copyright|Privacy\s*Policy|Disclaimer|Terms\s*of\s*Service|©", re.IGNORECASE)
    marketing_pattern = re.compile(r"og:image|meta\s+name=['\"]description['\"]|favicon|logo")
    hitl_pattern = re.compile(r"HumanInTheLoop|confirm|Approve|Reject|Gate")
    streaming_pattern = re.compile(r"Suspense|Stream|Markdown|chunk")
    mobile_pattern = re.compile(r"@media\s*\(max-width:|max-width:\s*\d+px|viewport|flex-direction:\s*column")
    mcp_ui_pattern = re.compile(r"MCPClient|mcp-server|stdio-client|ModelContextProtocol")
    agui_pattern = re.compile(r"AgenticGraph|GraphView|StateNode|Edge|GraphRegistry")
    mcp_apps_pattern = re.compile(r"MCPApp|ToolSurface|McpToolRenderer|mcp-tool-id")


    for root, _dirs, files in os.walk(path):
        if any(d in root for d in [".venv", "node_modules", ".git", "dist"]):
            continue
            
        for file in files:
            # Skip non-component files to reduce noise
            if file.endswith((".tsx", ".ts", ".js", ".jsx")):
                if any(x in file.lower() for x in ["config", "test", "spec", "d.ts", "setup", "main", "index"]):
                    continue
                
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
                        findings.append({"line": 1, "issue": "Missing 'surfaceId' mapping", "fix": "Add 'surfaceId: string' to props. Snippet: `interface Props { surfaceId: string; ... }`"})
                    
                    if not registry_pattern.search(content) and "Registry" in file:
                        findings.append({"line": 1, "issue": "Registry component without A2UIRegistry registration", "fix": "Wrap with: `export const MyComponent = A2UIRegistry.registerComponent('my-id', Component);`"})
                    
                    if "Button" in file and not trigger_pattern.search(content):
                        # Try to find the button line
                        line_no = 1
                        for i, line in enumerate(lines):
                            if "<button" in line.lower() or "<Button" in line:
                                line_no = i + 1
                                break
                        findings.append({"line": line_no, "issue": "Interactive component without Tool/Agent triggers", "fix": "Add: `onClick={() => onTrigger({ action: 'click', surfaceId })}`"})

                    if not ux_feedback_pattern.search(content) and ("Page" in file or "View" in file):
                         findings.append({"line": 1, "issue": "Missing 'Thinking' feedback (Skeleton/Spinner)", "fix": "Add: `{isThinking && <Skeleton className='h-4 w-[250px]' />}`"})
                    
                    if not a11y_pattern.search(content) and ("Button" in file or "Input" in file):
                        line_no = 1
                        for i, line in enumerate(lines):
                            if "<button" in line.lower() or "<input" in line.lower():
                                line_no = i + 1
                                break
                        findings.append({"line": line_no, "issue": "Missing i18n/Accessibility labels (aria-label)", "fix": "Add: `<button aria-label={t('actions.submit')}>`"})

                    if not legal_pattern.search(content) and ("Page" in file or "Layout" in file or "Footer" in file):
                        findings.append({"line": 1, "issue": "Missing Legal Disclaimer or Privacy Policy link", "fix": "Add footer: `<footer><a href='/privacy'>Privacy Policy</a></footer>`"})
                    
                    if not marketing_pattern.search(content) and ("index" in file.lower() or "head" in file.lower() or "App" in file):
                        findings.append({"line": 1, "issue": "Missing Branding (Logo) or SEO Metadata (OG/Description)", "fix": "Add: `<meta property='og:image' content='/logo.png' />`"})

                    if not hitl_pattern.search(content) and ("Action" in file or "Tool" in file or "Transfer" in file):
                         findings.append({"line": 1, "issue": "Missing HITL (Human-in-the-Loop) Gating", "fix": "Add: `if (impact === 'high') return <ConfirmationModal onConfirm={proceed} />`"})
                    
                    if not streaming_pattern.search(content) and ("Chat" in file or "Thread" in file or "Log" in file):
                         findings.append({"line": 1, "issue": "Missing Streaming Resilience (Suspense/Stream)", "fix": "Wrap with: `<Suspense fallback={<Loader />}>{children}</Suspense>`"})

                    if not mobile_pattern.search(content) and ("Layout" in file or "Page" in file or "Home" in file or file.endswith(".css")):
                         findings.append({"line": 1, "issue": "Missing Mobile Responsiveness (@media queries)", "fix": "Add: `@media (max-width: 768px) { .container { flex-direction: column; } }`"})

                    if not mcp_ui_pattern.search(content) and ("MCP" in file or "Tool" in file):
                         findings.append({"line": 1, "issue": "MCP-UI protocol misalignment", "fix": "Use: `const { callTool } = useMCPClient();`"})

                    if not agui_pattern.search(content) and ("Graph" in file or "Flow" in file or "Workflow" in file):
                         findings.append({"line": 1, "issue": "Missing AGUI (Agentic Graph UI) mapping", "fix": "Add: `<AgenticGraph data={flowData} onNodeClick={handleNode} />`"})

                    if not mcp_apps_pattern.search(content) and ("App" in file and "MCP" in file):
                         findings.append({"line": 1, "issue": "Non-compliant MCP Apps UI", "fix": "Use: `<McpToolRenderer toolId={selectedTool} />`"})



                    if findings:
                        issues.append({"file": rel_path, "findings": findings})

                except Exception:
                    pass

    # Quantitative Scoring (Principal v1.2)
    max_score = 100
    deductions = {
        "Missing 'surfaceId'": 20,
        "Missing 'Thinking' feedback": 15,
        "Missing HITL": 15,
        "Missing Streaming Resilience": 10,
        "interactive component without triggers": 10,
        "Missing a11y labels": 10,
        "Missing Mobile Responsiveness": 10,
        "Missing AGUI mapping": 15,
        "Non-compliant MCP Apps UI": 10,
        "Missing Legal/SEO": 5
    }

    
    total_deduction = 0
    unique_issues = set()
    for issue in issues:
        for finding in issue["findings"]:
            for key, val in deductions.items():
                if key.lower() in finding["issue"].lower():
                    if key not in unique_issues:
                        total_deduction += val
                        unique_issues.add(key)
    
    score = max(0, max_score - total_deduction)
    verdict = "✅ APPROVED" if score >= 85 else "⚠️ WARN" if score >= 60 else "❌ REJECTED"
    
    console.print(f"📝 Scanned [bold]{files_scanned}[/bold] frontend files.")

    # Executive Summary Table (Product View v1.2)
    summary = Table(title="💎 PRINCIPAL UX EVALUATION (v1.2)", box=None)
    summary.add_column("Metric", style="cyan")
    summary.add_column("Value", style="bold white")
    summary.add_row("GenUI Readiness Score", f"{score}/100")
    summary.add_row("Consensus Verdict", f"[{'green' if score >= 85 else 'yellow' if score >= 60 else 'red'}]{verdict}[/]")
    summary.add_row("A2UI Registry Depth", "Fragmented" if "Missing 'surfaceId'" in unique_issues else "Aligned")
    summary.add_row("Latency Tolerance", "Low" if "Missing 'Thinking' feedback" in unique_issues else "Premium")
    summary.add_row("Autonomous Risk (HITL)", "HIGH" if "Missing HITL" in unique_issues else "Secured")
    summary.add_row("Streaming Fluidity", "Flicker-Prone" if "Missing Streaming Resilience" in unique_issues else "Smooth")
    summary.add_row("AGUI Interoperability", "None" if "Missing AGUI mapping" in unique_issues else "Visualized")
    summary.add_row("MCP App Compliance", "Legacy" if "Non-compliant MCP Apps UI" in unique_issues else "Modern")
    
    console.print(Panel(summary, border_style="green" if score >= 85 else "yellow"))

    table = Table(title="🔍 A2UI DETAILED FINDINGS")
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

    if score < 85:
        console.print(f"\n💡 [bold yellow]UX Principal Recommendation:[/bold yellow] Your 'Face' layer needs {100-score}% more alignment.")
        if "Missing 'surfaceId'" in unique_issues:
            console.print(" - Map components to 'surfaceId' to enable agent-driven UI updates.")
        if "Missing 'Thinking' feedback" in unique_issues:
            console.print(" - Add 'Skeleton' screens to mask LLM reasoning latency.")
        if "Missing HITL" in unique_issues:
            console.print(" - Implement Human-in-the-Loop gates (modals/approvals) for sensitive impacts.")
        if "Missing Streaming Resilience" in unique_issues:
            console.print(" - Use 'Suspense' boundaries to handle live token streaming without flicker.")
    else:
        console.print("\n✅ [bold green]Frontend is Well-Architected for GenUI interactions.[/bold green]")

@app.command()
def version():
    """Show the version of the Face Auditor."""
    console.print('[bold cyan]v1.3.0[/bold cyan]')

if __name__ == "__main__":
    app()
