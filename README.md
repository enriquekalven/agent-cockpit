# 🕹️ AgentOps Cockpit: The AI Agent Operations Platform

### "Infrastructure gives you the pipes. We give you the Intelligence."

The **Optimized Agent Stack** is a production-grade distribution for building AI agents on Google Cloud. It is built strictly on the **[Google Well-Architected Framework for Agents](/docs/google-architecture)** and focuses on high-performance, cost-effective, and secure "Day 2" Agent Operations: Cost Control, Semantic Caching, Shadow Deployments, and Adversarial Audits.

---

## 🏗️ The Agentic Trinity
A production agent requires three synchronized pillars. This repository serves as the **Cockpit**.

1. **⚙️ The Engine (The Brain)**: Reasoning and tool execution (via Python ADK & Vertex AI).
2. **🎭 The Face (The Experience)**: Adaptive surfaces and GenUI (via A2UI Standard).
3. **🕹️ The Cockpit (The Governance)**: Safety, scale, and profitability (Shadow Router, Hive Mind, Red Team, PII Scrubber).

---

## 🚀 Key Features

### 🕵️ Shadow Mode Deployment
**The Confidence Builder.** Send traffic to your production agent (v1) while asynchronously testing an experimental version (v2) in the background. Compare responses side-by-side in the Ops Dashboard before promoting.

### 🧠 The "Hive Mind" Semantic Cache
**Cut LLM costs by up to 40%.** A drop-in middleware that checks a Vector Store (Memorystore/AlloyDB AI) for semantically similar queries. If a match is found, returns the answer in 0.1s without calling the LLM.

### 🛡️ PII Scrubber & Evidence Packet
**Industrial-Grade Privacy & Trust.**
- **PIIScrubber**: Automatic detection and masking of sensitive data (Emails, Credit Cards, SSNs) before it reaches the model.
- **Evidence Packet**: Standardized output format that includes grounded sources and reasoning snippets for full auditability.

### 📉 Cost, Memory & Load Optimizers
**Production Efficiency.**
- **CostOptimizer**: Real-time token tracking with "Pro vs Flash" savings recommendations.
- **MemoryOptimizer**: Leaky-bucket eviction policies to prevent long-context memory bloat.
- **LoadTester**: Concurrency-based stress testing to ensure sub-second UI responsiveness.

---

## 🛠️ Installation & Usage

### 📟 Installation
Install the Cockpit CLI to manage your agent stack:
```bash
pip install agent-ops-cockpit
```

### ⌨️ CLI Commands
The most important commands for your workflow:
```bash
make audit      # 🔍 Run the Interactive Agent Optimizer
make red-team   # 🚩 Run the Red Team security audit
make load-test  # ⚡ Run the Base Load Test
make dev        # 💻 Start local dev stack (FastAPI + Vite)
make deploy-prod # 🚀 1-click deploy to Cloud Run + Firebase
```

### 🧬 Scaffolding New Projects
```bash
agent-ops create <my-new-agent>
```

---

## 🚢 Agent-First CI/CD (The "Code Lime" Standard)
We implement a "Code Lime" (Clean, Lean, Integrated, Monitored, Evaluated) standard for all deployments. Our built-in GitHub Action handles the heavy lifting:

1. **Linting**: Automated code quality checks via Ruff.
2. **Optimization**: Runs `make audit` to block deployments with wasteful token usage.
3. **Evaluation**: Runs `make red-team` to ensure security hardening.
4. **Build**: Concurrent frontend (Vite) and backend (FastAPI) builds.

---

## 🤝 Gemini Code Assist
This repo is optimized for **Gemini Code Assist**. We provide a deep context layer in `.github/docs/GEMINI_CONTEXT.md` to ensure Gemini understands the Trinity Architecture and can provide high-fidelity optimization code.

---

## 🏗️ Architecture & Standards
- **A2UI**: The protocol for adaptive, JSON-driven interfaces.
- **MCP**: Model Context Protocol for unified tool connectivity.
- **GCP Native**: Built for Vertex AI, Cloud Run, and Firebase.

---

## 📄 License
MIT © Enrique Kalven
