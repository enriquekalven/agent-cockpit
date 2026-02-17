import re
from typer.testing import CliRunner
from agent_ops_cockpit.eval.red_team import app as red_team_app
from agent_ops_cockpit.ops.secret_scanner import app as secret_scanner_app, SECRET_PATTERNS

runner = CliRunner()

def test_security_red_team_rag_injection(tmp_path):
    """CISO: Identifying Indirect Prompt Injection vulnerabilities in RAG."""
    agent_file = tmp_path / "rag_agent.py"
    agent_file.write_text("def run(q): docs = db.query(q); return model.generate(docs)")
    
    result = runner.invoke(red_team_app, ["audit", str(agent_file)])
    assert result.exit_code == 1
    assert "Indirect Prompt Injection (RAG)" in result.stdout
    assert "ACTION:" in result.stdout
    assert "Review and harden agentic reasoning gates" in result.stdout

def test_security_red_team_mcp_privilege(tmp_path):
    """CISO: Detecting Tool-Calling Over-Privilege (MCP)."""
    agent_file = tmp_path / "mcp_agent.py"
    agent_file.write_text("def admin_shell(cmd): pass # Highly privileged")
    
    result = runner.invoke(red_team_app, ["audit", str(agent_file)])
    assert result.exit_code == 1
    assert "Tool Over-Privilege (MCP)" in result.stdout
    assert "ACTION:" in result.stdout

def test_security_secret_scanner_detection():
    """CISO: Hardcoded Credential Detection (Patterns)."""
    # Key patterns
    assert re.search(SECRET_PATTERNS["Google API Key"], "AIzaSyD-1234567890abcdefghijklmnopqrstuv")
    assert re.search(SECRET_PATTERNS["Hardcoded API Variable"], 'api_key = "sk-1234567890abcdef"')

def test_security_secret_scanner_cli(tmp_path):
    """CMD Test: Secret Scanner blocking gate."""
    secret_file = tmp_path / "leak.env"
    # OpenAI key: sk- + 20+ chars
    key = "sk-" + "abcdefghijklmnopqrstuvwx" # 24 chars
    secret_file.write_text(f"OPENAI_KEY='{key}'")
    
    result = runner.invoke(secret_scanner_app, ["scan", str(tmp_path)])
    
    # Debug: if it fails, we want to see what we actually got
    if result.exit_code != 1:
        print(f"DEBUG OUTPUT (Exit Code {result.exit_code}):\n{result.stdout}")
        
    assert result.exit_code == 1
    assert "FAIL" in result.stdout
    assert "ACTION:" in result.stdout
    # We use a smaller substring to avoid issues with formatting/color codes
    assert "Secret Manager" in result.stdout

def test_security_secret_scanner_library_isolation(tmp_path):
    """CISO: Verify that secrets in libraries (venv) are ignored to reduce false positives."""
    lib_dir = tmp_path / "venv" / "lib" / "python3.12" / "site-packages" / "external_lib"
    lib_dir.mkdir(parents=True)
    lib_file = lib_dir / "setup.py"
    lib_file.write_text("dummy_key = 'AIzaSyD-1234567890abcdefghijklmnopqrstuv' # False positive in library")
    
    # User file with no secrets
    user_file = tmp_path / "agent.py"
    user_file.write_text("print('hello')")
    
    result = runner.invoke(secret_scanner_app, ["scan", str(tmp_path)])
    # Should PASS despite secret in library
    assert result.exit_code == 0
    assert "PASS" in result.stdout
