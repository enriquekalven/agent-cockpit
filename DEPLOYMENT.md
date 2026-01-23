## ⚡️ One-Liner Deployments (Makefile)

The project includes a `Makefile` that simplifies deployment to a single command. Ensure you have the respective CLIs installed and authenticated.

| Target | Command | Platform |
| :--- | :--- | :--- |
| **Cloud Run** | `make deploy-cloud-run` | Google Cloud (Serverless) |
| **Firebase** | `make deploy-firebase` | Firebase Hosting |
| **GKE** | `make deploy-gke` | Google Kubernetes Engine |

---

## 🏗️ Scaffolding Options

You can scaffold specialized versions of the Agent UI using `uvx`. Select the implementation standard that matches your tech stack:

### A2UI (Standard React)
The default template, optimized for performance and zero-dependency rendering.
```bash
uvx agentui-starter-pack create my-app
```

### AG UI (High-Fidelity)
Uses the **AG UI** standard (CopilotKit) for high-end React implementations.
```bash
uvx agentui-starter-pack create my-app --ui agui
```

### GenUI SDK (Flutter)
Scaffolds the project with the **GenUI SDK bridge**, ideal for cross-platform mobile and web apps.
```bash
uvx agentui-starter-pack create my-app --ui flutter
```

### Lit (Web Components)
Standardized Web Components that can be embedded into any framework (Angular, Vue, etc).
```bash
uvx agentui-starter-pack create my-app --ui lit
```

---

## 1. Google Cloud Run (Recommended)

Cloud Run is the best platform for serving the A2UI renderer as it offers serverless scaling and zero-config TLS.

### Prerequisites
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and authenticated.
- A Google Cloud Project.

### Deployment Steps
```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Deploy using the included Dockerfile
gcloud run deploy agent-ui-renderer \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 2. Firebase Hosting

Ideal for developers already using Firebase for their frontend assets.

### Prerequisites
- [Firebase CLI](https://firebase.google.com/docs/cli) installed (`npm install -g firebase-tools`).

### Deployment Steps
```bash
# Initialize Firebase (if not already done)
firebase init hosting

# Build production assets
npm run build

# Deploy to Firebase
firebase deploy --only hosting
```

---

## 3. Google Kubernetes Engine (GKE)

For enterprise environments requiring strict networking or integration with an existing Kubernetes mesh.

### Deployment Steps
1. **Build and Push Image**:
   ```bash
   IMAGE_TAG=gcr.io/YOUR_PROJECT_ID/a2ui-renderer:v1
   docker build -t $IMAGE_TAG .
   docker push $IMAGE_TAG
   ```

2. **Deploy to GKE**:
   Create a `deployment.yaml`:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: a2ui-renderer
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: a2ui-renderer
     template:
       metadata:
         labels:
           app: a2ui-renderer
       spec:
         containers:
         - name: a2ui-renderer
           image: gcr.io/YOUR_PROJECT_ID/a2ui-renderer:v1
           ports:
           - containerPort: 80
   ```
   Apply it: `kubectl apply -f deployment.yaml`

---

## 🛠️ Infrastructure Patterns

- **CI/CD**: Use `agent-starter-pack setup-cicd` to automatically scaffold GitHub Actions or Cloud Build triggers.
- **Observability**: Ensure **Cloud Trace** is enabled to follow requests from the UI into the agent backend.
