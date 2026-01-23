# Agent Ops Starter Pack (A2UI)

The world's first **Agent Ops Platform** for Google Cloud. Moving beyond "Hello World" to cost-optimized, security-hardened, and production-ready agent infrastructure.

## 🚀 Why This Starter Pack?

Most agent templates give you a chat window and leave you to figure out the rest. We focus on **Day 2 Operations**: Optimization, Cost Control, and Infrastructure. 

*   **Vercel for GCP Agents:** 1-click deployment to Cloud Run with automatic scaling to zero.
*   **The Optimizer:** Built-in CLI and CI/CD for prompt compression, context caching, and smart model routing. Supports interactive `approve/reject` workflows.
*   **Cost Guardrails:** Python middleware for budget management and turn-based token usage auditing.
*   **Production Stack:** Vertex AI (Gemini 2.0), Cloud Run, Firestore, and Google Cloud Trace out of the box.

---

## 🏗️ The Production Stack (The Google Cloud Agent Stack)

| Feature | Standard "Starter Pack" | **Agent UI Production Pack** |
| :--- | :--- | :--- |
| **Hosting** | Localhost / Vercel | **Cloud Run (Sidecar)** |
| **Model** | OpenAI Wrapper | **Vertex AI (Gemini 2.0)** |
| **Memory** | In-memory array | **Firestore / AlloyDB** |
| **Caching** | None | **Gemini Context Caching** |
| **Ops** | `print()` statements | **Google Cloud Trace** |

---

## 🔥 Viral & Production-First Features

Solve the "unsexy" problems that break agents in the real world. This isn't just a chat UI; it's a **Day 2 Operations Platform**.

### 1. 🕵️ Shadow Mode Deployment
**The Confidence Builder.** Traffic is sent to your production agent (v1), while asynchronously sending the same request to an experimental version (v2) in the background. Compare responses side-by-side in the Ops Dashboard before promoting.

### 2. 🧠 The "Hive Mind" Semantic Cache
**Cut costs by 40%.** Drop-in middleware that checks a Vector Store (Memorystore/AlloyDB AI) before calling the LLM. If a similar question was asked recently, it returns the cached answer in 0.1s.

### 3. 🚩 "Red Team" CI/CD Pipeline
**The Self-Hacking Starter Pack.** A pre-deployment GitHub Action that unleashes an aggressive LLM to try and jailbreak your agent or extract PII. If it succeeds, the deployment fails.

### 4. 📟 "The Black Box" Flight Recorder
**Debug like a Video Game.** A visual replay tool in the `/ops` dashboard that records the entire chain of thought, tool inputs/outputs, and state changes. Scrub through executions to find exactly where logic failed.

### 5. 📥 "Zero-Code" RAG Dropzone
**Drag, Drop, Deploy.** Any PDF, CSV, or Doc dropped into the `src/knowledge/` folder is automatically indexed into a Vertex AI Search data store upon deployment.

### 6. 🛠️ MCP Tool Hub (Optimization)
**Unified Tool Connectivity.** Standardize your agent's connection to external data using the **Model Context Protocol (MCP)**. Our built-in auditor detects legacy, high-latency Tool APIs and recommends 1-click migrations to MCP tools.

---

## Usage

You can use the CLI directly without installation using `uvx`.

```bash
# General Command Structure
uvx agentui-starter-pack create <project-name> [OPTIONS]
```

## Quick Start

Select the implementation standard that matches your tech stack:

### A2UI Standard (React + Vite)
The default template, optimized for performance and zero-dependency rendering.
```bash
uvx agentui-starter-pack create my-ui
```

### AG UI (High-Fidelity React)
Uses the **AG UI** standard (CopilotKit) for high-end React implementations with streaming pipes.
```bash
uvx agentui-starter-pack create my-ui --ui agui
```

### GenUI SDK (Flutter)
Scaffolds the project with the **GenUI SDK bridge**, ideal for cross-platform mobile and web apps.
```bash
uvx agentui-starter-pack create my-ui --ui flutter
```

### Web Components (Lit)
Standardized Web Components that can be embedded into any framework (Angular, Vue, etc).
```bash
uvx agentui-starter-pack create my-ui --ui lit
```

---

## 🔍 The Optimizer (Interactive Agent Ops)

Ensuring your agent is cost-efficient is critical for production. The `optimizer.py` CLI audits your agent code and proposes optimizations that you can interactively approve or reject.

```bash
# Run the audit
make audit
```

