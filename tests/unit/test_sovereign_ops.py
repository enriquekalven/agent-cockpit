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
    with open(os.path.join(temp_agent, "Dockerfile.aws"), "w") as f: f.write("FROM python")
    with open(os.path.join(temp_agent, "aws-sam.json"), "w") as f: f.write("{}")
    
    verification = sim._verify_hydration(temp_agent, "aws")
    assert verification is True
    
    shutil.rmtree(sim.tmp_dir)
