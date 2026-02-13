import os
import shutil
import asyncio
import tempfile
from rich.console import Console
from .sovereign import SovereignOrchestrator

console = Console()

class SovereignSimulator:
    """
    Sovereign Battle-Testing Suite (v1.6.7).
    Simulates the end-to-end factory across Multi-Cloud (GCP, AWS, Azure).
    """

    def __init__(self):
        self.tmp_dir = tempfile.mkdtemp(prefix="sovereign_sim_")
        console.print(f"🧪 [bold cyan]Initializing Sovereign Simulation Hub...[/]")
        console.print(f"📂 Simulation Workspace: [yellow]{self.tmp_dir}[/yellow]")

    def _prepare_mock_agent(self, name="sim-agent"):
        agent_path = os.path.join(self.tmp_dir, name)
        os.makedirs(agent_path, exist_ok=True)
        
        # Create a generic non-hardened agent
        with open(os.path.join(agent_path, "agent.py"), "w") as f:
            f.write("import os\ndef solve_task(text):\n    return f'Solved: {text}'\n")
            
        with open(os.path.join(agent_path, "requirements.txt"), "w") as f:
            f.write("google-adk\nfastapi\n")
            
        return agent_path

    async def run_battle_test(self):
        """Runs the pipeline for the same agent but targeting 3 different clouds."""
        clouds = ["google", "aws", "azure"]
        results = {}

        os.environ["SOVEREIGN_SIMULATION"] = "true"
        for cloud in clouds:
            console.print(f"\n--- 🌊 [bold magenta]BATTLE TESTING CLOUD: {cloud.upper()}[/] ---")
            agent_path = self._prepare_mock_agent(f"agent-{cloud}")
            
            orchestrator = SovereignOrchestrator(target_cloud=cloud)
            # Run the pipeline (mocking the deployment step for AWS/Azure to avoid external calls)
            # Note: The pipeline already handles local asset generation
            res = await orchestrator.run_pipeline(agent_path, fleet=False)
            
            # Verify Hydration Assets
            verification = self._verify_hydration(agent_path, cloud)
            results[cloud] = {
                "pipeline_status": "SUCCESS" if res else "FAILED",
                "hydration_verified": verification
            }

        os.environ.pop("SOVEREIGN_SIMULATION")

        self._print_results(results)
        shutil.rmtree(self.tmp_dir)
        return results

    def _verify_hydration(self, path, cloud):
        """Checks if the required cloud-specific assets exist."""
        exists = False
        if cloud == "google":
            exists = os.path.exists(os.path.join(path, "Dockerfile.gcp"))
        elif cloud == "aws":
            exists = os.path.exists(os.path.join(path, "Dockerfile.aws")) and os.path.exists(os.path.join(path, "aws-sam.json"))
        elif cloud == "azure":
            exists = os.path.exists(os.path.join(path, "Dockerfile.azure")) and os.path.exists(os.path.join(path, "azure-deploy.json"))
        
        if exists:
            console.print(f"  ✅ [green]Hydration Verified for {cloud} (Assets Present)[/]")
        else:
            console.print(f"  ❌ [red]Hydration Failed for {cloud} (Assets Missing)[/]")
        return exists

    def _print_results(self, results):
        console.print("\n" + "="*50)
        console.print("🏆 [bold cyan]Sovereign Battle-Test Summary[/]")
        console.print("="*50)
        for cloud, data in results.items():
            status = "[green]PASS[/]" if data["pipeline_status"] == "SUCCESS" and data["hydration_verified"] else "[red]FAIL[/]"
            console.print(f"• {cloud.upper()}: {status}")
        console.print("="*50)

if __name__ == "__main__":
    sim = SovereignSimulator()
    asyncio.run(sim.run_battle_test())

class ToolProxy:
    """
    [MOCKING DEPTH GAP] The Tool Proxy (Mocking Engine).
    Wraps external API calls during simulation to inject failures, 
    latency, or malformed data to test agent resiliency.
    """
    
    def __init__(self, mode: str = "nominal"):
        self.mode = mode
        console.print(f"🛠️ [bold cyan]AgentOps Tool Proxy active in {mode.upper()} mode.[/bold cyan]")

    def execute_mock_tool(self, tool_name: str, args: dict):
        """
        Intercepts tool execution and returns simulated results based on proxy mode.
        """
        if self.mode == "chaos":
            import random
            failure = random.choice(["500 Internal Server Error", "Timeout (30s)", "Malformed JSON Response", "Rate Limit Exceeded"])
            console.print(f"🔥 [red][CHAOS] Injecting failure into {tool_name}: {failure}[/red]")
            return {"status": "error", "message": failure}
        
        if self.mode == "latency":
             import time
             console.print(f"⏳ [yellow][LATENCY] Delaying {tool_name} by 2.5s...[/yellow]")
             time.sleep(2.5)
        
        console.print(f"🔌 [dim]Proxied Tool Call: {tool_name}({args})[/dim]")
        return {"status": "success", "data": f"Simulated output for {tool_name}"}
