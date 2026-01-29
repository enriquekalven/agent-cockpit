# ⚙️ Engine Integration: The Day 0 Brain

The **Engine** is the reasoning core of your Agentic Stack. We use **FastAPI** and Google’s **Agent Development Kit (ADK)** to build agents that are fast, tool-capable, and "Well-Architected."

## 🧩 Middleware Components
The Engine comes pre-installed with the **Cockpit Middleware Stack**:

1. **`CostOptimizer`**: Real-time token tracking and savings recommendations.
2. **`PIIScrubber`**: Automatic masking of sensitive user data.
3. **`SemanticCache`**: Integrated with the "Hive Mind" for 40%+ cost reduction.
4. **`MemoryOptimizer`**: Automates context truncation and summarization.

## 🛠️ Tool Orchestration (ADK)
We recommend building your tools as **MCP (Model Context Protocol)** or **ADK Extensions**. This ensures that the agent can discover and invoke them with high reliability.

```python
# Example Tool in src/agent_ops_cockpit/tools/search.py
from adk import Tool

@Tool
def search_docs(query: str):
    """Searches the knowledge base for agent-ops documentation."""
    return get_search_results(query)
```

## 🏗️ The Agentic Flow
A "Well-Architected" flow always follows this sequence:
1. **Sanitize**: Input passes through the `PIIScrubber`.
2. **Cache Check**: `Hive Mind` checks for a semantic hit.
3. **Reason**: Gemini 2.0 reasoning loop via Vertex AI.
4. **Action**: Tool execution via ADK.
5. **Pack**: Final output is wrapped in an `EvidencePacket` for transparency.

## 🏛️ Grounding
To prevent hallucinations, ensure all tool outputs are grounded in your data sources. Use the `EvidenceNode` class to report the sources used in your final response.
