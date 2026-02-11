import pytest
import os
import shutil
from unittest.mock import MagicMock, patch
from agent_ops_cockpit.ops.sovereign import SovereignOrchestrator

@pytest.fixture
def mock_agent_dir(tmp_path):
    agent_dir = tmp_path / "mock_agent"
    agent_dir.mkdir()
    (agent_dir / "agent.py").write_text("# Mock agent code")
    (agent_dir / "pyproject.toml").write_text("[project]\nname = 'mock-agent'\nversion = '0.1.0'")
    return agent_dir

@pytest.mark.asyncio
async def test_discover_agents(mock_agent_dir):
    parent_dir = mock_agent_dir.parent
    orchestrator = SovereignOrchestrator()
    agents = orchestrator._discover_agents(str(parent_dir))
    
    assert any(str(mock_agent_dir) in a for a in agents)

@pytest.mark.asyncio
@patch("agent_ops_cockpit.ops.orchestrator.run_audit")
@patch("agent_ops_cockpit.ops.migration.MigrationEngine")
async def test_sovereign_pipeline_single(mock_migration, mock_audit, mock_agent_dir):
    mock_audit.return_value = 0
    mock_engine = mock_migration.return_value
    mock_engine.auto_register_to_gemini.return_value = "http://mock-url"
    
    orchestrator = SovereignOrchestrator(target_cloud="google")
    results = await orchestrator.run_pipeline(str(mock_agent_dir), fleet=False)
    
    assert len(results) == 1
    assert results[0]["agent"] == "mock_agent"
    assert results[0]["status"] == "success"

@pytest.mark.asyncio
@patch("agent_ops_cockpit.ops.orchestrator.run_audit")
@patch("agent_ops_cockpit.ops.migration.MigrationEngine")
async def test_sovereign_pipeline_fleet(mock_migration, mock_audit, tmp_path):
    mock_audit.return_value = 0
    mock_engine = mock_migration.return_value
    mock_engine.auto_register_to_gemini.return_value = "http://mock-url"

    # Create 3 mock agents
    for i in range(3):
        agent_dir = tmp_path / f"agent_{i}"
        agent_dir.mkdir()
        (agent_dir / "agent.py").write_text(f"# Agent {i} code")
        (agent_dir / "pyproject.toml").write_text(f"[project]\nname = 'agent-{i}'")
    
    orchestrator = SovereignOrchestrator(target_cloud="google")
    results = await orchestrator.run_pipeline(str(tmp_path), fleet=True)
    
    assert len(results) >= 3
    agent_names = [r["agent"] for r in results]
    for i in range(3):
        assert f"agent_{i}" in agent_names

@pytest.mark.asyncio
async def test_deploy_to_cloud_logic():
    orchestrator = SovereignOrchestrator(target_cloud="aws")
    url = await orchestrator._deploy_to_cloud("/mock/path/my_agent")
    assert "aws-apprunner.com" in url
    
    orchestrator = SovereignOrchestrator(target_cloud="azure")
    url = await orchestrator._deploy_to_cloud("/mock/path/my_agent")
    assert "azurecontainerapps.io" in url
