# ⚙️ Backend Engine Integration (The Trinity Engine)

This guide explains how to connect the **Cockpit** to your agent's **Engine** (Backend). In the Optimized Agent Stack, the Engine handles reasoning while the Cockpit handles governance.

## 🏗️ The Integration Flow

1. **Client** (The Face) sends user `query` to the **Cockpit**.
2. **Cockpit Middleware** performs:
    - **Semantic Cache Check**: If a hit occurs, returns immediately.
    - **Cost Guard**: Estimates cost and blocks if over budget.
    - **Model Routing**: Selects Pro or Flash based on complexity.
3. **Engine** (The Brain) executes reasoning and tools via **ADK**.
4. **Cockpit Shadow Router** optionally sends the call to a shadow-agent for A/B testing.
5. **Combined Result** is returned to the client in **A2UI** format.

---

## 🔌 Connecting to an ADK Agent

### 1. The `agent.py` Protocol
Your agent must implement the `A2UISurface` schema to be rendered by the Face.

```python
from pydantic import BaseModel
from typing import List

class A2UIComponent(BaseModel):
    type: str # e.g. "Text", "Card", "StatBar"
    props: dict
    children: List['A2UIComponent'] = None

class A2UISurface(BaseModel):
    surfaceId: str
    content: List[A2UIComponent]
```

### 2. Using the Ops Middlewares
To make your Engine explicit about being "Optimized", use the Cockpit's decorators:

```python
from .cost_control import cost_guard
from .cache.semantic_cache import hive_mind

@app.get("/agent/query")
@cost_guard(budget_limit=0.05) # 🛡️ Guardrail
@hive_mind(cache=global_cache) # 🧠 Intelligence
async def chat(q: str):
    # Your reasoning logic here
    return result
```

---

## 🛠️ Tooling via MCP Hub
The Cockpit recommends using the **Model Context Protocol (MCP)** for all tool connections. This allows the `make audit` command to monitor tool health and latency.

```python
from .ops.mcp_hub import global_mcp_hub

# ❌ Avoid: requests.get("https://api.weather.com")
# ✅ Use:
result = await global_mcp_hub.execute_tool("weather", {"city": "NYC"})
```

---

## 🧪 Local Testing with the Face
1. Start the backend: `make dev`.
2. Open the **Playground** (`/playground`).
3. Select **"Connect to Local ADK Agent"** in the settings overlay.
4. Use **Agent Mode** to talk directly to your `agent.py` logic.

## 🚢 Deploying the Engine
Use the Cockpit CLI to push your engine to Google Cloud:
```bash
make deploy-cloud-run
```
*This command uses the `Dockerfile` to containerize your python logic and deploy it to a serverless Cloud Run instance.*
