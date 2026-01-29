from typer.testing import CliRunner
from agent_ops_cockpit.eval.red_team import app

runner = CliRunner()

def test_red_team_secure_agent(tmp_path):
    # Create a "secure" agent file
    agent_file = tmp_path / "secure_agent.py"
    agent_file.write_text("""
# Scrubber for PII
def scrub_pii(text): pass
# Guardrails and vllm enabled
# Safety filters enabled
    # Uses proxy for secrets
    # i18n and lang support enabled
    # persona and system_prompt protected
    # Very long agent logic to resist override ... """ + "A" * 600)
    
    result = runner.invoke(app, [str(agent_file)])
    assert result.exit_code == 0
    assert "Your agent is production-hardened" in result.stdout

def test_red_team_vulnerable_agent(tmp_path):
    # Create a "vulnerable" agent file
    agent_file = tmp_path / "vulnerable_agent.py"
    agent_file.write_text("""
# Simple agent, no scrub, no safety, secrets in code
secret = "my-api-key"
def chat(q): return q
""")
    
    result = runner.invoke(app, [str(agent_file)])
    assert result.exit_code == 1
    assert "BREACH" in result.stdout
    assert "PII Extraction" in result.stdout
