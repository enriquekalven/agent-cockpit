# 📡 A2A (Agent-to-Agent) & The Cockpit

The **Agent-to-Agent (A2A) Protocol** enables distributed agent architectures. In the **AgentOps Cockpit**, A2A is managed as a first-class orchestration pattern.

## 🌉 The Cockpit's Role in A2A
While A2A handles the communication, the Cockpit handles the **Intelligence of the Connection**:
1. **Auditing**: The `make audit` command detects "Chatty A2A" patterns where too many turns occur between agents, suggesting tool-offloading or prompt-collapsing.
2. **Security**: `make red-team` tests the trust boundaries between agents to prevent "Side-Channel Injections" (where a compromised agent hacks another agent).
3. **Caching**: The **Hive Mind Cache** can cache results of expensive A2A sub-tasks across your entire agent mesh.

## 🛠️ Implementation

### 1. Exposing an Agent Service
Wrap your agent as an A2A service for other agents in the Cockpit to consume:
```python
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from src.backend.agent import my_agent

# Standardizing the A2A port to 8001 (Engine is 8000)
a2a_app = to_a2a(my_agent, port=8001)
```

### 2. Orchestration via MCP
The Cockpit uses the **Model Context Protocol (MCP)** to manage A2A connections:
- **Unified Tooling**: Remote agents appear as standard tools in `src/backend/ops/mcp_hub.py`.
- **Latency Tracking**: The Cockpit monitors the round-trip time between agent calls to ensure sub-second UI responsiveness.

## 🔄 A2UI + A2A Flow
When Agent A calls Agent B, the A2UI content from Agent B is automatically passed through to the final surface if the **Cockpit Middleware** is enabled:
```python
# In agent.py
shadow_router = ShadowRouter(v1_func=agent_v1, v2_func=agent_v2)
# Handles A2UI + A2A metadata automatically
```

## 🏗️ Enterprise Mesh
In large-scale deployments, the Cockpit allows you to:
- **A/B Test Agents**: Split traffic between different expert agents using the Shadow Router.
- **Cost Guarding**: Set per-agent budgets to prevent one agent in the mesh from exhausting your quota.
