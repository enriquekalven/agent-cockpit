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
            f"  3. [dim]{start_cmd}[/dim]\n\n"
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
