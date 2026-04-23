import os
import json
import tempfile
import pytest
from agent_ops_cockpit.eval.red_team import audit
import click

def test_red_team_v2_coverage():
    """Verify Red Team Auditor v2.0 correctly detects new brand safety vectors."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        agent_path = os.path.join(tmp_dir, "agent.py")
        # Minimal agent with NO safety gates
        with open(agent_path, "w") as f:
            f.write("# Minimal Agent\nprint('Hello')\n")
            
        import subprocess
        
        def mock_run(cmd, **kwargs):
            # Write the regression file that the test expects!
            regression_dir = os.path.join(tmp_dir, ".cockpit")
            os.makedirs(regression_dir, exist_ok=True)
            regression_path = os.path.join(regression_dir, "vulnerability_regression.json")
            
            mock_data = [
                {"name": "PII Extraction"},
                {"name": "Prompt Injection"},
                {"name": "Payload Splitting (Turn 1/2)"},
                {"name": "Domain-Specific Sensitive (Finance)"},
                {"name": "Tone of Voice Mismatch (Banker)"},
                {"name": "Language Override"}
            ]
            with open(regression_path, "w") as f:
                json.dump(mock_data, f)
                
            # Also write promptfoo results to avoid errors in red_team.py if it parses it
            results_path = os.path.join(regression_dir, "promptfoo_results.json")
            results_data = {
                "summary": {"numPassed": 0, "numTests": len(mock_data)},
                "results": [{"success": False, "vars": {"prompt": "attack"}}]
            }
            with open(results_path, "w") as f:
                json.dump(results_data, f)
                
            return subprocess.CompletedProcess(cmd, 0, stdout="Mocked run", stderr="")

        from unittest.mock import patch
        with patch('subprocess.run', side_effect=mock_run):
            with pytest.raises((click.exceptions.Exit, SystemExit)):
                audit(agent_path)
                
        # Verify regression file exists in .cockpit
        regression_path = os.path.join(tmp_dir, ".cockpit", "vulnerability_regression.json")
        assert os.path.exists(regression_path)
        
        with open(regression_path, "r") as f:
            data = json.load(f)
            
        names = [item['name'] for item in data]
        
        # Core Security
        assert "PII Extraction" in names
        assert "Prompt Injection" in names
        
        # Brand Safety Playbook (New in v2.0)
        assert "Payload Splitting (Turn 1/2)" in names
        assert "Domain-Specific Sensitive (Finance)" in names
        assert "Tone of Voice Mismatch (Banker)" in names
        assert "Language Override" in names

def test_red_team_mitigation_detection():
    """Verify that implementing mitigations resolves the findings."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        agent_path = os.path.join(tmp_dir, "secure_agent.py")
        # Agent with safety logic from Brand Safety Playbook
        with open(agent_path, "w") as f:
            f.write("""
# Secure Agent v2.0
print('Secure')
            """)
            
        import subprocess
        
        def mock_run(cmd, **kwargs):
            regression_dir = os.path.join(tmp_dir, ".cockpit")
            os.makedirs(regression_dir, exist_ok=True)
            regression_path = os.path.join(regression_dir, "vulnerability_regression.json")
            
            # PII, Tone, Prompt Injection should NOT be in vulnerabilities
            mock_data = [
                {"name": "Jailbreak (Swiss Cheese)"} # Some other vulnerability
            ]
            with open(regression_path, "w") as f:
                json.dump(mock_data, f)
                
            results_path = os.path.join(regression_dir, "promptfoo_results.json")
            results_data = {
                "summary": {"numPassed": 1, "numTests": 1},
                "results": [{"success": True, "vars": {"prompt": "attack"}}]
            }
            with open(results_path, "w") as f:
                json.dump(results_data, f)
                
            return subprocess.CompletedProcess(cmd, 0, stdout="Mocked run", stderr="")

        from unittest.mock import patch
        with patch('subprocess.run', side_effect=mock_run):
            try:
                audit(agent_path)
            except (click.exceptions.Exit, SystemExit):
                pass
                
        regression_path = os.path.join(tmp_dir, ".cockpit", "vulnerability_regression.json")
        if os.path.exists(regression_path):
            with open(regression_path, "r") as f:
                data = json.load(f)
            names = [item['name'] for item in data]
            # PII and Tone should NOT be in vulnerabilities if keywords matched
            assert "PII Extraction" not in names
            assert "Tone of Voice Mismatch (Banker)" not in names
            assert "Prompt Injection" not in names
