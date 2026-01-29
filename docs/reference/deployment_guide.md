# 🚀 Technical Guide: One-Click Deploy (`make deploy-prod`)

The **One-Click Deploy** is the ultimate operational command that transforms your local source code into a globally distributed agent stack on Google Cloud.

## 🚀 Commands

### Basic Deployment
```bash
make deploy-prod
```

### Advanced Parameters
```bash
agent-ops deploy --name my-production-agent --region us-east1
```

---

## ⚙️ Modifiable Parameters

| Flag | Default | Description |
| :--- | :--- | :--- |
| `--name` | `agent-ops-backend` | The name of the service in Google Cloud Run. |
| `--region` | `us-central1` | The GCP data center where your agent will reside. |

---

## 🔄 The Deployment Pipeline

When you run this command, the Cockpit orchestrates four distinct stages:

### Stage 1: Pre-Flight Audit
Runs a non-interactive **Agent Optimizer Audit**. If critical architectural or cost-waste patterns are detected, the deployment will halt to prevent "leaking" money or exposing vulnerabilities.

### Stage 2: Face Build (Frontend)
Executes `npm run build` to compile the **React/Vite** frontend into production-ready assets (Minified JS, CSS, and A2UI definitions).

### Stage 3: Engine Deployment (GCP)
Uses `gcloud run deploy` to package your Python backend into a container and push it to **Google Cloud Run**. It automatically handles:
- Serverless scaling.
- Secure environment variable injection.
- Unauthenticated access (if configured).

### Stage 4: Face Distribution (Firebase)
Uploads the static assets to **Firebase Hosting** for low-latency distribution via Google's Global CDN.

---

## ✅ Outcome
At the end of the process, you receive a **Custom Domain URL** where your agent cockpit is live and secured.
