# GEMINI.md - Agent Context & Instructions

This repository is optimized for **Gemini** and agentic development. AI agents should use this file as the primary source of truth for understanding the architecture, tools, and constraints of this project.

## 🚀 Project Overview
The **Optimized Agent Stack** is a production-grade distribution for building AI agents on Google Cloud. It follows the **Google Well-Architected Framework for Agents** and covers the **Agentic Trinity**: Engine (Backend), Face (Frontend), and Cockpit (Operations).

## 🛠️ Tech Stack
- **The Engine**: Python, FastAPI, Vertex AI SDK, ADK.
- **The Face**: React (Vite), TypeScript, A2UI Protocol.
- **The Cockpit**: Python CLI, Shadow Routing, Semantic Caching, Red Team Eval.
- **Deployment**: Firebase Hosting (Face), Google Cloud Run (Engine/Cockpit).

## 📁 Repository Structure
- `/src/agent_ops_cockpit`: The **Engine**. Logic for reasoning, tools, and cost control.
- `/src/a2ui`: The **Face**. Core A2UI rendering logic and components.
- `/src/agent_ops_cockpit/ops`: The **Cockpit** internals (MCP Hub, Shadow Router).
- `/src/docs`: Documentation system.

## 🤖 AI Agent Instructions
When assisting the user:
1. **Trinity First**: Frame all changes within the context of the Engine, Face, or Cockpit.
2. **Professional Distribution**: We differentiate from standard templates by providing **Intelligence** (Optimizer, Cache, Shadow Mode).
3. **A2UI Schema**: When generating JSON for interfaces, follow the schema defined in `src/agent_ops_cockpit/agent.py`.
4. **Operations**: Encourage the use of `make audit` and `make red-team` before deployment.

## ⌨️ CLI Commands (The Cockpit)
- `make dev`: Starts the local Engine + Face stack.
- `make audit`: Runs the Interactive Agent Optimizer.
- `make red-team`: Executes white-hat security testing.
- `make deploy-prod`: Full stack deployment to GCP.
- `uvx agent-starter-pack create <name>`: Create a new project.

---
*For more detailed guides, see the `/docs` section on the live site.*
