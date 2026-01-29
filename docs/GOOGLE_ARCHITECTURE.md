---

<div align="center">
  <img src="diagrams/ecosystem.png" alt="Google Ecosystem Integrations" width="100%" />
</div>

## 🏗️ The Three Pillars

### 1. The Engine (Logic)
*   **Role**: Reasoning, Tool Selection, MCP Connectivity.
*   **Standard**: [Google ADK](https://github.com/a2aproject/adk) & Vertex AI.
*   **Operations**: Governed by `agent-ops report`.

### 2. The Face (User Interface)
*   **Role**: GenUI Rendering, Surface Dispatching, A2UI Protocol.
*   **Standard**: [A2UI Spec](https://a2ui.org).
*   **Operations**: Verified by `agent-ops-ui-auditor`.

### 3. The Cockpit (Agent Operations)
*   **Role**: Caching, Privacy Scrubbing, FinOps, Observability.
*   **Standard**: Google Well-Architected Framework.
*   **Operations**: The centralized control plane for Day 2 production.

---

## 📡 The A2A (Agent-to-Agent) Handshake

In a multi-agent world, trust is earned through evidence. The Cockpit implements the **Reasoning Evidence Packet** standard. 

When Agent A calls Agent B, it doesn't just send text; it sends:
-   **Trace IDs**: Full lineage of the thought process.
-   **Assurance Scores**: Confidence intervals for the reasoning path.
-   **PII Health**: Confirmation that data was scrubbed via the standard VPC proxy.

---

## 🏛️ Google Well-Architected Alignment

By using the Cockpit, you are automatically building toward four critical pillars:

| Pillar | Cockpit Mechanism |
| :--- | :--- |
| **Operational Excellence** | [Automated Flight Recording](./cockpit) |
| **Security & Privacy** | [Adversarial Red Teaming](./security) |
| **Cost Optimization** | [Context & Semantic Caching](./optimization) |
| **Performance Efficiency** | [MCP Protocol Multiplexing](./cli-commands) |

---

## ⚡ The Architectural Verdict
<div align="center">
  <img src="diagrams/workflow.png" alt="Operational Workflow" width="100%" />
</div>

Run the Architecture Review now to see how your current repo stacks up:
```bash
agent-ops arch-review --path .
```
