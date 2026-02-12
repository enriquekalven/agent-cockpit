try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.4.5 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
from tenacity import retry, wait_exponential, stop_after_attempt
import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from agent_ops_cockpit.ops.remediator import CodeRemediator
from agent_ops_cockpit.ops.arch_review import run_scan
app = typer.Typer(help='Interactive Remediation Workbench v1.4.2: Review and approve autonomous fixes.')
console = Console()

@app.command()
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def review(path: str=typer.Option('.', '--path', '-p', help='Path to the agent project to review')):
    """
    Launch the interactive workbench to review proposed fixes.
    """
    console.print(Panel.fit('🛠️ [bold blue]INTERACTIVE REMEDIATION WORKBENCH[/bold blue]', border_style='blue'))
    with console.status('[bold blue]Scanning for potential fixes...'):
        findings = run_scan(path)
    if not findings:
        console.print('✅ [green]No fixes proposed for this project.[/green]')
        return
    rem_map = {}
    for f in findings:
        if f.file_path and f.file_path.endswith('.py'):
            if f.file_path not in rem_map:
                rem_map[f.file_path] = CodeRemediator(f.file_path)
            if 'Resiliency' in f.title or 'retry' in f.description.lower():
                rem_map[f.file_path].apply_resiliency(f)
            elif 'Zombie' in f.title or 'Timeout' in f.title:
                rem_map[f.file_path].apply_timeouts(f)
            elif 'Caching' in f.title:
                rem_map[f.file_path].apply_caching(f)
            elif 'Hardening' in f.title:
                rem_map[f.file_path].apply_tool_hardening(f)
            elif 'Compaction' in f.title:
                rem_map[f.file_path].apply_context_compaction(f)
    for file_path, remediator in rem_map.items():
        diff = remediator.get_diff()
        if not diff:
            continue
        console.print(f'\n📄 [bold cyan]File: {file_path}[/bold cyan]')
        console.print(Panel(Syntax(diff, 'diff', theme='monokai', line_numbers=True), title='Proposed Changes'))
        choice = typer.prompt('Apply these changes? (y/n/skip)', default='y')
        if choice.lower() == 'y':
            remediator.save()
            console.print('✨ [green]Changes applied successfully.[/green]')
        elif choice.lower() == 'skip':
            console.print('⏭️ [yellow]Skipping this file...[/yellow]')
        else:
            console.print('🚫 [red]Changes rejected.[/red]')
    console.print('\n✅ [bold]Workbench session complete.[/bold]')
if __name__ == '__main__':
    app()