import os
import re
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

app = typer.Typer(help="Secret Scanner: Detects hardcoded credentials and leaks.")
console = Console()

# Common Secret Patterns
SECRET_PATTERNS = {
    "Google API Key": r"AIza[0-9A-Za-z-_]{35}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "OpenAI API Key": r"sk-[a-zA-Z0-9]{20,}",
    "Anthropic API Key": r"sk-ant-[a-zA-Z0-9]{20,}",
    "Azure OpenAI Key": r"[0-9a-f]{32}",
    "Generic Bearer Token": r"Bearer\s+[0-9a-zA-Z._-]{20,}",
    "Hardcoded API Variable": r"(?i)(api_key|app_secret|client_secret|access_token)\s*=\s*['\"][0-9a-zA-Z_-]{16,}['\"]",
    "GCP Service Account": r"\"type\":\s*\"service_account\"",
}

@app.command()
def scan(path: str = typer.Argument(".", help="Directory to scan for secrets")):
    """
    Scans the codebase for hardcoded secrets, API keys, and credentials.
    """
    console.print(Panel.fit("🔍 [bold yellow]SECRET SCANNER: CREDENTIAL LEAK DETECTION[/bold yellow]", border_style="yellow"))
    
    findings = []
    
    for root, dirs, files in os.walk(path):
        # Skip virtual environments, git, and tests
        if any(skip in root.lower() for skip in [".venv", ".git", "tests", "test_", "node_modules"]):
            continue
            
        for file in files:
            if file.endswith((".py", ".env", ".ts", ".js", ".json", ".yaml", ".yml")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", errors="ignore") as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            for secret_name, pattern in SECRET_PATTERNS.items():
                                match = re.search(pattern, line)
                                if match:
                                    findings.append({
                                        "file": os.path.relpath(file_path, path),
                                        "line": i + 1,
                                        "type": secret_name,
                                        "content": line.strip()[:50] + "..."
                                    })
                except Exception:
                    continue

    table = Table(title="🛡️ Security Findings: Hardcoded Secrets")
    table.add_column("File", style="cyan")
    table.add_column("Line", style="magenta")
    table.add_column("Type", style="bold red")
    table.add_column("Suggestion", style="green")

    if findings:
        console.print("\n[bold]🛠️  DEVELOPER ACTIONS REQUIRED:[/bold]")
        for finding in findings:
            table.add_row(
                finding["file"],
                str(finding["line"]),
                finding["type"],
                "Move to Secret Manager"
            )
            # Orchestrator parsing
            console.print(f"ACTION: {finding['file']}:{finding['line']} | Found {finding['type']} leak | Move this credential to Google Cloud Secret Manager or .env file.")
            
        console.print("\n", table)
        console.print(f"\n❌ [bold red]FAIL:[/bold red] Found {len(findings)} potential credential leaks.")
        console.print("💡 [bold green]Recommendation:[/bold green] Use Google Cloud Secret Manager or environment variables for all tokens.")
        raise typer.Exit(code=1)
    else:
        console.print("✅ [bold green]PASS:[/bold green] No hardcoded credentials detected in matched patterns.")

if __name__ == "__main__":
    app()
