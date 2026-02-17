import os
import re
from typing import Any, List

# Sovereign Alignment: ADK & Reasoning Engine Compatibility
try:
    from google import adk
    from google.adk.agents import base_agent
    from google.adk.agents.context_cache_config import ContextCacheConfig
    AgentBase = base_agent.BaseAgent
    HAS_ADK = True
except ImportError:
    HAS_ADK = False
    print("⚠️  Warning: google-adk not found. Running in Mock Mode.")
    class AgentBase:
        def __init__(self, **kwargs): pass

from tenacity import retry, wait_exponential, stop_after_attempt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PrivateAttr

app = FastAPI(title="My Super Agent Service")

class Query(BaseModel):
    text: str

class SuperAgent(AgentBase):
    """
    My Super Agent: ADK-powered for high-fidelity reasoning.
    Compatible with Vertex AI Agent Engine (Reasoning Engine).
    """
    name: str = "my_super_agent"
    description: str = "High-fidelity AI agent for solving complex laboratory tasks."
    project_id: str = "YOUR_PROJECT_ID"
    location: str = "us-central1"
    
    # Use PrivateAttr for non-serializable/internal state to bypass extra='forbid'
    _forbidden_patterns: List[str] = PrivateAttr(default_factory=list)
    context_cache_config: Any = None 

    def model_post_init(self, __context: Any) -> None:
        """Initialize non-pydantic fields or logic after model setup."""
        if HAS_ADK and not self.context_cache_config:
            try:
                from google.adk.agents.context_cache_config import ContextCacheConfig
                self.context_cache_config = ContextCacheConfig(ttl_seconds=3600)
            except Exception:
                pass
        
        self._forbidden_patterns = [
            r"(?i)password", r"(?i)secret", r"(?i)social security", r"\d{3}-\d{2}-\d{4}"
        ]

    def _sanitize_input(self, text: str) -> str:
        """Security: Guard against prompt injection and PII leakage."""
        if not text: return ""
        # jailbreak guard
        if any(x in text.lower() for x in ["ignore previous", "system prompt", "you are now"]):
            raise ValueError("Potential security breach detected.")
        
        # PII Redaction
        sanitized = text
        for pattern in self._forbidden_patterns:
            sanitized = re.sub(pattern, "[REDACTED]", sanitized)
        return sanitized

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    def solve_task(self, prompt: str) -> str:
        """Main reasoning logic."""
        sanitized_prompt = self._sanitize_input(prompt)
        return f"Sovereign Solution: Processed '{sanitized_prompt}' on {self.project_id}. (ADK: {HAS_ADK})"

    def query(self, input: str) -> str:
        """Vertex AI Agent Engine Requirement: Primary entry point."""
        return self.solve_task(input)

agent_instance = SuperAgent()

@app.post("/chat")
async def chat(query: Query):
    try:
        response = agent_instance.solve_task(query.text)
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        return {"response": f"Unexpected error: {str(e)}"}

@app.get("/health")
async def health():
    return {"status": "ok", "has_adk": HAS_ADK}

@app.get("/.well-known/agent-card.json")
async def agent_card():
    service_url = os.environ.get("SERVICE_URL", "https://my-super-agent-wbrvbbeq2a-uc.a.run.app")
    return {
        "protocolVersions": ["1.0"],
        "id": "my-super-agent",
        "name": "Super Agent (ADK)",
        "description": "High-fidelity AI agent for solving complex laboratory tasks.",
        "capabilities": {"streaming": False, "conversational": True},
        "skills": [
            {
                "name": "query",
                "description": "Primary task solver.",
                "parameters": {
                    "type": "object",
                    "properties": { "input": { "type": "string" } },
                    "required": ["input"]
                }
            }
        ],
        "endpoints": {
            "task": f"{service_url}/chat",
            "status": f"{service_url}/health",
            "card": f"{service_url}/.well-known/agent-card.json"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
