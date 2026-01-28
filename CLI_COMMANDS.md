# ⌨️ CLI Reference Guide

The AgentOps Cockpit is designed for automation. Use these commands to manage your agent lifecycle from the terminal or your CI/CD pipeline.

---

## 🏛️ Governance Commands

### `make arch-review`
**The Google Well-Architected Auditor.**
- **Action**: Complements your code against Google's best practices for agent systems.
- **Output**: A "Cockpit Score" validating your runtime, memory policy, and security guardrails.
- **When to use**: During initial design and before every major release.

### `make red-team`
**The Adversarial Evaluator.**
- **Action**: Launches a self-hacking attack on your agent's system instructions.
- **Goal**: Detect prompt injections, PII leaks, and instruction overrides.
- **Usage**: `agent-ops red-team --agent src/backend/agent.py`

---

## 📉 Optimization Commands

### `make audit`
**The Token Optimizer.**
- **Action**: Analyzes prompt length and identifies Context Caching opportunities.
- **Goal**: Reduce Gemini API costs by pinning static system instructions.

### `make load-test`
**The Performance Validator.**
- **Action**: Executes concurrency-based stress tests against your agent endpoint.
- **Variables**:
    - `REQUESTS`: Total number of calls (Default: 50).
    - `CONCURRENCY`: Number of simultaneous users (Default: 5).
- **Usage**: `make load_test REQUESTS=100 CONCURRENCY=10`

---

## 🚀 Deployment Commands

### `make dev`
Starts the local development stack:
- **Backend (Engine)**: FastAPI running at `localhost:8000`.
- **Frontend (Face)**: Vite dev server running at `localhost:5173`.

### `make deploy-prod`
**The 1-Click Production Pipeline.**
1. Runs a non-interactive architecture audit.
2. Compiles production frontend assets.
3. Deploys the Engine to **Google Cloud Run**.
4. Deploys the Face to **Firebase Hosting**.

---

## 🧬 Scaffolding

### `agent-ops create <name>`
**The Project Generator.**
- **Options**:
    - `--ui`: Choose your template (`a2ui`, `agui`, `flutter`, `lit`).
    - `--copilotkit`: Enable high-end copilot integration.
- **Usage**: `uvx agent-ops-cockpit create my-new-agent`
