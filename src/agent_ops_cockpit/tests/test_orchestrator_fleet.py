import os
import json
from agent_ops_cockpit.ops.orchestrator import CockpitOrchestrator, generate_fleet_dashboard

def test_get_dir_hash(tmp_path):
    """Ensure consistent hashing for unchanged directories."""
    agent_dir = tmp_path / "my_agent"
    agent_dir.mkdir()
    (agent_dir / "agent.py").write_text("print('hello')")
    
    orch = CockpitOrchestrator()
    hash1 = orch.get_dir_hash(str(agent_dir))
    hash2 = orch.get_dir_hash(str(agent_dir))
    assert hash1 == hash2
    
    # Change content
    (agent_dir / "agent.py").write_text("print('world')")
    hash3 = orch.get_dir_hash(str(agent_dir))
    assert hash1 != hash3

def test_evidence_lake_saving(tmp_path):
    """Verify that results are saved to the evidence lake."""
    lake_file = tmp_path / ".cockpit" / "evidence_lake.json"
    # Mock current working directory to control where evidence_lake.json is created
    os.chdir(tmp_path)
    
    orch = CockpitOrchestrator()
    orch.results = {"Test Module": {"success": True, "output": "Log output"}}
    target_abs = str(tmp_path / "target_agent")
    os.makedirs(target_abs, exist_ok=True)
    
    orch.save_to_evidence_lake(target_abs)
    
    assert lake_file.exists()
    with open(lake_file, 'r') as f:
        data = json.load(f)
    assert target_abs in data
    assert data[target_abs]["results"]["Test Module"]["success"]

def test_generate_fleet_dashboard(tmp_path):
    """Verify HTML dashboard generation."""
    os.chdir(tmp_path)
    results = {"./agent1": True, "./agent2": False}
    
    # Create a dummy evidence lake to avoid errors
    os.makedirs(".cockpit", exist_ok=True)
    with open(".cockpit/evidence_lake.json", "w") as f:
        json.dump({"global_summary": {"velocity": 5.0}}, f)
        
    generate_fleet_dashboard(results)
    
    dashboard = tmp_path / ".cockpit" / "fleet_dashboard.html"
    assert dashboard.exists()
    content = dashboard.read_text()
    assert "AgentOps Fleet Flight Deck" in content
    assert "PASSED" in content
    assert "FAILED" in content

def test_detect_entry_point(tmp_path):
    """Verify entry point detection heuristics."""
    orch = CockpitOrchestrator()
    
    (tmp_path / "main.py").touch()
    assert orch.detect_entry_point(str(tmp_path)) == "main.py"
    
    # Cleanup and try another
    os.remove(tmp_path / "main.py")
    (tmp_path / "index.js").touch()
    assert orch.detect_entry_point(str(tmp_path)) == "index.js"
    
    # Default
    os.remove(tmp_path / "index.js")
    assert orch.detect_entry_point(str(tmp_path)) == "agent.py"
