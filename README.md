# 🕹️ AgentOps Cockpit

<div align="center">
  <img src="public/assets/trinity.png" alt="AgentOps Cockpit Trinity" width="100%" />
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
 <h3>"Infrastructure is the plumbing. The Cockpit is the Intelligence."</h3>
 <p>The definitive production distribution for building, securing, and governing AI agents on Google Cloud.</p>
</div>

---

## 📽️ The Mission
Most AI agent templates stop at a single Python file and an API key. **The AgentOps Cockpit** is for developers moving into production. It provides framework-agnostic governance, safety, and cost guardrails for the entire agentic ecosystem.

- **Governance-as-Code**: Audit your agent against [Google Well-Architected](/docs/google-architecture) best practices with the **Evidence Bridge**—real-time citations for architectural integrity.
- **SME Persona Audits**: Parallelized review of your codebase by automated "Principal SMEs" across FinOps, SecOps, and Architecture.
- **Agentic Trinity**: Dedicated layers for the Engine (Logic), Face (UX), and Cockpit (Ops).
- **A2A Connectivity**: Implements the [Agent-to-Agent Transmission Standard](/A2A_GUIDE.md) for secure swarm orchestration.
- **MCP Native**: Registration as a [Model Context Protocol](https://modelcontextprotocol.io) server for 1P/2P/3P tool consumption.

---

## 🏗️ The Agentic Trinity
We divide the complexity of production agents into three focused pillars:

```mermaid
graph LR
   subgraph Trinity [The Agentic Trinity]
       E(The Engine: Reasoning)
       F(The Face: Interface)
       C(The Cockpit: Operations)
   end
   E <--> C
   F <--> C
   E <--> F
   style Trinity fill:#f9f9f9,stroke:#333,stroke-width:2px
```

- **⚙️ The Engine**: The reasoning core. Built with **ADK**, FastAPI, and Vertex AI.
- **🎭 The Face**: The user experience. Adaptive UI surfaces and **GenUI** standards via the A2UI spec.
- **🕹️ The Cockpit**: The operational brain. Cost control, semantic caching, shadow routing, and adversarial audits.

<div align="center">
 <img src="public/assets/ecosystem.png" alt="Ecosystem Integrations" width="100%" />
</div>

---

## 🌐 Framework Agnostic Governance
The Cockpit isn't just for ADK. It provides **Best Practices as Code** across all major agentic frameworks:

<div align="center">
 <img src="https://img.shields.io/badge/OpenAI_Agentkit-412991?style=for-the-badge&logo=openai" alt="OpenAI Agentkit" />
 <img src="https://img.shields.io/badge/Anthropic_Claude-D97757?style=for-the-badge&logo=anthropic" alt="Anthropic" />
 <img src="https://img.shields.io/badge/Microsoft_AutoGen-0078d4?style=for-the-badge&logo=microsoft" alt="Microsoft" />
 <img src="https://img.shields.io/badge/AWS_Bedrock-FF9900?style=for-the-badge&logo=amazon-aws" alt="AWS" />
 <img src="https://img.shields.io/badge/CopilotKit.ai-6366f1?style=for-the-badge" alt="CopilotKit" />
 <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge" alt="LangChain" />
 <img src="https://img.shields.io/badge/ADK-4285F4?style=for-the-badge&logo=google-cloud" alt="ADK" />
 <img src="public/assets/workflow.png" alt="Operational Workflow" width="100%" />
</div>

## 🛠️ Operational Flow

```mermaid
sequenceDiagram
   participant U as User
   participant C as Cockpit
   participant E as Engine
   participant F as Face
   
   U->>C: Prompt / Input
   C->>C: Policy Audit (Enterprise)
   C->>E: Execute Logic / Tools
   E->>C: Action Proposals
   C->>E: Approve (HITL)
   E->>F: GenUI Metadata
   F->>U: Reactive Surface (A2UI)
```

<br />

<div align="center">
 <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
 <img src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white" alt="Go" />
 <img src="https://img.shields.io/badge/NodeJS-339933?style=flat-square&logo=node.js&logoColor=white" alt="NodeJS" />
 <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
 <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit" />
 <img src="https://img.shields.io/badge/Angular-DD0031?style=flat-square&logo=angular&logoColor=white" alt="Angular" />
 <img src="https://img.shields.io/badge/Lit-324FFF?style=flat-square&logo=lit&logoColor=white" alt="Lit" />
</div>

Whether you are building a swarm in **CrewAI**, a Go-based high-perf engine, or a **Streamlit** dashboard, the Cockpit ensures your agent maps to the **Google Well-Architected Framework**.


---

## 🚀 Key Innovation: The "Intelligence" Layer

### 🛡️ Red Team Auditor (Self-Hacking)
Don't wait for your users to find prompt injections. Use the built-in Adversarial Evaluator to launch self-attacks against your agent, testing for PII leaks, instruction overrides, and safety filter bypasses.

### 🧠 Hive Mind (Semantic Caching)
**Reduce LLM costs by up to 40%.** The Hive Mind checks for semantically similar queries in 10ms, serving cached answers for common questions without calling the LLM.

### 🏛️ Arch Review & Framework Detection
Every agent in the cockpit is graded against a framework-aware checklist. The Cockpit intelligently detects your stack—**Google ADK**, **OpenAI Agentkit**, **Anthropic Claude**, **Microsoft AutoGen/Semantic Kernel**, **AWS Bedrock Agents**, or **CopilotKit**—and runs a tailored audit against corresponding production standards. Use `make arch-review` to verify your **Governance-as-Code**.

### 🕹️ MCP Connectivity Hub (Model Context Protocol)
Stop building one-off tool integrations. The Cockpit provides a unified hub for **MCP Servers**. Connect to Google Search, Slack, or your internal databases via the standardized Model Context Protocol for secure, audited tool execution. Start the server with `make mcp-serve`.

### 🗄️ Situational Database Audits
The Cockpit now performs platform-specific performance and security audits for:
- **AlloyDB**: Optimizes for the **Columnar Engine** (100x query speedup).
- **Pinecone**: Suggests **gRPC** and **Namespace Isolation** for high-perf RAG.
- **BigQuery**: Suggests **BQ Vector Search** for serverless, cost-effective grounding.
- **Cloud SQL**: Enforces **IAM-based authentication** via the official Python Connector.

### 🧗 Quality Hill Climbing (ADK Evaluation)
Following **Google ADK Evaluation** best practices, the Cockpit provides an iterative optimization loop. `make quality-baseline` runs your agent against a "Golden Dataset" using **LLM-as-a-Judge** scoring (Response Match & Tool Trajectory), climbing the quality curve until production-grade fidelity is reached.

### 🛸 v1.3.0: The Governance Intelligence Update
The Cockpit has evolved from a local auditor into a **Global Intelligence Engine**.
*   **🚩 Dynamic Pen-Testing**: Shift from static analysis to **Live Adversarial Probing**. The Red Team now simulates sequential conversational attacks with real-time **Resilience Scoring**.
*   **🧠 Cross-Agent Pattern Awareness**: The Orchestrator now correlates intelligence across your entire agent fleet, identifying recurring security debt and architectural anti-patterns.
*   **💰 Enterprise ROI Predictor**: A built-in FinOps engine that moves beyond "cost tracking" to **proactive savings forecasting** (e.g., "$1,250/mo potential savings via Caching").
*   **⚡ Hyper-Speed "Zero-Token" Audits**: Using recursive content hashing, the Cockpit intelligently skips unchanged agents, dropping fleet scan times to **sub-second** targets.
*   **⚖️ Governance-as-Code (SARIF)**: Natively integrate with enterprise security pipelines (GitHub Advanced Security, SonarQube) via the SARIF standard.
*   **🛠️ Strategy-First fix-fleet**: Orchestrate organizational-scale autonomous patching across hundreds of agents in a single, governed transaction.

---

## ⌨️ Command Reference: The Operations Manual

The AgentOps Cockpit provides multiple interfaces for governance. Use **`make`** for local development, **`agent-ops`** for global Python installs, or **`uvx`** for ad-hoc orchestration without installation.

### 🏛️ Governance & Compliance (The Audit Suite)
Ensure your agent maps to the [Google Well-Architected Framework](/docs/google-architecture).

| Scenario | Local (`make`) | Global (`agent-ops`) | Ad-hoc (`uvx`) |
| :--- | :--- | :--- | :--- |
| **Quick Safe-Build** | `make audit` | `agent-ops report --mode quick` | `uvx agentops-cockpit report --mode quick` |
| **Deep System Audit**| `make audit-deep` | `agent-ops report --mode deep` | `uvx agentops-cockpit report --mode deep` |
| **Arch Design Review**| `make arch-review` | `agent-ops arch-review` | `uvx agentops-cockpit arch-review` |

### 🚩 Security & Adversarial Hardening
Protect against prompt injection, PII leaks, and context escapes.

| Scenario | Local (`make`) | Global (`agent-ops`) | Ad-hoc (`uvx`) |
| :--- | :--- | :--- | :--- |
| **Dynamic Pen-Test** | — | `agent-ops pen-test agent.py` | `uvx agentops-cockpit pen-test agent.py` |
| **Red Team Audit**   | `make red-team` | `agent-ops red-team agent.py` | `uvx agentops-cockpit red-team agent.py` |
| **Secret Scanning**  | `make scan-secrets` | `agent-ops scan-secrets .` | `uvx agentops-cockpit scan-secrets .` |

### 🧗 Quality & Optimization (FinOps)
Climb the quality curve and reduce token waste/latency.

| Scenario | Local (`make`) | Global (`agent-ops`) | Ad-hoc (`uvx`) |
| :--- | :--- | :--- | :--- |
| **Quality Climbing** | `make quality-baseline`| `agent-ops quality climb` | `uvx agentops-cockpit quality climb` |
| **Code Optimizer**    | `make optimizer-audit` | `agent-ops audit . --quick`| `uvx agentops-cockpit audit . --quick` |
| **Load Testing**      | `make load-test` | `agent-ops load-test` | `uvx agentops-cockpit load-test` |

### 🏢 Fleet & Global Orchestration
Manage hundreds of agents across various repositories using the Hub pattern.

| Scenario | Local (`make`) | Global (`agent-ops`) | Ad-hoc (`uvx`) |
| :--- | :--- | :--- | :--- |
| **Workspace Audit**  | `make audit-all TARGET=./fleet`| `agent-ops report --workspace` | `uvx agentops-cockpit report --workspace` |
| **Bulk Remediation** | — | `agent-ops fix-fleet --issue PII` | `uvx agentops-cockpit fix-fleet --issue PII` |
| **Project Scaffold** | — | `agent-ops create my-agent` | `uvx agentops-cockpit create my-agent` |

### ⚓ Infrastructure & Ecosystem
Bridge the gap between local dev and global production.

- **MCP Tool Hub**: Connect to the Model Context Protocol ecosystem via `uvx agentops-cockpit mcp-serve`.
- **System Diagnosis**: Validate environment and SDK alignment using `make diagnose` or `agent-ops diagnose`.
- **Stakeholder Sync**: Email the latest Persona-Approved report using `make email-report`.
- **Production Push**: Execute 1-click CI/CD to Cloud Run + Firebase via `make deploy-prod`.

---

### 🧑‍💼 Principal SME Persona Approvals
Every audit is framed through a **Multi-Persona Governance Board**:
- **🏛️ Principal Platform Engineer** (Architecture & Design)
- **⚖️ Governance & Compliance SME** (Policy Enforcement)
- **🔐 SecOps Principal** (Security & Secret Scanning)
- **💰 FinOps Principal Architect** (Token & Cost Optimization)
- **🛡️ QA & Reliability Principal** (Test Coverage & Regression)
- **🎭 UX/UI Principal Designer** (Face/GenUI Compliance)

---

## 🧭 Roadmap
- [x] **One-Click GitHub Action**: Automated governance audits on every PR.
- [x] **Mandatory Build Gates**: Blocking CI/CD and Container audits for production safety.
- [x] **Multi-Agent Orchestrator**: Standardized A2A Swarm/Coordinator patterns.
- [ ] **Visual Mission Control**: Real-time cockpit observability dashboard.

[View full roadmap →](/ROADMAP.md)

---

## 🤝 Community
- **Star this repo** to help us build the future of AgentOps.
- **Join the Discussion** for patterns on Google Cloud.
- **Contribute**: Read our [Contributing Guide](/CONTRIBUTING.md).

---
*Reference: [Google Cloud Architecture Center - Agentic AI Overview](https://docs.cloud.google.com/architecture/agentic-ai-overview)*
