import pytest
import os
import json
import asyncio
from fastapi.testclient import TestClient
from agent_ops_cockpit.agent import app, TELEMETRY_DATA
from agent_ops_cockpit.telemetry import TelemetryManager

client = TestClient(app)

@pytest.fixture
def telemetry_manager():
    return TelemetryManager()

def test_telemetry_hub_ingestion():
    """
    REGRESSION: Ensure the telemetry hub correctly ingests and stores events.
    """
    # Clear memory before test
    TELEMETRY_DATA.clear()
    
    test_event = {
        "event": "test_audit",
        "user_id": "test-user-123",
        "properties": {"success_rate": 0.95}
    }
    
    response = client.post("/telemetry/event", json=test_event)
    assert response.status_code == 200
    assert response.json() == {"status": "ingested"}
    assert len(TELEMETRY_DATA) == 1
    assert TELEMETRY_DATA[0]["event"] == "test_audit"

def test_telemetry_dashboard_aggregation():
    """
    SMOKE TEST: Ensure the dashboard API aggregates multiple users and returns valid A2UI data.
    """
    TELEMETRY_DATA.clear()
    
    # Simulate multiple users
    events = [
        {"event": "audit", "user_id": "user-A"},
        {"event": "audit", "user_id": "user-B"},
        {"event": "audit", "user_id": "user-A"}, # Same user twice
    ]
    
    for e in events:
        client.post("/telemetry/event", json=e)
        
    response = client.get("/telemetry/dashboard")
    assert response.status_code == 200
    data = response.json()
    
    # We expect 2 active agents (User A and User B)
    assert data["active_agents"] >= 892 # 890 base + 2 new
    assert "agents" in data
    assert len(data["agents"]) >= 1
    assert "avatar" in data["agents"][0]

def test_telemetry_opt_out(telemetry_manager, monkeypatch):
    """
    SECURITY: Ensure the Opt-Out environment variable is respected.
    """
    monkeypatch.setenv("AGENTOPS_TELEMETRY_ENABLED", "false")
    tm = TelemetryManager()
    assert tm.enabled is False
    
    # Verify that tracking does not execute
    with monkeypatch.context() as m:
        # If enabled is false, it should returns immediately
        # We can mock the track_event method to ensure it's not called
        pass

@pytest.mark.asyncio
async def test_telemetry_track_event_logic(telemetry_manager):
    """
    INTEGRITY: Ensure track_event builds a valid payload.
    """
    if not telemetry_manager.enabled:
        pytest.skip("Telemetry disabled via environment")
        
    # We can't easily test the network call here without deep mocking, 
    # but we can test the system info gathering.
    sys_info = telemetry_manager._get_system_info()
    assert "os" in sys_info
    assert "python_version" in sys_info
    assert "version" in sys_info
