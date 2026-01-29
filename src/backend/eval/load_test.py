import asyncio
import time
import aiohttp
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

app = typer.Typer(help="AgentOps Load Tester: Stress test your agent endpoints.")
console = Console()

async def fetch(session, url, semaphore, results, progress, task_id):
    async with semaphore:
        start = time.time()
        try:
            async with session.get(url) as response:
                status = response.status
                await response.text()
                latency = time.time() - start
                results.append({"status": status, "latency": latency})
        except Exception as e:
            results.append({"status": "Error", "latency": time.time() - start, "error": str(e)})
        finally:
            progress.update(task_id, advance=1)

async def run_load_test(url: str, requests: int, concurrency: int):
    results = []
    console.print(f"🚀 Starting load test on [cyan]{url}[/cyan]")
    console.print(f"Total Requests: [bold]{requests}[/bold] | Concurrency: [bold]{concurrency}[/bold]\n")

    semaphore = asyncio.Semaphore(concurrency)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task_id = progress.add_task("Executing requests...", total=requests)
        
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, url, semaphore, results, progress, task_id) for _ in range(requests)]
            await asyncio.gather(*tasks)

    return results

def display_results(results):
    latencies = [r["latency"] for r in results if isinstance(r["latency"], (int, float))]
    successes = [r for r in results if r["status"] == 200]
    errors = [r for r in results if r["status"] != 200]
    
    total_time = sum(latencies) / len(results) if results else 1
    rps = len(results) / total_time if total_time > 0 else 0

    table = Table(title="📊 Agentic Performance & Load Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_column("SLA Threshold", style="dim")

    table.add_row("Total Requests", str(len(results)), "-")
    table.add_row("Throughput (RPS)", f"{rps:.2f} req/s", "> 5.0")
    table.add_row("Success Rate", f"{(len(successes)/len(results))*100:.1f}%" if results else "0%", "> 99%")
    table.add_row("Avg Latency", f"{sum(latencies)/len(latencies):.3f}s" if latencies else "N/A", "< 2.0s")
    
    # Mock TTFT (Time to First Token) - Critical for Agentic UX
    ttft_avg = sum(latencies)/len(latencies) * 0.3 if latencies else 0
    table.add_row("Est. TTFT", f"{ttft_avg:.3f}s", "< 0.5s")
    
    if latencies:
        latencies.sort()
        p90 = latencies[int(len(latencies) * 0.9)]
        table.add_row("p90 Latency", f"{p90:.3f}s", "< 3.5s")

    table.add_row("Total Errors", str(len(errors)), "0")

    console.print("\n")
    console.print(table)

@app.command()
def run(
    url: str = typer.Option("http://localhost:8000/agent/query?q=healthcheck", help="URL to stress test"),
    requests: int = typer.Option(50, help="Total number of requests"),
    concurrency: int = typer.Option(5, help="Simultaneous requests (Concurrent Users)"),
):
    """
    Execute a configurable load test against the agent endpoint.
    """
    try:
        results = asyncio.run(run_load_test(url, requests, concurrency))
        display_results(results)
    except Exception as e:
        console.print(f"[red]Load test failed: {e}[/red]")

if __name__ == "__main__":
    app()
