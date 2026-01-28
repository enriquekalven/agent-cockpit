import typer
import os
import shutil
import subprocess
from rich.console import Console
from rich.panel import Panel
from typing import Optional

app = typer.Typer(help="AgentOps Cockpit: The AI Agent Operations Platform", no_args_is_help=True)
console = Console()

REPO_URL = "https://github.com/enriquekalven/agent-ui-starter-pack"

@app.command()
def version():
    """Show the version of the Optimized Agent Stack CLI."""
    console.print("[bold cyan]agent-ops CLI v0.1.0[/bold cyan]")

@app.command()
def reliability():
    """
    Run reliability audit (Unit Tests + Regression Suite coverage).
    """
    console.print("🛡️ [bold green]Launching Reliability Audit...[/bold green]")
    subprocess.run([sys.executable, "-m", "backend.ops.reliability", "audit"], env={**os.environ, "PYTHONPATH": "src"})

@app.command()
def report():
    """
    Launch full AgentOps audit (Arch, Quality, Security, Cost) and generate a final report.
    """
    console.print("🕹️ [bold blue]Launching Full System Audit...[/bold blue]")
    subprocess.run([sys.executable, "-m", "backend.ops.orchestrator"], env={**os.environ, "PYTHONPATH": "src"})

@app.command()
def quality_baseline():
    """
    Run iterative 'Hill Climbing' quality audit against a golden dataset.
    """
    console.print("🧗 [bold cyan]Launching Quality Hill Climber...[/bold cyan]")
    subprocess.run([sys.executable, "-m", "backend.eval.quality_climber", "audit"], env={**os.environ, "PYTHONPATH": "src"})

@app.command()
def arch_review():
    """
    Audit agent design against Google Well-Architected Framework.
    """
    console.print("🏛️ [bold blue]Launching Architecture Design Review...[/bold blue]")
    subprocess.run([sys.executable, "-m", "backend.ops.arch_review", "audit"], env={**os.environ, "PYTHONPATH": "src"})

@app.command()
def audit(
    file_path: str = typer.Argument("src/backend/agent.py", help="Path to the agent code to audit"),
):
    """
    Run the Interactive Agent Optimizer audit.
    """
    console.print("🔍 [bold blue]Running Agent Operations Audit...[/bold blue]")
    # Run the optimizer module
    subprocess.run([sys.executable, "-m", "backend.optimizer", "audit", file_path], env={**os.environ, "PYTHONPATH": "src"})

@app.command()
def red_team(
    agent_path: str = typer.Argument("src/backend/agent.py", help="Path to the agent code to audit"),
):
    """
    Run the Red Team adversarial security evaluation.
    """
    console.print("🚩 [bold red]Launching Red Team Evaluation...[/bold red]")
    subprocess.run([sys.executable, "-m", "backend.eval.red_team", "audit", agent_path], env={**os.environ, "PYTHONPATH": "src"})

@app.command()
def load_test(
    url: str = typer.Option("http://localhost:8000/agent/query?q=healthcheck", help="URL to stress test"),
    requests: int = typer.Option(50, help="Total number of requests"),
    concurrency: int = typer.Option(5, help="Number of Concurrent Users"),
) -> None:
    """
    Stress test agent endpoints for performance and reliability.
    """
    console.print("⚡ [bold yellow]Launching Base Load Test...[/bold yellow]")
    subprocess.run([
        sys.executable, "-m", "backend.eval.load_test", "run", 
        "--url", url, 
        "--requests", str(requests), 
        "--concurrency", str(concurrency)
    ], env={**os.environ, "PYTHONPATH": "src"})

