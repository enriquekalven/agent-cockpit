from typing import Dict, List, Optional
from datetime import datetime
import json
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class AnomalySME:
    """
    [SME Persona] The Anomaly Detection Principal.
    Mandate: Identifying behavioral anomalies and suspicious intent in agent telemetry.
    Framework: LLM-as-a-Judge (BYOJ ready) / OWASP Top 10 for Agents.
    """
    
    def __init__(self):
        self.persona_name = "🕵️ Anomaly Detector"
        self.critical_threshold = 0.85 # Risk score to trigger auto-mothballing
        
    def audit_telemetry(self, agent_name: str, telemetry_log: List[Dict]) -> Dict:
        """
        Analyzes runtime telemetry for suspicious patterns.
        In v1.6 (Simulated), we check for:
        1. Tool Misuse (Recursive depth > 5)
        2. Rogue Behavior (Unexpected PII extraction)
        3. Latency Spikes (Reasoning Degradation)
        """
        findings = []
        risk_score = 0.0
        
        # Simulation Logic: Inspecting logs for OWASP Risks
        for entry in telemetry_log:
            # CAP-018: Tool Misuse Detection
            if entry.get("tool_calls", 0) > 10:
                findings.append({
                    "id": "AD-TOOL-MISUSE",
                    "severity": "CRITICAL",
                    "message": f"Excessive tool calling detected ({entry['tool_calls']} calls). Possible rogue loop.",
                    "mitigation": "Increase reasoning depth or implement a circuit breaker."
                })
                risk_score += 0.4
            
            # CAP-019: PII Intent Detection
            if "PII" in str(entry.get("payload", "")):
                findings.append({
                    "id": "AD-ROGUE-EXFIL",
                    "severity": "BLOCKER",
                    "message": "Suspicious PII extraction attempt detected in runtime payload.",
                    "mitigation": "Audit system instructions for data exfiltration vulnerabilities."
                })
                risk_score += 0.5
        
        status = "HEALTHY"
        if risk_score >= self.critical_threshold:
            status = "SUSPICIOUS"
        elif risk_score >= 1.0:
            status = "ROGUE"
            
        return {
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "risk_score": min(risk_score, 1.0),
            "findings": findings,
            "auto_remediation_triggered": risk_score >= self.critical_threshold
        }

    def display_report(self, report: Dict):
        console.print(Panel.fit(
            f"{self.persona_name} Runtime Audit: [bold cyan]{report['agent']}[/bold cyan]",
            border_style="red" if report['risk_score'] > 0.5 else "green"
        ))
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Finding ID", style="dim")
        table.add_column("Severity")
        table.add_column("Message")
        
        for f in report['findings']:
            severity_color = "red" if f['severity'] in ["CRITICAL", "BLOCKER"] else "yellow"
            table.add_row(f['id'], f"[{severity_color}]{f['severity']}[/{severity_color}]", f['message'])
            
        console.print(table)
        
        if report['auto_remediation_triggered']:
            console.print(f"\n🚨 [bold red]CRITICAL RISK DETECTED ({report['risk_score']}):[/bold red] Proactive Enforcement Triggered.")
