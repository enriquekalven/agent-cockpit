# 🚀 Production Deployment

Deploying a "Well-Architected" agent requires orchestration across two primary Google Cloud environments.

## ⚙️ The Engine (Cloud Run)
The Python backend (FastAPI) is deployed as a serverless service.
- **Scaling**: We default to scale-to-zero to minimize costs during idle time.
- **Regions**: Always deploy to `us-central1` or your local equivalent for lowest latency to Vertex AI endpoints.
- **Best Practice**: Enable **Startup CPU Boost** to reduce cold-start latency by up to 50%.

## 🧠 Agent Engine (Vertex AI Reasoning Engine)
Recommended for agents that require deep integration with the Google Cloud agentic ecosystem.
- **Why**: Provides a managed runtime that handles serialization, versioning, and built-in tracing.
- **Best Practice**: Use **Context Caching** for agents with extremely long system instructions (>32k tokens).

## ☸️ Enterprise Engine (GKE)
Recommended for agents with specialized isolation needs or high-intensity workloads.
- **Why**: Provides the highest level of control over networking (Service Mesh) and compute resources (GPUs).
- **Best Practice**: Use **Workload Identity** to assign fine-grained IAM roles to your K8s service accounts.

---

## 📊 Infrastructure Decision Matrix

| Feature | Agent Engine | Cloud Run | GKE |
| :--- | :--- | :--- | :--- |
| **Orchestration** | Managed (ADK) | Custom (FastAPI) | Custom (K8s) |
| **Scaling** | Automatic | Scale-to-Zero | Dynamic / GPU |
| **Observability** | Vertex AI Traces | Cloud Logging/Trace | Prometheus / Istio |
| **Best Case** | Fast ADK Prototyping | Standard Web Agents | High-Perf Enterprise |

---

## 🎭 The Face (Firebase Hosting)
The React/Vite frontend is deployed to Firebase for globally distributed edge performance.
- **Protocol**: Ensure all components use the **A2UI Protocol** for consistent engine-driven rendering.
- **Responsiveness**: Use mobile-first breakpoints to support iOS and Android high-density displays.
- **Accessibility**: All interactive elements must have `aria-labels` to support automated testing in the Cockpit.
- **Performance**: Split large components (>300 lines) to optimize React's virtual DOM reconciliation.

---

## 🏗️ Deployment Workflow

We use a **1-click deployment** strategy that builds safety into the process:

```bash
make deploy-prod
```

### The "Safe-Build" Sequence:
1. **Audit Phase**: The Cockpit runs `arch-review` (design) and `audit` (cost). 
2. **Security Phase**: Executes `red-team` to ensure no public breaches exist in the latest code.
3. **Build Phase**: Compiles the React application and optimizes static assets.
4. **Push Phase**: 
    - Containerizes the Engine and pushes to **Artifact Registry**.
    - Deploys the container to **Cloud Run**.
    - Deploys static assets to **Firebase Hosting**.

## 🛡️ Staging & Traffic Splitting
We recommend using Cloud Run **Revisions** for canary deployments:
- Deploy 5% of traffic to your new Revision.
- Monitor the **Cockpit Dashboard** for error rate anomalies.
- Promote to 100% when satisfied.

## 🤖 Automated CI/CD (GitHub Actions)

The AgentOps Cockpit is designed for "Policy-as-Code." Every commit to `main` triggers an automated governance pipeline that ensures your agent never regresses in quality or security.

![CI/CD Workflow](/public/cicd-workflow.png)

### The Automated Pipeline:
1.  **Architecture Audit**: Scans for design alignment with the detected framework (LangGraph, ADK, etc.).
2.  **Red Team Evaluation**: Automatically tests for prompt injection and instruction overrides on every PR.
3.  **Token Optimization**: Identifies non-cached prompts and expensive model routing before deployment.
4.  **Reliability Suite**: Runs all unit tests and regression checks against the core engine.

Refer to `.github/workflows/agent-ops-audit.yml` for the full pipeline definition.


## 🔑 Secret Management
Never commit `.env` files. Use **Google Cloud Secret Manager**:
- Store your `GOOGLE_API_KEY` and third-party tool tokens.
- Map them as environment variables in your Cloud Run configuration.
