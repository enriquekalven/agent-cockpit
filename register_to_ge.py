import json
import requests
import google.auth
import google.auth.transport.requests
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def register():
    project_id = "YOUR_PROJECT_ID"
    location = "global"
    collection = "default_collection"
    engine_id = "gemini-enterprise-17647929_1764792982975"
    project_number = "697625214430"
    
    # Get credentials
    credentials, _ = google.auth.default()
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)
    
    url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{project_number}/locations/{location}/collections/{collection}/engines/{engine_id}/assistants/default_assistant/agents"
    
    agent_card_data = {
        "protocolVersions": ["1.0"],
        "id": "my-super-agent",
        "name": "Super Agent (ADK)",
        "description": "High-fidelity AI agent for solving complex laboratory and operations tasks.",
        "capabilities": {"streaming": False, "conversational": True},
        "skills": [
            {
                "name": "solve_task",
                "description": "Processes a natural language prompt and returns a reasoned response.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "The task description."}
                    },
                    "required": ["text"]
                }
            }
        ],
        "endpoints": {
            "task": "https://my-super-agent-697625214430.us-central1.run.app/chat",
            "status": "https://my-super-agent-697625214430.us-central1.run.app/health",
            "card": "https://my-super-agent-697625214430.us-central1.run.app/.well-known/agent-card.json"
        }
    }
    
    payload = {
        "displayName": "Super Agent (ADK)",
        "description": "High-fidelity AI agent for solving complex laboratory and operations tasks.",
        "icon": {
            "uri": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/smart_toy/default/24px.svg"
        },
        "a2aAgentDefinition": {
            "jsonAgentCard": json.dumps(agent_card_data)
        }
    }
    
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json",
        "x-goog-user-project": project_id
    }
    
    print(f"📡 Registering Super Agent to Gemini Enterprise Engine: {engine_id}...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        print("✅ Successfully registered to Gemini Enterprise!")
        print(json.dumps(response.json(), indent=2))
    elif response.status_code == 409:
        print("⚠️ Agent already exists. Attempting to update...")
        # Get the existing agent name
        # In Discovery Engine, agents are usually listed or you can try to get them
        # For simplicity, if it's 409, we know it's there.
        print("Agent is already registered in this engine.")
    else:
        print(f"❌ Registration failed with status {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    register()
