# A2A (Agent-to-Agent) Protocol Guide

The **Agent-to-Agent (A2A) Protocol** is a core part of the ADK ecosystem, enabling distributed agent architectures and seamless communication between different agentic services.

## 📡 What is A2A?

While A2UI focuses on how agents talk to *users*, A2A focuses on how agents talk to *each other*. It provides a standardized way for an agent to:
1.  **Discover** other agents' capabilities.
2.  **Call** other agents as tools.
3.  **Stream** results (including A2UI payloads) back to a controller agent.

## 🛠️ Implementation Patterns

### 1. Exposing an Agent as an A2A Service
You can wrap any `LlmAgent` into a FastAPI-based A2A server using the `to_a2a` utility.

```python
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from my_project.agents import MyExpertAgent

expert_agent = MyExpertAgent(...)
a2a_app = to_a2a(expert_agent, port=8001)
```

### 2. Communicating via RemoteA2aAgent
A controller agent can interact with a remote A2A service as if it were a local tool.

```python
from google.adk.a2a.remote_a2a_agent import RemoteA2aAgent

# Point to the remote agent's descriptor
remote_expert = RemoteA2aAgent(
    name="expert_proxy",
    agent_card="http://expert-service:8001/a2a/expert/.well-known/agent.json"
)

# Add it to your main agent's toolset
orchestrator = LlmAgent(
    tools=[remote_expert],
    ...
)
```

## 🔄 A2A + A2UI
When a remote agent generates A2UI content, the `A2aAgentExecutor` automatically handles the conversion of tool outputs into A2A parts, ensuring the final client receives a correctly formatted UI.

```python
from a2ui.send_a2ui_to_client_toolset import convert_send_a2ui_to_client_genai_part_to_a2a_part

config = A2aAgentExecutorConfig(
    genai_part_converter=convert_send_a2ui_to_client_genai_part_to_a2a_part
)
executor = A2aAgentExecutor(config)
```

## 🌐 Enterprise Mesh
In a production environment, A2A agents can be registered in the **Vertex AI MCP Registry**, allowing for dynamic discovery and secure, authenticated cross-project communication.
