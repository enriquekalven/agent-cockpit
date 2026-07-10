---
description: Fully automate the entire release cycle from code validation to global deployment with AI-augmented quality gates.
---

// turbo-all
# 🚀 zero2hero: The Autonomous Release Engine (v2.0.20+ Distinguished Edition)

This workflow automates the end-to-end productionization of the AgentOps Cockpit. It ensures structural integrity, updates the intelligence core (Wisdom Store), executes multi-turn evaluation drift testing, and orchestrates global deployments.

## Phase 1: Preparation, Version Bumping & Intelligence Sync
1. **Semantic Version Sync**: 
   - Extract and increment the patch version (e.g. `2.0.20` -> `2.0.21`).
   - Synchronize across `pyproject.toml`, `package.json`, and `src/agent_ops_cockpit/config.py`.
2. **Upgrade Dependencies & Security Sweeps**: 
   - `uv sync --upgrade` and `npm install`
   - **Ecosystem Pulse**: Run `cockpit fleet watch` to catch drift.
   - **Secret Scanner Check**: Run `cockpit audit security` to guarantee zero leaked API tokens or credentials.
3. **Synchronize Wisdom Store**: 
   - **Context Hub Core**: Run `python3 scripts/sync_docs.py` to synchronize governance skills into the dynamic BM25 registry (`.cockpit/context_registry.json`).
   - **Manual Heuristic Updates**: 
     - Verify `src/agent_ops_cockpit/ops/maturity_patterns.json` (Architectural SME Wisdom).
     - Verify `src/agent_ops_cockpit/ops/policies.json` (Declarative Guardrail Rules).
4. **AI-Driven Changelog Generation**:
   - Leverage Gemini (`gemini-2.0-flash`) via the ADK to read `git log` and `git diff`, and append a high-fidelity Markdown delta to `CHANGELOG.md`.

## Phase 2: Structural Verification & Multi-Turn Drift Gates
5. **Linting & Formatting**:
   - Run `uv run ruff check src/agent_ops_cockpit/ --fix` and `npm run lint`.
6. **Live Cockpit Gateway Proxy Validation**:
   - Validate that the OpenAI-to-Gemini FastAPI proxy sidecar (`ops/gateway.py`) successfully passes its test suite (`test_gateway.py`) in both Live and Resilient Mock modes.
7. **The AIOps 10-Turn Drift Test Gate**:
   - Execute `cockpit test drift --path ./my_super_agent` to battle-test multi-turn persona stability and instruction retention. Minimum score required: **>= 4.0/5.0**.
8. **The Autonomous Gate (SITL Hard-Gate)**:
   - Run `cockpit certify` and ensure the **Autonomous Cockpit Score is > 90%**. 
   - *Logic Check*: If any "Blocker" capability (CAP-001, CAP-004, CAP-006, CAP-032) fails, the release MUST be aborted.
9. **Full Regression Suite**: 
   - `uv run pytest` (Ensure flawless **229/229 Passed** status).

## Phase 3: Global Deployment, Publishing & Tagging
10. **Frontend Production Build**: 
    - **Aggregate Fleet Telemetry**: `python3 scripts/aggregate_telemetry.py` (Ensures `/metrics` is live and hydrated).
    - **Build Assets**: `npm run build`
11. **Firebase Hosting Release**:
    - `firebase deploy --only hosting` (Review live fleet face at: https://agent-cockpit.web.app)
12. **Python Package Distribution**: 
    - `rm -rf dist/ build/`
    - `uv build`
13. **Git Release Management**:
    - `git checkout -b release/v[VERSION]`
    - `git add .`
    - `git commit -m "chore: release v[VERSION]"`
    - `git tag v[VERSION]`
    - `git push origin release/v[VERSION] --tags`
14. **PyPI Global Registry Push**:
    - `uv publish` (Requires `PYPI_TOKEN` set in environment).

## Phase 4: Post-Release Verification
15. **Live Integrity Check**:
    - Visit [https://agent-cockpit.web.app](https://agent-cockpit.web.app) and verify `/metrics` shows updated telemetries.
    - Run `uvx agentops-cockpit --version` to ensure the new package is downloadable.

---
*Note: This is a high-fidelity internal workflow for the Distinguished Platform Fellow and Fleet Owner.*
