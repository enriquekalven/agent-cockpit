# 🕹️ AgentOps Cockpit

<div align="center">
  <img src="public/assets/trinity_v2.png" alt="AgentOps Cockpit Trinity" width="100%" />
</div>

<div align="center">
  <br />
  <a href="https://agent-cockpit.web.app" target="_blank"><strong>🌐 Official Website & Live Demo</strong></a>
  <br /><br />
  <a href="https://deploy.cloud.google.com?repo=https://github.com/enriquekalven/agent-cockpit">
    <img src="https://deploy.cloud.google.com/button.svg" alt="Deploy to Google Cloud" />
  </a>
  <br />
  <br />
  <img src="https://img.shields.io/github/stars/enriquekalven/agent-cockpit?style=for-the-badge&color=ffd700" alt="GitHub Stars" />
  <img src="https://img.shields.io/github/license/enriquekalven/agent-cockpit?style=for-the-badge&color=007bff" alt="License" />
  <img src="https://img.shields.io/badge/Google-Well--Architected-4285F4?style=for-the-badge&logo=google-cloud" alt="Google Well-Architected" />
  <img src="https://img.shields.io/badge/A2A_Standard-Enabled-10b981?style=for-the-badge" alt="A2A Standard" />
</div>

<br />

<div align="center">
  <h3>"Infrastructure gives you the pipes. We give you the Intelligence."</h3>
  <p>The developer distribution for building, optimizing, and securing AI agents on Google Cloud.</p>
</div>

---

## 📽️ The Mission
Most AI agent templates stop at a single Python file and an API key. **The AgentOps Cockpit** is for developers moving into production. It provides framework-agnostic governance, safety, and cost guardrails for the entire agentic ecosystem.

