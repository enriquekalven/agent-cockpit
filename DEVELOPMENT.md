# 🛠️ Development Guide: Building the Cockpit

This repository is optimized for **AgentOps** development. Use this guide to extend the platform's optimization and governance capabilities.

## 📁 Repository Structure

### 🕹️ The Cockpit (Core Operations)
- `src/backend/optimizer.py`: The **Interactive Auditor**. Analyzes agent code for waste.
- `src/backend/eval/red_team.py`: The **Security Evaluator**. Simulates attacks.
- `src/backend/ops/`: Advanced optimization modules.
    - `cost_optimizer.py`: Token tracking and "Flash vs Pro" routing logic.
    - `memory_optimizer.py`: Leaky-bucket eviction and TTL management.
    - `mcp_hub.py`: Centralized tool connectivity.

### ⚙️ The Engine (Logic Layer)
- `src/backend/agent.py`: Entry point for agentic reasoning and middleware.
- `src/backend/cache/`: Semantic caching implementations (Hive Mind).
- `src/backend/shadow/`: Parallel traffic routing logic.

### 🎭 The Face (Internal Dashboard)
- `src/a2ui/`: A2UI rendering protocol and core surfaces.
- `src/components/OpsDashboard.tsx`: High-fidelity operations monitoring.

---

## 🔍 Extending the Agent Optimizer
The `optimizer.py` script uses heuristic analysis to find waste. To add a new check:
1. Open `src/backend/optimizer.py`.
2. Add a matching pattern to the `analyze_code` function.
3. Define the `OptimizationIssue` with a clear `impact`, `savings`, and `diff`.

## 🛡️ Hardening with Red Team
The `red_team.py` CLI simulates adversarial payloads.
- **Payrolls**: Defined in the `attacks` list.
- **Goal**: Fail the CI pipeline if a breach is detected.
- **Best Practice**: Add a Red Team test for every new tool or capability you add to the Engine.

## 🚢 CI/CD Workflow (Code Lime)
GitHub Actions are configured in `.github/workflows/main.yml`.
- **Linting**: Uses `ruff` for ultra-fast Python checks.
- **Agent Audit**: Runs `make audit` on every PR.
- **Red Team**: Runs adversarial tests before any deployment.

---

## 🧪 Local Testing
1. **Frontend + Backend**: `make dev`
2. **Optimizer Only**: `python src/backend/optimizer.py`
3. **Red Team Only**: `python src/backend/eval/red_team.py`
