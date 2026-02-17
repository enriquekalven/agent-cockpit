import os
import subprocess
import google.oauth2.credentials
import vertexai
from vertexai.preview import reasoning_engines
from agent import SuperAgent

# v1.4.7 Sovereign Alignment: Agent Engine (Reasoning Engine) Deployment Script
# Hardened with Gcloud Auth Fallback & Path Correction

def get_gcloud_credentials():
    """Helper to get credentials from gcloud if ADC is expired."""
    try:
        print("🔗 Attempting to retrieve credentials from gcloud...")
        token = subprocess.check_output(['gcloud', 'auth', 'print-access-token']).decode('utf-8').strip()
        return google.oauth2.credentials.Credentials(token)
    except Exception as e:
        print(f"⚠️  Gcloud auth fallback failed: {e}")
        return None

def deploy_to_agent_engine():
    """
    Deploys the SuperAgent to Vertex AI Agent Engine.
    This provides a serverless scaling environment native to Gemini.
    """
    project_id = "YOUR_PROJECT_ID"
    location = "us-central1"
    bucket = "gs://YOUR_PROJECT_ID-agent-engine"
    
    # Try to get credentials from gcloud if possible
    creds = get_gcloud_credentials()
    
    vertexai.init(
        project=project_id, 
        location=location, 
        staging_bucket=bucket,
        credentials=creds
    )

    print("🚀 Initializing Agent Engine Deployment for SuperAgent...")
    
    # Path to the current script's directory to find agent.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    agent_py_path = os.path.join(script_dir, "agent.py")
    
    # 1. Initialize Agent
    agent = SuperAgent(project_id=project_id)
    
    # 2. Trigger Production Deployment
    try:
        remote_agent = reasoning_engines.ReasoningEngine.create(
            agent,
            display_name="Super Agent (Agent Engine)",
            description="ADK Powered High-Fidelity Agent for Laboratory Ops",
            requirements=[
                "google-adk",
                "tenacity",
                "fastapi",
                "uvicorn",
                "pydantic"
            ],
            extra_packages=[agent_py_path]
        )
        print("\n✅ SUCCESS: Deployed to Vertex AI Agent Engine!")
        print(f"🔗 Resource Name: {remote_agent.resource_name}")
        
        # Ensure directory exists for metadata
        metadata_dir = os.path.join(script_dir, ".cockpit")
        os.makedirs(metadata_dir, exist_ok=True)
        with open(os.path.join(metadata_dir, "agent_engine_id.txt"), "w") as f:
            f.write(remote_agent.resource_name)
            
        return remote_agent.resource_name
    except Exception as e:
        print(f"❌ Deployment Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    deploy_to_agent_engine()
