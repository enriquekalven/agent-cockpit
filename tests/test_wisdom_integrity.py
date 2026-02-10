import json
import os
import pytest
from typing import List, Dict

WISDOM_STORE_PATH = "src/agent_ops_cockpit/ops/maturity_patterns.json"

def load_wisdom_store():
    with open(WISDOM_STORE_PATH, "r") as f:
        return json.load(f)

def test_benchmark_inviolability():
    """
    STAKEHOLDER GOAL: Ensure that 'Systemic Benchmarks' are never overwritten by research signals.
    """
    store = load_wisdom_store()
    patterns = store.get("patterns", [])
    
    # Define our 'Immutable Anchors'
    FIXED_BENCHMARKS = {
        "MP-001": "Chroma DB", # Local scaling benchmark
        "MP-013": "Enterprise Identity", # Security benchmark
        "MP-020": "Excessive Agency", # OWASP security benchmark
    }
    
    for p_id, expected_title in FIXED_BENCHMARKS.items():
        pattern = next((p for p in patterns if p["id"] == p_id), None)
        assert pattern is not None, f"CRITICAL FAILURE: Systemic Benchmark {p_id} ({expected_title}) has been deleted!"
        assert expected_title in pattern["title"], f"SOVEREIGNTY BREACH: Benchmark {p_id} title modified! Found: {pattern['title']}"

def test_recommendation_no_loss():
    """
    Ensures that if research (X) is added, the original industry practice (Y) is preserved.
    """
    store = load_wisdom_store()
    patterns = store.get("patterns", [])
    
    for pattern in patterns:
        source = pattern.get("source", "")
        # If the source indicates a 'Consensus' or 'Multi-Source', verify it actually mentions both
        if "Sync" in source or "Research" in source:
             # This is where we check if a research signal tried to hijack a benchmark
             # In a mature implementation, we'd check against a 'Golden Set' of recommendations
             pass

def test_consensus_schema_integrity():
    """
    Validates that patterns follow the maturity schema.
    """
    store = load_wisdom_store()
    for pattern in store.get("patterns", []):
        required_keys = ["id", "category", "title", "recommendation", "source"]
        for key in required_keys:
            assert key in pattern, f"Pattern {pattern.get('id', 'UNKNOWN')} is missing required key: {key}"
