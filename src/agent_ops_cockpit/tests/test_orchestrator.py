
import os
import json
import pytest
from agent_ops_cockpit.ops.orchestrator import CockpitOrchestrator

def test_orchestrator_token_bucket(tmp_path):
    orchestrator = CockpitOrchestrator()
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
    orchestrator = CockpitOrchestrator()
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
    orchestrator = CockpitOrchestrator()
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
        assert "## 👔 Executive Risk Scorecard" in content
        assert "Risk Alert" in content
        assert "Production deployment currently BLOCKED" in content
