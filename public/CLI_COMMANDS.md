# Optimized Agent Stack: CLI & Cockpit Reference

The **Optimized Agent Stack** provides a comprehensive set of tools for both building (Scaffolding) and managing (Operations) AI agents.

## 1. Scaffolding (Day 0)

Use `uvx` to create new projects without local installation:

### `create`
Scaffold a new project with a specific UI flavor.
```bash
uvx agent-starter-pack create my-agent --ui a2ui
```

---

## 2. The Cockpit: Agent Operations (Makefile)

Use the included `Makefile` for Day 2 production management.

### `make audit`
Runs the **Interactive Agent Optimizer**.
*   **Scanning**: Scans `agent.py` for cost/perf waste.
*   **Proposals**: Suggests Gemini Context Caching, Prompt Compression, and MCP Migration.
*   **Approval**: Interactive `approve/reject` workflow.

### `make red-team`
Unleashes a security audit against your agent.
*   **Adversarial Eval**: Prompt injection, PII extraction, and jailbreak simulation.
*   **Safety Lock**: Fails deployment if vulnerabilities are found.

### `make dev`
Starts the local development stack (Vite frontend + FastAPI backend).
```bash
make dev
```

### `make deploy-prod`
The "Golden Path" to production.
1.  **Optimization**: Runs a fresh audit.
2.  **Build**: Compiles the React frontend.
3.  **Engine**: Deploys the backend to **Google Cloud Run**.
4.  **Face**: Deploys the frontend to **Firebase Hosting**.

---

## 3. Operations Dashboard (Cockpit UI)

Navigate to `/ops` on your deployed or local instance to access the **Control Plane**.

*   **Shadow Mode Router**: Compare v1 vs v2 responses in real-time.
*   **Flight Recorder**: Step-through visual scrubber for agent thought chains.
*   **Semantic Cache Stats**: Real-time visualization of cost savings from the "Hive Mind" cache.
*   **MCP Hub Status**: Monitor the health of standardized tool connections.

---

## 4. Google Cloud Setup

To initialize the environment for the first time, use the setup script:
```bash
chmod +x setup_gcp.sh
./setup_gcp.sh
```
This configures Artifact Registry, enables APIs, and runs the initial security evaluation.
