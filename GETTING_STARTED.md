# Getting Started: The Agentic Trinity

Welcome to the **Optimized Agent Stack**. This guide will take you from zero to a production-ready agent in three phases.

## Phase 0: The Engine (Backend)
1.  **Initialize the Environment**:
    ```bash
    chmod +x setup_gcp.sh
    ./setup_gcp.sh
    ```
2.  **Understand `agent.py`**:
    Open `src/backend/agent.py`. This is where your agent's reasoning lives. It uses the **ADK** (Agent Development Kit) to communicate with Gemini.

## Phase 1: The Face (Frontend)
1.  **Launch the Development Stack**:
    ```bash
    make dev
    ```
2.  **The Playground**:
    Navigate to `localhost:5173/playground`. Here you can hand-craft A2UI blueprints or test real agent logic by selecting "ADK Backend".

## Phase 2: The Cockpit (Operations)
Once your agent is running, you need to manage it.

1.  **Optimization**:
    Run `make audit` to see how the **Interactive Optimizer** can save you up to 40% on token costs.
2.  **Security**:
    Run `make red-team` to simulate white-hat attacks against your agent.
3.  **Governance**:
    Open the **Ops Dashboard** at `localhost:5173/ops` to monitor Shadow Mode comparisons and the Flight Recorder.

---

## Deployment
When you are ready for production:
```bash
make deploy-prod
```
This 1-click command optimizes your code, builds the assets, and deploys everything to **Google Cloud (Cloud Run + Firebase)**.
