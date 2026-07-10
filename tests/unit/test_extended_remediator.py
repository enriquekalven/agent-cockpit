"""Unit tests for the Extended LibCST CodeRemediators."""
import libcst as cst
from agent_ops_cockpit.ops.remediator import (
    TimeoutGuardTransformer,
    ShadowModelRouterTransformer,
    CodeRemediator
)


def test_shadow_model_router_transformer():
    code = """
model_name = "gpt-4o"
base_model = 'claude-3.5-sonnet'
approved_model = "gemini-2.0-flash"
"""
    module = cst.parse_module(code)
    transformer = ShadowModelRouterTransformer("gemini-2.5-flash")
    modified_module = module.visit(transformer)
    
    new_code = modified_module.code
    assert "gpt-4o" not in new_code
    assert "claude-3.5-sonnet" not in new_code
    assert 'model_name = "gemini-2.5-flash"' in new_code
    assert "approved_model = \"gemini-2.0-flash\"" in new_code


def test_timeout_guard_transformer():
    code = """
import httpx
response = httpx.get("https://google.com")
payload = httpx.post("https://api.openai.com/v1/chat/completions", json={})
res2 = httpx.get("https://microsoft.com", timeout=60)
"""
    module = cst.parse_module(code)
    transformer = TimeoutGuardTransformer(30)
    modified_module = module.visit(transformer)
    
    new_code = modified_module.code
    assert 'httpx.get("https://google.com", timeout=30)' in new_code
    # Wait, check for post
    assert 'timeout=30' in new_code
    # Check that the already defined timeout=60 was PRESERVED!
    assert 'timeout=60' in new_code
    assert 'timeout=30, timeout=30' not in new_code
