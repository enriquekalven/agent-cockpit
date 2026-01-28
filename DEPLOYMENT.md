# 🚀 Production Deployment

Deploying a "Well-Architected" agent requires orchestration across two primary Google Cloud environments.

## ⚙️ The Engine (Cloud Run)
The Python backend (FastAPI) is deployed as a serverless service.
- **Scaling**: We default to scale-to-zero to minimize costs during idle time.
- **Regions**: Always deploy to `us-central1` or your local equivalent for lowest latency to Vertex AI endpoints.

## 🎭 The Face (Firebase Hosting)
The React/Vite frontend is deployed to Firebase for globally distributed edge performance.

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

## 🔑 Secret Management
Never commit `.env` files. Use **Google Cloud Secret Manager**:
- Store your `GOOGLE_API_KEY` and third-party tool tokens.
- Map them as environment variables in your Cloud Run configuration.
