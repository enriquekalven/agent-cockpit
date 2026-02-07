import os
import shutil
import subprocess
import socket
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class PreflightEngine:
    """
    Recommendation #2: Environment-Aware Dependency Pre-flight.
    Ensures the environment is consistent before running audits.
    """
    def __init__(self, target_path="."):
        self.target_path = target_path
        self.results = {}

    def check_registry_access(self, registry_url="https://pypi.org/simple"):
        """Verify if the current environment can reach the specified registry."""
        try:
            # Quick socket check
            host = registry_url.replace("https://", "").replace("http://", "").split("/")[0]
            socket.create_connection((host, 443), timeout=3)
            return True, f"Reachable: {host}"
        except Exception as e:
            return False, f"Unreachable: {registry_url} ({e})"

    def check_tooling(self):
        """Check for mandatory CLI tools."""
        tools = ["python3", "pip", "git"]
        missing = []
        for tool in tools:
            if not shutil.which(tool):
                missing.append(tool)
        
        if missing:
            return False, f"Missing tools: {', '.join(missing)}"
        return True, "All base tools detected."

    def check_environment_consistency(self):
        """Check for common environment debt (missing .env, virtualenvs)."""
        env_files = [f for f in os.listdir(self.target_path) if f.startswith(".env")]
        if not env_files:
             return True, "No .env detected (assuming local simulation or IAM auth)."
        return True, f"Found environment config: {', '.join(env_files)}"

    def run_all(self):
        """Executes all pre-flight checks and returns success status."""
        console.print("\n🛫 [bold blue]LAUNCHING PRE-FLIGHT SYSTEM VERIFICATION...[/bold blue]")
        
        checks = [
            ("Registry Connectivity", self.check_registry_access),
            ("Tooling Readiness", self.check_tooling),
            ("Env Consistency", self.check_environment_consistency)
        ]
        
        table = Table(title="📋 Pre-flight Readiness Checklist", show_header=True, header_style="bold magenta")
        table.add_column("System Component", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Details", style="dim")
        
        all_passed = True
        for name, func in checks:
            success, detail = func()
            status = "[green]READY[/green]" if success else "[red]BLOCKED[/red]"
            table.add_row(name, status, detail)
            if not success:
                all_passed = False
        
        console.print(table)
        
        if not all_passed:
            console.print("⚠️ [bold yellow]Pre-flight warnings detected. Some audit modules may exhibit drift.[/bold yellow]\n")
        else:
            console.print("✨ [bold green]Environment verified. Proceeding to Agent Audit.[/bold green]\n")
            
        return all_passed

def run_preflight(target_path="."):
    engine = PreflightEngine(target_path)
    return engine.run_all()
