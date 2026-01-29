import json
import os
import urllib.request
import xml.etree.ElementTree as ET
import re
import sys
from datetime import datetime
from typing import Dict, Optional
import importlib.metadata
from packaging import version
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

WATCHLIST_PATH = os.path.join(os.path.dirname(__file__), "watchlist.json")

def get_local_version(package_name: str) -> str:
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return "Not Installed"

def clean_version(v_str: str) -> str:
    """Extracts a clean version number from strings like 'v1.2.3', 'package==1.2.3', '2026-01-28 (v0.1.0)'"""
    # Look for patterns like X.Y.Z or X.Y
    match = re.search(r'(\d+\.\d+(?:\.\d+)?(?:[a-zA-Z]+\d+)?)', v_str)
    if match:
        return match.group(1)
    return v_str.strip().lstrip('v')

def fetch_latest_from_atom(url: str) -> Optional[Dict[str, str]]:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            tree = ET.parse(response)
            root = tree.getroot()
            ns = {'ns': 'http://www.w3.org/2005/Atom'}
            
            latest_entry = root.find('ns:entry', ns)
            if latest_entry is not None:
                title = latest_entry.find('ns:title', ns).text
                updated = latest_entry.find('ns:updated', ns).text
                raw_v = title.strip().split()[-1]
                return {
                    "version": clean_version(raw_v) if "==" not in raw_v else clean_version(raw_v.split("==")[-1]),
                    "date": updated,
                    "title": title
                }
    except Exception:
        # console.print(f"[dim red]Error fetching {url}: {e}[/dim red]")
        return None
    return None

def run_watch():
    console.print(Panel.fit("🔍 [bold blue]AGENTOPS COCKPIT: ECOSYSTEM WATCHER[/bold blue]", border_style="blue"))
    
    if not os.path.exists(WATCHLIST_PATH):
        console.print(f"❌ [red]Watchlist not found at {WATCHLIST_PATH}[/red]")
        return

    with open(WATCHLIST_PATH, 'r') as f:
        watchlist = json.load(f)

    table = Table(title=f"Ecosystem Pulse - {datetime.now().strftime('%Y-%m-%d')}", show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan")
    table.add_column("Component", style="white")
    table.add_column("Local", style="yellow")
    table.add_column("Latest", style="green")
    table.add_column("Status", justify="center")

    updates_found = []

    for category, items in watchlist.items():
        for name, info in items.items():
            package = info.get("package")
            local_v_raw = get_local_version(package) if package else None
            local_v = local_v_raw if local_v_raw else "N/A"
            
            with console.status(f"[dim]Checking {name}..."):
                latest_info = fetch_latest_from_atom(info["feed"])
            
            if latest_info:
                latest_v = latest_info["version"]
                
                is_outdated = False
                if local_v_raw and local_v_raw != "Not Installed":
                    try:
                        is_outdated = version.parse(latest_v) > version.parse(local_v_raw)
                    except Exception:
                        is_outdated = latest_v > local_v_raw

                status = "🚨 [bold red]UPDATE[/bold red]" if is_outdated else "✅ [green]OK[/green]"
                if local_v == "Not Installed":
                    status = "➕ [dim]NEW[/dim]"
                if package is None:
                    status = "🌐 [blue]SPEC[/blue]"

                display_local = local_v if local_v != "Not Installed" else "[dim]Not Installed[/dim]"
                table.add_row(
                    category.upper(),
                    name,
                    display_local,
                    latest_v,
                    status
                )

                if is_outdated:
                    updates_found.append({
                        "name": name,
                        "current": local_v,
                        "latest": latest_v,
                        "package": package,
                        "desc": info["description"]
                    })
            else:
                table.add_row(category.upper(), name, local_v, "[red]Fetch Failed[/red]", "❓")

    console.print(table)

    if updates_found:
        console.print("\n[bold yellow]⚠️ Actionable Intelligence:[/bold yellow]")
        for up in updates_found:
            console.print(f"• [bold]{up['name']}[/bold]: {up['current']} ➔ [bold green]{up['latest']}[/bold green]")
            console.print(f"  [dim]{up['desc']}[/dim]")
        
        pkgs = " ".join([u['package'] for u in updates_found if u['package']])
        if pkgs:
            console.print(f"\n[bold cyan]Pro-tip:[/bold cyan] Run `pip install --upgrade {pkgs}` to sync.")
        
        # Exit with special code to signal updates to CI/CD
        sys.exit(2)
    else:
        console.print("\n[bold green]✨ All components are currently in sync with the latest stable releases.[/bold green]")

if __name__ == "__main__":
    run_watch()
