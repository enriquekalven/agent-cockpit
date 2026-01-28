# 🚢 Deployment: Shipping the AgentOps Cockpit

The **AgentOps Cockpit** is designed for high-fidelity, cost-optimized deployment on **Google Cloud Platform**.

## ⚡ 1-Click Operations

The `Makefile` handles the entire production deployment flow.

| Target | Command | Platform |
| :--- | :--- | :--- |
| **Full Stack** | `make deploy-prod` | Cloud Run (Backend) + Firebase (Frontend) |
| **The Cockpit Engine** | `make deploy-cloud-run` | Google Cloud Run |
| **The Ops Dashboard** | `make deploy-firebase` | Firebase Hosting |

---

## 🏗️ 1. Initial Infrastructure Setup

Before your first deployment, run the setup script to configure your GCP project, enable required APIs (Vertex AI, Cloud Run, Artifact Registry), and set up IAM permissions.

```bash
chmod +x setup_gcp.sh
./setup_gcp.sh
```

---

## ⚙️ 2. Google Cloud Run (The Backend)

The **Cockpit Engine** is served via Cloud Run, offering serverless scaling and native integration with **Vertex AI**, **Cloud Logging**, and **Cloud Trace**.

### Manual Deployment
```bash
# Deploy the backend
gcloud run deploy agent-ops-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

---

## 🎭 3. Firebase Hosting (The Frontend)

Firebase Hosting serves the **Ops Dashboard** (React/A2UI). This ensures low-latency delivery of the interface blueprints.

### Manual Deployment
```bash
# Initialize Firebase (if not already done)
firebase init hosting

# Build and Deploy
npm run build
firebase deploy --only hosting
```

---

## 🛡️ CI/CD: The "Code Lime" Pipeline

We use **GitHub Actions** to enforce quality and security standards before any code reaches production.

1. **Audit**: Every PR runs `make audit`. If wasteful token usage is detected (e.g., missing Gemini Context Caching), the build warns the developer.
2. **Hardening**: `make red-team` runs adversarial attacks. Any security breach (PII leak, jailbreak) will **fail the build**.
3. **Deployment**: Successful merges to `main` trigger an automated deployment to Google Cloud.

---

## 🕵️ Shadow Mode Configuration

Shadow Mode splits traffic between two agent versions. After deployment, use the **Ops Dashboard** to evaluate the delta between `v1-stable` and `v2-experimental`. Once confidence is high, promote the shadow version to production.
