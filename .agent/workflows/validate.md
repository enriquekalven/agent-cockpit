---
description: Validate changes with full battery of tests
---

To ensure no capabilities or features are broken and the project maintains the Sovereign Standard, follow these steps after every significant change:

// turbo
1. Run the Smoke Test to verify command parity across personas:
   `PYTHONPATH=src .venv/bin/python -m agent_ops_cockpit.ops.reliability audit --smoke --path .`

// turbo
2. Run full Unit Tests:
   `PYTHONPATH=src .venv/bin/python -m pytest .`

// turbo
3. Run the Deep Master Audit (includes Load Tests, Red Team, and Hill Climbing):
   `PYTHONPATH=src .venv/bin/python -m agent_ops_cockpit.cli.main report --verbose --path . --mode deep`

4. Verify that the exit code is 0 and all SME personas show "APPROVED" in the final report.
