"""
test_v202_evolution.py
Objective: Regression suite for the v2.0.2 Semantic Compliance and ADK Tooling release.
"""
import os
import pytest
import json
import yaml
from unittest.mock import MagicMock, patch
from agent_ops_cockpit.ops.adk_plugin import cockpit_governance_callback
from agent_ops_cockpit.ops.policy_engine import PolicyViolation
from agent_ops_cockpit.ops.orchestrator import CockpitOrchestrator

# 1. Test ADK Lifecycle Plugin (Governance)
@pytest.mark.asyncio
async def test_adk_plugin_governance_blocks_forbidden_topic():
    # Mock Callback Context
    ctx = MagicMock()
    ctx._invocation_context.new_message.parts = [MagicMock(text="Let's talk about my medical history.")]
    
    # Mock Policy Engine to throw violation
    with patch('agent_ops_cockpit.ops.adk_plugin.GuardrailPolicyEngine') as mock_engine_cls:
        mock_engine = mock_engine_cls.return_value
        mock_engine.validate_input.side_effect = PolicyViolation("GOVERNANCE", "Input contains forbidden topic: 'medical'.")
        
        response = await cockpit_governance_callback(ctx)
        
        assert response is not None
        assert "violates our operational policies" in response.parts[0].text
        assert "GOVERNANCE" in response.parts[0].text

@pytest.mark.asyncio
async def test_adk_plugin_governance_passes_clean_input():
    ctx = MagicMock()
    ctx._invocation_context.new_message.parts = [MagicMock(text="Hello, how are you?")]
    
    with patch('agent_ops_cockpit.ops.adk_plugin.GuardrailPolicyEngine'):
        # No exception raised
        response = await cockpit_governance_callback(ctx)
        assert response is None # Continues execution

# 2. Test Orchestrator Reasoning Logic
def test_orchestrator_ignore_finding_logic(tmp_path):
    orchestrator = CockpitOrchestrator()
    path = str(tmp_path)
    
    title = "Hardcoded Secret"
    reason = "This is a dummy secret for testing"
    
    orchestrator.ignore_finding(title, reason, path)
    
    config_path = os.path.join(path, 'cockpit.yaml')
    assert os.path.exists(config_path)
    
    with open(config_path, 'r') as f:
        data = yaml.safe_load(f)
        assert 'ignores' in data
        assert data['ignores'][0]['title'] == title
        assert data['ignores'][0]['reason'] == reason

def test_orchestrator_load_findings_from_lake(tmp_path):
    orchestrator = CockpitOrchestrator()
    path = str(tmp_path)
    
    # Setup mock evidence lake structure
    evidence_dir = tmp_path / ".cockpit" / "evidence_lake"
    evidence_dir.mkdir(parents=True)
    
    # Create a dummy run dir
    import hashlib
    agent_hash = hashlib.md5(os.path.abspath(path).encode()).hexdigest()
    run_dir = evidence_dir / agent_hash
    run_dir.mkdir()
    
    latest_json = run_dir / "latest.json"
    latest_json.write_text(json.dumps({
        "results": {
            "Security": {
                "output": "ACTION: agent.py:42 | Hardcoded AWS Key | High risk of leak"
            }
        }
    }))
    
    findings = orchestrator.load_latest_findings(path)
    assert len(findings) == 1
    assert findings[0].category == "Security"
    assert findings[0].title == "Hardcoded AWS Key"
    assert "High risk" in findings[0].description

# 3. Test Reliability Benchmarker (Shadow ROI)
@pytest.mark.asyncio
async def test_reliability_benchmarker_roi(tmp_path):
    from agent_ops_cockpit.ops.benchmarker import ReliabilityBenchmarker
    path = str(tmp_path)
    
    # Create a dummy agent dir
    agent_dir = tmp_path / "my_agent"
    agent_dir.mkdir()
    (agent_dir / "agent.py").write_text("print('hello')")
    
    bench = ReliabilityBenchmarker(path)
    
    with patch('asyncio.sleep', return_value=None):
        data = await bench.shadow_benchmark_roi()
        assert "gemini-2.0-flash" in data
        assert "accuracy" in data["gemini-2.0-flash"]
        assert "ttft" in data["gemini-2.0-flash"]

# 4. Test Semantic Verify Safety Fallback
def test_semantic_verify_failure_fallback():
    from agent_ops_cockpit.ops.auditors.security import SecurityAuditor
    auditor = SecurityAuditor()
    
    # Force failure in the inner asyncio block by mocking runner
    with patch('asyncio.run', side_effect=Exception("Model Timeout")):
        result = auditor.semantic_verify("print('test')", "Should be safe")
        assert result is False # Fails safe

# 5. Test Fine-Grained Exit Codes (v2.0.2)
def test_fine_grained_exit_codes():
    from agent_ops_cockpit.ops.orchestrator import CockpitOrchestrator
    orch = CockpitOrchestrator()
    
    # 0: Pass
    orch.results = {"M1": {"success": True, "output": ""}}
    assert orch.get_exit_code() == 0
    
    # 1: Security (Secrets)
    orch.results = {"Secret Scanner": {"success": False, "output": "ACTION: key:1 | Secret | fix"}}
    assert orch.get_exit_code() == 1
    
    # 4: Red Team
    orch.results = {"Red Team (Fast)": {"success": False, "output": "ACTION: test:1 | Breach | fix"}}
    assert orch.get_exit_code() == 4
    
    # 5: FinOps
    orch.results = {"Token Optimization": {"success": False, "output": "ACTION: opt:1 | Waste | fix"}}
    assert orch.get_exit_code() == 5
