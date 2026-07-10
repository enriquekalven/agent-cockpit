"""Unit tests for the VectorSemanticRouter Wisdom Store component."""
import pytest
from agent_ops_cockpit.ops.context.vector_router import VectorSemanticRouter


def test_vector_router_local_embedding_deterministic():
    router = VectorSemanticRouter(use_remote=False)
    vec1 = router.get_embedding_local("Enable Human in the Loop for SecOps.")
    vec2 = router.get_embedding_local("Enable Human in the Loop for SecOps.")
    
    assert len(vec1) == 768
    assert len(vec2) == 768
    assert vec1 == vec2
    
    # Assert L2 Normalization (norm should be ~1.0)
    norm = sum(x * x for x in vec1)
    assert 0.999 <= norm <= 1.001


def test_vector_router_end_to_end_search():
    docs = [
        {
            "name": "SecOps HITL Policy",
            "description": "Enforce Human in the Loop for all destructive cloud actions.",
            "category": "security",
            "content": "Any action wiping disks or deleting VPCs requires MFA and HITL approval.",
        },
        {
            "name": "FinOps Routing Policy",
            "description": "Route bulk reasoning to Gemini Flash.",
            "category": "finops",
            "content": "For standard operations and basic text transformation, do NOT use GPT-4o.",
        },
    ]

    router = VectorSemanticRouter(use_remote=False)
    router.build_index(docs)
    
    # Search for SecOps
    results = router.search("destructive cloud actions and VPCs", limit=1)
    assert len(results) == 1
    assert results[0]["name"] == "SecOps HITL Policy"
    
    # Search for FinOps
    results2 = router.search("GPT-4o and reasoning pricing models", limit=1)
    assert len(results2) == 1
    assert results2[0]["name"] == "FinOps Routing Policy"
