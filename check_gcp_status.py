import vertexai
from vertexai.preview import reasoning_engines
from google.cloud import storage

project_id = "YOUR_PROJECT_ID"
location = "us-central1"

vertexai.init(project=project_id, location=location)

def check_status():
    print(f"Checking status for project: {project_id}")
    
    # 1. Check Buckets
    storage_client = storage.Client(project=project_id)
    buckets = list(storage_client.list_buckets())
    print("\nBuckets:")
    for b in buckets:
        print(f" - {b.name}")
    
    # 2. Check Reasoning Engines
    print("\nReasoning Engines:")
    try:
        engines = reasoning_engines.ReasoningEngine.list()
        for e in engines:
            print(f" - {e.display_name} ({e.resource_name})")
    except Exception as e:
        print(f"Error listing reasoning engines: {e}")

if __name__ == "__main__":
    check_status()
