import ast
import pytest
from agent_ops_cockpit.ops.auditors.compliance import ComplianceAuditor
from agent_ops_cockpit.ops.auditors.finops import FinOpsAuditor
from agent_ops_cockpit.ops.auditors.sre_a2a import SREAuditor
from agent_ops_cockpit.ops.auditors.maturity import MaturityAuditor
from agent_ops_cockpit.ops.auditors.reliability import ReliabilityAuditor

def test_hardened_compliance_logging():
    """Verify that ComplianceAuditor uses AST to detect structural logging."""
    auditor = ComplianceAuditor()
    
    # Case 1: Naive string match (should still fail if no import/call)
    content_fail = "def my_func():\n    x = 'log the result'"
    tree_fail = ast.parse(content_fail)
    findings = auditor.audit(tree_fail, content_fail, "test.py")
    assert any("SOC2 Control Gap" in f.title for f in findings)

    # Case 2: Structural logging (import)
    content_pass = "import logging\nlogging.info('test')"
    tree_pass = ast.parse(content_pass)
    findings = auditor.audit(tree_pass, content_pass, "test.py")
    assert not any("SOC2 Control Gap" in f.title for f in findings)

def test_hardened_finops_nested_inference():
    """Verify that FinOpsAuditor only applies multiplier for nested inference."""
    auditor = FinOpsAuditor()
    
    # Case 1: Single pass inference
    content_single = "model = 'gemini-3-pro'\nmodel.invoke(q)"
    tree_single = ast.parse(content_single)
    findings = auditor.audit(tree_single, content_single, "test.py")
    assert any("SINGLE PASS" in f.description for f in findings)
    assert any("$2.50" in f.description for f in findings)

    # Case 2: Nested inference in loop
    content_loop = "model = 'gemini-3-pro'\nfor i in range(10):\n    model.invoke(q)"
    tree_loop = ast.parse(content_loop)
    findings = auditor.audit(tree_loop, content_loop, "test.py")
    assert any("LOOP DETECTED" in f.description for f in findings)
    assert any("$25.00" in f.description for f in findings)

def test_hardened_sre_tracing_detection():
    """Verify that SREAuditor detects structural tracing SDKs."""
    auditor = SREAuditor()
    
    # Case 1: No tracing
    content_fail = "def main(): pass"
    tree_fail = ast.parse(content_fail)
    findings = auditor.audit(tree_fail, content_fail, "test.py")
    assert any("Missing 5th Golden Signal" in f.title for f in findings)

    # Case 2: Structural OTEL import
    content_pass = "from opentelemetry import trace\n# traces active"
    tree_pass = ast.parse(content_pass)
    findings = auditor.audit(tree_pass, content_pass, "test.py")
    assert not any("Missing 5th Golden Signal" in f.title for f in findings)

def test_hardened_reliability_url_scrutiny():
    """Verify that ReliabilityAuditor only flags external URLs."""
    auditor = ReliabilityAuditor()
    
    # Case 1: Local path (should NOT be flagged)
    content_local = "requests.get('/local/file.json')"
    tree_local = ast.parse(content_local)
    findings = auditor.audit(tree_local, content_local, "test.py")
    assert not any("Missing Resiliency Logic" in f.title for f in findings)

    # Case 2: External HTTP (SHOULD be flagged)
    content_external = "requests.get('https://api.google.com/data')"
    tree_external = ast.parse(content_external)
    findings = auditor.audit(tree_external, content_external, "test.py")
    assert any("Missing Resiliency Logic" in f.title for f in findings)

def test_maturity_framework_suppression():
    """Verify that MaturityAuditor suppresses advice if framework is present."""
    auditor = MaturityAuditor()
    
    # Case 1: Raw loop (Should trigger advice)
    content_loop = "while True:\n    step()"
    tree_loop = ast.parse(content_loop)
    findings = auditor.audit(tree_loop, content_loop, "agent.py")
    assert any("Orchestration Pattern Selection" in f.title for f in findings)

    # Case 2: LangGraph present (Should SUPPRESS advice)
    content_langgraph = "graph = StateGraph(State)\nwhile True:\n    graph.run()"
    tree_langgraph = ast.parse(content_langgraph)
    findings = auditor.audit(tree_langgraph, content_langgraph, "agent.py")
    assert not any("Orchestration Pattern Selection" in f.title for f in findings)

def test_cockpit_ignore_logic():
    """Verify that # cockpit-ignore correctly suppresses findings."""
    from agent_ops_cockpit.ops.auditors.security import SecurityAuditor
    auditor = SecurityAuditor()
    
    # Case 1: Hardcoded secret (SHOULD be flagged)
    content_secret = "API_KEY = 'sk-1234567890abcdef1234567890abcdef'"
    tree_secret = ast.parse(content_secret)
    findings = auditor.audit(tree_secret, content_secret, "test.py")
    assert any("Hardcoded Secret Detected" in f.title for f in findings)
    
    # Case 2: Hardcoded secret with INLINE ignore (SHOULD be suppressed)
    content_inline = "API_KEY = 'sk-1234567890abcdef1234567890abcdef' # cockpit-ignore: hardcoded-secret"
    tree_inline = ast.parse(content_inline)
    findings = auditor.audit(tree_inline, content_inline, "test.py")
    assert not any("Hardcoded Secret Detected" in f.title for f in findings)
    
    # Case 3: Whole-file ignore (SHOULD be suppressed)
    content_file = "# cockpit-ignore: all\nAPI_KEY = 'sk-1234567890abcdef1234567890abcdef'"
    tree_file = ast.parse(content_file)
    findings = auditor.audit(tree_file, content_file, "test.py")
    assert not any("Hardcoded Secret Detected" in f.title for f in findings)
