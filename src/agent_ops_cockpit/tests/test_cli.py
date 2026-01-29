
import os
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from agent_ops_cockpit.cli.main import app

runner = CliRunner()

def test_cli_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "agent-ops CLI v1.0.0" in result.stdout

def test_cli_diagnose():
    # Test with everything missing
    with patch.dict(os.environ, {}, clear=True), \
         patch("os.path.exists", return_value=False):
        result = runner.invoke(app, ["diagnose"])
        assert result.exit_code == 0
        assert "GOOGLE_API_KEY Missing" in result.stdout
        assert "No Git Repo Detected" in result.stdout

def test_cli_report_sim():
    # Mock orchestrator.run_audit
    with patch("agent_ops_cockpit.ops.orchestrator.run_audit") as mock_run:
        mock_run.return_value = True
        result = runner.invoke(app, ["report", "--sim"])
        assert result.exit_code == 0
        assert "Launching QUICK System Audit..." in result.stdout
        mock_run.assert_called()
        # Verify sim flag was passed
        args, kwargs = mock_run.call_args
        assert kwargs["sim"] is True

def test_cli_fix_command():
    # Mock apply_remediation
    with patch("agent_ops_cockpit.ops.remediation.apply_remediation") as mock_fix:
        mock_fix.return_value = True
        result = runner.invoke(app, ["fix", "my_agent.py", "--issue", "PII"])
        assert result.exit_code == 0
        assert "Remediation complete!" in result.stdout
        mock_fix.assert_called_with("my_agent.py", "PII", "Apply standard safety and architectural patterns")
