# ⌨️ Master Guide: AgentOps UVX Commands
## Portable Governance & Automation (v1.6.6 Stable)

This document provides a consolidated reference for all **`uvx`** commands available in the AgentOps ecosystem. `uvx` allows you to run these tools instantly without a local installation, making them ideal for CI/CD pipelines, ephemeral environments, and auditing external repositories.

The primary package is **`agentops-cockpit`**, which exposes the **`agentops-cockpit`** (alias `agent-ops`) binaries.

### ⚙️ The Portability Engine
Unlike standard CLI tools, the AgentOps `uvx` distribution uses **Binary Shimming**. This allows the tool to execute in an isolated environment with its own dependencies (e.g., specific versions of `ast`, `tenacity`, and `google-cloud-aiplatform`) without polluting the host's global Python space.

---

## 🏗️ Master Orchestration
Run the full range of AgentOps intelligence against any project or file.

| Command | Objective | Mode/Flags |
| :--- | :--- | :--- |
| `uvx agentops-cockpit report` | **Full Master Audit** | `--mode quick` (default) or `deep` |
| `uvx agentops-cockpit version` | **Version Check** | Display current CLI and Engine version. |
| `uvx agentops-cockpit diagnose`| **System Check** | Verify GCP Auth, API keys, and environment paths. |
| `uvx agentops-cockpit audit-maturity`| **Maturity Matrix**| v1.6.6: Expert competency and persona status dashboard. |
| `uvx agentops-cockpit email-report`| **Stakeholder Sync** | Send latest report (Usage: `... email-report user@example.com`) |

---

## 🏛️ Architecture & Interop
Audit designs against the Google Well-Architected Framework and Multi-Cloud Maturity Store.

| Command | Objective | Flags |
| :--- | :--- | :--- |
| `uvx agentops-cockpit arch-review`| **Architecture Review**| v1.4: Maturity Wisdom Store integration. |
| `uvx agentops-cockpit mcp-server` | **MCP Hub** | Start the Model Context Protocol Hub. |

---

## 🧗 AI Quality & Evaluation
Iterative science for the reasoning layer.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `uvx agentops-cockpit quality-baseline`| **Hill Climbing** | Iterative prompt optimization loop. |
| `uvx agentops-cockpit rag-truth` | **RAG Fidelity** | v1.4: Citation and grounding logic audit. |
| `uvx agentops-cockpit reliability` | **Unit Regression** | Runs core reliability suite. Use `--smoke` for E2E. |
| `uvx agentops-cockpit smoke-test` | **Persona Journey** | Validates the "Face" pillar via interactive pipelines. |

---

## 🚩 Security & Policy
Adversarial audits and declarative guardrail enforcement.

| Command | Objective | Flags |
| :--- | :--- | :--- |
| `uvx agentops-cockpit red-team` | **Adversarial Audit** | v1.4: Brand Safety Playbook integration. |
| `uvx agentops-cockpit policy-audit` | **Guardrail Check** | `--text "query"` to validate against the Policy Engine. |
| `uvx agentops-cockpit scan-secrets` | **Credential Leak Scan** | Scans for keys with Library Isolation. |

---

## 🛡️ Governance & Discovery
Intelligent workspace mapping and isolation.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `cockpit.yaml` | **Governance Config** | Define `entry_point`, `exclude`, and `threshold`. |
| Discovery Engine | **Auto-Discovery** | Logic that respects `.gitignore` and ignores `venv`. |

---

## 💰 FinOps & Infrastructure
Economic engineering and performance benchmarking.

| Command | Objective | Flags |
| :--- | :--- | :--- |
| `uvx agentops-cockpit audit` | **Token Optimizer** | `--quick` to skip live evidence; `--no-interactive` for CI. |
| `uvx agentops-cockpit report --roi` | **ROI Waterfall** | v1.4: Monthly cost modeling and efficiency pivots. |
| `uvx agentops-cockpit load-test` | **Stress Benchmarking** | `--url`, `--requests`, `--concurrency`. |

---

## 🎭 UX/UI & GenUI
Auditing the "Face" pillar for protocol compliance.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `uvx agentops-cockpit ui-audit` | **Face Auditor** | Scans frontend code for A2UI / `surfaceId` alignment. |

---

## 🚀 Scaffolding & Deployment
Initialize new projects and push to Google Cloud.

| Command | Objective | Flags |
| :--- | :--- | :--- |
| `uvx agentops-cockpit init` | **Trinity Scaffolder** | Fast-path initialization of Engine + Face + Cockpit. |
| `uvx agentops-cockpit deploy-prod` | **Readiness Audit** | Full Master Audit gate for production-readiness benchmarking. |

---

```bash
uvx agentops-cockpit report --mode deep
```

## 🛡️ Registry Resilience & Failover Logic (v1.4)
If you encounter a **401 Unauthorized** error during `uvx` (common in environments with private but expired registries), the Cockpit implements a **Logic-Based Failover**.

### ⚙️ How it works:
1.  **Detection**: The `orchestrator.py` captures `stderr` for 401/403 responses from private indices.
2.  **Synthesis**: It automatically reconstructs the `uvx` command with a `UV_INDEX_URL` override to `https://pypi.org/simple`.
3.  **Bypass**: This ensures CI/CD pipelines don't break when a private artifact registry (like Google Artifact Registry) has a token expiry during an audit run.

```bash
# Manual Override:
UV_INDEX_URL=https://pypi.org/simple uvx agentops-cockpit report
```

---
*Generated by the AgentOps Cockpit. Global Automation Division (v1.6.6 Stable).*
