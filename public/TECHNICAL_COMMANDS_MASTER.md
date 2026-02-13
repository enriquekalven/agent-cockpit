# 🕹️ Master Guide: AgentOps Cockpit Commands
## The "Watchtower Standard" Command Registry (v1.6.6 Stable)

This document is the definitive source of truth for all operational commands available in the **AgentOps Cockpit**. It consolidates the commands found across all specialized technical guides, organized by the **Agentic Trinity** pillars and the specific **SME Persona** they activate.

---

## 🏗️ Master Orchestration (The Cockpit)
These commands trigger cross-functional audits and generate the high-level board reports.

|| Method | Context | Command |
| :--- | :--- | :--- | :--- |
| 🛠️ | **Make (Local Dev)** | Inside repo | `make audit` |
| 🕹️ | **CLI (Global)** | Installed via Pip | `agent-ops report` |
| 📦 | **UVX (Portable)** | CI/CD / Ephemeral | `uvx agent-ops-cockpit report` |

### 🏗️ Master Orchestration (The Cockpit)
These commands trigger cross-functional audits and generate high-fidelity executive reports.

| Command (Make) | CLI Equivalent | Objective | Impact |
| :--- | :--- | :--- | :--- |
| `make audit` | `agent-ops report` | **Safe-Build** | Quick scan for secrets and reliability. |
| `make audit-deep` | `agent-ops report --mode deep` | **Final Exam** | Full benchmarks and stress tests. |
| `make audit-all` | `agentops-cockpit report --path <repo>` | **Global Audit** | Scan external repositories via Cockpit. |
| `make maturity` | `agent-ops audit-maturity` | **Expertise Matrix**| v1.6.6: High-fidelity expertise/persona dashboard. |
| `make diagnose` | `agentops-cockpit diagnose` | **Health Check** | Environment and dependency validation. |

---

## 🏛️ Architecture & Evolution (The Architect)
Commands focusing on systemic integrity, autonomous remediation, and long-term sovereignty.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `make arch-review` | **Autonomous Scan** | v1.4: Maturity Wisdom Store (Multi-Cloud Patterns) scan. |
| `make arch-review-export` | **Impact Waterfall** | Generates the premium v1.1 HTML Architecture Report. |
| `make apply-fixes` | **Autonomous Evolution** | (v1.4) Triggers AST-based code patches for detected gaps. |
| `agent-ops evolve` | **PR Closer (10X)** | Surgically fixes gaps and creates a hardened Git branch. |
| `agent-ops shadow` | **Reasoning Differential** | (10X) Compare V1 vs V2 for reasoning drift and cost delta. |
| `make propose-fixes`| **PR Factory** | Creates a feature branch and commits autonomous remediations. |
| `make arch-benchmark`| **Reliability Test** | Runs 50+ iterations to find the mean failure rate of agentic logic. |
| `make migrate` | **Sovereign Migration**| (10X) Move agents to Google Cloud, AWS, or Azure with auto-hydration. |
| `make register`| **Gemini Onboarding** | Auto-register the fleet to Gemini Enterprise (Vertex AI Extensions). |

---

## 🧗 AI Quality & Evaluation (The Quality SME)
Commands for optimizing the science of reasoning and mathematical quality baselines.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `make quality-baseline` | **Hill Climbing** | Iteratively optimizes prompts to reach the global quality peak. |
| `ops rag-truth` | **RAG Fidelity Audit**| v1.4: Citation accuracy and grounding logic validator. |
| `make simulation-run` | **Reasoning Stability**| Runs 100+ Digital Twin agents to detect reasoning degradation. |

---

## 🚩 Security & Adversarial SRE (The Red Team)
Commands for zero-trust hygiene and adversarial pressure testing.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `make scan-secrets` | **Zero-Trust Hygiene** | AST-based scan for hardcoded keys, tokens, and project IDs. |
| `make red-team` | **Adversarial Audit** | v1.4: Brand Safety Playbook checks (Payload Splitting, Tone). |

---

## 💰 FinOps & Token Economics (The Economist)
Commands for margin engineering and predictive OpEx simulation.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `make optimizer-audit` | **Waste Detection** | Identifies "Over-Modeling" and missing context caching layers. |
| `agent-ops report --roi` | **ROI Waterfall** | v1.4: Monthly cost-per-task TCO modeling. |

---

## 🌐 Infrastructure & Networking (The Cloud SRE)
Commands for latency reduction and 5th Golden Signal (TTFT) monitoring.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `make load-test` | **System Saturation** | Empirically measures RPS, P99 latency, and TTFT under load. |

---

## 🎭 UX/UI & A2UI Protocol (The Principal Designer)
Commands for generative interface audits and persona-driven journeys.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `make ui-audit` | **GenUI Face Scan** | Validates `surfaceId` mapping and A2UI visual handshake triggers. |
| `make smoke-test` | **Interactive Journey**| Simulates full-persona E2E journeys on the Face pillar. |

---

## 🧪 Testing & Reliability
Standard software engineering rigor integrated into the agentic stack.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `make reliability` | **Unit Regression** | Executes the core unit test suite and logic verification. |
| `make regression` | **Master Regression** | Full-spectrum testing: Reliability + Smoke Tests + PII guards. |

---

## 🚀 Production & Deployment
The path from cold code to cloud-scale intelligence.

| Command | Objective | Impact |
| :--- | :--- | :--- |
| `make dev` | **Local Stack** | Starts the local Engine (FastAPI) + Face (Vite/TS) development environment. |
| `make build` | **Production Bundle**| Compiles optimized assets for Cloud Run and Firebase Hosting. |
| `make deploy-prod` | **Readiness Audit**| (v1.6.6) Full ecosystem-wide production-readiness benchmarking gate. |
| `make mcp-serve` | **Ecosystem Hub** | Starts the Model Context Protocol server for tool discovery. |
| `make tdd` | **Design Documenter** | (Task 2) Output the Technical Design Document (TDD) with fixes as for PDF/HTML. |

---
*Generated by the AgentOps Cockpit Orchestrator. Global Governance Division (v1.6.6 Stable).*
