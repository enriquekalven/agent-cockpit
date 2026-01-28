# 🏁 Quickstart Guide

Welcome to the **AgentOps Cockpit**. This guide will take you from zero to a "Well-Architected" production agent on Google Cloud.

## 🏗️ Step 1: The Scaffolding
The fastest way to start is using our `uvx` generator. This sets up the **Agentic Trinity** (Engine, Face, Cockpit) in seconds.

```bash
uvx agent-ops-cockpit create my-agent --ui a2ui
cd my-agent
npm install
pip install -r requirements.txt
```

## ⚙️ Step 2: Configure the Engine (Backend)
Navigate to `src/backend/agent.py`. This is where your AI reasoning lives.
- **Tools**: Add your function calling logic in the `tools/` directory.
- **Middleware**: notice that **PII Scrubbing**, **Semantic Caching**, and **Evidence Packing** are pre-configured to protect your data.

## 🎭 Step 3: Launch the Face (Frontend)
Start the local development stack to see your agent in action.
```bash
make dev
```
Navigate to `localhost:5173`. You’ll see the **A2UI** interface, which renders your agent's reasoning into interactive surfaces.

## 🕹️ Step 4: Audit from the Cockpit
Before you even think about production, you must pass the **Architecture Review**.
```bash
# Audit your design against Google Well-Architected Framework
make arch-review
```
The Cockpit will grade your agent. If you see a low score, use `make audit` to find cost-saving opportunities like **Context Caching**.

## 🚀 Step 5: One-Click Deploy
Once you've run your **Red Team** security audit and verified performance with the **Load Tester**, deploy the entire stack to Google Cloud:
```bash
make deploy-prod
```

Your agent is now live on **Cloud Run** with professional governance.
