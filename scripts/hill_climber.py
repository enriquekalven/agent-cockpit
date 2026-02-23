import os
import subprocess

from rich.console import Console
from rich.panel import Panel

console = Console()

class HillClimber:
    """
    Sovereign Evolution Engine: Iterative Capability Improvements.
    Loop: Audit -> Refine -> Validate -> Deploy.
    """
    def __init__(self, target_repos):
        self.target_repos = target_repos
        self.iteration = 0
        self.max_iterations = 5

    def run_iteration(self, repo_path):
        self.iteration += 1
        console.print(Panel.fit(f"🧗 [bold green]Hill Climbing Iteration {self.iteration}/{self.max_iterations}[/]\n[bold]Target:[/] {repo_path}", border_style="green"))
        
        # 1. Audit Deep
        console.print(f"🔍 Running Deep Audit on {repo_path}...")
        cmd = ["PYTHONPATH=src", "uv", "run", "agentops-cockpit", "audit", "report", "--path", repo_path, "--mode", "deep", "--apply-fixes"]
        result = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)
        
        # Save logs for Antigravity to analyze
        log_path = f"hill_climb_logs/iteration_{self.iteration}.log"
        os.makedirs("hill_climb_logs", exist_ok=True)
        with open(log_path, "w") as f:
            f.write(result.stdout)
            f.write(result.stderr)
        
        console.print(f"✅ Audit complete. Logs saved to {log_path}")
        return result.stdout

    def trigger_validation(self):
        console.print("🚀 Triggering Zero2Hero Validation Gate...")
        # Running a subset of zero2hero for efficiency during hill climbing
        cmd = ["PYTHONPATH=src", "uv", "run", "pytest", "src/agent_ops_cockpit/tests/test_capabilities_gate.py"]
        subprocess.run(" ".join(cmd), shell=True)

if __name__ == "__main__":
    targets = [
        "lab-tutorial-agent-alt",
        "test-deployments/prod-sovereign-agent",
        "my_super_agent",
        "test-adk-agent",
        "temp_mixed"
    ]
    climber = HillClimber(targets)
    # The script acts as a step-by-step assistant for Antigravity
    console.print("Sovereign Hill Climber Ready. Antigravity will orchestrate the refinement.")
