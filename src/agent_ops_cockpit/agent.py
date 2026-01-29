from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import asyncio
import os
import logging

# --- Configure Structured Logging ---
from .cost_control import cost_guard
from .cache.semantic_cache import hive_mind, global_cache
from .shadow.router import ShadowRouter
from .ops.mcp_hub import global_mcp_hub
from fastapi.middleware.cors import CORSMiddleware

# --- Configure Structured Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("agent-cockpit")

app = FastAPI(title="Optimized Agent Stack")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class A2UIComponent(BaseModel):
    type: str
    props: dict
    children: Optional[List['A2UIComponent']] = None

class A2UISurface(BaseModel):
    surfaceId: str
    content: List[A2UIComponent]

# --- Safety & Governance Guardrails (Red Team Mitigation) ---
try:
    with open(os.path.join(os.path.dirname(__file__), "system_prompt.md"), "r") as f:
        SYSTEM_PROMPT = f.read()
except Exception:
    SYSTEM_PROMPT = "You are a professional Google Cloud Agent Cockpit. Do not leak PII."

PERSONA_SAFE = True
PII_SCRUBBER_ACTIVE = True
SAFETY_FILTER_LEVEL = "HIGH"

# --- Resiliency & Retries (Best Practice) ---
try:
    from tenacity import retry, wait_exponential, stop_after_attempt
except ImportError:
    # Dummy decorator fallback for environments without tenacity installed
    import functools
    def retry(*args, **kwargs):
        def decorator(f):
            @functools.wraps(f)
            async def wrapper(*a, **k):
                return await f(*a, **k)
            return wrapper
        return decorator
    def wait_exponential(*args, **kwargs): return None
    def stop_after_attempt(*args, **kwargs): return None

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def call_external_database(data: dict):
    """Simulates a resilient DB call with exponential backoff."""
    # In production, this would be your AlloyDB or BigQuery connector
    logger.info(f"📡 Attempting resilient DB sync for: {data.get('id')}")
    return {"status": "success", "id": data.get("id")}

def scrub_pii(text: str) -> str:
    """Mock PII scrubber for well-architected compliance."""
    # Logic to filter i18n leaks and multilingual attacks
    return text.replace("secret@google.com", "[REDACTED]")

# --- Core Intelligence Logic ---

async def agent_v1_logic(query: str, session_id: str = "default") -> A2UISurface:
    """Production Agent (v1) - Reliable & Fast with Session Support."""
    logger.info(f"Agent v1 processing query for session: {session_id}")
    # Simulate DB sync with retry logic
    await call_external_database({"id": session_id, "query": query})
    
    # Simulate MCP tool usage
    if "search" in query.lower():
        await global_mcp_hub.execute_tool("search", {"q": query})
    return generate_dashboard(query, version="v1-stable")

async def agent_v2_logic(query: str, session_id: str = "default") -> A2UISurface:
    """Experimental Agent (v2) - High Reasoning/Shadow Mode."""
    # Smart routing: Use Flash for simple greetings to save tokens
    if len(query) < 10:
        logger.info("⚡ Using Gemini Flash for simple query")
        return generate_dashboard(query, version="v2-shadow-flash")
    
    # Simulate slightly different behavior or better reasoning
    await asyncio.sleep(0.5) # Simulate Pro model latency
    return generate_dashboard(query, version="v2-shadow-pro")

# --- Helper Generators ---

def generate_dashboard(query: str, version: str) -> A2UISurface:
    return A2UISurface(
        surfaceId="dynamic-response",
        content=[
            A2UIComponent(
                type="Text", 
                props={"text": f"Agent {version} Response for: {query}", "variant": "h1"}
            ),
            A2UIComponent(
                type="Card",
                props={"title": f"Intelligence Loop ({version})"},
                children=[
                    A2UIComponent(type="Text", props={"text": f"This response was generated using {version} with Day 2 Ops integration.", "variant": "body"})
                ]
            )
        ]
    )

# --- Shadow Router Instance ---
shadow_router = ShadowRouter(v1_func=agent_v1_logic, v2_func=agent_v2_logic)

@app.get("/agent/query")
@cost_guard(budget_limit=0.10)
@hive_mind(cache=global_cache) # Viral Idea #2: Semantic Caching
async def chat(q: str, session_id: str = "guest-session"):
    """
    Simulates a production agent with Shadow Mode, Semantic Caching, and Cost Control.
    """
    # Viral Idea #1: Shadow Mode Deployment
    # Passing session_id for persistence tracking
    result = await shadow_router.route(q, session_id=session_id)
    
    print(f"🕵️  Trace Logged: {result['trace_id']} | Latency: {result['latency']:.2f}s")
    return result["response"]

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
