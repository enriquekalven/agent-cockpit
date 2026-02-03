import ast
from agent_ops_cockpit.ops.auditors.sre_a2a import SREAuditor

def test_sre_networking_latency_debt():
    """Principal SRE: Detecting sub-optimal vector retrieval protocols (REST vs gRPC)."""
    code = "vector_db = pinecone.Index('my-index') # No high-perf"
    tree = ast.parse(code)
    auditor = SREAuditor()
    findings = auditor.audit(tree, code, "agent.py")
    assert any("Sub-Optimal Vector Networking" in f.title for f in findings)

def test_sre_compute_performance_debt():
    """Principal SRE: Ensuring CPU Boost for serverless Python agents."""
    code = "# Running on cloud run without boost"
    tree = ast.parse(code)
    auditor = SREAuditor()
    findings = auditor.audit(tree, code, "agent.py")
    assert any("Time-to-Reasoning (TTR) Risk" in f.title for f in findings)

def test_sre_cicd_governance_gate():
    """Principal SRE: Verifying that CI/CD pipelines include blocking Audit Gates."""
    # Mocking a workflow file path to trigger the check
    code = "steps:\n  - run: deploy"
    tree = ast.parse("") 
    auditor = SREAuditor()
    findings = auditor.audit(tree, code, ".github/workflows/main.yml")
    assert any("Sovereign Gate: Bypass Detected" in f.title for f in findings)

def test_sre_regional_proximity_mismatch():
    """Principal SRE: Detecting cross-region latency risks."""
    code = "model_loc = 'us-central1'; db_loc = 'europe-west1'"
    tree = ast.parse(code)
    auditor = SREAuditor()
    findings = auditor.audit(tree, code, "agent.py")
    assert any("Regional Proximity Breach" in f.title for f in findings)

def test_sre_session_persistence_debt():
    """Principal SRE: Ensuring high-performance session state (Redis)."""
    code = "def handle_session(id): self.history.append(id) # No persistence layer"
    tree = ast.parse(code)
    auditor = SREAuditor()
    findings = auditor.audit(tree, code, "agent.py")
    assert any("Short-Term Memory (STM) at Risk" in f.title for f in findings)
