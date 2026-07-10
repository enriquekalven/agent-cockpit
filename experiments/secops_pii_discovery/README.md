# 🧬 AlphaEvolve Experiment: secops_pii_discovery

This directory contains the AlphaEvolve evolutionary search experiment for discovering optimized, high-fidelity PII and API Secret detection heuristics for the AgentOps Cockpit.

## Usage

Run tests to verify the initial program and evaluator:
```bash
uv run pytest
```

Execute the evaluator CLI directly against the seed program:
```bash
uv run python evaluator.py --output-file scores.json --program-dir .
```
