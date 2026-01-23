from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import asyncio
from .cost_control import cost_guard, model_router
from .cache.semantic_cache import hive_mind, global_cache
from .shadow.router import ShadowRouter

app = FastAPI(title="Agent Ops Starter Pack")

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
