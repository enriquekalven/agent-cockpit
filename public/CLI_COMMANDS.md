# CLI Reference

The Optimized Agent Stack provides several CLI tools and NPM scripts to streamline your workflow.

## 📦 NPM Scripts

| Command | Description |
| :--- | :--- |
| `npm run dev` | Start the local development server (Vite). |
| `npm run build` | Build the optimized production bundle. |
| `npm run preview` | Preview the local build. |
| `npm run deploy` | Deploy to Firebase Hosting. |
| `npm run lint` | Run ESLint to check for code quality. |

## 🛠️ Gemini CLI Integration

The project is fully compatible with **Gemini CLI**.

### Context Discovery
Gemini CLI uses the `GEMINI.md` and `llm.txt` files to understand your repository.
- `GEMINI.md`: Context for AI agents.
- `llm.txt`: Machine-readable summary.

### Proposed CLI Tool (`agent-ui-starter`)
We are developing a specialized CLI for easier initialization:
```bash
# Setup a project
uvx agent-ui-starter setup

# Generate a new A2UI component
uvx agent-ui-starter generate component [name]

# Deploy directly to Cloud Run
uvx agent-ui-starter deploy --platform cloudrun
```

## 🐋 Docker Commands

Deploy your agent backend or the frontend using Docker:
```bash
docker build -t agent-ui-starter .
docker run -p 8080:8080 agent-ui-starter
```

## ☁️ Firebase CLI

Manage your deployment to Firebase:
```bash
firebase init
firebase deploy --only hosting
```
