---
description: Fully automate the entire release cycle from code validation to global deployment.
---

// turbo-all
# 🚀 zero2hero: The Sovereign Release Engine

This workflow automates the end-to-end productionization of the AgentOps Cockpit. It ensures structural integrity, updates the intelligence core (Wisdom Store), and executes a multi-cloud/registry deployment.

## Phase 1: Preparation & Intelligence Sync
1. **Upgrade Dependencies**: 
   - `uv sync --upgrade` and `npm install`
   - **Ecosystem Pulse**: Run `agentops-cockpit fleet watch`
   - **Auto-Remediation**: If drift is detected, run `uv add pkg1 pkg2 ...` to sync.
2. **Sovereign Parity Verification**: 
   Ensure `agentops-cockpit sys version` matches the version in `pyproject.toml` and the latest version on PyPI.
   Also verify that `uv` and `make` (or `gmake`) are at the latest stable versions.
   `agentops-cockpit sys version`
   `grep version pyproject.toml`
   `pip index versions agentops-cockpit --index-url https://pypi.org/simple/`
   `uv --version`
   `make --version` (or `gmake --version`)
3. **Version Alignment**: 
   Ensure `pyproject.toml`, `package.json`, and `src/agent_ops_cockpit/` version strings are synchronized.
   `grep version pyproject.toml`
   `grep version package.json`
   `grep VERSION src/agent_ops_cockpit/config.py`
4. **Authentication Check**:
   - **Firebase**: `firebase login` (Ensure "Already logged in as...")
   - **PyPI**: Ensure `PYPI_TOKEN` is exported in the shell.
5. **Synchronize Wisdom Store**: 
   - **Automated Pulse**: Run `agentops-cockpit fleet watch` to ingest the latest research signals and ecosystem patterns into the intelligence core.
   - **Manual Verification**: 
     - Update `src/agent_ops_cockpit/ops/maturity_patterns.json` (Architectural heuristics).
     - Update `src/agent_ops_cockpit/ops/policies.json` (Governance rules).
     - Update `src/agent_ops_cockpit/ops/watchlist.json` (Ecosystem intelligence).
     - Update `CAPABILITIES_REGISTRY.md` (System capabilities).
6. **Strategic Documentation**:
   - Run `python3 scripts/sync_docs.py` to synchronize all guides from `/docs/` to `/public/`.
   - Manually verify that `public/TECHNICAL_UX_GUIDE.md` reflects AGUI and MCP Apps UI.
   - Update `ROADMAP.md`, `CHANGELOG.md`, `README.md` to reflect the latest release capabilities and versioning.

## Phase 2: Structural Verification (The Build Gates)
7. **Clean & Prep**:
   `rm -rf dist/ build/`
8. **Linting & Formatting**:
   `uv run ruff check .` and `npm run lint`
9. **Core Mission & Integrity Audit**:
   - **Capabilities Verification**: Run `PYTHONPATH=src:. uv run pytest src/agent_ops_cockpit/tests/test_capabilities_gate.py` to ensure all 19+ "Distinguished Fellow" capabilities are still active and tested.
   - **No-Regression Check**: Verify that `CAPABILITIES_REGISTRY.md` has not been downgraded or core mission descriptions overwritten.
10. **The Sovereign Gate (SITL Hard-Gate)**:
    - Run `agentops-cockpit certify` and ensure the **Sovereign Score is > 90**. 
    - *Logic Check*: If any "Blocker" capability (CAP-001, CAP-004, CAP-006, etc.) fails, the release MUST be aborted.
11. **Full Regression Suite**: 
    `PYTHONPATH=src:. uv run pytest` (Comprehensive 215-item sweep).

## Phase 3: Global Deployment & Publishing
12. **Frontend Production Build**: 
    - **Aggregate Fleet Telemetry**: `python3 scripts/aggregate_telemetry.py` (Ensures `/metrics` is live).
    - **Synchronize Documentation**: `python3 scripts/sync_docs.py` (Syncs guides to public repo).
    - **Build Assets**: `npm run build`
13. **Firebase Hosting Release**:
    - `firebase deploy --only hosting` (Review live at: https://agent-cockpit.web.app)
14. **Python Package Distribution**: 
    - `uv build`
15. **Git Release Management**:
    - `git add .`
    - `git commit -m "chore: release v[VERSION]"`
    - `git tag v[VERSION]`
    - `git push origin main --tags`
16. **PyPI Global Registry Push**:
    - `uv publish` (Requires `PYPI_TOKEN` set in environment)

## Phase 4: Post-Release Verification
17. **Live Integrity Check**:
    - Visit [https://agent-cockpit.web.app](https://agent-cockpit.web.app) and verify `/metrics` shows updated data.
    - Run `uvx agentops-cockpit --version` to ensure the new version is downloadable and functional.
    - Verify Git Tag is visible on GitHub.

---
*Note: This is a high-fidelity internal workflow for the distinguished owner.*
