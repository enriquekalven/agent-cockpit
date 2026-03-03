import logging

from agent_ops_cockpit.integrations.langchain import CockpitCallbackHandler

# Configure logging to see cockpit warnings
logging.basicConfig(level=logging.INFO)

def test_governance_simulation():
    print("🚀 Starting Sovereign Governance Simulation (v2.0.4)\n")
    
    # 1. Initialize the Cockpit Handler
    cockpit = CockpitCallbackHandler(app_name="langchain-test-agent")
    
    # 2. Simulate LLM Start with PII and a Large Prompt
    print("--- Phase 1: LLM Start Audit ---")
    prompts = [
        "Hello, my email is secret-dev@example.com and my credit card is 4111-1111-1111-1111.",
        "Very long prompt ... " * 500  # Simulate > 5000 chars
    ]
    
    cockpit.on_llm_start(serialized={}, prompts=prompts)
    
    # 3. Simulate High-Risk Tool Call
    print("\n--- Phase 2: Tool Execution Audit ---")
    tool_data = {"name": "delete_user_table"}
    cockpit.on_tool_start(serialized=tool_data, input_str="DROP TABLE users;")
    
    # 4. Simulate Chain End (Finalize and Sink to Evidence Lake)
    print("\n--- Phase 3: Evidence Lake Sink ---")
    cockpit.on_chain_end(outputs={"result": "Cleanup complete"})
    
    print("\n✅ Simulation Complete. Results stored in .cockpit/evidence_lake.json")
    
    # Show findings
    import json
    import os
    if os.path.exists(".cockpit/evidence_lake.json"):
        with open(".cockpit/evidence_lake.json", "r") as f:
            data = json.load(f)
            print("\n📊 EVIDENCE LAKE PREVIEW:")
            print(json.dumps(data[-1], indent=2))

if __name__ == "__main__":
    test_governance_simulation()
