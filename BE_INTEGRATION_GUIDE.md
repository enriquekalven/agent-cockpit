# Backend Agent Integration Guide

This guide explains how to connect your **Optimized Agent Stack** to a live backend agent powered by **ADK (Agent Development Kit)** and **Vertex AI Agent Engine**.

## 🏗️ Architecture

The A2UI flow typically follows this pattern:
1. **User Input**: Client sends a message to the Agent.
2. **Execution**: Agent executes tools and decides on the UI response.
3. **A2UI Response**: Agent returns a JSON object following the `A2UISurface` schema.
4. **Rendering**: The React frontend receives the JSON and renders it via `A2UISurfaceRenderer`.

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

### 2. Event-Driven (WebSocket / SSE)
For real-time streaming interfaces (e.g., watching an agent think), use WebSockets or Server-Sent Events (SSE).

ADK agents can be wrapped in a FastAPI server that exposes these streams.

---

## 🎮 Interactive Local Playground

The **A2UI Playground** now supports a "Real Backend" mode. To use it:

1. **Start the Sample Agent**:
   ```bash
   python3 src/backend/agent.py
   ```
   *This starts a FastAPI server on port 8000.*

2. **Enable Connection**:
   In the Playground header, switch to **Agent Mode**, then check the **"Connect to Local ADK Agent"** box at the bottom.

3. **Interact**:
   Type messages in the chat. The React frontend will now fetch real A2UI JSON from your Python backend instead of using the mock logic.

---

## 🤖 ADK Backend Setup

To send A2UI from an ADK agent, use the `SendA2uiToClientToolset`:

```python
from adk import LlmAgent, tool
from a2ui_tools import SendA2uiToClientToolset

# 1. Define your agent
agent = LlmAgent(
    name="DashboardAgent",
    instructions="Generate a system dashboard based on the user's query.",
    tools=[...my_tools]
)

# 2. Add the A2UI toolset
agent.use(SendA2uiToClientToolset())

# 3. Use it in a tool
@tool
def update_view(tool_context):
    """Updates the user's dashboard."""
    surface = {
        "surfaceId": "dynamic-dashboard",
        "content": [
            {"type": "Text", "props": {"text": "Updated via ADK!", "variant": "h1"}}
        ]
    }
    tool_context.send_a2ui(surface)
```

---

## 🚀 Deployment to Agent Engine

Once your agent is ready, deploy it to **Vertex AI Agent Engine**:

```bash
agent-starter-pack deploy --project YOUR_PROJECT_ID
```

Your React frontend can then call the Agent Engine API using the `RemoteA2aAgent` pattern or a custom bridge.

## 🔗 Resources
- [A2A Guide](./A2A_GUIDE.md)
- [Official A2UI Specs](https://a2ui.org)
- [ADK Documentation](https://github.com/a2aproject/adk)
