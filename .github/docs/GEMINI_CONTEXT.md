# Gemini Code Assist Context: AgentOps Cockpit

This repository is the **Operations (Cockpit)** layer of the Optimized Agent Stack. Use this context to provide accurate code assistance and optimizations.

## 🎯 Primary Objective
To manage, optimize, and secure AI agents in production. This includes:
- **Shadow Mode**: Parallel execution of v1 and v2 agents.
- **Semantic Caching**: Using `hive_mind` to cache LLM responses.
- **Cost Control**: Budgeting and model routing (Pro vs Flash).
- **Red Team**: Automated adversarial testing.

## 🧱 Key Components
- `src/backend/agent.py`: The entry point for the agent logic.
- `src/backend/optimizer.py`: The CLI tool for auditing agent waste.
- `src/backend/ops/`: Contains specialized optimization modules (Memory, Cost, Tooling).
- `src/a2ui/`: The React-based ops dashboard.

## 🤝 Relationship to Other Repos
- `agent-starter-pack`: The **Engine** (fastapi template).
- `agentui-starter-pack`: The **Face** (component library).
- `agent-ops-cockpit`: (This repo) The **Cockpit** (runtime ops).

## 🚀 Optimization Patterns
When writing code for this repo, prioritize:
1. **Gemini 1.5 Flash** for high-volume, low-reasoning tasks.
2. **Context Caching** for large system instructions.
3. **Pydantic Models** for structured A2UI outputs.
4. **FastAPI Dependencies** for auditing and cost guarding.
