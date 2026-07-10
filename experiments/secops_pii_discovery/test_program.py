"""Tests for the initial program."""
from initial_program import evaluate, solve


def test_solve_returns_valid_output():
    """solve() returns output of the expected type/shape."""
    res = solve("Contact us at support@google.com or call 1-800-555-0199.")
    assert "EMAIL" in res
    assert res["EMAIL"] == 1


def test_evaluate_returns_dict_with_metric():
    """evaluate() returns a dict containing the expected metric key."""
    result = evaluate()
    assert "f1_score" in result


def test_evaluate_returns_finite_score():
    """evaluate() returns a finite numeric score for the initial program."""
    result = evaluate()
    score = result["f1_score"]
    assert isinstance(score, (int, float))
    assert score >= 0.0
    assert score <= 1.0
