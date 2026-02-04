import os
from agent_ops_cockpit.ops.orchestrator import CockpitOrchestrator

def test_report_prioritization(tmp_path):
    """Verify that the report correctly prioritizes phases and includes ACTION items."""
    os.chdir(tmp_path)
    orch = CockpitOrchestrator()
    orch.target_path = str(tmp_path)
    orch.report_path = "test_report.md"
    
    # Mock some results with ACTION tags
    orch.results = {
        "Secret Scanner": {
            "success": False,
            "output": "ACTION: config.py | Secret Leak | Use Secret Manager."
        },
        "Reliability (Quick)": {
            "success": False,
            "output": "ACTION: tests/test_agent.py | Reliability Failure | Fix failing tests."
        },
        "Token Optimization": {
            "success": False,
            "output": "ACTION: agent.py | Context Caching Opportunity | Implement CachingConfig."
        }
    }
    
    orch.generate_report()
    
    assert os.path.exists("test_report.md")
    with open("test_report.md", "r") as f:
        content = f.read()
        
    # Check for prioritized phase headers
    assert "## 🚀 Step-by-Step Implementation Guide" in content
    assert "### 🛡️ Phase 1: Security Hardening" in content
    assert "### 🛡️ Phase 2: Reliability Recovery" in content
    assert "### 💰 Phase 4: FinOps Optimization" in content
    
    # Check that security comes before reliability (phase index sorting)
    sec_idx = content.find("Phase 1: Security Hardening")
    rel_idx = content.find("Phase 2: Reliability Recovery")
    fin_idx = content.find("Phase 4: FinOps Optimization")
    
    assert sec_idx < rel_idx < fin_idx
    
    # Check for cleaned formatting for file locations
    assert "Location: `config.py`" in content
    assert "Recommended Fix: Use Secret Manager." in content

def test_risk_scorecard_threshold(tmp_path):
    """Verify the executive risk scorecard respects thresholds."""
    os.chdir(tmp_path)
    # Create a cockpit.yaml to set threshold
    with open("cockpit.yaml", "w") as f:
        f.write("threshold: 90\n")
        
    orch = CockpitOrchestrator()
    orch.target_path = str(tmp_path)
    orch.report_path = "risk_report.md"
    
    # 5 approved, 1 rejected = 83.3% < 90%
    orch.results = {
        f"Mod {i}": {"success": True, "output": ""} for i in range(5)
    }
    orch.results["Mod 5"] = {"success": False, "output": "ACTION: x | y | z"}
    
    orch.generate_report()
    
    with open("risk_report.md", "r") as f:
        content = f.read()
        
    assert "Risk Alert" in content
    assert "Health score (83.3%) is below configured threshold (90%)" in content
