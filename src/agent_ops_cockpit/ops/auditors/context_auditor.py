from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class ContextSME:
    """
    [SME Persona] The Context Optimization Principal.
    Mandate: Visualizing Token windows, Caching efficiency, and Static vs. Dynamic context layers.
    """
    def __init__(self):
        self.persona_name = "🧠 Context Architect"

    def audit(self, path: str):
        console.print(Panel.fit(
            f"{self.persona_name}: Context & Token Audit for [bold cyan]{path}[/bold cyan]",
            border_style="blue"
        ))
        
        # Simulation of scanning for context patterns
        table = Table(title="📊 Context Layer Visualization", show_header=True)
        table.add_column("Layer", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Token usage (Est)", justify="right")
        table.add_column("Caching Status", justify="center")

        table.add_row("System Instructions", "Static", "1,200", "[green]CACHED[/green]")
        table.add_row("Tool Definitions (MCP)", "Static", "3,500", "[green]CACHED[/green]")
        table.add_row("Conversation History", "Dynamic", "8,400", "[yellow]VOLATILE[/yellow]")
        table.add_row("RAG Snippets", "Dynamic", "15,000", "[red]UNOPTIMIZED[/red]")

        console.print(table)
        
        console.print("\n💡 [bold blue]Recommendations:[/bold blue]")
        console.print("1. [bold]Context Caching[/bold]: Move RAG snippets to a cached preamble if reused across turns.")
        console.print("2. [bold]Token Compression[/bold]: High density detected in 'Conversation History'. Consider summarization.")
