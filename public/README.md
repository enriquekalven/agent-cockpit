# The Optimized Agent Stack for Google Cloud (A2UI)

### Infrastructure gives you the pipes. We give you the Intelligence.

The **Optimized Agent Stack** is the professional distribution for application developers building on Gemini. While the [official Google Cloud Agent Starter Pack](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/agent-starter-pack) focus on infrastructure (VPCs, IAM, Terraform), we focus on the **Application Layer**: State synchronization, Cost Control, Security Audits, and Premium UX.

---

## 🏗️ The Agentic Trinity

A production-grade agent requires three synchronized pillars. We've built the ultimate 1-click ecosystem to handle them all.

### 1. ⚙️ The Engine (Day 0)
**Role: The Brain.** Focuses on internal reasoning, tool execution, and state management.
*   **Powered by**: Python ADK, Reasoning Engine (Vertex AI).
*   **Feature**: Native Google Cloud Trace & Logging integration.

### 2. 🎭 The Face (Day 1)
**Role: The Experience.** Focuses on how the agent manifests to the user. Moving away from chat-bubbles to adaptive surfaces.
*   **Powered by**: React, A2UI Standard, GenUI.
*   **Feature**: Dynamic A2UI Renderer and Adaptive Component Library.

### 3. 🕹️ The Cockpit (Day 2)
**Role: The Governance.** Found in **AgentOps Starter Pack**. Focuses on safety, scale, and profitability.
*   **Powered by**: Shadow Router, Hive Mind Cache, Red Team Evaluation.
*   **Viral Hook**: "The only starter pack that hacks itself so your users can't."

---

## 🚀 The Blue Ocean Opportunity

We win by solving the features that application developers care about, not just sysadmins.

| Feature | Standard "Starter Pack" | **The Optimized Agent Stack** |
| :--- | :--- | :--- |
| **Frontend Layer** | Generic / None | **A2UI + State Sync Native** |
| **Cost Control** | "Dumb Pipes" | **Semantic Cache (40% Savings)** |
| **Assurance** | Staging Apps | **Shadow Mode Deployment** |
| **Connectivity** | REST Callbacks | **MCP Tool Hub Native** |
| **Optimization** | Manual Audit | **Interactive Agent Linter** |

---

## 🔥 Key "Cockpit" Features

### 🕵️ Shadow Mode Deployment
**The Confidence Builder.** Traffic is sent to your production agent (v1), while asynchronously sending the same request to an experimental version (v2) in the background. Compare responses side-by-side in the Ops Dashboard before promoting.

### 🧠 The "Hive Mind" Semantic Cache
**Cut costs by 40%.** Drop-in middleware that checks a Vector Store (Memorystore/AlloyDB AI) before calling the LLM. If a similar question was asked recently, it returns the cached answer in 0.1s.

### 🚩 "Red Team" CI/CD Audit
**The Self-Hacking Starter Pack.** A pre-deployment security check that unleashes an aggressive LLM to try and jailbreak your agent or extract PII. If it succeeds, the deployment fails.

### 📟 "The Black Box" Flight Recorder
**Debug like a Video Game.** A visual replay tool in the `/ops` dashboard that records the entire chain of thought, tool inputs/outputs, and state changes. Scrub through executions to find exactly where logic failed.

### 🛠️ MCP Tool Hub (Optimization)
**Unified Tool Connectivity.** Standardize your agent's connection to external data using the **Model Context Protocol (MCP)**. Our built-in auditor detects legacy, high-latency Tool APIs and recommends 1-click migrations to MCP tools.

---

## 🛠️ Usage

### Scaffolding
Use the CLI directly without installation:
```bash
uvx agent-starter-pack create <project-name>
```

### Operations (The Cockpit)
Built-in `Makefile` commands for Day 2 management:
```bash
make audit      # Run the Interactive Agent Optimizer
make red-team   # Unleash security self-hacking
make dev        # Start local dev stack (Vite + FastAPI)
make deploy-prod # 1-click deploy to Cloud Run + Firebase
```

---

## 🔍 The Optimizer (Interactive Agent Ops)

The `optimizer.py` CLI audits your agent code and proposes optimizations that you can interactively approve or reject.

**What it checks:**
1.  **Context Caching**: Identifies large static prompts and suggests Gemini Context Caching.
2.  **Prompt Compression**: Finds redundant tokens in your A2UI blueprints.
3.  **Model Routing**: Audits routing logic to ensure Gemini 2.0 Flash is used for simple tasks.
4.  **MCP Migration**: Suggests moving legacy Tool APIs to the MCP Hub.

---

## 🏗️ Architecture & Standards

- **A2UI**: The core protocol for adaptive, JSON-driven interfaces.
- **AG-UI**: State management and human-in-the-loop interaction layers.
- **Optimized Agent Stack**: The production platform for scale and cost.

---

## License

MIT
