from agent_ops_cockpit.ops.remediator import CodeRemediator
from agent_ops_cockpit.ops.auditors.base import AuditFinding

def test_apply_resiliency(tmp_path):
    """Test that CodeRemediator injects @retry and imports correctly."""
    code_path = tmp_path / "agent.py"
    code_path.write_text("""
def unprotected_call():
    return fetch_data()
""")
    
    finding = AuditFinding(
        category="Reliability",
        title="Missing Resiliency Strategy",
        description="Add retry logic",
        impact="High",
        roi="Low",
        file_path=str(code_path),
        line_number=2
    )
    
    remediator = CodeRemediator(str(code_path))
    remediator.apply_resiliency(finding)
    remediator.save()
    
    new_code = code_path.read_text()
    assert "from tenacity import retry, wait_exponential, stop_after_attempt" in new_code
    assert "@retry(" in new_code
    assert "def unprotected_call():" in new_code

def test_apply_timeouts(tmp_path):
    """Test that CodeRemediator injects timeout=10 to async calls."""
    code_path = tmp_path / "agent.py"
    # Using a simple call that would be targeted by find_by_line
    code_path.write_text("""
async def call_api():
    await client.get("url")
""")
    
    finding = AuditFinding(
        category="Reliability",
        title="Zombie Thread Risk",
        description="Missing timeout on async call",
        impact="High",
        roi="Medium",
        file_path=str(code_path),
        line_number=3
    )
    
    remediator = CodeRemediator(str(code_path))
    remediator.apply_timeouts(finding)
    remediator.save()
    
    new_code = code_path.read_text()
    assert "timeout=10" in new_code

def test_save_idempotency(tmp_path):
    """Ensure saving twice doesn't corrupt the file."""
    code_path = tmp_path / "agent.py"
    original_code = "def foo():\n    pass\n"
    code_path.write_text(original_code)
    
    remediator = CodeRemediator(str(code_path))
    remediator.save()
    
    # ast.unparse might change formatting slightly, but the logic should hold
    saved_code = code_path.read_text()
    
    remediator2 = CodeRemediator(str(code_path))
    remediator2.save()
    
    assert saved_code == code_path.read_text()

def test_apply_tool_hardening(tmp_path):
    """Test injection of Literal and Poka-Yoke comment."""
    code_path = tmp_path / "agent.py"
    code_path.write_text("def my_tool(mode: str):\n    pass")
    
    finding = AuditFinding("Reliability", "Hardening", "Use Literal", "High", "High", line_number=1, file_path=str(code_path))
    remediator = CodeRemediator(str(code_path))
    remediator.apply_tool_hardening(finding)
    remediator.save()
    
    content = code_path.read_text()
    assert "from typing import Literal" in content
    assert "POKA-YOKE" in content

def test_apply_context_compaction(tmp_path):
    """Test injection of compact_history strategy."""
    code_path = tmp_path / "agent.py"
    code_path.write_text("import os\n\nclass Agent:\n    pass")
    
    finding = AuditFinding("FinOps", "Compaction", "Add strategy", "Medium", "Medium", line_number=3, file_path=str(code_path))
    remediator = CodeRemediator(str(code_path))
    remediator.apply_context_compaction(finding)
    remediator.save()
    
    content = code_path.read_text()
    assert "def compact_history" in content
    assert "limit: int = 10" in content
