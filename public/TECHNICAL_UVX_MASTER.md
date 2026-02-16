# ⌨️ Master Guide: AgentOps UVX Commands
## Portable Governance & Automation (v1.8.4 Stable)

This document provides a consolidated reference for all **`uvx`** commands available in the AgentOps ecosystem. `uvx` allows you to run these tools instantly without a local installation, making them ideal for CI/CD pipelines, ephemeral environments, and auditing external repositories.

The primary package is **`agentops-cockpit`**, which exposes the **`agentops-cockpit`** (alias `agent-ops`) binaries.

### ⚙️ The Portability Engine
Unlike standard CLI tools, the AgentOps `uvx` distribution uses **Binary Shimming**. This allows the tool to execute in an isolated environment with its own dependencies (e.g., specific versions of `ast`, `tenacity`, and `google-cloud-aiplatform`) without polluting the host's global Python space.

---

## 🏗️ Master Orchestration
Run the full range of AgentOps intelligence against any project or file.

| Command | Objective | Mode/Flags |
| :--- | :--- | :--- |
| `uvx agentops-cockpit cockpit` | **Mission Control** | Main dashboard for fleet-wide visibility. |
| `uvx agentops-cockpit audit report` | **Full Master Audit** | `--mode quick` (default) or `deep` |
| `uvx agentops-cockpit sys version` | **Version Check** | Display current CLI and Engine version. |
| `uvx agentops-cockpit sys doctor`| **System Check** | Verify GCP Auth, API keys, and environment paths. |
| `uvx agentops-cockpit audit maturity`| **Maturity Matrix**| v1.8.4: Expert competency and persona status dashboard. |

---

## 🏛️ Architecture & Interop
Audit designs against the Google Well-Architected Framework and Multi-Cloud Maturity Store.

| Command | Objective | Flags |
| :--- | :--- | :--- |
| `uvx agentops-cockpit audit arch`| **Architecture Review**| v1.8.4: Semantic Paradigm Auditor. |
| `uvx agentops-cockpit ops mcp` | **MCP Hub** | Manage and scaffold MCP tool servers. |

---

## 🧗 AI Quality & Evaluation
Iterative science for the reasoning layer.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `uvx agentops-cockpit eval quality`| **Hill Climbing** | Iterative prompt optimization loop. |
| `uvx agentops-cockpit audit rag` | **RAG Fidelity** | v1.4: Citation and grounding logic audit. |
| `uvx agentops-cockpit test unit` | **Unit Regression** | Runs core reliability suite (pytest). |
| `uvx agentops-cockpit test smoke` | **Persona Journey** | Validates the "Face" pillar via interactive pipelines. |

---

## 🚩 Security & Policy
Adversarial audits and declarative guardrail enforcement.

| Command | Objective | Flags |
| :--- | :--- | :--- |
| `uvx agentops-cockpit eval red-team` | **Adversarial Audit** | v1.8.4: Brand Safety & Cross-Silo Risk. |
| `uvx agentops-cockpit audit policy` | **Guardrail Check** | Validate queries against the Policy Engine. |
| `uvx agentops-cockpit audit secrets` | **Credential Leak Scan** | High-fidelity secret scanning via AST. |

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
| `uvx agentops-cockpit audit --quick` | **Token Optimizer** | Dev-velocity audit for secrets and reliability. |
| `uvx agentops-cockpit fleet --roi` | **ROI Waterfall** | v1.4: Monthly cost modeling and efficiency pivots. |
| `uvx agentops-cockpit test load` | **Stress Benchmarking** | LLM latency and concurrency stress-testing. |

---

## 🎭 UX/UI & GenUI
Auditing the "Face" pillar for protocol compliance.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `uvx agentops-cockpit audit ui` | **Face Auditor** | Scans frontend code for A2UI / AGUI / MCP alignment. |

---

## 🚀 Scaffolding & Deployment
Initialize new projects and push to Google Cloud.

| Command | Objective | Flags |
| :--- | :--- | :--- |
| `uvx agentops-cockpit create trinity` | **Trinity Scaffolder** | Fast-path initialization of Engine + Face + Cockpit. |
| `uvx agentops-cockpit deploy sovereign` | **End-to-End Factory** | Audit -> Fix -> Hydrate -> Deploy in one command. |

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
*Generated by the AgentOps Cockpit. Global Automation Division (v1.8.4 Stable).*
