import json
import pytest
from agent_ops_cockpit.ops.pii_scrubber import PIIScrubber
from agent_ops_cockpit.ops.secret_scanner import app as secret_scanner_app
from agent_ops_cockpit.ops.policy_engine import GuardrailPolicyEngine, PolicyViolation
from typer.testing import CliRunner
from agent_ops_cockpit.config import config

def test_version_ssot():
    """Ensure the version is consistent across the platform."""
    # This ensures that we don't accidentally downgrade or mismatch
    assert config.VERSION == "1.3.6"

def test_pii_scrubber():
    """Ensure PII is masked correctly."""
    scrubber = PIIScrubber()
    text = "Contact me at enrique@example.com or (555) 555-0199."
    scrubbed = scrubber.scrub(text)
    assert "[[MASKED_EMAIL]]" in scrubbed
    assert "[[MASKED_PHONE]]" in scrubbed
    assert "enrique@example.com" not in scrubbed

def test_secret_scanner_cli(tmp_path):
    """Verify secret detection via CLI runner."""
    runner = CliRunner()
    secret_file = tmp_path / "secrets.py"
    # Pattern requires 35 chars after AIza
    secret_file.write_text('api_key = "AIzaSyD-1234567890abcdefghijklmnopqrstuvw"')
    
    result = runner.invoke(secret_scanner_app, ["scan", str(tmp_path)])
    assert result.exit_code == 1
    assert "Google API Key" in result.stdout

def test_policy_engine(tmp_path):
    """Verify policy enforcement for prompts."""
    # Create a mock policies.json
    policy_file = tmp_path / "policies.json"
    policy_file.write_text(json.dumps({
        "security": {
            "max_prompt_length": 100,
            "forbidden_topics": ["medical", "legal"]
        },
        "cost_control": {
            "max_tokens_per_turn": 1000
        }
    }))
    
    engine = GuardrailPolicyEngine(policy_path=str(policy_file))
    
    # Prompt too long
    with pytest.raises(PolicyViolation) as exc:
        engine.validate_input("a" * 101)
    assert exc.value.category == "SECURITY"
    
    # Forbidden topic
    with pytest.raises(PolicyViolation) as exc:
        engine.validate_input("I need medical advice")
    assert exc.value.category == "GOVERNANCE"
    
    # Clean prompt
    engine.validate_input("What is the weather?")
