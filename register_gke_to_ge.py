import os
import subprocess
import json
import requests
import google.auth
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def register():
    project_id = "YOUR_PROJECT_ID"
    location = "global"
    collection = "default_collection"
    engine_id = "gemini-enterprise-17647929_1764792982975"
    project_number = "697625214430"
    gke_ip = "34.135.249.104"
    
    # Try to get token from gcloud
    try:
        token = subprocess.check_output(['gcloud', 'auth', 'print-access-token']).decode('utf-8').strip()
        print("🔗 Using gcloud access token for registration...")
    except Exception as e:
        print(f"❌ Failed to get gcloud token: {e}")
        return
    
    url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{project_number}/locations/{location}/collections/{collection}/engines/{engine_id}/assistants/default_assistant/agents"
    
    agent_card_data = {
        "protocolVersion": "1.0",
        "id": "my-super-agent-gke",
        "version": "1.4.7",
        "url": f"http://{gke_ip}/",
        "name": "Super Agent (GKE Sovereignty)",
        "description": "High-fidelity AI agent running on GKE Autopilot with full sovereignty.",
        "capabilities": {"streaming": False, "conversational": True},
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": [
            {
                "id": "solve_task",
                "name": "solve_task",
                "tags": [],
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
            "task": f"http://{gke_ip}/chat",
            "status": f"http://{gke_ip}/health",
            "card": f"http://{gke_ip}/.well-known/agent-card.json"
        }
    }
    
    # Discovery Engine payload
    payload = {
        "displayName": "Super Agent (GKE Sovereignty)",
        "description": "High-fidelity AI agent running on GKE Autopilot with full sovereignty.",
        "icon": {
            "uri": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/hub/default/24px.svg"
        },
        "a2aAgentDefinition": {
            "jsonAgentCard": json.dumps(agent_card_data)
        }
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "x-goog-user-project": project_id
    }
    
    print(f"📡 Registering GKE Super Agent to Gemini Enterprise Engine: {engine_id}...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        print("✅ Successfully registered GKE Agent to Gemini Enterprise!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Registration failed with status {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    register()
