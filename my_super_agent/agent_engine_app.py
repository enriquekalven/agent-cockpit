import os
import vertexai
from typing import Any
from vertexai.agent_engines.templates.adk import AdkApp
from my_super_agent.agent import app as adk_app

class AgentEngineApp(AdkApp):
    def set_up(self) -> None:
        """Initialize the agent engine app."""
        vertexai.init()
        super().set_up()

    def register_feedback(self, feedback: dict[str, Any]) -> None:
        """Mock feedback registration for tests."""
        if not isinstance(feedback.get("score"), (int, float)):
            raise ValueError("Score must be numeric")
        print(f"Feedback registered: {feedback}")

    def register_operations(self) -> dict[str, list[str]]:
        """Registers the operations of the Agent."""
        operations = super().register_operations()
        operations[""] = operations.get("", []) + ["register_feedback"]
        return operations

agent_engine = AgentEngineApp(
    app=adk_app
)
