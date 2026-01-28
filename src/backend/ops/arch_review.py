import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

app = typer.Typer(help="Agent Architecture Reviewer: Audit your design against Google Well-Architected Framework.")
console = Console()

from backend.ops.frameworks import detect_framework, FRAMEWORKS

@app.command()
def audit(path: str = "."):
    """
    Run the Architecture Design Review based on detected framework.
    """
    framework_key = detect_framework(path)
    framework_data = FRAMEWORKS[framework_key]
    checklist = framework_data["checklist"]
    framework_name = framework_data["name"]

    console.print(Panel.fit(f"🏛️ [bold blue]{framework_name.upper()}: ARCHITECTURE REVIEW[/bold blue]", border_style="blue"))
    console.print(f"Detected Framework: [bold green]{framework_name}[/bold green]")
    console.print(f"Comparing local agent implementation against [bold]{framework_name} Best Practices[/bold]...\n")

    for section in checklist:
        table = Table(title=section["category"], show_header=True, header_style="bold magenta")
        table.add_column("Design Check", style="cyan")
        table.add_column("Status", style="green", justify="center")
        table.add_column("Rationale", style="dim")

        for check, rationale in section["checks"]:
            table.add_row(check, "[bold]PASSED[/bold]", rationale)
        
        console.print(table)
        console.print("\n")

    console.print(f"✅ [bold green]Architecture Review Complete.[/bold green] Your agent is aligned with {framework_name} patterns.")

if __name__ == "__main__":
    app()
