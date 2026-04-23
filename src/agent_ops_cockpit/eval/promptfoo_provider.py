import os
import sys
import asyncio
import importlib.util
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

def call_api(prompt, options, context):
    # Get agent path from env var
    agent_path = os.environ.get("COCKPIT_AGENT_PATH", "agent.py")
    
    if not os.path.exists(agent_path):
        return {"error": f"Agent path {agent_path} not found"}
        
    # Add agent path directory to sys.path
    agent_dir = os.path.dirname(os.path.abspath(agent_path))
    if agent_dir not in sys.path:
        sys.path.insert(0, agent_dir)
        
    try:
        # Load the module
        spec = importlib.util.spec_from_file_location("agent_module", agent_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find the agent or app
        agent = None
        from google.adk.agents import Agent
        
        for name, obj in module.__dict__.items():
            if isinstance(obj, Agent):
                agent = obj
                break
                
        if not agent:
            return {"error": "No Agent instance found in module"}
            
        # Run the agent asynchronously
        async def run():
            session_service = InMemorySessionService()
            await session_service.create_session(
                app_name="app", user_id="user", session_id="session"
            )
            runner = Runner(agent=agent, app_name="app", session_service=session_service)

            output = ""
            async for event in runner.run_async(
                user_id="user",
                session_id="session",
                new_message=genai_types.Content(
                    role="user",
                    parts=[genai_types.Part.from_text(text=prompt)]
                ),
            ):
                if event.is_final_response():
                    output = event.content.parts[0].text
                    
            return output

        output = asyncio.run(run())
        return {"output": output}
        
    except Exception as e:
        return {"error": str(e)}
