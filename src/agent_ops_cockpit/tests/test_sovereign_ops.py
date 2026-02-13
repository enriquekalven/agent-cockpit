import pytest
import os
import shutil
import tempfile
from unittest.mock import MagicMock, patch
from agent_ops_cockpit.ops.preflight import PreflightEngine
from agent_ops_cockpit.ops.simulator import SovereignSimulator

def test_preflight_registry_access():
    engine = PreflightEngine()
    # Mock socket to avoid real network call
    with patch("socket.create_connection") as mock_socket:
        mock_socket.return_value = MagicMock()
        success, detail = engine.check_registry_access("https://pypi.org")
        assert success is True
        assert "Reachable" in detail

def test_preflight_tooling():
    engine = PreflightEngine()
    with patch("shutil.which") as mock_which:
        mock_which.side_effect = lambda x: True
        success, detail = engine.check_tooling()
        assert success is True
        assert "All base tools detected" in detail

def test_preflight_cloud_auth_simulation():
    engine = PreflightEngine()
    os.environ["SOVEREIGN_SIMULATION"] = "true"
    success, detail = engine.check_cloud_auth("aws")
    assert success is True
    assert "SIMULATION MOCK" in detail
    os.environ.pop("SOVEREIGN_SIMULATION")

@pytest.mark.asyncio
async def test_simulator_hydration_verification():
    sim = SovereignSimulator()
    temp_agent = sim._prepare_mock_agent("test-agent")
    
    # Create fake hydration assets
    with open(os.path.join(temp_agent, "Dockerfile.aws"), "w") as f:
        f.write("FROM python")
    with open(os.path.join(temp_agent, "aws-sam.json"), "w") as f:
        f.write("{}")
    
    verification = sim._verify_hydration(temp_agent, "aws")
    assert verification is True
    
    shutil.rmtree(sim.tmp_dir)

def test_fleet_manager_registration():
    from agent_ops_cockpit.ops.fleet import FleetManager
    with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
        from agent_ops_cockpit.config import config
        manager = FleetManager(db_path=tmp.name)
        manager.register_agent("test-agent", "/tmp/path", "google", "https://test.url", config.VERSION)
        
        fleet = manager.list_fleet()
        assert len(fleet) == 1
        assert fleet[0]["name"] == "test-agent"
        assert fleet[0]["status"] == "HEALTHY"

def test_fleet_manager_mothballing():
    from agent_ops_cockpit.ops.fleet import FleetManager
    with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
        from agent_ops_cockpit.config import config
        manager = FleetManager(db_path=tmp.name)
        manager.register_agent("agent-1", "/tmp/1", "google", "https://url1", config.VERSION)
        manager.register_agent("agent-2", "/tmp/2", "aws", "https://url2", config.VERSION)
        
        # Mothball AWS
        count = manager.mothball_fleet(cloud="aws")
        assert count == 1
        
        fleet = manager.list_fleet()
        a1 = next(a for a in fleet if a["name"] == "agent-1")
        a2 = next(a for a in fleet if a["name"] == "agent-2")
        
        assert a1["status"] == "HEALTHY"
        assert a2["status"] == "MOTHBALLED"
        
        # Resume all
        manager.resume_fleet()
        assert all(a["status"] == "HEALTHY" for a in manager.list_fleet())
