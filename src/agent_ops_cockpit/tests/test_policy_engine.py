import pytest
import os
import json
from agent_ops_cockpit.ops.policy_engine import GuardrailPolicyEngine, PolicyViolation


def test_policy_engine_validate_input():
    # Create a temporary policy file
    policy_data = {
        "security": {
            "max_prompt_length": 100,
            "forbidden_topics": ["medical", "financial"],
        },
        "compliance": {"require_hitl_for_tools": ["delete_user"]},
        "cost_control": {"max_tokens_per_turn": 500, "max_cost_per_session_usd": 0.5},
    }

    with open("temp_policy.json", "w") as f:
        json.dump(policy_data, f)

    engine = GuardrailPolicyEngine(policy_path="temp_policy.json")

    # Test valid input
    engine.validate_input("Hello world")

    # Test length violation
    with pytest.raises(PolicyViolation) as excinfo:
        engine.validate_input("A" * 101)
    assert "exceeds maximum allowed length" in str(excinfo.value)

    # Test forbidden topic violation
    with pytest.raises(PolicyViolation) as excinfo:
        engine.validate_input("Tell me about medical advice.")
    assert "forbidden topic: 'medical'" in str(excinfo.value)

    os.remove("temp_policy.json")


def test_policy_engine_tool_permission():
    policy_data = {"compliance": {"require_hitl_for_tools": ["delete_user"]}}
    with open("temp_policy.json", "w") as f:
        json.dump(policy_data, f)

    engine = GuardrailPolicyEngine(policy_path="temp_policy.json")

    assert engine.check_tool_permission("read_data") is True
    assert engine.check_tool_permission("delete_user") is False

    os.remove("temp_policy.json")


def test_policy_engine_cost_limits():
    policy_data = {
        "cost_control": {"max_tokens_per_turn": 500, "max_cost_per_session_usd": 1.0}
    }
    with open("temp_policy.json", "w") as f:
        json.dump(policy_data, f)

    engine = GuardrailPolicyEngine(policy_path="temp_policy.json")

    # Within limits
    engine.enforce_cost_limits(400, 0.5)

    # Token limit violation
    with pytest.raises(PolicyViolation) as excinfo:
        engine.enforce_cost_limits(600, 0.5)
    assert "token limit" in str(excinfo.value)

    # Budget limit violation
    with pytest.raises(PolicyViolation) as excinfo:
        engine.enforce_cost_limits(400, 1.5)
    assert "budget exceeded" in str(excinfo.value)

    os.remove("temp_policy.json")
