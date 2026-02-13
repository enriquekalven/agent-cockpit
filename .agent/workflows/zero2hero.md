---
description: Fully automate the entire release cycle from code validation to global deployment.
---

// turbo-all
# 🚀 zero2hero: The Sovereign Release Engine

This workflow automates the end-to-end productionization of the AgentOps Cockpit. It ensures structural integrity, updates the intelligence core (Wisdom Store), and executes a multi-cloud/registry deployment.

## Phase 1: Preparation & Intelligence Sync
1. **Upgrade Dependencies**: 
   `uv sync --upgrade` and `npm install`
2. **Version Alignment**: 
   Ensure `pyproject.toml`, `package.json`, and `src/agent_ops_cockpit/` version strings are synchronized.
3. **Synchronize Wisdom Store**: 
   - Update `src/agent_ops_cockpit/ops/maturity_patterns.json` (Architectural heuristics).
   - Update `src/agent_ops_cockpit/ops/policies.json` (Governance rules).
   - Update `src/agent_ops_cockpit/ops/watchlist.json` (Ecosystem intelligence).
   - Update `CAPABILITIES_REGISTRY.md` (System capabilities).
4. **Strategic Documentation**:
   Update `ROADMAP.md`, `CHANGELOG.md`, `README.md`, and all guides in `/docs/` and `/public/` to reflect the latest release capabilities and versioning.

## Phase 2: Structural Verification (The Build Gates)
5. **Clean & Prep**:
   `rm -rf dist/ build/`
6. **Linting & Formatting**:
   `uv run ruff check .` and `npm run lint`
7. **Core Mission & Integrity Audit**:
   - **Capabilities Verification**: Run `PYTHONPATH=src:. uv run pytest src/agent_ops_cockpit/tests/test_capabilities_gate.py` to ensure all 19+ "Distinguished Fellow" capabilities are still active and tested.
   - **No-Regression Check**: Verify that `CAPABILITIES_REGISTRY.md` has not been downgraded or core mission descriptions overwritten.
8. **The Sovereign Gate (SITL Hard-Gate)**:
   - Run `agentops-cockpit certify` and ensure the **Sovereign Score is > 90**. 
   - *Logic Check*: If any "Blocker" capability (CAP-001, CAP-004, CAP-006, etc.) fails, the release MUST be aborted.
9. **Full Regression Suite**: 
   `PYTHONPATH=src:. uv run pytest` (Comprehensive 215-item sweep).

## Phase 3: Global Deployment & Publishing
7. **Frontend Build & Deploy**: 
   `npm run build` and `firebase deploy --only hosting`
8. **Package Build**: 
   `uv build`
9. **Git Release**:
   `git add .`
   `git commit -m "chore: release v[VERSION]"`
   `git tag v[VERSION]`
   `git push origin main --tags`
10. **Global Registry Push**:
    `uv publish` (Requires PYPI_TOKEN)

---
*Note: This is a high-fidelity internal workflow for the distinguished owner.*
