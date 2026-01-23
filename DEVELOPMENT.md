# Development Guide: Extending the Stack

The **Optimized Agent Stack** is built to be modular. You can extend the Engine (Backend), the Face (Frontend), or the Cockpit (Ops).

## 📁 Project Structure

### ⚙️ The Engine (Backend)
- `src/backend/agent.py`: The main FastAPI server and agent logic.
- `src/backend/cost_control.py`: Budget management middleware.
- `src/backend/cache/`: Semantic caching logic and vector store connectors.
- `src/backend/shadow/`: Traffic routing for Shadow Mode.

### 🎭 The Face (Frontend)
- `src/a2ui/`: The core JSON ↔ React rendering engine.
- `src/components/`: Shared UI components (Dashboard, StatusBars, etc.).
- `src/docs/`: Documentation site logic.

### 🕹️ The Cockpit (Ops)
- `src/backend/optimizer.py`: The Interactive Optimizer CLI.
- `src/backend/eval/red_team.py`: Adversarial security testing logic.

---

## 🎨 Adding New A2UI Components

To add a new visual component that the agent can "render":

1.  **Create the Component**: Add a new React component in `src/a2ui/components/`.
2.  **Register the Type**: Add the component to the mapping in `src/a2ui/A2UIRenderer.tsx`.
3.  **Update the Schema**: Add the new `props` definition to the `A2UIComponent` model in `src/backend/agent.py`.

---

## 🔍 Extending the Optimizer

You can add your own optimization heuristics to `src/backend/optimizer.py`. Common extensions include:
*   Checking for specific PII patterns in prompts.
*   Enforcing brand voice consistency.
*   Suggesting tool-offloading for specific logic blocks.

---

## 🧪 Testing

### Local Cockpit
Start the full stack locally:
```bash
make dev
```

### Adversarial Audit
Run the security suite:
```bash
make red-team
```
