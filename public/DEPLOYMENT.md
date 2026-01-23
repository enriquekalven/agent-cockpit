# Deployment: Shipping the Optimized Agent Stack

The **Optimized Agent Stack** is designed for high-fidelity, cost-optimized deployment on **Google Cloud**.

## ⚡️ 1-Click Operations (The Cockpit)

The built-in `Makefile` handles the entire production deployment flow.

| Target | Command | Platform |
| :--- | :--- | :--- |
| **Full Stack** | `make deploy-prod` | Cloud Run (Engine) + Firebase (Face) |
| **The Engine** | `make deploy-cloud-run` | Google Cloud Run (Backend) |
| **The Face** | `make deploy-firebase` | Firebase Hosting (Frontend) |

---

## 1. Initial GCP Setup

Before your first deployment, run the setup script to configure your project, enable APIs, and create the Artifact Registry repo.

```bash
chmod +x setup_gcp.sh
./setup_gcp.sh
```

---

## 2. Google Cloud Run (The Engine)

The backend agent is served via Cloud Run, offering serverless scaling and native integration with **Vertex AI** and **Cloud Trace**.

### Manual Deployment Steps
```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Deploy the backend (Engine)
# The setup_gcp.sh script handles this, but here is the manual command:
gcloud run deploy agent-ops-backend \
  --source . \
  --dockerfile Dockerfile.backend \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 3. Firebase Hosting (The Face)

Firebase is used for hosting the static A2UI renderer assets. This ensures your users get the fastest possible bundle delivery.

### Deployment Steps
```bash
# Set up hosting target (one-time)
firebase target:apply hosting agent-ui agent-cockpit

# Build and Deploy
npm run build
firebase deploy --only hosting:agent-ui
```

---

## 🏗️ Scaffolding New Projects

You can use the **Optimized Agent Stack** CLI to scaffold new specialized projects:

```bash
# Standard React Template
uvx agent-starter-pack create my-app

# High-End AG-UI (CopilotKit)
uvx agent-starter-pack create my-app --ui agui

# Mobile Integration (Flutter)
uvx agent-starter-pack create my-app --ui flutter
```

---

## 🛡️ CI/CD & Security

*   **GitHub Actions**: Integrated with `make red-team` to prevent unsafe code from reaching production.
*   **Shadow Mode**: Configured during deployment to allow safe v1/v2 traffic splitting.
*   **Observability**: **Google Cloud Trace** is pre-configured to track "Thought Chains" from the frontend into the backend agent.
