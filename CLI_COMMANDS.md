# ⌨️ CLI Reference Guide

The AgentOps Cockpit is designed for automation. Use these commands to manage your agent lifecycle from the terminal or your CI/CD pipeline.

---

## 🏛️ Governance Commands

### `make audit-all`
**The Master Cockpit Auditor.**
- **Action**: Orchestrates all governance modules in sequence: Arch Review → Secrets → Red Team → UI/UX → Optimization → Reliability.
- **Output**: Generates the `cockpit_final_report.md` master log.
- **When to use**: Mandatory before any production deployment.

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

### `make audit`
**The Token Optimizer.**
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
1. Runs the Full Suite Audit (`make audit-all`).
2. Compiles production frontend assets.
3. Deploys the Engine to **Google Cloud Run**.
4. Deploys the Face to **Firebase Hosting**.

---

## 🧬 Scaffolding

### `agent-ops create <name>`
**The Project Generator.**
- **Options**:
    - `--ui`: Choose your template (`a2ui`, `streamlit`, `angular`, `lit`).
    - `--lang`: Choose your engine language (`python`, `go`, `nodejs`).
- **Usage**: `uvx agent-ops-cockpit create my-new-agent --lang go`

