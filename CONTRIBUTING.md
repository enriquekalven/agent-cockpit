# Contributing to AgentOps Cockpit

First off, thank you for helping us build the future of Agent Operations! 🚀

## 🏗️ Architecture Philosophy
We follow the **Trinity** model:
1. **Engine**: Handled by the agent engine.
2. **Face**: Handled by A2UI.
3. **Cockpit**: This repo. Focus on the middleware, caching, routing, and auditing.

## 🛠️ Development Workflow
1. Fork the repo.
2. Install dependencies: `pip install -e .` and `npm install`.
3. Run the optimizer audit before committing: `make audit`.
4. Ensure your agent logic passes the `red-team` eval.

## 🔍 Agent Optimizer Standards
All new agent components should be auditable via `src/agent_ops_cockpit/optimizer.py`. If you add a new pattern (e.g., a new caching strategy), update the analyzer logic in `optimizer.py` to recognize it.

## 🚢 Deployment
We use a **1-click deployment** strategy via `Makefile`:
- `make deploy-prod`: Deploys both the backend (Cloud Run) and the dashboard (Firebase).

## 📄 License
By contributing, you agree that your contributions will be licensed under the MIT License.
