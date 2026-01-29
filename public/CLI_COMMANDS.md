# ⌨️ CLI Reference Guide

The AgentOps Cockpit is designed for automation. Use these commands to manage your agent lifecycle from the terminal or your CI/CD pipeline.

---

## 🏛️ Governance Commands

### `make audit`
**The Quick Safe-Build (15-30s).**
- **Action**: Orchestrates all essential governance modules in parallel: Arch Review → Secrets → Token Optimization → Fast Red-Team.
- **Output**: Generates a high-speed verification report.
- **When to use**: Continuous development and local testing. Default for `make deploy-prod`.

### `make audit-deep`
**The Master Cockpit Auditor (2-5m).**
- **Action**: Comprehensive benchmarking including full Red-Team, Quality Hill Climbing, and Load Testing.
- **Output**: Generates the `cockpit_final_report.md` master benchmarking log.
- **When to use**: Production-gate audits and final compliance checks.

### `make arch-review`
**The Google Well-Architected Auditor.**
- **Action**: Audits your design against Google's best practices.
- **Intelligence**: Automatically detects your stack (**Go, Python, NodeJS, Streamlit, Angular, Lit**) and applies specialized checklists.
- **Output**: A "Cockpit Score" validating your runtime, memory policy, and security guardrails.

### `make scan-secrets`
**The Credential Guard.**
- **Action**: Scans the entire codebase for hardcoded API keys, tokens, and service accounts.
- **Goal**: Prevent sensitive leakages before code is pushed to version control.

### `make red-team`
**The Adversarial Evaluator.**
- **Action**: Launches a self-hacking attack on your agent's system instructions.
- **Goal**: Detect prompt injections, PII leaks, and instruction overrides.

### `make ui-audit` (New!)
**The Face Auditor.**
- **Action**: Analyzes your frontend (React, Angular, Streamlit) for A2UI protocol compliance and accessibility.
- **Goal**: Ensures your agentic interface is responsive and inclusive.

---

## 📉 Optimization Commands

### `agent-ops audit` (CLI Tool)
**The Heuristic Auditor.**
- **Action**: Analyzes prompt length and identifies Context Caching opportunities.
- **Language Aware**: Provides specific Go and NodeJS performance tips.

### `make load-test`
**The Performance Validator.**
- **Action**: Executes concurrency-based stress tests against your agent endpoint.
- **Variables**:
    - `REQUESTS`: Total number of calls (Default: 50).
    - `CONCURRENCY`: Number of simultaneous users (Default: 5).

---

## 🚀 Deployment Commands

### `make dev`
Starts the local development stack:
- **Backend (Engine)**: FastAPI/ADK running at `localhost:8000`.
- **Frontend (Face)**: Vite dev server running at `localhost:5173`.

### `make deploy-prod`
**The 1-Click Production Pipeline.**
1. Runs the Quick Safe-Build (`make audit`).
2. Compiles production frontend assets.
3. Deploys the Engine to **Google Cloud Run**.
4. Deploys the Face to **Firebase Hosting**.

---

## 🧬 Scaffolding

### `agent-ops create <name>`
**The Project Generator.**
- **Options**:
    - `--ui`: Choose your template (`a2ui`, `agui`, `flutter`, `lit`).
    - `--copilotkit`: Enable high-fidelity features for AGUI.
- **Usage**: `uvx agentops-cockpit create my-new-agent --ui a2ui`

