import os
import json
import hashlib
from agent_ops_cockpit.ops.orchestrator import CockpitOrchestrator
from agent_ops_cockpit.ops.discovery import DiscoveryEngine

def test_partitioned_lake_saving(tmp_path):
    """Regression: Ensure evidence lake is partitioned by agent hash."""
    os.chdir(tmp_path)
    orch = CockpitOrchestrator()
    orch.results = {"Security": {"success": True, "output": "Pass"}}
    
    target_path = str(tmp_path / "my_agent")
    os.makedirs(target_path, exist_ok=True)
    target_abs = os.path.abspath(target_path)
    
    orch.save_to_evidence_lake(target_abs)
    
    agent_hash = hashlib.md5(target_abs.encode()).hexdigest()
    partition_path = tmp_path / "evidence_lake" / agent_hash / "latest.json"
    
    assert partition_path.exists()
    with open(partition_path, 'r') as f:
        data = json.load(f)
    assert data["target_path"] == target_abs
    assert data["results"]["Security"]["success"] == True

def test_cockpitignore_respect(tmp_path):
    """Regression: Ensure .cockpitignore is respected by discovery engine."""
    (tmp_path / "agent1").mkdir()
    (tmp_path / "agent1" / "agent.py").touch()
    (tmp_path / "ignored_dir").mkdir()
    (tmp_path / "ignored_dir" / "agent.py").touch()
    
    (tmp_path / ".cockpitignore").write_text("ignored_dir/")
    
    discovery = DiscoveryEngine(str(tmp_path))
    files = list(discovery.walk())
    
    # agent.py in agent1 should be found, but not in ignored_dir
    file_names = [os.path.basename(f) for f in files]
    assert "agent.py" in file_names
    assert not any("ignored_dir" in f for f in files)

def test_severity_exit_codes():
    """Regression: Ensure correct exit codes based on failure type."""
    orch = CockpitOrchestrator()
    
    # 0: All pass
    orch.results = {"Secret Scanner": {"success": True}, "Architecture Review": {"success": True}}
    assert orch.get_exit_code() == 0
    
    # 1: Security Critical
    orch.results = {"Secret Scanner": {"success": False}}
    assert orch.get_exit_code() == 1
    
    # 2: Architecture Violation
    orch.results = {"Secret Scanner": {"success": True}, "Architecture Review": {"success": False}}
    assert orch.get_exit_code() == 2
    
    # 3: General Failure
    orch.results = {"Secret Scanner": {"success": True}, "Reliability (Quick)": {"success": False}}
    assert orch.get_exit_code() == 3
