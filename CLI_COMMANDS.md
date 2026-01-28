# 📟 AgentOps Cockpit: CLI & Manual Reference

The **AgentOps Cockpit** provides a dual-interface for managing agent lifecycle: the `agent-ops` CLI for development and the `Makefile` for operations.

## 1. The `agent-ops` CLI (Development)

This command is provided by the `agent-ops-cockpit` python package.

### `version`
Check the installed version of the Cockpit tools.
```bash
agent-ops version
```

### `create`
Scaffold a new project in the "Optimized Agent Stack" architecture.
```bash
agent-ops create <project_name> [--ui a2ui|agui|flutter]
```
- **a2ui**: The standard adaptive-surface React template.
- **agui**: High-fidelity dashboard using CopilotKit.
- **flutter**: Cross-platform mobile SDK bridge.

---

## 2. Operational Intelligence (Makefile)

Use these commands for Day 2 management and CI/CD automation.

### `make arch-review`
Executes the **Google Well-Architected Design Review**.
- **Checks**: Runtime, Caching, PII Scrubbing, and Operational readiness.
- **Goal**: Full alignment with Google's production agent standards.

### `make audit`
Runs the **Interactive Agent Optimizer**.
- **Checks**: Context caching, prompt compression, model routing (Flash vs Pro).
- **Goal**: Token efficiency and cost reduction (Up to 40-90% savings).

### `make red-team`
Executes the **Adversarial Security Evaluator**.
- **Checks**: Prompt injections, PII extraction, and safety filter bypasses.
- **Goal**: Production hardening. Any breach will **fail the build**.

### `make load-test`
Executes the **Base Load Tester**.
- **Metrics**: Latency, success rate, and concurrency handling.
- **Goal**: Performance validation for high-traffic agents.
- **Usage**: `make load_test REQUESTS=200 CONCURRENCY=20`

### `make dev`
Starts the local development stack.
- **Backend**: FastAPI running at `localhost:8000`.
- **Frontend**: Vite/React running at `localhost:5173`.

### `make deploy-prod`
The automated 1-click deployment pipeline.
1. Runs `make audit`.
2. Runs `npm run build`.
3. Deploys Backend to **Google Cloud Run**.
4. Deploys Frontend to **Firebase Hosting**.

---

## 3. Advanced Operations (Dashboard)

Navigate to `/ops` to access the Visual Cockpit.

- **Shadow Mode**: Monitor parallel v1/v2 execution. Use this to compare model updates with zero risk.
- **Hive Mind (Semantic Cache)**: Monitor cache hits and see total saved tokens.
- **Memory Stats**: Observe the "Leaky Bucket" eviction policy in action.
- **Cost Guard**: Real-time spending analysis per agent turn.

---

## 4. Setup
Initialize your Google Cloud environment:
```bash
chmod +x setup_gcp.sh
./setup_gcp.sh
```
