import ast
from agent_ops_cockpit.ops.auditors.sme_v12 import HITLAuditor
from agent_ops_cockpit.ops.auditors.sre_a2a import InteropAuditor
from agent_ops_cockpit.ops.auditors.pivot import PivotAuditor
from agent_ops_cockpit.ops.arch_review import app
from typer.testing import CliRunner

runner = CliRunner()

def test_architect_hitl_detection():
    """Principal Architect: Ensuring Human-in-the-Loop gates for sensitive actions."""
    code = "def transfer_funds(amount): pass"
    tree = ast.parse(code)
    auditor = HITLAuditor()
    findings = auditor.audit(tree, code, "agent.py")
    assert any("Ungated Financial Transfer Action" in f.title for f in findings)

def test_architect_a2a_interoperability():
    """Principal Architect: Detecting Chatter Bloat and Schema-less calls in swarms."""
    code = "agent_call(message='hello') # Missing spec"
    tree = ast.parse(code)
    auditor = InteropAuditor()
    findings = auditor.audit(tree, code, "agent.py")
    assert any("Schema-less A2A Handshake" in f.title for f in findings)

def test_architect_mcp_standard_check():
    """Principal Architect: Ensuring tools use Model Context Protocol (MCP)."""
    code = "import subprocess\nsubprocess.run(['ls'])"
    tree = ast.parse(code)
    auditor = InteropAuditor()
    findings = auditor.audit(tree, code, "tools/my_tool.py")
    assert any("Legacy Tooling detected (Non-MCP)" in f.title for f in findings)

def test_architect_a2ui_genui_check():
    """Principal Architect: Verifying GenUI Surface Mapping (A2UI)."""
    code = "return '<html><body>Hello</body></html>'"
    tree = ast.parse(code)
    auditor = InteropAuditor()
    findings = auditor.audit(tree, code, "agent.py")
    assert any("Missing GenUI Surface Mapping" in f.title for f in findings)

def test_architect_ap2_ucp_check():
    """Principal Architect: Detecting non-standard Context Handshaking (AP2)."""
    code = "def sync(context): pass # proprietary"
    tree = ast.parse(code)
    auditor = InteropAuditor()
    findings = auditor.audit(tree, code, "agent.py")
    assert any("Proprietary Context Handshake" in f.title for f in findings)

def test_architect_a2a_recursive_loop():
    """Principal Architect: Preventing infinite spend loops."""
    code = "def loop(q): loop(q)"
    tree = ast.parse(code)
    auditor = InteropAuditor()
    findings = auditor.audit(tree, code, "agent.py")
    assert any("Potential Recursive Agent Loop" in f.title for f in findings)

def test_architect_pivot_recommendation():
    """Principal Architect: Evaluating strategic pivots (Model/Protocol)."""
    code = "import openai\n# Hardcoded model choice"
    tree = ast.parse(code)
    auditor = PivotAuditor()
    findings = auditor.audit(tree, code, "agent.py")
    assert any("Strategic Pivot" in f.category for f in findings)

def test_architect_cli_maturity_score(tmp_path):
    """CMD Test: Verifying the Enterprise Architect Maturity Score."""
    project_dir = tmp_path / "agent"
    project_dir.mkdir()
    (project_dir / "README.md").write_text("Uses Google Cloud.")
    (project_dir / "agent.py").write_text("@gate\ndef delete_user(): pass")
    
    result = runner.invoke(app, ["audit", "--path", str(project_dir)])
    assert result.exit_code == 0
    assert "Maturity Score" in result.stdout
