# Backend Engine Integration Guide

This guide explains how to connect your **Optimized Agent Stack** to a live backend agent powered by **ADK (Agent Development Kit)** and **Vertex AI Agent Engine**.

## 🏗️ Architecture: The Engine (Day 0)

The A2UI flow typically follows this pattern:
1. **User Input**: Client sends a message to the Agent.
2. **Execution**: The **Engine** (fastapi backend) executes tools and decides on the UI response.
3. **A2UI Response**: Agent returns a JSON object following the `A2UISurface` schema.
4. **Rendering**: The **Face** (React frontend) receives the JSON and renders it instantly.

---

## 🔌 Connecting to an ADK Agent

### 1. Simple POLLING (Fastest)
In your `Playground` component, you can poll a backend endpoint that returns the latest surface for a session.

```typescript
useEffect(() => {
  const interval = setInterval(async () => {
    const res = await fetch(`https://your-agent-backend.com/surface/${sessionId}`);
    const data = await res.json();
    setSurface(data);
  }, 2000);
  return () => clearInterval(interval);
}, [sessionId]);
```

---

## 🎮 Interactive Local Playground

The **A2UI Playground** supports a "Real Backend" mode to test your Engine logic locally.

1. **Start the Engine**:
   ```bash
   make dev
   ```
   *This starts the FastAPI server (agent.py) on port 8000.*

2. **Enable Connection**:
   In the Playground header, switch to **Agent Mode**, then check the **"Connect to Local ADK Agent"** box at the bottom.

---

## 🤖 Engine Setup (Python ADK)

To send A2UI from an ADK agent, use the `A2UISurface` model provided in `src/backend/agent.py`.

```python
from .agent import A2UISurface, A2UIComponent

# 1. Define your tool
async def generate_mcp_report(query: str):
    return A2UISurface(
        surfaceId="mcp-report",
        content=[
            A2UIComponent(type="Text", props={"text": "⚡ MCP Health", "variant": "h1"}),
            A2UIComponent(type="Card", props={"title": "Connectivity Status"})
        ]
    )
```

### Tool Usage Optimization (MCP Hub)
Instead of using fragmented Tool APIs, the **Optimized Agent Stack** recommends using the **MCP Hub**:

```python
from .ops.mcp_hub import global_mcp_hub

# Execute tools via standardized MCP protocol
result = await global_mcp_hub.execute_tool("search", {"q": query})
```

---

## 🚀 Deployment to Google Cloud

When you are ready to ship the **Engine**, use the **Cockpit** deployment command:

```bash
make deploy-prod
```

This will:
1.  Containerize your Python Engine logic.
2.  Deploy to **Google Cloud Run**.
3.  Configure IAM and Cloud Trace automatically.

## 🔗 Resources
- [A2A Guide](./A2A_GUIDE.md)
- [Official A2UI Specs](https://a2ui.org)
- [ADK Documentation](https://github.com/a2aproject/adk)
