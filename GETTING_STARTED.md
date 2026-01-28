# 🏁 Getting Started with AgentOps Cockpit

Welcome to the **AgentOps Cockpit**, the governance and optimization layer of the Optimized Agent Stack. This guide helps you set up "Day 2" operations for your agents.

## 🏗️ Phase 1: Installation & Setup

1.  **Clone & Install**:
    ```bash
    git clone https://github.com/enriquekalven/agent-ops-cockpit.git
    cd agent-ops-cockpit
    npm install
    pip install -r requirements.txt
    ```

2.  **GCP Environment**:
    Ensure you have `gcloud` configured and billing enabled.
    ```bash
    chmod +x setup_gcp.sh
    ./setup_gcp.sh
    ```

## ⚙️ Phase 2: Connecting the Engine (Backend)

The Cockpit manages an **Agent Engine**. 
- Open `src/backend/agent.py` to see the core reasoning logic.
- Notice the **Shadow Router**, **Hive Mind Cache**, and **Cost Guard** middlewares. These are the "Cockpit" features that make your agent production-ready.

## 🎭 Phase 3: The Face (Ops Dashboard)

1.  **Launch the Stack**:
    ```bash
    make dev
    ```
2.  **The Ops Dashboard**:
    Navigate to `localhost:5173/ops`. This is where you monitor:
    - **Shadow Mode**: Side-by-side v1 vs v2 comparisons.
    - **Intelligence Node**: Real-time status of your agent's reasoning.
    - **Cost/Memory Metrics**: Efficiency data from the optimizers.

## 🕹️ Phase 4: Running Operations

1.  **Optimization Audit**:
    Run `make audit` to identify wasteful tokens and implement Gemini Context Caching.
2.  **Security Evaluation**:
    Run `make red-team` to simulate adversarial attacks and harden your agent.

---

## 🚀 Production Deployment

When your agent is hardened and optimized:
```bash
make deploy-prod
```
This command runs a final audit, builds production assets, and deploys to **Google Cloud Run** (Backend) and **Firebase Hosting** (Frontend).
