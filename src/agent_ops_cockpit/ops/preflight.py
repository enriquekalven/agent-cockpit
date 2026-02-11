from tenacity import retry, wait_exponential, stop_after_attempt
from google.adk.agents.context_cache_config import ContextCacheConfig
# v1.4.5 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
import os
import shutil
import socket
from rich.console import Console
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

    def check_cloud_auth(self, target_cloud="google"):
        """Verify cloud-specific CLI tools and authentication."""
        import subprocess
        
        if os.environ.get("SOVEREIGN_SIMULATION") == "true":
            return True, f"SIMULATION MOCK: {target_cloud} Identity Verified"
            
        if target_cloud == "google":
            if not shutil.which("gcloud"):
                return False, "Missing 'gcloud' CLI."
            try:
                # Check for active account
                acc = subprocess.check_output(["gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"], text=True).strip()
                if not acc: return False, "No active gcloud account. Run 'gcloud auth login'."
                return True, f"Google Authenticated: {acc}"
            except:
                return False, "Failed to verify Google Auth."
                
        elif target_cloud == "aws":
            if not shutil.which("aws"):
                return False, "Missing 'aws' CLI."
            try:
                # Check for caller identity
                id_res = subprocess.check_output(["aws", "sts", "get-caller-identity", "--output", "json"], text=True)
                import json
                arn = json.loads(id_res).get("Arn")
                return True, f"AWS Authenticated: {arn}"
            except:
                return False, "No AWS credentials found. Configure 'aws configure'."
                
        elif target_cloud == "azure":
            if not shutil.which("az"):
                return False, "Missing 'az' CLI."
            try:
                # Check for logged in account
                acc_res = subprocess.check_output(["az", "account", "show", "--output", "json"], text=True)
                import json
                name = json.loads(acc_res).get("name")
                return True, f"Azure Authenticated: {name}"
            except:
                return False, "No Azure account found. Run 'az login'."
        
        return True, f"No specific auth checks for {target_cloud}."

    def run_all(self, target_cloud="google"):
        """Executes all pre-flight checks and returns success status."""
        console.print(f"\n🛫 [bold blue]LAUNCHING PRE-FLIGHT SYSTEM VERIFICATION ({target_cloud.upper()})...[/bold blue]")
        
        checks = [
            ("Registry Connectivity", self.check_registry_access),
            ("Tooling Readiness", self.check_tooling),
            ("Env Consistency", self.check_environment_consistency),
            ("Cloud Sovereignty Auth", lambda: self.check_cloud_auth(target_cloud))
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

def run_preflight(target_path=".", target_cloud="google"):
    engine = PreflightEngine(target_path)
    return engine.run_all(target_cloud)
