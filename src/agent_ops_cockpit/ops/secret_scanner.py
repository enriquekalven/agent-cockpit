from tenacity import retry, wait_exponential, stop_after_attempt
try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.6.7 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
import os
import re
import math
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

app = typer.Typer(help="Secret Scanner: Detects hardcoded credentials and leaks.")
console = Console()

def _calculate_entropy(data: str) -> float:
    """Calculates the Shannon entropy of a string (higher = more likely to be a random secret)."""
    if not data:
        return 0.0
    entropy = 0
    for char in set(data):
        p_x = float(data.count(char)) / len(data)
        if p_x > 0:
            entropy += -p_x * math.log(p_x, 2)
    return entropy

# Common Secret Patterns
SECRET_PATTERNS = {
    "Google API Key": r"AIza[0-9A-Za-z-_]{35}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "OpenAI API Key": r"sk-[a-zA-Z0-9]{20,}",
    "Anthropic API Key": r"sk-ant-[a-zA-Z0-9]{20,}",
    "Azure OpenAI Key": r"[0-9a-f]{32}",
    "Generic Bearer Token": r"Bearer\s+[0-9a-zA-Z._-]{20,}",
    "GCP Service Account": r"\"type\":\s*\"service_account\"",
    "Placeholder Credential": r"(?i)['\"](REPLACE_ME|INSERT_YOUR_KEY|YOUR_API_KEY|TODO_SET_KEY)['\"]",
    "Hardcoded API Variable": r"(?i)(api_key|client_secret|token)\s*=\s*['\"][a-zA-Z0-9_-]{10,}['\"]",
}

@app.command()
def scan(path: str = typer.Argument(".", help="Directory to scan for secrets")):
    """
    Scans the codebase for hardcoded secrets, API keys, and credentials.
    """
    console.print(Panel.fit("🔍 [bold yellow]SECRET SCANNER: CREDENTIAL LEAK DETECTION[/bold yellow]", border_style="yellow"))
    
    from agent_ops_cockpit.ops.discovery import DiscoveryEngine
    discovery = DiscoveryEngine(path)
    
    findings = []
    
    for file_path in discovery.walk(path):
        # Filter by relevant extensions
        if not file_path.endswith((".py", ".env", ".ts", ".js", ".json", ".yaml", ".yml")):
            continue
            
        is_lib = discovery.is_library_file(file_path)
        
        try:
            with open(file_path, "r", errors="ignore") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    for secret_name, pattern in SECRET_PATTERNS.items():
                        match = re.search(pattern, line)
                        if match:
                            # 1. Check for inline ignore
                            issue_slug = secret_name.lower().replace(" ", "-")
                            if "# cockpit-ignore" in line:
                                comment_part = line.split("# cockpit-ignore")[1].lower()
                                if issue_slug in comment_part or "all" in comment_part:
                                    continue
                            
                            # 2. Check for whole-file ignore (first 10 lines)
                            is_ignored_file = False
                            for j in range(min(10, len(lines))):
                                if "# cockpit-ignore" in lines[j]:
                                    comment_part = lines[j].split("# cockpit-ignore")[1].lower()
                                    if issue_slug in comment_part or "all" in comment_part:
                                        is_ignored_file = True
                                        break
                            if is_ignored_file:
                                continue

                            # 3. Entropy & Verification Layer (v1.6.7)
                            # Only apply to random-looking strings, skip standard prose or hex indices
                            secret_value = match.group(0)
                            entropy = _calculate_entropy(secret_value)
                            
                            # Threshold for a secret is usually > 3.5 bits for random strings
                            # Low-entropy strings (like '0000000000000000') are rarely real keys
                            if entropy < 3.2 and secret_name not in ["GCP Service Account", "Placeholder Credential"]:
                                continue

                            # Library Isolation: Skip hits in known libraries to reduce false positives
                            if is_lib:
                                continue
                                
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

@app.command()
def version():
    """Show the version of the Secret Scanner."""
    console.print('[bold cyan]v1.6.7[/bold cyan]')

if __name__ == "__main__":
    app()
