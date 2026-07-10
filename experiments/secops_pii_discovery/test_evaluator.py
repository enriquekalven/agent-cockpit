"""Tests for the evaluator."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import pytest

from evaluator import evaluate_program

INITIAL_CODE = """
import re
from typing import Any, Mapping

PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
}

BENCHMARK_CASES = [
    {"text": "My email is test@example.com", "label": "EMAIL", "count": 1},
    {"text": "def test_aws_key_parser():", "label": None, "count": 0},
]

def solve(text: str) -> dict[str, int]:
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
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for case in BENCHMARK_CASES:
        findings = solve(case["text"])
        target_label = case["label"]
        if target_label:
            if findings.get(target_label, 0) > 0:
                true_positives += 1
            else:
                false_negatives += 1
        else:
            if findings:
                false_positives += len(findings)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0.0

    return {"f1_score": f1}
"""

def test_evaluate_program_returns_score_and_insights():
    """evaluate_program() returns a dict with score and insights."""
    result = evaluate_program(INITIAL_CODE)
    assert isinstance(result["score"], float)
    assert result["score"] >= 0.0
    assert isinstance(result["insights"], list)


def test_evaluate_program_returns_error_insights_on_failure():
    """evaluate_program() returns error insights for bad code."""
    result = evaluate_program("def !!!")
    assert result["score"] is None
    labels = {i["label"] for i in result["insights"]}
    assert "error" in labels
    assert "traceback" in labels


def test_evaluate_program_captures_stdout():
    """stdout from the program is captured as an insight."""
    code = 'print("hello")\ndef evaluate(ei): return {"f1_score": 1.0}'
    result = evaluate_program(code)
    stdout = [i for i in result["insights"] if i["label"] == "stdout"]
    assert len(stdout) == 1
    assert "hello" in stdout[0]["text"]


def test_cli_main_writes_output_file():
    """main() writes a valid JSON output file."""
    tmpdir = tempfile.mkdtemp()
    try:
        shutil.copy("initial_program.py", os.path.join(tmpdir, "initial_program.py"))
        shutil.copy("evaluator.py", os.path.join(tmpdir, "evaluator.py"))
        output_file = os.path.join(tmpdir, "scores.json")

        cmd = [sys.executable, "evaluator.py", "--output-file", output_file, "--program-dir", tmpdir]

        result = subprocess.run(cmd, cwd=tmpdir, capture_output=True, text=True, timeout=60, check=False)
        assert result.returncode == 0, f"stderr: {result.stderr}"

        with open(output_file) as f:
            data = json.load(f)
        assert isinstance(data["score"], (int, float))
        assert "insights" in data
    finally:
        shutil.rmtree(tmpdir)
