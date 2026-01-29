# 🛸 AgentOps Cockpit: Documentation Hub

Welcome to the official documentation for the **Optimized Agent Stack**. This project is designed to bridge the gap between "experimental scripts" and "production-grade AI services" on Google Cloud.

To help you navigate, we have organized our guides by **Persona**. Choose the path that matches your current goal.

---

## 🧑‍💻 Choose Your Persona

### ⚙️ I am an Agent Developer (The Engine)
*Focus: Building reasoning logic, tool execution, and quality benchmarks.*
- **[Getting Started](../GETTING_STARTED.md)**: Your first 60 seconds with the stack.
- **[ADK Optimization](engine/optimization.md)**: Reducing token waste and latency.
- **[Reliability & Testing](engine/reliability.md)**: Unit tests and Regression Golden Sets.
- **[MCP Tool Hub](engine/mcp.md)**: Connecting 3rd party tools via Model Context Protocol.
- **[The Optimizer](engine/optimizer.md)**: Code-level audits for waste.
- **[Backend Integration](engine/backend_integration.md)**: Connecting to FastAPI and Cloud Run.

### 🎭 I am a UX/UI Architect (The Face)
*Focus: Building adaptive, intent-driven interfaces and GenUI components.*
- **[A2UI Protocol](face/a2a_protocol.md)**: The Agent-to-User Interface standard.
- **[Swarm Orchestration](face/a2a_protocol.md)**: Managing Agent-to-Agent (A2A) handoffs.
- **[Reactive Surfaces](face/a2a_protocol.md)**: Building dynamic UI components from agent metadata.

### 🕹️ I am an Operations or Security Lead (The Cockpit)
*Focus: Governance-as-Code, safety, fleet management, and production-readiness.*
- **[Cockpit Overview](cockpit/overview.md)**: Navigating the Mission Control dashboard.
- **[Enterprise Fleet Audits](cockpit/overview.md)**: High-velocity orchestration for hundreds of agents.
- **[Governance-as-Code](cockpit/governance.md)**: Standardized **SARIF** exports for GitHub/SonarQube integration.
- **[SME Verdicts](cockpit/governance.md)**: Educational rationales from Principal SME Personas.
- **[Security & Red Teaming](cockpit/security.md)**: Adversarial audits and PII scanning.
- **[Production Checklist](cockpit/production_checklist.md)**: The final gate before `make deploy-prod`.

---

## 📚 Technical Reference

| Category | Description |
| :--- | :--- |
| **[CLI Reference](reference/cli.md)** | Full list of `agent-ops` and `make` commands. |
| **[Deployment Guide](reference/deployment.md)** | Shipping to GCP (Cloud Run, Firebase). |
| **[Google Architecture](reference/google_architecture.md)** | The SME Personas and their audit benchmarks. |
| **[Limitations](reference/limitations.md)** | Known constraints and edge cases. |
| **[Project PRD](reference/prd.md)** | The strategic vision and technical requirements. |
| **[Gemini Context](reference/gemini_context.md)** | Instructions for AI Agents using this stack. |

---

## 🛠️ Global Commands

```bash
make audit         # 🕹️ Master Audit (Persona Approved)
make diagnose      # 🩺 Environment health check
make deploy-prod   # 🚀 1-click deploy to Google Cloud
```

*Don't know where to start? Read the **[Getting Started Guide](../GETTING_STARTED.md)**.*
