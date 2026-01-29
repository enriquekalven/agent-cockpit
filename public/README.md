# 🕹️ AgentOps Cockpit

<div align="center">
  <img src="https://raw.githubusercontent.com/enriquekalven/agent-cockpit/main/public/og-image.png" alt="AgentOps Cockpit Social Preview" width="100%" />
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

### Key Pillars:
- **Governance-as-Code**: Audit your agent against [Google Well-Architected](/docs/google-architecture) best practices.
- **Agentic Trinity**: Dedicated layers for the Engine (Logic), Face (UX), and Cockpit (Ops).
- **A2A Connectivity**: Implements the [Agent-to-Agent Transmission Standard](/A2A_GUIDE.md) for secure swarm orchestration.

---

## 🏗️ The Agentic Trinity
We divide the complexity of production agents into three focused pillars:

- **⚙️ The Engine**: The reasoning core. Built with **ADK**, FastAPI, and Vertex AI.
- **🎭 The Face**: The user experience. Adaptive UI surfaces and **GenUI** standards via the A2UI spec.
- **🕹️ The Cockpit**: The operational brain. Cost control, semantic caching, shadow routing, and adversarial audits.

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
</div>

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
Stop building one-off tool integrations. The Cockpit provides a unified hub for **MCP Servers**. Connect to Google Search, Slack, or your internal databases via the standardized Model Context Protocol for secure, audited tool execution.

### 🧗 Quality Hill Climbing (ADK Evaluation)
Following **Google ADK Evaluation** best practices, the Cockpit provides an iterative optimization loop. `make quality-baseline` runs your agent against a "Golden Dataset" using **LLM-as-a-Judge** scoring (Response Match & Tool Trajectory), climbing the quality curve until production-grade fidelity is reached.

### 🛑 Mandatory Governance Enforcement (NEW)
The Cockpit now acts as a mandatory gate for production.
- **Blocking CI/CD**: GitHub Actions now fail if **High Impact** cost issues or **Red Team** security vulnerabilities are detected.
- **Build-Time Audit**: The `Dockerfile` includes a mandatory `RUN` audit step. If your agent is not "Well-Architected," the container image will fail to build.

---

## ⌨️ Quick Start

The Cockpit is available as a first-class CLI on PyPI. 

```bash
# 1. Install the Cockpit globally
pip install agentops-cockpit

# 2. Run Global Audit (Produces unified report)
agent-ops report --mode quick        # ⚡ Quick Safe-Build
agent-ops report --mode deep         # 🚀 Full System Audit

# 3. Audit a specific agent file for waste
agent-ops audit agent.py --quick     # 🔍 Fast code optimization

# 4. Stress test your endpoint
agent-ops load-test --requests 100 --concurrency 10
```

You can also use `uvx` for one-off commands without installation:
```bash
# Unified Master Audit (Master Orchestrator)
uvx agentops-cockpit report --mode quick
uvx agentops-cockpit report --mode deep

# Individual Code Optimizer
uvx agentops-cockpit audit agent.py --quick
uvx agentops-cockpit audit agent.py
```

---

### 🔍 Agent Optimizer v2 (Situational Intelligence)
The Cockpit doesn't just look for generic waste. It now performs **Triple-State Analysis**:
- **Legacy Workarounds**: Suggests situational fixes for older SDK versions (e.g., manual prompt pruning).
- **Modernization Paths**: Highlights native performance gains (e.g., 90% cost reduction via Context Caching) available in latest SDKs.
- **Conflict Guard**: Real-time cross-package validation to prevent architectural deadlocks (e.g., CrewAI vs LangGraph state loops).

### ⚡ Quick-Safe Build (12x Faster Loops)
Development velocity shouldn't sacrifice safety. The new `--quick` mode in the auditor reduces check latency from **1.8s to 0.15s**, providing sub-second feedback while maintaining the integrity of the Conflict Guard and Architecture Review.

---

## 📊 Local Development
The Cockpit provides a unified "Mission Control" to evaluate your agents instantly.

```bash
make audit         # 🕹️ Run Master Audit (Quick Safe-Build Mode)
make audit-deep    # 🚀 Run Deep Audit (Full SDK Evidence & Benchmarks)
make optimizer-audit # 🔍 Run Optimizer on specific agent files
make reliability   # 🛡️ Run unit tests and regression suite
make dev           # Start the local Engine + Face stack
make arch-review   # 🏛️ Run the Google Well-Architected design review
make quality-baseline # 🧗 Run iterative 'Hill Climbing' quality audit
make red-team      # Execute a white-hat security audit
make deploy-prod   # 🚀 1-click deploy to Google Cloud
```

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
