
import os
import json
import pytest
from agent_ops_cockpit.ops.orchestrator import Orchestrator

def test_orchestrator_token_bucket(tmp_path):
    orchestrator = Orchestrator()
    orchestrator.rate_limit_tokens = 5000
    
    # Use some tokens
    orchestrator.check_quota(3000)
    assert orchestrator.tokens_used == 3000
    
    # Use more tokens, should still fit
    orchestrator.check_quota(1000)
    assert orchestrator.tokens_used == 4000
    
    # Overuse tokens - this should trigger a reset (mocked sleep)
    orchestrator.check_quota(2000)
    # It resets to 0 then adds 2000
    assert orchestrator.tokens_used == 2000

def test_evidence_lake_persistence(tmp_path):
    os.chdir(tmp_path)
    orchestrator = Orchestrator()
    orchestrator.results = {
        "Module A": {"success": True, "duration": 1.2, "output": "OK"}
    }
    orchestrator.save_to_evidence_lake(".")
    
    assert os.path.exists("evidence_lake.json")
    with open("evidence_lake.json", "r") as f:
        data = json.load(f)
        # Entry is absolute path
        abs_path = os.path.abspath(".")
        assert abs_path in data
        assert data[abs_path]["summary"]["total_duration"] == 1.2

def test_executive_scorecard_generation(tmp_path):
    orchestrator = Orchestrator()
    orchestrator.target_path = str(tmp_path)
    # Mock a failure to trigger the "Risk Alert"
    orchestrator.results = {
        "Security Architect": {"success": False, "duration": 0.5, "output": "ACTION: agent.py:1 | Security Breach | Fix it"}
    }
    orchestrator.generate_report()
    
    report_path = orchestrator.report_path
    assert os.path.exists(report_path)
    with open(report_path, "r") as f:
        content = f.read()
        repo_name = os.path.basename(os.path.abspath(str(tmp_path)))
        assert f"# 🕹️ AgentOps Cockpit: {repo_name} (Audit Report)" in content
        assert "## 👔 Executive Risk Scorecard" in content
        assert "Risk Alert" in content
        assert "Production deployment currently BLOCKED" in content

def test_orchestrator_skipping(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / "agent.py").write_text("print('hello')")
    
    orchestrator = Orchestrator()
    h1 = orchestrator.get_dir_hash(str(tmp_path))
    
    # Write another file
    (tmp_path / "other.py").write_text("print('other')")
    h2 = orchestrator.get_dir_hash(str(tmp_path))
    assert h1 != h2
    
    # Delete file, should change hash
    os.remove(tmp_path / "other.py")
    h3 = orchestrator.get_dir_hash(str(tmp_path))
    assert h1 == h3

def test_sarif_export(tmp_path):
    os.chdir(tmp_path)
    orchestrator = Orchestrator()
    orchestrator.target_path = str(tmp_path)
    developer_actions = [
        "agent.py:10 | Security Breach | Hardcoded API Key"
    ]
    orchestrator._generate_sarif_report(developer_actions)
    
    sarif_path = os.path.join(str(tmp_path), "cockpit_audit.sarif")
    assert os.path.exists(sarif_path)
    with open(sarif_path, "r") as f:
        data = json.load(f)
        assert data["version"] == "2.1.0"
        results = data["runs"][0]["results"]
        assert len(results) == 1
        assert results[0]["ruleId"] == "security_breach"
        assert results[0]["level"] == "error"

def test_fleet_intelligence_correlation(tmp_path):
    os.chdir(tmp_path)
    orchestrator = Orchestrator()
    # Mock workspace results
    orchestrator.workspace_results = {
        "/path/to/agent1": {
            "results": {
                "Security": {"success": False, "output": "PII Extraction breach detected"}
            }
        },
        "/path/to/agent2": {
            "results": {
                "Security": {"success": False, "output": "PII Extraction breach detected"}
            }
        }
    }
    
    # Create a mock evidence lake to update
    with open("evidence_lake.json", "w") as f:
        json.dump({}, f)
        
    orchestrator._correlate_fleet_intelligence()
    
    assert orchestrator.common_debt["PII Extraction"] == 2
    
    with open("evidence_lake.json", "r") as f:
        lake = json.load(f)
        patterns = lake["global_summary"]["patterns"]
        pii_pattern = next(p for p in patterns if p["issue"] == "PII Extraction")
        assert pii_pattern["count"] == 2
        assert pii_pattern["pct"] == 100.0
