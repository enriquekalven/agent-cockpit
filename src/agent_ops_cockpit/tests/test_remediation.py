
import os
from unittest.mock import patch, MagicMock
from agent_ops_cockpit.ops.remediation import apply_remediation

def test_remediation_dry_run_success(tmp_path):
    # Setup a mock vulnerable file
    agent_file = tmp_path / "vulnerable_agent.py"
    agent_file.write_text("def chat(): pass")
    
    # Mock Vertex AI
    with patch("agent_ops_cockpit.ops.remediation.vertexai.init"), \
         patch("agent_ops_cockpit.ops.remediation.GenerativeModel") as mock_model_class:
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "```python\ndef chat():\n    # Security Fix\n    pass\n```"
        mock_model_class.return_value = mock_model
        
        # We need to set env vars for the check to pass
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            success = apply_remediation(str(agent_file), "Missing Safety", "Add safety")
            
            assert success is True
            fixed_code = agent_file.read_text()
            assert "Security Fix" in fixed_code
            assert "def chat():" in fixed_code

def test_remediation_missing_target(tmp_path):
    # No file exists
    success = apply_remediation(str(tmp_path / "ghost.py"), "Issue", "Fix")
    assert success is False
