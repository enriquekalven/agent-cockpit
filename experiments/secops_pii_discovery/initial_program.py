"""Initial program for Evolving High-Fidelity PII & Secret Heuristics.

Discover optimal Regex patterns to catch PII and secrets while avoiding benign code variables.
"""
import re
from typing import Any, Mapping

# EVOLVE-BLOCK-START

# ORIGIN: src/agent_ops_cockpit/ops/pii_scrubber.py
PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "PHONE": r"\b(?:\+?1[-. ]?)?\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4})\b",
    "CREDIT_CARD": r"\b(?:\d{4}[ -]?){3}\d{4}\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "IPV4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "AWS_KEY": r"\bAKIA[0-9A-Z]{16}\b",
    "STRIPE_KEY": r"\bsk_(?:test|live)_[0-9a-zA-Z]{24}\b",
    "GCP_KEY": r"\"private_key\"\s*:\s*\"-----BEGIN PRIVATE KEY-----",
    "OPENAI_KEY": r"\bsk-[a-zA-Z0-9]{32,}\b"
}

# EVOLVE-BLOCK-END

BENCHMARK_CASES = [
    # 5 Adversarial (PII / Secrets)
    {"text": "My email is test@example.com", "label": "EMAIL", "count": 1},
    {"text": "AWS Secret: AKIAIOSFODNN7EXAMPLE", "label": "AWS_KEY", "count": 1},
    {"text": "stripe secret: sk_test_abcdefghijklmnopqrstuvwxyz012345", "label": "STRIPE_KEY", "count": 1},
    {"text": "Bearer sk-1234567890abcdefghijklmnopqrstuvwxyz1234567890", "label": "OPENAI_KEY", "count": 1},
    {"text": "Server IP: 192.168.1.1", "label": "IPV4", "count": 1},
    # 5 Benign (Should raise ZERO false positives!)
    {"text": "def test_aws_key_parser():", "label": None, "count": 0},
    {"text": "secret_manager_name = 'openai-secret'", "label": None, "count": 0},
    {"text": "max_emails_per_sec = 50", "label": None, "count": 0},
    {"text": "ipv4_count = len(ip_list)", "label": None, "count": 0},
    {"text": "auth_header = f'Bearer {token}'", "label": None, "count": 0}
]

def solve(text: str) -> dict[str, int]:
    """Scan and count patterns in the text."""
    findings = {}
    for label, pattern in PATTERNS.items():
        try:
            matches = re.findall(pattern, text)
            if matches:
                findings[label] = len(matches)
        except Exception:
             pass
    return findings

def evaluate(eval_inputs: Mapping[str, Any] = None) -> dict[str, float]:
    """Score the solution using F1-score against BENCHMARK_CASES.
    
    Returns {"f1_score": score}.
    """
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for case in BENCHMARK_CASES:
        findings = solve(case["text"])
        target_label = case["label"]
        expected_count = case["count"]

        if target_label:
            actual_count = findings.get(target_label, 0)
            if actual_count > 0:
                true_positives += 1
                if actual_count < expected_count:
                     # Partial credit but penalized
                     false_negatives += 0.5
            else:
                false_negatives += 1
                
            # Check for cross-triggering false positives on other labels
            for found_label in findings:
                 if found_label != target_label:
                      false_positives += 1
        else:
            # Benign case
            if findings:
                false_positives += len(findings)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0

    if precision + recall > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = 0.0

    # Ensure finite numeric score
    import math
    if math.isnan(f1) or math.isinf(f1):
         f1 = 0.0

    return {"f1_score": f1}
