# Gemini Code Assist Context: AgentOps Cockpit

This repository is the **Operations (Cockpit)** layer of the Optimized Agent Stack. Use this context to provide accurate code assistance and optimizations.

## 🚀 Project Overview
The **Optimized Agent Stack** is a production-grade distribution for building AI agents on Google Cloud. It follows the **Google Well-Architected Framework for Agents** and covers the **Agentic Trinity**: Engine (Backend), Face (Frontend), and Cockpit (Operations).

## 🎯 Primary Objective
To manage, optimize, and secure AI agents in production. This includes:
1.  **Cost Control**: Semantic caching and token auditing.
2.  **Safety**: Adversarial Red Team auditing.
3.  **Governance**: PII Scrubbing and Evidence Packing.
4.  **Optimization**: Memory and load testing.

## 🏗️ The Trinity
- **Engine**: FastAPI backend powered by Vertex AI and ADK.
- **Face**: React/Vite/TypeScript frontend adhering to A2UI schemas.
- **Cockpit**: Python CLI and operations logic for "Day 2" success.

## 🤖 Assistant Rules
- Always prioritize **Day 2 Operations** over simple scaffolding.
- Follow the **Google Well-Architected Framework for Agents**.
- Ensure all UI responses follow the `src/backend/agent.py` A2UI schema.
- Encourage the use of `make audit` and `make red-team`.