- **Governance-as-Code**: Audit your agent against [Google Well-Architected](/docs/GOOGLE_ARCHITECTURE.md) best practices with the **Evidence Bridge**—real-time citations for architectural integrity.
- **SME Persona Audits**: Parallelized review of your codebase by automated [**Principal SMEs**](docs/TECHNICAL_AUDIT_GUIDE.md) across FinOps, SecOps, Architecture, and Quality.
- **Agentic Trinity**: Dedicated layers for the Engine (Logic), Face (UX), and Cockpit (Ops).
- **A2A Connectivity**: Implements the [**Agent-to-Agent Transmission Standard**](docs/TECHNICAL_A2A_GUIDE.md) for secure swarm orchestration.
- **MCP Native**: Registration as a [Model Context Protocol](https://modelcontextprotocol.io) server for 1P/2P/3P tool consumption.

## 🚀 Quick Start: One Command to Rule Them All

The AgentOps Cockpit is designed for high-velocity fleet management. If you are overwhelmed by the options, just remember **one command**:

```bash
# 🕹️ Mission Control: Master Audit, Persona Review, & Fleet Tracking
agentops-cockpit cockpit
```

This single command launches the **Distinguished Fellow Master Dashboard**, where the principal SMEs (Architecture, Security, FinOps) provide a summary of your workspace and guide you toward deeper persona mandates.

### 🏛️ The Sovereign Workflow
1. **Explore**: `agentops-cockpit cockpit` (Mission Control)
2. **Modernize**: `agentops-cockpit mcp blueprint` (Legacy -> MCP Bridge)
3. **Certify**: `agentops-cockpit certify` (Production Readiness Badge)
4. **Evolve**: `agentops-cockpit deploy sovereign` (The Master Move)

---

## 🏗️ The Agentic Trinity
We divide the complexity of production agents into three focused pillars:

```mermaid
graph TD
   subgraph Trinity [The Agentic Trinity 2.0]
       E(The Engine: Reasoning)
       F(The Face: Interface)
       C(The Cockpit: Operations)
       S{Sovereignty & Compliance}
   end
   E <--> C
   F <--> C
   E <--> F
   E -.-> S
   F -.-> S
   C -.-> S
   style Trinity fill:#f8fafc,stroke:#334155,stroke-width:2px
   style S fill:#0ea5e9,color:#fff,stroke:#0284c7
```

- **⚙️ The Engine**: The reasoning core. Built with **ADK**, FastAPI, and Vertex AI.
- **🎭 The Face**: The user experience. [Adaptive UI surfaces](docs/TECHNICAL_UX_GUIDE.md) and **GenUI** standards via the A2UI spec.
- **🕹️ The Cockpit**: The operational brain. [Cost control](docs/TECHNICAL_FINOPS_GUIDE.md), semantic caching, shadow routing, and [adversarial audits](docs/TECHNICAL_REDTEAM_GUIDE.md).

<div align="center">
 <img src="public/assets/ecosystem.png" alt="Ecosystem Integrations" width="100%" />
</div>

---

## 🏛️ v1.8.2: The "Structural Wisdom" Release (LATEST)
Evolving into a full Strategic Governance Platform for AI Agents. See the [**v1.8.2 Release Notes**](/CHANGELOG.md).
The ultimate end-to-end management platform for professional AI agents. v1.8 introduces the **Principal Semantic Architect**, shifting focus from tactical implementation to strategic architectural paradigm alignment.

- **🏛️ Strategic Paradigm Auditor (`audit arch`)**: Detect high-level architectural mismatches. Are you using RAG for math? Prompt-stuffed structured data analysis? Manual state machines instead of dedicated frameworks?
- **🛰️ Fleet Hub (`fleet`)**: Stateful registry and runtime oversight. Monitor health with `fleet status`, watch ecosystem sync with `fleet watch`, and iterate with `fleet tunnel`.
- **🛡️ Audit Hub (`audit`)**: Principal SME board. Run master reviews with `audit report`, security scans with `audit security`, and context/token visualization with `audit context`.
- **🚀 Deployment Hub (`deploy`)**: The multi-cloud factory. End-to-End pipelines via `deploy sovereign` and GCP/AWS/Azure migration via `deploy migrate`.
- **🔧 Evolution Hub (`fix`)**: Autonomous code synthesis. Apply targeted audit fixes with `fix issue`, trigger the `fix evolve` "PR Closer", or use the `fix workbench` for interactive remediation.
- **🏗️ Scaffolding Hub (`create`)**: Trinity Project initialization. Bootstrap unified projects via `create trinity` or UIs via `create face`.
- **🧠 Knowledge Hub (`rag`)**: RAG Truth-Sayer. Audits RAG pipelines for grounding, and introduces **`rag blueprint`** for generating optimized indexing strategies.
- **📡 Interop Hub (`mcp`)**: Tool Governance. Discover and integrate Model Context Protocol (MCP) tools via `mcp list/install`. Start the MCP bridge with `mcp-server launch`.

---

## 🚀 Key Innovation: The "Intelligence" Layer

### 🛡️ Red Team Auditor (Adversarial SRE)
Don't wait for your users to find prompt injections. Use the built-in [**Adversarial Evaluator**](docs/TECHNICAL_REDTEAM_GUIDE.md) to launch self-attacks against your agent, testing for PII leaks, instruction overrides, and multilingual jailbreaks.

### 🧠 Hive Mind (Semantic Caching)
**Reduce LLM costs by up to 40%.** The Hive Mind checks for semantically similar queries in 10ms, serving cached answers for common questions without calling the LLM.

### 🏛️ Arch Review & Autonomous Evolution
Every agent in the cockpit is graded against a framework-aware checklist. The Cockpit intelligently detects your stack and runs a tailored [**Architecture Review**](docs/TECHNICAL_ARCH_REVIEW.md). v1.3 introduces **Autonomous Evolution**—the ability to synthesize code fixes directly from audit findings.

### 🕹️ MCP Connectivity Hub (Model Context Protocol)
Stop building one-off tool integrations. The Cockpit provides a unified hub for **MCP Servers**. Connect to 1P/2P/3P tools via the standardized Model Context Protocol for secure, audited tool execution. Start the server with `make mcp-serve`.

### 🗄️ Situational Database Audits
The Cockpit now performs platform-specific performance and security audits for **AlloyDB**, **Pinecone**, **BigQuery**, and **Cloud SQL**.

---

### 🛡️ Advanced Governance & Discovery (v1.8.2)
Modern agents don't just live in `agent.py`. The Cockpit uses a centralized **Discovery Engine** to intelligently map your project:
- **`.gitignore` Compliance**: Zero-noise scanning that respects your project's ignore rules.
- **Multi-Target Logic**: Define `targets: []` in `cockpit.yaml` to audit distributed agents in a single pass.
- **Template Isolation**: Automatically ignores raw template placeholders (e.g., Jinja/Cookiecutter) to focus on the active implementation.
- **Artifact Store**: All data (SARIF, Evidence, HTML) is now sovereignly stored in the `.cockpit/` directory.

---

## ⌨️ Master Command Registry

The Cockpit is available as a first-class CLI and a comprehensive Makefile-based operational toolkit.

| Registry | Description |
| :--- | :--- |
| 🕹️ [**Makefile Commands**](docs/TECHNICAL_COMMANDS_MASTER.md) | Standard local development and orchestration shortcuts. |
| 🚀 [**UVX Master Guide**](docs/TECHNICAL_UVX_MASTER.md) | Portable, zero-install commands for CI/CD and automation. |

---

## 🧑‍💼 Principal SME Persona Approvals
The Cockpit now features a **Multi-Persona Governance Board**. Every audit result is framed through the lens of a Principal Engineer in that domain:
*   [**🏛️ Architecture**](docs/TECHNICAL_ARCH_REVIEW.md)
*   [**💰 FinOps**](docs/TECHNICAL_FINOPS_GUIDE.md)
*   [**🛡️ Red Team**](docs/TECHNICAL_REDTEAM_GUIDE.md)
*   [**🧗 Quality**](docs/TECHNICAL_QUALITY_GUIDE.md)
*   [**🌐 Infrastructure**](docs/TECHNICAL_INFRA_GUIDE.md)
*   [**🎭 UX/UI**](docs/TECHNICAL_UX_GUIDE.md)

<div align="center">
  <img src="public/assets/persona_builder.png" width="32%" />
  <img src="public/assets/persona_strategist.png" width="32%" />
  <img src="public/assets/persona_guardian.png" width="32%" />
</div>
<div align="center">
  <img src="public/assets/persona_controller.png" width="32%" />
  <img src="public/assets/persona_visionary.png" width="32%" />
  <img src="public/assets/workflow_v2.png" width="32%" />
</div>

---

## 🚀 Production Readiness Auditor
The Cockpit serves as the final gate before production deployment. `make deploy-prod` triggers a deep benchmark of the entire ecosystem:
1. **v1.8.2 Deep System Audit**: Benchmarks models (Gemini 2.0 Pro/Flash) and logic.
2. **Stress Testing**: Load testing endpoints to ensure concurrency safety.
3. **Red Team Verification**: Adversarial security scans for prompt injection and PII.
4. **Resiliency Check**: Verifies `@retry` logic and `timeout` guards are active.

---

---

## 🛡️ Privacy & Telemetry
The AgentOps Cockpit follows a **Privacy-First, Sovereign Standard**. 

By default, the CLI sends anonymous operational metrics (e.g., event names, OS type, success rates) to the **Global Pulse** hub to help us understand fleet health and prioritize improvements. **We do not collect names, emails, code snippets, secrets, or folder paths.**

### 🌑 How to Opt-Out
If you prefer 100% isolation, you can disable telemetry by setting the following environment variable in your shell:
```bash
export AGENTOPS_TELEMETRY_ENABLED=false
```
Alternatively, you can set it in your local `cockpit.yaml`:
```yaml
telemetry:
  enabled: false
```

---

## 🤝 Ecosystem & Attribution
The AgentOps Cockpit is designed to leverage and secure the best-of-breed tools in the Google Cloud ecosystem. We explicitly acknowledge and leverage the excellent work from:

*   **[GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack/)**: We leverage this as a core reference for the **Agent Development Kit (ADK)** patterns and Vertex AI Agent Engine integration.
*   **[A2UI Protocol](https://github.com/GoogleCloudPlatform/agent-starter-pack/tree/main/src/a2ui)**: Standardized Generative UI handshake for building adaptive, agentic user interfaces.
*   **[A2A Standard](https://github.com/GoogleCloudPlatform/agent-starter-pack/blob/main/docs/A2A_GUIDE.md)**: Agent-to-Agent Transmission Protocol for secure swarm intelligence and inter-agent communication.
*   **[Model Context Protocol (MCP)](https://modelcontextprotocol.io)**: Our unified tool execution standard, enabling portable and secure 1P/2P/3P integrations.
*   **[LangChain & LangGraph](https://python.langchain.com/)**: Foundational libraries for stateful, multi-agent reasoning loops and graph-based orchestration.
*   **[CrewAI](https://www.crewai.com/)**: Multi-agent framework used as a reference for collaborative task execution and role-playing agents.
*   **[Firebase](https://firebase.google.com/)**: Provider for enterprise-grade hosting and global distribution of the **Face** layer.
*   **[Google Cloud Run & GKE](https://cloud.google.com/run)**: High-scale orchestration platforms for the **Engine** and cluster-wide agent fleets.
*   **[Vertex AI SDK](https://cloud.google.com/vertex-ai/docs/python-sdk)**: The backbone for frontier reasoning (Gemini 3) and enterprise-grade model governance.
*   **[Tenacity](https://tenacity.readthedocs.io/)**: The gold-standard library for the exponential backoff and resiliency patterns we enforce.
*   **[Rich](https://rich.readthedocs.io/)**: Modern visualization engine that powers the high-fidelity Cockpit CLI experience.

---
*Reference: [Google Cloud Architecture Center - Agentic AI Overview](https://docs.cloud.google.com/architecture/agentic-ai-overview)*
