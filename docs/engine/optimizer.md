# 🔍 Technical Guide: Agent Optimizer (`make audit`)

The **Agent Optimizer** is a code-level auditor that identifies waste, legacy patterns, and cost-reduction opportunities in your agent's source code.

## 🚀 Commands

### Local Installation
```bash
make audit         # Interactive audit
agent-ops audit src/agent_ops_cockpit/agent.py --quick
```

### Portable (Zero-Install)
```bash
uvx agentops-cockpit audit agent.py --quick
```

---

## 💡 Key Optimizations

### 1. Situational Intelligence (Triple-State Analysis)
The optimizer understands the state of your environment:
- **Missing SDKs**: Detects logic that predicts an SDK is needed but not installed.
- **Legacy Workarounds**: Provides situational fixes for older versions (e.g., pre-v1.70.0 Vertex AI).
- **Modernization**: Highlights native performance gains (e.g., Context Caching).

### 2. Conflict Guard
The optimizer catches "Cross-Framework Gridlock":
*   **Conflict**: Using `CrewAI` agents inside a `LangGraph` loop can cause state corruption.
*   **Synergy**: Pair `Google ADK` with `MCP Hub` for optimized tool discovery.

### 3. FinOps Projections
The audit provides a literal dollar-amount projection:
*   **Prompt Tokens**: Estimates cost per 1M tokens.
*   **Savings**: Calculates projected monthly savings if recommended optimizations (Caching, Routing) are applied.
