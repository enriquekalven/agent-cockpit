"""
distinguished_architect.py
SME Persona: Principal Architect Fellow
Objective: Demonstates ADK-native tool consumption of the Cockpit MCP Hub.
"""
import asyncio

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types


# v2.0.2: Programmatic Tool Definition for ADK
def cockpit_audit_tool(path: str) -> dict:
    """
    Invokes the AgentOps Cockpit to perform a Deep Architecture and Security audit.
    
    Args:
        path: The absolute path to the agent directory to audit.
        
    Returns:
        dict: The audit status and high-level findings summary.
    """
    # Logic to call the CockpitOrchestrator programmatically
    from agent_ops_cockpit.ops import orchestrator as orch_mod
    exit_code = orch_mod.run_audit(mode='deep', target_path=path)
    return {
        "status": "SUCCESS" if exit_code == 0 else "FINDINGS_DETECTED",
        "message": "Audit completed. Review .cockpit/ directory for full implementation plan."
    }

def shadow_roi_tool(path: str) -> dict:
    """
    Performs interactive ROI benchmarking to find the optimal model tier for an agent.
    
    Args:
        path: The directory path containing the agent(s) to benchmark.
        
    Returns:
        dict: Performance data comparing Flash vs Pro vs Lite tiers.
    """
    from agent_ops_cockpit.ops.benchmarker import ReliabilityBenchmarker
    bench = ReliabilityBenchmarker(path)
    # Using the async benchmark logic
    data = asyncio.run(bench.shadow_benchmark_roi())
    return {"status": "SUCCESS", "benchmark_data": data}

# Define the Distinguished Architect Agent
architect_agent = Agent(
    name="distinguished_architect",
    model="gemini-2.0-flash",
    instruction="""
    You are a Distinguished Architect Fellow at a major cloud provider.
    Your mission is to ensure every agent in the fleet follows the Google Well-Architected Framework.
    
    Capabilities:
    1. Audit code: Use 'cockpit_audit_tool' to run deep scans for Security, FinOps, and Strategy.
    2. Optimize costs: Use 'shadow_roi_tool' to find the best model configuration.
    
    When a user provides a path, you MUST audit it and provide a strategic executive digest.
    If costs are a concern, suggest a Shadow ROI benchmark.
    """,
    tools=[cockpit_audit_tool, shadow_roi_tool]
)

async def main():
    # Setup session
    session_service = InMemorySessionService()
    await session_service.create_session("architect_app", "admin_user", "session_001")
    
    runner = Runner(agent=architect_agent, app_name="architect_app", session_service=session_service)
    
    query = "I have a new agent at './src/agent_ops_cockpit'. Please audit it and tell me if I should use Gemini 1.5 Pro or Flash."
    
    print(f"🚀 User: {query}")
    print("---")
    
    async for event in runner.run_async(
        user_id="admin_user",
        session_id="session_001",
        new_message=genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=query)]
        )
    ):
        if event.is_final_response():
            print(f"🤖 Architect: {event.content.parts[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
