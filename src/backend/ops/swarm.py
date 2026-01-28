import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel

console = Console()

@dataclass
class SwarmMessage:
    sender: str
    recipient: str
    content: str
    evidence_packet: Optional[Dict[str, Any]] = None

class MultiAgentOrchestrator:
    """
    Standardizes Swarm/Coordinator patterns using the A2A spec.
    """
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.history: List[SwarmMessage] = []

    def register_agent(self, name: str, agent_func):
        self.agents[name] = agent_func
        console.print(f"🤖 Agent [bold cyan]{name}[/bold cyan] registered in swarm.")

    async def dispatch(self, sender: str, recipient: str, message: str):
        """Dispatches a message with an A2A Reasoning Evidence Packet."""
        console.print(f"\n📡 [dim]A2A Transmission:[/dim] [bold]{sender}[/bold] -> [bold]{recipient}[/bold]")
        
        # Simulated Evidence Packet for Governance
        evidence = {
            "assurance_score": 0.99,
            "origin_vpc": "secure-engine-zone",
            "pii_scrubbed": True
        }
        
        swarm_msg = SwarmMessage(sender, recipient, message, evidence)
        self.history.append(swarm_msg)
        
        if recipient in self.agents:
            response = await self.agents[recipient](message, evidence)
            return response
        else:
            return {"error": f"Agent {recipient} not found."}

    def get_swarm_report(self):
        console.print(Panel.fit("🐝 [bold]Swarm Orchestration Trace[/bold]", border_style="yellow"))
        for msg in self.history:
            console.print(f"[blue]{msg.sender}[/blue] -> [green]{msg.recipient}[/green]: {msg.content}")

def run_swarm_demo():
    orchestrator = MultiAgentOrchestrator()
    
    async def researcher(query, evidence):
        return f"Research results for {query} (Evidence verified: {evidence['assurance_score']})"
        
    async def writer(query, evidence):
        return f"Professional summary of {query}"

    orchestrator.register_agent("Researcher", researcher)
    orchestrator.register_agent("Writer", writer)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(orchestrator.dispatch("Orchestrator", "Researcher", "Analyze market trends"))
    orchestrator.get_swarm_report()

if __name__ == "__main__":
    run_swarm_demo()
