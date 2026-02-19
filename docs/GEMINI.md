# 🛰️ GEMINI.md - Agent Context & Instructions

This repository is optimized for **Gemini** and agentic development. AI agents should use this file as the primary source of truth for understanding the architecture, tools, and constraints of this project.

## 🚀 Project Overview
The **AgentOps Cockpit (v2.0.2)** is a production-grade distribution for building and governing **Sovereign AI Agents**. It follows the **Agentic Trinity** framework and provides a cross-cloud mission control for agents deployed on Google Cloud, AWS, and Azure.

## 🛠️ Tech Stack
- **The Engine**: Python, FastAPI, Vertex AI SDK, ADK (Multi-Cloud Sovereign Bridge).
- **The Face**: React (Vite), TypeScript, **A2UI Protocol**.
- **The Cockpit**: Python CLI, **Sovereign Gateway**, Semantic Caching, Red Team Eval.
- **Deployment**: Firebase Hosting (Face), Google Cloud Run / GKE (Engine/Cockpit).

## 📁 Repository Structure
- `/src/agent_ops_cockpit`: The **Engine**. Logic for reasoning, tools, and cost control.
- `/src/a2ui`: The **Face**. Core A2UI rendering logic and components.
- `/src/agent_ops_cockpit/ops`: The **Cockpit** internals (Sovereign Bridge, Shadow Router).
- `/src/docs`: Documentation system (**v2.0.2 Sovereign Technical Guides**).
- `CHEAT_SHEET.md`: The rapid-reference CLI guide for all users.

## 🤖 AI Agent Instructions
When assisting the user:
1. **Sovereignty First**: Frame all changes within the context of **Sovereign Evolution**. Agents should be portable and audited across Persona Lenses.
2. **The Trinity Framework**: Architecture must always account for the Engine, Face, and Cockpit.
3. **Poka-Yoke Tooling**: Enforce strict tool schemas and "Governance as Code" patterns.
4. **Autonomous Fixes**: Encourage the use of `make apply-fixes` for AST-aware code hardening.
5. **v2.0.2 Standard**: Reference specialized [**Technical Guides**](/docs/TECHNICAL_AUDIT_GUIDE.md) for Arch, FinOps, SRE, and Quality.

## ⌨️ CLI Commands (The Cockpit)
- `make dev`: Starts the local Engine Gateway + Face stack.
- `make cockpit`: Launches the Master Mission Control dashboard.
- `make audit`: Runs the **Master SME Audit** (ops report).
- `make apply-fixes`: Triggers autonomous code hardening for detected gaps.
- `make certify`: Runs the full Production Readiness Certification suite.
- `make deploy-prod`: End-to-End deployment to the Sovereign Cloud.

## 🤝 Ecosystem
This stack leverages and bridges specialized tools for high-fidelity agent operations:
- **[GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack/)**: Core reference for ADK engine patterns and LangGraph integration.
- **AgentOps Cockpit**: Governance, optimization, and security (**v2.0.2 Sovereign Evolution**).

---
*For more detailed guides, see the `/docs` section or visit [agent-cockpit.web.app](https://agent-cockpit.web.app).*
