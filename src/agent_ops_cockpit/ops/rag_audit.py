from google.adk.agents.context_cache_config import ContextCacheConfig
# v1.4.5 Sovereign Alignment: Optimized for Google Cloud Run
from tenacity import retry, wait_exponential, stop_after_attempt
import typer
from typing import Literal
import logging
import os
import ast
from rich.console import Console
from rich.panel import Panel
from agent_ops_cockpit.ops.auditors.rag_fidelity import RAGFidelityAuditor
from agent_ops_cockpit.ops.discovery import DiscoveryEngine

console = Console()

app = typer.Typer(help="RAG Truth-Sayer SME: Audits RAG pipelines for grounding and fidelity.")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        # If no command, just run audit with defaults
        audit_command('.') # Changed to call audit_command

@app.command(name="audit")
def audit_command(path: str = typer.Option('.', '--path', '-p', help='Path to the agent project to audit')):
    """
    Run the RAG Fidelity Audit.
    Detects retrieval-reasoning drift, high temperature risks, and weak prompt boundaries.
    """
    console.print(Panel.fit('🧗 [bold blue]RAG TRUTH-SAYER: FIDELITY AUDIT[/bold blue]', border_style='blue'))
    
    auditor = RAGFidelityAuditor()
    discovery = DiscoveryEngine()
    all_findings = []
    
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__', 'venv', '.venv']]
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                # Skip library files and specific internal files
                if discovery.is_library_file(file_path) or 'auditors' in file_path or 'frameworks.py' in file_path:
                    continue

                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    tree = ast.parse(content)
                    findings = auditor.audit(tree, content, file_path)
                    all_findings.extend(findings)
                except Exception as e:
                    logging.debug(f"Error processing file {file_path}: {e}")
                    pass
    
    if not all_findings:
        # Check if RAG was even detected
        # The auditor returns [] if no RAG indicators found.
        # We can be more explicit for the CLI.
        console.print("✅ [green]No RAG-specific risks detected or no RAG pattern found.[/green]")
        return

    for f in all_findings:
        console.print(f"🚩 [bold red]{f.title}[/bold red] ({f.file_path}:{f.line_number or ''})")
        console.print(f"   [dim]{f.description}[/dim]")
        console.print(f"   ⚖️ [bold green]Strategic ROI:[/bold green] {f.roi}")
        # Orchestrator capture line
        console.print(f"ACTION: {f.file_path}:{f.line_number or 1} | {f.title} | {f.description}")

if __name__ == "__main__":
    app()
