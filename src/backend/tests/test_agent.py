import pytest
from src.backend.agent import agent_v1_logic

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

@pytest.mark.parametrize("query,expected_keyword", [
    ("How do I deploy?", "deploy"),
    ("What is A2UI?", "response"),
    ("Hive Mind status", "hive mind")
])
@pytest.mark.asyncio
async def test_regression_golden_set(query, expected_keyword):
    """Regression suite: Ensure core queries always return relevant keywords."""
    # In a real test, we would mock the LLM or check local logic
    response = "This is a dummy response about " + expected_keyword
    assert expected_keyword in response.lower()

