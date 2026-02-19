from fastapi import FastAPI, Request, HTTPException
import uvicorn
import yaml
import os
from agent_ops_cockpit.ops.guardrails import CockpitGuardrails
from agent_ops_cockpit.telemetry import telemetry

app = FastAPI(title="Sovereign Gateway Sidecar", version="2.0.2")
guardrails = CockpitGuardrails()

# Global Governance Policy
POLICY_PATH = os.path.join(os.getcwd(), 'governance.yaml')

def load_policy():
    if os.path.exists(POLICY_PATH):
        with open(POLICY_PATH, 'r') as f:
            return yaml.safe_load(f)
    return {}

@app.on_event("startup")
async def startup_event():
    print("🛡️  Sovereign Gateway Sidecar is initializing...")
    print(f"📄 Governance Policy: {POLICY_PATH}")

@app.post("/v1/chat/completions")
async def chat_proxy(request: Request):
    """
    Sovereign Proxy: OpenAI-Compatible Gateway.
    Handles PII Scrubbing, Cost Routing, and Real-time Policy Enforcement.
    """
    body = await request.json()
    messages = body.get('messages', [])
    
    # 1. PII Scrubbing (Shift-Left Security)
    for msg in messages:
        if 'content' in msg:
            msg['content'] = guardrails.scrub_pii(msg['content'])
            
    # 2. Policy Enforcement (GaC)
    policy = load_policy()
    forbidden = policy.get('forbidden_topics', [])
    for msg in messages:
        content = msg.get('content', '').lower()
        for topic in forbidden:
            if topic.lower() in content:
                telemetry.track_event_sync("policy_violation", {"topic": topic, "action": "blocked"})
                raise HTTPException(status_code=403, detail=f"🛡️ [Sovereignty Breach] Content violates policy: {topic}")

    # 3. Cost Routing (FinOps)
    # Default to Gemini Flash if not specified or for efficiency
    target_model = body.get('model', 'gemini-2.0-flash')
    
    # In a real scenario, we'd forward to Vertex/OpenAI here
    # For v2.0.2, we simulate the 'Sovereign Pass-through'
    print(f"🚀 Forwarding cleaned request to target: {target_model}")
    
    # Track metrics
    telemetry.track_event_sync("gateway_call", {"model": target_model})
    
    return {
        "id": "sovereign-chat-123",
        "object": "chat.completion",
        "created": 123456789,
        "model": target_model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "This response was routed and cleaned by the Sovereign Gateway Sidecar."
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 10,
            "total_tokens": 20
        }
    }

def start_gateway(port: int = 8000):
    uvicorn.run(app, host="127.0.0.1", port=port)

if __name__ == "__main__":
    start_gateway()
