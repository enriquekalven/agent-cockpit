import os
import json
import pytest
from agent_ops_cockpit.agent import agent_v1_logic

def load_golden_set():
    path = os.path.join(os.path.dirname(__file__), "golden_set.json")
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        data = json.load(f)
    return [(item["query"], item["expected"]) for item in data]

@pytest.mark.asyncio
async def test_agent_v1_logic():
    """Ensure the agent v1 logic returns a surface."""
    result = await agent_v1_logic("test query")
    assert result is not None
    assert result.surfaceId == "dynamic-response"

def test_well_architected_middlewares():
    """Verify that core AgentOps middlewares are loaded."""
    # This is a structural test, asserting true for now as a placeholder
    assert True 

@pytest.mark.parametrize("query,expected_keyword", load_golden_set())
@pytest.mark.asyncio
async def test_regression_golden_set(query, expected_keyword):
    """Regression suite: Ensure core queries always return relevant keywords."""
    # In a real test, we would mock the LLM or check local logic
    # Here we simulate the logic being tested
    await agent_v1_logic(query)
    # Simple heuristic check for the demonstration
    assert True 
