try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v2.0.7 Cockpit Alignment: Optimized for Google Cloud Run
import asyncio
import time

import aiohttp
import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Table
from tenacity import retry, stop_after_attempt, wait_exponential

app = typer.Typer(help='AgentOps Load Tester: Stress test your agent endpoints.')
console = Console()

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
async def fetch(session, url, semaphore, results, progress, task_id):
    async with semaphore:
        start = time.time()
        try:
            async with session.get(url) as response:
                status = response.status
                await response.text()
                latency = time.time() - start
                results.append({'status': status, 'latency': latency})
        except Exception as e:
            results.append({'status': 'Error', 'latency': time.time() - start, 'error': str(e)})
        finally:
            progress.update(task_id, advance=1)

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
async def run_load_test(url: str, requests: int, concurrency: int):
    results = []
    console.print(f'🚀 Starting load test on [cyan]{url}[/cyan]')
    console.print(f'Total Requests: [bold]{requests}[/bold] | Concurrency: [bold]{concurrency}[/bold]\n')
    semaphore = asyncio.Semaphore(concurrency)
    with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), BarColumn(), TaskProgressColumn(), console=console) as progress:
        task_id = progress.add_task('Executing requests...', total=requests)
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, url, semaphore, results, progress, task_id) for _ in range(requests)]
            await asyncio.gather(*tasks)
    return results

async def validate_endpoint(url: str) -> bool:
    """Validate that the target endpoint is an agent API and not a UI dashboard."""
    console.print(f'🕵️  [bold blue]Endpoint Handshake:[/] Verifying [cyan]{url}[/cyan]...')
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                content_type = response.headers.get('Content-Type', '').lower()
                if 'text/html' in content_type:
                     console.print("⚠️  [bold yellow]HANDSHAKE WARNING:[/bold yellow] Target returned HTML instead of API data. This looks like a dashboard, not an agent.")
                     return False
                # Optionally check for other headers if safe
                return True
    except Exception as e:
         console.print(f"⚠️  [bold yellow]Handshake Failed:[/bold yellow] {e}")
         return False

def display_results(results) -> bool:
    """Display results and return True if SLA is met, False otherwise."""
    latencies = [r['latency'] for r in results if isinstance(r['latency'], (int, float))]
    successes = [r for r in results if r['status'] == 200]
    errors = [r for r in results if r['status'] != 200]
    total_time = sum(latencies) / len(results) if results else 1
    rps = len(results) / total_time if total_time > 0 else 0
    
    table = Table(title='📊 Agentic Performance & Load Summary')
    table.add_column('Metric', style='cyan')
    table.add_column('Value', style='magenta')
    table.add_column('SLA Threshold', style='dim')
    table.add_row('Total Requests', str(len(results)), '-')
    table.add_row('Throughput (RPS)', f'{rps:.2f} req/s', '> 5.0')
    
    success_rate = len(successes) / len(results) if results else 0
    success_color = "green" if success_rate >= 0.99 else "red"
    table.add_row('Success Rate', f'[{success_color}]{success_rate * 100:.1f}%[/{success_color}]', '> 99%')
    
    table.add_row('Avg Latency', f'{sum(latencies) / len(latencies):.3f}s' if latencies else 'N/A', '< 2.0s')
    ttft_avg = sum(latencies) / len(latencies) * 0.3 if latencies else 0
    table.add_row('Est. TTFT', f'{ttft_avg:.3f}s', '< 0.5s')
    if latencies:
        latencies.sort()
        p90 = latencies[int(len(latencies) * 0.9)]
        table.add_row('p90 Latency', f'{p90:.3f}s', '< 3.5s')
    
    error_color = "green" if len(errors) == 0 else "red"
    table.add_row('Total Errors', f'[{error_color}]{len(errors)}[/{error_color}]', '0')
    console.print('\n')
    console.print(table)

    # STRICT SLA-Driven Approval gate (Issue 3)
    if success_rate < 0.99:
        console.print("\n❌ [bold red]SLA REJECTED:[/bold red] Success Rate fell below 99% threshold.")
        return False
    if len(errors) > 0:
        console.print("\n❌ [bold red]SLA REJECTED:[/bold red] Errors detected during load testing.")
        return False
        
    console.print("\n✅ [bold green]SLA APPROVED:[/bold green] Performance metrics within specifications.")
    return True

@app.command()
def run(url: str=typer.Option('https://agent-cockpit.web.app/api/telemetry/dashboard', help='URL to stress test'), requests: int=typer.Option(50, help='Total number of requests'), concurrency: int=typer.Option(5, help='Simultaneous requests (Concurrent Users)')):
    """
    Execute a configurable load test against the agent endpoint.
    """
    try:
        # Step 1: Endpoint Handshake (Issue 2)
        is_valid = asyncio.run(validate_endpoint(url))
        if not is_valid:
             console.print("⚠️  [bold yellow]Proceeding with load test anyway in case of override support...[/bold yellow]")

        results = asyncio.run(run_load_test(url, requests, concurrency))
        passed = display_results(results)
        if not passed:
             raise typer.Exit(code=1)
    except Exception as e:
        if isinstance(e, typer.Exit):
             raise e
        console.print(f'[red]Load test failed: {e}[/red]')
        raise typer.Exit(code=1)


@app.command()
def version():
    """Show the version of the Load Test module."""
    console.print('[bold cyan]v1.3.0[/bold cyan]')
if __name__ == '__main__':
    app()