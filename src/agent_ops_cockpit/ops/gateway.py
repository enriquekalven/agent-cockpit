import os

import uvicorn
import yaml
from fastapi import FastAPI, HTTPException, Request
from google.genai import Client, types
from google.genai.errors import APIError

from agent_ops_cockpit.config import config
from agent_ops_cockpit.ops.guardrails import SafetyGate
from agent_ops_cockpit.telemetry import telemetry

app = FastAPI(title="Cockpit Gateway Sidecar", version=config.VERSION)

# Global Governance Policy
POLICY_PATH = os.path.join(os.getcwd(), "governance.yaml")


def load_policy():
    if os.path.exists(POLICY_PATH):
        try:
            with open(POLICY_PATH, "r") as f:
                return yaml.safe_load(f)
        except Exception:
            pass
    return {}


@app.on_event("startup")
async def startup_event():
    print(f"🛡️  Cockpit Gateway Sidecar v{config.VERSION} is initializing...")
    print(f"📄 Governance Policy: {POLICY_PATH}")


@app.post("/v1/chat/completions")
async def chat_proxy(request: Request):
    """
    Cockpit Proxy: OpenAI-Compatible Gateway.
    Handles PII Scrubbing, Cost Routing, Real-time Policy Enforcement,
    and forwards live requests to Gemini via Google GenAI SDK.
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body.")

    messages = body.get("messages", [])
    if not messages:
        raise HTTPException(
            status_code=400, detail="No messages provided in request."
        )

    # 1. PII Scrubbing (Shift-Left Security via SafetyGate)
    for msg in messages:
        if "content" in msg and isinstance(msg["content"], str):
            msg["content"] = SafetyGate.sanitize(msg["content"], mode="pii")

    # 2. Policy Enforcement (Governance as Code)
    policy = load_policy()
    forbidden = policy.get("forbidden_topics", [])
    for msg in messages:
        content = msg.get("content", "").lower()
        for topic in forbidden:
            if topic and str(topic).lower() in content:
                telemetry.track_event_sync(
                    "policy_violation", {"topic": topic, "action": "blocked"}
                )
                raise HTTPException(
                    status_code=403,
                    detail=f"🛡️ [Cockpitty Breach] Content violates policy: {topic}",
                )

    # Validate overall prompt integrity against injection patterns
    full_text = "\n".join(
        [
            m.get("content", "")
            for m in messages
            if isinstance(m.get("content"), str)
        ]
    )
    if not SafetyGate.validate_prompt(full_text):
        raise HTTPException(
            status_code=403,
            detail="🛡️ [Cockpitty Breach] Prompt violates safety injection patterns.",
        )

    # 3. Model Translation & Cost Routing (FinOps)
    openai_model = body.get("model", "gemini-2.0-flash")
    target_model = "gemini-2.0-flash"  # Default highly-efficient baseline

    if "gemini-2.5" in openai_model:
        target_model = openai_model
    elif "pro" in openai_model.lower():
        # Map Pro requests appropriately or stick to Flash for cost bounds
        target_model = "gemini-2.0-flash"

    telemetry.track_event_sync(
        "gateway_call", {"model": target_model, "original": openai_model}
    )
    print(f"🚀 [Gateway] Routing cleaned request to: {target_model}")

    # 4. Payload Translation (OpenAI -> Gemini)
    system_instruction = None
    contents = []

    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")

        if role == "system":
            system_instruction = content
        else:
            gemini_role = "model" if role in ["assistant", "model"] else "user"
            contents.append(
                types.Content(
                    role=gemini_role, parts=[types.Part.from_text(text=content)]
                )
            )

    # 5. Google GenAI Execution (Live with Mock/Simulation Fallback)
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    is_vertex = (
        os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() == "true"
    )
    force_mock = os.getenv(
        "COCKPIT_MOCK_GATEWAY", "false"
    ).lower() == "true" or (not api_key and not is_vertex)

    if force_mock:
        print(
            "⚠️  [Gateway] No API Key found or MOCK enabled. Returning simulated pass-through response."
        )
        import time

        return {
            "id": f"cockpit-chat-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": target_model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "This response was routed and cleaned by the Cockpit Gateway Sidecar.",
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 10,
                "total_tokens": 20,
            },
        }

    try:
        # Initialize Google GenAI Client
        # Implicitly loads GOOGLE_API_KEY or GOOGLE_GENAI_USE_VERTEXAI from environment
        client = Client()

        gen_config = types.GenerateContentConfig()
        if system_instruction:
            gen_config.system_instruction = system_instruction

        # Support optional generation parameters passed from OpenAI payload
        if "temperature" in body:
            gen_config.temperature = float(body["temperature"])
        if "max_tokens" in body:
            gen_config.max_output_tokens = int(body["max_tokens"])

        response = client.models.generate_content(
            model=target_model, contents=contents, config=gen_config
        )

        response_text = response.text if hasattr(response, "text") else ""

        # Extract usage metrics safely
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            prompt_tokens = response.usage_metadata.prompt_token_count or 0
            completion_tokens = (
                response.usage_metadata.candidates_token_count or 0
            )
            total_tokens = response.usage_metadata.total_token_count or 0

        # Translate back to OpenAI-compatible Chat Completions format
        import time

        return {
            "id": f"cockpit-chat-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": target_model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": response_text},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
            },
        }

    except APIError as e:
        print(f"❌ [Gateway] Gemini API Error: {e}")
        raise HTTPException(
            status_code=502, detail=f"Gemini API Gateway Error: {str(e)}"
        )
    except Exception as e:
        print(f"❌ [Gateway] Unexpected Execution Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Internal Gateway Error: {str(e)}"
        )


def start_gateway(port: int = 8000):
    uvicorn.run(app, host="127.0.0.1", port=port)


if __name__ == "__main__":
    start_gateway()
