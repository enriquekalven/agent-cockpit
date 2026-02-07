# GEMINI.md - Agent Context & Instructions

This repository is optimized for **Gemini** and agentic development. AI agents should use this file as the primary source of truth for understanding the architecture, tools, and constraints of this project.

## 🚀 Project Overview
The **Optimized Agent Stack** is a production-grade distribution for building AI agents on Google Cloud. It follows the **Google Well-Architected Framework for Agents** and covers the **Agentic Trinity**: Engine (Backend), Face (Frontend), and Cockpit (Operations).

## 🛠️ Tech Stack
- **The Engine**: Python, FastAPI, Vertex AI SDK, ADK (LangChain, CrewAI, LangGraph support).
- **The Face**: React (Vite), TypeScript, A2UI Protocol.
- **The Cockpit**: Python CLI, Shadow Routing, Semantic Caching, Red Team Eval.
- **Deployment**: Firebase Hosting (Face), Google Cloud Run (Engine/Cockpit).

## 📁 Repository Structure
- `/src/agent_ops_cockpit`: The **Engine**. Logic for reasoning, tools, and cost control.
- `/src/a2ui`: The **Face**. Core A2UI rendering logic and components.
- `/src/agent_ops_cockpit/ops`: The **Cockpit** internals (MCP Hub, Shadow Router).
- `/src/docs`: Documentation system (v1.0.0 Technical Guides).

## 🤖 AI Agent Instructions
When assisting the user:
1. **Trinity First**: Frame all changes within the context of the Engine, Face, or Cockpit.
2. **Professional Distribution**: We differentiate from standard templates by providing **Intelligence** (Optimizer, Cache, Shadow Mode, Hill Climbing).
3. **Governance & Regression**: Reference `CAPABILITIES_REGISTRY.md` to ensure core features remain stable.
4. **Operations**: Encourage the use of `make audit-deep` and `make red-team` before deployment. Audits are now **blocking gates** in CI/CD and container builds (Score > 90).
5. **v1.0.0 Standard**: Reference specialized [**Technical Guides**](/docs/TECHNICAL_AUDIT_GUIDE.md) for Arch, FinOps, SRE, and Quality.

## ⌨️ CLI Commands (The Cockpit)
- `make dev`: Starts the local Engine + Face stack.
- `make audit`: Runs the Quick Safe-Build (Secrets, Reliability).
- `make audit-deep`: Runs the Master Cockpit Audit (Hill Climbing, Benchmarks).
- `make arch-review`: Runs the v1.0.0 Autonomous Architect review.
- `make apply-fixes`: Triggers AST-based code patching for detected gaps.
- `make deploy-prod`: Full stack deployment to GCP.

## 🤝 Ecosystem
This stack leverages and bridges specialized tools for high-fidelity agent operations:
- **[GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack/)**: Core reference for ADK engine patterns and LangGraph integration.
- **AgentOps Cockpit**: Governance, optimization, and security (Shadow Mode, Intelligence, v1.0.0 Stability).

---
*For more detailed guides, see the `/docs` section on the live site.*
