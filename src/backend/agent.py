from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import asyncio
from .cost_control import cost_guard, model_router
from .cache.semantic_cache import hive_mind, global_cache
from .shadow.router import ShadowRouter
from .ops.mcp_hub import global_mcp_hub

app = FastAPI(title="Optimized Agent Stack")

class A2UIComponent(BaseModel):
    type: str
    props: dict
    children: Optional[List['A2UIComponent']] = None

class A2UISurface(BaseModel):
    surfaceId: str
    content: List[A2UIComponent]

# --- Core Intelligence Logic ---

async def agent_v1_logic(query: str, context: dict = None) -> A2UISurface:
    """Production Agent (v1) - Reliable & Fast."""
    # Simulate MCP tool usage
    if "search" in query.lower():
        await global_mcp_hub.execute_tool("search", {"q": query})
    return generate_dashboard(query, version="v1-stable")

async def agent_v2_logic(query: str, context: dict = None) -> A2UISurface:
    """Experimental Agent (v2) - High Reasoning/Shadow Mode."""
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
async def chat(q: str):
    """
    Simulates a production agent with Shadow Mode, Semantic Caching, and Cost Control.
    """
    # Viral Idea #1: Shadow Mode Deployment
    # This calls Production and Shadow in parallel, logging comparisons.
    result = await shadow_router.route(q)
    
    print(f"🕵️  Trace Logged: {result['trace_id']} | Latency: {result['latency']:.2f}s")
    return result["response"]

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
