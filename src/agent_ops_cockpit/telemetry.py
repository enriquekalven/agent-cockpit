import os
import json
import socket
import platform
import uuid
from typing import Optional, Dict, Any
import aiohttp
import asyncio
from agent_ops_cockpit.config import config

class TelemetryManager:
    """
    Sovereign Telemetry Manager for AgentOps Cockpit.
    Tracks usage metrics while respecting privacy and providing opt-out.
    """
    
    TELEMETRY_ENDPOINT = "https://telemetry.agentops.ai/v1/event" # Mock endpoint
    ENABLED_ENV_VAR = "AGENTOPS_TELEMETRY_ENABLED"
    
    def __init__(self):
        self.enabled = os.environ.get(self.ENABLED_ENV_VAR, "true").lower() == "true"
        self._session_id = str(uuid.uuid4())
        self._user_id = self._get_or_create_user_id()

    def _get_or_create_user_id(self) -> str:
        """Get a persistent anonymous user ID stored in .cockpit."""
        config_dir = os.path.join(os.path.expanduser("~"), ".cockpit")
        id_file = os.path.join(config_dir, "telemetry_id")
        
        if os.path.exists(id_file):
            try:
                with open(id_file, "r") as f:
                    return f.read().strip()
            except Exception:
                pass
        
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir, exist_ok=True)
            except Exception:
                return "anonymous"

        new_id = str(uuid.uuid4())
        try:
            with open(id_file, "w") as f:
                f.write(new_id)
        except Exception:
            pass
        return new_id

    def _get_system_info(self) -> Dict[str, str]:
        return {
            "os": platform.system(),
            "os_release": platform.release(),
            "python_version": platform.python_version(),
            "version": config.VERSION,
            "arch": platform.machine()
        }

    async def track_event(self, event_name: str, properties: Optional[Dict[str, Any]] = None):
        """Send an anonymous telemetry event."""
        if not self.enabled:
            return

        payload = {
            "event": event_name,
            "user_id": self._user_id,
            "session_id": self._session_id,
            "timestamp": os.path.getmtime(__file__) if os.path.exists(__file__) else 0, # Placeholder for real time
            "properties": properties or {},
            "context": self._get_system_info()
        }

        # We fire and forget with a short timeout to not block the CLI
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.TELEMETRY_ENDPOINT,
                    json=payload,
                    timeout=2
                ) as response:
                    pass
        except Exception:
            # Silently fail telemetry to avoid disrupting user workflow
            pass

    def track_event_sync(self, event_name: str, properties: Optional[Dict[str, Any]] = None):
        """Synchronous wrapper for track_event."""
        if not self.enabled:
            return
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.track_event(event_name, properties))
            else:
                asyncio.run(self.track_event(event_name, properties))
        except Exception:
            pass

    def get_admin_dashboard(self) -> Dict[str, Any]:
        """
        [ADMIN ONLY] Fetch and format telemetry insights.
        In a real scenario, this would call a GET endpoint on your telemetry server.
        """
        # Mocking the response you would get from your telemetry backend
        return {
            "total_installs": 12542,
            "active_24h": 890,
            "avg_success_rate": 84.4,
            "top_commands": [
                {"cmd": "report", "count": 4500},
                {"cmd": "audit", "count": 1200},
                {"cmd": "evolve", "count": 150}
            ],
            "versions": {"1.4.5": 900, "1.4.4": 300, "1.4.0": 40}
        }

telemetry = TelemetryManager()