**What it checks:**
1.  **Context Caching**: Identifies large static prompts and suggests Gemini Context Caching.
2.  **Prompt Compression**: Finds redundant tokens in your A2UI blueprints.
3.  **Model Routing**: Audits routing logic to ensure Gemini 2.0 Flash is used for simple tasks.

**Workflow:**
The CLI will show a diff of the proposed change and ask:
`Do you want to apply this optimization? (approve/reject) [approve]:`

---

## Prerequisites

- **Node.js**: v18 or higher
- **Python**: v3.10 or higher (for the CLI)
- **Git**: Installed and configured

---

## Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `project_name` | Argument | — | The name of the new project directory |
| `--ui` | Option | `a2ui` | UI Template flavor (`a2ui`, `agui`, `flutter`, `lit`) |
| `--copilotkit` | Flag | `false` | Enable extra CopilotKit features for AG UI |

---

## ✨ Features

- **Zero-Dependency Renderer**: Recursive rendering engine that handles complex A2UI JSON trees without external SDKs.
- **Visual Analytics**: Built-in support for **StatBars**, **Images**, and **Dynamic Lists** for rich dashboard generation.
- **Interactive Playground**: A built-in sandbox with **Agent Mode** to simulate real-world AI-driven UI updates.
- **Premium Design System**: Dark-mode aesthetic with glassmorphism, smooth transitions, and professional typography (Inter).
- **Protocol Ready**: Native support for **A2UI** (Agent-to-User) and **A2A** (Agent-to-Agent) standards.

---

## 🏗️ The Agentic Ecosystem

Agent UI Starter Pack is more than just a renderer—it is the bridge between the logic-heavy world of Agent Frameworks and the visual world of Modern Frontend.

### The Agentic Stack
![Agentic Stack](/diagrams/agentic-stack.png)

A2UI sits as the critical middleware layer:
1.  **Agent Brain**: Frameworks like LangGraph, CrewAI, or Google ADK reason and plan.
2.  **A2UI Gateway**: The agent outputs a structured JSON Blueprint instead of raw text.
3.  **A2UI Renderer**: This starter pack interprets the blueprint and manifests a high-fidelity React interface in real-time.

### Value Proposition: From Text to Interface
![Value Proposition](/diagrams/value-proposition.png)

*   **Move Beyond Chat**: Don't trap your users in a chat bubble. Provide full application surfaces that adapt to the agent's current task.
*   **Standardized Schema**: Use the Google-originated A2UI standard to ensure your UI is portable across Web, Mobile (Flutter), and Desktop.
*   **Production Ready**: Built-in support for Multi-Agent orchestration, human-in-the-loop approvals, and complex data visualization.

---

## 🏗️ Architecture & Standards

- **A2UI**: The core protocol for adaptive, JSON-driven interfaces. [Official Repo](https://github.com/google/A2UI)
- **GenUI (Generative UI)**: Full support for generative patterns across Web and Flutter.
- **AG UI (Agentic UI)**: Integration-ready for [CopilotKit](https://github.com/CopilotKit/CopilotKit) and high-end React surfaces.
- **Lit Web Components**: Standards-based components for any framework.

### Standard Comparison

| Standard | Role | Core Value |
| :--- | :--- | :--- |
| **CopilotKit** | Framework | Full-stack integration for AI Copilots. |
| **A2UI** | Specification | Declarative JSON schema for portable UI components. |
| **AG-UI** | Protocol | State management and human-in-the-loop interaction layers. |
| **Agent UI** | Platform | **Production Agent Ops.** Cost-optimized, secure, and auto-scaling infrastructure on Google Cloud. |

---

## 🚀 Deployment

One-liner deployment commands are provided via the included `Makefile`.

| Platform | Command |
| :--- | :--- |
| **Cloud Run** | `make deploy-cloud-run` |
| **Firebase** | `make deploy-firebase` |
| **GKE** | `make deploy-gke` |

For advanced configuration, see the [Deployment Guide](./DEPLOYMENT.md).

---

## 📡 Protocol Standards

### A2A Protocol
The **Agent-to-Agent (A2A)** protocol enables agents to communicate over a network. See the [A2A_GUIDE.md](./A2A_GUIDE.md) for multi-agent orchestration.

### A2UI Schema
The renderer expects an `A2UISurface` object:

```json
{
  "surfaceId": "unique-id",
  "content": [
    {
      "type": "Text",
      "props": { "text": "Hello World", "variant": "h1" }
    },
    {
      "type": "Card",
      "props": { "title": "System Meta" },
      "children": []
    }
  ]
}
```

---

## License

MIT
