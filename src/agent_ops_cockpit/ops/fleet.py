import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class FleetManager:
    """
    Fleet Lifecycle Manager v1.8.2.
    Manages the state, health, and Day 2 operations for Sovereign fleets.
    """
    def __init__(self, db_path: str = '.cockpit/fleet_registry.json'):
        # Ensure path is absolute relative to workspace if needed, but .cockpit is usually repo root
        self.db_path = db_path
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump([], f)

    def _load_fleet(self) -> List[Dict[str, Any]]:
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_fleet(self, fleet: List[Dict[str, Any]]):
        with open(self.db_path, 'w') as f:
            json.dump(fleet, f, indent=2)

    def register_agent(self, name: str, path: str, cloud: str, endpoint: str, version: str):
        """Registers or updates an agent in the stateful fleet registry."""
        fleet = self._load_fleet()
        existing = next((a for a in fleet if a['name'] == name), None)
        
        agent_data = {
            "name": name,
            "path": os.path.relpath(path, os.getcwd()) if os.path.isabs(path) else path,
            "cloud": cloud,
            "endpoint": endpoint,
            "version": version,
            "status": "HEALTHY",
            "last_seen": datetime.now().isoformat(),
            "created_at": existing['created_at'] if existing else datetime.now().isoformat()
        }
        
        if existing:
            # Preserve created_at
            agent_data["created_at"] = existing["created_at"]
            fleet = [a for a in fleet if a['name'] != name]
            
        fleet.append(agent_data)
        self._save_fleet(fleet)

    def list_fleet(self) -> List[Dict[str, Any]]:
        """Returns the entire fleet registry."""
        return self._load_fleet()

    def update_health(self, name: str, status: str):
        """Day 2 Ops: Update health status of an agent."""
        fleet = self._load_fleet()
        for agent in fleet:
            if agent['name'] == name:
                agent['status'] = status
                agent['last_seen'] = datetime.now().isoformat()
                break
        self._save_fleet(fleet)

    def mothball_fleet(self, cloud: Optional[str] = None, agent_name: Optional[str] = None) -> int:
        """
        FinOps Action: Scale fleet to zero (mocked for now).
        Marks agents as MOTHBALLED to stop incurring costs.
        """
        fleet = self._load_fleet()
        mothballed_count = 0
        for agent in fleet:
            if (not cloud or agent['cloud'] == cloud) and (not agent_name or agent['name'] == agent_name):
                if agent['status'] != "MOTHBALLED":
                    agent['status'] = "MOTHBALLED"
                    agent['last_seen'] = datetime.now().isoformat()
                    mothballed_count += 1
        self._save_fleet(fleet)
        return mothballed_count

    def resume_fleet(self, cloud: Optional[str] = None) -> int:
        """FinOps Action: Resume a mothballed fleet."""
        fleet = self._load_fleet()
        resumed_count = 0
        for agent in fleet:
            if not cloud or agent['cloud'] == cloud:
                if agent['status'] == "MOTHBALLED":
                    agent['status'] = "HEALTHY"
                    agent['last_seen'] = datetime.now().isoformat()
                    resumed_count += 1
        self._save_fleet(fleet)
        return resumed_count

    def monitor_agent_anomaly(self, name: str, telemetry: List[Dict]) -> Dict:
        """
        [v1.6 Watchtower] Perform an asynchronous anomaly audit on live telemetry.
        Triggers auto-enforcement (Mothballing) if risk is too high.
        """
        from .auditors.anomaly_auditor import AnomalySME
        auditor = AnomalySME()
        report = auditor.audit_telemetry(name, telemetry)
        
        # Update health in registry
        fleet = self._load_fleet()
        for agent in fleet:
            if agent['name'] == name:
                agent['status'] = report['status']
                agent['last_seen'] = datetime.now().isoformat()
                
        self._save_fleet(fleet)
        
        # Proactive Enforcement (Active Response Framework)
        if report['auto_remediation_triggered']:
            self.mothball_fleet(agent_name=name)
            
        return report
