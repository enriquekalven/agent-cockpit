# 🕹️ AgentOps Cockpit

<div align="center">
  <img src="https://img.shields.io/github/stars/enriquekalven/agent-cockpit?style=for-the-badge&color=ffd700" alt="GitHub Stars" />
  <img src="https://img.shields.io/github/license/enriquekalven/agent-cockpit?style=for-the-badge&color=007bff" alt="License" />
  <img src="https://img.shields.io/badge/Google-Well--Architected-4285F4?style=for-the-badge&logo=google-cloud" alt="Google Well-Architected" />
  <img src="https://img.shields.io/badge/Status-Day%202%20Operations-10b981?style=for-the-badge" alt="Status" />
</div>

<br />

<div align="center">
  <h3>"Infrastructure gives you the pipes. We give you the Intelligence."</h3>
  <p>The developer distribution for building, optimizing, and securing AI agents on Google Cloud.</p>
</div>

---

## 📽️ The Mission
Most AI agent templates stop at a single Python file and an API key. **The AgentOps Cockpit** is for developers moving into production. Based on the **[Google Well-Architected Framework for Agents](/docs/google-architecture)**, this stack provides the governance, safety, and cost guardrails required for "Day 2" success.

---

## 🏗️ The Agentic Trinity
We divide the complexity of production agents into three focused pillars:

- **⚙️ The Engine**: The reasoning core. Built with **ADK** (Agent Development Kit), FastAPI, and Vertex AI.
- **🎭 The Face**: The user experience. Adaptive UI surfaces and **GenUI** standards via the A2UI spec.
- **🕹️ The Cockpit**: The operational brain. Cost control, semantic caching, shadow routing, and adversarial audits.

---

## 🚀 Key Innovation: The "Intelligence" Layer

### 🛡️ Red Team Auditor (Self-Hacking)
Don't wait for your users to find prompt injections. Use the built-in Adversarial Evaluator to launch self-attacks against your agent, testing for PII leaks, instruction overrides, and safety filter bypasses.

### 🧠 Hive Mind (Semantic Caching)
**Reduce LLM costs by up to 40%.** The Hive Mind checks for semantically similar queries in 10ms, serving cached answers for common questions without calling the LLM.

### 🏛️ Arch Review & Cockpit Score
Every agent in the cockpit is graded against Google’s **Well-Architected Framework**. Use `make arch-review` to get your **Cockpit Score**—a measure of your agent's enterprise-readiness.

---

## ⌨️ Quick Start

You don't even need to clone the repo to start auditing.

```bash
# 1. Audit your existing agent design
uvx agent-ops-cockpit arch-review

# 2. Stress test your endpoint
uvx agent-ops-cockpit load-test --requests 100 --concurrency 10

# 3. Scaffold a new Well-Architected app
uvx agent-ops-cockpit create my-agent --ui a2ui
```

---

## 📊 Local Development
The Cockpit provides a unified "Mission Control" to evaluate your agents instantly.

```bash
make audit-all         # 🕹️ Run ALL audits and generate a Final Report
make reliability       # 🛡️ Run unit tests and regression suite
make dev               # Start the local Engine + Face stack
make arch-review   # 🏛️ Run the Google Well-Architected design review
make quality-baseline # 🧗 Run iterative 'Hill Climbing' quality audit
make audit         # 🔍 Run the Interactive Agent Optimizer
make red-team      # Execute a white-hat security audit
make deploy-prod   # 🚀 1-click deploy to Google Cloud
```

---

## 🧭 Roadmap
- [ ] **One-Click GitHub Action**: Automated audits on every PR.
- [ ] **Multi-Agent Orchestrator**: Support for Swarm/Coordinator patterns.
- [ ] **Visual Mission Control**: Real-time observability dashboard.

[View full roadmap →](/ROADMAP.md)

---

## 🤝 Community
- **Star this repo** to help us build the future of AgentOps.
- **Join the Discussion** for patterns on Google Cloud.
- **Contribute**: Read our [Contributing Guide](/CONTRIBUTING.md).

---
*Reference: [Google Cloud Architecture Center - Agentic AI Overview](https://docs.cloud.google.com/architecture/agentic-ai-overview)*
