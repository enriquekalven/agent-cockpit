import json
import requests
import google.auth
import google.auth.transport.requests
import subprocess
import os
from tenacity import retry, wait_exponential, stop_after_attempt

def get_gcloud_token():
    try:
        return subprocess.check_output(['gcloud', 'auth', 'print-access-token']).decode('utf-8').strip()
    except Exception:
        return None

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def register_to_ge():
    project_id = "YOUR_PROJECT_ID"
    project_number = "697625214430"
    location = "global"
    collection = "default_collection"
    # From register_to_ge.py
    engine_id = "gemini-enterprise-17647929_1764792982975"
    
    # ADK Agent Engine Resource Name
    agent_engine_id = "projects/697625214430/locations/us-central1/reasoningEngines/6609563517282418688"
    
    token = get_gcloud_token()
    if not token:
        print("❌ Could not get gcloud token. Please authenticate.")
        return

    # Discovery Engine API URL for registering an agent
    url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{project_number}/locations/{location}/collections/{collection}/engines/{engine_id}/assistants/default_assistant/agents"
    
    # Based on agent-starter-pack source code
    payload = {
        "displayName": "Super Agent (Agent Engine Native)",
        "description": "ADK Powered High-Fidelity Agent for Laboratory Ops",
        "icon": {
            "uri": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/smart_toy/default/24px.svg"
        },
        "adk_agent_definition": {
            "provisioned_reasoning_engine": {
                "reasoning_engine": agent_engine_id
            }
        }
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "x-goog-user-project": project_id
    }
    
    print(f"📡 Registering Native ADK Agent to Gemini Enterprise...")
    print(f"🔗 Agent Engine: {agent_engine_id}")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        print("✅ Successfully registered to Gemini Enterprise via Agent Engine Native route!")
        print(json.dumps(response.json(), indent=2))
    elif response.status_code == 409:
        print("⚠️ Agent already exists in this engine. Native registration complete.")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    register_to_ge()