@app.command()
def deploy(
    service_name: str = typer.Option("agent-ops-backend", "--name", help="Cloud Run service name"),
    region: str = typer.Option("us-central1", "--region", help="GCP region"),
):
    """
    One-click production deployment (Audit + Build + Deploy).
    """
    console.print(Panel.fit("🚀 [bold green]AGENT COCKPIT: 1-CLICK DEPLOY[/bold green]", border_style="green"))
    
    # 1. Audit
    console.print("\n[bold]Step 1: Code Optimization Audit[/bold]")
    audit_res = subprocess.run([sys.executable, "-m", "backend.optimizer", "audit", "--no-interactive"], env={**os.environ, "PYTHONPATH": "src"})
    
    # 2. Build Frontend
    console.print("\n[bold]Step 2: Building Frontend Assets[/bold]")
    subprocess.run(["npm", "run", "build"], check=True)
    
    # 3. Deploy to Cloud Run
    console.print(f"\n[bold]Step 3: Deploying Engine to Cloud Run ({region})[/bold]")
    deploy_cmd = [
        "gcloud", "run", "deploy", service_name,
        "--source", ".",
        "--region", region,
        "--allow-unauthenticated"
    ]
    subprocess.run(deploy_cmd, check=True)
    
    # 4. Deploy to Firebase
    console.print("\n[bold]Step 4: Deploying Face to Firebase Hosting[/bold]")
    subprocess.run(["firebase", "deploy", "--only", "hosting"], check=True)
    
    console.print("\n✅ [bold green]Deployment Complete![/bold green]")

@app.command()
def create(
    project_name: str = typer.Argument(..., help="The name of the new project"),
    ui: str = typer.Option("a2ui", "-ui", "--ui", help="UI Template (a2ui, agui, flutter, lit)"),
    copilotkit: bool = typer.Option(False, "--copilotkit", help="Enable extra CopilotKit features for AGUI"),
):
    """
    Scaffold a new Agent UI project. Defaults to A2UI (React/Vite).
    """
    console.print(Panel(f"🚀 Creating project: [bold cyan]{project_name}[/bold cyan]", expand=False))
    
    if os.path.exists(project_name):
        console.print(f"[bold red]Error:[/bold red] Directory '{project_name}' already exists.")
        raise typer.Exit(code=1)
        
    try:
        if ui == "agui" or copilotkit:
            console.print("✨ [bold yellow]Note:[/bold yellow] AG UI / CopilotKit selected. Using high-fidelity template.")
        elif ui == "flutter":
            console.print("💙 [bold blue]Note:[/bold blue] Flutter selected. Scaffolding GenUI SDK bridge logic.")
        elif ui == "lit":
            console.print("🔥 [bold orange1]Note:[/bold orange1] Lit selected. Scaffolding Web Components base.")
        
        console.print(f"📡 Cloning template from [cyan]{REPO_URL}[/cyan]...")
        subprocess.run(["git", "clone", "--depth", "1", REPO_URL, project_name], check=True, capture_output=True)
        
        # Remove git tracking
        shutil.rmtree(os.path.join(project_name, ".git"))
        
        # Initialize new git repo
        console.print("🔧 Initializing new git repository...")
        subprocess.run(["git", "init"], cwd=project_name, check=True, capture_output=True)
        
        # UI specific success message
        start_cmd = "npm run dev"
        if ui == "flutter":
            start_cmd = "flutter run"
        
        console.print(Panel(
            f"✅ [bold green]Success![/bold green] Project [bold cyan]{project_name}[/bold cyan] created.\n\n"
            f"[bold]Quick Start:[/bold]\n"
            f"  1. [dim]cd[/dim] {project_name}\n"
            f"  2. [dim]{'npm install' if ui != 'flutter' else 'flutter pub get'}[/dim]\n"
            f"  3. [dim]uvx agent-ops-cockpit audit[/dim]\n"
            f"  4. [dim]{start_cmd}[/dim]\n\n"
            f"Configuration: UI=[bold cyan]{ui}[/bold cyan], CopilotKit=[bold cyan]{'Enabled' if copilotkit else 'Disabled'}[/bold cyan]",
            title="[bold green]Project Scaffolding Complete[/bold green]",
            expand=False,
            border_style="green"
        ))
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error during git operation:[/bold red] {e.stderr.decode() if e.stderr else str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

def main():
    app()

if __name__ == "__main__":
    main()
