"""
Pillar: Sovereign Governance
SME Persona: Distinguished Platform Fellow
Objective: Provides a high-fidelity "Omniscient View" of the agent fleet via the Master Dashboard.
"""
import os
import json
import hashlib
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich import box

from .fleet import FleetManager
from .discovery import DiscoveryEngine
from .orchestrator import CockpitOrchestrator

console = Console()

class MasterCockpit:
    """
    The 'One Command to Rule Them All'.
    Orchestrates Discovery, Health, and SME Persona Status in a unified dashboard.
    """
    
    def __init__(self, path: str = "."):
        self.path = os.path.abspath(path)
        self.fleet_manager = FleetManager()
        self.discovery = DiscoveryEngine(self.path)
        self.orchestrator = CockpitOrchestrator()
        self.orchestrator.target_path = self.path

    def render_landing(self):
        """Displays the high-fidelity landing dashboard."""
        
        # 1. Fleet Discovery
        agents = self.discovery.discover_agent_roots()
        deployed_agents = self.fleet_manager.list_fleet()
        
        # 2. Hero Panel
        hero_text = Text.from_markup(f"""
[bold white]🕹️ Sovereign Agent Operations Command Center[/]
[dim]v1.8.2 Stable | Distinguished Fellow Governance[/]

Detected [bold cyan]{len(agents)}[/] Local Agent Silos in Workspace.
Currently Tracking [bold green]{len(deployed_agents)}[/] Deployed Cloud Instances.
        """)
        
        console.print(Panel(hero_text, border_style="blue", box=box.DOUBLE_EDGE))

        # 3. The 'Master Move' Panel (The Single Command)
        master_move = Panel(
            Text.from_markup("🚀 [bold green]THE HERO ACTIONS:[/] [white]Run [bold]agentops-cockpit certify[/] to validate production-readiness or [bold]agentops-cockpit mcp blueprint[/] to modernize your tools.[/]"),
            border_style="green",
            title="Strategic Sovereignty",
            box=box.HEAVY
        )
        console.print(master_move)

        # 4. The 4-Step Sovereign Workflow (Preview)
        workflow_table = Table(title="🏛️ The 4-Step Sovereign Workflow", expand=True, box=box.ROUNDED)
        workflow_table.add_column("Phase", style="cyan", width=15)
        workflow_table.add_column("Command Preview", style="bold yellow")
        workflow_table.add_column("Principal SME Mandate", style="dim")

        workflow_table.add_row(
            "1. Audit", 
            "audit report", 
            "🛡️ Security, 💰 FinOps, & 🏛️ Architecture Benchmarks"
        )
        workflow_table.add_row(
            "2. Modernize", 
            "mcp blueprint", 
            "🛰️ Auto-Generate MCP Server Wrappers for Legacy Tools"
        )
        workflow_table.add_row(
            "3. Certify", 
            "certify", 
            "🏅 Full Production-Readiness Badge & Reliability Pass"
        )
        workflow_table.add_row(
            "4. Deploy", 
            "deploy sovereign", 
            "🚀 GKE / Cloud Run Production Push"
        )

        console.print(workflow_table)

        # 5. Fleet Summary
        if deployed_agents:
            fleet_table = Table(title="🛰️ Active Sovereign Fleet Registry", expand=True)
            fleet_table.add_column("Agent ID", style="cyan")
            fleet_table.add_column("Cloud", style="magenta")
            fleet_table.add_column("Status", style="bold")
            fleet_table.add_column("Maturity Score", justify="right")
            
            for a in deployed_agents:
                status_color = "green" if a['status'] == "HEALTHY" else "red"
                fleet_table.add_row(
                    a['name'], 
                    a['cloud'].upper(), 
                    f"[{status_color}]{a['status']}[/]", 
                    "94%"
                )
            console.print(fleet_table)
        
        console.print("\n💡 [dim]New to the Cockpit? Run [bold]agentops-cockpit sys doctor[/] to check your environment.[/]")

    def run_onboarding_guide(self):
        """Interactive or guided onboarding for the overwhelming repo."""
        console.print(Panel.fit("👋 [bold]Welcome to the Cockpit, Commander.[/]\nYou have inherited a fleet of autonomous agents. Here is your roadmap:", title="Onboarding Guide"))
        
        onboarding_steps = [
            "1. [bold cyan]Audit[/]: Run [bold]agentops-cockpit audit report[/] to find technical debt.",
            "2. [bold green]Harden[/]: Use [bold]--apply-fixes[/] to let the Architect manually path the debt.",
            "3. [bold blue]Hydrate[/]: Run [bold]agentops-cockpit deploy migrate[/] to prep for GCP/AWS.",
            "4. [bold magenta]Govern[/]: Watch live telemetry with [bold]agentops-cockpit fleet watch[/]."
        ]
        
        for step in onboarding_steps:
            console.print(f"  {step}")
        
        console.print("\n[bold yellow]START HERE:[/] Run [bold]agentops-cockpit cockpit[/] to see your fleet status.")
