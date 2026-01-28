# Optimized Agent Stack: CLI & Cockpit Reference

The **Optimized Agent Stack** provides a comprehensive set of tools for both building (Scaffolding) and managing (Operations) AI agents.

## 1. Installation & Scaffolding (Day 0)

The AgentOps Cockpit is available as a professional CLI on PyPI.

### Install globally:
```bash
pip install agentops-cockpit
```

### Scaffold a new project:
```bash
# Creates a new Well-Architected agent repo
agent-ops create my-agent --ui a2ui
```

---

## 2. Operations & Auditing (The Cockpit)

Run these commands inside any agent repository to verify governance-as-code.

### `agent-ops arch-review`
Audits agent design against the **Google Well-Architected Framework**.
*   **Detection**: Automatically detects frameworks (LangGraph, ADK, CrewAI).
*   **Gap Analysis**: Identifies architectural weaknesses in security, cost, and reliability.

### `agent-ops audit`
Runs the **Interactive Agent Optimizer** on specific logic files.
*   **Scanning**: Checks for token waste, missing cache, or inefficient model routing.
*   **Proposals**: Suggests localized code improvements with an interactive diff viewer.
*   **Optimization**: Defaults to `agent.py`.

### `agent-ops red-team`
Unleashes adversarial security evaluations.
*   **Stress Test**: Simulates prompt injections, PII leaks, and jailbreak attempts.
*   **Safety Grade**: Provides a pass/fail grade for production readiness.

### `agent-ops report`
The "Full Mission Sweep". Runs all audits (Arch, Quality, Security, Cost) and generates a comprehensive `cockpit_final_report.md`.

---

### Tool Usage Optimization (MCP Hub)
Instead of using fragmented Tool APIs, the **Optimized Agent Stack** provides a unified **MCP (Model Context Protocol) Hub**. This allows you to connect to any industry-standard tool server (Google Search, SQL, Slack) with a single interface.

```python
from agent_ops_cockpit.ops.mcp_hub import global_mcp_hub

# 1. Register an MCP server (e.g., Google Search)
global_mcp_hub.register_server(
    "google-search", 
    "npx", 
    ["-y", "@modelcontextprotocol/server-google-search"]
)

# 2. Execute tools via standardized MCP protocol
result = await global_mcp_hub.execute_tool("search", {"q": "Vertex AI updates"})
```
Govern all execution metrics via the Cockpit dashboard.

---

## 3. Operations Dashboard (Cockpit UI)

Navigate to `/ops` on your deployed or local instance to access the **Control Plane**.

*   **Shadow Mode Router**: Compare v1 vs v2 responses in real-time.
*   **Flight Recorder**: Step-through visual scrubber for agent thought chains.
*   **Semantic Cache Stats**: Real-time visualization of cost savings from the "Hive Mind" cache.
*   **MCP Hub Status**: Monitor the health of standardized tool connections.

---

## 4. Google Cloud Setup

To initialize the environment for the first time, use the setup script:
```bash
chmod +x setup_gcp.sh
./setup_gcp.sh
```
This configures Artifact Registry, enables APIs, and runs the initial security evaluation.
